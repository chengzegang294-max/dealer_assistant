from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Audit TK-R4 USD overlap depth thresholds using b118 position-level output.")
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
        default=str(Path("backtest_out") / "stage2" / "indicator_audit" / "20260611_b121_tk_r4_usd_overlap_depth_since2022_v1"),
    )
    p.add_argument("--date_tag", default="20260611")
    p.add_argument("--thresholds", default="1,2,3")
    p.add_argument("--half_risk_scale", type=float, default=0.5)
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


def _parse_thresholds(raw: str) -> list[int]:
    vals: list[int] = []
    for x in str(raw).split(","):
        x2 = x.strip()
        if not x2:
            continue
        vals.append(int(x2))
    vals = sorted(set(v for v in vals if v >= 1))
    if not vals:
        raise ValueError("No valid thresholds were provided.")
    return vals


def _build_rows(df: pd.DataFrame, thresholds: list[int], half_risk_scale: float) -> pd.DataFrame:
    out = df.copy()
    depth = pd.to_numeric(out["concurrent_usd_same_dir"], errors="coerce").fillna(0.0)
    for th in thresholds:
        flag_col = f"usd_overlap_ge_{th}_flag"
        scale_col = f"risk_scale_ge_{th}"
        pnl_col = f"position_pnl_ge_{th}"
        risk_col = f"risk_amt_ge_{th}"
        out[flag_col] = depth >= float(th)
        out[scale_col] = 1.0
        out.loc[out[flag_col], scale_col] = float(half_risk_scale)
        out[pnl_col] = pd.to_numeric(out["position_pnl"], errors="coerce") * pd.to_numeric(out[scale_col], errors="coerce")
        out[risk_col] = pd.to_numeric(out["risk_amt"], errors="coerce") * pd.to_numeric(out[scale_col], errors="coerce")
    return out


def _threshold_summary(rows: pd.DataFrame, thresholds: list[int]) -> pd.DataFrame:
    base = _agg(rows, "position_pnl", "risk_amt")
    out_rows: list[dict[str, float | int]] = []
    for th in thresholds:
        flag_col = f"usd_overlap_ge_{th}_flag"
        pnl_col = f"position_pnl_ge_{th}"
        risk_col = f"risk_amt_ge_{th}"
        half = _agg(rows, pnl_col, risk_col)
        out_rows.append(
            {
                "threshold": int(th),
                "trigger_share": _safe_mean(rows[flag_col].astype(float)),
                "n": base["n"],
                "sum_pnl_base": base["sum_pnl"],
                "sum_pnl_half": half["sum_pnl"],
                "delta_sum_pnl": half["sum_pnl"] - base["sum_pnl"],
                "avg_pnl_base": base["avg_pnl"],
                "avg_pnl_half": half["avg_pnl"],
                "delta_avg_pnl": half["avg_pnl"] - base["avg_pnl"],
                "sum_risk_amt_base": base["sum_risk_amt"],
                "sum_risk_amt_half": half["sum_risk_amt"],
                "delta_sum_risk_amt": half["sum_risk_amt"] - base["sum_risk_amt"],
                "avg_r_mult_base": base["avg_r_mult"],
                "avg_r_mult_half": half["avg_r_mult"],
                "delta_avg_r_mult": half["avg_r_mult"] - base["avg_r_mult"],
                "win_rate_base": base["win_rate"],
                "win_rate_half": half["win_rate"],
                "delta_win_rate": half["win_rate"] - base["win_rate"],
                "max_drawdown_pnl_base": base["max_drawdown_pnl"],
                "max_drawdown_pnl_half": half["max_drawdown_pnl"],
                "delta_max_drawdown_pnl": half["max_drawdown_pnl"] - base["max_drawdown_pnl"],
            }
        )
    return pd.DataFrame(out_rows)


def _threshold_by_profile(rows: pd.DataFrame, thresholds: list[int]) -> pd.DataFrame:
    out_rows: list[dict[str, float | int | str]] = []
    for th in thresholds:
        flag_col = f"usd_overlap_ge_{th}_flag"
        pnl_col = f"position_pnl_ge_{th}"
        risk_col = f"risk_amt_ge_{th}"
        for (split, profile), sub in rows.groupby(["split", "profile"], sort=True):
            base = _agg(sub, "position_pnl", "risk_amt")
            half = _agg(sub, pnl_col, risk_col)
            out_rows.append(
                {
                    "threshold": int(th),
                    "split": str(split),
                    "profile": str(profile),
                    "trigger_share": _safe_mean(sub[flag_col].astype(float)),
                    "n": base["n"],
                    "sum_pnl_base": base["sum_pnl"],
                    "sum_pnl_half": half["sum_pnl"],
                    "delta_sum_pnl": half["sum_pnl"] - base["sum_pnl"],
                    "avg_r_mult_base": base["avg_r_mult"],
                    "avg_r_mult_half": half["avg_r_mult"],
                    "delta_avg_r_mult": half["avg_r_mult"] - base["avg_r_mult"],
                    "max_drawdown_pnl_base": base["max_drawdown_pnl"],
                    "max_drawdown_pnl_half": half["max_drawdown_pnl"],
                    "delta_max_drawdown_pnl": half["max_drawdown_pnl"] - base["max_drawdown_pnl"],
                }
            )
    return pd.DataFrame(out_rows)


def _format_terminal_summary(summary_df: pd.DataFrame) -> str:
    if summary_df.empty:
        return "usd_overlap_depth\n  summary unavailable"
    lines = ["usd_overlap_depth"]
    for _, r in summary_df.sort_values("threshold", kind="mergesort").iterrows():
        lines.append(
            "  "
            + f"ge_{int(r['threshold'])}: "
            + f"trigger_share={float(r['trigger_share']):.2%}, "
            + f"delta_sum_pnl={float(r['delta_sum_pnl']):+.2f}, "
            + f"delta_max_dd={float(r['delta_max_drawdown_pnl']):+.2f}, "
            + f"delta_avg_r={float(r['delta_avg_r_mult']):+.6f}"
        )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    date_tag = str(args.date_tag).strip()
    thresholds = _parse_thresholds(args.thresholds)
    half_risk_scale = float(args.half_risk_scale)

    df = pd.read_csv(args.position_level_csv)
    if df.empty:
        rows = pd.DataFrame()
    else:
        df["entry_time"] = pd.to_datetime(df["entry_time"], errors="coerce")
        rows = _build_rows(df, thresholds=thresholds, half_risk_scale=half_risk_scale)
        rows = rows.sort_values(["split", "profile", "entry_time", "symbol"], kind="mergesort").reset_index(drop=True)

    out_rows = out_dir / f"b121_usd_depth_position_level_{date_tag}_v1.csv"
    out_sum = out_dir / f"b121_usd_depth_threshold_summary_{date_tag}_v1.csv"
    out_prof = out_dir / f"b121_usd_depth_by_profile_{date_tag}_v1.csv"

    summary_df = _threshold_summary(rows, thresholds=thresholds)
    by_profile_df = _threshold_by_profile(rows, thresholds=thresholds)
    rows.to_csv(out_rows, index=False, encoding="utf-8-sig")
    summary_df.to_csv(out_sum, index=False, encoding="utf-8-sig")
    by_profile_df.to_csv(out_prof, index=False, encoding="utf-8-sig")

    print(_format_terminal_summary(summary_df))
    print(out_rows)
    print(out_sum)
    print(out_prof)


if __name__ == "__main__":
    main()
