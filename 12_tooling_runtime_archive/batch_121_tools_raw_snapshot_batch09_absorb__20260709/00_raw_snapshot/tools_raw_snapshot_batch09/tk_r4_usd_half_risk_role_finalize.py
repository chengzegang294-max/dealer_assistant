from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Finalize the current role contract for TK-R4 USD-only half-risk Scheme B.")
    p.add_argument(
        "--since_config_csv",
        default=str(
            Path("backtest_out")
            / "stage2"
            / "indicator_audit"
            / "20260611_b120_tk_r4_usd_half_risk_scheme_b_since2022_on_v1"
            / "b120_scheme_b_config_20260611_v1.csv"
        ),
    )
    p.add_argument(
        "--since_summary_csv",
        default=str(
            Path("backtest_out")
            / "stage2"
            / "indicator_audit"
            / "20260611_b120_tk_r4_usd_half_risk_scheme_b_since2022_on_v1"
            / "b120_scheme_b_summary_20260611_v1.csv"
        ),
    )
    p.add_argument(
        "--pre_summary_csv",
        default=str(
            Path("backtest_out")
            / "stage2"
            / "indicator_audit"
            / "20260611_b120_tk_r4_usd_half_risk_scheme_b_pre2022_on_v1"
            / "b120_scheme_b_summary_20260611_v1.csv"
        ),
    )
    p.add_argument(
        "--watchlist_csv",
        default=str(
            Path("backtest_out")
            / "stage2"
            / "indicator_audit"
            / "20260611_b123_tk_r4_usd_overlap_negative_pockets_v1"
            / "b123_usd_overlap_negative_watchlist_20260611_v1.csv"
        ),
    )
    p.add_argument(
        "--out_dir",
        default=str(Path("backtest_out") / "stage2" / "indicator_audit" / "20260611_b124_tk_r4_usd_half_risk_role_finalize_v1"),
    )
    p.add_argument("--date_tag", default="20260611")
    return p.parse_args()


def _safe_str(v: object) -> str:
    if pd.isna(v):
        return ""
    return str(v)


def _summary_delta(csv_path: str | Path) -> dict[str, float]:
    df = pd.read_csv(csv_path)
    sub = df.loc[df["scenario"] == "scheme_b_minus_base"]
    if sub.empty:
        return {
            "delta_sum_pnl": float("nan"),
            "delta_avg_r_mult": float("nan"),
            "delta_max_drawdown_pnl": float("nan"),
        }
    row = sub.iloc[0]
    return {
        "delta_sum_pnl": float(row["sum_pnl"]),
        "delta_avg_r_mult": float(row["avg_r_mult"]),
        "delta_max_drawdown_pnl": float(row["max_drawdown_pnl"]),
    }


def _join_keys(df: pd.DataFrame, scope: str, max_items: int = 8) -> str:
    sub = df.loc[df["scope"] == scope].copy()
    if sub.empty:
        return ""
    vals = list(sub["group_key"].astype(str).head(max_items))
    return " | ".join(vals)


def _build_role_contract(
    cfg_df: pd.DataFrame,
    since_delta: dict[str, float],
    pre_delta: dict[str, float],
    watch_df: pd.DataFrame,
) -> pd.DataFrame:
    cfg = cfg_df.iloc[0].to_dict()
    symbol_watch = watch_df.loc[watch_df["scope"] == "symbol"].copy()
    profile_symbol_watch = watch_df.loc[watch_df["scope"] == "profile_symbol"].copy()
    return pd.DataFrame(
        [
            {
                "scheme_b_name": _safe_str(cfg.get("scheme_b_name")),
                "enabled_default": bool(cfg.get("enabled_default")),
                "baseline_default_unchanged": True,
                "hard_gate_enabled": False,
                "watchlist_mode": "observe_only",
                "role_status": "global_candidate_with_watchlist",
                "trigger_col": _safe_str(cfg.get("trigger_col")),
                "trigger_theme": _safe_str(cfg.get("trigger_theme")),
                "risk_scale_when_triggered": float(cfg.get("risk_scale_when_triggered", float("nan"))),
                "validation_windows": "since2022|pre2022",
                "since2022_delta_sum_pnl": since_delta["delta_sum_pnl"],
                "since2022_delta_avg_r_mult": since_delta["delta_avg_r_mult"],
                "since2022_delta_max_drawdown_pnl": since_delta["delta_max_drawdown_pnl"],
                "pre2022_delta_sum_pnl": pre_delta["delta_sum_pnl"],
                "pre2022_delta_avg_r_mult": pre_delta["delta_avg_r_mult"],
                "pre2022_delta_max_drawdown_pnl": pre_delta["delta_max_drawdown_pnl"],
                "high_watch_symbol_count": float(len(symbol_watch)),
                "high_watch_profile_symbol_count": float(len(profile_symbol_watch)),
                "high_watch_symbols": _join_keys(symbol_watch, scope="symbol"),
                "high_watch_profile_symbols": _join_keys(profile_symbol_watch, scope="profile_symbol"),
                "notes": "Current role: keep global USD overlap >=1 Scheme B shell default-off; attach observe-only negative pocket watchlist.",
            }
        ]
    )


def _build_watchlist_contract(watch_df: pd.DataFrame) -> pd.DataFrame:
    if watch_df.empty:
        return pd.DataFrame()
    out = watch_df.copy()
    out = out.loc[
        out["priority"].isin(["high_watch", "single_split_hard_negative", "persistent_hard_negative"])
    ].copy()
    if out.empty:
        return out
    out["recommended_action"] = "observe_only"
    out["gate_recommendation"] = "do_not_hard_gate"
    out["current_role"] = "exception_watchlist"
    out = out.sort_values(
        ["scope", "priority", "n_splits_flagged", "max_fail_score", "worst_delta_sum_pnl"],
        ascending=[True, True, False, False, True],
        kind="mergesort",
    ).reset_index(drop=True)
    cols = [
        "scope",
        "group_key",
        "priority",
        "n_splits_flagged",
        "flag_since2022",
        "flag_pre2022",
        "max_fail_score",
        "worst_delta_sum_pnl",
        "worst_delta_max_drawdown_pnl",
        "worst_delta_avg_r_mult",
        "max_trigger_share",
        "min_n_trigger",
        "buckets",
        "recommended_action",
        "gate_recommendation",
        "current_role",
    ]
    return out[cols].copy()


def _build_validation_summary(
    since_delta: dict[str, float],
    pre_delta: dict[str, float],
    watch_contract_df: pd.DataFrame,
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "window": "since2022",
                "delta_sum_pnl": since_delta["delta_sum_pnl"],
                "delta_avg_r_mult": since_delta["delta_avg_r_mult"],
                "delta_max_drawdown_pnl": since_delta["delta_max_drawdown_pnl"],
                "improve_sum_pnl": bool(since_delta["delta_sum_pnl"] > 0.0),
                "improve_max_drawdown_pnl": bool(since_delta["delta_max_drawdown_pnl"] > 0.0),
                "watchlist_rows": float(len(watch_contract_df)),
            },
            {
                "window": "pre2022",
                "delta_sum_pnl": pre_delta["delta_sum_pnl"],
                "delta_avg_r_mult": pre_delta["delta_avg_r_mult"],
                "delta_max_drawdown_pnl": pre_delta["delta_max_drawdown_pnl"],
                "improve_sum_pnl": bool(pre_delta["delta_sum_pnl"] > 0.0),
                "improve_max_drawdown_pnl": bool(pre_delta["delta_max_drawdown_pnl"] > 0.0),
                "watchlist_rows": float(len(watch_contract_df)),
            },
        ]
    )


def _format_terminal_summary(role_df: pd.DataFrame, validation_df: pd.DataFrame, watch_contract_df: pd.DataFrame) -> str:
    if role_df.empty:
        return "usd_half_risk_role_finalize\n  role unavailable"
    role = role_df.iloc[0]
    lines = [
        "usd_half_risk_role_finalize",
        "  "
        + f"status={role['role_status']}, "
        + f"enabled_default={int(bool(role['enabled_default']))}, "
        + f"hard_gate={int(bool(role['hard_gate_enabled']))}, "
        + f"watchlist_mode={role['watchlist_mode']}",
    ]
    for _, r in validation_df.iterrows():
        lines.append(
            "  "
            + f"{r['window']}: "
            + f"delta_sum_pnl={float(r['delta_sum_pnl']):+.2f}, "
            + f"delta_max_dd={float(r['delta_max_drawdown_pnl']):+.2f}, "
            + f"delta_avg_r={float(r['delta_avg_r_mult']):+.6f}"
        )
    for _, r in watch_contract_df.head(6).iterrows():
        lines.append(
            "  "
            + f"watch {r['scope']} {r['group_key']}: "
            + f"priority={r['priority']}, "
            + f"action={r['recommended_action']}"
        )
    return "\n".join(lines)


def format_terminal_role_summary(role_df: pd.DataFrame, validation_df: pd.DataFrame, watch_contract_df: pd.DataFrame) -> str:
    return _format_terminal_summary(role_df, validation_df, watch_contract_df)


def run_role_finalize(
    since_config_csv: str | Path,
    since_summary_csv: str | Path,
    pre_summary_csv: str | Path,
    watchlist_csv: str | Path,
    out_dir: str | Path,
    date_tag: str,
) -> tuple[Path, Path, Path, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    date_tag = str(date_tag).strip()

    cfg_df = pd.read_csv(since_config_csv)
    since_delta = _summary_delta(since_summary_csv)
    pre_delta = _summary_delta(pre_summary_csv)
    watch_df = pd.read_csv(watchlist_csv)

    role_df = _build_role_contract(cfg_df, since_delta=since_delta, pre_delta=pre_delta, watch_df=watch_df)
    watch_contract_df = _build_watchlist_contract(watch_df)
    validation_df = _build_validation_summary(since_delta, pre_delta, watch_contract_df=watch_contract_df)

    out_role = out_dir / f"b124_usd_half_risk_role_contract_{date_tag}_v1.csv"
    out_watch = out_dir / f"b124_usd_half_risk_watchlist_contract_{date_tag}_v1.csv"
    out_val = out_dir / f"b124_usd_half_risk_validation_summary_{date_tag}_v1.csv"

    role_df.to_csv(out_role, index=False, encoding="utf-8-sig")
    watch_contract_df.to_csv(out_watch, index=False, encoding="utf-8-sig")
    validation_df.to_csv(out_val, index=False, encoding="utf-8-sig")
    return out_role, out_watch, out_val, role_df, watch_contract_df, validation_df


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    date_tag = str(args.date_tag).strip()

    out_role, out_watch, out_val, role_df, watch_contract_df, validation_df = run_role_finalize(
        since_config_csv=args.since_config_csv,
        since_summary_csv=args.since_summary_csv,
        pre_summary_csv=args.pre_summary_csv,
        watchlist_csv=args.watchlist_csv,
        out_dir=out_dir,
        date_tag=date_tag,
    )

    print(format_terminal_role_summary(role_df, validation_df, watch_contract_df))
    print(out_role)
    print(out_watch)
    print(out_val)


if __name__ == "__main__":
    main()
