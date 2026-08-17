"""
calc_index_daily_indicators_v1.py
作用：6 大指数日线 List[dict] → 输出结构化+MA/MACD/RSI/BOLL + 4 列事实判断
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


INDEX_CODE_MAPS = [
    ("000001", "上证指数"), ("000300", "沪深300"), ("000905", "中证500"),
    ("000852", "中证1000"), ("399006", "创业板指"), ("000688", "科创50"),
]

OUT_COLS = [
    "code", "name", "trade_date",
    "open", "high", "low", "close", "volume", "amount",
    "MA5", "MA10", "MA20",
    "EMA12", "EMA26",
    "DIF", "DEA", "MACD_BAR_x2",
    "RSI6", "RSI12", "RSI14", "RSI24",
    "BOLL_U_20_2", "BOLL_M_20", "BOLL_L_20_2",
    "MA20_ABOVE", "MA5_ABOVE_MA20", "MACD_GOLDEN_CROSS", "MACD_DEAD_CROSS",
]

TEST_CLOSE: List[float] = [
    101.0, 102.5, 103.2, 105.8, 106.1, 107.3, 108.9, 110.4, 112.0, 113.6,
    115.2, 116.8, 118.4, 120.0, 121.5, 123.1, 124.7, 126.2, 127.8, 129.3,
    130.9, 132.4, 133.9, 135.4, 136.8, 138.3, 139.7, 141.1, 142.5, 143.8,
    145.1, 146.4, 147.6, 148.8, 150.0, 148.5, 147.0, 145.5, 143.9, 142.3,
    140.7, 139.1, 137.5, 135.9, 134.3, 132.7, 131.2, 129.7, 128.2, 126.8,
    125.5, 124.3, 123.2, 122.2, 121.4, 120.7, 120.1, 119.7, 119.4, 119.2,
]


def ma(series: List[float], n: int) -> List[Optional[float]]:
    """一、简单移动平均：前 N 天算术平均；前 N-1 天 = NA"""
    out: List[Optional[float]] = [None] * len(series)
    s = 0.0
    for i in range(len(series)):
        s += series[i]
        if i >= n:
            s -= series[i - n]
        if i >= n - 1:
            out[i] = s / n
    return out


def ema(series: List[float], n: int) -> List[float]:
    """
    二、指数移动平均：
        EMA_today = EMA_prev * (N-1)/(N+1) + today * 2/(N+1)
        首日 EMA = 首日 close（而不是 SMA(N)，避免首日不一致）
    """
    out: List[float] = [0.0] * len(series)
    k = 2.0 / (n + 1.0)
    out[0] = series[0]
    for i in range(1, len(series)):
        out[i] = out[i - 1] * (1.0 - k) + series[i] * k
    return out


def macd(series: List[float], fast: int = 12, slow: int = 26, signal: int = 9
         ) -> Tuple[List[float], List[float], List[float]]:
    """
    三、MACD（标准参数 12, 26, 9）：
        DIF  = EMA(C, 12) - EMA(C, 26)
        DEA  = EMA(DIF, 9)
        MACD柱 = 2 * (DIF - DEA)  （很多软件都 x2，保持一致）
    """
    e12 = ema(series, fast)
    e26 = ema(series, slow)
    dif = [e12[i] - e26[i] for i in range(len(series))]
    dea = ema(dif, signal)
    bar = [2.0 * (dif[i] - dea[i]) for i in range(len(series))]
    return dif, dea, bar


def rsi(series: List[float], n: int) -> List[Optional[float]]:
    """
    四、RSI（Wilder 平滑法，不是 SMA，也不是 EMA_twice）：
        delta = today - yesterday
        gains[n-1..] = max(delta, 0)
        losses[n-1..] = max(-delta, 0)
        第一个 avg_g / avg_l = 前 N 个 delta 的简单平均
        后续 Wilder 平滑：avg = (prev_avg * (N-1) + today_delta) / N
        RSI = 100 - 100 / (1 + RS)，  RS = avg_g / avg_l  （avg_l=0 时 RSI=100）
    """
    out: List[Optional[float]] = [None] * len(series)
    if len(series) <= n:
        return out
    gains: List[float] = []
    losses: List[float] = []
    for i in range(1, len(series)):
        d = series[i] - series[i - 1]
        gains.append(max(d, 0.0))
        losses.append(max(-d, 0.0))
    avg_g = sum(gains[:n]) / n
    avg_l = sum(losses[:n]) / n
    out[n] = 100.0 - 100.0 / (1.0 + (avg_g / max(avg_l, 1e-12)))
    for i in range(n + 1, len(series)):
        g = gains[i - 1]
        l = losses[i - 1]
        avg_g = (avg_g * (n - 1) + g) / n
        avg_l = (avg_l * (n - 1) + l) / n
        out[i] = 100.0 - 100.0 / (1.0 + (avg_g / max(avg_l, 1e-12)))
    return out


def boll(series: List[float], n: int = 20, k: float = 2.0
         ) -> Tuple[List[Optional[float]], List[Optional[float]], List[Optional[float]]]:
    """
    五、BOLL（N=20，K 倍标准差 = 2）：
        中轨 = MA(C, 20)
        σ    = sqrt( (1/N) * Σ (C_i - 中轨)^2 )   （总体标准差，分母 N 不是 N-1）
        上轨 = 中轨 + K*σ
        下轨 = 中轨 - K*σ
    """
    mid = ma(series, n)
    up: List[Optional[float]] = [None] * len(series)
    lo: List[Optional[float]] = [None] * len(series)
    for i in range(len(series)):
        if mid[i] is None:
            continue
        win = series[i - n + 1:i + 1]
        mean = mid[i]
        assert mean is not None
        var = sum((x - mean) ** 2 for x in win) / n
        sigma = math.sqrt(var)
        up[i] = mean + k * sigma
        lo[i] = mean - k * sigma
    return up, mid, lo


def _f(v: object) -> Optional[float]:
    if v is None:
        return None
    s = str(v).strip()
    if s == "" or s.upper() == "NA" or s.upper() == "NONE":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _pick(r: Dict, *ks: str, default: str = "") -> str:
    for k in ks:
        v = r.get(k)
        if v is None:
            continue
        s = str(v).strip()
        if s != "":
            return s
    return default


def compute_indicators_on_closes(closes: List[float]) -> Dict[str, List[Optional[float]]]:
    ma5 = ma(closes, 5)
    ma10 = ma(closes, 10)
    ma20 = ma(closes, 20)
    ema12 = ema(closes, 12)
    ema26 = ema(closes, 26)
    dif, dea, bar = macd(closes)
    rsi6 = rsi(closes, 6)
    rsi12 = rsi(closes, 12)
    rsi14 = rsi(closes, 14)
    rsi24 = rsi(closes, 24)
    boll_u, boll_m, boll_l = boll(closes)
    ma20_above: List[Optional[float]] = [None] * len(closes)
    ma5_above_ma20: List[Optional[float]] = [None] * len(closes)
    golden: List[Optional[float]] = [None] * len(closes)
    dead: List[Optional[float]] = [None] * len(closes)
    for i in range(len(closes)):
        if ma20[i] is None:
            ma20_above[i] = None
        else:
            ma20_above[i] = 1 if closes[i] > ma20[i] else 0
        if ma5[i] is None or ma20[i] is None:
            ma5_above_ma20[i] = None
        else:
            ma5_above_ma20[i] = 1 if ma5[i] > ma20[i] else 0
        if i == 0:
            golden[i] = None
            dead[i] = None
        else:
            if dif[i - 1] <= dea[i - 1] and dif[i] > dea[i]:
                golden[i] = 1
            else:
                golden[i] = 0
            if dif[i - 1] >= dea[i - 1] and dif[i] < dea[i]:
                dead[i] = 1
            else:
                dead[i] = 0
    return {
        "MA5": ma5,
        "MA10": ma10,
        "MA20": ma20,
        "EMA12": list(ema12),
        "EMA26": list(ema26),
        "DIF": list(dif),
        "DEA": list(dea),
        "MACD_BAR_x2": list(bar),
        "RSI6": rsi6,
        "RSI12": rsi12,
        "RSI14": rsi14,
        "RSI24": rsi24,
        "BOLL_U_20_2": boll_u,
        "BOLL_M_20": boll_m,
        "BOLL_L_20_2": boll_l,
        "MA20_ABOVE": ma20_above,
        "MA5_ABOVE_MA20": ma5_above_ma20,
        "MACD_GOLDEN_CROSS": golden,
        "MACD_DEAD_CROSS": dead,
    }


def enrich_rows(rows: List[Dict]) -> List[Dict]:
    groups: Dict[str, List[Dict]] = {}
    order: List[str] = []
    for r in rows:
        code = _pick(r, "code", "index_code", "股票代码", "指数代码", "代码")
        if not code:
            continue
        if code not in groups:
            groups[code] = []
            order.append(code)
        groups[code].append(dict(r))
    out: List[Dict] = []
    for code in order:
        items = groups[code]
        items.sort(key=lambda x: _pick(x, "trade_date", "date", "日期"))
        closes: List[float] = []
        valid_idx: List[int] = []
        for i, it in enumerate(items):
            c = _f(_pick(it, "close", "收盘", "收盘价", "最新", "现价"))
            if c is None:
                continue
            closes.append(c)
            valid_idx.append(i)
        if not closes:
            for it in items:
                row = {c: "" for c in OUT_COLS}
                row["code"] = code
                row["name"] = _pick(it, "name", "index_name", "名称", "指数名称")
                row["trade_date"] = _pick(it, "trade_date", "date", "日期")
                row["open"] = _pick(it, "open", "开盘", "开盘价", "今开")
                row["high"] = _pick(it, "high", "最高", "最高价")
                row["low"] = _pick(it, "low", "最低", "最低价")
                row["close"] = _pick(it, "close", "收盘", "收盘价", "最新", "现价")
                row["volume"] = _pick(it, "volume", "vol", "成交量")
                row["amount"] = _pick(it, "amount", "amt", "amt_yuan", "成交额")
                out.append(row)
            continue
        ind = compute_indicators_on_closes(closes)
        pos_map = {vi: j for j, vi in enumerate(valid_idx)}
        for i, it in enumerate(items):
            row = {c: None for c in OUT_COLS}
            row["code"] = code
            row["name"] = _pick(it, "name", "index_name", "名称", "指数名称")
            row["trade_date"] = _pick(it, "trade_date", "date", "日期")
            row["open"] = _pick(it, "open", "开盘", "开盘价", "今开")
            row["high"] = _pick(it, "high", "最高", "最高价")
            row["low"] = _pick(it, "low", "最低", "最低价")
            row["close"] = _pick(it, "close", "收盘", "收盘价", "最新", "现价")
            row["volume"] = _pick(it, "volume", "vol", "成交量")
            row["amount"] = _pick(it, "amount", "amt", "amt_yuan", "成交额")
            j = pos_map.get(i)
            if j is not None:
                for k, arr in ind.items():
                    row[k] = arr[j]
            out.append(row)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-root", required=True)
    ap.add_argument("--out-root", required=True)
    ap.add_argument("--trade-date", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)
    raw_root, out_root, td = Path(args.raw_root), Path(args.out_root), args.trade_date
    matches = list(raw_root.glob(f"index_bar_raw_{td}.csv")) + list(raw_root.glob("index_bar_raw_*.csv"))
    if not matches:
        print("[6_指数] 未找到 index_bar_raw_*.csv，SKIP")
        return 0
    src = matches[0]
    print(f"[6_指数] 读原始CSV：{src.name}")
    raw_rows: List[Dict] = []
    with src.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            code_raw = _pick(r, "代码", "指数代码", "code", "index_code")
            name_raw = _pick(r, "名称", "指数名称", "name", "index_name")
            matched = None
            if code_raw:
                digits = "".join(ch for ch in code_raw if ch.isdigit())
                for cc, nn in INDEX_CODE_MAPS:
                    if cc in digits:
                        matched = (cc, nn)
                        break
            if not matched and name_raw:
                for cc, nn in INDEX_CODE_MAPS:
                    if nn in name_raw:
                        matched = (cc, nn)
                        break
            if not matched:
                if code_raw and len(code_raw) >= 6:
                    digits = "".join(ch for ch in code_raw if ch.isdigit())[-6:]
                    matched = (digits, name_raw or "指数")
                else:
                    continue
            cc, nn = matched
            raw_rows.append({
                "code": cc,
                "name": nn,
                "trade_date": td,
                "open": _pick(r, "今开", "开盘价", "open"),
                "high": _pick(r, "最高", "最高价", "high"),
                "low": _pick(r, "最低", "最低价", "low"),
                "close": _pick(r, "收盘", "收盘价", "最新", "现价", "close"),
                "volume": _pick(r, "成交量", "volume", "vol"),
                "amount": _pick(r, "成交额", "amount", "amt", "amt_yuan", "成交量(成交额)"),
            })
    rows_out = enrich_rows(raw_rows)
    out_p = out_root / f"a_share_index_daily_indicators_{td}.csv"
    if args.apply and rows_out:
        with out_p.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=OUT_COLS, extrasaction="ignore")
            w.writeheader()
            for r in rows_out:
                w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in OUT_COLS})
        print(f"[6_指数] WROTE {out_p} → {len(rows_out)} 行")
    else:
        print(f"[6_指数] DRY_RUN/空：匹配 {len(rows_out)} 行；加--apply写输出")
    return 0


def run_acceptance() -> int:
    ind = compute_indicators_on_closes(TEST_CLOSE)
    groups = [
        ("MA5", [0]),
        ("MA10", [1]),
        ("MA20", [2]),
        ("EMA12", [3]),
        ("EMA26", [4]),
        ("DIF", [5]),
        ("DEA", [6]),
        ("MACD_BAR_x2", [7]),
        ("RSI6", [8]),
        ("RSI12", [9]),
        ("RSI14", [10]),
        ("RSI24", [11]),
        ("BOLL", [12, 13, 14]),
    ]
    key_by_col = [
        "MA5", "MA10", "MA20",
        "EMA12", "EMA26",
        "DIF", "DEA", "MACD_BAR_x2",
        "RSI6", "RSI12", "RSI14", "RSI24",
        "BOLL_U_20_2", "BOLL_M_20", "BOLL_L_20_2",
    ]
    ref_path = Path(__file__).resolve().parent / "batch_11_tech_indicators_reference_values_20260813.csv"
    ref_rows: List[List[str]] = []
    with ref_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            ref_rows.append(row)
    pass_n = 0
    fail_n = 0
    max_abs = 0.0

    def cell_ok(key: str, col_i: int) -> bool:
        nonlocal max_abs
        ok = True
        for i, row in enumerate(ref_rows):
            ref_s = row[col_i + 2].strip() if col_i + 2 < len(row) else ""
            ours = ind[key][i]
            if ref_s == "":
                if ours is not None:
                    ok = False
                    max_abs = max(max_abs, abs(float(ours)))
                continue
            if ours is None:
                ok = False
                continue
            d = abs(float(ours) - float(ref_s))
            if d > max_abs:
                max_abs = d
            if d > 1e-6:
                ok = False
        return ok

    for _name, cols in groups:
        ok = True
        for col_i in cols:
            if not cell_ok(key_by_col[col_i], col_i):
                ok = False
        if ok:
            pass_n += 1
        else:
            fail_n += 1
    total = len(groups)
    print(f"【calc_index_daily_indicators_v1 验收】通过 {pass_n}/{total} 行，FAIL {fail_n}/{total} 行，最大绝对误差 = {max_abs}")
    return 0 if fail_n == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.exit(run_acceptance())
    sys.exit(main())
