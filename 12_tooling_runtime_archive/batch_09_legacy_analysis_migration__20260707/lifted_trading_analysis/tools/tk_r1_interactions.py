from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import backtest_p0 as m


EPS = 1e-12


def compute_b114_tuned(ohlc: pd.DataFrame, lookback_bars: int = 36) -> pd.DataFrame:
    o = pd.to_numeric(ohlc["open"], errors="coerce").astype(float)
    h = pd.to_numeric(ohlc["high"], errors="coerce").astype(float)
    l = pd.to_numeric(ohlc["low"], errors="coerce").astype(float)
    c = pd.to_numeric(ohlc["close"], errors="coerce").astype(float)
    prev_c = c.shift(1)
    tr = pd.concat([(h - l).abs(), (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
    atr = tr.ewm(span=14, adjust=False).mean()
    atr_eff = atr.where(atr > 0.0, np.nan)

    roll_high = h.rolling(lookback_bars, min_periods=max(20, lookback_bars // 6)).max().shift(1)
    roll_low = l.rolling(lookback_bars, min_periods=max(20, lookback_bars // 6)).min().shift(1)
    height = (roll_high - roll_low).astype(float)
    height_eff = height.where(height > 0.0, np.nan)
    height_atr = (height_eff / (atr_eff + EPS)).astype(float)
    range_ok = height_atr.notna() & (height_atr >= 1.0) & (height_atr <= 12.0)

    deep_long = roll_high - height_eff * 0.50
    deep_short = roll_low + height_eff * 0.50
    wick_breach_long = ((deep_long - l).clip(lower=0.0) / (atr_eff + EPS)).astype(float)
    wick_breach_short = ((h - deep_short).clip(lower=0.0) / (atr_eff + EPS)).astype(float)
    close_breach_long = ((deep_long - c).clip(lower=0.0) / (atr_eff + EPS)).astype(float)
    close_breach_short = ((c - deep_short).clip(lower=0.0) / (atr_eff + EPS)).astype(float)

    rng = (h - l).astype(float)
    rng_eff = rng.where(rng > 0.0, np.nan)
    body = (c - o).abs().astype(float)
    body_ratio = (body / (rng_eff + EPS)).astype(float)
    close_pos = ((c - l) / (rng_eff + EPS)).astype(float)
    upper_r = ((h - np.maximum(o, c)) / (rng_eff + EPS)).astype(float)
    lower_r = ((np.minimum(o, c) - l) / (rng_eff + EPS)).astype(float)

    reclaim_long = (wick_breach_long > EPS) & (close_breach_long <= EPS)
    reclaim_short = (wick_breach_short > EPS) & (close_breach_short <= EPS)
    wick_ok_long = (lower_r >= 0.15) & (close_pos >= 0.35)
    wick_ok_short = (upper_r >= 0.15) & (close_pos <= 0.65)
    strong_long = (c > o) & (body_ratio >= 0.20) & (close_pos >= 0.50) & wick_ok_long
    strong_short = (c < o) & (body_ratio >= 0.20) & (close_pos <= 0.50) & wick_ok_short

    stage_long = pd.Series(
        np.select(
            [
                wick_breach_long <= EPS,
                (wick_breach_long > EPS) & (~reclaim_long),
                reclaim_long & (~strong_long),
            ],
            [0, 1, 2],
            default=3,
        ),
        index=ohlc.index,
        dtype=float,
    ).where(range_ok)
    stage_short = pd.Series(
        np.select(
            [
                wick_breach_short <= EPS,
                (wick_breach_short > EPS) & (~reclaim_short),
                reclaim_short & (~strong_short),
            ],
            [0, 1, 2],
            default=3,
        ),
        index=ohlc.index,
        dtype=float,
    ).where(range_ok)

    return pd.DataFrame(
        {
            "stage_long": stage_long,
            "stage_short": stage_short,
            "reclaim_long": reclaim_long.astype(float).where(range_ok),
            "reclaim_short": reclaim_short.astype(float).where(range_ok),
        },
        index=ohlc.index,
    )


def compute_b46_signal_quality(ohlc: pd.DataFrame) -> pd.DataFrame:
    o = pd.to_numeric(ohlc["open"], errors="coerce").astype(float)
    h = pd.to_numeric(ohlc["high"], errors="coerce").astype(float)
    l = pd.to_numeric(ohlc["low"], errors="coerce").astype(float)
    c = pd.to_numeric(ohlc["close"], errors="coerce").astype(float)
    rng = (h - l).astype(float)
    rng_eff = rng.where(rng > 0.0, np.nan)
    body = (c - o).abs().astype(float)
    close_pos_long = (c - l).astype(float) / (rng_eff + EPS)
    close_pos_short = (h - c).astype(float) / (rng_eff + EPS)
    upper = (h - np.maximum(o, c)).astype(float) / (rng_eff + EPS)
    lower = (np.minimum(o, c) - l).astype(float) / (rng_eff + EPS)
    body_ratio = body.astype(float) / (rng_eff + EPS)
    is_doji = body_ratio < 0.05

    def _score(close_pos: pd.Series, upper_w: pd.Series, lower_w: pd.Series, body_r: pd.Series, doji: pd.Series) -> pd.Series:
        cp = pd.to_numeric(close_pos, errors="coerce").to_numpy(dtype=float)
        uw = pd.to_numeric(upper_w, errors="coerce").to_numpy(dtype=float)
        lw = pd.to_numeric(lower_w, errors="coerce").to_numpy(dtype=float)
        br = pd.to_numeric(body_r, errors="coerce").to_numpy(dtype=float)
        dj = pd.to_numeric(doji, errors="coerce").fillna(0).astype(int).to_numpy(dtype=int)
        s_close = np.select([cp >= 0.70, cp >= 0.55, cp >= 0.45], [2, 1, 0], default=-1).astype(int)
        s_lw = np.select([lw < 0.05, lw < 0.20, lw < 0.35], [2, 1, 0], default=-1).astype(int)
        s_uw = np.select([uw < 0.05, uw < 0.20, uw < 0.35], [2, 1, 0], default=-1).astype(int)
        s_pos = np.select([br > 0.60, br > 0.30, br > 0.10], [2, 1, 0], default=-1).astype(int)
        raw = s_close + s_lw + s_uw + s_pos - 2 * (dj == 1).astype(int)
        return pd.Series(np.clip(raw + 2, 0, 10).astype(int), index=close_pos.index)

    return pd.DataFrame(
        {
            "score_long": _score(close_pos_long, upper, lower, body_ratio, is_doji),
            "score_short": _score(close_pos_short, lower, upper, body_ratio, is_doji),
        },
        index=ohlc.index,
    )


def compute_b51_reversal(ohlc: pd.DataFrame) -> pd.DataFrame:
    o = pd.to_numeric(ohlc["open"], errors="coerce").astype(float)
    h = pd.to_numeric(ohlc["high"], errors="coerce").astype(float)
    l = pd.to_numeric(ohlc["low"], errors="coerce").astype(float)
    c = pd.to_numeric(ohlc["close"], errors="coerce").astype(float)
    rng = (h - l).astype(float)
    rng_eff = rng.where(rng > 0.0, np.nan)
    body = (c - o).abs().astype(float)
    body_ratio = body / (rng_eff + EPS)
    close_pos = ((c - l) / (rng_eff + EPS)).astype(float)
    prev_c = c.shift(1)
    tr = pd.concat([(h - l).abs(), (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
    atr = tr.ewm(span=14, adjust=False).mean()
    atr_eff = atr.where(atr > 0.0, np.nan)
    ema = c.ewm(span=20, adjust=False).mean()
    ema_diff = ema - ema.shift(12)
    slope_norm = (ema_diff.abs() / (atr_eff + EPS)).astype(float)
    trend_up = ema_diff > 0.0
    trend_dn = ema_diff < 0.0
    strong_up = trend_up & (slope_norm >= 0.20)
    strong_dn = trend_dn & (slope_norm >= 0.20)
    roll_max = h.rolling(20, min_periods=max(5, 20 // 4)).max().shift(1)
    roll_min = l.rolling(20, min_periods=max(5, 20 // 4)).min().shift(1)
    bo_up = c > roll_max
    bo_dn = c < roll_min
    bull_sig = (c > o) & (body_ratio >= 0.45) & (close_pos >= 0.60)
    bear_sig = (c < o) & (body_ratio >= 0.45) & (close_pos <= 0.40)
    ext_dn = ((ema - l) / (atr_eff + EPS) >= 1.0) & (c < ema)
    ext_up = ((h - ema) / (atr_eff + EPS) >= 1.0) & (c > ema)
    same_dir = (c > o).astype(int)
    climax_bars = 3
    same_dir_prev = same_dir.shift(1).rolling(climax_bars, min_periods=max(1, climax_bars)).sum()
    big_body = (body_ratio >= 0.45).astype(int).shift(1).rolling(climax_bars, min_periods=max(1, climax_bars)).sum()
    move_abs = (c.shift(1) - c.shift(1 + climax_bars)).abs() / (atr_eff.shift(1) + EPS)
    climax_up = (same_dir_prev >= float(climax_bars)) & (big_body >= float(climax_bars)) & (move_abs >= 3.0)
    climax_dn = ((climax_bars - same_dir_prev) >= float(climax_bars)) & (big_body >= float(climax_bars)) & (move_abs >= 3.0)
    lookback_bars = 48
    hilo_flat = (
        (
            ((h > h.shift(1)).astype(float).rolling(lookback_bars, min_periods=max(10, lookback_bars // 3)).mean())
            + ((l > l.shift(1)).astype(float).rolling(lookback_bars, min_periods=max(10, lookback_bars // 3)).mean())
        )
        / 2.0
        <= 0.55
    ) & (
        (
            ((h < h.shift(1)).astype(float).rolling(lookback_bars, min_periods=max(10, lookback_bars // 3)).mean())
            + ((l < l.shift(1)).astype(float).rolling(lookback_bars, min_periods=max(10, lookback_bars // 3)).mean())
        )
        / 2.0
        <= 0.55
    )
    ema_flat = slope_norm <= 0.15
    range_like = (hilo_flat & ema_flat).astype(int)
    bull_score = (
        strong_dn.astype(int)
        + (strong_dn & bo_up).astype(int)
        + (strong_dn & bull_sig).astype(int)
        + (strong_dn & ext_dn).astype(int)
        + (strong_dn & climax_dn).astype(int)
    )
    bull_score = (bull_score - range_like).clip(lower=0).astype(int)
    bear_score = (
        strong_up.astype(int)
        + (strong_up & bo_dn).astype(int)
        + (strong_up & bear_sig).astype(int)
        + (strong_up & ext_up).astype(int)
        + (strong_up & climax_up).astype(int)
    )
    bear_score = (bear_score - range_like).clip(lower=0).astype(int)
    return pd.DataFrame({"bull_score": bull_score, "bear_score": bear_score}, index=ohlc.index)


def compute_b53_pattern(ohlc: pd.DataFrame) -> pd.DataFrame:
    o = pd.to_numeric(ohlc["open"], errors="coerce").astype(float)
    h = pd.to_numeric(ohlc["high"], errors="coerce").astype(float)
    l = pd.to_numeric(ohlc["low"], errors="coerce").astype(float)
    c = pd.to_numeric(ohlc["close"], errors="coerce").astype(float)
    rng = (h - l).astype(float)
    rng_eff = rng.where(rng > 0.0, np.nan)
    body = (c - o).abs().astype(float)
    body_ratio = (body / (rng_eff + EPS)).astype(float)
    close_pos = ((c - l) / (rng_eff + EPS)).astype(float)
    upper_w = (h - np.maximum(o, c)).astype(float)
    lower_w = (np.minimum(o, c) - l).astype(float)
    upper_r = (upper_w / (rng_eff + EPS)).astype(float)
    lower_r = (lower_w / (rng_eff + EPS)).astype(float)
    bull_trend = (c > o) & (body_ratio >= 0.30) & (close_pos >= 0.60) & (lower_r <= 0.30)
    bear_trend = (c < o) & (body_ratio >= 0.30) & (close_pos <= 0.40) & (upper_r <= 0.30)
    strong_bull = bull_trend & (upper_r <= 0.05) & (body_ratio >= 0.50)
    strong_bear = bear_trend & (lower_r <= 0.05) & (body_ratio >= 0.50)
    mid_rng = ((h + l) / 2.0).astype(float)
    mid_body = ((np.maximum(o, c) + np.minimum(o, c)) / 2.0).astype(float)
    in_mid = (rng_eff.notna()) & ((mid_body - mid_rng).abs() <= (0.10 * rng_eff))
    long_wicks = (upper_w > (2.0 * body)) & (lower_w > (2.0 * body))
    doji = ((body_ratio < 0.10) | (in_mid & long_wicks)).astype(int)
    bull_strength = np.select([strong_bull, bull_trend], [2, 1], default=0).astype(int)
    bear_strength = np.select([strong_bear, bear_trend], [2, 1], default=0).astype(int)
    return pd.DataFrame(
        {
            "bull_strength": pd.Series(bull_strength, index=ohlc.index),
            "bear_strength": pd.Series(bear_strength, index=ohlc.index),
            "doji": pd.Series(doji, index=ohlc.index),
        },
        index=ohlc.index,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run tuned TK-R1 interactions against b46/b51/b53.")
    parser.add_argument("--p0_sweep_dir", default=str(Path("backtest_out") / "p0_sweep"))
    parser.add_argument("--csv_dir", default="data")
    parser.add_argument("--out_dir", default=str(Path("backtest_out") / "stage2" / "indicator_audit" / "20260611_b114_tk_tp3_extension_tuned_v2"))
    parser.add_argument("--split", default="since2022")
    parser.add_argument("--lookback_bars", type=int, default=36)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    p0_sweep_dir = Path(args.p0_sweep_dir)
    csv_dir = Path(args.csv_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    files = m._iter_trades_baseline_csvs(p0_sweep_dir)
    for trades_csv in files:
        symbol, split, profile = m._extract_symbol_split_profile(trades_csv, p0_sweep_dir)
        if str(split).strip() != str(args.split).strip():
            continue
        sym_u = str(symbol).strip().upper()
        try:
            merged = m._trade_level_merged_for_features(trades_csv, p0_sweep_dir, ["entry_score", "e1_break_strength_atr"])
        except Exception:
            continue
        if merged.empty:
            continue
        try:
            csv_path = m._find_symbol_csv(csv_dir, sym_u)
        except Exception:
            continue
        if csv_path is None or not Path(csv_path).exists():
            continue
        try:
            ohlc = m.load_ohlcv_1h(csv_path, tz=None)
        except Exception:
            continue
        if ohlc.empty:
            continue

        b114 = compute_b114_tuned(ohlc, lookback_bars=int(args.lookback_bars))
        b46 = compute_b46_signal_quality(ohlc)
        b51 = compute_b51_reversal(ohlc)
        b53 = compute_b53_pattern(ohlc)

        idx = ohlc.index
        idx_utc = idx.tz_localize("UTC") if getattr(idx, "tz", None) is None else idx.tz_convert("UTC")
        ts_ns = idx_utc.view("int64")
        entry_dt = pd.to_datetime(merged["entry_time"], utc=True, errors="coerce")
        entry_ns = entry_dt.astype("int64")
        side_s = merged["side"].astype(str).str.strip().str.upper()

        for i in range(len(merged)):
            en = entry_ns.iloc[i]
            if pd.isna(en):
                continue
            j = int(np.searchsorted(ts_ns, int(en), side="right")) - 1
            if not (0 <= j < len(ts_ns)):
                continue
            is_short = side_s.iloc[i] == "SHORT"
            stage = float(b114["stage_short" if is_short else "stage_long"].iloc[j])
            reclaim = float(b114["reclaim_short" if is_short else "reclaim_long"].iloc[j])
            if not np.isfinite(stage):
                continue
            rows.append(
                {
                    "symbol": sym_u,
                    "profile": str(profile).strip(),
                    "stage": int(stage),
                    "stage_active": int(stage >= 2),
                    "reclaim_flag": int(reclaim >= 1),
                    "trade_pnl": float(pd.to_numeric(merged["trade_pnl"].iloc[i], errors="coerce")),
                    "win": int(bool(pd.to_numeric(merged["win"].iloc[i], errors="coerce"))),
                    "stop_loss_any": int(bool(pd.to_numeric(merged["stop_loss_any"].iloc[i], errors="coerce"))),
                    "tp2_any": int(bool(pd.to_numeric(merged["tp2_any"].iloc[i], errors="coerce"))),
                    "b46_sig_quality": float(b46["score_short" if is_short else "score_long"].iloc[j]),
                    "b51_reversal_score": float(b51["bear_score" if is_short else "bull_score"].iloc[j]),
                    "b53_trendbar_strength": float(b53["bear_strength" if is_short else "bull_strength"].iloc[j]),
                    "b53_doji_flag": float(b53["doji"].iloc[j]),
                }
            )

    all_df = pd.DataFrame(rows)
    all_df.to_csv(out_dir / "b114_tuned_trade_level_interactions_20260611_v1.csv", index=False, encoding="utf-8-sig")

    stage_summary = (
        all_df.groupby("stage", dropna=False)
        .agg(
            n_trades=("trade_pnl", "size"),
            avg_pnl=("trade_pnl", "mean"),
            win_rate=("win", "mean"),
            stop_loss_rate=("stop_loss_any", "mean"),
            tp2_rate=("tp2_any", "mean"),
            b46_sig_quality=("b46_sig_quality", "mean"),
            b51_reversal_score=("b51_reversal_score", "mean"),
            b53_trendbar_strength=("b53_trendbar_strength", "mean"),
            b53_doji_flag=("b53_doji_flag", "mean"),
        )
        .reset_index()
    )
    stage_summary.to_csv(out_dir / "b114_tuned_stage_summary_20260611_v1.csv", index=False, encoding="utf-8-sig")

    def _compare_frames(a: pd.DataFrame, b: pd.DataFrame, name: str) -> dict[str, float | str]:
        return {
            "comparison": name,
            "n_a": float(len(a)),
            "n_b": float(len(b)),
            "avg_pnl_a": float(a["trade_pnl"].mean()),
            "avg_pnl_b": float(b["trade_pnl"].mean()),
            "delta_avg_pnl": float(b["trade_pnl"].mean() - a["trade_pnl"].mean()),
            "b46_sig_quality_a": float(a["b46_sig_quality"].mean()),
            "b46_sig_quality_b": float(b["b46_sig_quality"].mean()),
            "delta_b46_sig_quality": float(b["b46_sig_quality"].mean() - a["b46_sig_quality"].mean()),
            "b51_reversal_score_a": float(a["b51_reversal_score"].mean()),
            "b51_reversal_score_b": float(b["b51_reversal_score"].mean()),
            "delta_b51_reversal_score": float(b["b51_reversal_score"].mean() - a["b51_reversal_score"].mean()),
            "b53_trendbar_strength_a": float(a["b53_trendbar_strength"].mean()),
            "b53_trendbar_strength_b": float(b["b53_trendbar_strength"].mean()),
            "delta_b53_trendbar_strength": float(b["b53_trendbar_strength"].mean() - a["b53_trendbar_strength"].mean()),
            "b53_doji_flag_a": float(a["b53_doji_flag"].mean()),
            "b53_doji_flag_b": float(b["b53_doji_flag"].mean()),
            "delta_b53_doji_flag": float(b["b53_doji_flag"].mean() - a["b53_doji_flag"].mean()),
        }

    rows2 = []
    for flag_col, a_val, b_val, name in [
        ("stage_active", 0, 1, "stage23_vs_stage01"),
        ("reclaim_flag", 0, 1, "reclaim1_vs_0"),
    ]:
        a = all_df[all_df[flag_col].eq(a_val)].copy()
        b = all_df[all_df[flag_col].eq(b_val)].copy()
        rows2.append(_compare_frames(a, b, name))

    stage0 = all_df[all_df["stage"].eq(0)].copy()
    stage2 = all_df[all_df["stage"].eq(2)].copy()
    stage3 = all_df[all_df["stage"].eq(3)].copy()
    if not stage0.empty and not stage2.empty:
        rows2.append(_compare_frames(stage0, stage2, "stage2_vs_stage0"))
    if not stage0.empty and not stage3.empty:
        rows2.append(_compare_frames(stage0, stage3, "stage3_vs_stage0"))
    if not stage2.empty and not stage3.empty:
        rows2.append(_compare_frames(stage2, stage3, "stage3_vs_stage2"))
    delta = pd.DataFrame(rows2)
    delta.to_csv(out_dir / "b114_tuned_interaction_delta_20260611_v1.csv", index=False, encoding="utf-8-sig")

    print(out_dir / "b114_tuned_stage_summary_20260611_v1.csv")
    print(out_dir / "b114_tuned_interaction_delta_20260611_v1.csv")


if __name__ == "__main__":
    main()
