from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit TK-R2 trade-level stage split and profile x symbol stability.")
    parser.add_argument(
        "--trade_level_csv",
        default=str(
            Path("backtest_out")
            / "stage2"
            / "indicator_audit"
            / "20260611_b115_tk_r2_pullback_all_v1"
            / "b115_trade_level_20260611_v1.csv"
        ),
    )
    parser.add_argument(
        "--out_dir",
        default=str(Path("backtest_out") / "stage2" / "indicator_audit" / "20260611_b115_tk_r2_pullback_all_v1"),
    )
    return parser.parse_args()


def _safe_mean(df: pd.DataFrame, col: str) -> float:
    s = pd.to_numeric(df[col], errors="coerce")
    return float(s.mean()) if not s.empty else float("nan")


def _safe_median(df: pd.DataFrame, col: str) -> float:
    s = pd.to_numeric(df[col], errors="coerce")
    return float(s.median()) if not s.empty else float("nan")


def _agg_frame(df: pd.DataFrame) -> dict[str, float]:
    return {
        "n": float(len(df)),
        "avg_pnl": _safe_mean(df, "trade_pnl"),
        "median_pnl": _safe_median(df, "trade_pnl"),
        "win_rate": _safe_mean(df, "win"),
        "stop_loss_rate": _safe_mean(df, "stop_loss_any"),
        "tp2_rate": _safe_mean(df, "tp2_any"),
        "entry_score": _safe_mean(df, "entry_score"),
        "e1_break_strength_atr": _safe_mean(df, "e1_break_strength_atr"),
        "zone_hit_rate": _safe_mean(df, "tk_r2_zone_hit_flag_1h"),
        "cancel_rate": _safe_mean(df, "tk_r2_cancel_no_retrace_flag_1h"),
    }


def _compare_frames(a: pd.DataFrame, b: pd.DataFrame, name: str) -> dict[str, float | str]:
    agg_a = _agg_frame(a)
    agg_b = _agg_frame(b)
    return {
        "comparison": name,
        "n_a": agg_a["n"],
        "n_b": agg_b["n"],
        "avg_pnl_a": agg_a["avg_pnl"],
        "avg_pnl_b": agg_b["avg_pnl"],
        "delta_avg_pnl": agg_b["avg_pnl"] - agg_a["avg_pnl"],
        "median_pnl_a": agg_a["median_pnl"],
        "median_pnl_b": agg_b["median_pnl"],
        "delta_median_pnl": agg_b["median_pnl"] - agg_a["median_pnl"],
        "win_rate_a": agg_a["win_rate"],
        "win_rate_b": agg_b["win_rate"],
        "delta_win_rate": agg_b["win_rate"] - agg_a["win_rate"],
        "stop_loss_rate_a": agg_a["stop_loss_rate"],
        "stop_loss_rate_b": agg_b["stop_loss_rate"],
        "delta_stop_loss_rate": agg_b["stop_loss_rate"] - agg_a["stop_loss_rate"],
        "tp2_rate_a": agg_a["tp2_rate"],
        "tp2_rate_b": agg_b["tp2_rate"],
        "delta_tp2_rate": agg_b["tp2_rate"] - agg_a["tp2_rate"],
        "zone_hit_rate_a": agg_a["zone_hit_rate"],
        "zone_hit_rate_b": agg_b["zone_hit_rate"],
        "delta_zone_hit_rate": agg_b["zone_hit_rate"] - agg_a["zone_hit_rate"],
        "cancel_rate_a": agg_a["cancel_rate"],
        "cancel_rate_b": agg_b["cancel_rate"],
        "delta_cancel_rate": agg_b["cancel_rate"] - agg_a["cancel_rate"],
    }


def _flag_profile_symbol(df: pd.DataFrame, flag_col: str, flag_name: str) -> pd.DataFrame:
    rows: list[dict[str, float | str | bool]] = []
    for (profile, symbol), sub in df.groupby(["profile", "symbol"], sort=True):
        flag1 = sub[sub[flag_col].eq(1)].copy()
        flag0 = sub[sub[flag_col].eq(0)].copy()
        rows.append(
            {
                "flag": flag_name,
                "profile": str(profile),
                "symbol": str(symbol),
                "n_all": float(len(sub)),
                "n_flag1": float(len(flag1)),
                "n_flag0": float(len(flag0)),
                "flag1_share_all": float(len(flag1) / len(sub)) if len(sub) else 0.0,
                "avg_pnl_flag1": _safe_mean(flag1, "trade_pnl"),
                "avg_pnl_flag0": _safe_mean(flag0, "trade_pnl"),
                "delta_avg_pnl": _safe_mean(flag1, "trade_pnl") - _safe_mean(flag0, "trade_pnl"),
                "median_pnl_flag1": _safe_median(flag1, "trade_pnl"),
                "median_pnl_flag0": _safe_median(flag0, "trade_pnl"),
                "delta_median_pnl": _safe_median(flag1, "trade_pnl") - _safe_median(flag0, "trade_pnl"),
                "win_rate_flag1": _safe_mean(flag1, "win"),
                "win_rate_flag0": _safe_mean(flag0, "win"),
                "stop_loss_rate_flag1": _safe_mean(flag1, "stop_loss_any"),
                "stop_loss_rate_flag0": _safe_mean(flag0, "stop_loss_any"),
                "tp2_rate_flag1": _safe_mean(flag1, "tp2_any"),
                "tp2_rate_flag0": _safe_mean(flag0, "tp2_any"),
                "stage_mean_flag1": _safe_mean(flag1, "tk_r2_stage_1h"),
                "stage_mean_flag0": _safe_mean(flag0, "tk_r2_stage_1h"),
                "support_ge3": bool(len(flag1) >= 3),
                "support_ge5": bool(len(flag1) >= 5),
                "positive_avg_delta_ge3": bool(len(flag1) >= 3 and (_safe_mean(flag1, "trade_pnl") - _safe_mean(flag0, "trade_pnl")) > 0.0),
                "positive_avg_median_delta_ge3": bool(
                    len(flag1) >= 3
                    and (_safe_mean(flag1, "trade_pnl") - _safe_mean(flag0, "trade_pnl")) > 0.0
                    and (_safe_median(flag1, "trade_pnl") - _safe_median(flag0, "trade_pnl")) > 0.0
                ),
            }
        )
    out = pd.DataFrame(rows)
    if not out.empty:
        out = out.sort_values(
            ["n_flag1", "delta_avg_pnl", "delta_median_pnl"],
            ascending=[False, False, False],
            kind="mergesort",
        ).reset_index(drop=True)
    return out


def main() -> None:
    args = parse_args()
    trade_level_csv = Path(args.trade_level_csv)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(trade_level_csv)
    for col in [
        "trade_pnl",
        "win",
        "stop_loss_any",
        "tp2_any",
        "entry_score",
        "e1_break_strength_atr",
        "tk_r2_stage_1h",
        "tk_r2_zone_hit_flag_1h",
        "tk_r2_cancel_no_retrace_flag_1h",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df[df["tk_r2_stage_1h"].notna()].copy()
    df["stage"] = df["tk_r2_stage_1h"].astype(int)

    stage_summary = (
        df.groupby("stage", sort=True)
        .agg(
            n=("trade_pnl", "size"),
            avg_pnl=("trade_pnl", "mean"),
            median_pnl=("trade_pnl", "median"),
            win_rate=("win", "mean"),
            stop_loss_rate=("stop_loss_any", "mean"),
            tp2_rate=("tp2_any", "mean"),
            entry_score=("entry_score", "mean"),
            e1_break_strength_atr=("e1_break_strength_atr", "mean"),
            zone_hit_rate=("tk_r2_zone_hit_flag_1h", "mean"),
            cancel_rate=("tk_r2_cancel_no_retrace_flag_1h", "mean"),
        )
        .reset_index()
    )
    stage_summary.to_csv(out_dir / "b115_stage_split_summary_20260611_v1.csv", index=False, encoding="utf-8-sig")

    delta_rows: list[dict[str, float | str]] = []
    for a_stage, b_stage in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
        a = df[df["stage"].eq(a_stage)].copy()
        b = df[df["stage"].eq(b_stage)].copy()
        if a.empty or b.empty:
            continue
        delta_rows.append(_compare_frames(a, b, f"stage{b_stage}_vs_stage{a_stage}"))
    pd.DataFrame(delta_rows).to_csv(out_dir / "b115_stage_split_delta_20260611_v1.csv", index=False, encoding="utf-8-sig")

    stage_by_profile = (
        df.groupby(["profile", "stage"], sort=True)
        .agg(
            n=("trade_pnl", "size"),
            avg_pnl=("trade_pnl", "mean"),
            median_pnl=("trade_pnl", "median"),
            win_rate=("win", "mean"),
            stop_loss_rate=("stop_loss_any", "mean"),
            tp2_rate=("tp2_any", "mean"),
            zone_hit_rate=("tk_r2_zone_hit_flag_1h", "mean"),
            cancel_rate=("tk_r2_cancel_no_retrace_flag_1h", "mean"),
        )
        .reset_index()
        .sort_values(["stage", "n", "avg_pnl"], ascending=[True, False, False], kind="mergesort")
    )
    stage_by_profile.to_csv(out_dir / "b115_stage_by_profile_20260611_v1.csv", index=False, encoding="utf-8-sig")

    stage_by_symbol = (
        df.groupby(["symbol", "stage"], sort=True)
        .agg(
            n=("trade_pnl", "size"),
            avg_pnl=("trade_pnl", "mean"),
            median_pnl=("trade_pnl", "median"),
            win_rate=("win", "mean"),
            stop_loss_rate=("stop_loss_any", "mean"),
            tp2_rate=("tp2_any", "mean"),
            zone_hit_rate=("tk_r2_zone_hit_flag_1h", "mean"),
            cancel_rate=("tk_r2_cancel_no_retrace_flag_1h", "mean"),
        )
        .reset_index()
        .sort_values(["stage", "n", "avg_pnl"], ascending=[True, False, False], kind="mergesort")
    )
    stage_by_symbol.to_csv(out_dir / "b115_stage_by_symbol_20260611_v1.csv", index=False, encoding="utf-8-sig")

    zonehit_ps = _flag_profile_symbol(df, "tk_r2_zone_hit_flag_1h", "zone_hit")
    zonehit_ps.to_csv(out_dir / "b115_zonehit_profile_symbol_20260611_v1.csv", index=False, encoding="utf-8-sig")

    cancel_ps = _flag_profile_symbol(df, "tk_r2_cancel_no_retrace_flag_1h", "cancel_no_retrace")
    cancel_ps.to_csv(out_dir / "b115_cancel_profile_symbol_20260611_v1.csv", index=False, encoding="utf-8-sig")

    breadth_rows = []
    for flag_name, sub in [("zone_hit", zonehit_ps), ("cancel_no_retrace", cancel_ps)]:
        breadth_rows.append(
            {
                "flag": flag_name,
                "profile_symbol_total": float(len(sub)),
                "profile_symbol_ge1": float((sub["n_flag1"] >= 1).sum()),
                "profile_symbol_ge3": float((sub["n_flag1"] >= 3).sum()),
                "profile_symbol_ge5": float((sub["n_flag1"] >= 5).sum()),
                "positive_avg_delta_ge3": float(sub["positive_avg_delta_ge3"].sum()),
                "positive_avg_median_delta_ge3": float(sub["positive_avg_median_delta_ge3"].sum()),
            }
        )
    pd.DataFrame(breadth_rows).to_csv(out_dir / "b115_flag_breadth_20260611_v1.csv", index=False, encoding="utf-8-sig")

    print(out_dir / "b115_stage_split_summary_20260611_v1.csv")
    print(out_dir / "b115_stage_split_delta_20260611_v1.csv")
    print(out_dir / "b115_stage_by_profile_20260611_v1.csv")
    print(out_dir / "b115_stage_by_symbol_20260611_v1.csv")
    print(out_dir / "b115_zonehit_profile_symbol_20260611_v1.csv")
    print(out_dir / "b115_cancel_profile_symbol_20260611_v1.csv")
    print(out_dir / "b115_flag_breadth_20260611_v1.csv")


if __name__ == "__main__":
    main()
