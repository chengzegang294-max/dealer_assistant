from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit TK-R1 tuned stage2 stability.")
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


def main() -> None:
    args = parse_args()
    interactions_csv = Path(args.interactions_csv)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(interactions_csv)
    stage0 = df[df["stage"].eq(0)].copy()
    stage2 = df[df["stage"].eq(2)].copy()

    overall_rows = []
    for col in [
        "trade_pnl",
        "win",
        "stop_loss_any",
        "tp2_any",
        "b46_sig_quality",
        "b51_reversal_score",
        "b53_trendbar_strength",
        "b53_doji_flag",
    ]:
        a = pd.to_numeric(stage0[col], errors="coerce")
        b = pd.to_numeric(stage2[col], errors="coerce")
        overall_rows.append(
            {
                "metric": col,
                "stage0": float(a.mean()),
                "stage2": float(b.mean()),
                "delta_stage2_minus_stage0": float(b.mean() - a.mean()),
            }
        )
    overall = pd.DataFrame(overall_rows)
    overall.to_csv(out_dir / "b114_stage2_overall_audit_20260611_v1.csv", index=False, encoding="utf-8-sig")

    by_symbol = (
        stage2.groupby("symbol")
        .agg(
            n=("trade_pnl", "size"),
            avg_pnl=("trade_pnl", "mean"),
            win_rate=("win", "mean"),
            tp2_rate=("tp2_any", "mean"),
            stop_loss_rate=("stop_loss_any", "mean"),
            b46_sig_quality=("b46_sig_quality", "mean"),
            b51_reversal_score=("b51_reversal_score", "mean"),
            b53_trendbar_strength=("b53_trendbar_strength", "mean"),
        )
        .reset_index()
        .sort_values(["n", "avg_pnl"], ascending=[False, False], kind="mergesort")
    )
    by_symbol.to_csv(out_dir / "b114_stage2_by_symbol_20260611_v1.csv", index=False, encoding="utf-8-sig")

    by_profile = (
        stage2.groupby("profile")
        .agg(
            n=("trade_pnl", "size"),
            avg_pnl=("trade_pnl", "mean"),
            win_rate=("win", "mean"),
            tp2_rate=("tp2_any", "mean"),
            stop_loss_rate=("stop_loss_any", "mean"),
            b46_sig_quality=("b46_sig_quality", "mean"),
            b51_reversal_score=("b51_reversal_score", "mean"),
            b53_trendbar_strength=("b53_trendbar_strength", "mean"),
        )
        .reset_index()
        .sort_values(["n", "avg_pnl"], ascending=[False, False], kind="mergesort")
    )
    by_profile.to_csv(out_dir / "b114_stage2_by_profile_20260611_v1.csv", index=False, encoding="utf-8-sig")

    breadth = pd.DataFrame(
        [
            {
                "stage2_n": float(len(stage2)),
                "stage2_share_all": float(len(stage2) / len(df)) if len(df) else 0.0,
                "symbols_total": float(by_symbol.shape[0]),
                "symbols_ge10": float((by_symbol["n"] >= 10).sum()),
                "symbols_positive_avg_pnl": float((by_symbol["avg_pnl"] > 0.0).sum()),
                "profiles_total": float(by_profile.shape[0]),
                "profiles_positive_avg_pnl": float((by_profile["avg_pnl"] > 0.0).sum()),
            }
        ]
    )
    breadth.to_csv(out_dir / "b114_stage2_breadth_20260611_v1.csv", index=False, encoding="utf-8-sig")

    bucket_rows = []
    for col in ["b46_sig_quality", "b51_reversal_score", "b53_trendbar_strength"]:
        s = pd.to_numeric(stage2[col], errors="coerce")
        if s.nunique() < 2:
            continue
        if s.nunique() >= 4:
            bucket = pd.qcut(s, q=4, duplicates="drop")
        else:
            bucket = s.astype(str)
        tmp = stage2.copy()
        tmp["bucket"] = bucket.astype(str)
        agg = (
            tmp.groupby("bucket")
            .agg(
                n=("trade_pnl", "size"),
                avg_pnl=("trade_pnl", "mean"),
                win_rate=("win", "mean"),
                tp2_rate=("tp2_any", "mean"),
                stop_loss_rate=("stop_loss_any", "mean"),
            )
            .reset_index()
        )
        agg.insert(0, "feature", col)
        bucket_rows.append(agg)
    if bucket_rows:
        pd.concat(bucket_rows, ignore_index=True).to_csv(
            out_dir / "b114_stage2_feature_buckets_20260611_v1.csv", index=False, encoding="utf-8-sig"
        )

    print(out_dir / "b114_stage2_overall_audit_20260611_v1.csv")
    print(out_dir / "b114_stage2_by_symbol_20260611_v1.csv")
    print(out_dir / "b114_stage2_by_profile_20260611_v1.csv")
    print(out_dir / "b114_stage2_breadth_20260611_v1.csv")
    print(out_dir / "b114_stage2_feature_buckets_20260611_v1.csv")


if __name__ == "__main__":
    main()
