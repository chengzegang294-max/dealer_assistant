from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit the impact of TK-R2 pocket lists on trade-level performance.")
    parser.add_argument(
        "--out_dir",
        default=str(Path("backtest_out") / "stage2" / "indicator_audit" / "20260611_b115_tk_r2_pullback_all_v1"),
    )
    parser.add_argument("--date_tag", default="20260611")
    return parser.parse_args()


def _coerce_numeric(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


def _agg(df: pd.DataFrame) -> dict[str, float]:
    df = _coerce_numeric(df, ["trade_pnl", "win", "stop_loss_any", "tp2_any"])
    pnl = pd.to_numeric(df["trade_pnl"], errors="coerce") if "trade_pnl" in df.columns else pd.Series(dtype=float)
    return {
        "n": float(len(df)),
        "avg_pnl": float(pnl.mean()) if len(pnl) else float("nan"),
        "median_pnl": float(pnl.median()) if len(pnl) else float("nan"),
        "win_rate": float(pd.to_numeric(df["win"], errors="coerce").mean()) if "win" in df.columns and len(df) else float("nan"),
        "stop_loss_rate": float(pd.to_numeric(df["stop_loss_any"], errors="coerce").mean())
        if "stop_loss_any" in df.columns and len(df)
        else float("nan"),
        "tp2_rate": float(pd.to_numeric(df["tp2_any"], errors="coerce").mean()) if "tp2_any" in df.columns and len(df) else float("nan"),
    }


def _pair_key(profile: object, symbol: object) -> str:
    return f"{str(profile).strip()}|{str(symbol).strip()}"


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    date_tag = str(args.date_tag).strip()

    trade_csv = out_dir / f"b115_trade_level_{date_tag}_v1.csv"
    zone_pos_csv = out_dir / f"b115_zonehit_positive_pockets_{date_tag}_v1.csv"
    cancel_neg_csv = out_dir / f"b115_cancel_negative_pockets_{date_tag}_v1.csv"

    df = pd.read_csv(trade_csv)
    df = _coerce_numeric(df, ["tk_r2_zone_hit_flag_1h", "tk_r2_cancel_no_retrace_flag_1h", "tk_r2_stage_1h"])

    zone_pos = pd.read_csv(zone_pos_csv) if zone_pos_csv.exists() else pd.DataFrame()
    cancel_neg = pd.read_csv(cancel_neg_csv) if cancel_neg_csv.exists() else pd.DataFrame()

    zone_keys = set()
    if not zone_pos.empty:
        for _, r in zone_pos.iterrows():
            zone_keys.add(_pair_key(r.get("profile"), r.get("symbol")))
    cancel_keys = set()
    if not cancel_neg.empty:
        for _, r in cancel_neg.iterrows():
            cancel_keys.add(_pair_key(r.get("profile"), r.get("symbol")))

    df["profile_symbol_key"] = df.apply(lambda r: _pair_key(r.get("profile"), r.get("symbol")), axis=1)
    df["zonehit_in_pos_pocket"] = df["profile_symbol_key"].isin(zone_keys)
    df["cancel_in_neg_pocket"] = df["profile_symbol_key"].isin(cancel_keys)

    zone_hit = pd.to_numeric(df["tk_r2_zone_hit_flag_1h"], errors="coerce").fillna(0.0)
    cancel_flag = pd.to_numeric(df["tk_r2_cancel_no_retrace_flag_1h"], errors="coerce").fillna(0.0)

    cond_zonehit_pos = zone_hit.eq(1.0) & df["zonehit_in_pos_pocket"].astype(bool)
    cond_cancel_neg = cancel_flag.eq(1.0) & df["cancel_in_neg_pocket"].astype(bool)

    groups: list[tuple[str, pd.DataFrame]] = [
        ("all", df),
        ("zonehit_pos_pocket_hit", df[cond_zonehit_pos].copy()),
        ("cancel_neg_pocket_hit", df[cond_cancel_neg].copy()),
        ("kept_after_cancel_filter", df[~cond_cancel_neg].copy()),
        ("kept_and_zonehit_pos", df[(~cond_cancel_neg) & cond_zonehit_pos].copy()),
    ]
    rows: list[dict[str, float | str]] = []
    base = _agg(df)
    for name, g in groups:
        a = _agg(g)
        rows.append(
            {
                "group": name,
                **a,
                "share_all": (a["n"] / base["n"]) if base["n"] else 0.0,
                "delta_avg_pnl_vs_all": a["avg_pnl"] - base["avg_pnl"],
                "delta_median_pnl_vs_all": a["median_pnl"] - base["median_pnl"],
            }
        )
    overall_out = out_dir / f"b115_pocket_apply_overall_{date_tag}_v1.csv"
    pd.DataFrame(rows).to_csv(overall_out, index=False, encoding="utf-8-sig")

    pocket_rows: list[dict[str, float | str]] = []
    if zone_keys:
        for k in sorted(zone_keys):
            profile, symbol = k.split("|", 1)
            sub = df[(df["profile"].astype(str).str.strip().eq(profile)) & (df["symbol"].astype(str).str.strip().eq(symbol))].copy()
            hit = sub[pd.to_numeric(sub["tk_r2_zone_hit_flag_1h"], errors="coerce").fillna(0.0).eq(1.0)].copy()
            pocket_rows.append(
                {
                    "flag": "zone_hit",
                    "direction": "positive",
                    "profile": profile,
                    "symbol": symbol,
                    "n_all": float(len(sub)),
                    "n_hit": float(len(hit)),
                    "hit_share_all": float(len(hit) / len(sub)) if len(sub) else 0.0,
                    "avg_pnl_hit": _agg(hit)["avg_pnl"],
                    "median_pnl_hit": _agg(hit)["median_pnl"],
                    "avg_pnl_all": _agg(sub)["avg_pnl"],
                    "median_pnl_all": _agg(sub)["median_pnl"],
                    "delta_avg_pnl_hit_vs_all": _agg(hit)["avg_pnl"] - _agg(sub)["avg_pnl"],
                    "delta_median_pnl_hit_vs_all": _agg(hit)["median_pnl"] - _agg(sub)["median_pnl"],
                }
            )
    if cancel_keys:
        for k in sorted(cancel_keys):
            profile, symbol = k.split("|", 1)
            sub = df[(df["profile"].astype(str).str.strip().eq(profile)) & (df["symbol"].astype(str).str.strip().eq(symbol))].copy()
            hit = sub[pd.to_numeric(sub["tk_r2_cancel_no_retrace_flag_1h"], errors="coerce").fillna(0.0).eq(1.0)].copy()
            pocket_rows.append(
                {
                    "flag": "cancel_no_retrace",
                    "direction": "negative",
                    "profile": profile,
                    "symbol": symbol,
                    "n_all": float(len(sub)),
                    "n_hit": float(len(hit)),
                    "hit_share_all": float(len(hit) / len(sub)) if len(sub) else 0.0,
                    "avg_pnl_hit": _agg(hit)["avg_pnl"],
                    "median_pnl_hit": _agg(hit)["median_pnl"],
                    "avg_pnl_all": _agg(sub)["avg_pnl"],
                    "median_pnl_all": _agg(sub)["median_pnl"],
                    "delta_avg_pnl_hit_vs_all": _agg(hit)["avg_pnl"] - _agg(sub)["avg_pnl"],
                    "delta_median_pnl_hit_vs_all": _agg(hit)["median_pnl"] - _agg(sub)["median_pnl"],
                }
            )
    pockets_out = out_dir / f"b115_pocket_apply_pockets_{date_tag}_v1.csv"
    pd.DataFrame(pocket_rows).to_csv(pockets_out, index=False, encoding="utf-8-sig")

    print(overall_out)
    print(pockets_out)


if __name__ == "__main__":
    main()

