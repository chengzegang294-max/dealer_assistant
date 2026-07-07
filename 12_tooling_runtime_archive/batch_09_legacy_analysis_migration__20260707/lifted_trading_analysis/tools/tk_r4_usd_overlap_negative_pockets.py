from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build negative pocket watchlists from TK-R4 USD overlap heterogeneity outputs.")
    p.add_argument(
        "--since_symbol_csv",
        default=str(
            Path("backtest_out")
            / "stage2"
            / "indicator_audit"
            / "20260611_b122_tk_r4_usd_overlap_heterogeneity_since2022_v1"
            / "b122_usd_overlap_by_symbol_20260611_v1.csv"
        ),
    )
    p.add_argument(
        "--pre_symbol_csv",
        default=str(
            Path("backtest_out")
            / "stage2"
            / "indicator_audit"
            / "20260611_b122_tk_r4_usd_overlap_heterogeneity_pre2022_v1"
            / "b122_usd_overlap_by_symbol_20260611_v1.csv"
        ),
    )
    p.add_argument(
        "--since_profile_symbol_csv",
        default=str(
            Path("backtest_out")
            / "stage2"
            / "indicator_audit"
            / "20260611_b122_tk_r4_usd_overlap_heterogeneity_since2022_v1"
            / "b122_usd_overlap_profile_symbol_20260611_v1.csv"
        ),
    )
    p.add_argument(
        "--pre_profile_symbol_csv",
        default=str(
            Path("backtest_out")
            / "stage2"
            / "indicator_audit"
            / "20260611_b122_tk_r4_usd_overlap_heterogeneity_pre2022_v1"
            / "b122_usd_overlap_profile_symbol_20260611_v1.csv"
        ),
    )
    p.add_argument(
        "--out_dir",
        default=str(Path("backtest_out") / "stage2" / "indicator_audit" / "20260611_b123_tk_r4_usd_overlap_negative_pockets_v1"),
    )
    p.add_argument("--date_tag", default="20260611")
    p.add_argument("--support_min", type=int, default=3)
    return p.parse_args()


def _read_scope(csv_path: str | Path, scope: str, support_min: int) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    if df.empty:
        return df
    out = df.copy()
    out["scope"] = scope
    out = out[out["n_trigger"] >= float(support_min)].copy()
    if out.empty:
        return out
    out["group_key"] = out["symbol"].astype(str)
    if scope == "profile_symbol":
        out["group_key"] = out["profile"].astype(str) + "|" + out["symbol"].astype(str)
    out["fail_sum"] = pd.to_numeric(out["delta_sum_pnl"], errors="coerce") <= 0.0
    out["fail_dd"] = pd.to_numeric(out["delta_max_drawdown_pnl"], errors="coerce") <= 0.0
    out["fail_avg_r"] = pd.to_numeric(out["delta_avg_r_mult"], errors="coerce") <= 0.0
    out["fail_score"] = out[["fail_sum", "fail_dd", "fail_avg_r"]].astype(int).sum(axis=1)
    out["negative_bucket"] = "positive"
    out.loc[out["fail_avg_r"], "negative_bucket"] = "avg_r_only_negative"
    out.loc[out["fail_dd"], "negative_bucket"] = "dd_negative"
    out.loc[out["fail_sum"], "negative_bucket"] = "sum_negative"
    out.loc[out["fail_sum"] & out["fail_dd"], "negative_bucket"] = "sum_dd_negative"
    out.loc[out["fail_sum"] & out["fail_dd"] & out["fail_avg_r"], "negative_bucket"] = "sum_dd_avg_r_negative"
    out["negative_flag"] = out["fail_score"] > 0
    return out


def _negative_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    cols = [
        "scope",
        "split",
        "profile",
        "symbol",
        "group_key",
        "negative_bucket",
        "fail_score",
        "n_total",
        "n_trigger",
        "trigger_share",
        "delta_sum_pnl",
        "delta_max_drawdown_pnl",
        "delta_avg_r_mult",
        "trigger_avg_pnl_base",
        "nontrigger_avg_pnl_base",
        "trigger_avg_r_mult_base",
        "nontrigger_avg_r_mult_base",
    ]
    for col in cols:
        if col not in df.columns:
            df[col] = pd.NA
    out = df.loc[df["negative_flag"], cols].copy()
    out = out.sort_values(
        ["scope", "fail_score", "split", "negative_bucket", "delta_sum_pnl", "delta_max_drawdown_pnl"],
        ascending=[True, False, True, True, True, True],
        kind="mergesort",
    ).reset_index(drop=True)
    return out


def _watchlist(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    def summarize(sub: pd.DataFrame) -> pd.Series:
        return pd.Series(
            {
                "n_splits_flagged": float(sub["split"].nunique()),
                "flag_since2022": bool((sub["split"] == "since2022").any()),
                "flag_pre2022": bool((sub["split"] == "pre2022").any()),
                "max_fail_score": float(pd.to_numeric(sub["fail_score"], errors="coerce").max()),
                "worst_delta_sum_pnl": float(pd.to_numeric(sub["delta_sum_pnl"], errors="coerce").min()),
                "worst_delta_max_drawdown_pnl": float(pd.to_numeric(sub["delta_max_drawdown_pnl"], errors="coerce").min()),
                "worst_delta_avg_r_mult": float(pd.to_numeric(sub["delta_avg_r_mult"], errors="coerce").min()),
                "max_trigger_share": float(pd.to_numeric(sub["trigger_share"], errors="coerce").max()),
                "min_n_trigger": float(pd.to_numeric(sub["n_trigger"], errors="coerce").min()),
                "buckets": " | ".join(sorted(set(sub["negative_bucket"].astype(str)))),
            }
        )

    out = (
        df.groupby(["scope", "group_key"], dropna=False, sort=True)
        .apply(summarize)
        .reset_index()
    )
    out["priority"] = "watch"
    out.loc[(out["n_splits_flagged"] >= 2.0) & (out["max_fail_score"] >= 2.0), "priority"] = "high_watch"
    out.loc[(out["n_splits_flagged"] >= 2.0) & (out["max_fail_score"] >= 3.0), "priority"] = "persistent_hard_negative"
    out.loc[(out["n_splits_flagged"] == 1.0) & (out["max_fail_score"] >= 2.0), "priority"] = "single_split_hard_negative"
    out = out.sort_values(
        ["scope", "priority", "n_splits_flagged", "max_fail_score", "worst_delta_sum_pnl"],
        ascending=[True, True, False, False, True],
        kind="mergesort",
    ).reset_index(drop=True)
    return out


def _summary(neg_df: pd.DataFrame, watch_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for scope in ["symbol", "profile_symbol"]:
        neg_sub = neg_df.loc[neg_df["scope"] == scope].copy()
        watch_sub = watch_df.loc[watch_df["scope"] == scope].copy()
        rows.append(
            {
                "scope": scope,
                "n_negative_rows": float(len(neg_sub)),
                "n_distinct_groups": float(neg_sub["group_key"].nunique()) if not neg_sub.empty else 0.0,
                "n_persistent_groups": float((watch_sub["n_splits_flagged"] >= 2.0).sum()) if not watch_sub.empty else 0.0,
                "n_hard_negative_groups": float((watch_sub["max_fail_score"] >= 2.0).sum()) if not watch_sub.empty else 0.0,
            }
        )
    return pd.DataFrame(rows)


def _format_terminal_summary(summary_df: pd.DataFrame, watch_df: pd.DataFrame) -> str:
    lines = ["usd_overlap_negative_pockets"]
    for _, r in summary_df.iterrows():
        lines.append(
            "  "
            + f"{r['scope']}: "
            + f"negative_rows={int(r['n_negative_rows'])}, "
            + f"distinct_groups={int(r['n_distinct_groups'])}, "
            + f"persistent={int(r['n_persistent_groups'])}, "
            + f"hard={int(r['n_hard_negative_groups'])}"
        )
    top = watch_df.head(8)
    for _, r in top.iterrows():
        lines.append(
            "  "
            + f"{r['scope']} {r['group_key']}: "
            + f"priority={r['priority']}, "
            + f"splits={int(r['n_splits_flagged'])}, "
            + f"worst_sum={float(r['worst_delta_sum_pnl']):+.2f}, "
            + f"worst_dd={float(r['worst_delta_max_drawdown_pnl']):+.2f}"
        )
    return "\n".join(lines)


def format_terminal_negative_pockets_summary(summary_df: pd.DataFrame, watch_df: pd.DataFrame) -> str:
    return _format_terminal_summary(summary_df, watch_df)


def run_negative_pockets(
    since_symbol_csv: str | Path,
    pre_symbol_csv: str | Path,
    since_profile_symbol_csv: str | Path,
    pre_profile_symbol_csv: str | Path,
    out_dir: str | Path,
    date_tag: str,
    support_min: int,
) -> tuple[Path, Path, Path, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    date_tag = str(date_tag).strip()
    support_min = int(support_min)

    parts = [
        _read_scope(since_symbol_csv, scope="symbol", support_min=support_min),
        _read_scope(pre_symbol_csv, scope="symbol", support_min=support_min),
        _read_scope(since_profile_symbol_csv, scope="profile_symbol", support_min=support_min),
        _read_scope(pre_profile_symbol_csv, scope="profile_symbol", support_min=support_min),
    ]
    all_df = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()
    neg_df = _negative_rows(all_df)
    watch_df = _watchlist(neg_df)
    summary_df = _summary(neg_df, watch_df)

    out_neg = out_dir / f"b123_usd_overlap_negative_pockets_{date_tag}_v1.csv"
    out_watch = out_dir / f"b123_usd_overlap_negative_watchlist_{date_tag}_v1.csv"
    out_sum = out_dir / f"b123_usd_overlap_negative_summary_{date_tag}_v1.csv"

    neg_df.to_csv(out_neg, index=False, encoding="utf-8-sig")
    watch_df.to_csv(out_watch, index=False, encoding="utf-8-sig")
    summary_df.to_csv(out_sum, index=False, encoding="utf-8-sig")
    return out_neg, out_watch, out_sum, neg_df, watch_df, summary_df


def main() -> None:
    args = parse_args()
    date_tag = str(args.date_tag).strip()
    support_min = int(args.support_min)

    out_neg, out_watch, out_sum, _neg_df, watch_df, summary_df = run_negative_pockets(
        since_symbol_csv=args.since_symbol_csv,
        pre_symbol_csv=args.pre_symbol_csv,
        since_profile_symbol_csv=args.since_profile_symbol_csv,
        pre_profile_symbol_csv=args.pre_profile_symbol_csv,
        out_dir=args.out_dir,
        date_tag=date_tag,
        support_min=support_min,
    )

    print(format_terminal_negative_pockets_summary(summary_df, watch_df))
    print(out_neg)
    print(out_watch)
    print(out_sum)


if __name__ == "__main__":
    main()
