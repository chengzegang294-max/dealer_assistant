from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import MetaTrader5 as mt5
import numpy as np
import pandas as pd

from backtest_p0 import Config, Params, atr, compute_trend_flags, ema, load_ohlcv_1h, resample_ohlcv

_E1_CCI144_VETO_ENABLED = True
_E1_ADX_SCORE_ENABLED = False
_E2_CHASE_MAX_ATR: Optional[float] = None
_E2_CHASE_ACTION = "off"
_LIQUIDITY_GATE_ENABLED = False
_LIQUIDITY_MAX_SPREAD_REL = 0.15
_VOL_RISK_VOL_RATIO_MAX: Optional[float] = None
_VOL_RISK_VOL_PCT_MAX: Optional[float] = None
_VOL_RISK_ACTION = "off"
_ENTRY_SCORE_MAX: Optional[float] = None
_ENTRY_SCORE_ACTION = "off"
_ENTRY_SCORE_SCOPE = "all"
_ENTRY_SCORE_VOL_MODE = "off"
_ENTRY_SCORE_VOL_ATR_REL_CUTS: Optional[Tuple[float, float]] = None
_ENTRY_SCORE_VOL_MAXES: Optional[Tuple[float, float, float]] = None


def _cross_up(a: pd.Series, b: pd.Series) -> pd.Series:
    a0 = pd.Series(pd.to_numeric(a, errors="coerce"), index=a.index)
    b0 = pd.Series(pd.to_numeric(b, errors="coerce"), index=b.index)
    return (a0 > b0) & (a0.shift(1) <= b0.shift(1))


def _cross_down(a: pd.Series, b: pd.Series) -> pd.Series:
    a0 = pd.Series(pd.to_numeric(a, errors="coerce"), index=a.index)
    b0 = pd.Series(pd.to_numeric(b, errors="coerce"), index=b.index)
    return (a0 < b0) & (a0.shift(1) >= b0.shift(1))


def _zrf_macd_from_close(close: pd.Series) -> pd.DataFrame:
    close = pd.to_numeric(close, errors="coerce")
    xun = 8
    kuai = 13
    zhong = 21
    jie = 144
    diff = ema(close, kuai) - ema(close, zhong)
    dea = ema(diff, xun)
    watershed = ema(diff.abs(), jie)
    m_min = pd.concat([diff, dea], axis=1).min(axis=1)
    m_max = pd.concat([diff, dea], axis=1).max(axis=1)
    cross_up = _cross_up(diff, dea)
    cross_down = _cross_down(diff, dea)

    idx = np.arange(len(close), dtype=float)
    last_up_shifted = pd.Series(np.where(cross_up.shift(1).fillna(False).to_numpy(), idx, np.nan)).ffill().to_numpy()
    prev_up_idx = last_up_shifted - 1
    prev_up_valid = np.isfinite(prev_up_idx) & (prev_up_idx >= 0)
    prev_up_i = np.full(len(prev_up_idx), -1, dtype=int)
    if bool(np.any(prev_up_valid)):
        prev_up_i[prev_up_valid] = prev_up_idx[prev_up_valid].astype(int)

    last_dn_shifted = pd.Series(np.where(cross_down.shift(1).fillna(False).to_numpy(), idx, np.nan)).ffill().to_numpy()
    prev_dn_idx = last_dn_shifted - 1
    prev_dn_valid = np.isfinite(prev_dn_idx) & (prev_dn_idx >= 0)
    prev_dn_i = np.full(len(prev_dn_idx), -1, dtype=int)
    if bool(np.any(prev_dn_valid)):
        prev_dn_i[prev_dn_valid] = prev_dn_idx[prev_dn_valid].astype(int)

    diff_arr = diff.to_numpy(dtype=float)
    close_arr = close.to_numpy(dtype=float)
    diff_prev_up = np.where(prev_up_valid, diff_arr[prev_up_i], np.nan)
    close_prev_up = np.where(prev_up_valid, close_arr[prev_up_i], np.nan)
    diff_prev_dn = np.where(prev_dn_valid, diff_arr[prev_dn_i], np.nan)
    close_prev_dn = np.where(prev_dn_valid, close_arr[prev_dn_i], np.nan)

    m_bull_div = cross_up & (m_max < 0) & (diff > diff_prev_up) & (close < close_prev_up)
    m_bear_div = cross_down & (m_min > 0) & (diff < diff_prev_dn) & (close > close_prev_dn)

    low_kc = (diff < (-1.96 * watershed)) & cross_up
    high_dc = (diff > (1.96 * watershed)) & cross_down

    zb_start = (diff < (-1.0 * watershed)) & cross_up & (m_max < 0)
    za_start = (diff > (1.0 * watershed)) & cross_down & (m_min > 0)

    zb_buyin = np.zeros(len(close), dtype=bool)
    zb_2nd = np.zeros(len(close), dtype=bool)
    za_sellout = np.zeros(len(close), dtype=bool)
    za_2nd = np.zeros(len(close), dtype=bool)

    last_zb = None
    zb_pos_count = 0
    zb_buy_count = 0
    zb_diff0 = np.nan

    last_za = None
    za_neg_count = 0
    za_sell_count = 0
    za_diff0 = np.nan

    m_max_arr = m_max.to_numpy(dtype=float)
    m_min_arr = m_min.to_numpy(dtype=float)
    cross_up_arr = cross_up.to_numpy(dtype=bool)
    cross_down_arr = cross_down.to_numpy(dtype=bool)
    watershed_arr = watershed.to_numpy(dtype=float)

    for i in range(len(close)):
        if bool(zb_start.iloc[i]) and np.isfinite(watershed_arr[i]):
            last_zb = i
            zb_pos_count = 0
            zb_buy_count = 0
            zb_diff0 = diff_arr[i]
        if last_zb is not None:
            if np.isfinite(m_max_arr[i]) and m_max_arr[i] > 0:
                zb_pos_count += 1
            is_buy = bool(cross_up_arr[i]) and np.isfinite(m_max_arr[i]) and (m_max_arr[i] < 0)
            zb_buyin[i] = bool(is_buy and (zb_pos_count == 0) and np.isfinite(zb_diff0) and np.isfinite(diff_arr[i]) and (diff_arr[i] > zb_diff0))
            if zb_buyin[i]:
                zb_buy_count += 1
                zb_2nd[i] = zb_buy_count == 1

        if bool(za_start.iloc[i]) and np.isfinite(watershed_arr[i]):
            last_za = i
            za_neg_count = 0
            za_sell_count = 0
            za_diff0 = diff_arr[i]
        if last_za is not None:
            if np.isfinite(m_min_arr[i]) and m_min_arr[i] < 0:
                za_neg_count += 1
            is_sell = bool(cross_down_arr[i]) and np.isfinite(m_min_arr[i]) and (m_min_arr[i] > 0)
            za_sellout[i] = bool(is_sell and (za_neg_count == 0) and np.isfinite(za_diff0) and np.isfinite(diff_arr[i]) and (diff_arr[i] < za_diff0))
            if za_sellout[i]:
                za_sell_count += 1
                za_2nd[i] = za_sell_count == 1

    out = pd.DataFrame(
        {
            "zrf_diff": diff,
            "zrf_dea": dea,
            "zrf_watershed": watershed,
            "zrf_m_bull_div": m_bull_div.astype(bool),
            "zrf_m_bear_div": m_bear_div.astype(bool),
            "zrf_low_kc": low_kc.astype(bool),
            "zrf_high_dc": high_dc.astype(bool),
            "zrf_zb_buyin": pd.Series(zb_buyin, index=close.index),
            "zrf_zb_2nd_kc": pd.Series(zb_2nd, index=close.index),
            "zrf_za_sellout": pd.Series(za_sellout, index=close.index),
            "zrf_za_2nd_dc": pd.Series(za_2nd, index=close.index),
        },
        index=close.index,
    )
    return out


def _cci_from_ohlc(high: pd.Series, low: pd.Series, close: pd.Series, n: int) -> pd.Series:
    hi = pd.to_numeric(high, errors="coerce")
    lo = pd.to_numeric(low, errors="coerce")
    cl = pd.to_numeric(close, errors="coerce")
    tp = (hi + lo + cl) / 3.0
    ma = tp.rolling(int(n), min_periods=int(n)).mean()
    dev = (tp - ma).abs().rolling(int(n), min_periods=int(n)).mean()
    denom = 0.015 * dev.replace(0.0, np.nan)
    return (tp - ma) / denom


def _adx_from_ohlc(high: pd.Series, low: pd.Series, close: pd.Series, n: int) -> pd.DataFrame:
    hi = pd.to_numeric(high, errors="coerce")
    lo = pd.to_numeric(low, errors="coerce")
    cl = pd.to_numeric(close, errors="coerce")
    prev_hi = hi.shift(1)
    prev_lo = lo.shift(1)
    prev_cl = cl.shift(1)

    up_move = hi - prev_hi
    down_move = prev_lo - lo
    plus_dm = pd.Series(np.where((up_move > down_move) & (up_move > 0), up_move, 0.0), index=hi.index)
    minus_dm = pd.Series(np.where((down_move > up_move) & (down_move > 0), down_move, 0.0), index=hi.index)

    tr = pd.concat([(hi - lo).abs(), (hi - prev_cl).abs(), (lo - prev_cl).abs()], axis=1).max(axis=1)

    alpha = 1.0 / float(n)
    tr_rma = tr.ewm(alpha=alpha, adjust=False, min_periods=int(n)).mean()
    plus_rma = plus_dm.ewm(alpha=alpha, adjust=False, min_periods=int(n)).mean()
    minus_rma = minus_dm.ewm(alpha=alpha, adjust=False, min_periods=int(n)).mean()

    plus_di = 100.0 * (plus_rma / tr_rma.replace(0.0, np.nan))
    minus_di = 100.0 * (minus_rma / tr_rma.replace(0.0, np.nan))
    dx = 100.0 * ((plus_di - minus_di).abs() / (plus_di + minus_di).replace(0.0, np.nan))
    adx = dx.ewm(alpha=alpha, adjust=False, min_periods=int(n)).mean()

    return pd.DataFrame({"adx": adx, "plus_di": plus_di, "minus_di": minus_di})


def _stoch_kdj_from_ohlc(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    n: int = 9,
    k_n: int = 3,
    d_n: int = 3,
) -> pd.DataFrame:
    hi = pd.to_numeric(high, errors="coerce")
    lo = pd.to_numeric(low, errors="coerce")
    cl = pd.to_numeric(close, errors="coerce")
    ll = lo.rolling(int(n), min_periods=int(n)).min()
    hh = hi.rolling(int(n), min_periods=int(n)).max()
    rsv = 100.0 * ((cl - ll) / (hh - ll).replace(0.0, np.nan))
    k = rsv.ewm(alpha=1.0 / float(k_n), adjust=False, min_periods=int(n)).mean()
    d = k.ewm(alpha=1.0 / float(d_n), adjust=False, min_periods=int(n)).mean()
    j = 3.0 * k - 2.0 * d
    return pd.DataFrame({"k": k, "d": d, "j": j})


def _sr_nearest_levels(
    high_arr: np.ndarray,
    low_arr: np.ndarray,
    close_px: float,
    atr_px: float,
    i: int,
    lookback: int = 200,
    pivot: int = 3,
    cluster_atr: float = 0.25,
) -> Tuple[float, float, float, float, int, int]:
    n = int(len(high_arr))
    i = int(i)
    if n <= 0 or i < 0 or i >= n:
        return (float("nan"), float("nan"), float("nan"), float("nan"), 0, 0)
    if not np.isfinite(close_px):
        return (float("nan"), float("nan"), float("nan"), float("nan"), 0, 0)
    if not (np.isfinite(atr_px) and float(atr_px) > 0):
        atr_px = float("nan")
    lb = int(max(20, lookback))
    start = max(0, i - lb + 1)
    hi = np.asarray(high_arr[start : i + 1], dtype=float)
    lo = np.asarray(low_arr[start : i + 1], dtype=float)
    if len(hi) < int(pivot * 2 + 5) or len(lo) < int(pivot * 2 + 5):
        return (float("nan"), float("nan"), float("nan"), float("nan"), 0, 0)
    p = int(max(2, pivot))
    piv_hi: List[float] = []
    piv_lo: List[float] = []
    for j in range(p, len(hi) - p):
        xh = float(hi[j])
        xl = float(lo[j])
        if np.isfinite(xh):
            w = hi[j - p : j + p + 1]
            if np.isfinite(w).any() and xh >= float(np.nanmax(w)):
                piv_hi.append(xh)
        if np.isfinite(xl):
            w = lo[j - p : j + p + 1]
            if np.isfinite(w).any() and xl <= float(np.nanmin(w)):
                piv_lo.append(xl)
    if (not piv_hi) and (not piv_lo):
        return (float("nan"), float("nan"), float("nan"), float("nan"), 0, 0)
    tol = float(cluster_atr) * float(atr_px) if np.isfinite(atr_px) else float(abs(close_px) * 0.002)
    if not (np.isfinite(tol) and tol > 0):
        tol = float(abs(close_px) * 0.002)

    def _cluster(levels: List[float]) -> List[Tuple[float, int]]:
        xs = [float(x) for x in levels if np.isfinite(x)]
        xs.sort()
        out: List[Tuple[float, int]] = []
        cur: List[float] = []
        for x in xs:
            if not cur:
                cur = [x]
                continue
            if abs(float(x) - float(cur[-1])) <= tol:
                cur.append(x)
            else:
                out.append((float(np.mean(cur)), int(len(cur))))
                cur = [x]
        if cur:
            out.append((float(np.mean(cur)), int(len(cur))))
        return out

    hi_lv = _cluster(piv_hi)
    lo_lv = _cluster(piv_lo)
    support = float("nan")
    resistance = float("nan")
    sup_t = 0
    res_t = 0
    below = [(lv, t) for (lv, t) in lo_lv if float(lv) <= float(close_px)]
    above = [(lv, t) for (lv, t) in hi_lv if float(lv) >= float(close_px)]
    if below:
        below.sort(key=lambda z: (abs(float(close_px) - float(z[0])), -int(z[1])))
        support, sup_t = float(below[0][0]), int(below[0][1])
    if above:
        above.sort(key=lambda z: (abs(float(z[0]) - float(close_px)), -int(z[1])))
        resistance, res_t = float(above[0][0]), int(above[0][1])
    sup_dist = float(abs(float(close_px) - float(support)) / float(atr_px)) if (np.isfinite(support) and np.isfinite(atr_px) and atr_px > 0) else float("nan")
    res_dist = float(abs(float(resistance) - float(close_px)) / float(atr_px)) if (np.isfinite(resistance) and np.isfinite(atr_px) and atr_px > 0) else float("nan")
    return (support, resistance, sup_dist, res_dist, sup_t, res_t)


def _jinding_features(df1: pd.DataFrame) -> pd.DataFrame:
    close = pd.to_numeric(df1.get("close", np.nan), errors="coerce")
    high = pd.to_numeric(df1.get("high", np.nan), errors="coerce")
    low = pd.to_numeric(df1.get("low", np.nan), errors="coerce")
    open_ = pd.to_numeric(df1.get("open", np.nan), errors="coerce")
    atr_ = pd.to_numeric(df1.get("atr", np.nan), errors="coerce")

    ma13 = close.rolling(13, min_periods=13).mean()
    ma55 = close.rolling(55, min_periods=55).mean()
    ma160 = close.rolling(160, min_periods=160).mean()
    ma120 = close.rolling(120, min_periods=120).mean()
    ma60 = close.rolling(60, min_periods=60).mean()
    ma25 = close.rolling(25, min_periods=25).mean()

    ema20 = ema(close, 20)
    ema27 = ema(close, 27)
    ema29 = ema(close, 29)
    ema32 = ema(close, 32)
    ema36 = ema(close, 36)

    ma30 = close.rolling(30, min_periods=30).mean()
    ma72 = close.rolling(72, min_periods=72).mean()
    pivot_mid = (ma30 + ma72) / 2.0
    b3 = pivot_mid * 0.97
    s3 = pivot_mid * 1.03
    b5 = pivot_mid * 0.95
    s5 = pivot_mid * 1.05
    s7 = pivot_mid * 1.07

    hhv21 = high.rolling(21, min_periods=21).max()
    llv21 = low.rolling(21, min_periods=21).min()
    den21 = (hhv21 - llv21).replace(0.0, np.nan)
    var2 = 100.0 - (90.0 * (hhv21 - close) / den21)
    var1 = var2

    hhv6 = high.rolling(6, min_periods=6).max()
    llv6 = low.rolling(6, min_periods=6).min()
    den6 = (hhv6 - llv6).replace(0.0, np.nan)
    x6 = 100.0 * (hhv6 - close) / den6
    var3 = 100.0 - x6.rolling(34, min_periods=34).mean()
    var3_ma6 = var3.rolling(6, min_periods=6).mean()

    bar_yellow = (var2 < var3_ma6).astype(bool)
    bar_red = (var2 > var3_ma6).astype(bool)
    bar_yellow_prev = bar_yellow.shift(1).fillna(False).astype(bool)
    bar_red_prev = bar_red.shift(1).fillna(False).astype(bool)
    flip_to_yellow = (bar_yellow & bar_red_prev).astype(bool)
    flip_to_red = (bar_red & bar_yellow_prev).astype(bool)

    diff = ema(close, 12) - ema(close, 26)
    dea = ema(diff, 9)
    macd = 2.0 * (diff - dea)

    llv3 = low.rolling(3, min_periods=3).min()
    hhv4 = high.rolling(4, min_periods=4).max()
    cross_b = _cross_up(var2, var3_ma6)
    cross_s = _cross_up(var3_ma6, var1)

    buy = cross_b & (llv3 <= b3) & (macd > 0)
    sell = (cross_s & (hhv4 >= s3) & (macd < 0)) | (cross_s & (hhv4 >= s7))

    j = _stoch_kdj_from_ohlc(high, low, close, 9, 3, 3)["j"]
    gold = cross_b & (macd > 0) & (pd.to_numeric(j, errors="coerce") >= 90.0) & ((llv3 <= b3) | (llv3 <= (pivot_mid * 0.9)))

    wick_touch_ma13 = (low <= ma13) & (high >= ma13)
    wick_touch_ma55 = (low <= ma55) & (high >= ma55)
    wick_touch_ema27 = (low <= ema27) & (high >= ema27)
    wick_touch_ema29 = (low <= ema29) & (high >= ema29)
    wick_touch_ema32 = (low <= ema32) & (high >= ema32)
    wick_touch_ema36 = (low <= ema36) & (high >= ema36)

    close_breakdown_ma13 = (close < ma13) & (close.shift(1) >= ma13.shift(1))
    close_breakup_ma13 = (close > ma13) & (close.shift(1) <= ma13.shift(1))
    close_breakdown_ma55 = (close < ma55) & (close.shift(1) >= ma55.shift(1))
    close_breakup_ma55 = (close > ma55) & (close.shift(1) <= ma55.shift(1))

    cross_ma13_ema27_up = _cross_up(ma13, ema27)
    cross_ma13_ema27_down = _cross_down(ma13, ema27)
    cross_ma13_ema29_up = _cross_up(ma13, ema29)
    cross_ma13_ema29_down = _cross_down(ma13, ema29)
    cross_ma13_ema32_up = _cross_up(ma13, ema32)
    cross_ma13_ema32_down = _cross_down(ma13, ema32)
    cross_ma13_ema36_up = _cross_up(ma13, ema36)
    cross_ma13_ema36_down = _cross_down(ma13, ema36)

    j_num = pd.to_numeric(j, errors="coerce")
    after_cross_ma13_ema27_up_j_lt80 = cross_ma13_ema27_up.shift(1).fillna(False) & (j_num < 80.0)
    after_cross_ma13_ema27_down_j_gt20 = cross_ma13_ema27_down.shift(1).fillna(False) & (j_num > 20.0)

    dist_b3_atr = (close - b3) / atr_
    dist_s3_atr = (s3 - close) / atr_
    dist_pivot_atr = (close - pivot_mid) / atr_

    red_streak = np.zeros(len(close), dtype=int)
    yellow_streak = np.zeros(len(close), dtype=int)
    br = bar_red.fillna(False).to_numpy(dtype=bool)
    by = bar_yellow.fillna(False).to_numpy(dtype=bool)
    rr = 0
    yy = 0
    for i in range(len(close)):
        if bool(br[i]):
            rr += 1
        else:
            rr = 0
        if bool(by[i]):
            yy += 1
        else:
            yy = 0
        red_streak[i] = rr
        yellow_streak[i] = yy

    return pd.DataFrame(
        {
            "jg_ma13": ma13,
            "jg_ma55": ma55,
            "jg_ma160": ma160,
            "jg_ma120": ma120,
            "jg_ma60": ma60,
            "jg_ma25": ma25,
            "jg_ema20": ema20,
            "jg_ema27": ema27,
            "jg_ema29": ema29,
            "jg_ema32": ema32,
            "jg_ema36": ema36,
            "jg_pivot_mid": pivot_mid,
            "jg_b3": b3,
            "jg_s3": s3,
            "jg_b5": b5,
            "jg_s5": s5,
            "jg_var2": var2,
            "jg_var3": var3,
            "jg_var3_ma6": var3_ma6,
            "jg_bar_yellow": bar_yellow,
            "jg_bar_red": bar_red,
            "jg_flip_to_yellow": flip_to_yellow,
            "jg_flip_to_red": flip_to_red,
            "jg_macd": macd,
            "jg_buy": buy.astype(bool),
            "jg_sell": sell.astype(bool),
            "jg_wick_touch_ma13": wick_touch_ma13.astype(bool),
            "jg_wick_touch_ma55": wick_touch_ma55.astype(bool),
            "jg_wick_touch_ema27": wick_touch_ema27.astype(bool),
            "jg_wick_touch_ema29": wick_touch_ema29.astype(bool),
            "jg_wick_touch_ema32": wick_touch_ema32.astype(bool),
            "jg_wick_touch_ema36": wick_touch_ema36.astype(bool),
            "jg_close_breakdown_ma13": close_breakdown_ma13.astype(bool),
            "jg_close_breakup_ma13": close_breakup_ma13.astype(bool),
            "jg_close_breakdown_ma55": close_breakdown_ma55.astype(bool),
            "jg_close_breakup_ma55": close_breakup_ma55.astype(bool),
            "jg_cross_ma13_ema27_up": cross_ma13_ema27_up.astype(bool),
            "jg_cross_ma13_ema27_down": cross_ma13_ema27_down.astype(bool),
            "jg_cross_ma13_ema29_up": cross_ma13_ema29_up.astype(bool),
            "jg_cross_ma13_ema29_down": cross_ma13_ema29_down.astype(bool),
            "jg_cross_ma13_ema32_up": cross_ma13_ema32_up.astype(bool),
            "jg_cross_ma13_ema32_down": cross_ma13_ema32_down.astype(bool),
            "jg_cross_ma13_ema36_up": cross_ma13_ema36_up.astype(bool),
            "jg_cross_ma13_ema36_down": cross_ma13_ema36_down.astype(bool),
            "jg_after_cross_ma13_ema27_up_j_lt80": after_cross_ma13_ema27_up_j_lt80.astype(bool),
            "jg_after_cross_ma13_ema27_down_j_gt20": after_cross_ma13_ema27_down_j_gt20.astype(bool),
            "jg_dist_b3_atr": dist_b3_atr,
            "jg_dist_s3_atr": dist_s3_atr,
            "jg_dist_pivot_atr": dist_pivot_atr,
            "jg_red_streak": red_streak,
            "jg_yellow_streak": yellow_streak,
            "jg_j": j,
            "jg_gold": gold.astype(bool),
        }
    )


PROJECT_ROOT = Path(__file__).resolve().parent
STATE_PATH = PROJECT_ROOT / ".cache" / "mt5_exit_assistant_state.json"
DEFAULT_LOG_DIR = PROJECT_ROOT / "backtest_out" / "mt5_live"


@dataclass(frozen=True)
class ExitAction:
    ticket: int
    symbol: str
    side: str
    action: str
    volume: float
    price: float
    level_name: str
    level_price: float
    suggested_sl: Optional[float]
    current_sl: Optional[float]


@dataclass(frozen=True)
class EntrySignal:
    ts: str
    symbol: str
    side: str
    signal: str
    entry: float
    stop: float
    atr: float
    entry_score: float
    ema21_1h: float
    breakout_level: float
    touch_delta: int
    strong: bool
    kd_w1_long: bool
    kd_w1_short: bool
    kd_3line_long: bool
    kd_3line_short: bool
    cci144: float = float("nan")
    cci_veto: bool = False
    adx14: float = float("nan")
    chase_dist_atr: float = float("nan")
    score_filter_th: float = float("nan")
    score_filter_pass: bool = True
    e2_chase_max_atr: float = float("nan")
    e2_chase_blocked: bool = False
    e2_chase_action: str = ""
    tick_volume: float = float("nan")
    vol_sma20: float = float("nan")
    vol_ratio: float = float("nan")
    vol_pct: float = float("nan")
    atr_sma50: float = float("nan")
    atr_rel: float = float("nan")
    atr_pct: float = float("nan")
    spread_px: float = float("nan")
    spread_rel: float = float("nan")
    liquidity_gate_enabled: bool = False
    liquidity_max_spread_rel: float = float("nan")
    liquidity_risk: bool = False
    vol_risk_vol_ratio_max: float = float("nan")
    vol_risk_vol_pct_max: float = float("nan")
    vol_risk_action: str = ""
    vol_risk_blocked: bool = False
    entry_score_gate_max: float = float("nan")
    entry_score_gate_action: str = ""
    entry_score_gate_scope: str = ""
    entry_score_gate_hit: bool = False
    entry_score_gate_blocked: bool = False
    sr_support: float = float("nan")
    sr_resistance: float = float("nan")
    sr_support_dist_atr: float = float("nan")
    sr_resistance_dist_atr: float = float("nan")
    sr_support_touches: int = 0
    sr_resistance_touches: int = 0
    jg_macd_up: bool = False
    jg_macd_down: bool = False
    jg_sma175: float = float("nan")
    jg_j: float = float("nan")
    jg_long: bool = False
    jg_short: bool = False
    jg_ma13: float = float("nan")
    jg_ma55: float = float("nan")
    jg_ema20: float = float("nan")
    jg_ema27: float = float("nan")
    jg_ema29: float = float("nan")
    jg_ema32: float = float("nan")
    jg_ema36: float = float("nan")
    jg_pivot_mid: float = float("nan")
    jg_b3: float = float("nan")
    jg_s3: float = float("nan")
    jg_b5: float = float("nan")
    jg_s5: float = float("nan")
    jg_var2: float = float("nan")
    jg_var3: float = float("nan")
    jg_var3_ma6: float = float("nan")
    jg_bar_yellow: bool = False
    jg_bar_red: bool = False
    jg_macd: float = float("nan")
    jg_buy: bool = False
    jg_sell: bool = False
    jg_gold: bool = False
    jg_ma160: float = float("nan")
    jg_ma120: float = float("nan")
    jg_ma60: float = float("nan")
    jg_ma25: float = float("nan")
    jg_flip_to_yellow: bool = False
    jg_flip_to_red: bool = False
    jg_wick_touch_ma13: bool = False
    jg_wick_touch_ma55: bool = False
    jg_wick_touch_ema27: bool = False
    jg_wick_touch_ema29: bool = False
    jg_wick_touch_ema32: bool = False
    jg_wick_touch_ema36: bool = False
    jg_close_breakdown_ma13: bool = False
    jg_close_breakup_ma13: bool = False
    jg_close_breakdown_ma55: bool = False
    jg_close_breakup_ma55: bool = False
    jg_cross_ma13_ema27_up: bool = False
    jg_cross_ma13_ema27_down: bool = False
    jg_cross_ma13_ema29_up: bool = False
    jg_cross_ma13_ema29_down: bool = False
    jg_cross_ma13_ema32_up: bool = False
    jg_cross_ma13_ema32_down: bool = False
    jg_cross_ma13_ema36_up: bool = False
    jg_cross_ma13_ema36_down: bool = False
    jg_after_cross_ma13_ema27_up_j_lt80: bool = False
    jg_after_cross_ma13_ema27_down_j_gt20: bool = False
    jg_dist_b3_atr: float = float("nan")
    jg_dist_s3_atr: float = float("nan")
    jg_dist_pivot_atr: float = float("nan")
    jg_red_streak: int = 0
    jg_yellow_streak: int = 0


@dataclass(frozen=True)
class GateSnapshot:
    ts: str
    symbol: str
    require_strong_for_entry: bool
    strong_long: bool
    strong_short: bool
    regime_long: bool
    regime_short: bool
    confirm_long: bool
    confirm_short: bool
    kd_long: bool
    kd_short: bool
    kd_w1_long: bool
    kd_w1_short: bool
    kd_3line_long: bool
    kd_3line_short: bool
    ema21_1h: float


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _utc_date_tag() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _utc_midnight(dt: Optional[datetime] = None) -> datetime:
    x = dt or datetime.now()
    if getattr(x, "tzinfo", None) is not None:
        x = x.astimezone().replace(tzinfo=None)
    return datetime(x.year, x.month, x.day, 0, 0, 0)


def _parse_iso_dt_utc(s: str) -> datetime:
    t = datetime.fromisoformat(str(s).strip())
    if getattr(t, "tzinfo", None) is None:
        return t
    return t.astimezone().replace(tzinfo=None)


def _write_csv(path: Path, df: pd.DataFrame) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def _append_csv(path: Path, df: pd.DataFrame) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        df.to_csv(path, mode="a", header=False, index=False)
    else:
        df.to_csv(path, index=False)


def _log_dir_for_run(args: Dict[str, Any]) -> Path:
    base = Path(str(args.get("log_dir") or DEFAULT_LOG_DIR))
    return base / _utc_date_tag()


def _apply_private_names(row: Dict[str, object], private_names: bool) -> Dict[str, object]:
    if not private_names:
        return row
    m = {
        "jg_macd_up": "sig_macd_cross_up",
        "jg_macd_down": "sig_macd_cross_down",
        "jg_sma175": "trend_sma175",
        "jg_long": "sig_trend_long",
        "jg_short": "sig_trend_short",
        "jg_ma13": "ma_fast_13",
        "jg_ma55": "ma_slow_55",
        "jg_ma160": "ma_trend_160",
        "jg_ma120": "ma_trend_120",
        "jg_ma60": "ma_trend_60",
        "jg_ma25": "ma_trigger_25",
        "jg_ema20": "ema_20",
        "jg_ema27": "ema_27",
        "jg_ema29": "ema_29",
        "jg_ema32": "ema_32",
        "jg_ema36": "ema_36",
        "jg_pivot_mid": "zone_mid",
        "jg_b3": "zone_buy3",
        "jg_s3": "zone_sell3",
        "jg_b5": "zone_buy5",
        "jg_s5": "zone_sell5",
        "jg_var2": "osc_v2",
        "jg_var3": "osc_v3",
        "jg_var3_ma6": "osc_v3_ma6",
        "jg_bar_yellow": "bar_color_yellow",
        "jg_bar_red": "bar_color_red",
        "jg_flip_to_yellow": "bar_flip_to_yellow",
        "jg_flip_to_red": "bar_flip_to_red",
        "jg_macd": "macd_hist",
        "jg_j": "kdj_j",
        "jg_buy": "sig_buy",
        "jg_sell": "sig_sell",
        "jg_gold": "sig_high_conf",
        "jg_wick_touch_ma13": "sig_wick_touch_ma_fast",
        "jg_wick_touch_ma55": "sig_wick_touch_ma_slow",
        "jg_wick_touch_ema27": "sig_wick_touch_ema27",
        "jg_wick_touch_ema29": "sig_wick_touch_ema29",
        "jg_wick_touch_ema32": "sig_wick_touch_ema32",
        "jg_wick_touch_ema36": "sig_wick_touch_ema36",
        "jg_close_breakdown_ma13": "sig_close_breakdown_ma_fast",
        "jg_close_breakup_ma13": "sig_close_breakup_ma_fast",
        "jg_close_breakdown_ma55": "sig_close_breakdown_ma_slow",
        "jg_close_breakup_ma55": "sig_close_breakup_ma_slow",
        "jg_cross_ma13_ema27_up": "sig_cross_ma_fast_over_ema27",
        "jg_cross_ma13_ema27_down": "sig_cross_ma_fast_under_ema27",
        "jg_cross_ma13_ema29_up": "sig_cross_ma_fast_over_ema29",
        "jg_cross_ma13_ema29_down": "sig_cross_ma_fast_under_ema29",
        "jg_cross_ma13_ema32_up": "sig_cross_ma_fast_over_ema32",
        "jg_cross_ma13_ema32_down": "sig_cross_ma_fast_under_ema32",
        "jg_cross_ma13_ema36_up": "sig_cross_ma_fast_over_ema36",
        "jg_cross_ma13_ema36_down": "sig_cross_ma_fast_under_ema36",
        "jg_after_cross_ma13_ema27_up_j_lt80": "sig_post_cross_up_j_lt80",
        "jg_after_cross_ma13_ema27_down_j_gt20": "sig_post_cross_down_j_gt20",
        "jg_dist_b3_atr": "dist_zone_buy3_atr",
        "jg_dist_s3_atr": "dist_zone_sell3_atr",
        "jg_dist_pivot_atr": "dist_zone_mid_atr",
        "jg_red_streak": "bar_red_streak",
        "jg_yellow_streak": "bar_yellow_streak",
    }
    out: Dict[str, object] = {}
    for k, v in row.items():
        kk = str(k)
        if kk in m:
            out[m[kk]] = v
            continue
        if kk.startswith("jg_"):
            continue
        out[kk] = v
    return out


def _load_state() -> Dict[str, Any]:
    try:
        if STATE_PATH.exists():
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {"schema": 1, "updated_at": _now_utc_iso(), "peak_equity": None, "dd_halted": False, "positions": {}}


def _save_state(state: Dict[str, Any]) -> None:
    state = dict(state)
    state["updated_at"] = _now_utc_iso()
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _float_or_none(x: Any) -> Optional[float]:
    try:
        if x is None:
            return None
        v = float(x)
        if pd.isna(v):
            return None
        return v
    except Exception:
        return None


def _int_or_none(x: Any) -> Optional[int]:
    try:
        if x is None:
            return None
        if isinstance(x, bool):
            return int(x)
        if isinstance(x, (int, np.integer)):
            return int(x)
        s = str(x).strip()
        if s == "":
            return None
        return int(float(s))
    except Exception:
        return None


def _tf_seconds(timeframe: int) -> int:
    if timeframe == mt5.TIMEFRAME_M1:
        return 60
    if timeframe == mt5.TIMEFRAME_M5:
        return 300
    if timeframe == mt5.TIMEFRAME_M15:
        return 900
    if timeframe == mt5.TIMEFRAME_M30:
        return 1800
    if timeframe == mt5.TIMEFRAME_H1:
        return 3600
    if timeframe == mt5.TIMEFRAME_H4:
        return 14400
    if timeframe == mt5.TIMEFRAME_D1:
        return 86400
    raise ValueError(f"unsupported timeframe: {timeframe}")


def _sma_last(x: np.ndarray, window: int, i: int) -> float:
    w = int(window)
    if w <= 0:
        return float("nan")
    j0 = int(i) - w + 1
    if j0 < 0:
        return float("nan")
    seg = x[j0 : int(i) + 1]
    seg = seg[np.isfinite(seg)]
    if len(seg) < w:
        return float("nan")
    return float(np.mean(seg))


def _pct_rank(x: np.ndarray, lookback: int, i: int) -> float:
    lb = int(lookback)
    if lb <= 1:
        return float("nan")
    j0 = max(0, int(i) - lb + 1)
    seg = x[j0 : int(i) + 1]
    seg = seg[np.isfinite(seg)]
    if len(seg) < max(20, min(lb, 50)):
        return float("nan")
    v = float(seg[-1])
    return float(100.0 * float(np.mean(seg <= v)))


def _mt5_rates(symbol: str, timeframe: int, count: int) -> pd.DataFrame:
    symbol = str(symbol).strip()
    if not symbol:
        raise ValueError("empty symbol")
    _ensure_symbol_ready(symbol)
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, int(count))
    if rates is None:
        raise RuntimeError(f"copy_rates_from_pos returned None, error={_mt5_last_error()}")
    if len(rates) <= 2:
        raise RuntimeError(f"not enough rates for {symbol} tf={timeframe}: {len(rates)}")
    df = pd.DataFrame(rates)
    if "time" not in df.columns:
        raise RuntimeError(f"rates missing time field: {symbol} tf={timeframe}")
    dt = pd.to_datetime(df["time"], unit="s")
    close_dt = dt + pd.to_timedelta(_tf_seconds(timeframe), unit="s")
    df["ts"] = close_dt
    if "tick_volume" in df.columns:
        df["volume"] = df["tick_volume"]
    keep = [c for c in ["ts", "open", "high", "low", "close", "volume", "tick_volume"] if c in df.columns]
    df = df[keep].dropna(subset=["open", "high", "low", "close", "ts"])
    df = df.set_index("ts").sort_index()
    df = df.iloc[:-1].copy()
    return df


def _available_symbol_names() -> set[str]:
    syms = mt5.symbols_get()
    if syms is None:
        raise RuntimeError(f"symbols_get returned None, error={_mt5_last_error()}")
    out: set[str] = set()
    for s in syms:
        name = str(getattr(s, "name", "")).strip()
        if name:
            out.add(name)
    return out


def _resolve_symbol(symbol: str) -> str:
    raw = str(symbol).strip()
    if not raw:
        raise ValueError("empty symbol")
    available = _available_symbol_names()
    if raw in available:
        return raw
    u = raw.upper()
    candidates: List[str] = [raw, u, raw.lower()]
    if u.endswith("."):
        candidates.append(u[:-1])
    else:
        candidates.append(u + ".")
    if u.isalpha() and len(u) == 3:
        candidates.append(u + "USD")
        candidates.append(u + "USD.")
    if u in {"XAU", "XAG"}:
        candidates.append(u + "USD")
        candidates.append(u + "USD.")
    picked = _pick_symbol(available, candidates)
    if picked:
        return picked
    raise RuntimeError(f"symbol not found in MT5: {raw}")


def _read_deploy_pool(pool: str) -> Optional[List[str]]:
    pool = str(pool).strip().lower()
    if pool in {"all", "*"}:
        return None
    fn = {
        "core": "deploy_core.csv",
        "observe": "deploy_observe.csv",
        "exclude": "deploy_exclude.csv",
    }.get(pool)
    if not fn:
        raise ValueError(f"unknown pool: {pool}")
    p = PROJECT_ROOT / "backtest_out" / "p1_final_validate3" / fn
    if not p.exists():
        return None
    df = pd.read_csv(p)
    if "symbol" not in df.columns:
        return None
    syms = [str(s).strip() for s in df["symbol"].tolist() if str(s).strip()]
    out: List[str] = []
    seen = set()
    for s in syms:
        u = s.upper()
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out or None


def _parse_bool(x: Any) -> Optional[bool]:
    if x is None:
        return None
    if isinstance(x, bool):
        return bool(x)
    s = str(x).strip().lower()
    if not s:
        return None
    if s in {"1", "true", "t", "yes", "y"}:
        return True
    if s in {"0", "false", "f", "no", "n"}:
        return False
    return None


def _read_deploy_pool_df(pool: str) -> Optional[pd.DataFrame]:
    pool = str(pool).strip().lower()
    if pool in {"all", "*"}:
        return None
    fn = {
        "core": "deploy_core.csv",
        "observe": "deploy_observe.csv",
        "exclude": "deploy_exclude.csv",
    }.get(pool)
    if not fn:
        raise ValueError(f"unknown pool: {pool}")
    p = PROJECT_ROOT / "backtest_out" / "p1_final_validate3" / fn
    if not p.exists():
        return None
    df = pd.read_csv(p)
    if "symbol" not in df.columns:
        return None
    df = df.copy()
    df["symbol"] = df["symbol"].astype(str).str.strip().str.upper()
    df = df[df["symbol"].astype(str).str.len() > 0].reset_index(drop=True)
    if df.empty:
        return None
    return df


@dataclass(frozen=True)
class SymbolSettings:
    symbol: str
    risk_per_trade: Optional[float]
    entry_require_strong: Optional[int]
    enable_e1_atr_regime_gate: Optional[bool]
    enable_e2_touch_requires_strong: Optional[bool]
    enable_e2_break_confirm: Optional[bool]
    enable_e2_exec: Optional[bool]
    cam_enabled: Optional[bool]
    cam_tp1_frac: Optional[float]
    cam_tp2_frac: Optional[float]


def _symbol_settings_map(pool_df: Optional[pd.DataFrame]) -> Dict[str, SymbolSettings]:
    if pool_df is None or pool_df.empty:
        return {}
    out: Dict[str, SymbolSettings] = {}
    for _, r in pool_df.iterrows():
        sym = str(r.get("symbol", "")).strip().upper()
        if not sym:
            continue
        out[sym] = SymbolSettings(
            symbol=sym,
            risk_per_trade=_float_or_none(r.get("risk_per_trade", None)),
            entry_require_strong=_int_or_none(r.get("entry_require_strong", None)),
            enable_e1_atr_regime_gate=_parse_bool(r.get("enable_e1_atr_regime_gate", None)),
            enable_e2_touch_requires_strong=_parse_bool(r.get("enable_e2_touch_requires_strong", None)),
            enable_e2_break_confirm=_parse_bool(r.get("enable_e2_break_confirm", None)),
            enable_e2_exec=_parse_bool(r.get("enable_e2_exec", None)),
            cam_enabled=_parse_bool(r.get("cam_enabled", None)),
            cam_tp1_frac=_float_or_none(r.get("cam_tp1_frac", None)),
            cam_tp2_frac=_float_or_none(r.get("cam_tp2_frac", None)),
        )
    return out


def _params_for_symbol(base: Params, ss: Optional[SymbolSettings]) -> Params:
    if ss is None:
        return base
    kwargs: Dict[str, object] = {}
    if ss.entry_require_strong is not None:
        kwargs["require_strong_for_entry"] = bool(int(ss.entry_require_strong) != 0)
    if ss.enable_e1_atr_regime_gate is not None:
        kwargs["enable_e1_atr_regime_gate"] = bool(ss.enable_e1_atr_regime_gate)
    if ss.enable_e2_touch_requires_strong is not None:
        kwargs["enable_e2_touch_requires_strong"] = bool(ss.enable_e2_touch_requires_strong)
    if ss.enable_e2_break_confirm is not None:
        kwargs["enable_e2_break_confirm"] = bool(ss.enable_e2_break_confirm)
    if ss.cam_enabled is not None:
        kwargs["enable_cam_targets"] = bool(ss.cam_enabled)
    if ss.cam_tp1_frac is not None:
        kwargs["cam_tp1_frac"] = float(ss.cam_tp1_frac)
    if ss.cam_tp2_frac is not None:
        kwargs["cam_tp2_frac"] = float(ss.cam_tp2_frac)
    return replace(base, **kwargs) if kwargs else base


def _risk_money_per_lot(symbol: str, side: str, entry_price: float, sl_price: float) -> Optional[float]:
    sym = _resolve_symbol(symbol)
    _ensure_symbol_ready(sym)
    order_type = mt5.ORDER_TYPE_BUY if str(side).upper() == "LONG" else mt5.ORDER_TYPE_SELL
    r = mt5.order_calc_profit(int(order_type), sym, 1.0, float(entry_price), float(sl_price))
    if r is None:
        return None
    v = float(r)
    if pd.isna(v) or v == 0.0:
        return None
    return float(abs(v))


def _calc_lot_for_risk(symbol: str, side: str, entry_price: float, sl_price: float, risk_money: float) -> float:
    rm = float(risk_money)
    if not (rm > 0):
        return 0.0
    per_lot = _risk_money_per_lot(symbol, side=side, entry_price=entry_price, sl_price=sl_price)
    if per_lot is None or not (float(per_lot) > 0):
        info = mt5.symbol_info(_resolve_symbol(symbol))
        if info is None:
            return 0.0
        tick_value = _float_or_none(getattr(info, "trade_tick_value", None)) or 0.0
        tick_size = _float_or_none(getattr(info, "trade_tick_size", None)) or 0.0
        if not (tick_value > 0 and tick_size > 0):
            return 0.0
        value_per_price = float(tick_value) / float(tick_size)
        dist = abs(float(entry_price) - float(sl_price))
        per_lot = dist * value_per_price
        if not (float(per_lot) > 0):
            return 0.0
    return float(rm / float(per_lot))


def _mt5_last_error() -> str:
    try:
        return str(mt5.last_error())
    except Exception:
        return "unknown"


def _require_mt5_initialized() -> None:
    if mt5.initialize():
        return
    raise RuntimeError(f"mt5.initialize() failed, error={_mt5_last_error()}")


def _shutdown_mt5() -> None:
    try:
        mt5.shutdown()
    except Exception:
        pass


def _is_ipc_error(err: str) -> bool:
    s = str(err).lower()
    return ("ipc" in s) or ("send failed" in s) or ("-10001" in s)


def _mt5_reinit() -> bool:
    try:
        mt5.shutdown()
    except Exception:
        pass
    time.sleep(0.2)
    try:
        return bool(mt5.initialize())
    except Exception:
        return False


def _get_account_equity() -> float:
    info = mt5.account_info()
    if info is None:
        err = _mt5_last_error()
        if _is_ipc_error(err) and _mt5_reinit():
            info = mt5.account_info()
        if info is None:
            raise RuntimeError(f"account_info returned None, error={err}")
    eq = getattr(info, "equity", None)
    if eq is None:
        raise RuntimeError("account_info.equity is None")
    return float(eq)


def _get_account_info() -> Any:
    info = mt5.account_info()
    if info is None:
        err = _mt5_last_error()
        if _is_ipc_error(err) and _mt5_reinit():
            info = mt5.account_info()
        if info is None:
            raise RuntimeError(f"account_info returned None, error={err}")
    return info


def _get_terminal_info() -> Any:
    info = mt5.terminal_info()
    if info is None:
        err = _mt5_last_error()
        if _is_ipc_error(err) and _mt5_reinit():
            info = mt5.terminal_info()
        if info is None:
            raise RuntimeError(f"terminal_info returned None, error={err}")
    return info


def _mt5_history_check(args: Dict[str, Any]) -> None:
    tf_s = str(args.get("mt5_history_tf") or "H1").strip().upper()
    tf_map = {"M1": mt5.TIMEFRAME_M1, "M5": mt5.TIMEFRAME_M5, "M15": mt5.TIMEFRAME_M15, "M30": mt5.TIMEFRAME_M30, "H1": mt5.TIMEFRAME_H1, "H4": mt5.TIMEFRAME_H4, "D1": mt5.TIMEFRAME_D1}
    tf = tf_map.get(tf_s, mt5.TIMEFRAME_H1)

    acc = _get_account_info()
    term = _get_terminal_info()
    print(
        "[MT5][ACCOUNT] server="
        + str(getattr(acc, "server", ""))
        + " login="
        + str(getattr(acc, "login", ""))
        + " company="
        + str(getattr(acc, "company", ""))
        + " terminal_path="
        + str(getattr(term, "path", ""))
        + " data_path="
        + str(getattr(term, "data_path", ""))
    )

    dt_from_s = str(args.get("mt5_history_from") or "").strip()
    dt_to_s = str(args.get("mt5_history_to") or "").strip()
    dt_from = pd.to_datetime(dt_from_s or "2020-01-01", utc=True)
    dt_to = pd.to_datetime(dt_to_s or "2023-09-04", utc=True)

    syms_raw = str(args.get("mt5_history_symbols") or "").strip()
    if syms_raw:
        syms = [x.strip().upper() for x in syms_raw.split(",") if x.strip()]
    else:
        syms = ["XAUUSD", "XAGUSD", "NAS100", "GER40", "US30", "US500", "EURUSD"]

    available = _available_symbol_names()
    alias_map: Dict[str, List[str]] = {
        "US500": ["SP500", "SPX", "SP500.R", "SP500FT.R", "US500.R", "US500FT.R"],
        "SP500": ["US500", "SPX", "SP500.R", "SP500FT.R", "US500.R", "US500FT.R"],
        "US30": ["DJ30", "DOW", "DJI", "DJ30.R", "DJ30FT.R", "US30.R", "US30FT.R"],
        "DJ30": ["US30", "DOW", "DJI", "DJ30.R", "DJ30FT.R", "US30.R", "US30FT.R"],
        "NAS100": ["USTEC", "NAS100.R", "NAS100FT.R"],
        "USTEC": ["NAS100", "NAS100.R", "NAS100FT.R"],
        "GER40": ["DE40", "DAX40", "GER40.R", "GER40FT.R", "DE40.R", "DE40FT.R"],
        "DE40": ["GER40", "DAX40", "GER40.R", "GER40FT.R", "DE40.R", "DE40FT.R"],
        "UK100": ["FTSE100", "UK100.R", "UK100FT.R"],
        "AUS200": ["AU200", "AUS200.R", "AUS200FT.R"],
        "JPN225": ["JP225", "JPN225.R", "JPN225FT.R"],
        "XAUUSD": ["XAUUSD.", "GOLD", "GOLD.", "XAUUSD.R"],
        "XAGUSD": ["XAGUSD.", "SILVER", "SILVER.", "XAGUSD.R"],
    }

    def _resolve_for_history(raw: str) -> Tuple[Optional[str], List[str]]:
        r = str(raw).strip()
        if not r:
            return None, []
        if r in available:
            return r, [r]
        u = r.upper()
        candidates: List[str] = [r, u, r.lower()]
        if u.endswith("."):
            candidates.append(u[:-1])
        else:
            candidates.append(u + ".")
        if u.isalpha() and len(u) == 3:
            candidates.append(u + "USD")
            candidates.append(u + "USD.")
        if u in {"XAU", "XAG"}:
            candidates.append(u + "USD")
            candidates.append(u + "USD.")
        if u in alias_map:
            candidates.extend(alias_map[u])
        picked = _pick_symbol(available, candidates)
        if picked:
            return picked, candidates
        sug: List[str] = []
        uu = u.upper()
        for a in sorted(available):
            au = a.upper()
            if uu in au or au in uu:
                sug.append(a)
                if len(sug) >= 10:
                    break
        return None, sug

    print(f"[MT5][HISTORY] tf={tf_s} from={dt_from.isoformat()} to={dt_to.isoformat()} symbols={len(syms)}")
    for sym in syms:
        s, dbg = _resolve_for_history(sym)
        if not s:
            print(f"  {sym}: not_found suggestions={dbg}")
            continue
        if str(sym).strip().upper() != str(s).strip().upper():
            print(f"  {sym}: resolved={s}")
        try:
            _ensure_symbol_ready(s)
        except Exception as e:
            print(f"  {sym}: not_ready err={e}")
            continue
        rates = mt5.copy_rates_range(s, tf, dt_from.to_pydatetime(), dt_to.to_pydatetime())
        if rates is None:
            print(f"  {sym}: rates=None err={_mt5_last_error()}")
            continue
        df = pd.DataFrame(rates)
        if df.empty or "time" not in df.columns:
            print(f"  {sym}: bars=0")
            continue
        t = pd.to_datetime(df["time"].astype(int), unit="s", utc=True).sort_values()
        dt = t.diff().dropna()
        step = pd.to_timedelta(_tf_seconds(tf), unit="s")
        gaps = dt[dt > step]
        max_gap = gaps.max() if len(gaps) else pd.Timedelta(0)
        print(f"  {sym}: bars={len(df)} from={t.iloc[0]} to={t.iloc[-1]} gaps>{step}={len(gaps)} max_gap={max_gap}")


def _print_trade_api_status() -> bool:
    acc = _get_account_info()
    term = _get_terminal_info()
    connected = bool(getattr(term, "connected", False))
    api_disabled = bool(getattr(term, "tradeapi_disabled", False))
    term_trade_allowed = bool(getattr(term, "trade_allowed", False))
    acc_trade_allowed = bool(getattr(acc, "trade_allowed", False))
    acc_trade_expert = bool(getattr(acc, "trade_expert", False))
    ok = connected and (not api_disabled) and term_trade_allowed and acc_trade_allowed and acc_trade_expert
    print(
        "[MT5] connected="
        + str(connected)
        + " tradeapi_disabled="
        + str(api_disabled)
        + " terminal_trade_allowed="
        + str(term_trade_allowed)
        + " account_trade_allowed="
        + str(acc_trade_allowed)
        + " account_trade_expert="
        + str(acc_trade_expert)
    )
    if not ok:
        print("[MT5] Python 下单被终端拦截。请在 MT5 里开启：")
        print("  1) 顶部工具栏 Algo Trading = ON")
        print("  2) 工具 → 选项 → EA：勾选“允许算法交易”")
        print("  3) 确认未开启禁用交易的全局开关（终端里 terminal_info.trade_allowed 应为 True）")
    return ok

def _get_positions() -> List[Any]:
    ps = mt5.positions_get()
    if ps is None:
        raise RuntimeError(f"positions_get returned None, error={_mt5_last_error()}")
    return list(ps)


def _get_tick(symbol: str) -> Tuple[float, float]:
    t = mt5.symbol_info_tick(symbol)
    if t is None:
        raise RuntimeError(f"symbol_info_tick returned None: {symbol}")
    bid = float(getattr(t, "bid", 0.0))
    ask = float(getattr(t, "ask", 0.0))
    if bid <= 0 or ask <= 0:
        raise RuntimeError(f"invalid tick for {symbol}: bid={bid}, ask={ask}")
    return bid, ask


def _bid_ask(symbol: str) -> Tuple[float, float]:
    sym = _resolve_symbol(symbol)
    return _get_tick(sym)


def _yesterday_d1_hlc(symbol: str) -> Tuple[float, float, float]:
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, 5)
    if rates is None or len(rates) < 2:
        raise RuntimeError(f"not enough D1 rates for {symbol}")
    df = pd.DataFrame(rates)
    df = df.sort_values("time").reset_index(drop=True)
    prev = df.iloc[-2]
    h = float(prev["high"])
    l = float(prev["low"])
    c = float(prev["close"])
    if not (h > 0 and l > 0 and c > 0):
        raise RuntimeError(f"invalid D1 HLC for {symbol}: h={h}, l={l}, c={c}")
    return h, l, c


def _cam_levels_from_hlc(h: float, l: float, c: float, p: Params) -> Dict[str, float]:
    r = h - l
    if r <= 0:
        return {}
    pv = (h + l + c) / 3.0
    r1 = pv + p.cam_r1_mult * r
    r2 = pv + p.cam_r2_mult * r
    s1 = pv - p.cam_r1_mult * r
    s2 = pv - p.cam_r2_mult * r
    return {"R1": float(r1), "R2": float(r2), "S1": float(s1), "S2": float(s2)}


def _pos_side_str(pos_type: int) -> str:
    if pos_type == mt5.POSITION_TYPE_BUY:
        return "LONG"
    if pos_type == mt5.POSITION_TYPE_SELL:
        return "SHORT"
    return f"TYPE_{pos_type}"


def _pos_close_price(symbol: str, side: str) -> float:
    bid, ask = _get_tick(symbol)
    return bid if side == "LONG" else ask


def _ensure_pos_state(state: Dict[str, Any], ticket: int, volume: float) -> Dict[str, Any]:
    positions = state.setdefault("positions", {})
    k = str(int(ticket))
    if k not in positions:
        positions[k] = {
            "initial_volume": float(volume),
            "tp1_done": False,
            "tp2_done": False,
            "created_at": _now_utc_iso(),
        }
    pv = positions[k]
    if _float_or_none(pv.get("initial_volume")) is None:
        pv["initial_volume"] = float(volume)
    return pv


def _suggest_sl_to_be(side: str, entry_price: float, current_sl: Optional[float]) -> float:
    if side == "LONG":
        if current_sl is None:
            return float(entry_price)
        return float(max(float(current_sl), float(entry_price)))
    if current_sl is None:
        return float(entry_price)
    return float(min(float(current_sl), float(entry_price)))


def _build_actions_for_position(
    pos: Any, p: Params, state: Dict[str, Any], enable_cam: bool, symbols_filter: Optional[set[str]]
) -> List[ExitAction]:
    symbol = str(getattr(pos, "symbol", "")).strip()
    if not symbol:
        return []
    if symbols_filter is not None and symbol.upper() not in symbols_filter:
        return []

    ticket = int(getattr(pos, "ticket"))
    volume = float(getattr(pos, "volume"))
    if volume <= 0:
        return []
    entry_price = float(getattr(pos, "price_open"))
    pos_type = int(getattr(pos, "type"))
    side = _pos_side_str(pos_type)
    if side not in {"LONG", "SHORT"}:
        return []

    sl = _float_or_none(getattr(pos, "sl", None))

    pv = _ensure_pos_state(state, ticket=ticket, volume=volume)
    init_volume = float(pv.get("initial_volume", volume))
    tp1_done = bool(pv.get("tp1_done", False))
    tp2_done = bool(pv.get("tp2_done", False))

    if not enable_cam or not bool(p.enable_cam_targets):
        return []

    h, l, c = _yesterday_d1_hlc(symbol)
    levels = _cam_levels_from_hlc(h, l, c, p)
    if not levels:
        return []

    px = _pos_close_price(symbol, side=side)
    actions: List[ExitAction] = []

    if side == "LONG":
        if (not tp1_done) and ("R1" in levels) and (px >= levels["R1"]):
            v = max(0.0, min(init_volume, init_volume * float(p.cam_tp1_frac)))
            if v > 0:
                actions.append(
                    ExitAction(
                        ticket=ticket,
                        symbol=symbol,
                        side=side,
                        action="CLOSE_PARTIAL",
                        volume=float(v),
                        price=float(px),
                        level_name="R1",
                        level_price=float(levels["R1"]),
                        suggested_sl=_suggest_sl_to_be(side, entry_price, sl),
                        current_sl=sl,
                    )
                )
        if (not tp2_done) and ("R2" in levels) and (px >= levels["R2"]):
            v = max(0.0, min(init_volume, init_volume * float(p.cam_tp2_frac)))
            if v > 0:
                actions.append(
                    ExitAction(
                        ticket=ticket,
                        symbol=symbol,
                        side=side,
                        action="CLOSE_PARTIAL",
                        volume=float(v),
                        price=float(px),
                        level_name="R2",
                        level_price=float(levels["R2"]),
                        suggested_sl=_suggest_sl_to_be(side, entry_price, sl),
                        current_sl=sl,
                    )
                )
    else:
        if (not tp1_done) and ("S1" in levels) and (px <= levels["S1"]):
            v = max(0.0, min(init_volume, init_volume * float(p.cam_tp1_frac)))
            if v > 0:
                actions.append(
                    ExitAction(
                        ticket=ticket,
                        symbol=symbol,
                        side=side,
                        action="CLOSE_PARTIAL",
                        volume=float(v),
                        price=float(px),
                        level_name="S1",
                        level_price=float(levels["S1"]),
                        suggested_sl=_suggest_sl_to_be(side, entry_price, sl),
                        current_sl=sl,
                    )
                )
        if (not tp2_done) and ("S2" in levels) and (px <= levels["S2"]):
            v = max(0.0, min(init_volume, init_volume * float(p.cam_tp2_frac)))
            if v > 0:
                actions.append(
                    ExitAction(
                        ticket=ticket,
                        symbol=symbol,
                        side=side,
                        action="CLOSE_PARTIAL",
                        volume=float(v),
                        price=float(px),
                        level_name="S2",
                        level_price=float(levels["S2"]),
                        suggested_sl=_suggest_sl_to_be(side, entry_price, sl),
                        current_sl=sl,
                    )
                )

    return actions


def _send_close_partial(pos: Any, volume: float) -> Any:
    symbol = str(getattr(pos, "symbol", "")).strip()
    ticket = int(getattr(pos, "ticket"))
    pos_type = int(getattr(pos, "type"))
    if pos_type == mt5.POSITION_TYPE_BUY:
        order_type = mt5.ORDER_TYPE_SELL
        price = _get_tick(symbol)[0]
    else:
        order_type = mt5.ORDER_TYPE_BUY
        price = _get_tick(symbol)[1]
    req = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(volume),
        "type": order_type,
        "position": ticket,
        "price": float(price),
        "deviation": 50,
        "type_time": mt5.ORDER_TIME_GTC,
    }
    return _order_send_try_fillings(req)


def _send_modify_sl(pos: Any, sl: float) -> Any:
    symbol = str(getattr(pos, "symbol", "")).strip()
    ticket = int(getattr(pos, "ticket"))
    tp = _float_or_none(getattr(pos, "tp", None))
    req = {
        "action": mt5.TRADE_ACTION_SLTP,
        "symbol": symbol,
        "position": ticket,
        "sl": float(sl),
        "tp": float(tp) if tp is not None else 0.0,
    }
    return mt5.order_send(req)


def _send_open_market(symbol: str, side: str, volume: float, sl: float) -> Any:
    sym = _resolve_symbol(symbol)
    info = _ensure_symbol_ready(sym)
    v = _normalize_volume(info, float(volume))
    if v <= 0:
        raise ValueError(f"invalid volume: {volume}")
    bid, ask = _get_tick(sym)
    if side == "LONG":
        order_type = mt5.ORDER_TYPE_BUY
        px = float(ask)
    elif side == "SHORT":
        order_type = mt5.ORDER_TYPE_SELL
        px = float(bid)
    else:
        raise ValueError(f"invalid side: {side}")
    req = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": sym,
        "volume": float(v),
        "type": int(order_type),
        "price": float(px),
        "sl": float(sl),
        "deviation": 50,
        "type_time": mt5.ORDER_TIME_GTC,
    }
    return _order_send_try_fillings(req)


def _ensure_symbol_ready(symbol: str) -> Any:
    symbol = str(symbol).strip()
    if not symbol:
        raise ValueError("empty symbol")
    mt5.symbol_select(symbol, True)
    info = mt5.symbol_info(symbol)
    if info is None:
        raise RuntimeError(f"symbol_info returned None: {symbol}")
    if not bool(getattr(info, "visible", True)):
        mt5.symbol_select(symbol, True)
    return info


def _normalize_volume(info: Any, volume: float) -> float:
    v = float(volume)
    vmin = float(getattr(info, "volume_min", 0.0) or 0.0)
    vmax = float(getattr(info, "volume_max", v) or v)
    step = float(getattr(info, "volume_step", 0.0) or 0.0)
    if step <= 0:
        step = 0.01
    v = max(v, vmin if vmin > 0 else v)
    if vmax > 0:
        v = min(v, vmax)
    if step > 0:
        v = int(v / step) * step
    if vmin > 0 and v < vmin:
        v = vmin
    return float(round(v, 8))


def _order_send_try_fillings(req: Dict[str, Any]) -> Any:
    res = None
    for filling in [mt5.ORDER_FILLING_IOC, mt5.ORDER_FILLING_FOK, mt5.ORDER_FILLING_RETURN]:
        r = dict(req)
        r["type_filling"] = filling
        res = mt5.order_send(r)
        ret = getattr(res, "retcode", None) if res is not None else None
        if ret == mt5.TRADE_RETCODE_DONE:
            return res
    return res


def _print_dd_banner(equity: float, peak: float, dd: float, max_dd: float, halted: bool) -> None:
    dd_pct = dd * 100.0
    max_pct = max_dd * 100.0
    status = "HALTED" if halted else "OK"
    print(f"[DD] equity={equity:.2f} peak={peak:.2f} dd={dd_pct:.2f}% threshold={max_pct:.2f}% status={status}")


def _print_actions(actions: List[ExitAction]) -> None:
    if not actions:
        print("[ACTIONS] none")
        return
    rows: List[Dict[str, object]] = []
    for a in actions:
        rows.append(
            {
                "ticket": a.ticket,
                "symbol": a.symbol,
                "side": a.side,
                "action": a.action,
                "volume": round(float(a.volume), 4),
                "price": round(float(a.price), 6),
                "level": a.level_name,
                "level_price": round(float(a.level_price), 6),
                "sl_now": round(float(a.current_sl), 6) if a.current_sl is not None else "",
                "sl_suggest": round(float(a.suggested_sl), 6) if a.suggested_sl is not None else "",
            }
        )
    df = pd.DataFrame(rows)
    with pd.option_context("display.max_rows", 200, "display.width", 200):
        print(df.to_string(index=False))


def _print_entries(entries: List[EntrySignal]) -> None:
    if not entries:
        print("[ENTRY] none")
        return
    rows: List[Dict[str, object]] = []
    for e in entries:
        rows.append(
            {
                "ts": e.ts,
                "symbol": e.symbol,
                "side": e.side,
                "signal": e.signal,
                "entry": round(float(e.entry), 6),
                "stop": round(float(e.stop), 6),
                "atr": round(float(e.atr), 6),
                "score": round(float(e.entry_score), 4),
                "ema21": round(float(e.ema21_1h), 6),
                "breakout": round(float(e.breakout_level), 6) if not pd.isna(e.breakout_level) else "",
                "touch_d": int(e.touch_delta),
                "strong": bool(e.strong),
                "cci144": round(float(e.cci144), 2) if not pd.isna(e.cci144) else "",
                "cci_veto": bool(e.cci_veto),
                "adx14": round(float(e.adx14), 2) if not pd.isna(e.adx14) else "",
                "chase": round(float(e.chase_dist_atr), 3) if not pd.isna(e.chase_dist_atr) else "",
                "score_th": round(float(e.score_filter_th), 4) if not pd.isna(e.score_filter_th) else "",
                "score_pass": bool(e.score_filter_pass),
                "e2_thr": round(float(e.e2_chase_max_atr), 3) if not pd.isna(e.e2_chase_max_atr) else "",
                "e2_blk": bool(e.e2_chase_blocked),
                "vol_r": round(float(e.vol_ratio), 3) if not pd.isna(e.vol_ratio) else "",
                "vol_p": round(float(e.vol_pct), 1) if not pd.isna(e.vol_pct) else "",
                "atr_r": round(float(e.atr_rel), 3) if not pd.isna(e.atr_rel) else "",
                "atr_p": round(float(e.atr_pct), 1) if not pd.isna(e.atr_pct) else "",
                "spr_r": round(float(e.spread_rel), 4) if not pd.isna(e.spread_rel) else "",
                "liq_risk": bool(e.liquidity_risk),
                "vol_blk": bool(e.vol_risk_blocked),
            }
        )
    df = pd.DataFrame(rows)
    with pd.option_context("display.max_rows", 200, "display.width", 220):
        print(df.to_string(index=False))


def _last_bar_open_ts(symbol: str, timeframe: int) -> Optional[pd.Timestamp]:
    rates = mt5.copy_rates_from_pos(str(symbol), int(timeframe), 0, 2)
    if rates is None:
        return None
    try:
        if len(rates) <= 0:
            return None
        t = int(rates[-1]["time"])
        return pd.to_datetime(t, unit="s", utc=True)
    except Exception:
        return None


def _ts_utc_naive(x: pd.Timestamp) -> pd.Timestamp:
    if getattr(x, "tzinfo", None) is not None:
        return x.tz_convert("UTC").tz_localize(None)
    return x


def _tick_ts(symbol: str) -> Optional[pd.Timestamp]:
    tick = mt5.symbol_info_tick(str(symbol))
    if tick is None:
        return None
    try:
        t = getattr(tick, "time", None)
        if t is None:
            return None
        return pd.to_datetime(int(t), unit="s", utc=True)
    except Exception:
        return None


def _print_entry_status(rows: List[Dict[str, object]]) -> None:
    if not rows:
        print("[ENTRY][STATUS] none")
        return
    df = pd.DataFrame(rows)
    with pd.option_context("display.max_rows", 200, "display.width", 260):
        print(df.to_string(index=False))


def _print_gate_snapshots(rows: List[GateSnapshot]) -> None:
    if not rows:
        print("[GATE] none")
        return
    out_rows: List[Dict[str, object]] = []
    for r in rows:
        req_strong = bool(getattr(r, "require_strong_for_entry", True))
        if req_strong:
            allow_long = bool(r.regime_long) and bool(r.confirm_long) and bool(r.kd_long)
            allow_short = bool(r.regime_short) and bool(r.confirm_short) and bool(r.kd_short)
            pass_long = allow_long and bool(r.strong_long)
            pass_short = allow_short and bool(r.strong_short)
        else:
            allow_long = bool(r.regime_long) and bool(r.confirm_long)
            allow_short = bool(r.regime_short) and bool(r.confirm_short)
            pass_long = allow_long
            pass_short = allow_short
        out_rows.append(
            {
                "ts": r.ts,
                "symbol": r.symbol,
                "reqStrong": bool(req_strong),
                "allowL": bool(allow_long),
                "allowS": bool(allow_short),
                "passL": bool(pass_long),
                "passS": bool(pass_short),
                "strongL": bool(r.strong_long),
                "strongS": bool(r.strong_short),
                "regL": bool(r.regime_long),
                "regS": bool(r.regime_short),
                "confL": bool(r.confirm_long),
                "confS": bool(r.confirm_short),
                "kdL": bool(r.kd_long),
                "kdS": bool(r.kd_short),
                "kdWL": bool(r.kd_w1_long),
                "kdWS": bool(r.kd_w1_short),
                "kd3L": bool(r.kd_3line_long),
                "kd3S": bool(r.kd_3line_short),
                "ema21": round(float(r.ema21_1h), 6),
            }
        )
    df = pd.DataFrame(out_rows)
    with pd.option_context("display.max_rows", 200, "display.width", 260):
        print(df.to_string(index=False))


def _print_exit_diag(rows: List[Dict[str, object]]) -> None:
    if not rows:
        print("[EXIT] none")
        return
    df = pd.DataFrame(rows)
    with pd.option_context("display.max_rows", 200, "display.width", 260):
        print(df.to_string(index=False))


def _marketwatch_symbols(max_n: int) -> List[str]:
    out: List[str] = []
    seen = set()
    syms = mt5.symbols_get()
    if syms is None:
        raise RuntimeError(f"symbols_get returned None, error={_mt5_last_error()}")
    for s in syms:
        if len(out) >= int(max_n):
            break
        name = str(getattr(s, "name", "")).strip()
        if not name:
            continue
        if not bool(getattr(s, "visible", False)):
            continue
        u = name.upper()
        if u in seen:
            continue
        seen.add(u)
        out.append(u)
    return out


def _entry_universe(args: Dict[str, Any], pool_syms: Optional[List[str]]) -> List[str]:
    u = str(args.get("entry_universe") or "pool").strip().lower()
    if u in {"pool", "core", "observe", "exclude"}:
        return list(pool_syms or [])
    if u in {"marketwatch", "watch", "mw"}:
        return _marketwatch_symbols(int(args.get("entry_max") or 30))
    if u in {"symbols", "list"}:
        raw = str(args.get("entry_symbols") or "").strip()
        if not raw:
            return []
        parts = [x.strip().upper() for x in raw.split(",") if x.strip()]
        out: List[str] = []
        seen = set()
        for s in parts:
            if s not in seen:
                seen.add(s)
                out.append(s)
        return out
    raise ValueError(f"unknown entry_universe: {u}")


def _entry_last_ts_get(state: Dict[str, Any], symbol: str, key: str) -> str:
    d = state.get(str(key))
    if not isinstance(d, dict):
        return ""
    return str(d.get(str(symbol).upper(), "") or "")


def _entry_last_ts_set(state: Dict[str, Any], symbol: str, ts: str, key: str) -> None:
    k = str(key)
    d = state.get(k)
    if not isinstance(d, dict):
        d = {}
        state[k] = d
    d[str(symbol).upper()] = str(ts)


def _scan_entry_signal(symbol: str, p: Params, emit_gate_log: bool = False) -> Optional[EntrySignal]:
    sym = _resolve_symbol(symbol)
    df1 = _mt5_rates(sym, mt5.TIMEFRAME_H1, int(600))
    df4 = _mt5_rates(sym, mt5.TIMEFRAME_H4, int(400))
    dfd = _mt5_rates(sym, mt5.TIMEFRAME_D1, int(300))
    df1 = df1.copy()
    df1["atr"] = atr(df1, int(p.atr_n))
    tr = compute_trend_flags(df1, df4, dfd, p)
    tr = tr.reindex(df1.index)

    if len(df1) < int(max(p.n_break + 5, p.atr_n + 5, 60)):
        return None
    o_arr = df1["open"].to_numpy(dtype=float)
    h_arr = df1["high"].to_numpy(dtype=float)
    l_arr = df1["low"].to_numpy(dtype=float)
    c_arr = df1["close"].to_numpy(dtype=float)
    atr_arr = df1["atr"].to_numpy(dtype=float)
    tv_arr = df1["tick_volume"].to_numpy(dtype=float) if "tick_volume" in df1.columns else np.full(len(df1), np.nan, dtype=float)

    adx14_df = _adx_from_ohlc(df1["high"], df1["low"], df1["close"], 14)
    adx14_arr = adx14_df["adx"].to_numpy(dtype=float)
    cci144_arr = _cci_from_ohlc(df1["high"], df1["low"], df1["close"], 144).to_numpy(dtype=float)
    zrf_h1 = _zrf_macd_from_close(df1["close"])
    jg_macd_up_arr = _cross_up(zrf_h1["zrf_diff"], zrf_h1["zrf_dea"]).to_numpy(dtype=bool)
    jg_macd_down_arr = _cross_down(zrf_h1["zrf_diff"], zrf_h1["zrf_dea"]).to_numpy(dtype=bool)
    jg_sma175_arr = (
        pd.to_numeric(df1["close"], errors="coerce")
        .rolling(175, min_periods=175)
        .mean()
        .to_numpy(dtype=float)
    )
    jg_j_arr = _stoch_kdj_from_ohlc(df1["high"], df1["low"], df1["close"], 9, 3, 3)["j"].to_numpy(dtype=float)
    jg_df = _jinding_features(df1)
    jg_ma13_arr = jg_df["jg_ma13"].to_numpy(dtype=float)
    jg_ma55_arr = jg_df["jg_ma55"].to_numpy(dtype=float)
    jg_ema20_arr = jg_df["jg_ema20"].to_numpy(dtype=float)
    jg_ema27_arr = jg_df["jg_ema27"].to_numpy(dtype=float)
    jg_ema29_arr = jg_df["jg_ema29"].to_numpy(dtype=float)
    jg_ema32_arr = jg_df["jg_ema32"].to_numpy(dtype=float)
    jg_ema36_arr = jg_df["jg_ema36"].to_numpy(dtype=float)
    jg_pivot_mid_arr = jg_df["jg_pivot_mid"].to_numpy(dtype=float)
    jg_b3_arr = jg_df["jg_b3"].to_numpy(dtype=float)
    jg_s3_arr = jg_df["jg_s3"].to_numpy(dtype=float)
    jg_b5_arr = jg_df["jg_b5"].to_numpy(dtype=float)
    jg_s5_arr = jg_df["jg_s5"].to_numpy(dtype=float)
    jg_var2_arr = jg_df["jg_var2"].to_numpy(dtype=float)
    jg_var3_arr = jg_df["jg_var3"].to_numpy(dtype=float)
    jg_var3_ma6_arr = jg_df["jg_var3_ma6"].to_numpy(dtype=float)
    jg_bar_yellow_arr = jg_df["jg_bar_yellow"].to_numpy(dtype=bool)
    jg_bar_red_arr = jg_df["jg_bar_red"].to_numpy(dtype=bool)
    jg_flip_to_yellow_arr = jg_df["jg_flip_to_yellow"].to_numpy(dtype=bool)
    jg_flip_to_red_arr = jg_df["jg_flip_to_red"].to_numpy(dtype=bool)
    jg_macd_arr = jg_df["jg_macd"].to_numpy(dtype=float)
    jg_buy_arr = jg_df["jg_buy"].to_numpy(dtype=bool)
    jg_sell_arr = jg_df["jg_sell"].to_numpy(dtype=bool)
    jg_gold_arr = jg_df["jg_gold"].to_numpy(dtype=bool)
    jg_ma160_arr = jg_df["jg_ma160"].to_numpy(dtype=float)
    jg_ma120_arr = jg_df["jg_ma120"].to_numpy(dtype=float)
    jg_ma60_arr = jg_df["jg_ma60"].to_numpy(dtype=float)
    jg_ma25_arr = jg_df["jg_ma25"].to_numpy(dtype=float)
    jg_wick_touch_ma13_arr = jg_df["jg_wick_touch_ma13"].to_numpy(dtype=bool)
    jg_wick_touch_ma55_arr = jg_df["jg_wick_touch_ma55"].to_numpy(dtype=bool)
    jg_wick_touch_ema27_arr = jg_df["jg_wick_touch_ema27"].to_numpy(dtype=bool)
    jg_wick_touch_ema29_arr = jg_df["jg_wick_touch_ema29"].to_numpy(dtype=bool)
    jg_wick_touch_ema32_arr = jg_df["jg_wick_touch_ema32"].to_numpy(dtype=bool)
    jg_wick_touch_ema36_arr = jg_df["jg_wick_touch_ema36"].to_numpy(dtype=bool)
    jg_close_breakdown_ma13_arr = jg_df["jg_close_breakdown_ma13"].to_numpy(dtype=bool)
    jg_close_breakup_ma13_arr = jg_df["jg_close_breakup_ma13"].to_numpy(dtype=bool)
    jg_close_breakdown_ma55_arr = jg_df["jg_close_breakdown_ma55"].to_numpy(dtype=bool)
    jg_close_breakup_ma55_arr = jg_df["jg_close_breakup_ma55"].to_numpy(dtype=bool)
    jg_cross_ma13_ema27_up_arr = jg_df["jg_cross_ma13_ema27_up"].to_numpy(dtype=bool)
    jg_cross_ma13_ema27_down_arr = jg_df["jg_cross_ma13_ema27_down"].to_numpy(dtype=bool)
    jg_cross_ma13_ema29_up_arr = jg_df["jg_cross_ma13_ema29_up"].to_numpy(dtype=bool)
    jg_cross_ma13_ema29_down_arr = jg_df["jg_cross_ma13_ema29_down"].to_numpy(dtype=bool)
    jg_cross_ma13_ema32_up_arr = jg_df["jg_cross_ma13_ema32_up"].to_numpy(dtype=bool)
    jg_cross_ma13_ema32_down_arr = jg_df["jg_cross_ma13_ema32_down"].to_numpy(dtype=bool)
    jg_cross_ma13_ema36_up_arr = jg_df["jg_cross_ma13_ema36_up"].to_numpy(dtype=bool)
    jg_cross_ma13_ema36_down_arr = jg_df["jg_cross_ma13_ema36_down"].to_numpy(dtype=bool)
    jg_after_cross_ma13_ema27_up_j_lt80_arr = jg_df["jg_after_cross_ma13_ema27_up_j_lt80"].to_numpy(dtype=bool)
    jg_after_cross_ma13_ema27_down_j_gt20_arr = jg_df["jg_after_cross_ma13_ema27_down_j_gt20"].to_numpy(dtype=bool)
    jg_dist_b3_atr_arr = jg_df["jg_dist_b3_atr"].to_numpy(dtype=float)
    jg_dist_s3_atr_arr = jg_df["jg_dist_s3_atr"].to_numpy(dtype=float)
    jg_dist_pivot_atr_arr = jg_df["jg_dist_pivot_atr"].to_numpy(dtype=float)
    jg_red_streak_arr = jg_df["jg_red_streak"].to_numpy(dtype=int)
    jg_yellow_streak_arr = jg_df["jg_yellow_streak"].to_numpy(dtype=int)

    strong_long_arr = tr["strong_long"].to_numpy(dtype=bool)
    strong_short_arr = tr["strong_short"].to_numpy(dtype=bool)
    regime_long_arr = tr["regime_long"].to_numpy(dtype=bool)
    regime_short_arr = tr["regime_short"].to_numpy(dtype=bool)
    confirm_long_arr = tr["confirm_long"].to_numpy(dtype=bool)
    confirm_short_arr = tr["confirm_short"].to_numpy(dtype=bool)
    ema21_1h_arr = tr["ema21_1h"].to_numpy(dtype=float)
    ema13_4h_arr = tr["ema13_4h"].to_numpy(dtype=float)
    ema55_4h_arr = tr["ema55_4h"].to_numpy(dtype=float)
    ema144_4h_arr = tr["ema144_4h"].to_numpy(dtype=float)
    close_4h_arr = tr["close_4h"].to_numpy(dtype=float)
    kd_k_4h_arr = tr["kd_k_4h"].to_numpy(dtype=float)
    kd_d_4h_arr = tr["kd_d_4h"].to_numpy(dtype=float)
    kd_k_1d_arr = tr["kd_k_1d"].to_numpy(dtype=float)
    kd_d_1d_arr = tr["kd_d_1d"].to_numpy(dtype=float)
    kd_w1_long_arr = tr["kd_w1_long"].to_numpy(dtype=bool) if "kd_w1_long" in tr.columns else np.zeros(len(df1), dtype=bool)
    kd_w1_short_arr = tr["kd_w1_short"].to_numpy(dtype=bool) if "kd_w1_short" in tr.columns else np.zeros(len(df1), dtype=bool)
    kd_3line_long_arr = tr["kd_3line_long"].to_numpy(dtype=bool) if "kd_3line_long" in tr.columns else np.zeros(len(df1), dtype=bool)
    kd_3line_short_arr = tr["kd_3line_short"].to_numpy(dtype=bool) if "kd_3line_short" in tr.columns else np.zeros(len(df1), dtype=bool)
    bb_squeeze_4h_arr = tr["bb_squeeze_4h"].to_numpy(dtype=bool)

    level_long_arr = df1["high"].rolling(int(p.n_break), min_periods=int(p.n_break)).max().shift(1).to_numpy(dtype=float)
    level_short_arr = df1["low"].rolling(int(p.n_break), min_periods=int(p.n_break)).min().shift(1).to_numpy(dtype=float)

    e1_state: Optional[str] = None
    e1_dir = 0
    e1_level = np.nan
    e1_start_i = -1
    e1_end_i = -1
    e1_touched = False
    e1_break_i = -1
    e1_break_atr = np.nan
    e1_break_strength_atr_state = 0.0
    e1_touch_i = -1
    e1_retest_depth_atr_state = 0.0
    last_touch_i_long: Optional[int] = None
    last_touch_i_short: Optional[int] = None

    sigs: List[EntrySignal] = []
    idx = df1.index
    for i in range(len(df1)):
        emit_gate_this = bool(emit_gate_log) and (i == len(df1) - 1)
        o = float(o_arr[i])
        h = float(h_arr[i])
        l = float(l_arr[i])
        cl = float(c_arr[i])
        a = float(atr_arr[i])
        if not (a > 0) or pd.isna(a) or pd.isna(cl) or pd.isna(o) or pd.isna(h) or pd.isna(l):
            continue

        strong_long = bool(strong_long_arr[i])
        strong_short = bool(strong_short_arr[i])
        gate_long = strong_long if bool(p.require_strong_for_entry) else (bool(regime_long_arr[i]) and bool(confirm_long_arr[i]))
        gate_short = strong_short if bool(p.require_strong_for_entry) else (bool(regime_short_arr[i]) and bool(confirm_short_arr[i]))

        ema21_1h = float(ema21_1h_arr[i])
        if (not bool(p.enable_e2_touch_requires_strong)) or strong_long:
            if l <= ema21_1h - float(p.touch_k) * a:
                last_touch_i_long = i
        if (not bool(p.enable_e2_touch_requires_strong)) or strong_short:
            if h >= ema21_1h + float(p.touch_k) * a:
                last_touch_i_short = i

        e1_entry = False
        e1_entry_side = 0
        e1_break_strength_atr = 0.0
        e1_retest_depth_atr = 0.0
        e1_retest_bars = 0
        e1_touch_bars = 0
        e1_atr_ratio = 1.0
        touch_delta: Optional[int] = None
        body_atr = 0.0
        breakout_atr = 0.0

        if gate_long or gate_short:
            if e1_state is None:
                if gate_long:
                    level_long = float(level_long_arr[i])
                    if (not pd.isna(level_long)) and cl > level_long:
                        e1_state = "await"
                        e1_dir = 1
                        e1_level = float(level_long)
                        e1_start_i = i + 1
                        e1_end_i = i + int(p.m_retest)
                        e1_touched = False
                        e1_break_i = i
                        e1_break_atr = a
                        e1_break_strength_atr_state = (cl - e1_level) / a if a > 0 else 0.0
                        e1_touch_i = -1
                        e1_retest_depth_atr_state = 0.0
                elif gate_short:
                    level_short = float(level_short_arr[i])
                    if (not pd.isna(level_short)) and cl < level_short:
                        e1_state = "await"
                        e1_dir = -1
                        e1_level = float(level_short)
                        e1_start_i = i + 1
                        e1_end_i = i + int(p.m_retest)
                        e1_touched = False
                        e1_break_i = i
                        e1_break_atr = a
                        e1_break_strength_atr_state = (e1_level - cl) / a if a > 0 else 0.0
                        e1_touch_i = -1
                        e1_retest_depth_atr_state = 0.0
            else:
                if i < e1_start_i or i > e1_end_i:
                    e1_state = None
                else:
                    band_low = float(e1_level) - float(p.k) * a
                    band_high = float(e1_level) + float(p.k) * a
                    touched = (l <= band_high) and (h >= band_low)
                    if touched:
                        e1_touched = True
                        if e1_touch_i < 0:
                            e1_touch_i = i
                    if e1_dir == 1:
                        depth_atr = (float(e1_level) - l) / a if a > 0 else 0.0
                    else:
                        depth_atr = (h - float(e1_level)) / a if a > 0 else 0.0
                    if float(depth_atr) > float(e1_retest_depth_atr_state):
                        e1_retest_depth_atr_state = float(depth_atr)

                    fail = False
                    if float(p.e1_fail_k) > 0:
                        if e1_dir == 1:
                            fail = cl < (float(e1_level) - float(p.e1_fail_k) * a)
                        else:
                            fail = cl > (float(e1_level) + float(p.e1_fail_k) * a)
                    if fail:
                        e1_state = None
                    else:
                        confirmed = (cl >= float(e1_level)) if e1_dir == 1 else (cl <= float(e1_level))
                        if e1_touched and confirmed:
                            e1_entry = True
                            e1_entry_side = int(e1_dir)
                            breakout_atr = abs(cl - float(e1_level)) / a if a > 0 else 0.0
                            e1_break_strength_atr = float(e1_break_strength_atr_state)
                            e1_retest_depth_atr = float(e1_retest_depth_atr_state)
                            e1_retest_bars = int(i - e1_break_i) if e1_break_i >= 0 else 0
                            e1_touch_bars = int(i - e1_touch_i) if e1_touch_i >= 0 else e1_retest_bars
                            e1_atr_ratio = float(a / e1_break_atr) if (e1_break_atr is not None and not pd.isna(e1_break_atr) and float(e1_break_atr) > 0) else 1.0
                            e1_state = None

        if e1_entry:
            entry_side = int(e1_entry_side)
            entry_reason = "E1"
        else:
            entry_side = 0
            entry_reason = ""
            if gate_long:
                touched_ok = last_touch_i_long is not None and 1 <= i - int(last_touch_i_long) <= int(p.x_touch)
                if touched_ok:
                    touch_delta = i - int(last_touch_i_long)
                    body = abs(cl - o)
                    body_atr = body / a if a > 0 else 0.0
                    wick_ok = l >= ema21_1h - float(p.shadow_k) * a
                    reclaim = (cl > ema21_1h) and (cl > o) and (body >= float(p.body_k) * a) and wick_ok
                    if reclaim:
                        if bool(p.enable_e2_break_confirm):
                            level_long = float(level_long_arr[i])
                            if (not pd.isna(level_long)) and (cl > level_long):
                                breakout_atr = (cl - level_long) / a if a > 0 else 0.0
                                entry_side = 1
                                entry_reason = "E2"
                        else:
                            entry_side = 1
                            entry_reason = "E2"
            elif gate_short:
                touched_ok = last_touch_i_short is not None and 1 <= i - int(last_touch_i_short) <= int(p.x_touch)
                if touched_ok:
                    touch_delta = i - int(last_touch_i_short)
                    body = abs(cl - o)
                    body_atr = body / a if a > 0 else 0.0
                    wick_ok = h <= ema21_1h + float(p.shadow_k) * a
                    reclaim = (cl < ema21_1h) and (cl < o) and (body >= float(p.body_k) * a) and wick_ok
                    if reclaim:
                        if bool(p.enable_e2_break_confirm):
                            level_short = float(level_short_arr[i])
                            if (not pd.isna(level_short)) and (cl < level_short):
                                breakout_atr = (level_short - cl) / a if a > 0 else 0.0
                                entry_side = -1
                                entry_reason = "E2"
                        else:
                            entry_side = -1
                            entry_reason = "E2"

        if entry_side != 0:
            cci144_v = float(cci144_arr[i]) if i < len(cci144_arr) else np.nan
            adx14_v = float(adx14_arr[i]) if i < len(adx14_arr) else np.nan

            dist_ema = (cl - ema21_1h) if entry_side == 1 else (ema21_1h - cl)
            dist_ema_atr = dist_ema / a if a > 0 else 0.0
            chase_dist_atr = abs(dist_ema) / a if a > 0 else float("inf")

            entry_score = 1.0
            if entry_reason == "E2":
                entry_score += 0.5
            entry_score += max(0.0, min(float(dist_ema_atr), 2.0)) / 2.0
            entry_score += min(max(float(body_atr), 0.0), 2.0) / 2.0 * 0.5
            if touch_delta is not None:
                entry_score += 0.5 if int(touch_delta) <= 2 else (0.25 if int(touch_delta) <= int(p.x_touch) else 0.0)
            entry_score += min(max(float(breakout_atr), 0.0), 1.0) * 0.5

            if entry_reason == "E1":
                entry_score += min(max(float(e1_break_strength_atr), 0.0), 2.0) / 2.0 * 0.9
                entry_score += max(0.0, 1.0 - min(max(float(e1_retest_depth_atr), 0.0), 2.0) / 2.0) * 0.7
                if int(p.m_retest) > 0:
                    entry_score += max(0.0, 1.0 - min(float(e1_retest_bars), float(p.m_retest)) / float(p.m_retest)) * 0.6
                    entry_score += max(0.0, 1.0 - min(float(e1_touch_bars), float(p.m_retest)) / float(p.m_retest)) * 0.3
                entry_score += max(0.0, min(float(e1_atr_ratio) - 1.0, 0.5)) / 0.5 * 0.4

                if _E1_ADX_SCORE_ENABLED and (not pd.isna(adx14_v)):
                    if float(adx14_v) >= 25.0:
                        entry_score += 0.3
                    elif float(adx14_v) < 15.0:
                        entry_score -= 0.2

            e2_chase_max_atr = float("nan")
            e2_chase_blocked = False
            e2_chase_action = ""
            if entry_reason == "E2" and _E2_CHASE_ACTION != "off" and _E2_CHASE_MAX_ATR is not None and float(_E2_CHASE_MAX_ATR) > 0:
                e2_chase_max_atr = float(_E2_CHASE_MAX_ATR)
                e2_chase_action = str(_E2_CHASE_ACTION)
                e2_chase_blocked = bool(float(chase_dist_atr) >= float(_E2_CHASE_MAX_ATR))
                if e2_chase_blocked and emit_gate_log:
                    side_s0 = "LONG" if entry_side == 1 else "SHORT"
                    print(
                        f"[GATE] {str(sym).upper()} sig={entry_reason} side={side_s0} ts={str(idx[i])} "
                        f"chase={float(chase_dist_atr):.3f} e2_thr={float(_E2_CHASE_MAX_ATR):.3f} action={str(_E2_CHASE_ACTION)} -> E2_CHASE_BLOCK"
                    )
                if e2_chase_blocked and str(_E2_CHASE_ACTION) == "drop":
                    continue

            ema13_4h = float(ema13_4h_arr[i])
            ema55_4h = float(ema55_4h_arr[i])
            close_4h = float(close_4h_arr[i])
            ema144_4h = float(ema144_4h_arr[i])
            if (not pd.isna(ema13_4h)) and (not pd.isna(ema55_4h)) and a > 0:
                align = (ema13_4h - ema55_4h) / a if entry_side == 1 else (ema55_4h - ema13_4h) / a
                entry_score += max(0.0, min(float(align), 3.0)) / 3.0 * 0.9
            if (not pd.isna(close_4h)) and (not pd.isna(ema144_4h)) and a > 0:
                reg_dist = (close_4h - ema144_4h) / a if entry_side == 1 else (ema144_4h - close_4h) / a
                entry_score += max(0.0, min(float(reg_dist), 6.0)) / 6.0 * 0.5

            kk4 = float(kd_k_4h_arr[i])
            kd4 = float(kd_d_4h_arr[i])
            kk1 = float(kd_k_1d_arr[i])
            kd1 = float(kd_d_1d_arr[i])
            if (not pd.isna(kk4)) and (not pd.isna(kd4)) and (not pd.isna(kk1)) and (not pd.isna(kd1)):
                mom = ((kk4 - kd4) + (kk1 - kd1)) / 40.0
                if entry_side == -1:
                    mom = -mom
                entry_score += max(0.0, min(float(mom), 1.0)) * 0.7

            if entry_reason == "E1":
                squeeze = bool(bb_squeeze_4h_arr[i])
                if bool(p.enable_e1_bb_squeeze_veto) and squeeze:
                    continue
                if squeeze:
                    entry_score -= float(p.e1_bb_squeeze_penalty)

                if float(p.e1_min_break_strength_atr) > 0 and float(e1_break_strength_atr) < float(p.e1_min_break_strength_atr):
                    frac = (float(p.e1_min_break_strength_atr) - float(e1_break_strength_atr)) / float(p.e1_min_break_strength_atr)
                    entry_score -= min(max(float(frac), 0.0), 1.0) * 0.6
                if float(p.e1_max_retest_depth_atr) > 0 and float(e1_retest_depth_atr) > float(p.e1_max_retest_depth_atr):
                    frac = (float(e1_retest_depth_atr) - float(p.e1_max_retest_depth_atr)) / float(p.e1_max_retest_depth_atr)
                    entry_score -= min(max(float(frac), 0.0), 1.0) * 0.6

            cci_veto = bool(
                _E1_CCI144_VETO_ENABLED
                and entry_reason == "E1"
                and (not pd.isna(cci144_v))
                and float(cci144_v) < -144.0
            )
            if cci_veto:
                if emit_gate_this:
                    side_s0 = "LONG" if entry_side == 1 else "SHORT"
                    print(
                        f"[GATE] {str(sym).upper()} sig={entry_reason} side={side_s0} ts={str(idx[i])} cci144={float(cci144_v):.2f} "
                        f"cci_veto=True score={float(entry_score):.4f} th=NA score_pass=NA adx14={float(adx14_v):.2f} "
                        f"chase={float(chase_dist_atr):.3f} -> CCI_BLOCK"
                    )
                continue

            score_filter_th = float("nan")
            score_filter_pass = True
            if bool(p.enable_score_filter):
                th = float(p.min_score_to_trade)
                if entry_reason == "E1":
                    th = float(p.min_score_to_trade_e1)
                elif entry_reason == "E2":
                    th = float(p.min_score_to_trade_e2)
                score_filter_th = float(th)
                score_filter_pass = bool(float(entry_score) >= float(th))
                if not score_filter_pass:
                    if emit_gate_this:
                        side_s0 = "LONG" if entry_side == 1 else "SHORT"
                        cci_s = f"{float(cci144_v):.2f}" if not pd.isna(cci144_v) else "nan"
                        adx_s = f"{float(adx14_v):.2f}" if not pd.isna(adx14_v) else "nan"
                        print(
                            f"[GATE] {str(sym).upper()} sig={entry_reason} side={side_s0} ts={str(idx[i])} cci144={cci_s} "
                            f"cci_veto=False score={float(entry_score):.4f} th={float(th):.4f} score_pass=False adx14={adx_s} "
                            f"chase={float(chase_dist_atr):.3f} -> SCORE_BLOCK"
                        )
                    continue

            stop_k_use = float(p.stop_k_e1) if entry_reason == "E1" else float(p.stop_k)
            tick_volume_v = float(tv_arr[i]) if (i < len(tv_arr) and np.isfinite(tv_arr[i])) else float("nan")
            vol_sma20_v = _sma_last(tv_arr, 20, i)
            vol_ratio_v = float(tick_volume_v / vol_sma20_v) if (np.isfinite(tick_volume_v) and vol_sma20_v > 0) else float("nan")
            vol_pct_v = _pct_rank(tv_arr, 200, i)
            atr_sma50_v = _sma_last(atr_arr, 50, i)
            atr_rel_v = float(a / atr_sma50_v) if (atr_sma50_v > 0) else float("nan")
            atr_pct_v = _pct_rank(atr_arr, 200, i)
            spread_px_v = float("nan")
            spread_rel_v = float("nan")
            if i == len(df1) - 1:
                try:
                    bid, ask = _bid_ask(sym)
                    spread_px_v = float(abs(float(ask) - float(bid)))
                    spread_rel_v = float(spread_px_v / a) if a > 0 else float("inf")
                except Exception:
                    pass
            liq_gate_on_v = bool(_LIQUIDITY_GATE_ENABLED)
            liq_thr_v = float(_LIQUIDITY_MAX_SPREAD_REL)
            liquidity_risk_v = bool(np.isfinite(spread_rel_v) and spread_rel_v > liq_thr_v)
            vol_risk_ratio_max_v = float(_VOL_RISK_VOL_RATIO_MAX) if _VOL_RISK_VOL_RATIO_MAX is not None else float("nan")
            vol_risk_pct_max_v = float(_VOL_RISK_VOL_PCT_MAX) if _VOL_RISK_VOL_PCT_MAX is not None else float("nan")
            vol_risk_action_v = str(_VOL_RISK_ACTION)
            vol_risk_hit_v = bool(
                (np.isfinite(vol_ratio_v) and np.isfinite(vol_risk_ratio_max_v) and float(vol_ratio_v) > float(vol_risk_ratio_max_v))
                or (np.isfinite(vol_pct_v) and np.isfinite(vol_risk_pct_max_v) and float(vol_pct_v) > float(vol_risk_pct_max_v))
            )
            vol_risk_blocked_v = bool(vol_risk_hit_v and vol_risk_action_v in {"block", "drop"})
            stop = cl - stop_k_use * a if entry_side == 1 else cl + stop_k_use * a
            side_s = "LONG" if entry_side == 1 else "SHORT"
            breakout_level = float(level_long_arr[i]) if entry_side == 1 else float(level_short_arr[i])
            td = int(touch_delta) if touch_delta is not None else 0
            sr_support_v, sr_resistance_v, sr_sup_dist_atr_v, sr_res_dist_atr_v, sr_sup_t_v, sr_res_t_v = _sr_nearest_levels(
                h_arr,
                l_arr,
                float(cl),
                float(a),
                int(i),
                lookback=200,
                pivot=3,
                cluster_atr=0.25,
            )
            jg_macd_up_v = bool(jg_macd_up_arr[i]) if i < len(jg_macd_up_arr) else False
            jg_macd_down_v = bool(jg_macd_down_arr[i]) if i < len(jg_macd_down_arr) else False
            jg_sma175_v = float(jg_sma175_arr[i]) if (i < len(jg_sma175_arr) and np.isfinite(jg_sma175_arr[i])) else float("nan")
            jg_j_v = float(jg_j_arr[i]) if (i < len(jg_j_arr) and np.isfinite(jg_j_arr[i])) else float("nan")
            jg_long_v = bool(jg_macd_up_v and np.isfinite(jg_sma175_v) and float(cl) > float(jg_sma175_v) and np.isfinite(jg_j_v) and float(jg_j_v) < 80.0)
            jg_short_v = bool(jg_macd_down_v and np.isfinite(jg_sma175_v) and float(cl) < float(jg_sma175_v) and np.isfinite(jg_j_v) and float(jg_j_v) > 20.0)
            if emit_gate_this and liq_gate_on_v and liquidity_risk_v:
                print(
                    f"[GATE] {str(sym).upper()} sig={entry_reason} side={side_s} ts={str(idx[i])} "
                    f"spread_rel={float(spread_rel_v):.4f} thr={float(liq_thr_v):.4f} -> LIQUIDITY_BLOCK"
                )
            if emit_gate_this and vol_risk_hit_v and vol_risk_action_v != "off":
                vr_s = f"{float(vol_ratio_v):.3f}" if np.isfinite(vol_ratio_v) else "nan"
                vp_s = f"{float(vol_pct_v):.1f}" if np.isfinite(vol_pct_v) else "nan"
                rth_s = f"{float(vol_risk_ratio_max_v):.3f}" if np.isfinite(vol_risk_ratio_max_v) else ""
                pth_s = f"{float(vol_risk_pct_max_v):.1f}" if np.isfinite(vol_risk_pct_max_v) else ""
                print(
                    f"[GATE] {str(sym).upper()} sig={entry_reason} side={side_s} ts={str(idx[i])} "
                    f"vol_ratio={vr_s} rth={rth_s} vol_pct={vp_s} pth={pth_s} action={vol_risk_action_v} -> VOL_RISK"
                )
            if vol_risk_hit_v and vol_risk_action_v == "drop":
                continue
            if emit_gate_this and not (entry_reason == "E2" and e2_chase_blocked and _E2_CHASE_ACTION == "block") and not (liq_gate_on_v and liquidity_risk_v) and not (vol_risk_hit_v and vol_risk_action_v != "off"):
                cci_s = f"{float(cci144_v):.2f}" if not pd.isna(cci144_v) else "nan"
                adx_s = f"{float(adx14_v):.2f}" if not pd.isna(adx14_v) else "nan"
                th_s = f"{float(score_filter_th):.4f}" if not pd.isna(score_filter_th) else ""
                print(
                    f"[GATE] {str(sym).upper()} sig={entry_reason} side={side_s} ts={str(idx[i])} cci144={cci_s} "
                    f"cci_veto=False score={float(entry_score):.4f} th={th_s} score_pass={bool(score_filter_pass)} adx14={adx_s} "
                    f"chase={float(chase_dist_atr):.3f} -> ALLOW"
                )

            entry_score_gate_max_v = float(_ENTRY_SCORE_MAX) if _ENTRY_SCORE_MAX is not None else float("nan")
            entry_score_gate_action_v = str(_ENTRY_SCORE_ACTION)
            entry_score_gate_scope_v = str(_ENTRY_SCORE_SCOPE)
            entry_score_gate_hit_v = bool(False)
            entry_score_gate_blocked_v = bool(False)
            entry_score_gate_dyn_v = float("nan")
            if (
                _ENTRY_SCORE_VOL_MODE == "atr_rel_bins"
                and _ENTRY_SCORE_VOL_ATR_REL_CUTS is not None
                and _ENTRY_SCORE_VOL_MAXES is not None
                and float(cl) > 0
                and float(a) > 0
            ):
                atr_rel_px = float(a) / float(cl)
                if np.isfinite(atr_rel_px):
                    c1, c2 = _ENTRY_SCORE_VOL_ATR_REL_CUTS
                    m0, m1, m2 = _ENTRY_SCORE_VOL_MAXES
                    if float(atr_rel_px) < float(c1):
                        entry_score_gate_dyn_v = float(m0)
                    elif float(atr_rel_px) < float(c2):
                        entry_score_gate_dyn_v = float(m1)
                    else:
                        entry_score_gate_dyn_v = float(m2)
            max_use = entry_score_gate_dyn_v if np.isfinite(entry_score_gate_dyn_v) else float(entry_score_gate_max_v)
            entry_score_gate_max_v = float(max_use) if np.isfinite(max_use) else float("nan")
            if _ENTRY_SCORE_ACTION != "off" and np.isfinite(entry_score_gate_max_v) and float(entry_score_gate_max_v) > 0:
                if _ENTRY_SCORE_SCOPE == "all" or (_ENTRY_SCORE_SCOPE == "e2" and entry_reason == "E2"):
                    entry_score_gate_hit_v = bool(float(entry_score) > float(entry_score_gate_max_v))
                    entry_score_gate_blocked_v = bool(entry_score_gate_hit_v and _ENTRY_SCORE_ACTION in {"block", "drop"})
                    if entry_score_gate_hit_v and _ENTRY_SCORE_ACTION == "drop":
                        continue
            sigs.append(
                EntrySignal(
                ts=str(idx[i]),
                symbol=str(sym).upper(),
                side=side_s,
                signal=str(entry_reason),
                entry=float(cl),
                stop=float(stop),
                atr=float(a),
                entry_score=float(entry_score),
                ema21_1h=float(ema21_1h),
                breakout_level=float(breakout_level),
                touch_delta=td,
                strong=bool(strong_long if entry_side == 1 else strong_short),
                kd_w1_long=bool(kd_w1_long_arr[i]),
                kd_w1_short=bool(kd_w1_short_arr[i]),
                kd_3line_long=bool(kd_3line_long_arr[i]),
                kd_3line_short=bool(kd_3line_short_arr[i]),
                cci144=float(cci144_v) if not pd.isna(cci144_v) else float("nan"),
                cci_veto=False,
                adx14=float(adx14_v) if not pd.isna(adx14_v) else float("nan"),
                chase_dist_atr=float(chase_dist_atr),
                score_filter_th=float(score_filter_th) if not pd.isna(score_filter_th) else float("nan"),
                score_filter_pass=bool(score_filter_pass),
                e2_chase_max_atr=float(e2_chase_max_atr) if not pd.isna(e2_chase_max_atr) else float("nan"),
                e2_chase_blocked=bool(e2_chase_blocked),
                e2_chase_action=str(e2_chase_action),
                tick_volume=float(tick_volume_v) if np.isfinite(tick_volume_v) else float("nan"),
                vol_sma20=float(vol_sma20_v) if np.isfinite(vol_sma20_v) else float("nan"),
                vol_ratio=float(vol_ratio_v) if np.isfinite(vol_ratio_v) else float("nan"),
                vol_pct=float(vol_pct_v) if np.isfinite(vol_pct_v) else float("nan"),
                atr_sma50=float(atr_sma50_v) if np.isfinite(atr_sma50_v) else float("nan"),
                atr_rel=float(atr_rel_v) if np.isfinite(atr_rel_v) else float("nan"),
                atr_pct=float(atr_pct_v) if np.isfinite(atr_pct_v) else float("nan"),
                spread_px=float(spread_px_v) if np.isfinite(spread_px_v) else float("nan"),
                spread_rel=float(spread_rel_v) if np.isfinite(spread_rel_v) else float("nan"),
                liquidity_gate_enabled=bool(liq_gate_on_v),
                liquidity_max_spread_rel=float(liq_thr_v),
                liquidity_risk=bool(liquidity_risk_v),
                vol_risk_vol_ratio_max=float(vol_risk_ratio_max_v) if np.isfinite(vol_risk_ratio_max_v) else float("nan"),
                vol_risk_vol_pct_max=float(vol_risk_pct_max_v) if np.isfinite(vol_risk_pct_max_v) else float("nan"),
                vol_risk_action=str(vol_risk_action_v),
                vol_risk_blocked=bool(vol_risk_blocked_v),
                entry_score_gate_max=float(entry_score_gate_max_v) if np.isfinite(entry_score_gate_max_v) else float("nan"),
                entry_score_gate_action=str(entry_score_gate_action_v),
                entry_score_gate_scope=str(entry_score_gate_scope_v),
                entry_score_gate_hit=bool(entry_score_gate_hit_v),
                entry_score_gate_blocked=bool(entry_score_gate_blocked_v),
                sr_support=float(sr_support_v) if np.isfinite(sr_support_v) else float("nan"),
                sr_resistance=float(sr_resistance_v) if np.isfinite(sr_resistance_v) else float("nan"),
                sr_support_dist_atr=float(sr_sup_dist_atr_v) if np.isfinite(sr_sup_dist_atr_v) else float("nan"),
                sr_resistance_dist_atr=float(sr_res_dist_atr_v) if np.isfinite(sr_res_dist_atr_v) else float("nan"),
                sr_support_touches=int(sr_sup_t_v),
                sr_resistance_touches=int(sr_res_t_v),
                jg_macd_up=bool(jg_macd_up_v),
                jg_macd_down=bool(jg_macd_down_v),
                jg_sma175=float(jg_sma175_v) if np.isfinite(jg_sma175_v) else float("nan"),
                jg_j=float(jg_j_v) if np.isfinite(jg_j_v) else float("nan"),
                jg_long=bool(jg_long_v),
                jg_short=bool(jg_short_v),
                jg_ma13=float(jg_ma13_arr[i]) if (i < len(jg_ma13_arr) and np.isfinite(jg_ma13_arr[i])) else float("nan"),
                jg_ma55=float(jg_ma55_arr[i]) if (i < len(jg_ma55_arr) and np.isfinite(jg_ma55_arr[i])) else float("nan"),
                jg_ema20=float(jg_ema20_arr[i]) if (i < len(jg_ema20_arr) and np.isfinite(jg_ema20_arr[i])) else float("nan"),
                jg_ema27=float(jg_ema27_arr[i]) if (i < len(jg_ema27_arr) and np.isfinite(jg_ema27_arr[i])) else float("nan"),
                jg_ema29=float(jg_ema29_arr[i]) if (i < len(jg_ema29_arr) and np.isfinite(jg_ema29_arr[i])) else float("nan"),
                jg_ema32=float(jg_ema32_arr[i]) if (i < len(jg_ema32_arr) and np.isfinite(jg_ema32_arr[i])) else float("nan"),
                jg_ema36=float(jg_ema36_arr[i]) if (i < len(jg_ema36_arr) and np.isfinite(jg_ema36_arr[i])) else float("nan"),
                jg_pivot_mid=float(jg_pivot_mid_arr[i]) if (i < len(jg_pivot_mid_arr) and np.isfinite(jg_pivot_mid_arr[i])) else float("nan"),
                jg_b3=float(jg_b3_arr[i]) if (i < len(jg_b3_arr) and np.isfinite(jg_b3_arr[i])) else float("nan"),
                jg_s3=float(jg_s3_arr[i]) if (i < len(jg_s3_arr) and np.isfinite(jg_s3_arr[i])) else float("nan"),
                jg_b5=float(jg_b5_arr[i]) if (i < len(jg_b5_arr) and np.isfinite(jg_b5_arr[i])) else float("nan"),
                jg_s5=float(jg_s5_arr[i]) if (i < len(jg_s5_arr) and np.isfinite(jg_s5_arr[i])) else float("nan"),
                jg_var2=float(jg_var2_arr[i]) if (i < len(jg_var2_arr) and np.isfinite(jg_var2_arr[i])) else float("nan"),
                jg_var3=float(jg_var3_arr[i]) if (i < len(jg_var3_arr) and np.isfinite(jg_var3_arr[i])) else float("nan"),
                jg_var3_ma6=float(jg_var3_ma6_arr[i]) if (i < len(jg_var3_ma6_arr) and np.isfinite(jg_var3_ma6_arr[i])) else float("nan"),
                jg_bar_yellow=bool(jg_bar_yellow_arr[i]) if (i < len(jg_bar_yellow_arr)) else False,
                jg_bar_red=bool(jg_bar_red_arr[i]) if (i < len(jg_bar_red_arr)) else False,
                jg_macd=float(jg_macd_arr[i]) if (i < len(jg_macd_arr) and np.isfinite(jg_macd_arr[i])) else float("nan"),
                jg_buy=bool(jg_buy_arr[i]) if (i < len(jg_buy_arr)) else False,
                jg_sell=bool(jg_sell_arr[i]) if (i < len(jg_sell_arr)) else False,
                jg_gold=bool(jg_gold_arr[i]) if (i < len(jg_gold_arr)) else False,
                jg_ma160=float(jg_ma160_arr[i]) if (i < len(jg_ma160_arr) and np.isfinite(jg_ma160_arr[i])) else float("nan"),
                jg_ma120=float(jg_ma120_arr[i]) if (i < len(jg_ma120_arr) and np.isfinite(jg_ma120_arr[i])) else float("nan"),
                jg_ma60=float(jg_ma60_arr[i]) if (i < len(jg_ma60_arr) and np.isfinite(jg_ma60_arr[i])) else float("nan"),
                jg_ma25=float(jg_ma25_arr[i]) if (i < len(jg_ma25_arr) and np.isfinite(jg_ma25_arr[i])) else float("nan"),
                jg_flip_to_yellow=bool(jg_flip_to_yellow_arr[i]) if (i < len(jg_flip_to_yellow_arr)) else False,
                jg_flip_to_red=bool(jg_flip_to_red_arr[i]) if (i < len(jg_flip_to_red_arr)) else False,
                jg_wick_touch_ma13=bool(jg_wick_touch_ma13_arr[i]) if (i < len(jg_wick_touch_ma13_arr)) else False,
                jg_wick_touch_ma55=bool(jg_wick_touch_ma55_arr[i]) if (i < len(jg_wick_touch_ma55_arr)) else False,
                jg_wick_touch_ema27=bool(jg_wick_touch_ema27_arr[i]) if (i < len(jg_wick_touch_ema27_arr)) else False,
                jg_wick_touch_ema29=bool(jg_wick_touch_ema29_arr[i]) if (i < len(jg_wick_touch_ema29_arr)) else False,
                jg_wick_touch_ema32=bool(jg_wick_touch_ema32_arr[i]) if (i < len(jg_wick_touch_ema32_arr)) else False,
                jg_wick_touch_ema36=bool(jg_wick_touch_ema36_arr[i]) if (i < len(jg_wick_touch_ema36_arr)) else False,
                jg_close_breakdown_ma13=bool(jg_close_breakdown_ma13_arr[i]) if (i < len(jg_close_breakdown_ma13_arr)) else False,
                jg_close_breakup_ma13=bool(jg_close_breakup_ma13_arr[i]) if (i < len(jg_close_breakup_ma13_arr)) else False,
                jg_close_breakdown_ma55=bool(jg_close_breakdown_ma55_arr[i]) if (i < len(jg_close_breakdown_ma55_arr)) else False,
                jg_close_breakup_ma55=bool(jg_close_breakup_ma55_arr[i]) if (i < len(jg_close_breakup_ma55_arr)) else False,
                jg_cross_ma13_ema27_up=bool(jg_cross_ma13_ema27_up_arr[i]) if (i < len(jg_cross_ma13_ema27_up_arr)) else False,
                jg_cross_ma13_ema27_down=bool(jg_cross_ma13_ema27_down_arr[i]) if (i < len(jg_cross_ma13_ema27_down_arr)) else False,
                jg_cross_ma13_ema29_up=bool(jg_cross_ma13_ema29_up_arr[i]) if (i < len(jg_cross_ma13_ema29_up_arr)) else False,
                jg_cross_ma13_ema29_down=bool(jg_cross_ma13_ema29_down_arr[i]) if (i < len(jg_cross_ma13_ema29_down_arr)) else False,
                jg_cross_ma13_ema32_up=bool(jg_cross_ma13_ema32_up_arr[i]) if (i < len(jg_cross_ma13_ema32_up_arr)) else False,
                jg_cross_ma13_ema32_down=bool(jg_cross_ma13_ema32_down_arr[i]) if (i < len(jg_cross_ma13_ema32_down_arr)) else False,
                jg_cross_ma13_ema36_up=bool(jg_cross_ma13_ema36_up_arr[i]) if (i < len(jg_cross_ma13_ema36_up_arr)) else False,
                jg_cross_ma13_ema36_down=bool(jg_cross_ma13_ema36_down_arr[i]) if (i < len(jg_cross_ma13_ema36_down_arr)) else False,
                jg_after_cross_ma13_ema27_up_j_lt80=bool(jg_after_cross_ma13_ema27_up_j_lt80_arr[i]) if (i < len(jg_after_cross_ma13_ema27_up_j_lt80_arr)) else False,
                jg_after_cross_ma13_ema27_down_j_gt20=bool(jg_after_cross_ma13_ema27_down_j_gt20_arr[i]) if (i < len(jg_after_cross_ma13_ema27_down_j_gt20_arr)) else False,
                jg_dist_b3_atr=float(jg_dist_b3_atr_arr[i]) if (i < len(jg_dist_b3_atr_arr) and np.isfinite(jg_dist_b3_atr_arr[i])) else float("nan"),
                jg_dist_s3_atr=float(jg_dist_s3_atr_arr[i]) if (i < len(jg_dist_s3_atr_arr) and np.isfinite(jg_dist_s3_atr_arr[i])) else float("nan"),
                jg_dist_pivot_atr=float(jg_dist_pivot_atr_arr[i]) if (i < len(jg_dist_pivot_atr_arr) and np.isfinite(jg_dist_pivot_atr_arr[i])) else float("nan"),
                jg_red_streak=int(jg_red_streak_arr[i]) if (i < len(jg_red_streak_arr)) else 0,
                jg_yellow_streak=int(jg_yellow_streak_arr[i]) if (i < len(jg_yellow_streak_arr)) else 0,
            )
            )

    return sigs[-1] if (sigs and sigs[-1].ts == str(idx[-1])) else None


def _scan_entry_signals(symbol: str, p: Params, lookback_bars: int, emit_gate_log: bool = False) -> List[EntrySignal]:
    sym = _resolve_symbol(symbol)
    df1 = _mt5_rates(sym, mt5.TIMEFRAME_H1, int(600))
    df4 = _mt5_rates(sym, mt5.TIMEFRAME_H4, int(400))
    dfd = _mt5_rates(sym, mt5.TIMEFRAME_D1, int(300))
    df1 = df1.copy()
    df1["atr"] = atr(df1, int(p.atr_n))
    tr = compute_trend_flags(df1, df4, dfd, p)
    tr = tr.reindex(df1.index)

    if len(df1) < int(max(p.n_break + 5, p.atr_n + 5, 60)):
        return []
    o_arr = df1["open"].to_numpy(dtype=float)
    h_arr = df1["high"].to_numpy(dtype=float)
    l_arr = df1["low"].to_numpy(dtype=float)
    c_arr = df1["close"].to_numpy(dtype=float)
    atr_arr = df1["atr"].to_numpy(dtype=float)
    tv_arr = df1["tick_volume"].to_numpy(dtype=float) if "tick_volume" in df1.columns else np.full(len(df1), np.nan, dtype=float)

    adx14_df = _adx_from_ohlc(df1["high"], df1["low"], df1["close"], 14)
    adx14_arr = adx14_df["adx"].to_numpy(dtype=float)
    cci144_arr = _cci_from_ohlc(df1["high"], df1["low"], df1["close"], 144).to_numpy(dtype=float)
    zrf_h1 = _zrf_macd_from_close(df1["close"])
    jg_macd_up_arr = _cross_up(zrf_h1["zrf_diff"], zrf_h1["zrf_dea"]).to_numpy(dtype=bool)
    jg_macd_down_arr = _cross_down(zrf_h1["zrf_diff"], zrf_h1["zrf_dea"]).to_numpy(dtype=bool)
    jg_sma175_arr = (
        pd.to_numeric(df1["close"], errors="coerce")
        .rolling(175, min_periods=175)
        .mean()
        .to_numpy(dtype=float)
    )
    jg_j_arr = _stoch_kdj_from_ohlc(df1["high"], df1["low"], df1["close"], 9, 3, 3)["j"].to_numpy(dtype=float)
    jg_df = _jinding_features(df1)
    jg_ma13_arr = jg_df["jg_ma13"].to_numpy(dtype=float)
    jg_ma55_arr = jg_df["jg_ma55"].to_numpy(dtype=float)
    jg_ema20_arr = jg_df["jg_ema20"].to_numpy(dtype=float)
    jg_ema27_arr = jg_df["jg_ema27"].to_numpy(dtype=float)
    jg_ema29_arr = jg_df["jg_ema29"].to_numpy(dtype=float)
    jg_ema32_arr = jg_df["jg_ema32"].to_numpy(dtype=float)
    jg_ema36_arr = jg_df["jg_ema36"].to_numpy(dtype=float)
    jg_pivot_mid_arr = jg_df["jg_pivot_mid"].to_numpy(dtype=float)
    jg_b3_arr = jg_df["jg_b3"].to_numpy(dtype=float)
    jg_s3_arr = jg_df["jg_s3"].to_numpy(dtype=float)
    jg_b5_arr = jg_df["jg_b5"].to_numpy(dtype=float)
    jg_s5_arr = jg_df["jg_s5"].to_numpy(dtype=float)
    jg_var2_arr = jg_df["jg_var2"].to_numpy(dtype=float)
    jg_var3_arr = jg_df["jg_var3"].to_numpy(dtype=float)
    jg_var3_ma6_arr = jg_df["jg_var3_ma6"].to_numpy(dtype=float)
    jg_bar_yellow_arr = jg_df["jg_bar_yellow"].to_numpy(dtype=bool)
    jg_bar_red_arr = jg_df["jg_bar_red"].to_numpy(dtype=bool)
    jg_flip_to_yellow_arr = jg_df["jg_flip_to_yellow"].to_numpy(dtype=bool)
    jg_flip_to_red_arr = jg_df["jg_flip_to_red"].to_numpy(dtype=bool)
    jg_macd_arr = jg_df["jg_macd"].to_numpy(dtype=float)
    jg_buy_arr = jg_df["jg_buy"].to_numpy(dtype=bool)
    jg_sell_arr = jg_df["jg_sell"].to_numpy(dtype=bool)
    jg_gold_arr = jg_df["jg_gold"].to_numpy(dtype=bool)
    jg_ma160_arr = jg_df["jg_ma160"].to_numpy(dtype=float)
    jg_ma120_arr = jg_df["jg_ma120"].to_numpy(dtype=float)
    jg_ma60_arr = jg_df["jg_ma60"].to_numpy(dtype=float)
    jg_ma25_arr = jg_df["jg_ma25"].to_numpy(dtype=float)
    jg_wick_touch_ma13_arr = jg_df["jg_wick_touch_ma13"].to_numpy(dtype=bool)
    jg_wick_touch_ma55_arr = jg_df["jg_wick_touch_ma55"].to_numpy(dtype=bool)
    jg_wick_touch_ema27_arr = jg_df["jg_wick_touch_ema27"].to_numpy(dtype=bool)
    jg_wick_touch_ema29_arr = jg_df["jg_wick_touch_ema29"].to_numpy(dtype=bool)
    jg_wick_touch_ema32_arr = jg_df["jg_wick_touch_ema32"].to_numpy(dtype=bool)
    jg_wick_touch_ema36_arr = jg_df["jg_wick_touch_ema36"].to_numpy(dtype=bool)
    jg_close_breakdown_ma13_arr = jg_df["jg_close_breakdown_ma13"].to_numpy(dtype=bool)
    jg_close_breakup_ma13_arr = jg_df["jg_close_breakup_ma13"].to_numpy(dtype=bool)
    jg_close_breakdown_ma55_arr = jg_df["jg_close_breakdown_ma55"].to_numpy(dtype=bool)
    jg_close_breakup_ma55_arr = jg_df["jg_close_breakup_ma55"].to_numpy(dtype=bool)
    jg_cross_ma13_ema27_up_arr = jg_df["jg_cross_ma13_ema27_up"].to_numpy(dtype=bool)
    jg_cross_ma13_ema27_down_arr = jg_df["jg_cross_ma13_ema27_down"].to_numpy(dtype=bool)
    jg_cross_ma13_ema29_up_arr = jg_df["jg_cross_ma13_ema29_up"].to_numpy(dtype=bool)
    jg_cross_ma13_ema29_down_arr = jg_df["jg_cross_ma13_ema29_down"].to_numpy(dtype=bool)
    jg_cross_ma13_ema32_up_arr = jg_df["jg_cross_ma13_ema32_up"].to_numpy(dtype=bool)
    jg_cross_ma13_ema32_down_arr = jg_df["jg_cross_ma13_ema32_down"].to_numpy(dtype=bool)
    jg_cross_ma13_ema36_up_arr = jg_df["jg_cross_ma13_ema36_up"].to_numpy(dtype=bool)
    jg_cross_ma13_ema36_down_arr = jg_df["jg_cross_ma13_ema36_down"].to_numpy(dtype=bool)
    jg_after_cross_ma13_ema27_up_j_lt80_arr = jg_df["jg_after_cross_ma13_ema27_up_j_lt80"].to_numpy(dtype=bool)
    jg_after_cross_ma13_ema27_down_j_gt20_arr = jg_df["jg_after_cross_ma13_ema27_down_j_gt20"].to_numpy(dtype=bool)
    jg_dist_b3_atr_arr = jg_df["jg_dist_b3_atr"].to_numpy(dtype=float)
    jg_dist_s3_atr_arr = jg_df["jg_dist_s3_atr"].to_numpy(dtype=float)
    jg_dist_pivot_atr_arr = jg_df["jg_dist_pivot_atr"].to_numpy(dtype=float)
    jg_red_streak_arr = jg_df["jg_red_streak"].to_numpy(dtype=int)
    jg_yellow_streak_arr = jg_df["jg_yellow_streak"].to_numpy(dtype=int)

    strong_long_arr = tr["strong_long"].to_numpy(dtype=bool)
    strong_short_arr = tr["strong_short"].to_numpy(dtype=bool)
    regime_long_arr = tr["regime_long"].to_numpy(dtype=bool)
    regime_short_arr = tr["regime_short"].to_numpy(dtype=bool)
    confirm_long_arr = tr["confirm_long"].to_numpy(dtype=bool)
    confirm_short_arr = tr["confirm_short"].to_numpy(dtype=bool)
    ema21_1h_arr = tr["ema21_1h"].to_numpy(dtype=float)
    ema13_4h_arr = tr["ema13_4h"].to_numpy(dtype=float)
    ema55_4h_arr = tr["ema55_4h"].to_numpy(dtype=float)
    ema144_4h_arr = tr["ema144_4h"].to_numpy(dtype=float)
    close_4h_arr = tr["close_4h"].to_numpy(dtype=float)
    kd_k_4h_arr = tr["kd_k_4h"].to_numpy(dtype=float)
    kd_d_4h_arr = tr["kd_d_4h"].to_numpy(dtype=float)
    kd_k_1d_arr = tr["kd_k_1d"].to_numpy(dtype=float)
    kd_d_1d_arr = tr["kd_d_1d"].to_numpy(dtype=float)
    kd_w1_long_arr = tr["kd_w1_long"].to_numpy(dtype=bool) if "kd_w1_long" in tr.columns else np.zeros(len(df1), dtype=bool)
    kd_w1_short_arr = tr["kd_w1_short"].to_numpy(dtype=bool) if "kd_w1_short" in tr.columns else np.zeros(len(df1), dtype=bool)
    kd_3line_long_arr = tr["kd_3line_long"].to_numpy(dtype=bool) if "kd_3line_long" in tr.columns else np.zeros(len(df1), dtype=bool)
    kd_3line_short_arr = tr["kd_3line_short"].to_numpy(dtype=bool) if "kd_3line_short" in tr.columns else np.zeros(len(df1), dtype=bool)
    bb_squeeze_4h_arr = tr["bb_squeeze_4h"].to_numpy(dtype=bool)

    level_long_arr = df1["high"].rolling(int(p.n_break), min_periods=int(p.n_break)).max().shift(1).to_numpy(dtype=float)
    level_short_arr = df1["low"].rolling(int(p.n_break), min_periods=int(p.n_break)).min().shift(1).to_numpy(dtype=float)

    e1_state: Optional[str] = None
    e1_dir = 0
    e1_level = np.nan
    e1_start_i = -1
    e1_end_i = -1
    e1_touched = False
    e1_break_i = -1
    e1_break_atr = np.nan
    e1_break_strength_atr_state = 0.0
    e1_touch_i = -1
    e1_retest_depth_atr_state = 0.0
    last_touch_i_long: Optional[int] = None
    last_touch_i_short: Optional[int] = None

    idx = df1.index
    lb = max(1, int(lookback_bars))
    keep_start = max(0, len(df1) - lb)
    keep_ts = set(str(x) for x in idx[-lb:])
    sigs: List[EntrySignal] = []
    for i in range(len(df1)):
        emit_gate_this = bool(emit_gate_log) and (i >= keep_start)
        o = float(o_arr[i])
        h = float(h_arr[i])
        l = float(l_arr[i])
        cl = float(c_arr[i])
        a = float(atr_arr[i])
        if not (a > 0) or pd.isna(a) or pd.isna(cl) or pd.isna(o) or pd.isna(h) or pd.isna(l):
            continue

        strong_long = bool(strong_long_arr[i])
        strong_short = bool(strong_short_arr[i])
        gate_long = strong_long if bool(p.require_strong_for_entry) else (bool(regime_long_arr[i]) and bool(confirm_long_arr[i]))
        gate_short = strong_short if bool(p.require_strong_for_entry) else (bool(regime_short_arr[i]) and bool(confirm_short_arr[i]))

        ema21_1h = float(ema21_1h_arr[i])
        if (not bool(p.enable_e2_touch_requires_strong)) or strong_long:
            if l <= ema21_1h - float(p.touch_k) * a:
                last_touch_i_long = i
        if (not bool(p.enable_e2_touch_requires_strong)) or strong_short:
            if h >= ema21_1h + float(p.touch_k) * a:
                last_touch_i_short = i

        e1_entry = False
        e1_entry_side = 0
        e1_break_strength_atr = 0.0
        e1_retest_depth_atr = 0.0
        e1_retest_bars = 0
        e1_touch_bars = 0
        e1_atr_ratio = 1.0
        touch_delta: Optional[int] = None
        body_atr = 0.0
        breakout_atr = 0.0

        if gate_long or gate_short:
            if e1_state is None:
                if gate_long:
                    level_long = float(level_long_arr[i])
                    if (not pd.isna(level_long)) and cl > level_long:
                        e1_state = "await"
                        e1_dir = 1
                        e1_level = float(level_long)
                        e1_start_i = i + 1
                        e1_end_i = i + int(p.m_retest)
                        e1_touched = False
                        e1_break_i = i
                        e1_break_atr = a
                        e1_break_strength_atr_state = (cl - e1_level) / a if a > 0 else 0.0
                        e1_touch_i = -1
                        e1_retest_depth_atr_state = 0.0
                elif gate_short:
                    level_short = float(level_short_arr[i])
                    if (not pd.isna(level_short)) and cl < level_short:
                        e1_state = "await"
                        e1_dir = -1
                        e1_level = float(level_short)
                        e1_start_i = i + 1
                        e1_end_i = i + int(p.m_retest)
                        e1_touched = False
                        e1_break_i = i
                        e1_break_atr = a
                        e1_break_strength_atr_state = (e1_level - cl) / a if a > 0 else 0.0
                        e1_touch_i = -1
                        e1_retest_depth_atr_state = 0.0
            else:
                if i < e1_start_i or i > e1_end_i:
                    e1_state = None
                else:
                    band_low = float(e1_level) - float(p.k) * a
                    band_high = float(e1_level) + float(p.k) * a
                    touched = (l <= band_high) and (h >= band_low)
                    if touched:
                        e1_touched = True
                        if e1_touch_i < 0:
                            e1_touch_i = i
                    if e1_dir == 1:
                        depth_atr = (float(e1_level) - l) / a if a > 0 else 0.0
                    else:
                        depth_atr = (h - float(e1_level)) / a if a > 0 else 0.0
                    if float(depth_atr) > float(e1_retest_depth_atr_state):
                        e1_retest_depth_atr_state = float(depth_atr)

                    fail = False
                    if float(p.e1_fail_k) > 0:
                        if e1_dir == 1:
                            fail = cl < (float(e1_level) - float(p.e1_fail_k) * a)
                        else:
                            fail = cl > (float(e1_level) + float(p.e1_fail_k) * a)
                    if fail:
                        e1_state = None
                    else:
                        confirmed = (cl >= float(e1_level)) if e1_dir == 1 else (cl <= float(e1_level))
                        if e1_touched and confirmed:
                            e1_entry = True
                            e1_entry_side = int(e1_dir)
                            breakout_atr = abs(cl - float(e1_level)) / a if a > 0 else 0.0
                            e1_break_strength_atr = float(e1_break_strength_atr_state)
                            e1_retest_depth_atr = float(e1_retest_depth_atr_state)
                            e1_retest_bars = int(i - e1_break_i) if e1_break_i >= 0 else 0
                            e1_touch_bars = int(i - e1_touch_i) if e1_touch_i >= 0 else e1_retest_bars
                            e1_atr_ratio = float(a / e1_break_atr) if (e1_break_atr is not None and not pd.isna(e1_break_atr) and float(e1_break_atr) > 0) else 1.0
                            e1_state = None

        if e1_entry:
            entry_side = int(e1_entry_side)
            entry_reason = "E1"
        else:
            entry_side = 0
            entry_reason = ""
            if gate_long:
                touched_ok = last_touch_i_long is not None and 1 <= i - int(last_touch_i_long) <= int(p.x_touch)
                if touched_ok:
                    touch_delta = i - int(last_touch_i_long)
                    body = abs(cl - o)
                    body_atr = body / a if a > 0 else 0.0
                    wick_ok = l >= ema21_1h - float(p.shadow_k) * a
                    reclaim = (cl > ema21_1h) and (cl > o) and (body >= float(p.body_k) * a) and wick_ok
                    if reclaim:
                        if bool(p.enable_e2_break_confirm):
                            level_long = float(level_long_arr[i])
                            if (not pd.isna(level_long)) and (cl > level_long):
                                breakout_atr = (cl - level_long) / a if a > 0 else 0.0
                                entry_side = 1
                                entry_reason = "E2"
                        else:
                            entry_side = 1
                            entry_reason = "E2"
            elif gate_short:
                touched_ok = last_touch_i_short is not None and 1 <= i - int(last_touch_i_short) <= int(p.x_touch)
                if touched_ok:
                    touch_delta = i - int(last_touch_i_short)
                    body = abs(cl - o)
                    body_atr = body / a if a > 0 else 0.0
                    wick_ok = h <= ema21_1h + float(p.shadow_k) * a
                    reclaim = (cl < ema21_1h) and (cl < o) and (body >= float(p.body_k) * a) and wick_ok
                    if reclaim:
                        if bool(p.enable_e2_break_confirm):
                            level_short = float(level_short_arr[i])
                            if (not pd.isna(level_short)) and (cl < level_short):
                                breakout_atr = (level_short - cl) / a if a > 0 else 0.0
                                entry_side = -1
                                entry_reason = "E2"
                        else:
                            entry_side = -1
                            entry_reason = "E2"

        if entry_side != 0:
            cci144_v = float(cci144_arr[i]) if i < len(cci144_arr) else np.nan
            adx14_v = float(adx14_arr[i]) if i < len(adx14_arr) else np.nan

            dist_ema = (cl - ema21_1h) if entry_side == 1 else (ema21_1h - cl)
            dist_ema_atr = dist_ema / a if a > 0 else 0.0
            chase_dist_atr = abs(dist_ema) / a if a > 0 else float("inf")

            entry_score = 1.0
            if entry_reason == "E2":
                entry_score += 0.5
            entry_score += max(0.0, min(float(dist_ema_atr), 2.0)) / 2.0
            entry_score += min(max(float(body_atr), 0.0), 2.0) / 2.0 * 0.5
            if touch_delta is not None:
                entry_score += 0.5 if int(touch_delta) <= 2 else (0.25 if int(touch_delta) <= int(p.x_touch) else 0.0)
            entry_score += min(max(float(breakout_atr), 0.0), 1.0) * 0.5

            if entry_reason == "E1":
                entry_score += min(max(float(e1_break_strength_atr), 0.0), 2.0) / 2.0 * 0.9
                entry_score += max(0.0, 1.0 - min(max(float(e1_retest_depth_atr), 0.0), 2.0) / 2.0) * 0.7
                if int(p.m_retest) > 0:
                    entry_score += max(0.0, 1.0 - min(float(e1_retest_bars), float(p.m_retest)) / float(p.m_retest)) * 0.6
                    entry_score += max(0.0, 1.0 - min(float(e1_touch_bars), float(p.m_retest)) / float(p.m_retest)) * 0.3
                entry_score += max(0.0, min(float(e1_atr_ratio) - 1.0, 0.5)) / 0.5 * 0.4
                if _E1_ADX_SCORE_ENABLED and (not pd.isna(adx14_v)):
                    if float(adx14_v) >= 25.0:
                        entry_score += 0.3
                    elif float(adx14_v) < 15.0:
                        entry_score -= 0.2

            e2_chase_max_atr = float("nan")
            e2_chase_blocked = False
            e2_chase_action = ""
            if entry_reason == "E2" and _E2_CHASE_ACTION != "off" and _E2_CHASE_MAX_ATR is not None and float(_E2_CHASE_MAX_ATR) > 0:
                e2_chase_max_atr = float(_E2_CHASE_MAX_ATR)
                e2_chase_action = str(_E2_CHASE_ACTION)
                e2_chase_blocked = bool(float(chase_dist_atr) >= float(_E2_CHASE_MAX_ATR))
                if e2_chase_blocked and emit_gate_this:
                    side_s0 = "LONG" if entry_side == 1 else "SHORT"
                    print(
                        f"[GATE] {str(sym).upper()} sig={entry_reason} side={side_s0} ts={str(idx[i])} "
                        f"chase={float(chase_dist_atr):.3f} e2_thr={float(_E2_CHASE_MAX_ATR):.3f} action={str(_E2_CHASE_ACTION)} -> E2_CHASE_BLOCK"
                    )
                if e2_chase_blocked and str(_E2_CHASE_ACTION) == "drop":
                    continue

            ema13_4h = float(ema13_4h_arr[i])
            ema55_4h = float(ema55_4h_arr[i])
            close_4h = float(close_4h_arr[i])
            ema144_4h = float(ema144_4h_arr[i])
            if (not pd.isna(ema13_4h)) and (not pd.isna(ema55_4h)) and a > 0:
                align = (ema13_4h - ema55_4h) / a if entry_side == 1 else (ema55_4h - ema13_4h) / a
                entry_score += max(0.0, min(float(align), 3.0)) / 3.0 * 0.9
            if (not pd.isna(close_4h)) and (not pd.isna(ema144_4h)) and a > 0:
                reg_dist = (close_4h - ema144_4h) / a if entry_side == 1 else (ema144_4h - close_4h) / a
                entry_score += max(0.0, min(float(reg_dist), 6.0)) / 6.0 * 0.5

            kk4 = float(kd_k_4h_arr[i])
            kd4 = float(kd_d_4h_arr[i])
            kk1 = float(kd_k_1d_arr[i])
            kd1 = float(kd_d_1d_arr[i])
            if (not pd.isna(kk4)) and (not pd.isna(kd4)) and (not pd.isna(kk1)) and (not pd.isna(kd1)):
                mom = ((kk4 - kd4) + (kk1 - kd1)) / 40.0
                if entry_side == -1:
                    mom = -mom
                entry_score += max(0.0, min(float(mom), 1.0)) * 0.7

            if entry_reason == "E1":
                squeeze = bool(bb_squeeze_4h_arr[i])
                if bool(p.enable_e1_bb_squeeze_veto) and squeeze:
                    continue
                if squeeze:
                    entry_score -= float(p.e1_bb_squeeze_penalty)

                if float(p.e1_min_break_strength_atr) > 0 and float(e1_break_strength_atr) < float(p.e1_min_break_strength_atr):
                    frac = (float(p.e1_min_break_strength_atr) - float(e1_break_strength_atr)) / float(p.e1_min_break_strength_atr)
                    entry_score -= min(max(float(frac), 0.0), 1.0) * 0.6
                if float(p.e1_max_retest_depth_atr) > 0 and float(e1_retest_depth_atr) > float(p.e1_max_retest_depth_atr):
                    frac = (float(e1_retest_depth_atr) - float(p.e1_max_retest_depth_atr)) / float(p.e1_max_retest_depth_atr)
                    entry_score -= min(max(float(frac), 0.0), 1.0) * 0.6

            cci_veto = bool(
                _E1_CCI144_VETO_ENABLED
                and entry_reason == "E1"
                and (not pd.isna(cci144_v))
                and float(cci144_v) < -144.0
            )
            if cci_veto:
                if emit_gate_this:
                    side_s0 = "LONG" if entry_side == 1 else "SHORT"
                    print(
                        f"[GATE] {str(sym).upper()} sig={entry_reason} side={side_s0} ts={str(idx[i])} cci144={float(cci144_v):.2f} "
                        f"cci_veto=True score={float(entry_score):.4f} th=NA score_pass=NA adx14={float(adx14_v):.2f} "
                        f"chase={float(chase_dist_atr):.3f} -> CCI_BLOCK"
                    )
                continue

            score_filter_th = float("nan")
            score_filter_pass = True
            if bool(p.enable_score_filter):
                th = float(p.min_score_to_trade)
                if entry_reason == "E1":
                    th = float(p.min_score_to_trade_e1)
                elif entry_reason == "E2":
                    th = float(p.min_score_to_trade_e2)
                score_filter_th = float(th)
                score_filter_pass = bool(float(entry_score) >= float(th))
                if not score_filter_pass:
                    if emit_gate_this:
                        side_s0 = "LONG" if entry_side == 1 else "SHORT"
                        cci_s = f"{float(cci144_v):.2f}" if not pd.isna(cci144_v) else "nan"
                        adx_s = f"{float(adx14_v):.2f}" if not pd.isna(adx14_v) else "nan"
                        print(
                            f"[GATE] {str(sym).upper()} sig={entry_reason} side={side_s0} ts={str(idx[i])} cci144={cci_s} "
                            f"cci_veto=False score={float(entry_score):.4f} th={float(th):.4f} score_pass=False adx14={adx_s} "
                            f"chase={float(chase_dist_atr):.3f} -> SCORE_BLOCK"
                        )
                    continue

            stop_k_use = float(p.stop_k_e1) if entry_reason == "E1" else float(p.stop_k)
            tick_volume_v = float(tv_arr[i]) if (i < len(tv_arr) and np.isfinite(tv_arr[i])) else float("nan")
            vol_sma20_v = _sma_last(tv_arr, 20, i)
            vol_ratio_v = float(tick_volume_v / vol_sma20_v) if (np.isfinite(tick_volume_v) and vol_sma20_v > 0) else float("nan")
            vol_pct_v = _pct_rank(tv_arr, 200, i)
            atr_sma50_v = _sma_last(atr_arr, 50, i)
            atr_rel_v = float(a / atr_sma50_v) if (atr_sma50_v > 0) else float("nan")
            atr_pct_v = _pct_rank(atr_arr, 200, i)
            spread_px_v = float("nan")
            spread_rel_v = float("nan")
            if i == len(df1) - 1:
                try:
                    bid, ask = _bid_ask(sym)
                    spread_px_v = float(abs(float(ask) - float(bid)))
                    spread_rel_v = float(spread_px_v / a) if a > 0 else float("inf")
                except Exception:
                    pass
            liq_gate_on_v = bool(_LIQUIDITY_GATE_ENABLED)
            liq_thr_v = float(_LIQUIDITY_MAX_SPREAD_REL)
            liquidity_risk_v = bool(np.isfinite(spread_rel_v) and spread_rel_v > liq_thr_v)
            vol_risk_ratio_max_v = float(_VOL_RISK_VOL_RATIO_MAX) if _VOL_RISK_VOL_RATIO_MAX is not None else float("nan")
            vol_risk_pct_max_v = float(_VOL_RISK_VOL_PCT_MAX) if _VOL_RISK_VOL_PCT_MAX is not None else float("nan")
            vol_risk_action_v = str(_VOL_RISK_ACTION)
            vol_risk_hit_v = bool(
                (np.isfinite(vol_ratio_v) and np.isfinite(vol_risk_ratio_max_v) and float(vol_ratio_v) > float(vol_risk_ratio_max_v))
                or (np.isfinite(vol_pct_v) and np.isfinite(vol_risk_pct_max_v) and float(vol_pct_v) > float(vol_risk_pct_max_v))
            )
            vol_risk_blocked_v = bool(vol_risk_hit_v and vol_risk_action_v in {"block", "drop"})
            stop = cl - stop_k_use * a if entry_side == 1 else cl + stop_k_use * a
            side_s = "LONG" if entry_side == 1 else "SHORT"
            breakout_level = float(level_long_arr[i]) if entry_side == 1 else float(level_short_arr[i])
            td = int(touch_delta) if touch_delta is not None else 0
            sr_support_v, sr_resistance_v, sr_sup_dist_atr_v, sr_res_dist_atr_v, sr_sup_t_v, sr_res_t_v = _sr_nearest_levels(
                h_arr,
                l_arr,
                float(cl),
                float(a),
                int(i),
                lookback=200,
                pivot=3,
                cluster_atr=0.25,
            )
            jg_macd_up_v = bool(jg_macd_up_arr[i]) if i < len(jg_macd_up_arr) else False
            jg_macd_down_v = bool(jg_macd_down_arr[i]) if i < len(jg_macd_down_arr) else False
            jg_sma175_v = float(jg_sma175_arr[i]) if (i < len(jg_sma175_arr) and np.isfinite(jg_sma175_arr[i])) else float("nan")
            jg_j_v = float(jg_j_arr[i]) if (i < len(jg_j_arr) and np.isfinite(jg_j_arr[i])) else float("nan")
            jg_long_v = bool(jg_macd_up_v and np.isfinite(jg_sma175_v) and float(cl) > float(jg_sma175_v) and np.isfinite(jg_j_v) and float(jg_j_v) < 80.0)
            jg_short_v = bool(jg_macd_down_v and np.isfinite(jg_sma175_v) and float(cl) < float(jg_sma175_v) and np.isfinite(jg_j_v) and float(jg_j_v) > 20.0)
            if emit_gate_this and liq_gate_on_v and liquidity_risk_v:
                print(
                    f"[GATE] {str(sym).upper()} sig={entry_reason} side={side_s} ts={str(idx[i])} "
                    f"spread_rel={float(spread_rel_v):.4f} thr={float(liq_thr_v):.4f} -> LIQUIDITY_BLOCK"
                )
            if emit_gate_this and vol_risk_hit_v and vol_risk_action_v != "off":
                vr_s = f"{float(vol_ratio_v):.3f}" if np.isfinite(vol_ratio_v) else "nan"
                vp_s = f"{float(vol_pct_v):.1f}" if np.isfinite(vol_pct_v) else "nan"
                rth_s = f"{float(vol_risk_ratio_max_v):.3f}" if np.isfinite(vol_risk_ratio_max_v) else ""
                pth_s = f"{float(vol_risk_pct_max_v):.1f}" if np.isfinite(vol_risk_pct_max_v) else ""
                print(
                    f"[GATE] {str(sym).upper()} sig={entry_reason} side={side_s} ts={str(idx[i])} "
                    f"vol_ratio={vr_s} rth={rth_s} vol_pct={vp_s} pth={pth_s} action={vol_risk_action_v} -> VOL_RISK"
                )
            if vol_risk_hit_v and vol_risk_action_v == "drop":
                continue
            if emit_gate_this and not (entry_reason == "E2" and e2_chase_blocked and _E2_CHASE_ACTION == "block") and not (liq_gate_on_v and liquidity_risk_v) and not (vol_risk_hit_v and vol_risk_action_v != "off"):
                cci_s = f"{float(cci144_v):.2f}" if not pd.isna(cci144_v) else "nan"
                adx_s = f"{float(adx14_v):.2f}" if not pd.isna(adx14_v) else "nan"
                th_s = f"{float(score_filter_th):.4f}" if not pd.isna(score_filter_th) else ""
                print(
                    f"[GATE] {str(sym).upper()} sig={entry_reason} side={side_s} ts={str(idx[i])} cci144={cci_s} "
                    f"cci_veto=False score={float(entry_score):.4f} th={th_s} score_pass={bool(score_filter_pass)} adx14={adx_s} "
                    f"chase={float(chase_dist_atr):.3f} -> ALLOW"
                )
            sigs.append(
                EntrySignal(
                    ts=str(idx[i]),
                    symbol=str(sym).upper(),
                    side=side_s,
                    signal=str(entry_reason),
                    entry=float(cl),
                    stop=float(stop),
                    atr=float(a),
                    entry_score=float(entry_score),
                    ema21_1h=float(ema21_1h),
                    breakout_level=float(breakout_level),
                    touch_delta=td,
                    strong=bool(strong_long if entry_side == 1 else strong_short),
                kd_w1_long=bool(kd_w1_long_arr[i]),
                kd_w1_short=bool(kd_w1_short_arr[i]),
                kd_3line_long=bool(kd_3line_long_arr[i]),
                kd_3line_short=bool(kd_3line_short_arr[i]),
                cci144=float(cci144_v) if not pd.isna(cci144_v) else float("nan"),
                cci_veto=False,
                adx14=float(adx14_v) if not pd.isna(adx14_v) else float("nan"),
                chase_dist_atr=float(chase_dist_atr),
                score_filter_th=float(score_filter_th) if not pd.isna(score_filter_th) else float("nan"),
                score_filter_pass=bool(score_filter_pass),
                e2_chase_max_atr=float(e2_chase_max_atr) if not pd.isna(e2_chase_max_atr) else float("nan"),
                e2_chase_blocked=bool(e2_chase_blocked),
                e2_chase_action=str(e2_chase_action),
                tick_volume=float(tick_volume_v) if np.isfinite(tick_volume_v) else float("nan"),
                vol_sma20=float(vol_sma20_v) if np.isfinite(vol_sma20_v) else float("nan"),
                vol_ratio=float(vol_ratio_v) if np.isfinite(vol_ratio_v) else float("nan"),
                vol_pct=float(vol_pct_v) if np.isfinite(vol_pct_v) else float("nan"),
                atr_sma50=float(atr_sma50_v) if np.isfinite(atr_sma50_v) else float("nan"),
                atr_rel=float(atr_rel_v) if np.isfinite(atr_rel_v) else float("nan"),
                atr_pct=float(atr_pct_v) if np.isfinite(atr_pct_v) else float("nan"),
                spread_px=float(spread_px_v) if np.isfinite(spread_px_v) else float("nan"),
                spread_rel=float(spread_rel_v) if np.isfinite(spread_rel_v) else float("nan"),
                liquidity_gate_enabled=bool(liq_gate_on_v),
                liquidity_max_spread_rel=float(liq_thr_v),
                liquidity_risk=bool(liquidity_risk_v),
                vol_risk_vol_ratio_max=float(vol_risk_ratio_max_v) if np.isfinite(vol_risk_ratio_max_v) else float("nan"),
                vol_risk_vol_pct_max=float(vol_risk_pct_max_v) if np.isfinite(vol_risk_pct_max_v) else float("nan"),
                vol_risk_action=str(vol_risk_action_v),
                vol_risk_blocked=bool(vol_risk_blocked_v),
                sr_support=float(sr_support_v) if np.isfinite(sr_support_v) else float("nan"),
                sr_resistance=float(sr_resistance_v) if np.isfinite(sr_resistance_v) else float("nan"),
                sr_support_dist_atr=float(sr_sup_dist_atr_v) if np.isfinite(sr_sup_dist_atr_v) else float("nan"),
                sr_resistance_dist_atr=float(sr_res_dist_atr_v) if np.isfinite(sr_res_dist_atr_v) else float("nan"),
                sr_support_touches=int(sr_sup_t_v),
                sr_resistance_touches=int(sr_res_t_v),
                jg_macd_up=bool(jg_macd_up_v),
                jg_macd_down=bool(jg_macd_down_v),
                jg_sma175=float(jg_sma175_v) if np.isfinite(jg_sma175_v) else float("nan"),
                jg_j=float(jg_j_v) if np.isfinite(jg_j_v) else float("nan"),
                jg_long=bool(jg_long_v),
                jg_short=bool(jg_short_v),
                jg_ma13=float(jg_ma13_arr[i]) if (i < len(jg_ma13_arr) and np.isfinite(jg_ma13_arr[i])) else float("nan"),
                jg_ma55=float(jg_ma55_arr[i]) if (i < len(jg_ma55_arr) and np.isfinite(jg_ma55_arr[i])) else float("nan"),
                jg_ema20=float(jg_ema20_arr[i]) if (i < len(jg_ema20_arr) and np.isfinite(jg_ema20_arr[i])) else float("nan"),
                jg_ema27=float(jg_ema27_arr[i]) if (i < len(jg_ema27_arr) and np.isfinite(jg_ema27_arr[i])) else float("nan"),
                jg_ema29=float(jg_ema29_arr[i]) if (i < len(jg_ema29_arr) and np.isfinite(jg_ema29_arr[i])) else float("nan"),
                jg_ema32=float(jg_ema32_arr[i]) if (i < len(jg_ema32_arr) and np.isfinite(jg_ema32_arr[i])) else float("nan"),
                jg_ema36=float(jg_ema36_arr[i]) if (i < len(jg_ema36_arr) and np.isfinite(jg_ema36_arr[i])) else float("nan"),
                jg_pivot_mid=float(jg_pivot_mid_arr[i]) if (i < len(jg_pivot_mid_arr) and np.isfinite(jg_pivot_mid_arr[i])) else float("nan"),
                jg_b3=float(jg_b3_arr[i]) if (i < len(jg_b3_arr) and np.isfinite(jg_b3_arr[i])) else float("nan"),
                jg_s3=float(jg_s3_arr[i]) if (i < len(jg_s3_arr) and np.isfinite(jg_s3_arr[i])) else float("nan"),
                jg_b5=float(jg_b5_arr[i]) if (i < len(jg_b5_arr) and np.isfinite(jg_b5_arr[i])) else float("nan"),
                jg_s5=float(jg_s5_arr[i]) if (i < len(jg_s5_arr) and np.isfinite(jg_s5_arr[i])) else float("nan"),
                jg_var2=float(jg_var2_arr[i]) if (i < len(jg_var2_arr) and np.isfinite(jg_var2_arr[i])) else float("nan"),
                jg_var3=float(jg_var3_arr[i]) if (i < len(jg_var3_arr) and np.isfinite(jg_var3_arr[i])) else float("nan"),
                jg_var3_ma6=float(jg_var3_ma6_arr[i]) if (i < len(jg_var3_ma6_arr) and np.isfinite(jg_var3_ma6_arr[i])) else float("nan"),
                jg_bar_yellow=bool(jg_bar_yellow_arr[i]) if (i < len(jg_bar_yellow_arr)) else False,
                jg_bar_red=bool(jg_bar_red_arr[i]) if (i < len(jg_bar_red_arr)) else False,
                jg_macd=float(jg_macd_arr[i]) if (i < len(jg_macd_arr) and np.isfinite(jg_macd_arr[i])) else float("nan"),
                jg_buy=bool(jg_buy_arr[i]) if (i < len(jg_buy_arr)) else False,
                jg_sell=bool(jg_sell_arr[i]) if (i < len(jg_sell_arr)) else False,
                jg_gold=bool(jg_gold_arr[i]) if (i < len(jg_gold_arr)) else False,
                jg_ma160=float(jg_ma160_arr[i]) if (i < len(jg_ma160_arr) and np.isfinite(jg_ma160_arr[i])) else float("nan"),
                jg_ma120=float(jg_ma120_arr[i]) if (i < len(jg_ma120_arr) and np.isfinite(jg_ma120_arr[i])) else float("nan"),
                jg_ma60=float(jg_ma60_arr[i]) if (i < len(jg_ma60_arr) and np.isfinite(jg_ma60_arr[i])) else float("nan"),
                jg_ma25=float(jg_ma25_arr[i]) if (i < len(jg_ma25_arr) and np.isfinite(jg_ma25_arr[i])) else float("nan"),
                jg_flip_to_yellow=bool(jg_flip_to_yellow_arr[i]) if (i < len(jg_flip_to_yellow_arr)) else False,
                jg_flip_to_red=bool(jg_flip_to_red_arr[i]) if (i < len(jg_flip_to_red_arr)) else False,
                jg_wick_touch_ma13=bool(jg_wick_touch_ma13_arr[i]) if (i < len(jg_wick_touch_ma13_arr)) else False,
                jg_wick_touch_ma55=bool(jg_wick_touch_ma55_arr[i]) if (i < len(jg_wick_touch_ma55_arr)) else False,
                jg_wick_touch_ema27=bool(jg_wick_touch_ema27_arr[i]) if (i < len(jg_wick_touch_ema27_arr)) else False,
                jg_wick_touch_ema29=bool(jg_wick_touch_ema29_arr[i]) if (i < len(jg_wick_touch_ema29_arr)) else False,
                jg_wick_touch_ema32=bool(jg_wick_touch_ema32_arr[i]) if (i < len(jg_wick_touch_ema32_arr)) else False,
                jg_wick_touch_ema36=bool(jg_wick_touch_ema36_arr[i]) if (i < len(jg_wick_touch_ema36_arr)) else False,
                jg_close_breakdown_ma13=bool(jg_close_breakdown_ma13_arr[i]) if (i < len(jg_close_breakdown_ma13_arr)) else False,
                jg_close_breakup_ma13=bool(jg_close_breakup_ma13_arr[i]) if (i < len(jg_close_breakup_ma13_arr)) else False,
                jg_close_breakdown_ma55=bool(jg_close_breakdown_ma55_arr[i]) if (i < len(jg_close_breakdown_ma55_arr)) else False,
                jg_close_breakup_ma55=bool(jg_close_breakup_ma55_arr[i]) if (i < len(jg_close_breakup_ma55_arr)) else False,
                jg_cross_ma13_ema27_up=bool(jg_cross_ma13_ema27_up_arr[i]) if (i < len(jg_cross_ma13_ema27_up_arr)) else False,
                jg_cross_ma13_ema27_down=bool(jg_cross_ma13_ema27_down_arr[i]) if (i < len(jg_cross_ma13_ema27_down_arr)) else False,
                jg_cross_ma13_ema29_up=bool(jg_cross_ma13_ema29_up_arr[i]) if (i < len(jg_cross_ma13_ema29_up_arr)) else False,
                jg_cross_ma13_ema29_down=bool(jg_cross_ma13_ema29_down_arr[i]) if (i < len(jg_cross_ma13_ema29_down_arr)) else False,
                jg_cross_ma13_ema32_up=bool(jg_cross_ma13_ema32_up_arr[i]) if (i < len(jg_cross_ma13_ema32_up_arr)) else False,
                jg_cross_ma13_ema32_down=bool(jg_cross_ma13_ema32_down_arr[i]) if (i < len(jg_cross_ma13_ema32_down_arr)) else False,
                jg_cross_ma13_ema36_up=bool(jg_cross_ma13_ema36_up_arr[i]) if (i < len(jg_cross_ma13_ema36_up_arr)) else False,
                jg_cross_ma13_ema36_down=bool(jg_cross_ma13_ema36_down_arr[i]) if (i < len(jg_cross_ma13_ema36_down_arr)) else False,
                jg_after_cross_ma13_ema27_up_j_lt80=bool(jg_after_cross_ma13_ema27_up_j_lt80_arr[i]) if (i < len(jg_after_cross_ma13_ema27_up_j_lt80_arr)) else False,
                jg_after_cross_ma13_ema27_down_j_gt20=bool(jg_after_cross_ma13_ema27_down_j_gt20_arr[i]) if (i < len(jg_after_cross_ma13_ema27_down_j_gt20_arr)) else False,
                jg_dist_b3_atr=float(jg_dist_b3_atr_arr[i]) if (i < len(jg_dist_b3_atr_arr) and np.isfinite(jg_dist_b3_atr_arr[i])) else float("nan"),
                jg_dist_s3_atr=float(jg_dist_s3_atr_arr[i]) if (i < len(jg_dist_s3_atr_arr) and np.isfinite(jg_dist_s3_atr_arr[i])) else float("nan"),
                jg_dist_pivot_atr=float(jg_dist_pivot_atr_arr[i]) if (i < len(jg_dist_pivot_atr_arr) and np.isfinite(jg_dist_pivot_atr_arr[i])) else float("nan"),
                jg_red_streak=int(jg_red_streak_arr[i]) if (i < len(jg_red_streak_arr)) else 0,
                jg_yellow_streak=int(jg_yellow_streak_arr[i]) if (i < len(jg_yellow_streak_arr)) else 0,
                )
            )

    out = [s for s in sigs if str(s.ts) in keep_ts]
    out.sort(key=lambda x: str(x.ts))
    return out


def _scan_gate_snapshot(symbol: str, p: Params) -> Optional[GateSnapshot]:
    sym = _resolve_symbol(symbol)
    df1 = _mt5_rates(sym, mt5.TIMEFRAME_H1, int(300))
    df4 = _mt5_rates(sym, mt5.TIMEFRAME_H4, int(250))
    dfd = _mt5_rates(sym, mt5.TIMEFRAME_D1, int(250))
    tr = compute_trend_flags(df1, df4, dfd, p).reindex(df1.index)
    if tr.empty:
        return None
    last = tr.iloc[-1]
    ts = str(tr.index[-1])
    return GateSnapshot(
        ts=ts,
        symbol=str(sym).upper(),
        require_strong_for_entry=bool(getattr(p, "require_strong_for_entry", True)),
        strong_long=bool(last.get("strong_long", False)),
        strong_short=bool(last.get("strong_short", False)),
        regime_long=bool(last.get("regime_long", False)),
        regime_short=bool(last.get("regime_short", False)),
        confirm_long=bool(last.get("confirm_long", False)),
        confirm_short=bool(last.get("confirm_short", False)),
        kd_long=bool(last.get("kd_long", False)),
        kd_short=bool(last.get("kd_short", False)),
        kd_w1_long=bool(last.get("kd_w1_long", False)),
        kd_w1_short=bool(last.get("kd_w1_short", False)),
        kd_3line_long=bool(last.get("kd_3line_long", False)),
        kd_3line_short=bool(last.get("kd_3line_short", False)),
        ema21_1h=float(last.get("ema21_1h", np.nan)),
    )


def _parse_args(argv: List[str]) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "execute": False,
        "pool": "core",
        "reset_peak": False,
        "enable_cam": True,
        "watch": False,
        "interval_sec": 30,
        "max_loops": None,
        "simulate_dd": None,
        "close_all": 0,
        "mt5_status": 0,
        "mt5_history_check": 0,
        "mt5_history_from": "",
        "mt5_history_to": "",
        "mt5_history_symbols": "",
        "mt5_history_tf": "H1",
        "test_trade": False,
        "test_symbol": "EURUSD",
        "test_side": "buy",
        "test_volume": 0.01,
        "test_close_after_sec": 1,
        "test18": False,
        "test18_symbol": "EURUSD",
        "test18_volume": 0.01,
        "log_enabled": True,
        "log_dir": str(DEFAULT_LOG_DIR),
        "log_every_n": 1,
        "private_names": 0,
        "export_today": False,
        "export_from": "",
        "export_to": "",
        "summary_today": False,
        "enable_entry": False,
        "entry_universe": "pool",
        "entry_symbols": "",
        "entry_max": 30,
        "entry_lookback_bars": 1,
        "entry_gate_snapshot": False,
        "exit_diag": False,
        "entry_execute": False,
        "entry_lot": 0.01,
        "entry_max_orders": 1,
        "entry_scan_pools": "",
        "entry_trade_pool": "pool",
        "entry_require_strong": 1,
        "entry_status": 0,
        "entry_show_all": 0,
        "watch_on_new_h1": 0,
        "paper_replay": 0,
        "paper_replay_csv": 0,
        "paper_commentary": 0,
        "paper_dir": "",
        "paper_lookahead_bars": 48,
        "paper_tp1_r": 1.0,
        "paper_tp2_r": 2.0,
        "paper_bar_rule": "sl_first",
        "paper_e2_chase_max": None,
        "paper_e1_diagnose": 1,
        "commentary_symbol": "",
        "commentary_topk": 5,
        "commentary_min_n": 15,
        "paper_scan": 0,
        "paper_scan_csv": 0,
        "paper_from": "",
        "paper_to": "",
        "paper_symbols": "",
        "paper_bobby_signals": 0,
        "paper_bobby_sl_atr": 1.0,
        "csv_dir": str((Path(__file__).resolve().parent / "data").resolve()),
        "e1_cci144_veto": 1,
        "e1_adx_score": 0,
        "enable_score_filter": 1,
        "e2_chase_max_atr": None,
        "e2_chase_action": "off",
        "enable_liquidity_gate": 0,
        "liquidity_max_spread_rel": 0.15,
        "vol_risk_vol_ratio_max": None,
        "vol_risk_vol_pct_max": None,
        "vol_risk_action": "off",
        "entry_score_max": None,
        "entry_score_action": "off",
        "entry_score_scope": "all",
        "entry_score_vol_mode": "off",
        "entry_score_vol_cuts": "",
        "entry_score_vol_maxes": "",
    }
    i = 0
    while i < len(argv):
        k = str(argv[i]).strip()
        if k in {"--execute", "execute"}:
            out["execute"] = True
        elif k in {"--dry-run", "dry-run"}:
            out["execute"] = False
        elif k in {"--test-trade", "test-trade"}:
            out["test_trade"] = True
        elif k in {"--test-symbol"}:
            i += 1
            out["test_symbol"] = str(argv[i]).strip()
        elif k in {"--test-side"}:
            i += 1
            out["test_side"] = str(argv[i]).strip().lower()
        elif k in {"--test-volume"}:
            i += 1
            out["test_volume"] = float(str(argv[i]).strip())
        elif k in {"--close-after-sec", "--test-close-after-sec"}:
            i += 1
            out["test_close_after_sec"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--test18", "--test-18", "test18", "test-18"}:
            out["test18"] = True
        elif k in {"--test18-symbol"}:
            i += 1
            out["test18_symbol"] = str(argv[i]).strip()
        elif k in {"--test18-volume"}:
            i += 1
            out["test18_volume"] = float(str(argv[i]).strip())
        elif k in {"--watch", "watch"}:
            out["watch"] = True
        elif k in {"--interval-sec", "--interval", "interval"}:
            i += 1
            out["interval_sec"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--max-loops"}:
            i += 1
            v = str(argv[i]).strip()
            out["max_loops"] = int(v) if v else None
        elif k in {"--simulate-dd", "--simulate-dd-pct"}:
            i += 1
            v = str(argv[i]).strip()
            out["simulate_dd"] = float(v) if v else None
        elif k in {"--close-all", "--panic-close"}:
            out["close_all"] = 1
        elif k in {"--mt5-status", "--mt5-check"}:
            out["mt5_status"] = 1
        elif k in {"--mt5-history-check"}:
            out["mt5_history_check"] = 1
        elif k in {"--mt5-history-from"}:
            i += 1
            out["mt5_history_from"] = str(argv[i]).strip()
        elif k in {"--mt5-history-to"}:
            i += 1
            out["mt5_history_to"] = str(argv[i]).strip()
        elif k in {"--mt5-history-symbols"}:
            i += 1
            out["mt5_history_symbols"] = str(argv[i]).strip()
        elif k in {"--mt5-history-tf"}:
            i += 1
            out["mt5_history_tf"] = str(argv[i]).strip().upper()
        elif k in {"--pool"}:
            i += 1
            out["pool"] = str(argv[i]).strip()
        elif k in {"--reset-peak"}:
            out["reset_peak"] = True
        elif k in {"--enable-cam"}:
            i += 1
            out["enable_cam"] = bool(int(str(argv[i]).strip()))
        elif k in {"--log-enabled"}:
            i += 1
            out["log_enabled"] = bool(int(str(argv[i]).strip()))
        elif k in {"--log-dir"}:
            i += 1
            out["log_dir"] = str(argv[i]).strip()
        elif k in {"--log-every-n"}:
            i += 1
            out["log_every_n"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--private-names"}:
            i += 1
            out["private_names"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--export-today"}:
            out["export_today"] = True
        elif k in {"--export-from"}:
            i += 1
            out["export_from"] = str(argv[i]).strip()
        elif k in {"--export-to"}:
            i += 1
            out["export_to"] = str(argv[i]).strip()
        elif k in {"--summary-today"}:
            out["summary_today"] = True
        elif k in {"--enable-entry"}:
            i += 1
            out["enable_entry"] = bool(int(str(argv[i]).strip()))
        elif k in {"--entry-universe"}:
            i += 1
            out["entry_universe"] = str(argv[i]).strip()
        elif k in {"--entry-symbols"}:
            i += 1
            out["entry_symbols"] = str(argv[i]).strip()
        elif k in {"--entry-max"}:
            i += 1
            out["entry_max"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--entry-lookback-bars"}:
            i += 1
            out["entry_lookback_bars"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--entry-gate-snapshot"}:
            i += 1
            out["entry_gate_snapshot"] = bool(int(str(argv[i]).strip()))
        elif k in {"--exit-diag"}:
            i += 1
            out["exit_diag"] = bool(int(str(argv[i]).strip()))
        elif k in {"--entry-execute"}:
            i += 1
            out["entry_execute"] = bool(int(str(argv[i]).strip()))
        elif k in {"--entry-lot"}:
            i += 1
            out["entry_lot"] = float(str(argv[i]).strip())
        elif k in {"--entry-max-orders"}:
            i += 1
            out["entry_max_orders"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--entry-require-strong"}:
            i += 1
            out["entry_require_strong"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--entry-status"}:
            i += 1
            out["entry_status"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--entry-show-all"}:
            i += 1
            out["entry_show_all"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--watch-on-new-h1", "--on-new-h1"}:
            i += 1
            out["watch_on_new_h1"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--paper-replay", "--paper", "paper"}:
            out["paper_replay"] = 1
        elif k in {"--paper-replay-csv"}:
            out["paper_replay_csv"] = 1
        elif k in {"--paper-commentary", "--paper-report", "--commentary", "commentary"}:
            out["paper_commentary"] = 1
        elif k in {"--paper-dir"}:
            i += 1
            out["paper_dir"] = str(argv[i]).strip()
        elif k in {"--csv-dir", "--paper-csv-dir"}:
            i += 1
            out["csv_dir"] = str(argv[i]).strip()
        elif k in {"--commentary-symbol"}:
            i += 1
            out["commentary_symbol"] = str(argv[i]).strip()
        elif k in {"--commentary-topk"}:
            i += 1
            out["commentary_topk"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--commentary-min-n"}:
            i += 1
            out["commentary_min_n"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--paper-lookahead-bars"}:
            i += 1
            out["paper_lookahead_bars"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--paper-tp1-r"}:
            i += 1
            out["paper_tp1_r"] = float(str(argv[i]).strip())
        elif k in {"--paper-tp2-r"}:
            i += 1
            out["paper_tp2_r"] = float(str(argv[i]).strip())
        elif k in {"--paper-bar-rule"}:
            i += 1
            out["paper_bar_rule"] = str(argv[i]).strip()
        elif k in {"--paper-e2-chase-max"}:
            i += 1
            v = str(argv[i]).strip()
            if not v or v.lower() in {"none", "null", "nan"}:
                out["paper_e2_chase_max"] = None
            else:
                out["paper_e2_chase_max"] = float(v)
        elif k in {"--paper-e1-diagnose"}:
            i += 1
            out["paper_e1_diagnose"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--paper-scan"}:
            out["paper_scan"] = 1
        elif k in {"--paper-scan-csv"}:
            out["paper_scan_csv"] = 1
        elif k in {"--paper-from"}:
            i += 1
            out["paper_from"] = str(argv[i]).strip()
        elif k in {"--paper-to"}:
            i += 1
            out["paper_to"] = str(argv[i]).strip()
        elif k in {"--paper-symbols"}:
            i += 1
            out["paper_symbols"] = str(argv[i]).strip()
        elif k in {"--paper-bobby-signals"}:
            i += 1
            out["paper_bobby_signals"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--paper-bobby-sl-atr"}:
            i += 1
            out["paper_bobby_sl_atr"] = float(str(argv[i]).strip())
        elif k in {"--e1-cci144-veto"}:
            i += 1
            out["e1_cci144_veto"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--e1-adx-score"}:
            i += 1
            out["e1_adx_score"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--enable-score-filter"}:
            i += 1
            out["enable_score_filter"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--e2-chase-max-atr", "--e2-chase-max"}:
            i += 1
            v = str(argv[i]).strip()
            out["e2_chase_max_atr"] = float(v) if v else None
        elif k in {"--e2-chase-action"}:
            i += 1
            out["e2_chase_action"] = str(argv[i]).strip().lower()
        elif k in {"--enable-liquidity-gate", "--liquidity-gate"}:
            i += 1
            out["enable_liquidity_gate"] = int(round(float(str(argv[i]).strip())))
        elif k in {"--liquidity-max-spread-rel", "--liquidity-risk-max-spread-rel"}:
            i += 1
            out["liquidity_max_spread_rel"] = float(str(argv[i]).strip())
        elif k in {"--vol-ratio-max", "--volume-risk-vol-ratio-max"}:
            i += 1
            v = str(argv[i]).strip()
            out["vol_risk_vol_ratio_max"] = float(v) if v else None
        elif k in {"--vol-pct-max", "--volume-risk-vol-pct-max"}:
            i += 1
            v = str(argv[i]).strip()
            out["vol_risk_vol_pct_max"] = float(v) if v else None
        elif k in {"--vol-risk-action", "--volume-risk-action"}:
            i += 1
            out["vol_risk_action"] = str(argv[i]).strip().lower()
        elif k in {"--entry-score-max"}:
            i += 1
            v = str(argv[i]).strip()
            out["entry_score_max"] = float(v) if v else None
        elif k in {"--entry-score-action"}:
            i += 1
            out["entry_score_action"] = str(argv[i]).strip().lower()
        elif k in {"--entry-score-scope"}:
            i += 1
            out["entry_score_scope"] = str(argv[i]).strip().lower()
        elif k in {"--entry-score-vol-mode"}:
            i += 1
            out["entry_score_vol_mode"] = str(argv[i]).strip().lower()
        elif k in {"--entry-score-vol-cuts"}:
            i += 1
            out["entry_score_vol_cuts"] = str(argv[i]).strip()
        elif k in {"--entry-score-vol-maxes"}:
            i += 1
            out["entry_score_vol_maxes"] = str(argv[i]).strip()
        elif k in {"--entry-scan-pools"}:
            i += 1
            out["entry_scan_pools"] = str(argv[i]).strip()
        elif k in {"--entry-trade-pool"}:
            i += 1
            out["entry_trade_pool"] = str(argv[i]).strip()
        elif k in {"-h", "--help", "help"}:
            out["help"] = True
        else:
            raise ValueError(f"unknown arg: {k}")
        i += 1
    return out


def _parse_csv_list(s: Any) -> List[str]:
    raw = str(s or "").strip()
    if not raw:
        return []
    parts = [x.strip().lower() for x in raw.split(",") if x.strip()]
    out: List[str] = []
    seen = set()
    for p in parts:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def _merge_pool_dfs(pools: List[str]) -> Optional[pd.DataFrame]:
    dfs: List[pd.DataFrame] = []
    for p in pools:
        df = _read_deploy_pool_df(p)
        if df is not None and not df.empty:
            df = df.copy()
            df["pool"] = str(p).lower()
            dfs.append(df)
    if not dfs:
        return None
    merged = pd.concat(dfs, axis=0, ignore_index=True)
    merged = merged.drop_duplicates(subset=["symbol"], keep="first").reset_index(drop=True)
    return merged if not merged.empty else None


def _run_once(args: Dict[str, Any], p: Params, c: Config, state: Dict[str, Any]) -> Dict[str, Any]:
    equity = _get_account_equity()
    ts = _now_utc_iso()

    peak = _float_or_none(state.get("peak_equity"))
    if args.get("reset_peak") or peak is None or peak <= 0:
        peak = float(equity)
    peak = float(max(float(peak), float(equity)))
    state["peak_equity"] = float(peak)

    dd = 0.0 if peak <= 0 else max(0.0, min(1.0, 1.0 - float(equity) / float(peak)))
    halted = bool(dd >= float(c.max_drawdown))
    state["dd_halted"] = bool(halted)
    _print_dd_banner(equity, peak, dd, float(c.max_drawdown), halted)
    if halted:
        print("[P0] 达到 25% 最大回撤停机线：禁止新开仓（仅允许减仓/出场/风控处理）")

    pool_df = _read_deploy_pool_df(str(args.get("pool", "core")))
    pool_syms = None if pool_df is None else pool_df["symbol"].tolist()
    symbols_filter = {s.upper() for s in pool_syms} if pool_syms else None
    sym_settings = _symbol_settings_map(pool_df)
    core_df = _read_deploy_pool_df("core")
    core_set = set(core_df["symbol"].tolist()) if core_df is not None else set()
    core_settings = _symbol_settings_map(core_df)

    positions = _get_positions()
    pos_syms = [str(getattr(pos, "symbol", "")).strip() for pos in positions]
    pos_syms = [s for s in pos_syms if s]
    if symbols_filter is None:
        print(f"[POS] count={len(positions)} symbols={pos_syms}")
    else:
        print(f"[POS] count={len(positions)} symbols={pos_syms} pool_size={len(symbols_filter)}")

    close_all = bool(int(args.get("close_all") or 0) != 0)
    if close_all:
        if not positions:
            print("[PANIC] close_all: no positions")
        else:
            targets: List[Any] = []
            for pos in positions:
                sym_u = str(getattr(pos, "symbol", "")).strip().upper()
                if not sym_u:
                    continue
                if symbols_filter is not None and sym_u not in symbols_filter:
                    continue
                targets.append(pos)
            print(f"[PANIC] close_all: targets={len(targets)} execute={bool(args.get('execute'))}")
            if targets and bool(args.get("execute")):
                if not _print_trade_api_status():
                    return state
                for pos in targets:
                    ticket = int(getattr(pos, "ticket"))
                    sym = str(getattr(pos, "symbol", "")).strip()
                    vol = float(getattr(pos, "volume", 0.0) or 0.0)
                    if vol <= 0:
                        continue
                    r = _send_close_partial(pos, volume=vol)
                    ok = bool(getattr(r, "retcode", None) == mt5.TRADE_RETCODE_DONE)
                    print(
                        f"[PANIC][EXEC] close ticket={ticket} symbol={sym} vol={vol:.4f} ok={ok} ret={getattr(r,'retcode',None)}"
                    )
                positions = _get_positions()
        return state
    actions: List[ExitAction] = []
    for pos in positions:
        sym_u = str(getattr(pos, "symbol", "")).strip().upper()
        ss = sym_settings.get(sym_u)
        p_sym = _params_for_symbol(p, ss)
        p_sym = _params_for_symbol(p, ss)
        cam_on = bool(args.get("enable_cam", True)) and (True if ss is None or ss.cam_enabled is None else bool(ss.cam_enabled))
        actions.extend(
            _build_actions_for_position(
                pos,
                p=p_sym,
                state=state,
                enable_cam=cam_on,
                symbols_filter=symbols_filter,
            )
        )

    _print_actions(actions)

    entries: List[EntrySignal] = []
    if bool(args.get("enable_entry")) and (not halted):
        is_entry_exec = bool(args.get("execute")) and bool(args.get("entry_execute"))
        last_ts_key = "entry_last_ts_exec" if is_entry_exec else "entry_last_ts_print"
        show_all = bool(int(args.get("entry_show_all") or 0) != 0)
        pos_set = {str(getattr(pos, "symbol", "")).strip().upper() for pos in positions if str(getattr(pos, "symbol", "")).strip()}
        entry_syms = _entry_universe(args, pool_syms)
        scan_pools = _parse_csv_list(args.get("entry_scan_pools"))
        scan_df = _merge_pool_dfs(scan_pools) if scan_pools else None
        entry_settings = _symbol_settings_map(scan_df) if scan_df is not None else sym_settings
        scan_set = set(scan_df["symbol"].tolist()) if scan_df is not None else None
        if scan_set is not None:
            entry_syms = [s for s in entry_syms if str(s).upper() in scan_set]
        lookback = max(1, int(args.get("entry_lookback_bars") or 1))
        entry_status_rows: List[Dict[str, object]] = []
        if entry_syms:
            for sym in entry_syms:
                if str(sym).upper() in pos_set:
                    continue
                try:
                    sym_u = str(sym).upper()
                    p_sym = _params_for_symbol(p, entry_settings.get(sym_u))
                    sigs = _scan_entry_signals(
                        sym_u,
                        p=p_sym,
                        lookback_bars=lookback,
                        emit_gate_log=bool(args.get("entry_gate_snapshot")),
                    )
                except Exception as e:
                    print(f"[ENTRY][ERROR] {sym}: {type(e).__name__}: {e}")
                    continue
                if int(args.get("entry_status") or 0) != 0:
                    sym_res = _resolve_symbol(sym_u)
                    last_bar = _last_bar_open_ts(sym_res, mt5.TIMEFRAME_H1)
                    last_tick = _tick_ts(sym_res)
                    newest_sig = sigs[-1].ts if sigs else ""
                    entry_status_rows.append(
                        {
                            "symbol": sym_u,
                            "resolved": sym_res,
                            "reqStrong": bool(getattr(p_sym, "require_strong_for_entry", True)),
                            "lastBarH1": str(last_bar) if last_bar is not None else "",
                            "lastTick": str(last_tick) if last_tick is not None else "",
                            "newestSig": str(newest_sig),
                        }
                    )
                if not sigs:
                    continue
                last_ts_v = None
                if not show_all:
                    last_ts = _entry_last_ts_get(state, str(sigs[-1].symbol), key=last_ts_key)
                    last_ts_v = pd.to_datetime(last_ts) if last_ts else None
                for sig in sigs:
                    if (not show_all) and (last_ts_v is not None):
                        try:
                            if pd.to_datetime(str(sig.ts)) <= last_ts_v:
                                continue
                        except Exception:
                            pass
                    entries.append(sig)

        if int(args.get("entry_status") or 0) != 0:
            _print_entry_status(entry_status_rows)
        _print_entries(entries)

        if (not entries) and bool(args.get("entry_gate_snapshot")) and entry_syms:
            snaps: List[GateSnapshot] = []
            for sym in entry_syms:
                if str(sym).upper() in pos_set:
                    continue
                try:
                    sym_u = str(sym).upper()
                    p_sym = _params_for_symbol(p, entry_settings.get(sym_u))
                    s = _scan_gate_snapshot(sym_u, p=p_sym)
                except Exception as e:
                    print(f"[GATE][ERROR] {sym}: {type(e).__name__}: {e}")
                    continue
                if s is not None:
                    snaps.append(s)
            _print_gate_snapshots(snaps)

    if bool(args.get("exit_diag")) and positions:
        rows: List[Dict[str, object]] = []
        for pos in positions:
            sym = str(getattr(pos, "symbol", "")).strip()
            if not sym:
                continue
            ticket = int(getattr(pos, "ticket"))
            side = _pos_side_str(int(getattr(pos, "type")))
            px = _pos_close_price(sym, side=side)
            pv = _ensure_pos_state(state, ticket=ticket, volume=float(getattr(pos, "volume", 0.0)))
            tp1 = bool(pv.get("tp1_done", False))
            tp2 = bool(pv.get("tp2_done", False))
            try:
                h, l, c0 = _yesterday_d1_hlc(sym)
                levels = _cam_levels_from_hlc(h, l, c0, p)
            except Exception:
                levels = {}
            rows.append(
                {
                    "ticket": ticket,
                    "symbol": sym,
                    "side": side,
                    "px": round(float(px), 6),
                    "tp1_done": tp1,
                    "tp2_done": tp2,
                    "R1": round(float(levels.get("R1", np.nan)), 6) if levels else "",
                    "R2": round(float(levels.get("R2", np.nan)), 6) if levels else "",
                    "S1": round(float(levels.get("S1", np.nan)), 6) if levels else "",
                    "S2": round(float(levels.get("S2", np.nan)), 6) if levels else "",
                }
            )
        _print_exit_diag(rows)

    entry_exec_rows: List[Dict[str, object]] = []
    if bool(args.get("execute")) and bool(args.get("enable_entry")) and bool(args.get("entry_execute")) and (not halted) and entries:
        if not _print_trade_api_status():
            return state
        recent_cutoff = datetime.now(timezone.utc).astimezone().replace(tzinfo=None) - pd.to_timedelta(180, unit="min")
        max_n = max(0, int(args.get("entry_max_orders") or 0))
        lot_arg = float(args.get("entry_lot") or 0.0)
        trade_pool = str(args.get("entry_trade_pool") or "pool").strip().lower()
        if trade_pool in {"none", "off", "disable"}:
            trade_allowed_set: Optional[set[str]] = set()
        elif trade_pool in {"all", "*"}:
            trade_allowed_set = None
        elif trade_pool == "core":
            trade_allowed_set = set(core_set)
        elif trade_pool == "pool":
            trade_allowed_set = set(symbols_filter) if symbols_filter is not None else None
        elif trade_pool == "observe":
            df = _read_deploy_pool_df("observe")
            trade_allowed_set = set(df["symbol"].tolist()) if df is not None else set()
        else:
            raise ValueError(f"unknown entry_trade_pool: {trade_pool}")

        if max_n > 0 and (lot_arg > 0 or sym_settings or core_set):
            try:
                max_ts = max(pd.to_datetime(str(e.ts)) for e in entries)
                entries_now = [e for e in entries if pd.to_datetime(str(e.ts)) == max_ts]
            except Exception:
                entries_now = list(entries)
            entries_sorted = sorted(entries_now, key=lambda x: float(x.entry_score), reverse=True)
            for e in entries_sorted[:max_n]:
                try:
                    if pd.to_datetime(str(e.ts)).to_pydatetime() < recent_cutoff:
                        continue
                except Exception:
                    pass
                if str(e.symbol).upper() in pos_set:
                    continue
                sym_u = str(e.symbol).upper()
                if trade_allowed_set is not None and sym_u not in trade_allowed_set:
                    continue
                if str(e.signal).upper() == "E2" and bool(getattr(e, "e2_chase_blocked", False)) and _E2_CHASE_ACTION == "block":
                    print(
                        f"[ENTRY][SKIP] {sym_u}: e2_chase_blocked chase={float(getattr(e, 'chase_dist_atr', float('nan'))):.3f} thr={float(_E2_CHASE_MAX_ATR):.3f}"
                    )
                    continue
                if bool(_LIQUIDITY_GATE_ENABLED) and bool(getattr(e, "liquidity_risk", False)):
                    print(
                        f"[ENTRY][SKIP] {sym_u}: liquidity_risk spread_rel={float(getattr(e, 'spread_rel', float('nan'))):.4f} thr={float(_LIQUIDITY_MAX_SPREAD_REL):.4f}"
                    )
                    continue
                if bool(getattr(e, "vol_risk_blocked", False)) and str(_VOL_RISK_ACTION) == "block":
                    print(
                        f"[ENTRY][SKIP] {sym_u}: vol_risk vol_ratio={float(getattr(e, 'vol_ratio', float('nan'))):.3f} vol_pct={float(getattr(e, 'vol_pct', float('nan'))):.1f}"
                    )
                    continue
                if bool(getattr(e, "entry_score_gate_blocked", False)) and str(_ENTRY_SCORE_ACTION) == "block":
                    print(
                        f"[ENTRY][SKIP] {sym_u}: entry_score_gate entry_score={float(getattr(e, 'entry_score', float('nan'))):.3f} max={float(getattr(e, 'entry_score_gate_max', float('nan'))):.3f}"
                    )
                    continue

                ss = sym_settings.get(sym_u) or core_settings.get(sym_u)
                if ss is not None and str(e.signal).upper() == "E2" and ss.enable_e2_exec is False:
                    print(f"[ENTRY][SKIP] {sym_u}: e2_exec_disabled")
                    continue
                sym_resolved = _resolve_symbol(sym_u)
                last_bar = _last_bar_open_ts(sym_resolved, mt5.TIMEFRAME_H1)
                if last_bar is not None:
                    try:
                        dt_bar = pd.to_datetime(str(last_bar), errors="coerce")
                        dt_sig = pd.to_datetime(str(e.ts), errors="coerce")
                        if pd.notna(dt_bar) and pd.notna(dt_sig):
                            dt_bar = _ts_utc_naive(dt_bar)
                            dt_sig = dt_sig.tz_convert("UTC").tz_localize(None) if getattr(dt_sig, "tzinfo", None) is not None else dt_sig
                            dt_bar_close = dt_bar + pd.to_timedelta(_tf_seconds(mt5.TIMEFRAME_H1), unit="s")
                            if dt_sig.to_pydatetime() != dt_bar_close.to_pydatetime():
                                print(f"[ENTRY][SKIP] {sym_u}: stale signal ts={e.ts} lastBarH1Close={str(dt_bar_close)}")
                                continue
                    except Exception:
                        pass
                bid, ask = _get_tick(sym_resolved)
                entry_px = float(ask) if str(e.side).upper() == "LONG" else float(bid)
                sl = _valid_sl_for_side(sym_resolved, "buy" if e.side == "LONG" else "sell", float(entry_px))
                if e.side == "LONG":
                    sl = float(min(float(sl), float(e.stop)))
                else:
                    sl = float(max(float(sl), float(e.stop)))

                risk_per_trade = None if ss is None else ss.risk_per_trade
                if lot_arg > 0:
                    vol = float(lot_arg)
                else:
                    if risk_per_trade is None or not (float(risk_per_trade) > 0):
                        print(f"[ENTRY][SKIP] {sym_u}: entry_lot not set and risk_per_trade missing in deploy pool")
                        continue
                    risk_money = float(equity) * float(risk_per_trade)
                    raw_lot = _calc_lot_for_risk(
                        sym_resolved, side=str(e.side), entry_price=float(entry_px), sl_price=float(sl), risk_money=risk_money
                    )
                    info = _ensure_symbol_ready(sym_resolved)
                    vol = _normalize_volume(info, float(raw_lot))
                    implied = _risk_money_per_lot(sym_resolved, side=str(e.side), entry_price=float(entry_px), sl_price=float(sl))
                    if implied is not None:
                        implied_risk = float(implied) * float(vol)
                        if implied_risk > risk_money * 1.25:
                            print(
                                f"[ENTRY][SKIP] {sym_u}: min lot too large for risk (risk_money={risk_money:.2f} implied={implied_risk:.2f} vol={vol:.4f})"
                            )
                            continue

                r = _send_open_market(sym_resolved, side=str(e.side), volume=float(vol), sl=float(sl))
                ok = bool(getattr(r, "retcode", None) == mt5.TRADE_RETCODE_DONE)
                print(
                    f"[ENTRY][EXEC] open symbol={sym_resolved} side={e.side} signal={e.signal} vol={vol:.4f} sl={sl:.6f} ok={ok} ret={getattr(r,'retcode',None)}"
                )
                entry_exec_rows.append(
                    {
                        "ts_utc": ts,
                        "ticket": "",
                        "symbol": str(sym_resolved),
                        "op": "open_market",
                        "volume": float(vol),
                        "retcode": getattr(r, "retcode", None) if r is not None else None,
                        "comment": getattr(r, "comment", "") if r is not None else "",
                        "side": str(e.side),
                        "signal": str(e.signal),
                        "sl": float(sl),
                        "risk_per_trade": float(risk_per_trade) if risk_per_trade is not None else np.nan,
                    }
                )
                _entry_last_ts_set(state, e.symbol, str(e.ts), key="entry_last_ts_exec")

    log_enabled = bool(args.get("log_enabled", True))
    log_every_n = max(1, int(args.get("log_every_n") or 1))
    loop_no = int(state.get("loop_no") or 0) + 1
    state["loop_no"] = loop_no
    if log_enabled and (loop_no % log_every_n == 0):
        out_dir = _log_dir_for_run(args)
        _append_csv(
            out_dir / "run_log.csv",
            pd.DataFrame(
                [
                    {
                        "ts_utc": ts,
                        "equity": float(equity),
                        "peak_equity": float(peak),
                        "dd": float(dd),
                        "dd_threshold": float(c.max_drawdown),
                        "dd_halted": bool(halted),
                        "positions": int(len(positions)),
                        "actions": int(len(actions)),
                        "execute": bool(args.get("execute", False)),
                        "pool": str(args.get("pool", "")),
                    }
                ]
            ),
        )
        if positions:
            rows: List[Dict[str, object]] = []
            for pos in positions:
                rows.append(
                    {
                        "ts_utc": ts,
                        "ticket": int(getattr(pos, "ticket")),
                        "symbol": str(getattr(pos, "symbol", "")),
                        "type": int(getattr(pos, "type", -1)),
                        "volume": float(getattr(pos, "volume", 0.0)),
                        "price_open": float(getattr(pos, "price_open", 0.0)),
                        "sl": _float_or_none(getattr(pos, "sl", None)),
                        "tp": _float_or_none(getattr(pos, "tp", None)),
                        "profit": float(getattr(pos, "profit", 0.0)),
                        "swap": float(getattr(pos, "swap", 0.0)),
                    }
                )
            _append_csv(out_dir / "positions_snapshot.csv", pd.DataFrame(rows))
        if actions:
            _append_csv(
                out_dir / "actions_suggested.csv",
                pd.DataFrame(
                    [
                        {
                            "ts_utc": ts,
                            "ticket": int(a.ticket),
                            "symbol": str(a.symbol),
                            "side": str(a.side),
                            "action": str(a.action),
                            "volume": float(a.volume),
                            "price": float(a.price),
                            "level": str(a.level_name),
                            "level_price": float(a.level_price),
                            "sl_now": _float_or_none(a.current_sl),
                            "sl_suggest": _float_or_none(a.suggested_sl),
                        }
                        for a in actions
                    ]
                ),
            )
        if entries:
            entries_path = out_dir / "entries_suggested.csv"
            if entries_path.exists():
                try:
                    hdr = entries_path.read_text(encoding="utf-8", errors="ignore").splitlines()[0]
                except Exception:
                    hdr = ""
                if "sig_ts" not in hdr:
                    entries_path = out_dir / "entries_suggested_v2.csv"
                elif "kd_3line_long" not in hdr:
                    entries_path = out_dir / "entries_suggested_v3.csv"
                elif "score_filter_pass" not in hdr:
                    entries_path = out_dir / "entries_suggested_v4.csv"
                elif "e2_chase_blocked" not in hdr:
                    entries_path = out_dir / "entries_suggested_v5.csv"
                elif "liquidity_risk" not in hdr:
                    entries_path = out_dir / "entries_suggested_v6.csv"
                elif "vol_risk_blocked" not in hdr:
                    entries_path = out_dir / "entries_suggested_v7.csv"
            private_names = bool(int(args.get("private_names", 0) or 0))
            _append_csv(
                entries_path,
                pd.DataFrame(
                    [
                        _apply_private_names(
                            {
                            "ts_utc": ts,
                            "sig_ts": str(e.ts),
                            "symbol": e.symbol,
                            "side": e.side,
                            "signal": e.signal,
                            "entry": float(e.entry),
                            "stop": float(e.stop),
                            "atr": float(e.atr),
                            "entry_score": float(e.entry_score),
                            "ema21_1h": float(e.ema21_1h),
                            "breakout_level": float(e.breakout_level) if not pd.isna(e.breakout_level) else np.nan,
                            "touch_delta": int(e.touch_delta),
                            "strong": bool(e.strong),
                            "kd_w1_long": bool(e.kd_w1_long),
                            "kd_w1_short": bool(e.kd_w1_short),
                            "kd_3line_long": bool(e.kd_3line_long),
                            "kd_3line_short": bool(e.kd_3line_short),
                            "cci144": float(e.cci144) if not pd.isna(e.cci144) else np.nan,
                            "cci_veto": bool(e.cci_veto),
                            "adx14": float(e.adx14) if not pd.isna(e.adx14) else np.nan,
                            "chase_dist_atr": float(e.chase_dist_atr) if not pd.isna(e.chase_dist_atr) else np.nan,
                            "score_filter_th": float(e.score_filter_th) if not pd.isna(e.score_filter_th) else np.nan,
                            "score_filter_pass": bool(e.score_filter_pass),
                            "e2_chase_max_atr": float(e.e2_chase_max_atr) if not pd.isna(e.e2_chase_max_atr) else np.nan,
                            "e2_chase_blocked": bool(e.e2_chase_blocked),
                            "e2_chase_action": str(e.e2_chase_action),
                            "tick_volume": float(e.tick_volume) if not pd.isna(e.tick_volume) else np.nan,
                            "vol_sma20": float(e.vol_sma20) if not pd.isna(e.vol_sma20) else np.nan,
                            "vol_ratio": float(e.vol_ratio) if not pd.isna(e.vol_ratio) else np.nan,
                            "vol_pct": float(e.vol_pct) if not pd.isna(e.vol_pct) else np.nan,
                            "atr_sma50": float(e.atr_sma50) if not pd.isna(e.atr_sma50) else np.nan,
                            "atr_rel": float(e.atr_rel) if not pd.isna(e.atr_rel) else np.nan,
                            "atr_pct": float(e.atr_pct) if not pd.isna(e.atr_pct) else np.nan,
                            "spread_px": float(e.spread_px) if not pd.isna(e.spread_px) else np.nan,
                            "spread_rel": float(e.spread_rel) if not pd.isna(e.spread_rel) else np.nan,
                            "liquidity_gate_enabled": bool(e.liquidity_gate_enabled),
                            "liquidity_max_spread_rel": float(e.liquidity_max_spread_rel) if not pd.isna(e.liquidity_max_spread_rel) else np.nan,
                            "liquidity_risk": bool(e.liquidity_risk),
                            "vol_risk_vol_ratio_max": float(e.vol_risk_vol_ratio_max) if not pd.isna(e.vol_risk_vol_ratio_max) else np.nan,
                            "vol_risk_vol_pct_max": float(e.vol_risk_vol_pct_max) if not pd.isna(e.vol_risk_vol_pct_max) else np.nan,
                            "vol_risk_action": str(e.vol_risk_action),
                            "vol_risk_blocked": bool(e.vol_risk_blocked),
                            "sr_support": float(e.sr_support) if not pd.isna(e.sr_support) else np.nan,
                            "sr_resistance": float(e.sr_resistance) if not pd.isna(e.sr_resistance) else np.nan,
                            "sr_support_dist_atr": float(e.sr_support_dist_atr) if not pd.isna(e.sr_support_dist_atr) else np.nan,
                            "sr_resistance_dist_atr": float(e.sr_resistance_dist_atr) if not pd.isna(e.sr_resistance_dist_atr) else np.nan,
                            "sr_support_touches": int(e.sr_support_touches),
                            "sr_resistance_touches": int(e.sr_resistance_touches),
                            "jg_macd_up": bool(e.jg_macd_up),
                            "jg_macd_down": bool(e.jg_macd_down),
                            "jg_sma175": float(e.jg_sma175) if not pd.isna(e.jg_sma175) else np.nan,
                            "jg_j": float(e.jg_j) if not pd.isna(e.jg_j) else np.nan,
                            "jg_long": bool(e.jg_long),
                            "jg_short": bool(e.jg_short),
                            "jg_ma13": float(e.jg_ma13) if not pd.isna(e.jg_ma13) else np.nan,
                            "jg_ma55": float(e.jg_ma55) if not pd.isna(e.jg_ma55) else np.nan,
                            "jg_ema20": float(e.jg_ema20) if not pd.isna(e.jg_ema20) else np.nan,
                            "jg_ema27": float(e.jg_ema27) if not pd.isna(e.jg_ema27) else np.nan,
                            "jg_ema29": float(e.jg_ema29) if not pd.isna(e.jg_ema29) else np.nan,
                            "jg_ema32": float(e.jg_ema32) if not pd.isna(e.jg_ema32) else np.nan,
                            "jg_ema36": float(e.jg_ema36) if not pd.isna(e.jg_ema36) else np.nan,
                            "jg_pivot_mid": float(e.jg_pivot_mid) if not pd.isna(e.jg_pivot_mid) else np.nan,
                            "jg_b3": float(e.jg_b3) if not pd.isna(e.jg_b3) else np.nan,
                            "jg_s3": float(e.jg_s3) if not pd.isna(e.jg_s3) else np.nan,
                            "jg_b5": float(e.jg_b5) if not pd.isna(e.jg_b5) else np.nan,
                            "jg_s5": float(e.jg_s5) if not pd.isna(e.jg_s5) else np.nan,
                            "jg_var2": float(e.jg_var2) if not pd.isna(e.jg_var2) else np.nan,
                            "jg_var3": float(e.jg_var3) if not pd.isna(e.jg_var3) else np.nan,
                            "jg_var3_ma6": float(e.jg_var3_ma6) if not pd.isna(e.jg_var3_ma6) else np.nan,
                            "jg_bar_yellow": bool(e.jg_bar_yellow),
                            "jg_bar_red": bool(e.jg_bar_red),
                            "jg_macd": float(e.jg_macd) if not pd.isna(e.jg_macd) else np.nan,
                            "jg_buy": bool(e.jg_buy),
                            "jg_sell": bool(e.jg_sell),
                            "jg_gold": bool(e.jg_gold),
                            "jg_ma160": float(e.jg_ma160) if not pd.isna(e.jg_ma160) else np.nan,
                            "jg_ma120": float(e.jg_ma120) if not pd.isna(e.jg_ma120) else np.nan,
                            "jg_ma60": float(e.jg_ma60) if not pd.isna(e.jg_ma60) else np.nan,
                            "jg_ma25": float(e.jg_ma25) if not pd.isna(e.jg_ma25) else np.nan,
                            "jg_flip_to_yellow": bool(e.jg_flip_to_yellow),
                            "jg_flip_to_red": bool(e.jg_flip_to_red),
                            "jg_wick_touch_ma13": bool(e.jg_wick_touch_ma13),
                            "jg_wick_touch_ma55": bool(e.jg_wick_touch_ma55),
                            "jg_wick_touch_ema27": bool(e.jg_wick_touch_ema27),
                            "jg_wick_touch_ema29": bool(e.jg_wick_touch_ema29),
                            "jg_wick_touch_ema32": bool(e.jg_wick_touch_ema32),
                            "jg_wick_touch_ema36": bool(e.jg_wick_touch_ema36),
                            "jg_close_breakdown_ma13": bool(e.jg_close_breakdown_ma13),
                            "jg_close_breakup_ma13": bool(e.jg_close_breakup_ma13),
                            "jg_close_breakdown_ma55": bool(e.jg_close_breakdown_ma55),
                            "jg_close_breakup_ma55": bool(e.jg_close_breakup_ma55),
                            "jg_cross_ma13_ema27_up": bool(e.jg_cross_ma13_ema27_up),
                            "jg_cross_ma13_ema27_down": bool(e.jg_cross_ma13_ema27_down),
                            "jg_cross_ma13_ema29_up": bool(e.jg_cross_ma13_ema29_up),
                            "jg_cross_ma13_ema29_down": bool(e.jg_cross_ma13_ema29_down),
                            "jg_cross_ma13_ema32_up": bool(e.jg_cross_ma13_ema32_up),
                            "jg_cross_ma13_ema32_down": bool(e.jg_cross_ma13_ema32_down),
                            "jg_cross_ma13_ema36_up": bool(e.jg_cross_ma13_ema36_up),
                            "jg_cross_ma13_ema36_down": bool(e.jg_cross_ma13_ema36_down),
                            "jg_after_cross_ma13_ema27_up_j_lt80": bool(e.jg_after_cross_ma13_ema27_up_j_lt80),
                            "jg_after_cross_ma13_ema27_down_j_gt20": bool(e.jg_after_cross_ma13_ema27_down_j_gt20),
                            "jg_dist_b3_atr": float(e.jg_dist_b3_atr) if not pd.isna(e.jg_dist_b3_atr) else np.nan,
                            "jg_dist_s3_atr": float(e.jg_dist_s3_atr) if not pd.isna(e.jg_dist_s3_atr) else np.nan,
                            "jg_dist_pivot_atr": float(e.jg_dist_pivot_atr) if not pd.isna(e.jg_dist_pivot_atr) else np.nan,
                            "jg_red_streak": int(e.jg_red_streak),
                            "jg_yellow_streak": int(e.jg_yellow_streak),
                            },
                            private_names=private_names,
                        )
                        for e in entries
                    ]
                ),
            )
            if not show_all:
                for e in entries:
                    _entry_last_ts_set(state, e.symbol, str(e.ts), key=last_ts_key)
        if entry_exec_rows:
            _append_csv(out_dir / "execution_log.csv", pd.DataFrame(entry_exec_rows))

    if args.get("execute") and actions:
        if not _print_trade_api_status():
            return state
        exec_rows: List[Dict[str, object]] = []
        pos_by_ticket = {int(getattr(pos, "ticket")): pos for pos in positions}
        for a in actions:
            pos = pos_by_ticket.get(int(a.ticket))
            if pos is None:
                continue
            vol = float(a.volume)
            if vol <= 0:
                continue

            r1 = _send_close_partial(pos, volume=vol)
            ok1 = bool(getattr(r1, "retcode", None) == mt5.TRADE_RETCODE_DONE)
            print(
                f"[EXEC] close_partial ticket={a.ticket} symbol={a.symbol} vol={vol:.4f} ok={ok1} ret={getattr(r1,'retcode',None)}"
            )
            exec_rows.append(
                {
                    "ts_utc": ts,
                    "ticket": int(a.ticket),
                    "symbol": str(a.symbol),
                    "op": "close_partial",
                    "volume": float(vol),
                    "retcode": getattr(r1, "retcode", None) if r1 is not None else None,
                    "comment": getattr(r1, "comment", "") if r1 is not None else "",
                }
            )
            if ok1:
                st = _ensure_pos_state(state, ticket=a.ticket, volume=float(getattr(pos, "volume")))
                if a.level_name in {"R1", "S1"}:
                    st["tp1_done"] = True
                if a.level_name in {"R2", "S2"}:
                    st["tp2_done"] = True

            if a.suggested_sl is not None:
                r2 = _send_modify_sl(pos, sl=float(a.suggested_sl))
                ok2 = bool(getattr(r2, "retcode", None) == mt5.TRADE_RETCODE_DONE)
                print(
                    f"[EXEC] modify_sl ticket={a.ticket} symbol={a.symbol} sl={a.suggested_sl:.6f} ok={ok2} ret={getattr(r2,'retcode',None)}"
                )
                exec_rows.append(
                    {
                        "ts_utc": ts,
                        "ticket": int(a.ticket),
                        "symbol": str(a.symbol),
                        "op": "modify_sl",
                        "volume": "",
                        "retcode": getattr(r2, "retcode", None) if r2 is not None else None,
                        "comment": getattr(r2, "comment", "") if r2 is not None else "",
                        "sl": float(a.suggested_sl),
                    }
                )

        if log_enabled and exec_rows:
            out_dir = _log_dir_for_run(args)
            _append_csv(out_dir / "execution_log.csv", pd.DataFrame(exec_rows))

    return state


def _run_test_trade(args: Dict[str, Any]) -> None:
    if not _print_trade_api_status():
        raise RuntimeError("trade api not enabled")

    symbol = str(args.get("test_symbol") or "EURUSD").strip()
    side = str(args.get("test_side") or "buy").strip().lower()
    if side not in {"buy", "sell"}:
        raise ValueError(f"invalid --test-side: {side}")
    close_after = max(0, int(args.get("test_close_after_sec") or 0))
    info = _ensure_symbol_ready(symbol)
    vol = _normalize_volume(info, float(args.get("test_volume") or 0.01))

    bid, ask = _get_tick(symbol)
    if side == "buy":
        order_type = mt5.ORDER_TYPE_BUY
        price = ask
        want_pos_type = mt5.POSITION_TYPE_BUY
        close_type = mt5.ORDER_TYPE_SELL
        close_px = bid
    else:
        order_type = mt5.ORDER_TYPE_SELL
        price = bid
        want_pos_type = mt5.POSITION_TYPE_SELL
        close_type = mt5.ORDER_TYPE_BUY
        close_px = ask

    req = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(vol),
        "type": int(order_type),
        "price": float(price),
        "deviation": 50,
        "type_time": mt5.ORDER_TIME_GTC,
    }
    res = _order_send_try_fillings(req)
    print(
        "[TEST] open",
        "symbol",
        symbol,
        "side",
        side,
        "vol",
        vol,
        "ret",
        None if res is None else (res.retcode, res.comment, res.order, res.deal),
    )
    if res is None or getattr(res, "retcode", None) != mt5.TRADE_RETCODE_DONE:
        raise RuntimeError(f"test open failed: {None if res is None else (res.retcode, res.comment)}")

    if close_after > 0:
        time.sleep(float(close_after))

    ps = mt5.positions_get(symbol=symbol) or []
    ps2 = [p for p in ps if int(getattr(p, "type", -1)) == int(want_pos_type)]
    if not ps2:
        raise RuntimeError("position not found after open")
    pos = sorted(ps2, key=lambda x: float(getattr(x, "volume", 0.0)), reverse=True)[0]

    req2 = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(getattr(pos, "volume")),
        "type": int(close_type),
        "position": int(getattr(pos, "ticket")),
        "price": float(close_px),
        "deviation": 50,
        "type_time": mt5.ORDER_TIME_GTC,
    }
    res2 = _order_send_try_fillings(req2)
    print(
        "[TEST] close",
        "ticket",
        int(getattr(pos, "ticket")),
        "vol",
        float(getattr(pos, "volume")),
        "ret",
        None if res2 is None else (res2.retcode, res2.comment, res2.order, res2.deal),
    )
    if res2 is None or getattr(res2, "retcode", None) != mt5.TRADE_RETCODE_DONE:
        raise RuntimeError(f"test close failed: {None if res2 is None else (res2.retcode, res2.comment)}")


def _pick_symbol(available: set[str], candidates: List[str]) -> Optional[str]:
    cands = [str(x).strip() for x in candidates if str(x).strip()]
    for c in cands:
        if c in available:
            return c
    upper_map = {a.upper(): a for a in available}
    for c in cands:
        u = c.upper()
        if u in upper_map:
            return upper_map[u]
    for c in cands:
        u = c.upper()
        for a in available:
            au = a.upper()
            if au == u or au.startswith(u) or au.endswith(u) or (u in au):
                return a
    return None


def _valid_sl_for_side(symbol: str, side: str, entry_price: float) -> float:
    info = mt5.symbol_info(symbol)
    if info is None:
        raise RuntimeError(f"symbol_info returned None: {symbol}")
    point = float(getattr(info, "point", 0.0) or 0.0)
    if point <= 0:
        point = 0.00001
    stops_level = float(getattr(info, "trade_stops_level", 0.0) or 0.0)
    min_dist = max(stops_level * point, 20.0 * point)
    bid, ask = _get_tick(symbol)
    if side == "buy":
        sl = min(float(entry_price), float(bid) - float(min_dist))
        sl = float(min(sl, float(bid) - float(min_dist)))
        return sl
    sl = max(float(entry_price), float(ask) + float(min_dist))
    sl = float(max(sl, float(ask) + float(min_dist)))
    return sl


def _run_test18(args: Dict[str, Any]) -> None:
    available = {s.name for s in (mt5.symbols_get() or [])}
    base_symbol = str(args.get("test18_symbol") or "EURUSD").strip()
    sym = _pick_symbol(available, [base_symbol, base_symbol.upper(), base_symbol.lower(), "EURUSD", "EURUSD."])
    if not sym:
        raise RuntimeError(f"symbol not found: {base_symbol}")

    ok_trade = _print_trade_api_status()
    if not ok_trade:
        raise RuntimeError("trade api not enabled")

    print("[T01] mt5 initialized: OK")
    print("[T02] symbols_get:", "OK" if len(available) else "FAIL")
    print("[T03] test symbol:", sym)

    info = _ensure_symbol_ready(sym)
    print("[T04] symbol ready:", sym, "OK" if info is not None else "FAIL")

    bid, ask = _get_tick(sym)
    print("[T05] tick:", "OK" if (bid > 0 and ask > 0) else "FAIL")

    h, l, c = _yesterday_d1_hlc(sym)
    print("[T06] D1 prev HLC:", "OK" if (h > 0 and l > 0 and c > 0) else "FAIL")

    levels = _cam_levels_from_hlc(h, l, c, Params())
    ok_levels = all(k in levels and float(levels[k]) > 0 for k in ["R1", "R2", "S1", "S2"])
    print("[T07] CAM levels:", "OK" if ok_levels else "FAIL")

    vol = _normalize_volume(info, float(args.get("test18_volume") or 0.01))
    req = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": sym,
        "volume": float(vol),
        "type": int(mt5.ORDER_TYPE_BUY),
        "price": float(ask),
        "deviation": 50,
        "type_time": mt5.ORDER_TIME_GTC,
    }
    res = _order_send_try_fillings(req)
    print("[T08] open buy:", None if res is None else (res.retcode, res.comment))
    if res is None or getattr(res, "retcode", None) != mt5.TRADE_RETCODE_DONE:
        raise RuntimeError(f"open failed: {None if res is None else (res.retcode, res.comment)}")

    time.sleep(1.0)
    ps = mt5.positions_get(symbol=sym) or []
    if not ps:
        raise RuntimeError("position not found after open")
    pos = sorted(ps, key=lambda x: float(getattr(x, "volume", 0.0)), reverse=True)[0]
    entry_price = float(getattr(pos, "price_open"))
    print("[T09] position appeared:", "OK", "ticket", int(getattr(pos, "ticket")))

    sl = _valid_sl_for_side(sym, "buy", entry_price=entry_price)
    res_sl = _send_modify_sl(pos, sl=sl)
    print("[T10] set SL:", None if res_sl is None else (res_sl.retcode, res_sl.comment))
    if res_sl is None or getattr(res_sl, "retcode", None) != mt5.TRADE_RETCODE_DONE:
        raise RuntimeError(f"set sl failed: {None if res_sl is None else (res_sl.retcode, res_sl.comment)}")

    info2 = _ensure_symbol_ready(sym)
    v_now = float(getattr(pos, "volume", 0.0))
    v_half = _normalize_volume(info2, max(float(getattr(info2, "volume_min", 0.0) or 0.0), v_now * 0.5))
    if v_half >= v_now:
        v_half = _normalize_volume(info2, max(float(getattr(info2, "volume_min", 0.0) or 0.0), v_now))
    if v_half > 0 and v_half < v_now:
        res_pc = _send_close_partial(pos, volume=v_half)
        print("[T11] partial close:", None if res_pc is None else (res_pc.retcode, res_pc.comment))
        if res_pc is None or getattr(res_pc, "retcode", None) != mt5.TRADE_RETCODE_DONE:
            raise RuntimeError(f"partial close failed: {None if res_pc is None else (res_pc.retcode, res_pc.comment)}")
    else:
        print("[T11] partial close: SKIP")

    time.sleep(1.0)
    ps2 = mt5.positions_get(symbol=sym) or []
    if not ps2:
        print("[T12] remaining close: SKIP (already flat)")
    else:
        pos2 = sorted(ps2, key=lambda x: float(getattr(x, "volume", 0.0)), reverse=True)[0]
        res_c = _send_close_partial(pos2, volume=float(getattr(pos2, "volume")))
        print("[T12] remaining close:", None if res_c is None else (res_c.retcode, res_c.comment))
        if res_c is None or getattr(res_c, "retcode", None) != mt5.TRADE_RETCODE_DONE:
            raise RuntimeError(f"close failed: {None if res_c is None else (res_c.retcode, res_c.comment)}")

    time.sleep(1.0)
    ps3 = mt5.positions_get(symbol=sym) or []
    print("[T13] flat:", "OK" if len(ps3) == 0 else f"FAIL positions={len(ps3)}")
    print("[T14] done: OK")


def _export_history(args: Dict[str, Any]) -> Path:
    out_dir = _log_dir_for_run(args)

    from_s = str(args.get("export_from") or "").strip()
    to_s = str(args.get("export_to") or "").strip()
    if bool(args.get("export_today")) or (not from_s and not to_s):
        dt0 = _utc_midnight()
        dt1 = datetime.now()
    else:
        dt0 = _parse_iso_dt_utc(from_s) if from_s else _utc_midnight()
        dt1 = _parse_iso_dt_utc(to_s) if to_s else datetime.now()

    deals = mt5.history_deals_get(dt0, dt1)
    if deals is None:
        raise RuntimeError(f"history_deals_get returned None, error={_mt5_last_error()}")
    orders = mt5.history_orders_get(dt0, dt1)
    if orders is None:
        raise RuntimeError(f"history_orders_get returned None, error={_mt5_last_error()}")

    ddf = pd.DataFrame(list(deals))
    odf = pd.DataFrame(list(orders))
    if ddf.empty:
        ddf = pd.DataFrame(
            columns=[
                "ticket",
                "order",
                "time",
                "time_msc",
                "type",
                "entry",
                "magic",
                "position_id",
                "reason",
                "volume",
                "price",
                "commission",
                "swap",
                "profit",
                "fee",
                "symbol",
                "comment",
                "external_id",
            ]
        )
    if odf.empty:
        odf = pd.DataFrame(
            columns=[
                "ticket",
                "time_setup",
                "time_setup_msc",
                "time_done",
                "time_done_msc",
                "type",
                "state",
                "magic",
                "position_id",
                "volume_initial",
                "volume_current",
                "price_open",
                "sl",
                "tp",
                "symbol",
                "comment",
                "external_id",
            ]
        )

    _write_csv(out_dir / "mt5_deals.csv", ddf)
    _write_csv(out_dir / "mt5_orders.csv", odf)
    print(f"[EXPORT] {dt0.isoformat()} -> {dt1.isoformat()} deals={len(ddf)} orders={len(odf)} dir={str(out_dir)}")
    return out_dir


def _summary_today(args: Dict[str, Any]) -> None:
    out_dir = _export_history({**args, "export_today": True})
    deals_path = out_dir / "mt5_deals.csv"
    if not deals_path.exists():
        print("[SUMMARY] no deals file")
        return
    try:
        d = pd.read_csv(deals_path)
    except Exception:
        print("[SUMMARY] no deals today")
        return
    if d.empty:
        print("[SUMMARY] no deals today")
        return

    for c in ["profit", "commission", "swap", "volume", "price"]:
        if c in d.columns:
            d[c] = pd.to_numeric(d[c], errors="coerce")
    if "profit" not in d.columns:
        d["profit"] = 0.0
    d["commission"] = pd.to_numeric(d.get("commission", 0.0), errors="coerce").fillna(0.0)
    d["swap"] = pd.to_numeric(d.get("swap", 0.0), errors="coerce").fillna(0.0)
    d["profit"] = pd.to_numeric(d.get("profit", 0.0), errors="coerce").fillna(0.0)
    d["pnl"] = d["profit"] + d["swap"] + d["commission"]

    sym = d["symbol"].astype(str) if "symbol" in d.columns else pd.Series([""], index=d.index, dtype="string")
    out = (
        pd.DataFrame({"symbol": sym, "pnl": d["pnl"]})
        .groupby("symbol", observed=True)
        .agg(deals=("pnl", "size"), pnl=("pnl", "sum"))
        .reset_index()
        .sort_values(["pnl"], ascending=[False])
    )
    total = float(out["pnl"].sum()) if not out.empty else 0.0
    out2 = pd.concat([out, pd.DataFrame([{"symbol": "__TOTAL__", "deals": float(out["deals"].sum()), "pnl": total}])], ignore_index=True)
    _write_csv(out_dir / "daily_summary.csv", out2)
    with pd.option_context("display.max_rows", 200, "display.width", 200):
        print(out2.to_string(index=False))


def _paper_replay(args: Dict[str, Any]) -> None:
    src = str(args.get("paper_dir") or "").strip()
    if src:
        src_dir = Path(src)
    else:
        src_dir = _log_dir_for_run(args)
    private_names = bool(int(args.get("private_names", 0) or 0))
    if not src_dir.exists():
        raise FileNotFoundError(f"paper_dir not found: {str(src_dir)}")

    entry_files: List[Path] = []
    direct6 = src_dir / "entries_suggested_v7.csv"
    direct5 = src_dir / "entries_suggested_v6.csv"
    direct4 = src_dir / "entries_suggested_v5.csv"
    direct3 = src_dir / "entries_suggested_v4.csv"
    direct2 = src_dir / "entries_suggested_v3.csv"
    direct1 = src_dir / "entries_suggested_v2.csv"
    direct0 = src_dir / "entries_suggested.csv"
    entry_files = []
    if direct6.exists():
        entry_files = [direct6]
    elif direct5.exists():
        entry_files = [direct5]
    elif direct4.exists():
        entry_files = [direct4]
    elif direct3.exists():
        entry_files = [direct3]
    elif direct2.exists():
        entry_files = [direct2]
    elif direct1.exists():
        entry_files = [direct1]
    elif direct0.exists():
        entry_files = [direct0]
        entry_files = sorted(
            list(src_dir.rglob("entries_suggested_v7.csv"))
            + list(src_dir.rglob("entries_suggested_v6.csv"))
            + list(src_dir.rglob("entries_suggested_v5.csv"))
            + list(src_dir.rglob("entries_suggested_v4.csv"))
            + list(src_dir.rglob("entries_suggested_v3.csv"))
            + list(src_dir.rglob("entries_suggested_v2.csv"))
            + list(src_dir.rglob("entries_suggested.csv"))
        )
    if not entry_files:
        raise FileNotFoundError(f"no entries_suggested.csv under: {str(src_dir)}")

    dfs: List[pd.DataFrame] = []
    for f in entry_files:
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        if df is not None and not df.empty:
            df = df.copy()
            df["__src"] = str(f)
            dfs.append(df)
    if not dfs:
        raise RuntimeError(f"entries files unreadable or empty under: {str(src_dir)}")

    raw = pd.concat(dfs, axis=0, ignore_index=True)
    if "sig_ts" not in raw.columns:
        raw["sig_ts"] = raw.get("ts_utc", "")
    raw["sig_ts"] = pd.to_datetime(raw["sig_ts"], errors="coerce")
    raw["ts_utc"] = pd.to_datetime(raw.get("ts_utc", ""), errors="coerce", utc=True)
    raw = raw.dropna(subset=["sig_ts"])
    for c in ["entry", "stop", "atr", "entry_score"]:
        if c in raw.columns:
            raw[c] = pd.to_numeric(raw[c], errors="coerce")
    raw["symbol"] = raw.get("symbol", "").astype(str).str.upper()
    raw["side"] = raw.get("side", "").astype(str).str.upper()
    raw["signal"] = raw.get("signal", "").astype(str).str.upper()

    raw = raw.sort_values(["ts_utc"], ascending=[True]).reset_index(drop=True)
    raw = raw.drop_duplicates(subset=["symbol", "sig_ts", "side", "signal", "entry", "stop"], keep="last").reset_index(drop=True)
    raw = raw[(raw["symbol"] != "") & (raw["side"].isin(["LONG", "SHORT"])) & (raw["entry"].notna()) & (raw["stop"].notna())]
    if raw.empty:
        raise RuntimeError("no valid rows after dedup/filter")

    lookahead = max(1, int(args.get("paper_lookahead_bars") or 48))
    tp1_r = float(args.get("paper_tp1_r") or 1.0)
    tp2_r = float(args.get("paper_tp2_r") or 2.0)
    local_tz = datetime.now().astimezone().tzinfo
    bar_rule = str(args.get("paper_bar_rule") or "sl_first").strip().lower()
    if bar_rule not in {"sl_first", "tp_first"}:
        raise ValueError(f"unknown paper_bar_rule: {bar_rule}")
    e2_chase_max_raw = args.get("paper_e2_chase_max", None)
    try:
        e2_chase_max = float(e2_chase_max_raw) if e2_chase_max_raw is not None and str(e2_chase_max_raw).strip() != "" else None
    except Exception:
        e2_chase_max = None
    if e2_chase_max is not None and not (float(e2_chase_max) > 0):
        e2_chase_max = None

    raw["_symbol_res"] = raw["symbol"].astype(str).map(lambda s: _resolve_symbol(s))
    sym_cache: Dict[str, pd.DataFrame] = {}
    lookback_h = 520
    for sym_res, g in raw.groupby("_symbol_res", observed=True):
        sym_res = str(sym_res).strip()
        if not sym_res:
            continue
        _ensure_symbol_ready(sym_res)
        g_ts = pd.to_datetime(g["sig_ts"], errors="coerce").dropna()
        if g_ts.empty:
            continue
        dt_min = g_ts.min().to_pydatetime()
        dt_max = g_ts.max().to_pydatetime()
        dt0 = dt_min - timedelta(hours=int(lookback_h))
        dt1 = dt_max + timedelta(hours=int(lookahead) + 10)
        rates = mt5.copy_rates_range(sym_res, mt5.TIMEFRAME_H1, dt0, dt1)
        if rates is None or len(rates) <= 2:
            n = int(max(10, min(60000, int((dt1 - dt0).total_seconds() / 3600.0) + 10)))
            rates = mt5.copy_rates_from(sym_res, mt5.TIMEFRAME_H1, dt0, n)
        if rates is None or len(rates) <= 2:
            continue
        df_sym = pd.DataFrame(rates)
        if "time" not in df_sym.columns:
            continue
        ts_open = pd.to_datetime(df_sym["time"].astype(int), unit="s", utc=True).dt.tz_convert(local_tz).dt.tz_localize(None)
        df_sym["ts"] = ts_open + timedelta(hours=1)
        df_sym = df_sym.sort_values("ts").reset_index(drop=True)
        z = _zrf_macd_from_close(df_sym["close"])
        a = _adx_from_ohlc(df_sym["high"], df_sym["low"], df_sym["close"], 14)
        cci144 = _cci_from_ohlc(df_sym["high"], df_sym["low"], df_sym["close"], 144)
        df_sym = pd.concat([df_sym, z.reset_index(drop=True), a.reset_index(drop=True)], axis=1)
        df_sym["cci144"] = cci144.reset_index(drop=True)
        sym_cache[str(sym_res)] = df_sym

    rows: List[Dict[str, object]] = []
    for r in raw.itertuples(index=False):
        sym = str(getattr(r, "_symbol_res", getattr(r, "symbol", "")))
        sym = _resolve_symbol(sym)
        _ensure_symbol_ready(sym)
        side = str(getattr(r, "side"))
        sig_ts = getattr(r, "sig_ts")
        entry = float(getattr(r, "entry"))
        stop = float(getattr(r, "stop"))
        signal = str(getattr(r, "signal"))
        score = float(getattr(r, "entry_score")) if hasattr(r, "entry_score") and not pd.isna(getattr(r, "entry_score")) else np.nan
        atr_v = float(getattr(r, "atr")) if hasattr(r, "atr") and not pd.isna(getattr(r, "atr")) else np.nan
        ema21_1h_v = float(getattr(r, "ema21_1h")) if hasattr(r, "ema21_1h") and not pd.isna(getattr(r, "ema21_1h")) else np.nan
        breakout_level_v = float(getattr(r, "breakout_level")) if hasattr(r, "breakout_level") and not pd.isna(getattr(r, "breakout_level")) else np.nan
        touch_delta_v = int(getattr(r, "touch_delta")) if hasattr(r, "touch_delta") and not pd.isna(getattr(r, "touch_delta")) else np.nan
        strong_v = bool(getattr(r, "strong")) if hasattr(r, "strong") and not pd.isna(getattr(r, "strong")) else np.nan
        kd_w1_long_v = bool(getattr(r, "kd_w1_long")) if hasattr(r, "kd_w1_long") and not pd.isna(getattr(r, "kd_w1_long")) else np.nan
        kd_w1_short_v = bool(getattr(r, "kd_w1_short")) if hasattr(r, "kd_w1_short") and not pd.isna(getattr(r, "kd_w1_short")) else np.nan
        kd_3line_long_v = bool(getattr(r, "kd_3line_long")) if hasattr(r, "kd_3line_long") and not pd.isna(getattr(r, "kd_3line_long")) else np.nan
        kd_3line_short_v = bool(getattr(r, "kd_3line_short")) if hasattr(r, "kd_3line_short") and not pd.isna(getattr(r, "kd_3line_short")) else np.nan
        ts_utc_v = getattr(r, "ts_utc") if hasattr(r, "ts_utc") else pd.NaT
        src_v = str(getattr(r, "__src")) if hasattr(r, "__src") else ""
        chase_dist_atr_v = float("inf")
        if not pd.isna(atr_v) and float(atr_v) > 0 and not pd.isna(ema21_1h_v):
            chase_dist_atr_v = float(abs(float(entry) - float(ema21_1h_v)) / float(atr_v))

        df_sym = sym_cache.get(str(sym))
        if df_sym is None or df_sym.empty:
            continue
        df = df_sym[df_sym["ts"] >= pd.to_datetime(sig_ts)].reset_index(drop=True)
        if df.empty:
            continue
        z0 = df.iloc[0]
        zrf_diff_v = float(z0["zrf_diff"]) if "zrf_diff" in df.columns and not pd.isna(z0["zrf_diff"]) else np.nan
        zrf_dea_v = float(z0["zrf_dea"]) if "zrf_dea" in df.columns and not pd.isna(z0["zrf_dea"]) else np.nan
        zrf_ws_v = float(z0["zrf_watershed"]) if "zrf_watershed" in df.columns and not pd.isna(z0["zrf_watershed"]) else np.nan
        zrf_bull_div_v = bool(z0["zrf_m_bull_div"]) if "zrf_m_bull_div" in df.columns and not pd.isna(z0["zrf_m_bull_div"]) else np.nan
        zrf_bear_div_v = bool(z0["zrf_m_bear_div"]) if "zrf_m_bear_div" in df.columns and not pd.isna(z0["zrf_m_bear_div"]) else np.nan
        zrf_low_kc_v = bool(z0["zrf_low_kc"]) if "zrf_low_kc" in df.columns and not pd.isna(z0["zrf_low_kc"]) else np.nan
        zrf_high_dc_v = bool(z0["zrf_high_dc"]) if "zrf_high_dc" in df.columns and not pd.isna(z0["zrf_high_dc"]) else np.nan
        zrf_zb_2nd_kc_v = bool(z0["zrf_zb_2nd_kc"]) if "zrf_zb_2nd_kc" in df.columns and not pd.isna(z0["zrf_zb_2nd_kc"]) else np.nan
        zrf_za_2nd_dc_v = bool(z0["zrf_za_2nd_dc"]) if "zrf_za_2nd_dc" in df.columns and not pd.isna(z0["zrf_za_2nd_dc"]) else np.nan
        cci144_v = float(z0["cci144"]) if "cci144" in df.columns and not pd.isna(z0["cci144"]) else np.nan
        adx14_v = float(z0["adx"]) if "adx" in df.columns and not pd.isna(z0["adx"]) else np.nan
        plus_di_v = float(z0["plus_di"]) if "plus_di" in df.columns and not pd.isna(z0["plus_di"]) else np.nan
        minus_di_v = float(z0["minus_di"]) if "minus_di" in df.columns and not pd.isna(z0["minus_di"]) else np.nan

        r0 = abs(float(entry) - float(stop))
        if not (r0 > 0):
            continue
        tp1 = float(entry) + float(tp1_r) * float(r0) if side == "LONG" else float(entry) - float(tp1_r) * float(r0)
        tp2 = float(entry) + float(tp2_r) * float(r0) if side == "LONG" else float(entry) - float(tp2_r) * float(r0)

        outcome = "NONE"
        bars_to = np.nan
        realized_r = np.nan
        mfe_r = -np.inf
        mae_r = np.inf

        for i in range(min(int(lookahead), int(len(df)))):
            hi = float(df.loc[i, "high"])
            lo = float(df.loc[i, "low"])
            cl = float(df.loc[i, "close"])

            if side == "LONG":
                mfe_r = max(float(mfe_r), (hi - entry) / r0)
                mae_r = min(float(mae_r), (lo - entry) / r0)
                stop_hit = lo <= stop
                tp2_hit = hi >= tp2
                tp1_hit = hi >= tp1
                if bar_rule == "tp_first":
                    if tp2_hit:
                        outcome = "TP2"
                        bars_to = float(i)
                        realized_r = float(tp2_r)
                        break
                    if tp1_hit:
                        outcome = "TP1"
                        bars_to = float(i)
                        realized_r = float(tp1_r)
                        break
                    if stop_hit:
                        outcome = "SL"
                        bars_to = float(i)
                        realized_r = -1.0
                        break
                else:
                    if stop_hit:
                        outcome = "SL"
                        bars_to = float(i)
                        realized_r = -1.0
                        break
                    if tp2_hit:
                        outcome = "TP2"
                        bars_to = float(i)
                        realized_r = float(tp2_r)
                        break
                    if tp1_hit:
                        outcome = "TP1"
                        bars_to = float(i)
                        realized_r = float(tp1_r)
                        break
            else:
                mfe_r = max(float(mfe_r), (entry - lo) / r0)
                mae_r = min(float(mae_r), (entry - hi) / r0)
                stop_hit = hi >= stop
                tp2_hit = lo <= tp2
                tp1_hit = lo <= tp1
                if bar_rule == "tp_first":
                    if tp2_hit:
                        outcome = "TP2"
                        bars_to = float(i)
                        realized_r = float(tp2_r)
                        break
                    if tp1_hit:
                        outcome = "TP1"
                        bars_to = float(i)
                        realized_r = float(tp1_r)
                        break
                    if stop_hit:
                        outcome = "SL"
                        bars_to = float(i)
                        realized_r = -1.0
                        break
                else:
                    if stop_hit:
                        outcome = "SL"
                        bars_to = float(i)
                        realized_r = -1.0
                        break
                    if tp2_hit:
                        outcome = "TP2"
                        bars_to = float(i)
                        realized_r = float(tp2_r)
                        break
                    if tp1_hit:
                        outcome = "TP1"
                        bars_to = float(i)
                        realized_r = float(tp1_r)
                        break

        if outcome == "NONE":
            last_close = float(df.loc[min(int(lookahead) - 1, len(df) - 1), "close"])
            realized_r = (last_close - entry) / r0 if side == "LONG" else (entry - last_close) / r0
            bars_to = float(min(int(lookahead) - 1, len(df) - 1))

        rows.append(
            _apply_private_names(
                {
                "symbol": sym,
                "signal": signal,
                "side": side,
                "ts_utc": str(pd.to_datetime(ts_utc_v)) if not pd.isna(ts_utc_v) else "",
                "sig_ts": str(pd.to_datetime(sig_ts)),
                "entry": float(entry),
                "stop": float(stop),
                "atr": float(atr_v) if not pd.isna(atr_v) else np.nan,
                "r0": float(r0),
                "tp1": float(tp1),
                "tp2": float(tp2),
                "outcome": outcome,
                "bars_to_outcome": bars_to,
                "realized_r": float(realized_r),
                "mfe_r": float(mfe_r) if np.isfinite(mfe_r) else np.nan,
                "mae_r": float(mae_r) if np.isfinite(mae_r) else np.nan,
                "entry_score": float(score) if not pd.isna(score) else np.nan,
                "ema21_1h": float(ema21_1h_v) if not pd.isna(ema21_1h_v) else np.nan,
                "breakout_level": float(breakout_level_v) if not pd.isna(breakout_level_v) else np.nan,
                "touch_delta": int(touch_delta_v) if not pd.isna(touch_delta_v) else np.nan,
                "strong": bool(strong_v) if not pd.isna(strong_v) else np.nan,
                "kd_w1_long": bool(kd_w1_long_v) if not pd.isna(kd_w1_long_v) else np.nan,
                "kd_w1_short": bool(kd_w1_short_v) if not pd.isna(kd_w1_short_v) else np.nan,
                "kd_3line_long": bool(kd_3line_long_v) if not pd.isna(kd_3line_long_v) else np.nan,
                "kd_3line_short": bool(kd_3line_short_v) if not pd.isna(kd_3line_short_v) else np.nan,
                "chase_dist_atr": float(chase_dist_atr_v) if not pd.isna(chase_dist_atr_v) else np.nan,
                "tick_volume": float(getattr(r, "tick_volume")) if hasattr(r, "tick_volume") and not pd.isna(getattr(r, "tick_volume")) else np.nan,
                "vol_ratio": float(getattr(r, "vol_ratio")) if hasattr(r, "vol_ratio") and not pd.isna(getattr(r, "vol_ratio")) else np.nan,
                "vol_pct": float(getattr(r, "vol_pct")) if hasattr(r, "vol_pct") and not pd.isna(getattr(r, "vol_pct")) else np.nan,
                "atr_rel": float(getattr(r, "atr_rel")) if hasattr(r, "atr_rel") and not pd.isna(getattr(r, "atr_rel")) else np.nan,
                "atr_pct": float(getattr(r, "atr_pct")) if hasattr(r, "atr_pct") and not pd.isna(getattr(r, "atr_pct")) else np.nan,
                "spread_rel": float(getattr(r, "spread_rel")) if hasattr(r, "spread_rel") and not pd.isna(getattr(r, "spread_rel")) else np.nan,
                "liquidity_risk": bool(getattr(r, "liquidity_risk")) if hasattr(r, "liquidity_risk") and not pd.isna(getattr(r, "liquidity_risk")) else np.nan,
                "vol_risk_vol_ratio_max": float(getattr(r, "vol_risk_vol_ratio_max")) if hasattr(r, "vol_risk_vol_ratio_max") and not pd.isna(getattr(r, "vol_risk_vol_ratio_max")) else np.nan,
                "vol_risk_vol_pct_max": float(getattr(r, "vol_risk_vol_pct_max")) if hasattr(r, "vol_risk_vol_pct_max") and not pd.isna(getattr(r, "vol_risk_vol_pct_max")) else np.nan,
                "vol_risk_action": str(getattr(r, "vol_risk_action")) if hasattr(r, "vol_risk_action") and not pd.isna(getattr(r, "vol_risk_action")) else "",
                "vol_risk_blocked": bool(getattr(r, "vol_risk_blocked")) if hasattr(r, "vol_risk_blocked") and not pd.isna(getattr(r, "vol_risk_blocked")) else np.nan,
                "sr_support": float(getattr(r, "sr_support")) if hasattr(r, "sr_support") and not pd.isna(getattr(r, "sr_support")) else np.nan,
                "sr_resistance": float(getattr(r, "sr_resistance")) if hasattr(r, "sr_resistance") and not pd.isna(getattr(r, "sr_resistance")) else np.nan,
                "sr_support_dist_atr": float(getattr(r, "sr_support_dist_atr")) if hasattr(r, "sr_support_dist_atr") and not pd.isna(getattr(r, "sr_support_dist_atr")) else np.nan,
                "sr_resistance_dist_atr": float(getattr(r, "sr_resistance_dist_atr")) if hasattr(r, "sr_resistance_dist_atr") and not pd.isna(getattr(r, "sr_resistance_dist_atr")) else np.nan,
                "sr_support_touches": int(getattr(r, "sr_support_touches")) if hasattr(r, "sr_support_touches") and not pd.isna(getattr(r, "sr_support_touches")) else np.nan,
                "sr_resistance_touches": int(getattr(r, "sr_resistance_touches")) if hasattr(r, "sr_resistance_touches") and not pd.isna(getattr(r, "sr_resistance_touches")) else np.nan,
                "jg_macd_up": bool(getattr(r, "jg_macd_up")) if hasattr(r, "jg_macd_up") and not pd.isna(getattr(r, "jg_macd_up")) else np.nan,
                "jg_macd_down": bool(getattr(r, "jg_macd_down")) if hasattr(r, "jg_macd_down") and not pd.isna(getattr(r, "jg_macd_down")) else np.nan,
                "jg_sma175": float(getattr(r, "jg_sma175")) if hasattr(r, "jg_sma175") and not pd.isna(getattr(r, "jg_sma175")) else np.nan,
                "jg_j": float(getattr(r, "jg_j")) if hasattr(r, "jg_j") and not pd.isna(getattr(r, "jg_j")) else np.nan,
                "jg_long": bool(getattr(r, "jg_long")) if hasattr(r, "jg_long") and not pd.isna(getattr(r, "jg_long")) else np.nan,
                "jg_short": bool(getattr(r, "jg_short")) if hasattr(r, "jg_short") and not pd.isna(getattr(r, "jg_short")) else np.nan,
                "jg_ma13": float(getattr(r, "jg_ma13")) if hasattr(r, "jg_ma13") and not pd.isna(getattr(r, "jg_ma13")) else np.nan,
                "jg_ma55": float(getattr(r, "jg_ma55")) if hasattr(r, "jg_ma55") and not pd.isna(getattr(r, "jg_ma55")) else np.nan,
                "jg_ema20": float(getattr(r, "jg_ema20")) if hasattr(r, "jg_ema20") and not pd.isna(getattr(r, "jg_ema20")) else np.nan,
                "jg_ema27": float(getattr(r, "jg_ema27")) if hasattr(r, "jg_ema27") and not pd.isna(getattr(r, "jg_ema27")) else np.nan,
                "jg_ema29": float(getattr(r, "jg_ema29")) if hasattr(r, "jg_ema29") and not pd.isna(getattr(r, "jg_ema29")) else np.nan,
                "jg_ema32": float(getattr(r, "jg_ema32")) if hasattr(r, "jg_ema32") and not pd.isna(getattr(r, "jg_ema32")) else np.nan,
                "jg_ema36": float(getattr(r, "jg_ema36")) if hasattr(r, "jg_ema36") and not pd.isna(getattr(r, "jg_ema36")) else np.nan,
                "jg_pivot_mid": float(getattr(r, "jg_pivot_mid")) if hasattr(r, "jg_pivot_mid") and not pd.isna(getattr(r, "jg_pivot_mid")) else np.nan,
                "jg_b3": float(getattr(r, "jg_b3")) if hasattr(r, "jg_b3") and not pd.isna(getattr(r, "jg_b3")) else np.nan,
                "jg_s3": float(getattr(r, "jg_s3")) if hasattr(r, "jg_s3") and not pd.isna(getattr(r, "jg_s3")) else np.nan,
                "jg_b5": float(getattr(r, "jg_b5")) if hasattr(r, "jg_b5") and not pd.isna(getattr(r, "jg_b5")) else np.nan,
                "jg_s5": float(getattr(r, "jg_s5")) if hasattr(r, "jg_s5") and not pd.isna(getattr(r, "jg_s5")) else np.nan,
                "jg_var2": float(getattr(r, "jg_var2")) if hasattr(r, "jg_var2") and not pd.isna(getattr(r, "jg_var2")) else np.nan,
                "jg_var3": float(getattr(r, "jg_var3")) if hasattr(r, "jg_var3") and not pd.isna(getattr(r, "jg_var3")) else np.nan,
                "jg_var3_ma6": float(getattr(r, "jg_var3_ma6")) if hasattr(r, "jg_var3_ma6") and not pd.isna(getattr(r, "jg_var3_ma6")) else np.nan,
                "jg_bar_yellow": bool(getattr(r, "jg_bar_yellow")) if hasattr(r, "jg_bar_yellow") and not pd.isna(getattr(r, "jg_bar_yellow")) else np.nan,
                "jg_bar_red": bool(getattr(r, "jg_bar_red")) if hasattr(r, "jg_bar_red") and not pd.isna(getattr(r, "jg_bar_red")) else np.nan,
                "jg_macd": float(getattr(r, "jg_macd")) if hasattr(r, "jg_macd") and not pd.isna(getattr(r, "jg_macd")) else np.nan,
                "jg_buy": bool(getattr(r, "jg_buy")) if hasattr(r, "jg_buy") and not pd.isna(getattr(r, "jg_buy")) else np.nan,
                "jg_sell": bool(getattr(r, "jg_sell")) if hasattr(r, "jg_sell") and not pd.isna(getattr(r, "jg_sell")) else np.nan,
                "jg_gold": bool(getattr(r, "jg_gold")) if hasattr(r, "jg_gold") and not pd.isna(getattr(r, "jg_gold")) else np.nan,
                "jg_ma160": float(getattr(r, "jg_ma160")) if hasattr(r, "jg_ma160") and not pd.isna(getattr(r, "jg_ma160")) else np.nan,
                "jg_ma120": float(getattr(r, "jg_ma120")) if hasattr(r, "jg_ma120") and not pd.isna(getattr(r, "jg_ma120")) else np.nan,
                "jg_ma60": float(getattr(r, "jg_ma60")) if hasattr(r, "jg_ma60") and not pd.isna(getattr(r, "jg_ma60")) else np.nan,
                "jg_ma25": float(getattr(r, "jg_ma25")) if hasattr(r, "jg_ma25") and not pd.isna(getattr(r, "jg_ma25")) else np.nan,
                "jg_flip_to_yellow": bool(getattr(r, "jg_flip_to_yellow")) if hasattr(r, "jg_flip_to_yellow") and not pd.isna(getattr(r, "jg_flip_to_yellow")) else np.nan,
                "jg_flip_to_red": bool(getattr(r, "jg_flip_to_red")) if hasattr(r, "jg_flip_to_red") and not pd.isna(getattr(r, "jg_flip_to_red")) else np.nan,
                "jg_wick_touch_ma13": bool(getattr(r, "jg_wick_touch_ma13")) if hasattr(r, "jg_wick_touch_ma13") and not pd.isna(getattr(r, "jg_wick_touch_ma13")) else np.nan,
                "jg_wick_touch_ma55": bool(getattr(r, "jg_wick_touch_ma55")) if hasattr(r, "jg_wick_touch_ma55") and not pd.isna(getattr(r, "jg_wick_touch_ma55")) else np.nan,
                "jg_wick_touch_ema27": bool(getattr(r, "jg_wick_touch_ema27")) if hasattr(r, "jg_wick_touch_ema27") and not pd.isna(getattr(r, "jg_wick_touch_ema27")) else np.nan,
                "jg_wick_touch_ema29": bool(getattr(r, "jg_wick_touch_ema29")) if hasattr(r, "jg_wick_touch_ema29") and not pd.isna(getattr(r, "jg_wick_touch_ema29")) else np.nan,
                "jg_wick_touch_ema32": bool(getattr(r, "jg_wick_touch_ema32")) if hasattr(r, "jg_wick_touch_ema32") and not pd.isna(getattr(r, "jg_wick_touch_ema32")) else np.nan,
                "jg_wick_touch_ema36": bool(getattr(r, "jg_wick_touch_ema36")) if hasattr(r, "jg_wick_touch_ema36") and not pd.isna(getattr(r, "jg_wick_touch_ema36")) else np.nan,
                "jg_close_breakdown_ma13": bool(getattr(r, "jg_close_breakdown_ma13")) if hasattr(r, "jg_close_breakdown_ma13") and not pd.isna(getattr(r, "jg_close_breakdown_ma13")) else np.nan,
                "jg_close_breakup_ma13": bool(getattr(r, "jg_close_breakup_ma13")) if hasattr(r, "jg_close_breakup_ma13") and not pd.isna(getattr(r, "jg_close_breakup_ma13")) else np.nan,
                "jg_close_breakdown_ma55": bool(getattr(r, "jg_close_breakdown_ma55")) if hasattr(r, "jg_close_breakdown_ma55") and not pd.isna(getattr(r, "jg_close_breakdown_ma55")) else np.nan,
                "jg_close_breakup_ma55": bool(getattr(r, "jg_close_breakup_ma55")) if hasattr(r, "jg_close_breakup_ma55") and not pd.isna(getattr(r, "jg_close_breakup_ma55")) else np.nan,
                "jg_cross_ma13_ema27_up": bool(getattr(r, "jg_cross_ma13_ema27_up")) if hasattr(r, "jg_cross_ma13_ema27_up") and not pd.isna(getattr(r, "jg_cross_ma13_ema27_up")) else np.nan,
                "jg_cross_ma13_ema27_down": bool(getattr(r, "jg_cross_ma13_ema27_down")) if hasattr(r, "jg_cross_ma13_ema27_down") and not pd.isna(getattr(r, "jg_cross_ma13_ema27_down")) else np.nan,
                "jg_cross_ma13_ema29_up": bool(getattr(r, "jg_cross_ma13_ema29_up")) if hasattr(r, "jg_cross_ma13_ema29_up") and not pd.isna(getattr(r, "jg_cross_ma13_ema29_up")) else np.nan,
                "jg_cross_ma13_ema29_down": bool(getattr(r, "jg_cross_ma13_ema29_down")) if hasattr(r, "jg_cross_ma13_ema29_down") and not pd.isna(getattr(r, "jg_cross_ma13_ema29_down")) else np.nan,
                "jg_cross_ma13_ema32_up": bool(getattr(r, "jg_cross_ma13_ema32_up")) if hasattr(r, "jg_cross_ma13_ema32_up") and not pd.isna(getattr(r, "jg_cross_ma13_ema32_up")) else np.nan,
                "jg_cross_ma13_ema32_down": bool(getattr(r, "jg_cross_ma13_ema32_down")) if hasattr(r, "jg_cross_ma13_ema32_down") and not pd.isna(getattr(r, "jg_cross_ma13_ema32_down")) else np.nan,
                "jg_cross_ma13_ema36_up": bool(getattr(r, "jg_cross_ma13_ema36_up")) if hasattr(r, "jg_cross_ma13_ema36_up") and not pd.isna(getattr(r, "jg_cross_ma13_ema36_up")) else np.nan,
                "jg_cross_ma13_ema36_down": bool(getattr(r, "jg_cross_ma13_ema36_down")) if hasattr(r, "jg_cross_ma13_ema36_down") and not pd.isna(getattr(r, "jg_cross_ma13_ema36_down")) else np.nan,
                "jg_after_cross_ma13_ema27_up_j_lt80": bool(getattr(r, "jg_after_cross_ma13_ema27_up_j_lt80")) if hasattr(r, "jg_after_cross_ma13_ema27_up_j_lt80") and not pd.isna(getattr(r, "jg_after_cross_ma13_ema27_up_j_lt80")) else np.nan,
                "jg_after_cross_ma13_ema27_down_j_gt20": bool(getattr(r, "jg_after_cross_ma13_ema27_down_j_gt20")) if hasattr(r, "jg_after_cross_ma13_ema27_down_j_gt20") and not pd.isna(getattr(r, "jg_after_cross_ma13_ema27_down_j_gt20")) else np.nan,
                "jg_dist_b3_atr": float(getattr(r, "jg_dist_b3_atr")) if hasattr(r, "jg_dist_b3_atr") and not pd.isna(getattr(r, "jg_dist_b3_atr")) else np.nan,
                "jg_dist_s3_atr": float(getattr(r, "jg_dist_s3_atr")) if hasattr(r, "jg_dist_s3_atr") and not pd.isna(getattr(r, "jg_dist_s3_atr")) else np.nan,
                "jg_dist_pivot_atr": float(getattr(r, "jg_dist_pivot_atr")) if hasattr(r, "jg_dist_pivot_atr") and not pd.isna(getattr(r, "jg_dist_pivot_atr")) else np.nan,
                "jg_red_streak": int(getattr(r, "jg_red_streak")) if hasattr(r, "jg_red_streak") and not pd.isna(getattr(r, "jg_red_streak")) else np.nan,
                "jg_yellow_streak": int(getattr(r, "jg_yellow_streak")) if hasattr(r, "jg_yellow_streak") and not pd.isna(getattr(r, "jg_yellow_streak")) else np.nan,
                "zrf_diff": float(zrf_diff_v) if not pd.isna(zrf_diff_v) else np.nan,
                "zrf_dea": float(zrf_dea_v) if not pd.isna(zrf_dea_v) else np.nan,
                "zrf_watershed": float(zrf_ws_v) if not pd.isna(zrf_ws_v) else np.nan,
                "zrf_m_bull_div": bool(zrf_bull_div_v) if not pd.isna(zrf_bull_div_v) else np.nan,
                "zrf_m_bear_div": bool(zrf_bear_div_v) if not pd.isna(zrf_bear_div_v) else np.nan,
                "zrf_low_kc": bool(zrf_low_kc_v) if not pd.isna(zrf_low_kc_v) else np.nan,
                "zrf_high_dc": bool(zrf_high_dc_v) if not pd.isna(zrf_high_dc_v) else np.nan,
                "zrf_zb_2nd_kc": bool(zrf_zb_2nd_kc_v) if not pd.isna(zrf_zb_2nd_kc_v) else np.nan,
                "zrf_za_2nd_dc": bool(zrf_za_2nd_dc_v) if not pd.isna(zrf_za_2nd_dc_v) else np.nan,
                "cci144": float(cci144_v) if not pd.isna(cci144_v) else np.nan,
                "cci144_lt_m144": bool(float(cci144_v) < -144.0) if not pd.isna(cci144_v) else np.nan,
                "cci144_gt_p144": bool(float(cci144_v) > 144.0) if not pd.isna(cci144_v) else np.nan,
                "adx14": float(adx14_v) if not pd.isna(adx14_v) else np.nan,
                "plus_di14": float(plus_di_v) if not pd.isna(plus_di_v) else np.nan,
                "minus_di14": float(minus_di_v) if not pd.isna(minus_di_v) else np.nan,
                "__src": str(src_v),
                },
                private_names=private_names,
            )
        )

    out_df = pd.DataFrame(rows)
    out_dir = src_dir
    _write_csv(out_dir / "paper_replay_trades.csv", out_df)

    if out_df.empty:
        _write_csv(out_dir / "paper_replay_summary.csv", pd.DataFrame([{"trades": 0}]))
        print("[PAPER] no trades produced (insufficient rates or invalid rows)")
        return

    out_df["realized_r"] = pd.to_numeric(out_df["realized_r"], errors="coerce")
    out_df["is_win"] = out_df["realized_r"] > 0
    summ = (
        out_df.groupby(["symbol", "signal"], observed=True)
        .agg(
            n=("realized_r", "size"),
            win_rate=("is_win", "mean"),
            avg_r=("realized_r", "mean"),
            sl_rate=("outcome", lambda s: float((s == "SL").mean())),
            tp1_rate=("outcome", lambda s: float((s == "TP1").mean())),
            tp2_rate=("outcome", lambda s: float((s == "TP2").mean())),
            none_rate=("outcome", lambda s: float((s == "NONE").mean())),
            avg_mfe_r=("mfe_r", "mean"),
            avg_mae_r=("mae_r", "mean"),
        )
        .reset_index()
        .sort_values(["n", "avg_r"], ascending=[False, False])
    )
    total = pd.DataFrame(
        [
            {
                "symbol": "__TOTAL__",
                "signal": "",
                "n": float(len(out_df)),
                "win_rate": float(out_df["is_win"].mean()),
                "avg_r": float(out_df["realized_r"].mean()),
                "sl_rate": float((out_df["outcome"] == "SL").mean()),
                "tp1_rate": float((out_df["outcome"] == "TP1").mean()),
                "tp2_rate": float((out_df["outcome"] == "TP2").mean()),
                "none_rate": float((out_df["outcome"] == "NONE").mean()),
                "avg_mfe_r": float(pd.to_numeric(out_df["mfe_r"], errors="coerce").mean()),
                "avg_mae_r": float(pd.to_numeric(out_df["mae_r"], errors="coerce").mean()),
            }
        ]
    )
    summ2 = pd.concat([summ, total], axis=0, ignore_index=True)
    if e2_chase_max is not None:
        def _summ_row(df_sub: pd.DataFrame, label: str) -> Dict[str, object]:
            df_sub = df_sub.copy()
            df_sub["realized_r"] = pd.to_numeric(df_sub.get("realized_r", np.nan), errors="coerce")
            df_sub["is_win"] = pd.to_numeric(df_sub.get("realized_r", np.nan), errors="coerce") > 0
            return {
                "symbol": "__TOTAL__",
                "signal": str(label),
                "n": float(len(df_sub)),
                "win_rate": float(df_sub["is_win"].mean()) if len(df_sub) else np.nan,
                "avg_r": float(df_sub["realized_r"].mean()) if len(df_sub) else np.nan,
                "sl_rate": float((df_sub.get("outcome", "") == "SL").mean()) if len(df_sub) else np.nan,
                "tp1_rate": float((df_sub.get("outcome", "") == "TP1").mean()) if len(df_sub) else np.nan,
                "tp2_rate": float((df_sub.get("outcome", "") == "TP2").mean()) if len(df_sub) else np.nan,
                "none_rate": float((df_sub.get("outcome", "") == "NONE").mean()) if len(df_sub) else np.nan,
                "avg_mfe_r": float(pd.to_numeric(df_sub.get("mfe_r", np.nan), errors="coerce").mean()) if len(df_sub) else np.nan,
                "avg_mae_r": float(pd.to_numeric(df_sub.get("mae_r", np.nan), errors="coerce").mean()) if len(df_sub) else np.nan,
            }

        thr = float(e2_chase_max)
        thr_s = ("%g" % thr).strip()
        e2_base = out_df[out_df["signal"] == "E2"].copy()
        e2c = e2_base[(pd.to_numeric(e2_base.get("chase_dist_atr", np.nan), errors="coerce") < thr)].copy()
        e1 = out_df[out_df["signal"] == "E1"].copy()
        e1_e2c = pd.concat([e1, e2c], axis=0, ignore_index=True)

        extra = pd.DataFrame(
            [
                _summ_row(e2_base, "E2_base"),
                _summ_row(e2c, f"E2c<{thr_s}"),
                _summ_row(e1_e2c, f"E1+E2c<{thr_s}"),
            ]
        )
        summ2 = pd.concat([summ2, extra], axis=0, ignore_index=True)

        kept_share = float(len(e2c) / len(e2_base)) if len(e2_base) else 0.0
        print(f"[PAPER][E2GATE] chase_dist_atr < {thr_s}: e2_base_n={len(e2_base)} e2c_n={len(e2c)} kept_share={kept_share:.4f}")
        if len(e2_base):
            print(f"[PAPER][E2GATE] e2_base_avg_r={float(pd.to_numeric(e2_base['realized_r'], errors='coerce').mean()):.6f} e2_base_sl_rate={float((e2_base['outcome']=='SL').mean()):.6f}")
        if len(e2c):
            print(f"[PAPER][E2GATE] e2c_avg_r={float(pd.to_numeric(e2c['realized_r'], errors='coerce').mean()):.6f} e2c_sl_rate={float((e2c['outcome']=='SL').mean()):.6f}")
        if len(e1_e2c):
            print(f"[PAPER][E2GATE] e1_e2c_avg_r={float(pd.to_numeric(e1_e2c['realized_r'], errors='coerce').mean()):.6f} e1_e2c_sl_rate={float((e1_e2c['outcome']=='SL').mean()):.6f}")
    if bool(int(args.get("paper_e1_diagnose") or 0) != 0):
        e1_df = out_df[out_df["signal"] == "E1"].copy()
        if not e1_df.empty:
            e1_df["realized_r"] = pd.to_numeric(e1_df.get("realized_r", np.nan), errors="coerce")
            e1_df["is_win"] = pd.to_numeric(e1_df.get("realized_r", np.nan), errors="coerce") > 0
            e1_base = pd.DataFrame(
                [
                    {
                        "group": "E1_BASE",
                        "key": "__TOTAL__",
                        "n": float(len(e1_df)),
                        "win_rate": float(e1_df["is_win"].mean()),
                        "avg_r": float(e1_df["realized_r"].mean()),
                        "sl_rate": float((e1_df["outcome"] == "SL").mean()),
                        "tp1_rate": float((e1_df["outcome"] == "TP1").mean()),
                        "tp2_rate": float((e1_df["outcome"] == "TP2").mean()),
                        "none_rate": float((e1_df["outcome"] == "NONE").mean()),
                    }
                ]
            )
            atr_col = pd.to_numeric(e1_df.get("atr", np.nan), errors="coerce")
            e1_df["_atr"] = atr_col
            med = float(atr_col.median()) if atr_col.notna().any() else np.nan
            e1_df["_atr_bucket"] = np.where(e1_df["_atr"].notna() & (e1_df["_atr"] <= med), "ATR_LOW", "ATR_HIGH")
            e1_atr = (
                e1_df[e1_df["_atr"].notna()]
                .groupby(["_atr_bucket"], observed=True)
                .agg(
                    n=("realized_r", "size"),
                    win_rate=("is_win", "mean"),
                    avg_r=("realized_r", "mean"),
                    sl_rate=("outcome", lambda s: float((s == "SL").mean())),
                    tp1_rate=("outcome", lambda s: float((s == "TP1").mean())),
                    tp2_rate=("outcome", lambda s: float((s == "TP2").mean())),
                    none_rate=("outcome", lambda s: float((s == "NONE").mean())),
                    atr_median=("_atr", "median"),
                )
                .reset_index()
                .rename(columns={"_atr_bucket": "key"})
            )
            e1_atr.insert(0, "group", "E1_ATR_MEDIAN_SPLIT")
            e1_kd3 = pd.DataFrame()
            if ("kd_3line_long" in e1_df.columns) and ("kd_3line_short" in e1_df.columns) and ("side" in e1_df.columns):
                kd3l = pd.to_numeric(e1_df.get("kd_3line_long", np.nan), errors="coerce")
                kd3s = pd.to_numeric(e1_df.get("kd_3line_short", np.nan), errors="coerce")
                side_s = e1_df.get("side", "").astype(str).str.upper()
                e1_df["_kd3_ok"] = np.where(side_s == "SHORT", kd3s, kd3l)
                e1_df["_kd3_ok"] = pd.to_numeric(e1_df["_kd3_ok"], errors="coerce")
                e1_kd3 = (
                    e1_df[e1_df["_kd3_ok"].notna()]
                    .groupby(["_kd3_ok"], observed=True)
                    .agg(
                        n=("realized_r", "size"),
                        win_rate=("is_win", "mean"),
                        avg_r=("realized_r", "mean"),
                        sl_rate=("outcome", lambda s: float((s == "SL").mean())),
                        tp1_rate=("outcome", lambda s: float((s == "TP1").mean())),
                        tp2_rate=("outcome", lambda s: float((s == "TP2").mean())),
                        none_rate=("outcome", lambda s: float((s == "NONE").mean())),
                    )
                    .reset_index()
                )
                e1_kd3["_kd3_ok"] = e1_kd3["_kd3_ok"].astype(int)
                e1_kd3["key"] = np.where(e1_kd3["_kd3_ok"] == 1, "KD3_OK", "KD3_NO")
                e1_kd3 = e1_kd3.drop(columns=["_kd3_ok"])
                e1_kd3.insert(0, "group", "E1_KD3_SPLIT")
            e1_zrf = pd.DataFrame()
            if ("zrf_m_bull_div" in e1_df.columns) and ("zrf_m_bear_div" in e1_df.columns) and ("side" in e1_df.columns):
                side_s = e1_df.get("side", "").astype(str).str.upper()
                bull = pd.to_numeric(e1_df.get("zrf_m_bull_div", np.nan), errors="coerce")
                bear = pd.to_numeric(e1_df.get("zrf_m_bear_div", np.nan), errors="coerce")
                e1_df["_zrf_div_ok"] = np.where(side_s == "SHORT", bear, bull)
                e1_df["_zrf_div_ok"] = pd.to_numeric(e1_df["_zrf_div_ok"], errors="coerce")
                e1_zrf = (
                    e1_df[e1_df["_zrf_div_ok"].notna()]
                    .groupby(["_zrf_div_ok"], observed=True)
                    .agg(
                        n=("realized_r", "size"),
                        win_rate=("is_win", "mean"),
                        avg_r=("realized_r", "mean"),
                        sl_rate=("outcome", lambda s: float((s == "SL").mean())),
                        tp1_rate=("outcome", lambda s: float((s == "TP1").mean())),
                        tp2_rate=("outcome", lambda s: float((s == "TP2").mean())),
                        none_rate=("outcome", lambda s: float((s == "NONE").mean())),
                    )
                    .reset_index()
                )
                e1_zrf["_zrf_div_ok"] = e1_zrf["_zrf_div_ok"].astype(int)
                e1_zrf["key"] = np.where(e1_zrf["_zrf_div_ok"] == 1, "ZRF_DIV_OK", "ZRF_DIV_NO")
                e1_zrf = e1_zrf.drop(columns=["_zrf_div_ok"])
                e1_zrf.insert(0, "group", "E1_ZRF_MACD_DIV_SPLIT")
            e1_adx = pd.DataFrame()
            if "adx14" in e1_df.columns:
                adx = pd.to_numeric(e1_df.get("adx14", np.nan), errors="coerce")
                e1_df["_adx14"] = adx
                e1_df["_adx_bucket"] = np.where(
                    e1_df["_adx14"].notna() & (e1_df["_adx14"] < 20.0),
                    "ADX_LT_20",
                    np.where(e1_df["_adx14"].notna() & (e1_df["_adx14"] < 25.0), "ADX_20_25", "ADX_GE_25"),
                )
                e1_adx = (
                    e1_df[e1_df["_adx14"].notna()]
                    .groupby(["_adx_bucket"], observed=True)
                    .agg(
                        n=("realized_r", "size"),
                        win_rate=("is_win", "mean"),
                        avg_r=("realized_r", "mean"),
                        sl_rate=("outcome", lambda s: float((s == "SL").mean())),
                        tp1_rate=("outcome", lambda s: float((s == "TP1").mean())),
                        tp2_rate=("outcome", lambda s: float((s == "TP2").mean())),
                        none_rate=("outcome", lambda s: float((s == "NONE").mean())),
                        adx_median=("_adx14", "median"),
                    )
                    .reset_index()
                    .rename(columns={"_adx_bucket": "key"})
                )
                e1_adx.insert(0, "group", "E1_ADX14_BUCKETS")
            e1_cci = pd.DataFrame()
            if "cci144" in e1_df.columns:
                cci = pd.to_numeric(e1_df.get("cci144", np.nan), errors="coerce")
                e1_df["_cci144"] = cci
                e1_df["_cci_bucket"] = np.where(
                    e1_df["_cci144"].notna() & (e1_df["_cci144"] < -144.0),
                    "CCI_LT_M144",
                    np.where(e1_df["_cci144"].notna() & (e1_df["_cci144"] > 144.0), "CCI_GT_P144", "CCI_MID"),
                )
                e1_cci = (
                    e1_df[e1_df["_cci144"].notna()]
                    .groupby(["_cci_bucket"], observed=True)
                    .agg(
                        n=("realized_r", "size"),
                        win_rate=("is_win", "mean"),
                        avg_r=("realized_r", "mean"),
                        sl_rate=("outcome", lambda s: float((s == "SL").mean())),
                        tp1_rate=("outcome", lambda s: float((s == "TP1").mean())),
                        tp2_rate=("outcome", lambda s: float((s == "TP2").mean())),
                        none_rate=("outcome", lambda s: float((s == "NONE").mean())),
                        cci_median=("_cci144", "median"),
                    )
                    .reset_index()
                    .rename(columns={"_cci_bucket": "key"})
                )
                e1_cci.insert(0, "group", "E1_CCI144_BUCKETS")
            e1_sym = (
                e1_df.groupby(["symbol"], observed=True)
                .agg(
                    n=("realized_r", "size"),
                    win_rate=("is_win", "mean"),
                    avg_r=("realized_r", "mean"),
                    sl_rate=("outcome", lambda s: float((s == "SL").mean())),
                    tp1_rate=("outcome", lambda s: float((s == "TP1").mean())),
                    tp2_rate=("outcome", lambda s: float((s == "TP2").mean())),
                    none_rate=("outcome", lambda s: float((s == "NONE").mean())),
                )
                .reset_index()
                .rename(columns={"symbol": "key"})
                .sort_values(["n", "avg_r"], ascending=[False, False])
            )
            e1_sym.insert(0, "group", "E1_BY_SYMBOL")
            parts = [e1_base, e1_atr]
            if not e1_kd3.empty:
                parts.append(e1_kd3)
            if not e1_zrf.empty:
                parts.append(e1_zrf)
            if not e1_adx.empty:
                parts.append(e1_adx)
            if not e1_cci.empty:
                parts.append(e1_cci)
            parts.append(e1_sym)
            e1_diag = pd.concat(parts, axis=0, ignore_index=True)
            _write_csv(out_dir / "paper_replay_e1_diag.csv", e1_diag)
            print(f"[PAPER][E1DIAG] e1_n={len(e1_df)} e1_avg_r={float(e1_df['realized_r'].mean()):.6f} e1_sl_rate={float((e1_df['outcome']=='SL').mean()):.6f}")
            if not e1_atr.empty and ("ATR_LOW" in set(e1_atr["key"])) and ("ATR_HIGH" in set(e1_atr["key"])):
                low = e1_atr[e1_atr["key"] == "ATR_LOW"].iloc[0]
                high = e1_atr[e1_atr["key"] == "ATR_HIGH"].iloc[0]
                print(f"[PAPER][E1DIAG] atr_median={med:.6f} low_avg_r={float(low['avg_r']):.6f} high_avg_r={float(high['avg_r']):.6f}")
            if not e1_kd3.empty and ("KD3_OK" in set(e1_kd3["key"])) and ("KD3_NO" in set(e1_kd3["key"])):
                ok = e1_kd3[e1_kd3["key"] == "KD3_OK"].iloc[0]
                no = e1_kd3[e1_kd3["key"] == "KD3_NO"].iloc[0]
                print(f"[PAPER][E1DIAG] kd3_ok_avg_r={float(ok['avg_r']):.6f} kd3_no_avg_r={float(no['avg_r']):.6f}")
            if not e1_zrf.empty and ("ZRF_DIV_OK" in set(e1_zrf["key"])) and ("ZRF_DIV_NO" in set(e1_zrf["key"])):
                ok = e1_zrf[e1_zrf["key"] == "ZRF_DIV_OK"].iloc[0]
                no = e1_zrf[e1_zrf["key"] == "ZRF_DIV_NO"].iloc[0]
                print(f"[PAPER][E1DIAG] zrf_div_ok_avg_r={float(ok['avg_r']):.6f} zrf_div_no_avg_r={float(no['avg_r']):.6f}")
            if not e1_adx.empty:
                adx_med = float(pd.to_numeric(e1_df.get("adx14", np.nan), errors="coerce").median())
                print(f"[PAPER][E1DIAG] adx14_median={adx_med:.6f}")
            if not e1_cci.empty:
                cci_med = float(pd.to_numeric(e1_df.get("cci144", np.nan), errors="coerce").median())
                print(f"[PAPER][E1DIAG] cci144_median={cci_med:.6f}")

    def _pick_col(df0: pd.DataFrame, names: List[str]) -> Optional[str]:
        for n in names:
            if n in df0.columns:
                return n
        return None

    def _bobby_filter_candidates(df0: pd.DataFrame) -> pd.DataFrame:
        if df0 is None or df0.empty:
            return pd.DataFrame()
        df0 = df0.copy()
        df0["signal"] = df0.get("signal", "").astype(str).str.upper()
        df0["realized_r"] = pd.to_numeric(df0.get("realized_r", np.nan), errors="coerce")
        df0["is_win"] = pd.to_numeric(df0.get("realized_r", np.nan), errors="coerce") > 0

        col_ma13 = _pick_col(df0, ["ma_fast_13", "jg_ma13"])
        col_ma55 = _pick_col(df0, ["ma_slow_55", "jg_ma55"])
        col_bar_red = _pick_col(df0, ["bar_color_red", "jg_bar_red"])
        col_bar_yellow = _pick_col(df0, ["bar_color_yellow", "jg_bar_yellow"])
        col_chase = _pick_col(df0, ["chase_dist_atr"])
        if (col_ma13 is None) or (col_ma55 is None) or (col_bar_red is None) or (col_bar_yellow is None) or (col_chase is None):
            return pd.DataFrame()

        ma13 = pd.to_numeric(df0.get(col_ma13, np.nan), errors="coerce")
        ma55 = pd.to_numeric(df0.get(col_ma55, np.nan), errors="coerce")
        chase = pd.to_numeric(df0.get(col_chase, np.nan), errors="coerce")
        bar_red = pd.to_numeric(df0.get(col_bar_red, np.nan), errors="coerce")
        bar_yellow = pd.to_numeric(df0.get(col_bar_yellow, np.nan), errors="coerce")
        side_s = df0.get("side", "").astype(str).str.upper()

        trend_long = ma13.notna() & ma55.notna() & (ma13 > ma55)
        trend_short = ma13.notna() & ma55.notna() & (ma13 < ma55)
        bar_red_ok = bar_red.notna() & (bar_red != 0)
        bar_yellow_ok = bar_yellow.notna() & (bar_yellow != 0)

        df0["_trend_ok"] = ((side_s == "LONG") & trend_long) | ((side_s == "SHORT") & trend_short)
        df0["_bar_ok"] = ((side_s == "LONG") & bar_red_ok) | ((side_s == "SHORT") & bar_yellow_ok)
        df0["_chase15"] = chase.notna() & (chase <= 1.5)

        def _row(df_sub: pd.DataFrame, name: str) -> Dict[str, object]:
            df_sub = df_sub.copy()
            df_sub["realized_r"] = pd.to_numeric(df_sub.get("realized_r", np.nan), errors="coerce")
            df_sub["is_win"] = pd.to_numeric(df_sub.get("realized_r", np.nan), errors="coerce") > 0
            return {
                "case": str(name),
                "n": float(len(df_sub)),
                "win_rate": float(df_sub["is_win"].mean()) if len(df_sub) else np.nan,
                "avg_r": float(df_sub["realized_r"].mean()) if len(df_sub) else np.nan,
                "sl_rate": float((df_sub.get("outcome", "") == "SL").mean()) if len(df_sub) else np.nan,
            }

        e1 = df0[df0["signal"] == "E1"].copy()
        e2 = df0[df0["signal"] == "E2"].copy()
        rows: List[Dict[str, object]] = [
            _row(e1, "E1:ALL"),
            _row(df0[(df0["signal"] == "E1") & df0["_trend_ok"] & df0["_bar_ok"]], "E1:F1(trend_ok & bar_ok)"),
            _row(e2, "E2:ALL"),
            _row(df0[(df0["signal"] == "E2") & df0["_chase15"]], "E2:chase<=1.5"),
            _row(df0[(df0["signal"] == "E2") & df0["_chase15"] & df0["_trend_ok"]], "E2:F2(chase<=1.5 & trend_ok)"),
            _row(df0[(df0["signal"] == "E2") & df0["_chase15"] & df0["_trend_ok"] & df0["_bar_ok"]], "E2:F3(chase<=1.5 & trend_ok & bar_ok)"),
        ]
        return pd.DataFrame(rows)

    cand = _bobby_filter_candidates(out_df)
    if not cand.empty:
        _write_csv(out_dir / "paper_replay_bobby_filter_candidates.csv", cand)
        with pd.option_context("display.max_rows", 200, "display.width", 200):
            print(cand.to_string(index=False))
    _write_csv(out_dir / "paper_replay_summary.csv", summ2)
    with pd.option_context("display.max_rows", 200, "display.width", 200):
        print(summ2.to_string(index=False))


def _csv_index(csv_dir: Path) -> List[Path]:
    if not csv_dir.exists():
        return []
    return list(csv_dir.rglob("*.csv"))


def _resolve_csv_symbol(sym: str) -> str:
    s = str(sym).strip().upper()
    m = {
        "GER40": "GER30",
        "DE40": "GER30",
        "DE30": "GER30",
        "DAX": "GER30",
        "DAX30": "GER30",
        "DAX40": "GER30",
        "NAS100": "NAS100",
        "USTEC": "NAS100",
        "US100": "NAS100",
        "US500": "US500",
        "SPX500": "US500",
        "USA500": "US500",
        "US30": "US30",
        "DJ30": "US30",
        "DJI": "US30",
        "XAU": "XAUUSD",
    }
    return m.get(s, s)


def _detect_csv_tz(csv_path: Path) -> str:
    try:
        with open(csv_path, "rb") as f:
            h = f.readline().decode("utf-8", errors="ignore").strip().lower()
    except Exception:
        h = ""
    if "(eet)" in h or "time (eet)" in h:
        return "Europe/Bucharest"
    return "UTC"


def _vendor_code_for_symbol(sym: str) -> List[str]:
    s = _resolve_csv_symbol(sym)
    m = {
        "US500": ["USA500IDXUSD"],
        "NAS100": ["USATECHIDXUSD"],
        "US30": ["USA30IDXUSD"],
        "GER30": ["DEUIDXEUR"],
        "XAUUSD": ["XAUUSD"],
    }
    return m.get(s, [s])


def _find_vendor_csv(sym: str, csv_files: List[Path]) -> Path:
    codes = [c.strip().upper() for c in _vendor_code_for_symbol(sym) if str(c).strip()]
    if not codes:
        raise FileNotFoundError(f"no vendor code mapping for: {sym}")
    cand: List[Path] = []
    for p in csv_files:
        name_u = p.name.upper()
        if any(code in name_u for code in codes):
            cand.append(p)
    if not cand:
        raise FileNotFoundError(f"vendor csv not found for {sym} under csv_dir")

    if _resolve_csv_symbol(sym) == "XAUUSD":
        c1 = [p for p in cand if "HOURLY" in p.name.upper()]
        if c1:
            return sorted(c1, key=lambda x: len(str(x)))[0]
    return sorted(cand, key=lambda x: len(str(x)))[0]


def _load_vendor_1h(sym: str, csv_files: List[Path]) -> pd.DataFrame:
    src = _find_vendor_csv(sym, csv_files)
    tz = _detect_csv_tz(src)
    df = load_ohlcv_1h(src, tz=tz)
    try:
        df = df.tz_convert("UTC")
    except Exception:
        pass
    df1h = resample_ohlcv(df, "1H")
    df1h = df1h.sort_index()
    df1h["tick_volume"] = df1h.get("volume", 0.0)
    return df1h


def _paper_scan_csv(args: Dict[str, Any], p: Params) -> Path:
    dt_from_s = str(args.get("paper_from") or "").strip()
    dt_to_s = str(args.get("paper_to") or "").strip()
    if not dt_from_s or not dt_to_s:
        raise ValueError("paper-scan-csv requires --paper-from and --paper-to")
    dt_from = pd.to_datetime(dt_from_s, utc=True, errors="raise")
    dt_to = pd.to_datetime(dt_to_s, utc=True, errors="raise")
    if dt_to <= dt_from:
        raise ValueError("paper-to must be after paper-from")

    syms_raw = str(args.get("paper_symbols") or "").strip()
    if syms_raw:
        syms = [x.strip().upper() for x in syms_raw.split(",") if x.strip()]
        pool_df = None
    else:
        pool = str(args.get("pool") or "core").strip().lower()
        if pool in {"core", "observe", "exclude"}:
            dfp = _read_deploy_pool_df(pool)
            syms = [str(x).upper() for x in dfp["symbol"].tolist()] if dfp is not None and "symbol" in dfp.columns else []
            pool_df = dfp
        elif pool in {"all", "*"}:
            dfc = _read_deploy_pool_df("core")
            dfo = _read_deploy_pool_df("observe")
            syms = []
            if dfc is not None and "symbol" in dfc.columns:
                syms += [str(x).upper() for x in dfc["symbol"].tolist()]
            if dfo is not None and "symbol" in dfo.columns:
                syms += [str(x).upper() for x in dfo["symbol"].tolist()]
            syms = list(dict.fromkeys(syms))
            pool_df = _merge_pool_dfs(["core", "observe"])
        else:
            raise ValueError("paper-scan-csv: unknown pool; use --paper-symbols or --pool core|observe|exclude|all")
    if not syms:
        raise ValueError("paper-scan-csv: empty symbols (use --paper-symbols or ensure deploy pool has symbols)")

    base = Path(str(args.get("log_dir") or DEFAULT_LOG_DIR))
    out_dir = base / dt_to.to_pydatetime().strftime("%Y-%m-%d")
    private_names = bool(int(args.get("private_names", 0) or 0))
    ss_map = _symbol_settings_map(pool_df)

    csv_dir = Path(str(args.get("csv_dir") or "")).resolve()
    csv_files = _csv_index(csv_dir)
    if not csv_files:
        raise FileNotFoundError(f"csv_dir has no .csv files: {str(csv_dir)}")

    warm_h1 = timedelta(days=30)
    warm_h4 = timedelta(days=120)
    warm_d1 = timedelta(days=500)

    rows: List[Dict[str, object]] = []
    include_bobby_signals = bool(int(args.get("paper_bobby_signals") or 0) != 0)
    bobby_sl_atr = float(args.get("paper_bobby_sl_atr") or 1.0)
    if not (bobby_sl_atr > 0):
        bobby_sl_atr = 1.0
    for sym0 in syms:
        p_sym = _params_for_symbol(p, ss_map.get(str(sym0).strip().upper()))
        sym = _resolve_csv_symbol(sym0)
        df1h = _load_vendor_1h(sym, csv_files)
        warm0 = (dt_from - warm_d1).to_pydatetime()
        warm1 = (dt_to + timedelta(days=2)).to_pydatetime()
        df_all = df1h[(df1h.index >= warm0) & (df1h.index <= warm1)].copy()
        df1 = df_all[(df_all.index >= dt_from.to_pydatetime()) & (df_all.index <= dt_to.to_pydatetime())].copy()
        if df1.empty:
            continue
        df4 = df_all[(df_all.index >= (dt_from - warm_h4).to_pydatetime()) & (df_all.index <= (dt_to + timedelta(days=5)).to_pydatetime())].copy()
        dfd = df_all[(df_all.index >= (dt_from - warm_d1).to_pydatetime()) & (df_all.index <= (dt_to + timedelta(days=10)).to_pydatetime())].copy()
        df4 = resample_ohlcv(df4, "4H")
        dfd = resample_ohlcv(dfd, "1D")
        df4["tick_volume"] = df4.get("volume", 0.0)
        dfd["tick_volume"] = dfd.get("volume", 0.0)

        df1n = df1.copy()
        try:
            df1n.index = pd.to_datetime(df1n.index, utc=True).tz_localize(None)
        except Exception:
            df1n.index = pd.to_datetime(df1n.index, errors="coerce")
        df4n = df4.copy()
        dfdn = dfd.copy()
        try:
            df4n.index = pd.to_datetime(df4n.index, utc=True).tz_localize(None)
        except Exception:
            df4n.index = pd.to_datetime(df4n.index, errors="coerce")
        try:
            dfdn.index = pd.to_datetime(dfdn.index, utc=True).tz_localize(None)
        except Exception:
            dfdn.index = pd.to_datetime(dfdn.index, errors="coerce")

        sigs = _scan_entry_signals_from_dfs(
            sym,
            df1=df1n,
            df4=df4n,
            dfd=dfdn,
            p=p_sym,
            include_bobby_signals=include_bobby_signals,
            bobby_sl_atr=bobby_sl_atr,
        )
        for e in sigs:
            try:
                t = pd.to_datetime(str(e.ts), errors="coerce")
            except Exception:
                t = pd.NaT
            if pd.isna(t):
                continue
            rows.append(
                _apply_private_names(
                    {
                        "ts_utc": _now_utc_iso(),
                        "sig_ts": str(e.ts),
                        "symbol": e.symbol,
                        "side": e.side,
                        "signal": e.signal,
                        "entry": float(e.entry),
                        "stop": float(e.stop),
                        "atr": float(e.atr),
                        "entry_score": float(e.entry_score),
                        "ema21_1h": float(e.ema21_1h),
                        "breakout_level": float(e.breakout_level) if not pd.isna(e.breakout_level) else np.nan,
                        "touch_delta": int(e.touch_delta),
                        "strong": bool(e.strong),
                        "kd_w1_long": bool(e.kd_w1_long),
                        "kd_w1_short": bool(e.kd_w1_short),
                        "kd_3line_long": bool(e.kd_3line_long),
                        "kd_3line_short": bool(e.kd_3line_short),
                        "cci144": float(e.cci144) if not pd.isna(e.cci144) else np.nan,
                        "adx14": float(e.adx14) if not pd.isna(e.adx14) else np.nan,
                        "chase_dist_atr": float(e.chase_dist_atr) if not pd.isna(e.chase_dist_atr) else np.nan,
                        "score_filter_th": float(e.score_filter_th) if not pd.isna(e.score_filter_th) else np.nan,
                        "score_filter_pass": bool(e.score_filter_pass),
                        "entry_score_gate_max": float(e.entry_score_gate_max) if not pd.isna(e.entry_score_gate_max) else np.nan,
                        "entry_score_gate_action": str(e.entry_score_gate_action),
                        "entry_score_gate_scope": str(e.entry_score_gate_scope),
                        "entry_score_gate_hit": bool(e.entry_score_gate_hit),
                        "entry_score_gate_blocked": bool(e.entry_score_gate_blocked),
                        "tick_volume": float(e.tick_volume) if not pd.isna(e.tick_volume) else np.nan,
                        "vol_sma20": float(e.vol_sma20) if not pd.isna(e.vol_sma20) else np.nan,
                        "vol_ratio": float(e.vol_ratio) if not pd.isna(e.vol_ratio) else np.nan,
                        "vol_pct": float(e.vol_pct) if not pd.isna(e.vol_pct) else np.nan,
                        "atr_sma50": float(e.atr_sma50) if not pd.isna(e.atr_sma50) else np.nan,
                        "atr_rel": float(e.atr_rel) if not pd.isna(e.atr_rel) else np.nan,
                        "atr_pct": float(e.atr_pct) if not pd.isna(e.atr_pct) else np.nan,
                        "spread_rel": float(e.spread_rel) if not pd.isna(e.spread_rel) else np.nan,
                        "liquidity_risk": bool(e.liquidity_risk),
                        "vol_risk_vol_ratio_max": float(e.vol_risk_vol_ratio_max) if not pd.isna(e.vol_risk_vol_ratio_max) else np.nan,
                        "vol_risk_vol_pct_max": float(e.vol_risk_vol_pct_max) if not pd.isna(e.vol_risk_vol_pct_max) else np.nan,
                        "vol_risk_action": str(e.vol_risk_action),
                        "vol_risk_blocked": bool(e.vol_risk_blocked),
                        "sr_support": float(e.sr_support) if not pd.isna(e.sr_support) else np.nan,
                        "sr_resistance": float(e.sr_resistance) if not pd.isna(e.sr_resistance) else np.nan,
                        "sr_support_dist_atr": float(e.sr_support_dist_atr) if not pd.isna(e.sr_support_dist_atr) else np.nan,
                        "sr_resistance_dist_atr": float(e.sr_resistance_dist_atr) if not pd.isna(e.sr_resistance_dist_atr) else np.nan,
                        "sr_support_touches": int(e.sr_support_touches),
                        "sr_resistance_touches": int(e.sr_resistance_touches),
                        "jg_macd_up": bool(e.jg_macd_up),
                        "jg_macd_down": bool(e.jg_macd_down),
                        "jg_sma175": float(e.jg_sma175) if not pd.isna(e.jg_sma175) else np.nan,
                        "jg_j": float(e.jg_j) if not pd.isna(e.jg_j) else np.nan,
                        "jg_long": bool(e.jg_long),
                        "jg_short": bool(e.jg_short),
                        "jg_ma13": float(e.jg_ma13) if not pd.isna(e.jg_ma13) else np.nan,
                        "jg_ma55": float(e.jg_ma55) if not pd.isna(e.jg_ma55) else np.nan,
                        "jg_ema20": float(e.jg_ema20) if not pd.isna(e.jg_ema20) else np.nan,
                        "jg_ema27": float(e.jg_ema27) if not pd.isna(e.jg_ema27) else np.nan,
                        "jg_ema29": float(e.jg_ema29) if not pd.isna(e.jg_ema29) else np.nan,
                        "jg_ema32": float(e.jg_ema32) if not pd.isna(e.jg_ema32) else np.nan,
                        "jg_ema36": float(e.jg_ema36) if not pd.isna(e.jg_ema36) else np.nan,
                        "jg_pivot_mid": float(e.jg_pivot_mid) if not pd.isna(e.jg_pivot_mid) else np.nan,
                        "jg_b3": float(e.jg_b3) if not pd.isna(e.jg_b3) else np.nan,
                        "jg_s3": float(e.jg_s3) if not pd.isna(e.jg_s3) else np.nan,
                        "jg_b5": float(e.jg_b5) if not pd.isna(e.jg_b5) else np.nan,
                        "jg_s5": float(e.jg_s5) if not pd.isna(e.jg_s5) else np.nan,
                        "jg_var2": float(e.jg_var2) if not pd.isna(e.jg_var2) else np.nan,
                        "jg_var3": float(e.jg_var3) if not pd.isna(e.jg_var3) else np.nan,
                        "jg_var3_ma6": float(e.jg_var3_ma6) if not pd.isna(e.jg_var3_ma6) else np.nan,
                        "jg_bar_yellow": bool(e.jg_bar_yellow),
                        "jg_bar_red": bool(e.jg_bar_red),
                        "jg_macd": float(e.jg_macd) if not pd.isna(e.jg_macd) else np.nan,
                        "jg_buy": bool(e.jg_buy),
                        "jg_sell": bool(e.jg_sell),
                        "jg_gold": bool(e.jg_gold),
                        "jg_ma160": float(e.jg_ma160) if not pd.isna(e.jg_ma160) else np.nan,
                        "jg_ma120": float(e.jg_ma120) if not pd.isna(e.jg_ma120) else np.nan,
                        "jg_ma60": float(e.jg_ma60) if not pd.isna(e.jg_ma60) else np.nan,
                        "jg_ma25": float(e.jg_ma25) if not pd.isna(e.jg_ma25) else np.nan,
                        "jg_flip_to_yellow": bool(e.jg_flip_to_yellow),
                        "jg_flip_to_red": bool(e.jg_flip_to_red),
                        "jg_wick_touch_ma13": bool(e.jg_wick_touch_ma13),
                        "jg_wick_touch_ma55": bool(e.jg_wick_touch_ma55),
                        "jg_wick_touch_ema27": bool(e.jg_wick_touch_ema27),
                        "jg_wick_touch_ema29": bool(e.jg_wick_touch_ema29),
                        "jg_wick_touch_ema32": bool(e.jg_wick_touch_ema32),
                        "jg_wick_touch_ema36": bool(e.jg_wick_touch_ema36),
                        "jg_close_breakdown_ma13": bool(e.jg_close_breakdown_ma13),
                        "jg_close_breakup_ma13": bool(e.jg_close_breakup_ma13),
                        "jg_close_breakdown_ma55": bool(e.jg_close_breakdown_ma55),
                        "jg_close_breakup_ma55": bool(e.jg_close_breakup_ma55),
                        "jg_cross_ma13_ema27_up": bool(e.jg_cross_ma13_ema27_up),
                        "jg_cross_ma13_ema27_down": bool(e.jg_cross_ma13_ema27_down),
                        "jg_cross_ma13_ema29_up": bool(e.jg_cross_ma13_ema29_up),
                        "jg_cross_ma13_ema29_down": bool(e.jg_cross_ma13_ema29_down),
                        "jg_cross_ma13_ema32_up": bool(e.jg_cross_ma13_ema32_up),
                        "jg_cross_ma13_ema32_down": bool(e.jg_cross_ma13_ema32_down),
                        "jg_cross_ma13_ema36_up": bool(e.jg_cross_ma13_ema36_up),
                        "jg_cross_ma13_ema36_down": bool(e.jg_cross_ma13_ema36_down),
                        "jg_after_cross_ma13_ema27_up_j_lt80": bool(e.jg_after_cross_ma13_ema27_up_j_lt80),
                        "jg_after_cross_ma13_ema27_down_j_gt20": bool(e.jg_after_cross_ma13_ema27_down_j_gt20),
                        "jg_dist_b3_atr": float(e.jg_dist_b3_atr) if not pd.isna(e.jg_dist_b3_atr) else np.nan,
                        "jg_dist_s3_atr": float(e.jg_dist_s3_atr) if not pd.isna(e.jg_dist_s3_atr) else np.nan,
                        "jg_dist_pivot_atr": float(e.jg_dist_pivot_atr) if not pd.isna(e.jg_dist_pivot_atr) else np.nan,
                        "jg_red_streak": int(e.jg_red_streak),
                        "jg_yellow_streak": int(e.jg_yellow_streak),
                        "ma13_ma55_gap_atr": (
                            float(abs(float(e.jg_ma13) - float(e.jg_ma55)) / float(e.atr))
                            if (not pd.isna(e.atr) and float(e.atr) > 0 and not pd.isna(e.jg_ma13) and not pd.isna(e.jg_ma55))
                            else np.nan
                        ),
                        "pat_flydragon_v1": (not pd.isna(e.jg_ma13) and not pd.isna(e.jg_ma55) and float(e.jg_ma13) > float(e.jg_ma55))
                        and bool(e.jg_wick_touch_ma13)
                        and bool(e.jg_buy),
                        "pat_flydragon_v2": (not pd.isna(e.jg_ma13) and not pd.isna(e.jg_ma55) and float(e.jg_ma13) > float(e.jg_ma55))
                        and (bool(e.jg_wick_touch_ma13) or bool(e.jg_wick_touch_ema27))
                        and bool(e.jg_buy)
                        and bool(e.jg_flip_to_red),
                        "pat_flydragon_v3_gold": (not pd.isna(e.jg_ma13) and not pd.isna(e.jg_ma55) and float(e.jg_ma13) > float(e.jg_ma55)) and bool(e.jg_gold),
                        "pat_cloudcover_momo_v1": (not pd.isna(e.jg_ma13) and not pd.isna(e.jg_ma55) and float(e.jg_ma13) > float(e.jg_ma55))
                        and bool(e.jg_flip_to_yellow)
                        and bool(e.jg_close_breakdown_ma13),
                        "pat_boundary_long_v1": (
                            (not pd.isna(e.atr) and float(e.atr) > 0 and not pd.isna(e.jg_ma13) and not pd.isna(e.jg_ma55))
                            and (float(abs(float(e.jg_ma13) - float(e.jg_ma55)) / float(e.atr)) <= 0.5)
                            and bool(e.jg_buy)
                        ),
                        "pat_boundary_short_v1": (
                            (not pd.isna(e.atr) and float(e.atr) > 0 and not pd.isna(e.jg_ma13) and not pd.isna(e.jg_ma55))
                            and (float(abs(float(e.jg_ma13) - float(e.jg_ma55)) / float(e.atr)) <= 0.5)
                            and bool(e.jg_sell)
                        ),
                        "pat_sunrise_v1": bool(e.jg_flip_to_red) and bool(e.jg_buy),
                        "pat_sunset_v1": bool(e.jg_flip_to_yellow) and bool(e.jg_sell),
                    },
                    private_names=private_names,
                )
            )
    out_df = pd.DataFrame(rows)
    _write_csv(out_dir / "entries_suggested_v7.csv", out_df)
    return out_dir


def _paper_replay_csv(args: Dict[str, Any]) -> None:
    src = str(args.get("paper_dir") or "").strip()
    if src:
        src_dir = Path(src)
    else:
        src_dir = _log_dir_for_run(args)
    private_names = bool(int(args.get("private_names", 0) or 0))
    if not src_dir.exists():
        raise FileNotFoundError(f"paper_dir not found: {str(src_dir)}")

    entry_files: List[Path] = []
    direct6 = src_dir / "entries_suggested_v7.csv"
    direct5 = src_dir / "entries_suggested_v6.csv"
    direct4 = src_dir / "entries_suggested_v5.csv"
    direct3 = src_dir / "entries_suggested_v4.csv"
    direct2 = src_dir / "entries_suggested_v3.csv"
    direct1 = src_dir / "entries_suggested_v2.csv"
    direct0 = src_dir / "entries_suggested.csv"
    entry_files = []
    if direct6.exists():
        entry_files = [direct6]
    elif direct5.exists():
        entry_files = [direct5]
    elif direct4.exists():
        entry_files = [direct4]
    elif direct3.exists():
        entry_files = [direct3]
    elif direct2.exists():
        entry_files = [direct2]
    elif direct1.exists():
        entry_files = [direct1]
    elif direct0.exists():
        entry_files = [direct0]
        entry_files = sorted(
            list(src_dir.rglob("entries_suggested_v7.csv"))
            + list(src_dir.rglob("entries_suggested_v6.csv"))
            + list(src_dir.rglob("entries_suggested_v5.csv"))
            + list(src_dir.rglob("entries_suggested_v4.csv"))
            + list(src_dir.rglob("entries_suggested_v3.csv"))
            + list(src_dir.rglob("entries_suggested_v2.csv"))
            + list(src_dir.rglob("entries_suggested.csv"))
        )
    if not entry_files:
        raise FileNotFoundError(f"no entries_suggested.csv under: {str(src_dir)}")

    dfs: List[pd.DataFrame] = []
    for f in entry_files:
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        if df is not None and not df.empty:
            df = df.copy()
            df["__src"] = str(f)
            dfs.append(df)
    if not dfs:
        raise RuntimeError(f"entries files unreadable or empty under: {str(src_dir)}")

    raw = pd.concat(dfs, axis=0, ignore_index=True)
    if "sig_ts" not in raw.columns:
        raw["sig_ts"] = raw.get("ts_utc", "")
    raw["sig_ts"] = pd.to_datetime(raw["sig_ts"], errors="coerce", utc=True)
    raw["ts_utc"] = pd.to_datetime(raw.get("ts_utc", ""), errors="coerce", utc=True)
    raw = raw.dropna(subset=["sig_ts"])
    for c in ["entry", "stop", "atr", "entry_score"]:
        if c in raw.columns:
            raw[c] = pd.to_numeric(raw[c], errors="coerce")
    raw["symbol"] = raw.get("symbol", "").astype(str).str.upper()
    raw["side"] = raw.get("side", "").astype(str).str.upper()
    raw["signal"] = raw.get("signal", "").astype(str).str.upper()

    raw = raw.sort_values(["ts_utc"], ascending=[True]).reset_index(drop=True)
    raw = raw.drop_duplicates(subset=["symbol", "sig_ts", "side", "signal", "entry", "stop"], keep="last").reset_index(drop=True)
    raw = raw[(raw["symbol"] != "") & (raw["side"].isin(["LONG", "SHORT"])) & (raw["entry"].notna()) & (raw["stop"].notna())]
    if raw.empty:
        raise RuntimeError("no valid rows after dedup/filter")

    lookahead = max(1, int(args.get("paper_lookahead_bars") or 48))
    tp1_r = float(args.get("paper_tp1_r") or 1.0)
    tp2_r = float(args.get("paper_tp2_r") or 2.0)
    bar_rule = str(args.get("paper_bar_rule") or "sl_first").strip().lower()
    if bar_rule not in {"sl_first", "tp_first"}:
        raise ValueError(f"unknown paper_bar_rule: {bar_rule}")
    e2_chase_max_raw = args.get("paper_e2_chase_max", None)
    try:
        e2_chase_max = float(e2_chase_max_raw) if e2_chase_max_raw is not None and str(e2_chase_max_raw).strip() != "" else None
    except Exception:
        e2_chase_max = None
    if e2_chase_max is not None and not (float(e2_chase_max) > 0):
        e2_chase_max = None

    raw["_symbol_res"] = raw["symbol"].astype(str).map(lambda s: _resolve_csv_symbol(s))
    csv_dir = Path(str(args.get("csv_dir") or "")).resolve()
    csv_files = _csv_index(csv_dir)
    if not csv_files:
        raise FileNotFoundError(f"csv_dir has no .csv files: {str(csv_dir)}")
    sym_cache: Dict[str, pd.DataFrame] = {}
    for sym_res, g in raw.groupby("_symbol_res", observed=True):
        sym_res = str(sym_res).strip()
        if not sym_res:
            continue
        g_ts = pd.to_datetime(g["sig_ts"], errors="coerce", utc=True).dropna()
        if g_ts.empty:
            continue
        dt_min = g_ts.min()
        dt_max = g_ts.max()
        dt0 = dt_min - timedelta(hours=520)
        dt1 = dt_max + timedelta(hours=int(lookahead) + 10)
        df1h = _load_vendor_1h(sym_res, csv_files)
        df1h = df1h[(df1h.index >= dt0.to_pydatetime()) & (df1h.index <= dt1.to_pydatetime())].copy()
        if df1h is None or df1h.empty:
            continue
        df_sym = df1h.copy()
        df_sym["ts"] = pd.to_datetime(df_sym.index, utc=True).tz_localize(None)
        df_sym = df_sym.sort_values("ts").reset_index(drop=True)
        z = _zrf_macd_from_close(df_sym["close"])
        a = _adx_from_ohlc(df_sym["high"], df_sym["low"], df_sym["close"], 14)
        cci144 = _cci_from_ohlc(df_sym["high"], df_sym["low"], df_sym["close"], 144)
        df_sym = pd.concat([df_sym, z.reset_index(drop=True), a.reset_index(drop=True)], axis=1)
        df_sym["cci144"] = cci144.reset_index(drop=True)
        sym_cache[str(sym_res)] = df_sym

    rows: List[Dict[str, object]] = []
    for r in raw.itertuples(index=False):
        sym = str(getattr(r, "_symbol_res", getattr(r, "symbol", "")))
        sym = _resolve_csv_symbol(sym)
        side = str(getattr(r, "side"))
        sig_ts = getattr(r, "sig_ts")
        entry = float(getattr(r, "entry"))
        stop = float(getattr(r, "stop"))
        signal = str(getattr(r, "signal"))
        score = float(getattr(r, "entry_score")) if hasattr(r, "entry_score") and not pd.isna(getattr(r, "entry_score")) else np.nan
        atr_v = float(getattr(r, "atr")) if hasattr(r, "atr") and not pd.isna(getattr(r, "atr")) else np.nan
        ema21_1h_v = float(getattr(r, "ema21_1h")) if hasattr(r, "ema21_1h") and not pd.isna(getattr(r, "ema21_1h")) else np.nan
        breakout_level_v = float(getattr(r, "breakout_level")) if hasattr(r, "breakout_level") and not pd.isna(getattr(r, "breakout_level")) else np.nan
        touch_delta_v = int(getattr(r, "touch_delta")) if hasattr(r, "touch_delta") and not pd.isna(getattr(r, "touch_delta")) else np.nan
        strong_v = bool(getattr(r, "strong")) if hasattr(r, "strong") and not pd.isna(getattr(r, "strong")) else np.nan
        kd_w1_long_v = bool(getattr(r, "kd_w1_long")) if hasattr(r, "kd_w1_long") and not pd.isna(getattr(r, "kd_w1_long")) else np.nan
        kd_w1_short_v = bool(getattr(r, "kd_w1_short")) if hasattr(r, "kd_w1_short") and not pd.isna(getattr(r, "kd_w1_short")) else np.nan
        kd_3line_long_v = bool(getattr(r, "kd_3line_long")) if hasattr(r, "kd_3line_long") and not pd.isna(getattr(r, "kd_3line_long")) else np.nan
        kd_3line_short_v = bool(getattr(r, "kd_3line_short")) if hasattr(r, "kd_3line_short") and not pd.isna(getattr(r, "kd_3line_short")) else np.nan
        ts_utc_v = getattr(r, "ts_utc") if hasattr(r, "ts_utc") else pd.NaT
        src_v = str(getattr(r, "__src")) if hasattr(r, "__src") else ""
        chase_dist_atr_v = float("inf")
        if not pd.isna(atr_v) and float(atr_v) > 0 and not pd.isna(ema21_1h_v):
            chase_dist_atr_v = float(abs(float(entry) - float(ema21_1h_v)) / float(atr_v))

        df_sym = sym_cache.get(str(sym))
        if df_sym is None or df_sym.empty:
            continue
        ts0 = pd.to_datetime(sig_ts, utc=True).tz_convert("UTC").tz_localize(None)
        df = df_sym[df_sym["ts"] >= ts0].reset_index(drop=True)
        if df.empty:
            continue
        z0 = df.iloc[0]
        zrf_diff_v = float(z0["zrf_diff"]) if "zrf_diff" in df.columns and not pd.isna(z0["zrf_diff"]) else np.nan
        zrf_dea_v = float(z0["zrf_dea"]) if "zrf_dea" in df.columns and not pd.isna(z0["zrf_dea"]) else np.nan
        zrf_ws_v = float(z0["zrf_watershed"]) if "zrf_watershed" in df.columns and not pd.isna(z0["zrf_watershed"]) else np.nan
        zrf_bull_div_v = bool(z0["zrf_m_bull_div"]) if "zrf_m_bull_div" in df.columns and not pd.isna(z0["zrf_m_bull_div"]) else np.nan
        zrf_bear_div_v = bool(z0["zrf_m_bear_div"]) if "zrf_m_bear_div" in df.columns and not pd.isna(z0["zrf_m_bear_div"]) else np.nan
        zrf_low_kc_v = bool(z0["zrf_low_kc"]) if "zrf_low_kc" in df.columns and not pd.isna(z0["zrf_low_kc"]) else np.nan
        zrf_high_dc_v = bool(z0["zrf_high_dc"]) if "zrf_high_dc" in df.columns and not pd.isna(z0["zrf_high_dc"]) else np.nan
        zrf_zb_2nd_kc_v = bool(z0["zrf_zb_2nd_kc"]) if "zrf_zb_2nd_kc" in df.columns and not pd.isna(z0["zrf_zb_2nd_kc"]) else np.nan
        zrf_za_2nd_dc_v = bool(z0["zrf_za_2nd_dc"]) if "zrf_za_2nd_dc" in df.columns and not pd.isna(z0["zrf_za_2nd_dc"]) else np.nan
        cci144_v = float(z0["cci144"]) if "cci144" in df.columns and not pd.isna(z0["cci144"]) else np.nan
        adx14_v = float(z0["adx"]) if "adx" in df.columns and not pd.isna(z0["adx"]) else np.nan
        plus_di_v = float(z0["plus_di"]) if "plus_di" in df.columns and not pd.isna(z0["plus_di"]) else np.nan
        minus_di_v = float(z0["minus_di"]) if "minus_di" in df.columns and not pd.isna(z0["minus_di"]) else np.nan

        r0 = abs(float(entry) - float(stop))
        if not (r0 > 0):
            continue
        tp1 = float(entry) + float(tp1_r) * float(r0) if side == "LONG" else float(entry) - float(tp1_r) * float(r0)
        tp2 = float(entry) + float(tp2_r) * float(r0) if side == "LONG" else float(entry) - float(tp2_r) * float(r0)

        outcome = "NONE"
        bars_to = np.nan
        realized_r = np.nan
        mfe_r = -np.inf
        mae_r = np.inf

        for i in range(min(int(lookahead), int(len(df)))):
            hi = float(df.loc[i, "high"])
            lo = float(df.loc[i, "low"])
            cl = float(df.loc[i, "close"])

            if side == "LONG":
                mfe_r = max(float(mfe_r), (hi - entry) / r0)
                mae_r = min(float(mae_r), (lo - entry) / r0)
                stop_hit = lo <= stop
                tp2_hit = hi >= tp2
                tp1_hit = hi >= tp1
                if bar_rule == "tp_first":
                    if tp2_hit:
                        outcome = "TP2"
                        bars_to = float(i)
                        realized_r = float(tp2_r)
                        break
                    if tp1_hit:
                        outcome = "TP1"
                        bars_to = float(i)
                        realized_r = float(tp1_r)
                        break
                    if stop_hit:
                        outcome = "SL"
                        bars_to = float(i)
                        realized_r = -1.0
                        break
                else:
                    if stop_hit:
                        outcome = "SL"
                        bars_to = float(i)
                        realized_r = -1.0
                        break
                    if tp2_hit:
                        outcome = "TP2"
                        bars_to = float(i)
                        realized_r = float(tp2_r)
                        break
                    if tp1_hit:
                        outcome = "TP1"
                        bars_to = float(i)
                        realized_r = float(tp1_r)
                        break
            else:
                mfe_r = max(float(mfe_r), (entry - lo) / r0)
                mae_r = min(float(mae_r), (entry - hi) / r0)
                stop_hit = hi >= stop
                tp2_hit = lo <= tp2
                tp1_hit = lo <= tp1
                if bar_rule == "tp_first":
                    if tp2_hit:
                        outcome = "TP2"
                        bars_to = float(i)
                        realized_r = float(tp2_r)
                        break
                    if tp1_hit:
                        outcome = "TP1"
                        bars_to = float(i)
                        realized_r = float(tp1_r)
                        break
                    if stop_hit:
                        outcome = "SL"
                        bars_to = float(i)
                        realized_r = -1.0
                        break
                else:
                    if stop_hit:
                        outcome = "SL"
                        bars_to = float(i)
                        realized_r = -1.0
                        break
                    if tp2_hit:
                        outcome = "TP2"
                        bars_to = float(i)
                        realized_r = float(tp2_r)
                        break
                    if tp1_hit:
                        outcome = "TP1"
                        bars_to = float(i)
                        realized_r = float(tp1_r)
                        break
            if i == 0 and outcome == "NONE":
                if not pd.isna(cl):
                    realized_r = float((cl - entry) / r0) if side == "LONG" else float((entry - cl) / r0)

        rows.append(
            _apply_private_names(
                {
                    "ts_utc": str(ts_utc_v) if not pd.isna(ts_utc_v) else "",
                    "sig_ts": str(sig_ts),
                    "symbol": sym,
                    "side": side,
                    "signal": signal,
                    "entry": float(entry),
                    "stop": float(stop),
                    "tp1": float(tp1),
                    "tp2": float(tp2),
                    "tp1_r": float(tp1_r),
                    "tp2_r": float(tp2_r),
                    "lookahead": float(lookahead),
                    "bar_rule": str(bar_rule),
                    "outcome": str(outcome),
                    "bars_to": float(bars_to) if not pd.isna(bars_to) else np.nan,
                    "realized_r": float(realized_r) if not pd.isna(realized_r) else np.nan,
                    "mfe_r": float(mfe_r) if not pd.isna(mfe_r) else np.nan,
                    "mae_r": float(mae_r) if not pd.isna(mae_r) else np.nan,
                    "entry_score": float(score) if not pd.isna(score) else np.nan,
                    "atr": float(atr_v) if not pd.isna(atr_v) else np.nan,
                    "ema21_1h": float(ema21_1h_v) if not pd.isna(ema21_1h_v) else np.nan,
                    "breakout_level": float(breakout_level_v) if not pd.isna(breakout_level_v) else np.nan,
                    "touch_delta": float(touch_delta_v) if not pd.isna(touch_delta_v) else np.nan,
                    "strong": bool(strong_v) if not pd.isna(strong_v) else np.nan,
                    "kd_w1_long": bool(kd_w1_long_v) if not pd.isna(kd_w1_long_v) else np.nan,
                    "kd_w1_short": bool(kd_w1_short_v) if not pd.isna(kd_w1_short_v) else np.nan,
                    "kd_3line_long": bool(kd_3line_long_v) if not pd.isna(kd_3line_long_v) else np.nan,
                    "kd_3line_short": bool(kd_3line_short_v) if not pd.isna(kd_3line_short_v) else np.nan,
                    "chase_dist_atr": float(chase_dist_atr_v) if not pd.isna(chase_dist_atr_v) else np.nan,
                    "zrf_diff": float(zrf_diff_v) if not pd.isna(zrf_diff_v) else np.nan,
                    "zrf_dea": float(zrf_dea_v) if not pd.isna(zrf_dea_v) else np.nan,
                    "zrf_watershed": float(zrf_ws_v) if not pd.isna(zrf_ws_v) else np.nan,
                    "zrf_m_bull_div": bool(zrf_bull_div_v) if not pd.isna(zrf_bull_div_v) else np.nan,
                    "zrf_m_bear_div": bool(zrf_bear_div_v) if not pd.isna(zrf_bear_div_v) else np.nan,
                    "zrf_low_kc": bool(zrf_low_kc_v) if not pd.isna(zrf_low_kc_v) else np.nan,
                    "zrf_high_dc": bool(zrf_high_dc_v) if not pd.isna(zrf_high_dc_v) else np.nan,
                    "zrf_zb_2nd_kc": bool(zrf_zb_2nd_kc_v) if not pd.isna(zrf_zb_2nd_kc_v) else np.nan,
                    "zrf_za_2nd_dc": bool(zrf_za_2nd_dc_v) if not pd.isna(zrf_za_2nd_dc_v) else np.nan,
                    "cci144": float(cci144_v) if not pd.isna(cci144_v) else np.nan,
                    "cci144_lt_m144": bool(float(cci144_v) < -144.0) if not pd.isna(cci144_v) else np.nan,
                    "cci144_gt_p144": bool(float(cci144_v) > 144.0) if not pd.isna(cci144_v) else np.nan,
                    "adx14": float(adx14_v) if not pd.isna(adx14_v) else np.nan,
                    "plus_di14": float(plus_di_v) if not pd.isna(plus_di_v) else np.nan,
                    "minus_di14": float(minus_di_v) if not pd.isna(minus_di_v) else np.nan,
                    "__src": str(src_v),
                },
                private_names=private_names,
            )
        )

    out_df = pd.DataFrame(rows)
    out_dir = src_dir
    _write_csv(out_dir / "paper_replay_trades.csv", out_df)
    if out_df.empty:
        _write_csv(out_dir / "paper_replay_summary.csv", pd.DataFrame([{"trades": 0}]))
        print("[PAPER] no trades produced (csv)")
        return

    out_df["realized_r"] = pd.to_numeric(out_df["realized_r"], errors="coerce")
    out_df["is_win"] = out_df["realized_r"] > 0
    summ = (
        out_df.groupby(["symbol", "signal"], observed=True)
        .agg(
            n=("realized_r", "size"),
            win_rate=("is_win", "mean"),
            avg_r=("realized_r", "mean"),
            sl_rate=("outcome", lambda s: float((s == "SL").mean())),
            tp1_rate=("outcome", lambda s: float((s == "TP1").mean())),
            tp2_rate=("outcome", lambda s: float((s == "TP2").mean())),
            none_rate=("outcome", lambda s: float((s == "NONE").mean())),
            avg_mfe_r=("mfe_r", "mean"),
            avg_mae_r=("mae_r", "mean"),
        )
        .reset_index()
        .sort_values(["n", "avg_r"], ascending=[False, False])
    )
    total = pd.DataFrame(
        [
            {
                "symbol": "__TOTAL__",
                "signal": "",
                "n": float(len(out_df)),
                "win_rate": float(out_df["is_win"].mean()),
                "avg_r": float(out_df["realized_r"].mean()),
                "sl_rate": float((out_df["outcome"] == "SL").mean()),
                "tp1_rate": float((out_df["outcome"] == "TP1").mean()),
                "tp2_rate": float((out_df["outcome"] == "TP2").mean()),
                "none_rate": float((out_df["outcome"] == "NONE").mean()),
                "avg_mfe_r": float(pd.to_numeric(out_df["mfe_r"], errors="coerce").mean()),
                "avg_mae_r": float(pd.to_numeric(out_df["mae_r"], errors="coerce").mean()),
            }
        ]
    )
    summ2 = pd.concat([summ, total], axis=0, ignore_index=True)
    if e2_chase_max is not None:
        def _summ_row(df_sub: pd.DataFrame, label: str) -> Dict[str, object]:
            df_sub = df_sub.copy()
            df_sub["realized_r"] = pd.to_numeric(df_sub.get("realized_r", np.nan), errors="coerce")
            df_sub["is_win"] = pd.to_numeric(df_sub.get("realized_r", np.nan), errors="coerce") > 0
            return {
                "symbol": "__TOTAL__",
                "signal": str(label),
                "n": float(len(df_sub)),
                "win_rate": float(df_sub["is_win"].mean()) if len(df_sub) else np.nan,
                "avg_r": float(df_sub["realized_r"].mean()) if len(df_sub) else np.nan,
                "sl_rate": float((df_sub.get("outcome", "") == "SL").mean()) if len(df_sub) else np.nan,
                "tp1_rate": float((df_sub.get("outcome", "") == "TP1").mean()) if len(df_sub) else np.nan,
                "tp2_rate": float((df_sub.get("outcome", "") == "TP2").mean()) if len(df_sub) else np.nan,
                "none_rate": float((df_sub.get("outcome", "") == "NONE").mean()) if len(df_sub) else np.nan,
                "avg_mfe_r": float(pd.to_numeric(df_sub.get("mfe_r", np.nan), errors="coerce").mean()) if len(df_sub) else np.nan,
                "avg_mae_r": float(pd.to_numeric(df_sub.get("mae_r", np.nan), errors="coerce").mean()) if len(df_sub) else np.nan,
            }

        thr = float(e2_chase_max)
        thr_s = ("%g" % thr).strip()
        e2_base = out_df[out_df["signal"] == "E2"].copy()
        e2c = e2_base[(pd.to_numeric(e2_base.get("chase_dist_atr", np.nan), errors="coerce") < thr)].copy()
        e1 = out_df[out_df["signal"] == "E1"].copy()
        e1_e2c = pd.concat([e1, e2c], axis=0, ignore_index=True)
        extra = pd.DataFrame(
            [
                _summ_row(e2_base, "E2_base"),
                _summ_row(e2c, f"E2c<{thr_s}"),
                _summ_row(e1_e2c, f"E1+E2c<{thr_s}"),
            ]
        )
        summ2 = pd.concat([summ2, extra], axis=0, ignore_index=True)
    _write_csv(out_dir / "paper_replay_summary.csv", summ2)
    with pd.option_context("display.max_rows", 200, "display.width", 200):
        print(summ2.to_string(index=False))


def _paper_commentary(args: Dict[str, Any]) -> None:
    src = str(args.get("paper_dir") or "").strip()
    src_dir = Path(src) if src else _log_dir_for_run(args)
    if not src_dir.exists():
        raise FileNotFoundError(f"paper_dir not found: {str(src_dir)}")

    trades_path = src_dir / "paper_replay_trades.csv"
    if not trades_path.exists():
        raise FileNotFoundError(
            "paper_replay_trades.csv not found under paper_dir. "
            "Run: python mt5_exit_assistant.py --paper-replay --paper-dir <DIR>"
        )

    df = pd.read_csv(trades_path)
    if df is None or df.empty:
        print(f"[COMMENTARY] empty trades: {str(trades_path)}")
        return

    df = df.copy()
    df["symbol"] = df.get("symbol", "").astype(str).str.upper()
    df["signal"] = df.get("signal", "").astype(str).str.upper()
    df["side"] = df.get("side", "").astype(str).str.upper()
    df["sig_ts"] = pd.to_datetime(df.get("sig_ts", ""), errors="coerce")
    df["realized_r"] = pd.to_numeric(df.get("realized_r", np.nan), errors="coerce")
    df["mfe_r"] = pd.to_numeric(df.get("mfe_r", np.nan), errors="coerce")
    df["mae_r"] = pd.to_numeric(df.get("mae_r", np.nan), errors="coerce")
    df["chase_dist_atr"] = pd.to_numeric(df.get("chase_dist_atr", np.nan), errors="coerce")
    df["sr_support_dist_atr"] = pd.to_numeric(df.get("sr_support_dist_atr", np.nan), errors="coerce")
    df["sr_resistance_dist_atr"] = pd.to_numeric(df.get("sr_resistance_dist_atr", np.nan), errors="coerce")

    df = df.dropna(subset=["realized_r"])
    if df.empty:
        print(f"[COMMENTARY] no valid realized_r rows: {str(trades_path)}")
        return

    sym_req = str(args.get("commentary_symbol") or "").strip().upper()
    syms = [s for s in sorted(set(df["symbol"].dropna().astype(str).tolist())) if s and s != "NAN"]
    if sym_req:
        sym = sym_req
    elif len(syms) == 1:
        sym = syms[0]
    else:
        cand = [s for s in syms if "XAU" in s]
        sym = cand[0] if cand else (syms[0] if syms else "")

    df_sym = df[df["symbol"] == sym].copy() if sym else df.copy()
    if df_sym.empty:
        print(f"[COMMENTARY] no rows for symbol={sym} in {str(trades_path)}")
        return

    def _sig_label(s: str) -> str:
        s = str(s or "").strip().upper()
        if s == "B_BUY":
            return "SIG_BUY"
        if s == "B_SELL":
            return "SIG_SELL"
        if s == "B_GOLD":
            return "SIG_HIGH_CONF"
        return s

    df_sym["_sig_label"] = df_sym["signal"].map(_sig_label)
    df_sym["sig_label"] = df_sym["_sig_label"]
    df_sym["is_win"] = df_sym["realized_r"] > 0
    df_sym["outcome"] = df_sym.get("outcome", "").astype(str).str.upper()

    start_ts = df_sym["sig_ts"].min()
    end_ts = df_sym["sig_ts"].max()
    n = int(len(df_sym))
    win_rate = float(df_sym["is_win"].mean()) if n else np.nan
    avg_r = float(df_sym["realized_r"].mean()) if n else np.nan
    sl_rate = float((df_sym["outcome"] == "SL").mean()) if n else np.nan
    tp2_rate = float((df_sym["outcome"] == "TP2").mean()) if n else np.nan
    tp1_rate = float((df_sym["outcome"] == "TP1").mean()) if n else np.nan

    min_n = max(1, int(args.get("commentary_min_n") or 15))
    topk = max(1, int(args.get("commentary_topk") or 5))

    by_sig = (
        df_sym.groupby(["sig_label"], observed=True)
        .agg(
            n=("realized_r", "size"),
            win_rate=("is_win", "mean"),
            avg_r=("realized_r", "mean"),
            sl_rate=("outcome", lambda s: float((s == "SL").mean())),
            tp2_rate=("outcome", lambda s: float((s == "TP2").mean())),
        )
        .reset_index()
    )
    by_sig = by_sig[by_sig["n"] >= float(min_n)].sort_values(["avg_r", "n"], ascending=[False, False]).reset_index(drop=True)

    def _fmt_pct(x: Any) -> str:
        try:
            if x is None or pd.isna(x):
                return "NA"
            return f"{float(x) * 100:.1f}%"
        except Exception:
            return "NA"

    def _fmt_f(x: Any, nd: int = 3) -> str:
        try:
            if x is None or pd.isna(x):
                return "NA"
            return f"{float(x):.{nd}f}"
        except Exception:
            return "NA"

    print("")
    print("[COMMENTARY] 只读分析（不触发交易）")
    print(f"[COMMENTARY] src={str(trades_path)}")
    print(
        f"[COMMENTARY] symbol={sym if sym else '__ALL__'} trades={n} range={str(start_ts) if not pd.isna(start_ts) else ''} ~ {str(end_ts) if not pd.isna(end_ts) else ''}"
    )
    print(
        f"[COMMENTARY] win_rate={_fmt_pct(win_rate)} avg_r={_fmt_f(avg_r)} sl_rate={_fmt_pct(sl_rate)} tp1_rate={_fmt_pct(tp1_rate)} tp2_rate={_fmt_pct(tp2_rate)}"
    )

    if not by_sig.empty:
        print("")
        print(f"[COMMENTARY] 信号分组（n>={min_n}）按 avg_r 排序 Top{topk}:")
        top = by_sig.head(topk)
        for r in top.itertuples(index=False):
            print(
                f"  - signal={str(getattr(r, 'sig_label'))} n={int(getattr(r, 'n'))} "
                f"win_rate={_fmt_pct(getattr(r, 'win_rate'))} avg_r={_fmt_f(getattr(r, 'avg_r'))} "
                f"sl_rate={_fmt_pct(getattr(r, 'sl_rate'))} tp2_rate={_fmt_pct(getattr(r, 'tp2_rate'))}"
            )
        bot = by_sig.tail(min(topk, len(by_sig))).sort_values(["avg_r", "n"], ascending=[True, False])
        print(f"[COMMENTARY] 信号分组（n>={min_n}）按 avg_r 排序 Bottom{min(topk, len(by_sig))}:")
        for r in bot.itertuples(index=False):
            print(
                f"  - signal={str(getattr(r, 'sig_label'))} n={int(getattr(r, 'n'))} "
                f"win_rate={_fmt_pct(getattr(r, 'win_rate'))} avg_r={_fmt_f(getattr(r, 'avg_r'))} "
                f"sl_rate={_fmt_pct(getattr(r, 'sl_rate'))} tp2_rate={_fmt_pct(getattr(r, 'tp2_rate'))}"
            )

    e2 = df_sym[df_sym["sig_label"] == "E2"].copy()
    if not e2.empty and e2["chase_dist_atr"].notna().any():
        chase = pd.to_numeric(e2["chase_dist_atr"], errors="coerce")
        e2["_chase_bucket"] = np.where(
            chase.notna() & (chase < 1.0),
            "CHASE<1.0",
            np.where(chase.notna() & (chase < 1.5), "1.0<=CHASE<1.5", "CHASE>=1.5/NA"),
        )
        e2["chase_bucket"] = e2["_chase_bucket"]
        e2_b = (
            e2.groupby(["chase_bucket"], observed=True)
            .agg(
                n=("realized_r", "size"),
                win_rate=("is_win", "mean"),
                avg_r=("realized_r", "mean"),
                sl_rate=("outcome", lambda s: float((s == "SL").mean())),
            )
            .reset_index()
            .sort_values(["chase_bucket"], ascending=[True])
        )
        print("")
        print("[COMMENTARY] E2 追价距离分桶（chase_dist_atr）:")
        for r in e2_b.itertuples(index=False):
            print(
                f"  - {str(getattr(r, 'chase_bucket'))}: n={int(getattr(r, 'n'))} "
                f"win_rate={_fmt_pct(getattr(r, 'win_rate'))} avg_r={_fmt_f(getattr(r, 'avg_r'))} sl_rate={_fmt_pct(getattr(r, 'sl_rate'))}"
            )

    def _split_stats(mask: pd.Series, label_true: str, label_false: str) -> None:
        if mask is None:
            return
        m = pd.to_numeric(mask, errors="coerce")
        if not m.notna().any():
            return
        t = df_sym[m != 0].copy()
        f = df_sym[m == 0].copy()
        if t.empty or f.empty:
            return
        for sub in (t, f):
            sub["is_win"] = pd.to_numeric(sub.get("realized_r", np.nan), errors="coerce") > 0
            sub["outcome"] = sub.get("outcome", "").astype(str).str.upper()
        print("")
        print(f"[COMMENTARY] 条件对比：{label_true} vs {label_false}")
        print(
            f"  - {label_true}: n={len(t)} win_rate={_fmt_pct(float(t['is_win'].mean()))} avg_r={_fmt_f(float(t['realized_r'].mean()))} sl_rate={_fmt_pct(float((t['outcome']=='SL').mean()))}"
        )
        print(
            f"  - {label_false}: n={len(f)} win_rate={_fmt_pct(float(f['is_win'].mean()))} avg_r={_fmt_f(float(f['realized_r'].mean()))} sl_rate={_fmt_pct(float((f['outcome']=='SL').mean()))}"
        )

    if "liquidity_risk" in df_sym.columns:
        _split_stats(df_sym.get("liquidity_risk"), "liquidity_risk=1", "liquidity_risk=0")
    if "vol_risk_blocked" in df_sym.columns:
        _split_stats(df_sym.get("vol_risk_blocked"), "vol_risk_blocked=1", "vol_risk_blocked=0")

    long_sr = df_sym[df_sym["side"] == "LONG"].copy()
    short_sr = df_sym[df_sym["side"] == "SHORT"].copy()
    if not long_sr.empty and long_sr["sr_support_dist_atr"].notna().any():
        m = pd.to_numeric(long_sr["sr_support_dist_atr"], errors="coerce")
        long_sr["_near"] = np.where(m.notna() & (m <= 0.5), 1, 0)
        t = long_sr[long_sr["_near"] == 1]
        f = long_sr[long_sr["_near"] == 0]
        if (not t.empty) and (not f.empty):
            print("")
            print("[COMMENTARY] LONG：离支撑近（sr_support_dist_atr<=0.5） vs 其他:")
            print(
                f"  - near: n={len(t)} win_rate={_fmt_pct(float((t['realized_r']>0).mean()))} avg_r={_fmt_f(float(t['realized_r'].mean()))} sl_rate={_fmt_pct(float((t['outcome']=='SL').mean()))}"
            )
            print(
                f"  - far:  n={len(f)} win_rate={_fmt_pct(float((f['realized_r']>0).mean()))} avg_r={_fmt_f(float(f['realized_r'].mean()))} sl_rate={_fmt_pct(float((f['outcome']=='SL').mean()))}"
            )

    if not short_sr.empty and short_sr["sr_resistance_dist_atr"].notna().any():
        m = pd.to_numeric(short_sr["sr_resistance_dist_atr"], errors="coerce")
        short_sr["_near"] = np.where(m.notna() & (m <= 0.5), 1, 0)
        t = short_sr[short_sr["_near"] == 1]
        f = short_sr[short_sr["_near"] == 0]
        if (not t.empty) and (not f.empty):
            print("")
            print("[COMMENTARY] SHORT：离压力近（sr_resistance_dist_atr<=0.5） vs 其他:")
            print(
                f"  - near: n={len(t)} win_rate={_fmt_pct(float((t['realized_r']>0).mean()))} avg_r={_fmt_f(float(t['realized_r'].mean()))} sl_rate={_fmt_pct(float((t['outcome']=='SL').mean()))}"
            )
            print(
                f"  - far:  n={len(f)} win_rate={_fmt_pct(float((f['realized_r']>0).mean()))} avg_r={_fmt_f(float(f['realized_r'].mean()))} sl_rate={_fmt_pct(float((f['outcome']=='SL').mean()))}"
            )

    def _print_examples(title: str, df_ex: pd.DataFrame) -> None:
        if df_ex is None or df_ex.empty:
            return
        print("")
        print(f"[COMMENTARY] {title}:")
        cols = [
            "sig_ts",
            "sig_label",
            "side",
            "realized_r",
            "outcome",
            "chase_dist_atr",
            "sr_support_dist_atr",
            "sr_resistance_dist_atr",
        ]
        for r in df_ex[cols].itertuples(index=False):
            ts = str(getattr(r, "sig_ts")) if not pd.isna(getattr(r, "sig_ts")) else ""
            print(
                f"  - ts={ts} signal={str(getattr(r, 'sig_label'))} side={str(getattr(r, 'side'))} "
                f"outcome={str(getattr(r, 'outcome'))} realized_r={_fmt_f(getattr(r, 'realized_r'))} "
                f"chase_atr={_fmt_f(getattr(r, 'chase_dist_atr'), 2)} "
                f"sr_sup_atr={_fmt_f(getattr(r, 'sr_support_dist_atr'), 2)} sr_res_atr={_fmt_f(getattr(r, 'sr_resistance_dist_atr'), 2)}"
            )

    df_sym = df_sym.sort_values(["realized_r"], ascending=[False]).reset_index(drop=True)
    _print_examples("代表性强势样本（realized_r Top3）", df_sym.head(3))
    _print_examples("代表性回撤样本（realized_r Bottom3）", df_sym.tail(3).sort_values(["realized_r"], ascending=[True]))

    print("")
    print("[COMMENTARY] 结论模板（需结合你自己的风险偏好）")
    print("  - 现阶段的重点不是“看对方向”，而是把能稳定降低 SL_rate / 提高 avg_r 的条件固化为标签→分桶→再门控。")
    print("  - 先从上面各分桶/对比里，挑 1-2 个最稳的提升点作为下一轮验证对象。")
    print("")


def _mt5_rates_range_local(symbol: str, timeframe: int, dt_from: datetime, dt_to: datetime) -> pd.DataFrame:
    symbol = str(symbol).strip()
    if not symbol:
        raise ValueError("empty symbol")
    _ensure_symbol_ready(symbol)
    local_tz = datetime.now().astimezone().tzinfo
    rates = mt5.copy_rates_range(symbol, timeframe, dt_from, dt_to)
    if rates is None:
        raise RuntimeError(f"copy_rates_range returned None, error={_mt5_last_error()}")
    if len(rates) <= 2:
        raise RuntimeError(f"not enough rates for {symbol} tf={timeframe}: {len(rates)}")
    df = pd.DataFrame(rates)
    if "time" not in df.columns:
        raise RuntimeError(f"rates missing time field: {symbol} tf={timeframe}")
    dt_open = pd.to_datetime(df["time"].astype(int), unit="s", utc=True).dt.tz_convert(local_tz).dt.tz_localize(None)
    close_dt = dt_open + pd.to_timedelta(_tf_seconds(timeframe), unit="s")
    df["ts"] = close_dt
    if "tick_volume" in df.columns:
        df["volume"] = df["tick_volume"]
    keep = [c for c in ["ts", "open", "high", "low", "close", "volume", "tick_volume"] if c in df.columns]
    df = df[keep].dropna(subset=["open", "high", "low", "close", "ts"])
    df = df.set_index("ts").sort_index()
    df = df.iloc[:-1].copy()
    return df


def _scan_entry_signals_from_dfs(
    symbol: str,
    df1: pd.DataFrame,
    df4: pd.DataFrame,
    dfd: pd.DataFrame,
    p: Params,
    include_bobby_signals: bool = False,
    bobby_sl_atr: float = 1.0,
) -> List[EntrySignal]:
    df1 = df1.copy()
    df1["atr"] = atr(df1, int(p.atr_n))
    tr = compute_trend_flags(df1, df4, dfd, p)
    tr = tr.reindex(df1.index)

    if len(df1) < int(max(p.n_break + 5, p.atr_n + 5, 60)):
        return []
    o_arr = df1["open"].to_numpy(dtype=float)
    h_arr = df1["high"].to_numpy(dtype=float)
    l_arr = df1["low"].to_numpy(dtype=float)
    c_arr = df1["close"].to_numpy(dtype=float)
    atr_arr = df1["atr"].to_numpy(dtype=float)
    tv_arr = df1["tick_volume"].to_numpy(dtype=float) if "tick_volume" in df1.columns else np.full(len(df1), np.nan, dtype=float)
    adx14_df = _adx_from_ohlc(df1["high"], df1["low"], df1["close"], 14)
    adx14_arr = adx14_df["adx"].to_numpy(dtype=float)
    cci144_arr = _cci_from_ohlc(df1["high"], df1["low"], df1["close"], 144).to_numpy(dtype=float)
    zrf_h1 = _zrf_macd_from_close(df1["close"])
    jg_macd_up_arr = _cross_up(zrf_h1["zrf_diff"], zrf_h1["zrf_dea"]).to_numpy(dtype=bool)
    jg_macd_down_arr = _cross_down(zrf_h1["zrf_diff"], zrf_h1["zrf_dea"]).to_numpy(dtype=bool)
    jg_sma175_arr = (
        pd.to_numeric(df1["close"], errors="coerce")
        .rolling(175, min_periods=175)
        .mean()
        .to_numpy(dtype=float)
    )
    jg_j_arr = _stoch_kdj_from_ohlc(df1["high"], df1["low"], df1["close"], 9, 3, 3)["j"].to_numpy(dtype=float)
    jg_df = _jinding_features(df1)
    jg_ma13_arr = jg_df["jg_ma13"].to_numpy(dtype=float)
    jg_ma55_arr = jg_df["jg_ma55"].to_numpy(dtype=float)
    jg_ema20_arr = jg_df["jg_ema20"].to_numpy(dtype=float)
    jg_ema27_arr = jg_df["jg_ema27"].to_numpy(dtype=float)
    jg_ema29_arr = jg_df["jg_ema29"].to_numpy(dtype=float)
    jg_ema32_arr = jg_df["jg_ema32"].to_numpy(dtype=float)
    jg_ema36_arr = jg_df["jg_ema36"].to_numpy(dtype=float)
    jg_pivot_mid_arr = jg_df["jg_pivot_mid"].to_numpy(dtype=float)
    jg_b3_arr = jg_df["jg_b3"].to_numpy(dtype=float)
    jg_s3_arr = jg_df["jg_s3"].to_numpy(dtype=float)
    jg_b5_arr = jg_df["jg_b5"].to_numpy(dtype=float)
    jg_s5_arr = jg_df["jg_s5"].to_numpy(dtype=float)
    jg_var2_arr = jg_df["jg_var2"].to_numpy(dtype=float)
    jg_var3_arr = jg_df["jg_var3"].to_numpy(dtype=float)
    jg_var3_ma6_arr = jg_df["jg_var3_ma6"].to_numpy(dtype=float)
    jg_bar_yellow_arr = jg_df["jg_bar_yellow"].to_numpy(dtype=bool)
    jg_bar_red_arr = jg_df["jg_bar_red"].to_numpy(dtype=bool)
    jg_flip_to_yellow_arr = jg_df["jg_flip_to_yellow"].to_numpy(dtype=bool)
    jg_flip_to_red_arr = jg_df["jg_flip_to_red"].to_numpy(dtype=bool)
    jg_macd_arr = jg_df["jg_macd"].to_numpy(dtype=float)
    jg_buy_arr = jg_df["jg_buy"].to_numpy(dtype=bool)
    jg_sell_arr = jg_df["jg_sell"].to_numpy(dtype=bool)
    jg_gold_arr = jg_df["jg_gold"].to_numpy(dtype=bool)
    jg_ma160_arr = jg_df["jg_ma160"].to_numpy(dtype=float)
    jg_ma120_arr = jg_df["jg_ma120"].to_numpy(dtype=float)
    jg_ma60_arr = jg_df["jg_ma60"].to_numpy(dtype=float)
    jg_ma25_arr = jg_df["jg_ma25"].to_numpy(dtype=float)
    jg_wick_touch_ma13_arr = jg_df["jg_wick_touch_ma13"].to_numpy(dtype=bool)
    jg_wick_touch_ma55_arr = jg_df["jg_wick_touch_ma55"].to_numpy(dtype=bool)
    jg_wick_touch_ema27_arr = jg_df["jg_wick_touch_ema27"].to_numpy(dtype=bool)
    jg_wick_touch_ema29_arr = jg_df["jg_wick_touch_ema29"].to_numpy(dtype=bool)
    jg_wick_touch_ema32_arr = jg_df["jg_wick_touch_ema32"].to_numpy(dtype=bool)
    jg_wick_touch_ema36_arr = jg_df["jg_wick_touch_ema36"].to_numpy(dtype=bool)
    jg_close_breakdown_ma13_arr = jg_df["jg_close_breakdown_ma13"].to_numpy(dtype=bool)
    jg_close_breakup_ma13_arr = jg_df["jg_close_breakup_ma13"].to_numpy(dtype=bool)
    jg_close_breakdown_ma55_arr = jg_df["jg_close_breakdown_ma55"].to_numpy(dtype=bool)
    jg_close_breakup_ma55_arr = jg_df["jg_close_breakup_ma55"].to_numpy(dtype=bool)
    jg_cross_ma13_ema27_up_arr = jg_df["jg_cross_ma13_ema27_up"].to_numpy(dtype=bool)
    jg_cross_ma13_ema27_down_arr = jg_df["jg_cross_ma13_ema27_down"].to_numpy(dtype=bool)
    jg_cross_ma13_ema29_up_arr = jg_df["jg_cross_ma13_ema29_up"].to_numpy(dtype=bool)
    jg_cross_ma13_ema29_down_arr = jg_df["jg_cross_ma13_ema29_down"].to_numpy(dtype=bool)
    jg_cross_ma13_ema32_up_arr = jg_df["jg_cross_ma13_ema32_up"].to_numpy(dtype=bool)
    jg_cross_ma13_ema32_down_arr = jg_df["jg_cross_ma13_ema32_down"].to_numpy(dtype=bool)
    jg_cross_ma13_ema36_up_arr = jg_df["jg_cross_ma13_ema36_up"].to_numpy(dtype=bool)
    jg_cross_ma13_ema36_down_arr = jg_df["jg_cross_ma13_ema36_down"].to_numpy(dtype=bool)
    jg_after_cross_ma13_ema27_up_j_lt80_arr = jg_df["jg_after_cross_ma13_ema27_up_j_lt80"].to_numpy(dtype=bool)
    jg_after_cross_ma13_ema27_down_j_gt20_arr = jg_df["jg_after_cross_ma13_ema27_down_j_gt20"].to_numpy(dtype=bool)
    jg_dist_b3_atr_arr = jg_df["jg_dist_b3_atr"].to_numpy(dtype=float)
    jg_dist_s3_atr_arr = jg_df["jg_dist_s3_atr"].to_numpy(dtype=float)
    jg_dist_pivot_atr_arr = jg_df["jg_dist_pivot_atr"].to_numpy(dtype=float)
    jg_red_streak_arr = jg_df["jg_red_streak"].to_numpy(dtype=int)
    jg_yellow_streak_arr = jg_df["jg_yellow_streak"].to_numpy(dtype=int)

    strong_long_arr = tr["strong_long"].to_numpy(dtype=bool)
    strong_short_arr = tr["strong_short"].to_numpy(dtype=bool)
    regime_long_arr = tr["regime_long"].to_numpy(dtype=bool)
    regime_short_arr = tr["regime_short"].to_numpy(dtype=bool)
    confirm_long_arr = tr["confirm_long"].to_numpy(dtype=bool)
    confirm_short_arr = tr["confirm_short"].to_numpy(dtype=bool)
    ema21_1h_arr = tr["ema21_1h"].to_numpy(dtype=float)
    ema13_4h_arr = tr["ema13_4h"].to_numpy(dtype=float)
    ema55_4h_arr = tr["ema55_4h"].to_numpy(dtype=float)
    ema144_4h_arr = tr["ema144_4h"].to_numpy(dtype=float)
    close_4h_arr = tr["close_4h"].to_numpy(dtype=float)
    kd_k_4h_arr = tr["kd_k_4h"].to_numpy(dtype=float)
    kd_d_4h_arr = tr["kd_d_4h"].to_numpy(dtype=float)
    kd_k_1d_arr = tr["kd_k_1d"].to_numpy(dtype=float)
    kd_d_1d_arr = tr["kd_d_1d"].to_numpy(dtype=float)
    kd_w1_long_arr = tr["kd_w1_long"].to_numpy(dtype=bool) if "kd_w1_long" in tr.columns else np.zeros(len(df1), dtype=bool)
    kd_w1_short_arr = tr["kd_w1_short"].to_numpy(dtype=bool) if "kd_w1_short" in tr.columns else np.zeros(len(df1), dtype=bool)
    kd_3line_long_arr = tr["kd_3line_long"].to_numpy(dtype=bool) if "kd_3line_long" in tr.columns else np.zeros(len(df1), dtype=bool)
    kd_3line_short_arr = tr["kd_3line_short"].to_numpy(dtype=bool) if "kd_3line_short" in tr.columns else np.zeros(len(df1), dtype=bool)
    bb_squeeze_4h_arr = tr["bb_squeeze_4h"].to_numpy(dtype=bool)

    level_long_arr = df1["high"].rolling(int(p.n_break), min_periods=int(p.n_break)).max().shift(1).to_numpy(dtype=float)
    level_short_arr = df1["low"].rolling(int(p.n_break), min_periods=int(p.n_break)).min().shift(1).to_numpy(dtype=float)

    e1_state: Optional[str] = None
    e1_dir = 0
    e1_level = np.nan
    e1_start_i = -1
    e1_end_i = -1
    e1_touched = False
    e1_break_i = -1
    e1_break_atr = np.nan
    e1_break_strength_atr_state = 0.0
    e1_touch_i = -1
    e1_retest_depth_atr_state = 0.0
    last_touch_i_long: Optional[int] = None
    last_touch_i_short: Optional[int] = None

    idx = df1.index
    sigs: List[EntrySignal] = []
    sym_u = str(symbol).upper()
    for i in range(len(df1)):
        o = float(o_arr[i])
        h = float(h_arr[i])
        l = float(l_arr[i])
        cl = float(c_arr[i])
        a = float(atr_arr[i])
        if not (a > 0) or pd.isna(a) or pd.isna(cl) or pd.isna(o) or pd.isna(h) or pd.isna(l):
            continue

        strong_long = bool(strong_long_arr[i])
        strong_short = bool(strong_short_arr[i])
        gate_long = strong_long if bool(p.require_strong_for_entry) else (bool(regime_long_arr[i]) and bool(confirm_long_arr[i]))
        gate_short = strong_short if bool(p.require_strong_for_entry) else (bool(regime_short_arr[i]) and bool(confirm_short_arr[i]))

        ema21_1h = float(ema21_1h_arr[i])
        if (not bool(p.enable_e2_touch_requires_strong)) or strong_long:
            if l <= ema21_1h - float(p.touch_k) * a:
                last_touch_i_long = i
        if (not bool(p.enable_e2_touch_requires_strong)) or strong_short:
            if h >= ema21_1h + float(p.touch_k) * a:
                last_touch_i_short = i

        e1_entry = False
        e1_entry_side = 0
        e1_break_strength_atr = 0.0
        e1_retest_depth_atr = 0.0
        e1_retest_bars = 0
        e1_touch_bars = 0
        e1_atr_ratio = 1.0
        touch_delta: Optional[int] = None
        body_atr = 0.0
        breakout_atr = 0.0

        if gate_long or gate_short:
            if e1_state is None:
                if gate_long:
                    level_long = float(level_long_arr[i])
                    if (not pd.isna(level_long)) and cl > level_long:
                        e1_state = "await"
                        e1_dir = 1
                        e1_level = float(level_long)
                        e1_start_i = i + 1
                        e1_end_i = i + int(p.m_retest)
                        e1_touched = False
                        e1_break_i = i
                        e1_break_atr = a
                        e1_break_strength_atr_state = (cl - e1_level) / a if a > 0 else 0.0
                        e1_touch_i = -1
                        e1_retest_depth_atr_state = 0.0
                elif gate_short:
                    level_short = float(level_short_arr[i])
                    if (not pd.isna(level_short)) and cl < level_short:
                        e1_state = "await"
                        e1_dir = -1
                        e1_level = float(level_short)
                        e1_start_i = i + 1
                        e1_end_i = i + int(p.m_retest)
                        e1_touched = False
                        e1_break_i = i
                        e1_break_atr = a
                        e1_break_strength_atr_state = (e1_level - cl) / a if a > 0 else 0.0
                        e1_touch_i = -1
                        e1_retest_depth_atr_state = 0.0
            else:
                if i < e1_start_i or i > e1_end_i:
                    e1_state = None
                else:
                    band_low = float(e1_level) - float(p.k) * a
                    band_high = float(e1_level) + float(p.k) * a
                    touched = (l <= band_high) and (h >= band_low)
                    if touched:
                        e1_touched = True
                        if e1_touch_i < 0:
                            e1_touch_i = i
                    if e1_dir == 1:
                        depth_atr = (float(e1_level) - l) / a if a > 0 else 0.0
                    else:
                        depth_atr = (h - float(e1_level)) / a if a > 0 else 0.0
                    if float(depth_atr) > float(e1_retest_depth_atr_state):
                        e1_retest_depth_atr_state = float(depth_atr)

                    fail = False
                    if float(p.e1_fail_k) > 0:
                        if e1_dir == 1:
                            fail = cl < (float(e1_level) - float(p.e1_fail_k) * a)
                        else:
                            fail = cl > (float(e1_level) + float(p.e1_fail_k) * a)
                    if fail:
                        e1_state = None
                    else:
                        confirmed = (cl >= float(e1_level)) if e1_dir == 1 else (cl <= float(e1_level))
                        if e1_touched and confirmed:
                            e1_entry = True
                            e1_entry_side = int(e1_dir)
                            breakout_atr = abs(cl - float(e1_level)) / a if a > 0 else 0.0
                            e1_break_strength_atr = float(e1_break_strength_atr_state)
                            e1_retest_depth_atr = float(e1_retest_depth_atr_state)
                            e1_retest_bars = int(i - e1_break_i) if e1_break_i >= 0 else 0
                            e1_touch_bars = int(i - e1_touch_i) if e1_touch_i >= 0 else e1_retest_bars
                            e1_atr_ratio = (
                                float(a / e1_break_atr)
                                if (e1_break_atr is not None and not pd.isna(e1_break_atr) and float(e1_break_atr) > 0)
                                else 1.0
                            )
                            e1_state = None

        if e1_entry:
            entry_side = int(e1_entry_side)
            entry_reason = "E1"
        else:
            entry_side = 0
            entry_reason = ""
            if gate_long:
                touched_ok = last_touch_i_long is not None and 1 <= i - int(last_touch_i_long) <= int(p.x_touch)
                if touched_ok:
                    touch_delta = i - int(last_touch_i_long)
                    body = abs(cl - o)
                    body_atr = body / a if a > 0 else 0.0
                    wick_ok = l >= ema21_1h - float(p.shadow_k) * a
                    reclaim = (cl > ema21_1h) and (cl > o) and (body >= float(p.body_k) * a) and wick_ok
                    if reclaim:
                        if bool(p.enable_e2_break_confirm):
                            level_long = float(level_long_arr[i])
                            if (not pd.isna(level_long)) and (cl > level_long):
                                breakout_atr = (cl - level_long) / a if a > 0 else 0.0
                                entry_side = 1
                                entry_reason = "E2"
                        else:
                            entry_side = 1
                            entry_reason = "E2"
            elif gate_short:
                touched_ok = last_touch_i_short is not None and 1 <= i - int(last_touch_i_short) <= int(p.x_touch)
                if touched_ok:
                    touch_delta = i - int(last_touch_i_short)
                    body = abs(cl - o)
                    body_atr = body / a if a > 0 else 0.0
                    wick_ok = h <= ema21_1h + float(p.shadow_k) * a
                    reclaim = (cl < ema21_1h) and (cl < o) and (body >= float(p.body_k) * a) and wick_ok
                    if reclaim:
                        if bool(p.enable_e2_break_confirm):
                            level_short = float(level_short_arr[i])
                            if (not pd.isna(level_short)) and (cl < level_short):
                                breakout_atr = (level_short - cl) / a if a > 0 else 0.0
                                entry_side = -1
                                entry_reason = "E2"
                        else:
                            entry_side = -1
                            entry_reason = "E2"

        if entry_side != 0:
            cci144_v = float(cci144_arr[i]) if i < len(cci144_arr) else np.nan
            adx14_v = float(adx14_arr[i]) if i < len(adx14_arr) else np.nan
            if _E1_CCI144_VETO_ENABLED and entry_reason == "E1" and (not pd.isna(cci144_v)) and float(cci144_v) < -144.0:
                continue

            dist_ema = (cl - ema21_1h) if entry_side == 1 else (ema21_1h - cl)
            dist_ema_atr = dist_ema / a if a > 0 else 0.0
            chase_dist_atr = abs(dist_ema) / a if a > 0 else float("inf")

            entry_score = 1.0
            if entry_reason == "E2":
                entry_score += 0.5
            entry_score += max(0.0, min(float(dist_ema_atr), 2.0)) / 2.0
            entry_score += min(max(float(body_atr), 0.0), 2.0) / 2.0 * 0.5
            if touch_delta is not None:
                entry_score += 0.5 if int(touch_delta) <= 2 else (0.25 if int(touch_delta) <= int(p.x_touch) else 0.0)
            entry_score += min(max(float(breakout_atr), 0.0), 1.0) * 0.5

            if entry_reason == "E1":
                entry_score += min(max(float(e1_break_strength_atr), 0.0), 2.0) / 2.0 * 0.9
                entry_score += max(0.0, 1.0 - min(max(float(e1_retest_depth_atr), 0.0), 2.0) / 2.0) * 0.7
                if int(p.m_retest) > 0:
                    entry_score += max(0.0, 1.0 - min(float(e1_retest_bars), float(p.m_retest)) / float(p.m_retest)) * 0.6
                    entry_score += max(0.0, 1.0 - min(float(e1_touch_bars), float(p.m_retest)) / float(p.m_retest)) * 0.3
                entry_score += max(0.0, min(float(e1_atr_ratio) - 1.0, 0.5)) / 0.5 * 0.4
                if _E1_ADX_SCORE_ENABLED and (not pd.isna(adx14_v)):
                    if float(adx14_v) >= 25.0:
                        entry_score += 0.3
                    elif float(adx14_v) < 15.0:
                        entry_score -= 0.2

            ema13_4h = float(ema13_4h_arr[i])
            ema55_4h = float(ema55_4h_arr[i])
            close_4h = float(close_4h_arr[i])
            ema144_4h = float(ema144_4h_arr[i])
            if (not pd.isna(ema13_4h)) and (not pd.isna(ema55_4h)) and a > 0:
                align = (ema13_4h - ema55_4h) / a if entry_side == 1 else (ema55_4h - ema13_4h) / a
                entry_score += max(0.0, min(float(align), 3.0)) / 3.0 * 0.9
            if (not pd.isna(close_4h)) and (not pd.isna(ema144_4h)) and a > 0:
                reg_dist = (close_4h - ema144_4h) / a if entry_side == 1 else (ema144_4h - close_4h) / a
                entry_score += max(0.0, min(float(reg_dist), 6.0)) / 6.0 * 0.5

            kk4 = float(kd_k_4h_arr[i])
            kd4 = float(kd_d_4h_arr[i])
            kk1 = float(kd_k_1d_arr[i])
            kd1 = float(kd_d_1d_arr[i])
            if (not pd.isna(kk4)) and (not pd.isna(kd4)) and (not pd.isna(kk1)) and (not pd.isna(kd1)):
                mom = ((kk4 - kd4) + (kk1 - kd1)) / 40.0
                if entry_side == -1:
                    mom = -mom
                entry_score += max(0.0, min(float(mom), 1.0)) * 0.7

            if entry_reason == "E1":
                squeeze = bool(bb_squeeze_4h_arr[i])
                if bool(p.enable_e1_bb_squeeze_veto) and squeeze:
                    continue
                if squeeze:
                    entry_score -= float(p.e1_bb_squeeze_penalty)

                if float(p.e1_min_break_strength_atr) > 0 and float(e1_break_strength_atr) < float(p.e1_min_break_strength_atr):
                    frac = (float(p.e1_min_break_strength_atr) - float(e1_break_strength_atr)) / float(p.e1_min_break_strength_atr)
                    entry_score -= min(max(float(frac), 0.0), 1.0) * 0.6
                if float(p.e1_max_retest_depth_atr) > 0 and float(e1_retest_depth_atr) > float(p.e1_max_retest_depth_atr):
                    frac = (float(e1_retest_depth_atr) - float(p.e1_max_retest_depth_atr)) / float(p.e1_max_retest_depth_atr)
                    entry_score -= min(max(float(frac), 0.0), 1.0) * 0.6

            score_filter_th = float("nan")
            score_filter_pass = True
            if bool(p.enable_score_filter):
                th = float(p.min_score_to_trade)
                if entry_reason == "E1":
                    th = float(p.min_score_to_trade_e1)
                elif entry_reason == "E2":
                    th = float(p.min_score_to_trade_e2)
                score_filter_th = float(th)
                score_filter_pass = bool(float(entry_score) >= float(th))
                if not score_filter_pass:
                    continue

            entry_score_gate_max_v = float(_ENTRY_SCORE_MAX) if _ENTRY_SCORE_MAX is not None else float("nan")
            entry_score_gate_action_v = str(_ENTRY_SCORE_ACTION)
            entry_score_gate_scope_v = str(_ENTRY_SCORE_SCOPE)
            entry_score_gate_hit_v = bool(False)
            entry_score_gate_blocked_v = bool(False)
            entry_score_gate_dyn_v = float("nan")
            if (
                _ENTRY_SCORE_VOL_MODE == "atr_rel_bins"
                and _ENTRY_SCORE_VOL_ATR_REL_CUTS is not None
                and _ENTRY_SCORE_VOL_MAXES is not None
                and float(cl) > 0
                and float(a) > 0
            ):
                atr_rel_px = float(a) / float(cl)
                if np.isfinite(atr_rel_px):
                    c1, c2 = _ENTRY_SCORE_VOL_ATR_REL_CUTS
                    m0, m1, m2 = _ENTRY_SCORE_VOL_MAXES
                    if float(atr_rel_px) < float(c1):
                        entry_score_gate_dyn_v = float(m0)
                    elif float(atr_rel_px) < float(c2):
                        entry_score_gate_dyn_v = float(m1)
                    else:
                        entry_score_gate_dyn_v = float(m2)
            max_use = entry_score_gate_dyn_v if np.isfinite(entry_score_gate_dyn_v) else float(entry_score_gate_max_v)
            entry_score_gate_max_v = float(max_use) if np.isfinite(max_use) else float("nan")
            if _ENTRY_SCORE_ACTION != "off" and np.isfinite(entry_score_gate_max_v) and float(entry_score_gate_max_v) > 0:
                if _ENTRY_SCORE_SCOPE == "all" or (_ENTRY_SCORE_SCOPE == "e2" and entry_reason == "E2"):
                    entry_score_gate_hit_v = bool(float(entry_score) > float(entry_score_gate_max_v))
                    entry_score_gate_blocked_v = bool(entry_score_gate_hit_v and _ENTRY_SCORE_ACTION in {"block", "drop"})
                    if entry_score_gate_hit_v and _ENTRY_SCORE_ACTION == "drop":
                        continue

            stop_k_use = float(p.stop_k_e1) if entry_reason == "E1" else float(p.stop_k)
            tick_volume_v = float(tv_arr[i]) if (i < len(tv_arr) and np.isfinite(tv_arr[i])) else float("nan")
            vol_sma20_v = _sma_last(tv_arr, 20, i)
            vol_ratio_v = float(tick_volume_v / vol_sma20_v) if (np.isfinite(tick_volume_v) and vol_sma20_v > 0) else float("nan")
            vol_pct_v = _pct_rank(tv_arr, 200, i)
            atr_sma50_v = _sma_last(atr_arr, 50, i)
            atr_rel_v = float(a / atr_sma50_v) if (atr_sma50_v > 0) else float("nan")
            atr_pct_v = _pct_rank(atr_arr, 200, i)
            vol_risk_ratio_max_v = float(_VOL_RISK_VOL_RATIO_MAX) if _VOL_RISK_VOL_RATIO_MAX is not None else float("nan")
            vol_risk_pct_max_v = float(_VOL_RISK_VOL_PCT_MAX) if _VOL_RISK_VOL_PCT_MAX is not None else float("nan")
            vol_risk_action_v = str(_VOL_RISK_ACTION)
            vol_risk_hit_v = bool(
                (np.isfinite(vol_ratio_v) and np.isfinite(vol_risk_ratio_max_v) and float(vol_ratio_v) > float(vol_risk_ratio_max_v))
                or (np.isfinite(vol_pct_v) and np.isfinite(vol_risk_pct_max_v) and float(vol_pct_v) > float(vol_risk_pct_max_v))
            )
            vol_risk_blocked_v = bool(vol_risk_hit_v and vol_risk_action_v in {"block", "drop"})
            if vol_risk_hit_v and vol_risk_action_v == "drop":
                continue
            stop = cl - stop_k_use * a if entry_side == 1 else cl + stop_k_use * a
            side_s = "LONG" if entry_side == 1 else "SHORT"
            breakout_level = float(level_long_arr[i]) if entry_side == 1 else float(level_short_arr[i])
            td = int(touch_delta) if touch_delta is not None else 0
            sr_support_v, sr_resistance_v, sr_sup_dist_atr_v, sr_res_dist_atr_v, sr_sup_t_v, sr_res_t_v = _sr_nearest_levels(
                h_arr,
                l_arr,
                float(cl),
                float(a),
                int(i),
                lookback=200,
                pivot=3,
                cluster_atr=0.25,
            )
            jg_macd_up_v = bool(jg_macd_up_arr[i]) if i < len(jg_macd_up_arr) else False
            jg_macd_down_v = bool(jg_macd_down_arr[i]) if i < len(jg_macd_down_arr) else False
            jg_sma175_v = float(jg_sma175_arr[i]) if (i < len(jg_sma175_arr) and np.isfinite(jg_sma175_arr[i])) else float("nan")
            jg_j_v = float(jg_j_arr[i]) if (i < len(jg_j_arr) and np.isfinite(jg_j_arr[i])) else float("nan")
            jg_long_v = bool(jg_macd_up_v and np.isfinite(jg_sma175_v) and float(cl) > float(jg_sma175_v) and np.isfinite(jg_j_v) and float(jg_j_v) < 80.0)
            jg_short_v = bool(jg_macd_down_v and np.isfinite(jg_sma175_v) and float(cl) < float(jg_sma175_v) and np.isfinite(jg_j_v) and float(jg_j_v) > 20.0)
            sigs.append(
                EntrySignal(
                    ts=str(idx[i]),
                    symbol=sym_u,
                    side=side_s,
                    signal=str(entry_reason),
                    entry=float(cl),
                    stop=float(stop),
                    atr=float(a),
                    entry_score=float(entry_score),
                    ema21_1h=float(ema21_1h),
                    breakout_level=float(breakout_level),
                    touch_delta=td,
                    strong=bool(strong_long if entry_side == 1 else strong_short),
                kd_w1_long=bool(kd_w1_long_arr[i]),
                kd_w1_short=bool(kd_w1_short_arr[i]),
                kd_3line_long=bool(kd_3line_long_arr[i]),
                kd_3line_short=bool(kd_3line_short_arr[i]),
                cci144=float(cci144_v) if not pd.isna(cci144_v) else float("nan"),
                cci_veto=False,
                adx14=float(adx14_v) if not pd.isna(adx14_v) else float("nan"),
                chase_dist_atr=float(chase_dist_atr),
                score_filter_th=float(score_filter_th) if not pd.isna(score_filter_th) else float("nan"),
                score_filter_pass=bool(score_filter_pass),
                entry_score_gate_max=float(entry_score_gate_max_v) if np.isfinite(entry_score_gate_max_v) else float("nan"),
                entry_score_gate_action=str(entry_score_gate_action_v),
                entry_score_gate_scope=str(entry_score_gate_scope_v),
                entry_score_gate_hit=bool(entry_score_gate_hit_v),
                entry_score_gate_blocked=bool(entry_score_gate_blocked_v),
                e2_chase_max_atr=float("nan"),
                e2_chase_blocked=bool(False),
                e2_chase_action=str(""),
                tick_volume=float(tick_volume_v) if np.isfinite(tick_volume_v) else float("nan"),
                vol_sma20=float(vol_sma20_v) if np.isfinite(vol_sma20_v) else float("nan"),
                vol_ratio=float(vol_ratio_v) if np.isfinite(vol_ratio_v) else float("nan"),
                vol_pct=float(vol_pct_v) if np.isfinite(vol_pct_v) else float("nan"),
                atr_sma50=float(atr_sma50_v) if np.isfinite(atr_sma50_v) else float("nan"),
                atr_rel=float(atr_rel_v) if np.isfinite(atr_rel_v) else float("nan"),
                atr_pct=float(atr_pct_v) if np.isfinite(atr_pct_v) else float("nan"),
                spread_px=float("nan"),
                spread_rel=float("nan"),
                liquidity_gate_enabled=bool(False),
                liquidity_max_spread_rel=float("nan"),
                liquidity_risk=bool(False),
                vol_risk_vol_ratio_max=float(vol_risk_ratio_max_v) if np.isfinite(vol_risk_ratio_max_v) else float("nan"),
                vol_risk_vol_pct_max=float(vol_risk_pct_max_v) if np.isfinite(vol_risk_pct_max_v) else float("nan"),
                vol_risk_action=str(vol_risk_action_v),
                vol_risk_blocked=bool(vol_risk_blocked_v),
                sr_support=float(sr_support_v) if np.isfinite(sr_support_v) else float("nan"),
                sr_resistance=float(sr_resistance_v) if np.isfinite(sr_resistance_v) else float("nan"),
                sr_support_dist_atr=float(sr_sup_dist_atr_v) if np.isfinite(sr_sup_dist_atr_v) else float("nan"),
                sr_resistance_dist_atr=float(sr_res_dist_atr_v) if np.isfinite(sr_res_dist_atr_v) else float("nan"),
                sr_support_touches=int(sr_sup_t_v),
                sr_resistance_touches=int(sr_res_t_v),
                jg_macd_up=bool(jg_macd_up_v),
                jg_macd_down=bool(jg_macd_down_v),
                jg_sma175=float(jg_sma175_v) if np.isfinite(jg_sma175_v) else float("nan"),
                jg_j=float(jg_j_v) if np.isfinite(jg_j_v) else float("nan"),
                jg_long=bool(jg_long_v),
                jg_short=bool(jg_short_v),
                jg_ma13=float(jg_ma13_arr[i]) if (i < len(jg_ma13_arr) and np.isfinite(jg_ma13_arr[i])) else float("nan"),
                jg_ma55=float(jg_ma55_arr[i]) if (i < len(jg_ma55_arr) and np.isfinite(jg_ma55_arr[i])) else float("nan"),
                jg_ema20=float(jg_ema20_arr[i]) if (i < len(jg_ema20_arr) and np.isfinite(jg_ema20_arr[i])) else float("nan"),
                jg_ema27=float(jg_ema27_arr[i]) if (i < len(jg_ema27_arr) and np.isfinite(jg_ema27_arr[i])) else float("nan"),
                jg_ema29=float(jg_ema29_arr[i]) if (i < len(jg_ema29_arr) and np.isfinite(jg_ema29_arr[i])) else float("nan"),
                jg_ema32=float(jg_ema32_arr[i]) if (i < len(jg_ema32_arr) and np.isfinite(jg_ema32_arr[i])) else float("nan"),
                jg_ema36=float(jg_ema36_arr[i]) if (i < len(jg_ema36_arr) and np.isfinite(jg_ema36_arr[i])) else float("nan"),
                jg_pivot_mid=float(jg_pivot_mid_arr[i]) if (i < len(jg_pivot_mid_arr) and np.isfinite(jg_pivot_mid_arr[i])) else float("nan"),
                jg_b3=float(jg_b3_arr[i]) if (i < len(jg_b3_arr) and np.isfinite(jg_b3_arr[i])) else float("nan"),
                jg_s3=float(jg_s3_arr[i]) if (i < len(jg_s3_arr) and np.isfinite(jg_s3_arr[i])) else float("nan"),
                jg_b5=float(jg_b5_arr[i]) if (i < len(jg_b5_arr) and np.isfinite(jg_b5_arr[i])) else float("nan"),
                jg_s5=float(jg_s5_arr[i]) if (i < len(jg_s5_arr) and np.isfinite(jg_s5_arr[i])) else float("nan"),
                jg_var2=float(jg_var2_arr[i]) if (i < len(jg_var2_arr) and np.isfinite(jg_var2_arr[i])) else float("nan"),
                jg_var3=float(jg_var3_arr[i]) if (i < len(jg_var3_arr) and np.isfinite(jg_var3_arr[i])) else float("nan"),
                jg_var3_ma6=float(jg_var3_ma6_arr[i]) if (i < len(jg_var3_ma6_arr) and np.isfinite(jg_var3_ma6_arr[i])) else float("nan"),
                jg_bar_yellow=bool(jg_bar_yellow_arr[i]) if (i < len(jg_bar_yellow_arr)) else False,
                jg_bar_red=bool(jg_bar_red_arr[i]) if (i < len(jg_bar_red_arr)) else False,
                jg_macd=float(jg_macd_arr[i]) if (i < len(jg_macd_arr) and np.isfinite(jg_macd_arr[i])) else float("nan"),
                jg_buy=bool(jg_buy_arr[i]) if (i < len(jg_buy_arr)) else False,
                jg_sell=bool(jg_sell_arr[i]) if (i < len(jg_sell_arr)) else False,
                jg_gold=bool(jg_gold_arr[i]) if (i < len(jg_gold_arr)) else False,
                jg_ma160=float(jg_ma160_arr[i]) if (i < len(jg_ma160_arr) and np.isfinite(jg_ma160_arr[i])) else float("nan"),
                jg_ma120=float(jg_ma120_arr[i]) if (i < len(jg_ma120_arr) and np.isfinite(jg_ma120_arr[i])) else float("nan"),
                jg_ma60=float(jg_ma60_arr[i]) if (i < len(jg_ma60_arr) and np.isfinite(jg_ma60_arr[i])) else float("nan"),
                jg_ma25=float(jg_ma25_arr[i]) if (i < len(jg_ma25_arr) and np.isfinite(jg_ma25_arr[i])) else float("nan"),
                jg_flip_to_yellow=bool(jg_flip_to_yellow_arr[i]) if (i < len(jg_flip_to_yellow_arr)) else False,
                jg_flip_to_red=bool(jg_flip_to_red_arr[i]) if (i < len(jg_flip_to_red_arr)) else False,
                jg_wick_touch_ma13=bool(jg_wick_touch_ma13_arr[i]) if (i < len(jg_wick_touch_ma13_arr)) else False,
                jg_wick_touch_ma55=bool(jg_wick_touch_ma55_arr[i]) if (i < len(jg_wick_touch_ma55_arr)) else False,
                jg_wick_touch_ema27=bool(jg_wick_touch_ema27_arr[i]) if (i < len(jg_wick_touch_ema27_arr)) else False,
                jg_wick_touch_ema29=bool(jg_wick_touch_ema29_arr[i]) if (i < len(jg_wick_touch_ema29_arr)) else False,
                jg_wick_touch_ema32=bool(jg_wick_touch_ema32_arr[i]) if (i < len(jg_wick_touch_ema32_arr)) else False,
                jg_wick_touch_ema36=bool(jg_wick_touch_ema36_arr[i]) if (i < len(jg_wick_touch_ema36_arr)) else False,
                jg_close_breakdown_ma13=bool(jg_close_breakdown_ma13_arr[i]) if (i < len(jg_close_breakdown_ma13_arr)) else False,
                jg_close_breakup_ma13=bool(jg_close_breakup_ma13_arr[i]) if (i < len(jg_close_breakup_ma13_arr)) else False,
                jg_close_breakdown_ma55=bool(jg_close_breakdown_ma55_arr[i]) if (i < len(jg_close_breakdown_ma55_arr)) else False,
                jg_close_breakup_ma55=bool(jg_close_breakup_ma55_arr[i]) if (i < len(jg_close_breakup_ma55_arr)) else False,
                jg_cross_ma13_ema27_up=bool(jg_cross_ma13_ema27_up_arr[i]) if (i < len(jg_cross_ma13_ema27_up_arr)) else False,
                jg_cross_ma13_ema27_down=bool(jg_cross_ma13_ema27_down_arr[i]) if (i < len(jg_cross_ma13_ema27_down_arr)) else False,
                jg_cross_ma13_ema29_up=bool(jg_cross_ma13_ema29_up_arr[i]) if (i < len(jg_cross_ma13_ema29_up_arr)) else False,
                jg_cross_ma13_ema29_down=bool(jg_cross_ma13_ema29_down_arr[i]) if (i < len(jg_cross_ma13_ema29_down_arr)) else False,
                jg_cross_ma13_ema32_up=bool(jg_cross_ma13_ema32_up_arr[i]) if (i < len(jg_cross_ma13_ema32_up_arr)) else False,
                jg_cross_ma13_ema32_down=bool(jg_cross_ma13_ema32_down_arr[i]) if (i < len(jg_cross_ma13_ema32_down_arr)) else False,
                jg_cross_ma13_ema36_up=bool(jg_cross_ma13_ema36_up_arr[i]) if (i < len(jg_cross_ma13_ema36_up_arr)) else False,
                jg_cross_ma13_ema36_down=bool(jg_cross_ma13_ema36_down_arr[i]) if (i < len(jg_cross_ma13_ema36_down_arr)) else False,
                jg_after_cross_ma13_ema27_up_j_lt80=bool(jg_after_cross_ma13_ema27_up_j_lt80_arr[i]) if (i < len(jg_after_cross_ma13_ema27_up_j_lt80_arr)) else False,
                jg_after_cross_ma13_ema27_down_j_gt20=bool(jg_after_cross_ma13_ema27_down_j_gt20_arr[i]) if (i < len(jg_after_cross_ma13_ema27_down_j_gt20_arr)) else False,
                jg_dist_b3_atr=float(jg_dist_b3_atr_arr[i]) if (i < len(jg_dist_b3_atr_arr) and np.isfinite(jg_dist_b3_atr_arr[i])) else float("nan"),
                jg_dist_s3_atr=float(jg_dist_s3_atr_arr[i]) if (i < len(jg_dist_s3_atr_arr) and np.isfinite(jg_dist_s3_atr_arr[i])) else float("nan"),
                jg_dist_pivot_atr=float(jg_dist_pivot_atr_arr[i]) if (i < len(jg_dist_pivot_atr_arr) and np.isfinite(jg_dist_pivot_atr_arr[i])) else float("nan"),
                jg_red_streak=int(jg_red_streak_arr[i]) if (i < len(jg_red_streak_arr)) else 0,
                jg_yellow_streak=int(jg_yellow_streak_arr[i]) if (i < len(jg_yellow_streak_arr)) else 0,
                )
            )
    if include_bobby_signals:
        sl_atr = float(bobby_sl_atr)
        if not (sl_atr > 0):
            sl_atr = 1.0
        for i in range(len(df1)):
            cl = float(c_arr[i])
            a = float(atr_arr[i])
            if not (np.isfinite(cl) and np.isfinite(a) and a > 0):
                continue
            ema21_1h = float(ema21_1h_arr[i]) if (i < len(ema21_1h_arr) and np.isfinite(ema21_1h_arr[i])) else float("nan")
            chase_dist_atr = float(abs(float(cl) - float(ema21_1h)) / float(a)) if (np.isfinite(ema21_1h) and a > 0) else float("inf")

            def _emit(sig_name: str, side_s: str) -> None:
                is_long = side_s == "LONG"
                stop = float(cl - sl_atr * a) if is_long else float(cl + sl_atr * a)
                if not np.isfinite(stop):
                    return
                sigs.append(
                    EntrySignal(
                        ts=str(idx[i]),
                        symbol=sym_u,
                        side=side_s,
                        signal=str(sig_name),
                        entry=float(cl),
                        stop=float(stop),
                        atr=float(a),
                        entry_score=0.0,
                        ema21_1h=float(ema21_1h) if np.isfinite(ema21_1h) else float("nan"),
                        breakout_level=float("nan"),
                        touch_delta=0,
                        strong=bool(strong_long_arr[i]) if is_long and (i < len(strong_long_arr)) else (bool(strong_short_arr[i]) if (i < len(strong_short_arr)) else False),
                        kd_w1_long=bool(kd_w1_long_arr[i]) if (i < len(kd_w1_long_arr)) else False,
                        kd_w1_short=bool(kd_w1_short_arr[i]) if (i < len(kd_w1_short_arr)) else False,
                        kd_3line_long=bool(kd_3line_long_arr[i]) if (i < len(kd_3line_long_arr)) else False,
                        kd_3line_short=bool(kd_3line_short_arr[i]) if (i < len(kd_3line_short_arr)) else False,
                        chase_dist_atr=float(chase_dist_atr),
                        tick_volume=float(tv_arr[i]) if (i < len(tv_arr) and np.isfinite(tv_arr[i])) else float("nan"),
                        jg_j=float(jg_j_arr[i]) if (i < len(jg_j_arr) and np.isfinite(jg_j_arr[i])) else float("nan"),
                        jg_ma13=float(jg_ma13_arr[i]) if (i < len(jg_ma13_arr) and np.isfinite(jg_ma13_arr[i])) else float("nan"),
                        jg_ma55=float(jg_ma55_arr[i]) if (i < len(jg_ma55_arr) and np.isfinite(jg_ma55_arr[i])) else float("nan"),
                        jg_bar_red=bool(jg_bar_red_arr[i]) if (i < len(jg_bar_red_arr)) else False,
                        jg_bar_yellow=bool(jg_bar_yellow_arr[i]) if (i < len(jg_bar_yellow_arr)) else False,
                        jg_flip_to_red=bool(jg_flip_to_red_arr[i]) if (i < len(jg_flip_to_red_arr)) else False,
                        jg_flip_to_yellow=bool(jg_flip_to_yellow_arr[i]) if (i < len(jg_flip_to_yellow_arr)) else False,
                        jg_buy=bool(jg_buy_arr[i]) if (i < len(jg_buy_arr)) else False,
                        jg_sell=bool(jg_sell_arr[i]) if (i < len(jg_sell_arr)) else False,
                        jg_gold=bool(jg_gold_arr[i]) if (i < len(jg_gold_arr)) else False,
                        jg_wick_touch_ma13=bool(jg_wick_touch_ma13_arr[i]) if (i < len(jg_wick_touch_ma13_arr)) else False,
                        jg_wick_touch_ema27=bool(jg_wick_touch_ema27_arr[i]) if (i < len(jg_wick_touch_ema27_arr)) else False,
                        jg_close_breakdown_ma13=bool(jg_close_breakdown_ma13_arr[i]) if (i < len(jg_close_breakdown_ma13_arr)) else False,
                        jg_close_breakup_ma13=bool(jg_close_breakup_ma13_arr[i]) if (i < len(jg_close_breakup_ma13_arr)) else False,
                    )
                )

            if bool(jg_buy_arr[i]):
                _emit("B_BUY", "LONG")
            if bool(jg_gold_arr[i]):
                _emit("B_GOLD", "LONG")
            if bool(jg_sell_arr[i]):
                _emit("B_SELL", "SHORT")
    return sigs


def _paper_scan(args: Dict[str, Any], p: Params) -> Path:
    dt_from_s = str(args.get("paper_from") or "").strip()
    dt_to_s = str(args.get("paper_to") or "").strip()
    if not dt_from_s or not dt_to_s:
        raise ValueError("paper-scan requires --paper-from and --paper-to")
    dt_from = pd.to_datetime(dt_from_s).to_pydatetime()
    dt_to = pd.to_datetime(dt_to_s).to_pydatetime()
    if dt_to <= dt_from:
        raise ValueError("paper-to must be after paper-from")

    syms_raw = str(args.get("paper_symbols") or "").strip()
    if syms_raw:
        syms = [x.strip().upper() for x in syms_raw.split(",") if x.strip()]
        pool_df = None
    else:
        pool = str(args.get("pool") or "core").strip().lower()
        if pool in {"core", "observe", "exclude"}:
            dfp = _read_deploy_pool_df(pool)
            syms = [str(x).upper() for x in dfp["symbol"].tolist()] if dfp is not None and "symbol" in dfp.columns else []
            pool_df = dfp
        elif pool in {"all", "*"}:
            dfc = _read_deploy_pool_df("core")
            dfo = _read_deploy_pool_df("observe")
            syms = []
            if dfc is not None and "symbol" in dfc.columns:
                syms += [str(x).upper() for x in dfc["symbol"].tolist()]
            if dfo is not None and "symbol" in dfo.columns:
                syms += [str(x).upper() for x in dfo["symbol"].tolist()]
            syms = list(dict.fromkeys(syms))
            pool_df = _merge_pool_dfs(["core", "observe"])
        else:
            raise ValueError("paper-scan: unknown pool; use --paper-symbols or --pool core|observe|exclude|all")
    if not syms:
        raise ValueError("paper-scan: empty symbols (use --paper-symbols or ensure deploy pool has symbols)")

    base = Path(str(args.get("log_dir") or DEFAULT_LOG_DIR))
    out_dir = base / dt_to.strftime("%Y-%m-%d")
    private_names = bool(int(args.get("private_names", 0) or 0))
    ss_map = _symbol_settings_map(pool_df)
    warm_h1 = timedelta(days=30)
    warm_h4 = timedelta(days=120)
    warm_d1 = timedelta(days=500)

    rows: List[Dict[str, object]] = []
    include_bobby_signals = bool(int(args.get("paper_bobby_signals") or 0) != 0)
    bobby_sl_atr = float(args.get("paper_bobby_sl_atr") or 1.0)
    if not (bobby_sl_atr > 0):
        bobby_sl_atr = 1.0
    for sym0 in syms:
        p_sym = _params_for_symbol(p, ss_map.get(str(sym0).strip().upper()))
        sym = _resolve_symbol(sym0)
        _ensure_symbol_ready(sym)
        df1 = _mt5_rates_range_local(sym, mt5.TIMEFRAME_H1, dt_from - warm_h1, dt_to + timedelta(days=2))
        df4 = _mt5_rates_range_local(sym, mt5.TIMEFRAME_H4, dt_from - warm_h4, dt_to + timedelta(days=5))
        dfd = _mt5_rates_range_local(sym, mt5.TIMEFRAME_D1, dt_from - warm_d1, dt_to + timedelta(days=10))
        df1 = df1[(df1.index >= dt_from) & (df1.index <= dt_to)].copy()
        if df1.empty:
            continue
        sigs = _scan_entry_signals_from_dfs(
            sym,
            df1=df1,
            df4=df4,
            dfd=dfd,
            p=p_sym,
            include_bobby_signals=include_bobby_signals,
            bobby_sl_atr=bobby_sl_atr,
        )
        for e in sigs:
            try:
                t = pd.to_datetime(str(e.ts), errors="coerce")
            except Exception:
                t = pd.NaT
            if pd.isna(t):
                continue
            if t < pd.to_datetime(dt_from) or t > pd.to_datetime(dt_to):
                continue
            rows.append(
                _apply_private_names(
                    {
                    "ts_utc": _now_utc_iso(),
                    "sig_ts": str(e.ts),
                    "symbol": e.symbol,
                    "side": e.side,
                    "signal": e.signal,
                    "entry": float(e.entry),
                    "stop": float(e.stop),
                    "atr": float(e.atr),
                    "entry_score": float(e.entry_score),
                    "ema21_1h": float(e.ema21_1h),
                    "breakout_level": float(e.breakout_level) if not pd.isna(e.breakout_level) else np.nan,
                    "touch_delta": int(e.touch_delta),
                    "strong": bool(e.strong),
                    "kd_w1_long": bool(e.kd_w1_long),
                    "kd_w1_short": bool(e.kd_w1_short),
                    "kd_3line_long": bool(e.kd_3line_long),
                    "kd_3line_short": bool(e.kd_3line_short),
                    "cci144": float(e.cci144) if not pd.isna(e.cci144) else np.nan,
                    "adx14": float(e.adx14) if not pd.isna(e.adx14) else np.nan,
                    "chase_dist_atr": float(e.chase_dist_atr) if not pd.isna(e.chase_dist_atr) else np.nan,
                    "score_filter_th": float(e.score_filter_th) if not pd.isna(e.score_filter_th) else np.nan,
                    "score_filter_pass": bool(e.score_filter_pass),
                    "entry_score_gate_max": float(e.entry_score_gate_max) if not pd.isna(e.entry_score_gate_max) else np.nan,
                    "entry_score_gate_action": str(e.entry_score_gate_action),
                    "entry_score_gate_scope": str(e.entry_score_gate_scope),
                    "entry_score_gate_hit": bool(e.entry_score_gate_hit),
                    "entry_score_gate_blocked": bool(e.entry_score_gate_blocked),
                    "tick_volume": float(e.tick_volume) if not pd.isna(e.tick_volume) else np.nan,
                    "vol_sma20": float(e.vol_sma20) if not pd.isna(e.vol_sma20) else np.nan,
                    "vol_ratio": float(e.vol_ratio) if not pd.isna(e.vol_ratio) else np.nan,
                    "vol_pct": float(e.vol_pct) if not pd.isna(e.vol_pct) else np.nan,
                    "atr_sma50": float(e.atr_sma50) if not pd.isna(e.atr_sma50) else np.nan,
                    "atr_rel": float(e.atr_rel) if not pd.isna(e.atr_rel) else np.nan,
                    "atr_pct": float(e.atr_pct) if not pd.isna(e.atr_pct) else np.nan,
                    "spread_rel": float(e.spread_rel) if not pd.isna(e.spread_rel) else np.nan,
                    "liquidity_risk": bool(e.liquidity_risk),
                    "vol_risk_vol_ratio_max": float(e.vol_risk_vol_ratio_max) if not pd.isna(e.vol_risk_vol_ratio_max) else np.nan,
                    "vol_risk_vol_pct_max": float(e.vol_risk_vol_pct_max) if not pd.isna(e.vol_risk_vol_pct_max) else np.nan,
                    "vol_risk_action": str(e.vol_risk_action),
                    "vol_risk_blocked": bool(e.vol_risk_blocked),
                    "sr_support": float(e.sr_support) if not pd.isna(e.sr_support) else np.nan,
                    "sr_resistance": float(e.sr_resistance) if not pd.isna(e.sr_resistance) else np.nan,
                    "sr_support_dist_atr": float(e.sr_support_dist_atr) if not pd.isna(e.sr_support_dist_atr) else np.nan,
                    "sr_resistance_dist_atr": float(e.sr_resistance_dist_atr) if not pd.isna(e.sr_resistance_dist_atr) else np.nan,
                    "sr_support_touches": int(e.sr_support_touches),
                    "sr_resistance_touches": int(e.sr_resistance_touches),
                    "jg_macd_up": bool(e.jg_macd_up),
                    "jg_macd_down": bool(e.jg_macd_down),
                    "jg_sma175": float(e.jg_sma175) if not pd.isna(e.jg_sma175) else np.nan,
                    "jg_j": float(e.jg_j) if not pd.isna(e.jg_j) else np.nan,
                    "jg_long": bool(e.jg_long),
                    "jg_short": bool(e.jg_short),
                    "jg_ma13": float(e.jg_ma13) if not pd.isna(e.jg_ma13) else np.nan,
                    "jg_ma55": float(e.jg_ma55) if not pd.isna(e.jg_ma55) else np.nan,
                    "jg_ema20": float(e.jg_ema20) if not pd.isna(e.jg_ema20) else np.nan,
                    "jg_ema27": float(e.jg_ema27) if not pd.isna(e.jg_ema27) else np.nan,
                    "jg_ema29": float(e.jg_ema29) if not pd.isna(e.jg_ema29) else np.nan,
                    "jg_ema32": float(e.jg_ema32) if not pd.isna(e.jg_ema32) else np.nan,
                    "jg_ema36": float(e.jg_ema36) if not pd.isna(e.jg_ema36) else np.nan,
                    "jg_pivot_mid": float(e.jg_pivot_mid) if not pd.isna(e.jg_pivot_mid) else np.nan,
                    "jg_b3": float(e.jg_b3) if not pd.isna(e.jg_b3) else np.nan,
                    "jg_s3": float(e.jg_s3) if not pd.isna(e.jg_s3) else np.nan,
                    "jg_b5": float(e.jg_b5) if not pd.isna(e.jg_b5) else np.nan,
                    "jg_s5": float(e.jg_s5) if not pd.isna(e.jg_s5) else np.nan,
                    "jg_var2": float(e.jg_var2) if not pd.isna(e.jg_var2) else np.nan,
                    "jg_var3": float(e.jg_var3) if not pd.isna(e.jg_var3) else np.nan,
                    "jg_var3_ma6": float(e.jg_var3_ma6) if not pd.isna(e.jg_var3_ma6) else np.nan,
                    "jg_bar_yellow": bool(e.jg_bar_yellow),
                    "jg_bar_red": bool(e.jg_bar_red),
                    "jg_macd": float(e.jg_macd) if not pd.isna(e.jg_macd) else np.nan,
                    "jg_buy": bool(e.jg_buy),
                    "jg_sell": bool(e.jg_sell),
                    "jg_gold": bool(e.jg_gold),
                    "jg_ma160": float(e.jg_ma160) if not pd.isna(e.jg_ma160) else np.nan,
                    "jg_ma120": float(e.jg_ma120) if not pd.isna(e.jg_ma120) else np.nan,
                    "jg_ma60": float(e.jg_ma60) if not pd.isna(e.jg_ma60) else np.nan,
                    "jg_ma25": float(e.jg_ma25) if not pd.isna(e.jg_ma25) else np.nan,
                    "jg_flip_to_yellow": bool(e.jg_flip_to_yellow),
                    "jg_flip_to_red": bool(e.jg_flip_to_red),
                    "jg_wick_touch_ma13": bool(e.jg_wick_touch_ma13),
                    "jg_wick_touch_ma55": bool(e.jg_wick_touch_ma55),
                    "jg_wick_touch_ema27": bool(e.jg_wick_touch_ema27),
                    "jg_wick_touch_ema29": bool(e.jg_wick_touch_ema29),
                    "jg_wick_touch_ema32": bool(e.jg_wick_touch_ema32),
                    "jg_wick_touch_ema36": bool(e.jg_wick_touch_ema36),
                    "jg_close_breakdown_ma13": bool(e.jg_close_breakdown_ma13),
                    "jg_close_breakup_ma13": bool(e.jg_close_breakup_ma13),
                    "jg_close_breakdown_ma55": bool(e.jg_close_breakdown_ma55),
                    "jg_close_breakup_ma55": bool(e.jg_close_breakup_ma55),
                    "jg_cross_ma13_ema27_up": bool(e.jg_cross_ma13_ema27_up),
                    "jg_cross_ma13_ema27_down": bool(e.jg_cross_ma13_ema27_down),
                    "jg_cross_ma13_ema29_up": bool(e.jg_cross_ma13_ema29_up),
                    "jg_cross_ma13_ema29_down": bool(e.jg_cross_ma13_ema29_down),
                    "jg_cross_ma13_ema32_up": bool(e.jg_cross_ma13_ema32_up),
                    "jg_cross_ma13_ema32_down": bool(e.jg_cross_ma13_ema32_down),
                    "jg_cross_ma13_ema36_up": bool(e.jg_cross_ma13_ema36_up),
                    "jg_cross_ma13_ema36_down": bool(e.jg_cross_ma13_ema36_down),
                    "jg_after_cross_ma13_ema27_up_j_lt80": bool(e.jg_after_cross_ma13_ema27_up_j_lt80),
                    "jg_after_cross_ma13_ema27_down_j_gt20": bool(e.jg_after_cross_ma13_ema27_down_j_gt20),
                    "jg_dist_b3_atr": float(e.jg_dist_b3_atr) if not pd.isna(e.jg_dist_b3_atr) else np.nan,
                    "jg_dist_s3_atr": float(e.jg_dist_s3_atr) if not pd.isna(e.jg_dist_s3_atr) else np.nan,
                    "jg_dist_pivot_atr": float(e.jg_dist_pivot_atr) if not pd.isna(e.jg_dist_pivot_atr) else np.nan,
                    "jg_red_streak": int(e.jg_red_streak),
                    "jg_yellow_streak": int(e.jg_yellow_streak),
                    "ma13_ma55_gap_atr": (
                        float(abs(float(e.jg_ma13) - float(e.jg_ma55)) / float(e.atr))
                        if (not pd.isna(e.atr) and float(e.atr) > 0 and not pd.isna(e.jg_ma13) and not pd.isna(e.jg_ma55))
                        else np.nan
                    ),
                    "pat_flydragon_v1": (not pd.isna(e.jg_ma13) and not pd.isna(e.jg_ma55) and float(e.jg_ma13) > float(e.jg_ma55))
                    and bool(e.jg_wick_touch_ma13)
                    and bool(e.jg_buy),
                    "pat_flydragon_v2": (not pd.isna(e.jg_ma13) and not pd.isna(e.jg_ma55) and float(e.jg_ma13) > float(e.jg_ma55))
                    and (bool(e.jg_wick_touch_ma13) or bool(e.jg_wick_touch_ema27))
                    and bool(e.jg_buy)
                    and bool(e.jg_flip_to_red),
                    "pat_flydragon_v3_gold": (not pd.isna(e.jg_ma13) and not pd.isna(e.jg_ma55) and float(e.jg_ma13) > float(e.jg_ma55)) and bool(e.jg_gold),
                    "pat_cloudcover_momo_v1": (not pd.isna(e.jg_ma13) and not pd.isna(e.jg_ma55) and float(e.jg_ma13) > float(e.jg_ma55))
                    and bool(e.jg_flip_to_yellow)
                    and bool(e.jg_close_breakdown_ma13),
                    "pat_boundary_long_v1": (
                        (not pd.isna(e.atr) and float(e.atr) > 0 and not pd.isna(e.jg_ma13) and not pd.isna(e.jg_ma55))
                        and (float(abs(float(e.jg_ma13) - float(e.jg_ma55)) / float(e.atr)) <= 0.5)
                        and bool(e.jg_buy)
                    ),
                    "pat_boundary_short_v1": (
                        (not pd.isna(e.atr) and float(e.atr) > 0 and not pd.isna(e.jg_ma13) and not pd.isna(e.jg_ma55))
                        and (float(abs(float(e.jg_ma13) - float(e.jg_ma55)) / float(e.atr)) <= 0.5)
                        and bool(e.jg_sell)
                    ),
                    "pat_sunrise_v1": bool(e.jg_flip_to_red) and bool(e.jg_buy),
                    "pat_sunset_v1": bool(e.jg_flip_to_yellow) and bool(e.jg_sell),
                    },
                    private_names=private_names,
                )
            )
    out_df = pd.DataFrame(rows)
    _write_csv(out_dir / "entries_suggested_v7.csv", out_df)
    return out_dir


def main() -> None:
    args = _parse_args(sys.argv[1:])
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    if args.get("help"):
        print("Usage:")
        print(
            "  python mt5_exit_assistant.py [--dry-run|--execute] [--watch] [--interval-sec N] [--max-loops N] [--watch-on-new-h1 0|1] [--pool core|observe|exclude|all] [--reset-peak] [--simulate-dd 0.26] [--mt5-status] [--close-all] [--enable-cam 0|1] [--enable-entry 0|1] [--entry-universe pool|marketwatch|symbols] [--entry-symbols A,B,C] [--entry-max N] [--entry-lookback-bars N] [--entry-show-all 0|1] [--entry-gate-snapshot 0|1] [--entry-status 0|1] [--entry-scan-pools core,observe,exclude] [--entry-trade-pool pool|core|observe|all|none] [--entry-execute 0|1] [--entry-lot LOT] [--entry-max-orders N] [--enable-liquidity-gate 0|1] [--liquidity-max-spread-rel 0.15] [--vol-ratio-max 1.5] [--vol-pct-max 80] [--vol-risk-action off|tag|block|drop] [--log-enabled 0|1] [--log-dir PATH] [--log-every-n N] [--private-names 0|1] [--paper-scan --paper-from ISO --paper-to ISO --paper-symbols A,B,C] [--paper-replay --paper-dir PATH --paper-lookahead-bars N --paper-tp1-r 1.0 --paper-tp2-r 2.0 --paper-bar-rule sl_first|tp_first --paper-e2-chase-max 1.5 --paper-e1-diagnose 0|1] [--paper-commentary --paper-dir PATH --commentary-symbol XAUUSD --commentary-topk 5 --commentary-min-n 15] [--export-today] [--export-from ISO] [--export-to ISO] [--summary-today] [--test-trade --test-symbol EURUSD --test-side buy|sell --test-volume 0.01 --close-after-sec 1] [--test18 --test18-symbol EURUSD --test18-volume 0.01]"
        )
        return

    if bool(int(args.get("paper_commentary") or 0) != 0):
        _paper_commentary(args)
        return

    p = Params()
    global _E1_CCI144_VETO_ENABLED
    global _E1_ADX_SCORE_ENABLED
    global _E2_CHASE_MAX_ATR
    global _E2_CHASE_ACTION
    global _LIQUIDITY_GATE_ENABLED
    global _LIQUIDITY_MAX_SPREAD_REL
    global _VOL_RISK_VOL_RATIO_MAX
    global _VOL_RISK_VOL_PCT_MAX
    global _VOL_RISK_ACTION
    global _ENTRY_SCORE_MAX
    global _ENTRY_SCORE_ACTION
    global _ENTRY_SCORE_SCOPE
    global _ENTRY_SCORE_VOL_MODE
    global _ENTRY_SCORE_VOL_ATR_REL_CUTS
    global _ENTRY_SCORE_VOL_MAXES
    _E1_CCI144_VETO_ENABLED = bool(int(args.get("e1_cci144_veto") or 0) != 0)
    _E1_ADX_SCORE_ENABLED = bool(int(args.get("e1_adx_score") or 0) != 0)
    _E2_CHASE_MAX_ATR = args.get("e2_chase_max_atr", None)
    _E2_CHASE_ACTION = str(args.get("e2_chase_action") or "off").strip().lower()
    if _E2_CHASE_ACTION not in {"off", "tag", "block", "drop"}:
        raise ValueError(f"unknown e2_chase_action: {_E2_CHASE_ACTION}")
    if _E2_CHASE_MAX_ATR is not None and not (float(_E2_CHASE_MAX_ATR) > 0):
        _E2_CHASE_MAX_ATR = None
    _LIQUIDITY_GATE_ENABLED = bool(int(args.get("enable_liquidity_gate") or 0) != 0)
    try:
        _LIQUIDITY_MAX_SPREAD_REL = float(args.get("liquidity_max_spread_rel") or _LIQUIDITY_MAX_SPREAD_REL)
    except Exception:
        pass
    if not (_LIQUIDITY_MAX_SPREAD_REL > 0):
        _LIQUIDITY_MAX_SPREAD_REL = 0.15
    _VOL_RISK_VOL_RATIO_MAX = args.get("vol_risk_vol_ratio_max", None)
    _VOL_RISK_VOL_PCT_MAX = args.get("vol_risk_vol_pct_max", None)
    _VOL_RISK_ACTION = str(args.get("vol_risk_action") or "off").strip().lower()
    if _VOL_RISK_ACTION not in {"off", "tag", "block", "drop"}:
        raise ValueError(f"unknown vol_risk_action: {_VOL_RISK_ACTION}")
    if _VOL_RISK_VOL_RATIO_MAX is not None and not (float(_VOL_RISK_VOL_RATIO_MAX) > 0):
        _VOL_RISK_VOL_RATIO_MAX = None
    if _VOL_RISK_VOL_PCT_MAX is not None and not (float(_VOL_RISK_VOL_PCT_MAX) >= 0):
        _VOL_RISK_VOL_PCT_MAX = None

    _ENTRY_SCORE_MAX = args.get("entry_score_max", None)
    _ENTRY_SCORE_ACTION = str(args.get("entry_score_action") or "off").strip().lower()
    _ENTRY_SCORE_SCOPE = str(args.get("entry_score_scope") or "all").strip().lower()
    if _ENTRY_SCORE_ACTION not in {"off", "tag", "block", "drop"}:
        raise ValueError(f"unknown entry_score_action: {_ENTRY_SCORE_ACTION}")
    if _ENTRY_SCORE_SCOPE not in {"all", "e2"}:
        raise ValueError(f"unknown entry_score_scope: {_ENTRY_SCORE_SCOPE}")
    if _ENTRY_SCORE_MAX is not None and not (float(_ENTRY_SCORE_MAX) > 0):
        _ENTRY_SCORE_MAX = None
    _ENTRY_SCORE_VOL_MODE = str(args.get("entry_score_vol_mode") or "off").strip().lower()
    if _ENTRY_SCORE_VOL_MODE not in {"off", "atr_rel_bins"}:
        raise ValueError(f"unknown entry_score_vol_mode: {_ENTRY_SCORE_VOL_MODE}")
    _ENTRY_SCORE_VOL_ATR_REL_CUTS = None
    _ENTRY_SCORE_VOL_MAXES = None
    if _ENTRY_SCORE_VOL_MODE != "off":
        cuts_raw = str(args.get("entry_score_vol_cuts") or "").strip()
        maxes_raw = str(args.get("entry_score_vol_maxes") or "").strip()
        cuts_parts = [x.strip() for x in cuts_raw.split(",") if x.strip()]
        maxes_parts = [x.strip() for x in maxes_raw.split(",") if x.strip()]
        if len(cuts_parts) != 2:
            raise ValueError("--entry-score-vol-cuts requires 2 comma-separated floats: cut1,cut2")
        if len(maxes_parts) != 3:
            raise ValueError("--entry-score-vol-maxes requires 3 comma-separated floats: max_low,max_mid,max_high")
        c1 = float(cuts_parts[0])
        c2 = float(cuts_parts[1])
        m0 = float(maxes_parts[0])
        m1 = float(maxes_parts[1])
        m2 = float(maxes_parts[2])
        if not (c1 > 0 and c2 > 0 and c1 < c2):
            raise ValueError("--entry-score-vol-cuts must satisfy 0 < cut1 < cut2")
        if not (m0 > 0 and m1 > 0 and m2 > 0):
            raise ValueError("--entry-score-vol-maxes must all be > 0")
        _ENTRY_SCORE_VOL_ATR_REL_CUTS = (c1, c2)
        _ENTRY_SCORE_VOL_MAXES = (m0, m1, m2)
    p = replace(p, enable_score_filter=bool(int(args.get("enable_score_filter") or 0) != 0))
    try:
        v = int(args.get("entry_require_strong", 1))
    except Exception:
        v = 1
    p = replace(p, require_strong_for_entry=bool(v != 0))
    c = Config()

    if bool(int(args.get("paper_replay_csv") or 0) != 0):
        _paper_replay_csv(args)
        return
    if bool(int(args.get("paper_scan_csv") or 0) != 0):
        out_dir = _paper_scan_csv(args, p=p)
        print(f"[PAPER] scan_csv ok: {str(out_dir)}")
        return

    state = _load_state()

    _require_mt5_initialized()
    try:
        if bool(int(args.get("mt5_status") or 0) != 0):
            _print_trade_api_status()
            return
        if bool(int(args.get("mt5_history_check") or 0) != 0):
            _mt5_history_check(args)
            return
        if bool(int(args.get("paper_replay") or 0) != 0):
            _paper_replay(args)
            return
        if bool(int(args.get("paper_scan") or 0) != 0):
            out_dir = _paper_scan(args, p=p)
            print(f"[PAPER] scan ok: {str(out_dir)}")
            return
        sim_dd_raw = args.get("simulate_dd")
        if sim_dd_raw is not None and str(sim_dd_raw) != "":
            try:
                dd_v = float(sim_dd_raw)
            except Exception:
                dd_v = 0.0
            if dd_v > 1.0:
                dd_v = dd_v / 100.0
            dd_v = max(0.0, min(0.95, float(dd_v)))
            eq0 = _get_account_equity()
            if float(eq0) > 0 and dd_v > 0:
                peak0 = float(eq0) / float(max(1e-9, 1.0 - float(dd_v)))
                state["peak_equity"] = float(peak0)
                state["dd_halted"] = bool(dd_v >= float(Config().max_drawdown))
                print(f"[DRILL] simulate_dd={dd_v:.4f} equity={float(eq0):.2f} peak_equity_set={float(peak0):.2f}")
                _save_state(state)
        if bool(args.get("test_trade")):
            _run_test_trade(args)
            return
        if bool(args.get("test18")):
            _run_test18(args)
            return
        if bool(args.get("export_today")) or str(args.get("export_from") or "").strip() or str(args.get("export_to") or "").strip():
            _export_history(args)
            return
        if bool(args.get("summary_today")):
            _summary_today(args)
            return
        interval_sec = max(1, int(args.get("interval_sec") or 30))
        max_loops = args.get("max_loops")
        loops = 0
        watch_wait_printed = False
        while True:
            try:
                if bool(args.get("watch")) and int(args.get("watch_on_new_h1") or 0) != 0:
                    try:
                        pos_total = int(mt5.positions_total() or 0)
                    except Exception:
                        pos_total = 0
                    if pos_total <= 0:
                        core_df = _read_deploy_pool_df("core")
                        ref_sym = str(args.get("test_symbol") or "EURUSD")
                        if core_df is not None and (not core_df.empty) and ("symbol" in core_df.columns):
                            try:
                                ref_sym = str(core_df["symbol"].iloc[0])
                            except Exception:
                                pass
                        ref_sym = _resolve_symbol(str(ref_sym).strip().upper())
                        bar_ts = _last_bar_open_ts(ref_sym, mt5.TIMEFRAME_H1)
                        if bar_ts is not None:
                            bar_key = str(bar_ts)
                            last_key = str(state.get("watch_last_h1_bar") or "")
                            if last_key and bar_key == last_key:
                                if not watch_wait_printed:
                                    print(f"[WATCH] waiting new H1 bar: lastBarH1={bar_key} symbol={ref_sym} interval_sec={interval_sec}")
                                    watch_wait_printed = True
                                time.sleep(interval_sec)
                                continue
                            state["watch_last_h1_bar"] = bar_key
                            watch_wait_printed = False
                state = _run_once(args, p=p, c=c, state=state)
                _save_state(state)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"[ERROR] {type(e).__name__}: {e}")

            loops += 1
            if not bool(args.get("watch")):
                break
            if max_loops is not None and loops >= int(max_loops):
                break
            time.sleep(interval_sec)
    finally:
        _shutdown_mt5()


if __name__ == "__main__":
    main()
