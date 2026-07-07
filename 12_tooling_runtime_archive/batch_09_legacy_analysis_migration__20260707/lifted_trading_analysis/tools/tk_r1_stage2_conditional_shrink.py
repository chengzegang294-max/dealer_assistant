from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run TK-R1 stage2 conditional shrink audit.")
    parser.add_argument(
        "--interactions_csv",
        default=str(
            Path("backtest_out")
            / "stage2"
            / "indicator_audit"
            / "20260611_b114_tk_tp3_extension_tuned_v2"
            / "b114_tuned_trade_level_interactions_20260611_v1.csv"
        ),
    )
    parser.add_argument(
        "--out_dir",
        default=str(Path("backtest_out") / "stage2" / "indicator_audit" / "20260611_b114_tk_tp3_extension_tuned_v2"),
    )
    return parser.parse_args()


def _b46_focus_bin(x: float) -> str:
    if pd.isna(x):
        return "nan"
    if x <= 5:
        return "<=5"
    if x <= 8:
        return "(5,8]"
    if x <= 9:
        return "(8,9]"
    return ">=10"


def main() -> None:
    args = parse_args()
    interactions_csv = Path(args.interactions_csv)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(interactions_csv)
    s2 = df[df["stage"].eq(2)].copy()
    s2["b46_focus_bin"] = pd.to_numeric(s2["b46_sig_quality"], errors="coerce").map(_b46_focus_bin)

    agg_bins = (
        s2.groupby("b46_focus_bin")
        .agg(
            n=("trade_pnl", "size"),
            avg_pnl=("trade_pnl", "mean"),
            win_rate=("win", "mean"),
            tp2_rate=("tp2_any", "mean"),
            stop_loss_rate=("stop_loss_any", "mean"),
            b51=("b51_reversal_score", "mean"),
            b53=("b53_trendbar_strength", "mean"),
        )
        .reset_index()
    )
    agg_bins.to_csv(out_dir / "b114_stage2_b46_focus_bins_20260611_v1.csv", index=False, encoding="utf-8-sig")

    agg_profile_bin = (
        s2.groupby(["profile", "b46_focus_bin"])
        .agg(
            n=("trade_pnl", "size"),
            avg_pnl=("trade_pnl", "mean"),
            win_rate=("win", "mean"),
            tp2_rate=("tp2_any", "mean"),
            stop_loss_rate=("stop_loss_any", "mean"),
        )
        .reset_index()
        .sort_values(["profile", "b46_focus_bin"], kind="mergesort")
    )
    agg_profile_bin.to_csv(
        out_dir / "b114_stage2_profile_x_b46_focus_20260611_v1.csv", index=False, encoding="utf-8-sig"
    )

    mid = s2[s2["b46_focus_bin"].isin(["(5,8]", "(8,9]"])].copy()
    agg_mid_profiles = (
        mid.groupby("profile")
        .agg(
            n=("trade_pnl", "size"),
            avg_pnl=("trade_pnl", "mean"),
            win_rate=("win", "mean"),
            tp2_rate=("tp2_any", "mean"),
            stop_loss_rate=("stop_loss_any", "mean"),
        )
        .reset_index()
        .sort_values(["avg_pnl", "n"], ascending=[False, False], kind="mergesort")
    )
    agg_mid_profiles.to_csv(
        out_dir / "b114_stage2_midbin_profiles_20260611_v1.csv", index=False, encoding="utf-8-sig"
    )

    print(out_dir / "b114_stage2_b46_focus_bins_20260611_v1.csv")
    print(out_dir / "b114_stage2_profile_x_b46_focus_20260611_v1.csv")
    print(out_dir / "b114_stage2_midbin_profiles_20260611_v1.csv")


if __name__ == "__main__":
    main()
