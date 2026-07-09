from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Dict, List

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import backtest_p0 as m


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Audit TK-R4 fixed-risk and cross-symbol correlation risk concentration.")
    p.add_argument("--p0_sweep_dir", default=str(Path("backtest_out") / "p0_sweep"))
    p.add_argument("--split", default="since2022")
    p.add_argument("--date_tag", default="20260611")
    p.add_argument(
        "--out_dir",
        default=str(Path("backtest_out") / "stage2" / "indicator_audit" / "20260611_b118_tk_r4_risk_corr_since2022_v1"),
    )
    return p.parse_args()


def _safe_mean(s: pd.Series) -> float:
    s2 = pd.to_numeric(s, errors="coerce")
    return float(s2.mean()) if len(s2) else float("nan")


def _safe_median(s: pd.Series) -> float:
    s2 = pd.to_numeric(s, errors="coerce")
    return float(s2.median()) if len(s2) else float("nan")


def _agg(df: pd.DataFrame) -> dict[str, float]:
    return {
        "n": float(len(df)),
        "avg_pnl": _safe_mean(df.get("position_pnl", pd.Series(dtype=float))),
        "median_pnl": _safe_median(df.get("position_pnl", pd.Series(dtype=float))),
        "avg_r_mult": _safe_mean(df.get("r_mult", pd.Series(dtype=float))),
        "median_r_mult": _safe_median(df.get("r_mult", pd.Series(dtype=float))),
        "win_rate": _safe_mean(pd.to_numeric(df.get("position_pnl", pd.Series(dtype=float)), errors="coerce") > 0.0),
        "avg_concurrent_positions": _safe_mean(df.get("concurrent_positions", pd.Series(dtype=float))),
        "avg_usd_overlap": _safe_mean(df.get("concurrent_usd_same_dir", pd.Series(dtype=float))),
        "avg_commodity_overlap": _safe_mean(df.get("concurrent_commodity_same_dir", pd.Series(dtype=float))),
    }


def _fx_pair(sym: str) -> tuple[str, str] | None:
    s = str(sym).strip().upper()
    if len(s) == 6 and s.isalpha():
        return s[:3], s[3:]
    return None


def _ccy_exposure_sign(sym: str, side_s: str, ccy: str) -> int:
    pair = _fx_pair(sym)
    if pair is None:
        return 0
    base, quote = pair
    side_sign = 1 if str(side_s).strip().upper() == "LONG" else -1
    if base == ccy:
        return side_sign
    if quote == ccy:
        return -side_sign
    return 0


def _load_positions(trades_csv: Path, p0_sweep_dir: Path) -> pd.DataFrame:
    symbol, split, profile = m._extract_symbol_split_profile(trades_csv, p0_sweep_dir)
    usecols = ["entry_time", "exit_time", "side", "entry", "exit", "size", "pnl", "stop", "signal", "reason"]
    try:
        df = pd.read_csv(trades_csv, encoding="utf-8-sig", usecols=lambda c: c in set(usecols))
    except Exception:
        return pd.DataFrame()
    if df.empty:
        return pd.DataFrame()

    df["entry_time"] = pd.to_datetime(df["entry_time"], errors="coerce")
    df["exit_time"] = pd.to_datetime(df["exit_time"], errors="coerce")
    df["entry"] = pd.to_numeric(df["entry"], errors="coerce")
    df["exit"] = pd.to_numeric(df["exit"], errors="coerce")
    df["size"] = pd.to_numeric(df["size"], errors="coerce")
    df["pnl"] = pd.to_numeric(df["pnl"], errors="coerce")
    df["stop"] = pd.to_numeric(df["stop"], errors="coerce")
    df["symbol"] = str(symbol).strip().upper()
    df["split"] = str(split).strip()
    df["profile"] = str(profile).strip()
    df = df.dropna(subset=["entry_time", "exit_time", "entry", "size"]).copy()
    if df.empty:
        return pd.DataFrame()

    key_cols = ["symbol", "split", "profile", "entry_time", "side", "entry"]
    out_rows: List[Dict[str, object]] = []
    for _, sub in df.groupby(key_cols, sort=False):
        side_s = str(sub["side"].iloc[0]).strip().upper()
        stop_min = float(pd.to_numeric(sub["stop"], errors="coerce").min())
        stop_max = float(pd.to_numeric(sub["stop"], errors="coerce").max())
        entry_stop_ref = stop_min if side_s == "LONG" else stop_max
        total_size = float(pd.to_numeric(sub["size"], errors="coerce").sum())
        total_pnl = float(pd.to_numeric(sub["pnl"], errors="coerce").sum())
        risk_px = abs(float(sub["entry"].iloc[0]) - entry_stop_ref)
        risk_amt = risk_px * total_size
        out_rows.append(
            {
                "symbol": str(sub["symbol"].iloc[0]).strip().upper(),
                "split": str(sub["split"].iloc[0]).strip(),
                "profile": str(sub["profile"].iloc[0]).strip(),
                "entry_time": pd.to_datetime(sub["entry_time"].iloc[0], errors="coerce"),
                "exit_time": pd.to_datetime(sub["exit_time"].max(), errors="coerce"),
                "side": side_s,
                "entry": float(sub["entry"].iloc[0]),
                "entry_stop_ref": float(entry_stop_ref),
                "position_size": total_size,
                "position_pnl": total_pnl,
                "signal": str(sub["signal"].dropna().iloc[0]).strip() if "signal" in sub.columns and sub["signal"].notna().any() else "",
                "final_reason": str(sub["reason"].dropna().iloc[-1]).strip() if "reason" in sub.columns and sub["reason"].notna().any() else "",
                "risk_px": float(risk_px),
                "risk_amt": float(risk_amt),
                "r_mult": float(total_pnl / risk_amt) if risk_amt > 0 else float("nan"),
                "usd_bias": _ccy_exposure_sign(str(sub["symbol"].iloc[0]), side_s, "USD"),
                "aud_bias": _ccy_exposure_sign(str(sub["symbol"].iloc[0]), side_s, "AUD"),
                "nzd_bias": _ccy_exposure_sign(str(sub["symbol"].iloc[0]), side_s, "NZD"),
                "cad_bias": _ccy_exposure_sign(str(sub["symbol"].iloc[0]), side_s, "CAD"),
            }
        )
    return pd.DataFrame(out_rows)


def _annotate_overlaps(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    out_frames: List[pd.DataFrame] = []
    for (_, profile), sub in df.groupby(["split", "profile"], sort=False):
        g = sub.sort_values(["entry_time", "exit_time", "symbol"], kind="mergesort").reset_index(drop=True).copy()
        active: List[dict[str, object]] = []
        rows: List[dict[str, object]] = []
        for _, r in g.iterrows():
            et = pd.to_datetime(r["entry_time"], errors="coerce")
            active = [a for a in active if pd.to_datetime(a["exit_time"], errors="coerce") > et]
            usd_same = 0
            commodity_same = 0
            for a in active:
                if int(r["usd_bias"]) != 0 and int(a["usd_bias"]) == int(r["usd_bias"]):
                    usd_same += 1
                same_commodity = False
                for c in ["aud_bias", "nzd_bias", "cad_bias"]:
                    if int(r[c]) != 0 and int(a[c]) == int(r[c]):
                        same_commodity = True
                        break
                if same_commodity:
                    commodity_same += 1
            rows.append(
                {
                    "concurrent_positions": float(len(active)),
                    "concurrent_usd_same_dir": float(usd_same),
                    "concurrent_commodity_same_dir": float(commodity_same),
                    "usd_overlap_flag": bool(usd_same > 0),
                    "commodity_overlap_flag": bool(commodity_same > 0),
                    "any_corr_overlap_flag": bool((usd_same > 0) or (commodity_same > 0)),
                    "theme_risk_units_baseline": float(1 + max(usd_same, commodity_same)),
                    "theme_risk_units_half_rule": float(0.5 * (1 + max(usd_same, commodity_same)))
                    if ((usd_same > 0) or (commodity_same > 0))
                    else 1.0,
                }
            )
            active.append(r.to_dict())
        anno = pd.concat([g.reset_index(drop=True), pd.DataFrame(rows)], axis=1)
        out_frames.append(anno)
    return pd.concat(out_frames, ignore_index=True) if out_frames else pd.DataFrame()


def _summary_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    groups = {
        "all": df,
        "usd_overlap_any": df[df["usd_overlap_flag"].astype(bool)].copy(),
        "usd_overlap_none": df[~df["usd_overlap_flag"].astype(bool)].copy(),
        "commodity_overlap_any": df[df["commodity_overlap_flag"].astype(bool)].copy(),
        "commodity_overlap_none": df[~df["commodity_overlap_flag"].astype(bool)].copy(),
        "any_corr_overlap_any": df[df["any_corr_overlap_flag"].astype(bool)].copy(),
        "any_corr_overlap_none": df[~df["any_corr_overlap_flag"].astype(bool)].copy(),
    }
    rows: List[dict[str, object]] = []
    for name, sub in groups.items():
        a = _agg(sub)
        rows.append({"group": name, **a})
    return pd.DataFrame(rows)


def _profile_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    rows: List[dict[str, object]] = []
    for (split, profile), sub in df.groupby(["split", "profile"], sort=True):
        a = _agg(sub)
        rows.append(
            {
                "split": str(split),
                "profile": str(profile),
                **a,
                "usd_overlap_share": _safe_mean(pd.Series(sub["usd_overlap_flag"]).astype(float)),
                "commodity_overlap_share": _safe_mean(pd.Series(sub["commodity_overlap_flag"]).astype(float)),
                "any_corr_overlap_share": _safe_mean(pd.Series(sub["any_corr_overlap_flag"]).astype(float)),
                "theme_risk_units_baseline": _safe_mean(sub["theme_risk_units_baseline"]),
                "theme_risk_units_half_rule": _safe_mean(sub["theme_risk_units_half_rule"]),
            }
        )
    return pd.DataFrame(rows).sort_values(["split", "profile"], kind="mergesort").reset_index(drop=True)


def main() -> None:
    args = parse_args()
    out_pos, out_sum, out_prof, _pos_df = run_risk_corr_audit(
        p0_sweep_dir=args.p0_sweep_dir,
        split=args.split,
        out_dir=args.out_dir,
        date_tag=args.date_tag,
    )
    print(out_pos)
    print(out_sum)
    print(out_prof)


def run_risk_corr_audit(
    p0_sweep_dir: str | Path,
    split: str,
    out_dir: str | Path,
    date_tag: str,
) -> tuple[Path, Path, Path, pd.DataFrame]:
    p0_sweep_dir = Path(p0_sweep_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    split_filter = str(split).strip()
    date_tag = str(date_tag).strip()

    frames: List[pd.DataFrame] = []
    for trades_csv in m._iter_trades_baseline_csvs_latest(p0_sweep_dir):
        _, split_name, _ = m._extract_symbol_split_profile(trades_csv, p0_sweep_dir)
        if split_filter and str(split_name).strip() != split_filter:
            continue
        pos = _load_positions(trades_csv, p0_sweep_dir)
        if not pos.empty:
            frames.append(pos)
    pos_df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    pos_df = _annotate_overlaps(pos_df)

    out_pos = out_dir / f"b118_position_level_{date_tag}_v1.csv"
    out_sum = out_dir / f"b118_overlap_summary_{date_tag}_v1.csv"
    out_prof = out_dir / f"b118_overlap_by_profile_{date_tag}_v1.csv"
    pos_df.to_csv(out_pos, index=False, encoding="utf-8-sig")
    _summary_rows(pos_df).to_csv(out_sum, index=False, encoding="utf-8-sig")
    _profile_summary(pos_df).to_csv(out_prof, index=False, encoding="utf-8-sig")
    return out_pos, out_sum, out_prof, pos_df


if __name__ == "__main__":
    main()
