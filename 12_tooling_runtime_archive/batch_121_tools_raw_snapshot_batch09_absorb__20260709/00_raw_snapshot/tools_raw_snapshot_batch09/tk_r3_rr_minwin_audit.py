from __future__ import annotations

import argparse
from pathlib import Path
import sys
import re

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import backtest_p0 as m


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit risk-reward (R multiple) and estimate breakeven win rate from baseline trades.")
    parser.add_argument("--p0_sweep_dir", default=str(Path("backtest_out") / "p0_sweep"))
    parser.add_argument("--split", default="since2022")
    parser.add_argument("--date_tag", default="20260611")
    parser.add_argument(
        "--out_dir",
        default=str(Path("backtest_out") / "stage2" / "indicator_audit" / "20260611_b116_tk_r3_rr_minwin_since2022_v1"),
    )
    return parser.parse_args()


def _safe_mean(s: pd.Series) -> float:
    s2 = pd.to_numeric(s, errors="coerce")
    return float(s2.mean()) if len(s2) else float("nan")


def _safe_median(s: pd.Series) -> float:
    s2 = pd.to_numeric(s, errors="coerce")
    return float(s2.median()) if len(s2) else float("nan")


def _breakeven_win_rate(avg_win_r: float, avg_loss_r_abs: float) -> float:
    if not (pd.notna(avg_win_r) and pd.notna(avg_loss_r_abs)):
        return float("nan")
    if avg_win_r <= 0.0 or avg_loss_r_abs <= 0.0:
        return float("nan")
    return float(avg_loss_r_abs / (avg_win_r + avg_loss_r_abs))


def _compute_r_multiple(df: pd.DataFrame) -> pd.Series:
    side = df["side"].astype(str).str.strip().str.upper()
    entry = pd.to_numeric(df["entry"], errors="coerce")
    exit_px = pd.to_numeric(df["exit"], errors="coerce")
    stop_num = pd.to_numeric(df["stop"], errors="coerce")
    key_cols = [c for c in ["entry_time", "side", "entry"] if c in df.columns]
    if key_cols:
        min_stop = df.assign(_stop=stop_num).groupby(key_cols, sort=False)["_stop"].transform("min")
        max_stop = df.assign(_stop=stop_num).groupby(key_cols, sort=False)["_stop"].transform("max")
        entry_stop_ref = min_stop.where(side.eq("LONG"), max_stop)
    else:
        entry_stop_ref = stop_num

    risk = (entry - entry_stop_ref).abs()
    reward = pd.Series(index=df.index, dtype=float)
    is_long = side.eq("LONG")
    is_short = side.eq("SHORT")
    reward.loc[is_long] = (exit_px - entry).loc[is_long]
    reward.loc[is_short] = (entry - exit_px).loc[is_short]
    r = reward / risk.replace(0.0, float("nan"))
    return r


def _reason_class(reason: str) -> tuple[str, str]:
    s = str(reason).strip().lower()
    m = re.match(r"^tp_cam_[rs](\d+)$", s)
    if m:
        try:
            lvl = int(m.group(1))
        except Exception:
            lvl = 0
        if lvl <= 1:
            return "TP1", "TP1"
        if lvl == 2:
            return "TP2", "TP2"
        return "TP3", "TP3"
    if "trail" in s:
        return "Trail", ""
    if "stop" in s:
        return "Stop", ""
    return "Stop", ""


def _init_stats() -> dict[str, float]:
    return {"n": 0.0, "wins": 0.0, "losses": 0.0, "sum_r": 0.0, "sum_win_r": 0.0, "sum_loss_r_abs": 0.0}


def _finalize_stats(s: dict[str, float]) -> dict[str, float]:
    n = float(s["n"])
    wins = float(s["wins"])
    losses = float(s["losses"])
    avg_r = float(s["sum_r"] / n) if n else float("nan")
    avg_win_r = float(s["sum_win_r"] / wins) if wins else float("nan")
    avg_loss_r_abs = float(s["sum_loss_r_abs"] / losses) if losses else float("nan")
    return {
        "n": n,
        "win_rate": float(wins / n) if n else float("nan"),
        "avg_r": avg_r,
        "avg_win_r": avg_win_r,
        "avg_loss_r_abs": avg_loss_r_abs,
        "breakeven_win_rate_est": _breakeven_win_rate(avg_win_r, avg_loss_r_abs),
    }


def main() -> None:
    args = parse_args()
    p0_sweep_dir = Path(args.p0_sweep_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    date_tag = str(args.date_tag).strip()
    split_filter = str(args.split).strip()

    class_order = ["TP1", "TP2", "TP3", "Stop", "Trail"]
    class_stats = {k: _init_stats() for k in class_order}
    rows: list[dict[str, float | str]] = []

    files = m._iter_trades_baseline_csvs(p0_sweep_dir)
    for trades_csv in files:
        symbol, split, profile = m._extract_symbol_split_profile(trades_csv, p0_sweep_dir)
        if split_filter and str(split).strip() != split_filter:
            continue

        try:
            df = pd.read_csv(trades_csv, usecols=["side", "entry", "stop", "exit", "reason"])
        except Exception:
            continue
        if df.empty:
            continue

        df = df[df["exit"].notna()].copy()
        if df.empty:
            continue

        df["r_mult"] = _compute_r_multiple(df)
        df = df[df["r_mult"].notna()].copy()
        if df.empty:
            continue

        df["reason"] = df["reason"].astype(str).str.strip()
        df["reason_class"] = df["reason"].map(lambda x: _reason_class(str(x))[0])
        df["tp_bucket"] = df["reason"].map(lambda x: _reason_class(str(x))[1])

        r_all = pd.to_numeric(df["r_mult"], errors="coerce")
        win_mask = r_all > 0.0
        df["win"] = win_mask.astype(int)
        df["loss_r_abs"] = (-r_all).where(~win_mask, float("nan"))
        df["win_r"] = r_all.where(win_mask, float("nan"))

        for cls, subc in df.groupby("reason_class", sort=True):
            cls_key = str(cls).strip()
            if cls_key not in class_stats:
                continue
            r = pd.to_numeric(subc["r_mult"], errors="coerce")
            wins = float(pd.to_numeric(subc["win"], errors="coerce").fillna(0.0).sum())
            class_stats[cls_key]["n"] += float(len(subc))
            class_stats[cls_key]["wins"] += wins
            class_stats[cls_key]["losses"] += float(len(subc)) - wins
            class_stats[cls_key]["sum_r"] += float(r.sum())
            class_stats[cls_key]["sum_win_r"] += float(pd.to_numeric(subc["win_r"], errors="coerce").sum(skipna=True))
            class_stats[cls_key]["sum_loss_r_abs"] += float(pd.to_numeric(subc["loss_r_abs"], errors="coerce").sum(skipna=True))

        for reason, sub in df.groupby("reason", sort=True):
            r = pd.to_numeric(sub["r_mult"], errors="coerce")
            avg_win_r = _safe_mean(sub["win_r"])
            avg_loss_r_abs = _safe_mean(sub["loss_r_abs"])
            rc, tp_bucket = _reason_class(str(reason))
            rows.append(
                {
                    "symbol": str(symbol).strip().upper(),
                    "split": str(split).strip(),
                    "profile": str(profile).strip(),
                    "reason_class": rc,
                    "tp_bucket": tp_bucket,
                    "reason": str(reason),
                    "n": float(len(sub)),
                    "win_rate": _safe_mean(sub["win"]),
                    "avg_r": _safe_mean(r),
                    "median_r": _safe_median(r),
                    "avg_win_r": avg_win_r,
                    "avg_loss_r_abs": avg_loss_r_abs,
                    "breakeven_win_rate_est": _breakeven_win_rate(avg_win_r, avg_loss_r_abs),
                }
            )

    df_by = pd.DataFrame(rows)
    out_by_v1 = out_dir / f"b116_rr_minwin_by_reason_{date_tag}_v1.csv"
    if not df_by.empty:
        df_by = df_by.sort_values(
            ["reason_class", "tp_bucket", "reason", "breakeven_win_rate_est", "n"],
            ascending=[True, True, True, True, False],
            kind="mergesort",
        ).reset_index(drop=True)
    df_by.to_csv(out_by_v1, index=False, encoding="utf-8-sig")

    overall_rows: list[dict[str, float | str]] = []
    if not df_by.empty:
        for reason, sub in df_by.groupby("reason", sort=True):
            n_w = pd.to_numeric(sub["n"], errors="coerce").astype(float)
            n_sum = float(n_w.sum()) if len(n_w) else 0.0

            def _wmean(col: str) -> float:
                x = pd.to_numeric(sub[col], errors="coerce").astype(float)
                m = x.notna() & n_w.notna()
                if not int(m.sum()):
                    return float("nan")
                denom = float(n_w[m].sum())
                return float((x[m] * n_w[m]).sum() / denom) if denom else float("nan")

            overall_rows.append(
                {
                    "split": split_filter,
                    "reason": str(reason),
                    "n": n_sum,
                    "win_rate": _wmean("win_rate"),
                    "avg_r": _wmean("avg_r"),
                    "median_r": _safe_median(sub["median_r"]),
                    "avg_win_r": _wmean("avg_win_r"),
                    "avg_loss_r_abs": _wmean("avg_loss_r_abs"),
                    "breakeven_win_rate_est": _wmean("breakeven_win_rate_est"),
                }
            )

    out_overall_v1 = out_dir / f"b116_rr_minwin_overall_{date_tag}_v1.csv"
    pd.DataFrame(overall_rows).to_csv(out_overall_v1, index=False, encoding="utf-8-sig")

    out_by_v2 = out_dir / f"b116_rr_minwin_by_reason_{date_tag}_v2.csv"
    out_overall_v2 = out_dir / f"b116_rr_minwin_overall_{date_tag}_v2.csv"
    df_by.to_csv(out_by_v2, index=False, encoding="utf-8-sig")
    pd.DataFrame(overall_rows).to_csv(out_overall_v2, index=False, encoding="utf-8-sig")

    class_rows: list[dict[str, float | str]] = []
    for cls in class_order:
        s = _finalize_stats(class_stats[cls])
        class_rows.append({"split": split_filter, "reason_class": cls, **s})
    out_class = out_dir / f"b116_rr_minwin_by_class_{date_tag}_v1.csv"
    pd.DataFrame(class_rows).to_csv(out_class, index=False, encoding="utf-8-sig")

    tp2 = _finalize_stats(class_stats["TP2"])
    tp3 = _finalize_stats(class_stats["TP3"])
    out_tp = out_dir / f"b116_rr_minwin_tp2_vs_tp3_{date_tag}_v1.csv"
    tp_rows = [
        {"split": split_filter, "tp_bucket": "TP2", **tp2},
        {"split": split_filter, "tp_bucket": "TP3", **tp3},
        {
            "split": split_filter,
            "tp_bucket": "TP3_minus_TP2",
            "n": tp3["n"] - tp2["n"] if pd.notna(tp3["n"]) and pd.notna(tp2["n"]) else float("nan"),
            "win_rate": tp3["win_rate"] - tp2["win_rate"] if pd.notna(tp3["win_rate"]) and pd.notna(tp2["win_rate"]) else float("nan"),
            "avg_r": tp3["avg_r"] - tp2["avg_r"] if pd.notna(tp3["avg_r"]) and pd.notna(tp2["avg_r"]) else float("nan"),
            "avg_win_r": tp3["avg_win_r"] - tp2["avg_win_r"] if pd.notna(tp3["avg_win_r"]) and pd.notna(tp2["avg_win_r"]) else float("nan"),
            "avg_loss_r_abs": tp3["avg_loss_r_abs"] - tp2["avg_loss_r_abs"]
            if pd.notna(tp3["avg_loss_r_abs"]) and pd.notna(tp2["avg_loss_r_abs"])
            else float("nan"),
            "breakeven_win_rate_est": tp3["breakeven_win_rate_est"] - tp2["breakeven_win_rate_est"]
            if pd.notna(tp3["breakeven_win_rate_est"]) and pd.notna(tp2["breakeven_win_rate_est"])
            else float("nan"),
        },
    ]
    pd.DataFrame(tp_rows).to_csv(out_tp, index=False, encoding="utf-8-sig")

    print(out_by_v2)
    print(out_overall_v2)
    print(out_class)
    print(out_tp)


if __name__ == "__main__":
    main()
