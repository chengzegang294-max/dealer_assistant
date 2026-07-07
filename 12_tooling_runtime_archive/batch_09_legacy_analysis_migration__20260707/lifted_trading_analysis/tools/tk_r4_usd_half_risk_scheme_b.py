from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def default_position_level_csv(split: str, date_tag: str) -> Path:
    split_key = str(split).strip().lower()
    if split_key not in {"since2022", "pre2022"}:
        raise ValueError(f"Unsupported split: {split}")
    return (
        Path("backtest_out")
        / "stage2"
        / "indicator_audit"
        / f"{date_tag}_b118_tk_r4_risk_corr_{split_key}_v1"
        / f"b118_position_level_{date_tag}_v1.csv"
    )


def default_out_dir(split: str, enable_usd_half_risk: bool, date_tag: str) -> Path:
    split_key = str(split).strip().lower()
    if split_key not in {"since2022", "pre2022"}:
        raise ValueError(f"Unsupported split: {split}")
    mode = "on" if enable_usd_half_risk else "off"
    return (
        Path("backtest_out")
        / "stage2"
        / "indicator_audit"
        / f"{date_tag}_b120_tk_r4_usd_half_risk_scheme_b_{split_key}_{mode}_v1"
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Draft Scheme B shell for TK-R4 USD-only half-risk.")
    p.add_argument(
        "--position_level_csv",
        default=str(default_position_level_csv(split="since2022", date_tag="20260611")),
    )
    p.add_argument(
        "--out_dir",
        default=str(default_out_dir(split="since2022", enable_usd_half_risk=False, date_tag="20260611")),
    )
    p.add_argument("--date_tag", default="20260611")
    p.add_argument("--enable_usd_half_risk", type=int, default=0)
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


def _build_rows(df: pd.DataFrame, enable_usd_half_risk: bool, half_risk_scale: float) -> pd.DataFrame:
    out = df.copy()
    out["scheme_b_name"] = "tk_r4_usd_half_risk"
    out["scheme_b_enabled"] = bool(enable_usd_half_risk)
    out["scheme_b_trigger_flag"] = out["usd_overlap_flag"].astype(bool)
    out["scheme_b_trigger_reason"] = ""
    out.loc[out["scheme_b_trigger_flag"], "scheme_b_trigger_reason"] = "usd_overlap_flag"
    out["scheme_b_risk_scale"] = 1.0
    if enable_usd_half_risk:
        out.loc[out["scheme_b_trigger_flag"], "scheme_b_risk_scale"] = float(half_risk_scale)
    out["position_pnl_scheme_b"] = pd.to_numeric(out["position_pnl"], errors="coerce") * pd.to_numeric(
        out["scheme_b_risk_scale"], errors="coerce"
    )
    out["risk_amt_scheme_b"] = pd.to_numeric(out["risk_amt"], errors="coerce") * pd.to_numeric(
        out["scheme_b_risk_scale"], errors="coerce"
    )
    return out


def _summary(df: pd.DataFrame) -> pd.DataFrame:
    base = _agg(df, "position_pnl", "risk_amt")
    scheme = _agg(df, "position_pnl_scheme_b", "risk_amt_scheme_b")
    return pd.DataFrame(
        [
            {"scenario": "baseline", **base},
            {"scenario": "scheme_b", **scheme},
            {
                "scenario": "scheme_b_minus_base",
                "n": scheme["n"] - base["n"],
                "sum_pnl": scheme["sum_pnl"] - base["sum_pnl"],
                "avg_pnl": scheme["avg_pnl"] - base["avg_pnl"],
                "median_pnl": scheme["median_pnl"] - base["median_pnl"],
                "sum_risk_amt": scheme["sum_risk_amt"] - base["sum_risk_amt"],
                "avg_r_mult": scheme["avg_r_mult"] - base["avg_r_mult"],
                "win_rate": scheme["win_rate"] - base["win_rate"],
                "max_drawdown_pnl": scheme["max_drawdown_pnl"] - base["max_drawdown_pnl"],
            },
        ]
    )


def _config_row(df: pd.DataFrame, enable_usd_half_risk: bool, half_risk_scale: float) -> pd.DataFrame:
    trigger_share = _safe_mean(df["scheme_b_trigger_flag"].astype(float)) if not df.empty else float("nan")
    return pd.DataFrame(
        [
            {
                "scheme_b_name": "tk_r4_usd_half_risk",
                "scheme_b_enabled": bool(enable_usd_half_risk),
                "enabled_default": False,
                "trigger_col": "usd_overlap_flag",
                "trigger_theme": "usd",
                "risk_scale_when_triggered": float(half_risk_scale),
                "position_level_csv": "",
                "trigger_share": trigger_share,
                "notes": "Draft Scheme B shell only. Keeps baseline default unchanged; accounting/audit only.",
            }
        ]
    )


def _summary_map(summary_df: pd.DataFrame, scenario: str) -> dict[str, float]:
    sub = summary_df.loc[summary_df["scenario"] == scenario]
    if sub.empty:
        return {}
    row = sub.iloc[0].to_dict()
    out: dict[str, float] = {}
    for k, v in row.items():
        if k == "scenario":
            continue
        out[str(k)] = float(v) if pd.notna(v) else float("nan")
    return out


def format_terminal_summary(summary_df: pd.DataFrame, split: str | None = None, enabled: bool | None = None) -> str:
    label = []
    if split is not None:
        label.append(f"split={split}")
    if enabled is not None:
        label.append(f"enabled={int(enabled)}")
    header = " ".join(label) if label else "scheme_b"

    base = _summary_map(summary_df, "baseline")
    scheme = _summary_map(summary_df, "scheme_b")
    delta = _summary_map(summary_df, "scheme_b_minus_base")
    if not base or not scheme or not delta:
        return f"{header}\n  summary unavailable"

    return "\n".join(
        [
            header,
            (
                "  baseline: "
                f"sum_pnl={base['sum_pnl']:.2f}, "
                f"max_dd={base['max_drawdown_pnl']:.2f}, "
                f"avg_r={base['avg_r_mult']:.6f}"
            ),
            (
                "  scheme_b: "
                f"sum_pnl={scheme['sum_pnl']:.2f}, "
                f"max_dd={scheme['max_drawdown_pnl']:.2f}, "
                f"avg_r={scheme['avg_r_mult']:.6f}"
            ),
            (
                "  delta: "
                f"sum_pnl={delta['sum_pnl']:+.2f}, "
                f"max_dd={delta['max_drawdown_pnl']:+.2f}, "
                f"avg_r={delta['avg_r_mult']:+.6f}"
            ),
        ]
    )


def run_scheme_b(
    position_level_csv: str | Path,
    out_dir: str | Path,
    date_tag: str,
    enable_usd_half_risk: bool,
    half_risk_scale: float,
) -> tuple[Path, Path, Path, pd.DataFrame]:
    position_level_csv = Path(position_level_csv)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(position_level_csv)
    if df.empty:
        rows = pd.DataFrame()
    else:
        df["entry_time"] = pd.to_datetime(df["entry_time"], errors="coerce")
        rows = _build_rows(df, enable_usd_half_risk=enable_usd_half_risk, half_risk_scale=half_risk_scale)
        rows = rows.sort_values(["split", "profile", "entry_time", "symbol"], kind="mergesort").reset_index(drop=True)

    out_cfg = out_dir / f"b120_scheme_b_config_{date_tag}_v1.csv"
    out_rows = out_dir / f"b120_scheme_b_position_level_{date_tag}_v1.csv"
    out_sum = out_dir / f"b120_scheme_b_summary_{date_tag}_v1.csv"

    cfg = _config_row(rows, enable_usd_half_risk=enable_usd_half_risk, half_risk_scale=half_risk_scale)
    cfg.loc[0, "position_level_csv"] = str(position_level_csv)

    summary_df = _summary(rows)
    cfg.to_csv(out_cfg, index=False, encoding="utf-8-sig")
    rows.to_csv(out_rows, index=False, encoding="utf-8-sig")
    summary_df.to_csv(out_sum, index=False, encoding="utf-8-sig")
    return out_cfg, out_rows, out_sum, summary_df


def main() -> None:
    args = parse_args()
    date_tag = str(args.date_tag).strip()
    enable_usd_half_risk = bool(int(args.enable_usd_half_risk))
    half_risk_scale = float(args.half_risk_scale)
    out_cfg, out_rows, out_sum, summary_df = run_scheme_b(
        position_level_csv=args.position_level_csv,
        out_dir=args.out_dir,
        date_tag=date_tag,
        enable_usd_half_risk=enable_usd_half_risk,
        half_risk_scale=half_risk_scale,
    )

    print(format_terminal_summary(summary_df, enabled=enable_usd_half_risk))
    print(out_cfg)
    print(out_rows)
    print(out_sum)


if __name__ == "__main__":
    main()
