from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Audit TK-R4 USD overlap heterogeneity for the >=1 trigger.")
    p.add_argument(
        "--position_level_csv",
        default=str(
            Path("backtest_out")
            / "stage2"
            / "indicator_audit"
            / "20260611_b118_tk_r4_risk_corr_since2022_v1"
            / "b118_position_level_20260611_v1.csv"
        ),
    )
    p.add_argument(
        "--out_dir",
        default=str(Path("backtest_out") / "stage2" / "indicator_audit" / "20260611_b122_tk_r4_usd_overlap_heterogeneity_since2022_v1"),
    )
    p.add_argument("--date_tag", default="20260611")
    p.add_argument("--half_risk_scale", type=float, default=0.5)
    p.add_argument("--support_min", type=int, default=3)
    return p.parse_args()


def _safe_mean(s: pd.Series) -> float:
    s2 = pd.to_numeric(s, errors="coerce")
    return float(s2.mean()) if len(s2) else float("nan")


def _safe_median(s: pd.Series) -> float:
    s2 = pd.to_numeric(s, errors="coerce")
    return float(s2.median()) if len(s2) else float("nan")


def _max_drawdown_from_pnl(pnl: pd.Series) -> float:
    x = pd.to_numeric(pnl, errors="coerce").fillna(0.0)
    if x.empty:
        return 0.0
    equity = x.cumsum()
    peak = equity.cummax()
    dd = equity - peak
    return float(dd.min()) if len(dd) else 0.0


def _agg(df: pd.DataFrame, pnl_col: str, risk_col: str) -> dict[str, float]:
    pnl = pd.to_numeric(df[pnl_col], errors="coerce")
    risk = pd.to_numeric(df[risk_col], errors="coerce")
    risk_sum = float(risk.sum()) if len(risk) else 0.0
    return {
        "n": float(len(df)),
        "sum_pnl": float(pnl.sum()) if len(pnl) else 0.0,
        "avg_pnl": _safe_mean(pnl),
        "median_pnl": _safe_median(pnl),
        "sum_risk_amt": risk_sum,
        "avg_r_mult": float(pnl.sum() / risk_sum) if risk_sum > 0.0 else float("nan"),
        "win_rate": _safe_mean((pnl > 0.0).astype(float)),
        "max_drawdown_pnl": _max_drawdown_from_pnl(pnl),
    }


def _build_rows(df: pd.DataFrame, half_risk_scale: float) -> pd.DataFrame:
    out = df.copy()
    out["usd_overlap_flag"] = out["usd_overlap_flag"].astype(bool)
    out["risk_scale_usd_ge1"] = 1.0
    out.loc[out["usd_overlap_flag"], "risk_scale_usd_ge1"] = float(half_risk_scale)
    out["position_pnl_usd_ge1"] = pd.to_numeric(out["position_pnl"], errors="coerce") * pd.to_numeric(
        out["risk_scale_usd_ge1"], errors="coerce"
    )
    out["risk_amt_usd_ge1"] = pd.to_numeric(out["risk_amt"], errors="coerce") * pd.to_numeric(
        out["risk_scale_usd_ge1"], errors="coerce"
    )
    return out


def _summary_for_group(sub: pd.DataFrame, group_cols: dict[str, object]) -> dict[str, object]:
    base = _agg(sub, "position_pnl", "risk_amt")
    half = _agg(sub, "position_pnl_usd_ge1", "risk_amt_usd_ge1")
    flag = sub["usd_overlap_flag"].astype(bool)
    trig = sub.loc[flag].copy()
    non = sub.loc[~flag].copy()
    trig_base = _agg(trig, "position_pnl", "risk_amt")
    non_base = _agg(non, "position_pnl", "risk_amt")
    return {
        **group_cols,
        "n_total": base["n"],
        "n_trigger": trig_base["n"],
        "n_nontrigger": non_base["n"],
        "trigger_share": _safe_mean(flag.astype(float)),
        "sum_pnl_base": base["sum_pnl"],
        "sum_pnl_half": half["sum_pnl"],
        "delta_sum_pnl": half["sum_pnl"] - base["sum_pnl"],
        "avg_pnl_base": base["avg_pnl"],
        "avg_pnl_half": half["avg_pnl"],
        "delta_avg_pnl": half["avg_pnl"] - base["avg_pnl"],
        "avg_r_mult_base": base["avg_r_mult"],
        "avg_r_mult_half": half["avg_r_mult"],
        "delta_avg_r_mult": half["avg_r_mult"] - base["avg_r_mult"],
        "max_drawdown_pnl_base": base["max_drawdown_pnl"],
        "max_drawdown_pnl_half": half["max_drawdown_pnl"],
        "delta_max_drawdown_pnl": half["max_drawdown_pnl"] - base["max_drawdown_pnl"],
        "trigger_avg_pnl_base": trig_base["avg_pnl"],
        "nontrigger_avg_pnl_base": non_base["avg_pnl"],
        "trigger_avg_r_mult_base": trig_base["avg_r_mult"],
        "nontrigger_avg_r_mult_base": non_base["avg_r_mult"],
    }


def _group_summary(rows: pd.DataFrame, by: list[str]) -> pd.DataFrame:
    out_rows: list[dict[str, object]] = []
    for keys, sub in rows.groupby(by, sort=True):
        if not isinstance(keys, tuple):
            keys = (keys,)
        group_cols = {by[i]: keys[i] for i in range(len(by))}
        out_rows.append(_summary_for_group(sub, group_cols))
    return pd.DataFrame(out_rows)


def _breadth_summary(symbol_df: pd.DataFrame, profile_symbol_df: pd.DataFrame, support_min: int) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for split, sub in symbol_df.groupby("split", sort=True):
        eligible = sub[sub["n_trigger"] >= float(support_min)].copy()
        rows.append(
            {
                "scope": "symbol",
                "split": str(split),
                "support_min": int(support_min),
                "n_groups": float(len(sub)),
                "n_eligible": float(len(eligible)),
                "n_delta_sum_positive": float((eligible["delta_sum_pnl"] > 0.0).sum()),
                "n_delta_dd_positive": float((eligible["delta_max_drawdown_pnl"] > 0.0).sum()),
                "n_both_positive": float(((eligible["delta_sum_pnl"] > 0.0) & (eligible["delta_max_drawdown_pnl"] > 0.0)).sum()),
            }
        )
    for split, sub in profile_symbol_df.groupby("split", sort=True):
        eligible = sub[sub["n_trigger"] >= float(support_min)].copy()
        rows.append(
            {
                "scope": "profile_symbol",
                "split": str(split),
                "support_min": int(support_min),
                "n_groups": float(len(sub)),
                "n_eligible": float(len(eligible)),
                "n_delta_sum_positive": float((eligible["delta_sum_pnl"] > 0.0).sum()),
                "n_delta_dd_positive": float((eligible["delta_max_drawdown_pnl"] > 0.0).sum()),
                "n_both_positive": float(((eligible["delta_sum_pnl"] > 0.0) & (eligible["delta_max_drawdown_pnl"] > 0.0)).sum()),
            }
        )
    return pd.DataFrame(rows)


def _format_terminal_summary(profile_df: pd.DataFrame, breadth_df: pd.DataFrame) -> str:
    lines = ["usd_overlap_heterogeneity"]
    for _, r in profile_df.sort_values(["split", "profile"], kind="mergesort").iterrows():
        lines.append(
            "  "
            + f"{r['split']} {r['profile']}: "
            + f"trigger_share={float(r['trigger_share']):.2%}, "
            + f"delta_sum_pnl={float(r['delta_sum_pnl']):+.2f}, "
            + f"delta_max_dd={float(r['delta_max_drawdown_pnl']):+.2f}, "
            + f"delta_avg_r={float(r['delta_avg_r_mult']):+.6f}"
        )
    for _, r in breadth_df.sort_values(["scope", "split"], kind="mergesort").iterrows():
        lines.append(
            "  "
            + f"{r['scope']} {r['split']}: "
            + f"eligible={int(r['n_eligible'])}, "
            + f"both_positive={int(r['n_both_positive'])}"
        )
    return "\n".join(lines)


def format_terminal_heterogeneity_summary(profile_df: pd.DataFrame, breadth_df: pd.DataFrame) -> str:
    return _format_terminal_summary(profile_df, breadth_df)


def run_heterogeneity(
    position_level_csv: str | Path,
    out_dir: str | Path,
    date_tag: str,
    half_risk_scale: float,
    support_min: int,
) -> tuple[Path, Path, Path, Path, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    date_tag = str(date_tag).strip()

    df = pd.read_csv(position_level_csv)
    if df.empty:
        rows = pd.DataFrame()
    else:
        df["entry_time"] = pd.to_datetime(df["entry_time"], errors="coerce")
        rows = _build_rows(df, half_risk_scale=float(half_risk_scale))
        rows = rows.sort_values(["split", "profile", "entry_time", "symbol"], kind="mergesort").reset_index(drop=True)

    profile_df = _group_summary(rows, ["split", "profile"])
    symbol_df = _group_summary(rows, ["split", "symbol"])
    profile_symbol_df = _group_summary(rows, ["split", "profile", "symbol"])
    breadth_df = _breadth_summary(symbol_df, profile_symbol_df, support_min=int(support_min))

    out_profile = out_dir / f"b122_usd_overlap_by_profile_{date_tag}_v1.csv"
    out_symbol = out_dir / f"b122_usd_overlap_by_symbol_{date_tag}_v1.csv"
    out_profile_symbol = out_dir / f"b122_usd_overlap_profile_symbol_{date_tag}_v1.csv"
    out_breadth = out_dir / f"b122_usd_overlap_breadth_{date_tag}_v1.csv"

    profile_df.to_csv(out_profile, index=False, encoding="utf-8-sig")
    symbol_df.to_csv(out_symbol, index=False, encoding="utf-8-sig")
    profile_symbol_df.to_csv(out_profile_symbol, index=False, encoding="utf-8-sig")
    breadth_df.to_csv(out_breadth, index=False, encoding="utf-8-sig")
    return out_profile, out_symbol, out_profile_symbol, out_breadth, rows, profile_df, symbol_df, profile_symbol_df, breadth_df


def main() -> None:
    args = parse_args()
    date_tag = str(args.date_tag).strip()
    support_min = int(args.support_min)
    half_risk_scale = float(args.half_risk_scale)

    out_profile, out_symbol, out_profile_symbol, out_breadth, _rows, profile_df, _symbol_df, _profile_symbol_df, breadth_df = (
        run_heterogeneity(
            position_level_csv=args.position_level_csv,
            out_dir=args.out_dir,
            date_tag=date_tag,
            half_risk_scale=half_risk_scale,
            support_min=support_min,
        )
    )

    print(format_terminal_heterogeneity_summary(profile_df, breadth_df))
    print(out_profile)
    print(out_symbol)
    print(out_profile_symbol)
    print(out_breadth)


if __name__ == "__main__":
    main()
