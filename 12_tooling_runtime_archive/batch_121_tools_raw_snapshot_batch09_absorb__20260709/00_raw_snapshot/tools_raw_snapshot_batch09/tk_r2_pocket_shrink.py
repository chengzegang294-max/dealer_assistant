from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Shrink TK-R2 zone_hit positive pockets and cancel_no_retrace negative pockets.")
    parser.add_argument(
        "--out_dir",
        default=str(Path("backtest_out") / "stage2" / "indicator_audit" / "20260611_b115_tk_r2_pullback_all_v1"),
    )
    parser.add_argument("--date_tag", default="20260611")
    parser.add_argument("--min_support", type=int, default=3)
    parser.add_argument("--strong_support", type=int, default=5)
    parser.add_argument("--min_pos_delta_avg", type=float, default=0.0)
    parser.add_argument("--min_pos_delta_median", type=float, default=0.0)
    parser.add_argument("--max_neg_delta_avg", type=float, default=0.0)
    parser.add_argument("--max_neg_delta_median", type=float, default=0.0)
    return parser.parse_args()


def _coerce_numeric(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


def _tier(n_flag1: float, strong_support: int) -> str:
    try:
        n = int(n_flag1)
    except Exception:
        n = 0
    return "strong" if n >= int(strong_support) else "weak"


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    date_tag = str(args.date_tag).strip()

    zonehit_csv = out_dir / f"b115_zonehit_profile_symbol_{date_tag}_v1.csv"
    cancel_csv = out_dir / f"b115_cancel_profile_symbol_{date_tag}_v1.csv"

    zonehit = pd.read_csv(zonehit_csv)
    cancel = pd.read_csv(cancel_csv)

    num_cols = ["n_all", "n_flag1", "flag1_share_all", "delta_avg_pnl", "delta_median_pnl", "avg_pnl_flag1", "avg_pnl_flag0", "median_pnl_flag1", "median_pnl_flag0"]
    zonehit = _coerce_numeric(zonehit, num_cols)
    cancel = _coerce_numeric(cancel, num_cols)

    min_support = int(args.min_support)
    strong_support = int(args.strong_support)

    zonehit_pos = zonehit[
        (zonehit["n_flag1"] >= float(min_support))
        & (zonehit["delta_avg_pnl"] >= float(args.min_pos_delta_avg))
        & (zonehit["delta_median_pnl"] >= float(args.min_pos_delta_median))
    ].copy()
    zonehit_pos["direction"] = "positive"
    zonehit_pos["tier"] = zonehit_pos["n_flag1"].map(lambda x: _tier(x, strong_support))
    zonehit_pos["action"] = "pocket_keep_observe"
    if not zonehit_pos.empty:
        zonehit_pos = zonehit_pos.sort_values(
            ["tier", "delta_median_pnl", "delta_avg_pnl", "n_flag1"],
            ascending=[True, False, False, False],
            kind="mergesort",
        ).reset_index(drop=True)

    cancel_neg = cancel[
        (cancel["n_flag1"] >= float(min_support))
        & (cancel["delta_avg_pnl"] <= float(args.max_neg_delta_avg))
        & (cancel["delta_median_pnl"] <= float(args.max_neg_delta_median))
    ].copy()
    cancel_neg["direction"] = "negative"
    cancel_neg["tier"] = cancel_neg["n_flag1"].map(lambda x: _tier(x, strong_support))
    cancel_neg["action"] = "pocket_avoid_warn"
    if not cancel_neg.empty:
        cancel_neg = cancel_neg.sort_values(
            ["tier", "delta_median_pnl", "delta_avg_pnl", "n_flag1"],
            ascending=[True, True, True, False],
            kind="mergesort",
        ).reset_index(drop=True)

    out_zonehit = out_dir / f"b115_zonehit_positive_pockets_{date_tag}_v1.csv"
    out_cancel = out_dir / f"b115_cancel_negative_pockets_{date_tag}_v1.csv"
    out_summary = out_dir / f"b115_pocket_shrink_summary_{date_tag}_v1.csv"

    zonehit_pos.to_csv(out_zonehit, index=False, encoding="utf-8-sig")
    cancel_neg.to_csv(out_cancel, index=False, encoding="utf-8-sig")

    summary_rows = [
        {
            "flag": "zone_hit",
            "direction": "positive",
            "min_support": float(min_support),
            "strong_support": float(strong_support),
            "n_pockets": float(len(zonehit_pos)),
            "n_strong": float((zonehit_pos["tier"].eq("strong")).sum()) if not zonehit_pos.empty else 0.0,
        },
        {
            "flag": "cancel_no_retrace",
            "direction": "negative",
            "min_support": float(min_support),
            "strong_support": float(strong_support),
            "n_pockets": float(len(cancel_neg)),
            "n_strong": float((cancel_neg["tier"].eq("strong")).sum()) if not cancel_neg.empty else 0.0,
        },
    ]
    pd.DataFrame(summary_rows).to_csv(out_summary, index=False, encoding="utf-8-sig")

    print(out_zonehit)
    print(out_cancel)
    print(out_summary)


if __name__ == "__main__":
    main()

