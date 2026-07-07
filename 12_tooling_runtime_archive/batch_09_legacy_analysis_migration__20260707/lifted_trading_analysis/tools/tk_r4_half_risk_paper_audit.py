from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Paper audit TK-R4 same-theme half-risk rule using b118 position-level output.")
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
        default=str(Path("backtest_out") / "stage2" / "indicator_audit" / "20260611_b119_tk_r4_half_risk_since2022_v1"),
    )
    p.add_argument("--date_tag", default="20260611")
    p.add_argument("--theme", default="any", choices=["any", "usd", "commodity"])
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
    return {
        "n": float(len(df)),
        "sum_pnl": float(pnl.sum()) if len(pnl) else 0.0,
        "avg_pnl": _safe_mean(pnl),
        "median_pnl": _safe_median(pnl),
        "sum_risk_amt": float(risk.sum()) if len(risk) else 0.0,
        "avg_r_mult": float(pnl.sum() / risk.sum()) if float(risk.sum()) > 0.0 else float("nan"),
        "win_rate": _safe_mean((pnl > 0.0).astype(float)),
        "max_drawdown_pnl": _max_drawdown_from_pnl(pnl),
    }


def _theme_flag(df: pd.DataFrame, theme: str) -> pd.Series:
    if theme == "usd":
        return df["usd_overlap_flag"].astype(bool)
    if theme == "commodity":
        return df["commodity_overlap_flag"].astype(bool)
    return df["any_corr_overlap_flag"].astype(bool)


def _build_rows(df: pd.DataFrame, theme: str) -> pd.DataFrame:
    flag = _theme_flag(df, theme)
    out = df.copy()
    out["theme_flag"] = flag.astype(bool)
    out["risk_scale_half_rule"] = 0.5
    out.loc[~out["theme_flag"], "risk_scale_half_rule"] = 1.0
    out["position_pnl_half_rule"] = pd.to_numeric(out["position_pnl"], errors="coerce") * pd.to_numeric(out["risk_scale_half_rule"], errors="coerce")
    out["risk_amt_half_rule"] = pd.to_numeric(out["risk_amt"], errors="coerce") * pd.to_numeric(out["risk_scale_half_rule"], errors="coerce")
    return out


def _overall_summary(df: pd.DataFrame) -> pd.DataFrame:
    base = _agg(df, "position_pnl", "risk_amt")
    half = _agg(df, "position_pnl_half_rule", "risk_amt_half_rule")
    return pd.DataFrame(
        [
            {"scenario": "baseline", **base},
            {"scenario": "half_rule", **half},
            {
                "scenario": "half_minus_base",
                "n": half["n"] - base["n"],
                "sum_pnl": half["sum_pnl"] - base["sum_pnl"],
                "avg_pnl": half["avg_pnl"] - base["avg_pnl"],
                "median_pnl": half["median_pnl"] - base["median_pnl"],
                "sum_risk_amt": half["sum_risk_amt"] - base["sum_risk_amt"],
                "avg_r_mult": half["avg_r_mult"] - base["avg_r_mult"],
                "win_rate": half["win_rate"] - base["win_rate"],
                "max_drawdown_pnl": half["max_drawdown_pnl"] - base["max_drawdown_pnl"],
            },
        ]
    )


def _by_profile_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, float | str]] = []
    for (split, profile), sub in df.groupby(["split", "profile"], sort=True):
        base = _agg(sub, "position_pnl", "risk_amt")
        half = _agg(sub, "position_pnl_half_rule", "risk_amt_half_rule")
        rows.append(
            {
                "split": str(split),
                "profile": str(profile),
                "n": base["n"],
                "theme_overlap_share": _safe_mean(sub["theme_flag"].astype(float)),
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
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    date_tag = str(args.date_tag).strip()
    theme = str(args.theme).strip().lower()

    df = pd.read_csv(args.position_level_csv)
    if df.empty:
        rows = pd.DataFrame()
    else:
        df["entry_time"] = pd.to_datetime(df["entry_time"], errors="coerce")
        rows = _build_rows(df, theme).sort_values(["split", "profile", "entry_time", "symbol"], kind="mergesort").reset_index(drop=True)

    out_rows = out_dir / f"b119_half_risk_position_level_{date_tag}_v1.csv"
    out_sum = out_dir / f"b119_half_risk_summary_{date_tag}_v1.csv"
    out_prof = out_dir / f"b119_half_risk_by_profile_{date_tag}_v1.csv"

    rows.to_csv(out_rows, index=False, encoding="utf-8-sig")
    _overall_summary(rows).to_csv(out_sum, index=False, encoding="utf-8-sig")
    _by_profile_summary(rows).to_csv(out_prof, index=False, encoding="utf-8-sig")

    print(out_rows)
    print(out_sum)
    print(out_prof)


if __name__ == "__main__":
    main()

