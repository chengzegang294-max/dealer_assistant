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
    p = argparse.ArgumentParser(description="Recompute baseline trades with cam TP3 enabled, then audit R multiple and breakeven win rate.")
    p.add_argument("--p0_sweep_dir", default=str(Path("backtest_out") / "p0_sweep"))
    p.add_argument("--csv_dir", default=str(Path("data")))
    p.add_argument("--split", default="since2022")
    p.add_argument("--date_tag", default="20260611")
    p.add_argument("--out_dir", default=str(Path("backtest_out") / "stage2" / "indicator_audit" / "20260611_b117_tk_r3_rr_minwin_cam_tp3_since2022_v1"))
    p.add_argument("--cam_r3_mult", type=float, default=0.70)
    p.add_argument("--cam_tp3_frac", type=float, default=0.20)
    return p.parse_args()


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
    return reward / risk.replace(0.0, float("nan"))


def _reason_class(reason: str) -> tuple[str, str]:
    s = str(reason).strip().lower()
    m1 = re.match(r"^tp_cam_[rs](\d+)$", s)
    if m1:
        try:
            lvl = int(m1.group(1))
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
    csv_dir = Path(args.csv_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    split_filter = str(args.split).strip()
    date_tag = str(args.date_tag).strip()

    base = m.Params()
    p = m.Params(
        **{
            **base.__dict__,
            "enable_cam_targets": True,
            "enable_cam_tp3": True,
            "cam_r3_mult": float(args.cam_r3_mult),
            "cam_tp3_frac": float(args.cam_tp3_frac),
        }
    )

    class_order = ["TP1", "TP2", "TP3", "Stop", "Trail"]
    class_stats = {k: _init_stats() for k in class_order}
    rows: list[dict[str, float | str]] = []

    files = m._iter_trades_baseline_csvs(p0_sweep_dir)
    for trades_csv in files:
        symbol, split, profile = m._extract_symbol_split_profile(trades_csv, p0_sweep_dir)
        if split_filter and str(split).strip() != split_filter:
            continue

        sym_u = str(symbol).strip().upper()
        csv_path = m._find_symbol_csv(csv_dir, sym_u)
        if csv_path is None or not Path(csv_path).exists():
            continue

        df1h = m.load_ohlcv_1h(csv_path, tz=None)
        if df1h.empty:
            continue
        df4h = m.resample_ohlcv(df1h, "4H")
        df1d = m.resample_ohlcv(df1h, "1D")
        trend = m.compute_trend_flags(df1h, df4h, df1d, p)
        trades, metrics, events = m.backtest_one(df1h, trend, p, m.Config())
        if trades.empty:
            continue

        trades = trades[trades["exit"].notna()].copy()
        if trades.empty:
            continue

        trades["r_mult"] = _compute_r_multiple(trades)
        trades = trades[trades["r_mult"].notna()].copy()
        if trades.empty:
            continue

        trades["reason"] = trades["reason"].astype(str).str.strip()
        trades["reason_class"] = trades["reason"].map(lambda x: _reason_class(str(x))[0])
        trades["tp_bucket"] = trades["reason"].map(lambda x: _reason_class(str(x))[1])

        r_all = pd.to_numeric(trades["r_mult"], errors="coerce")
        win_mask = r_all > 0.0
        trades["win"] = win_mask.astype(int)
        trades["loss_r_abs"] = (-r_all).where(~win_mask, float("nan"))
        trades["win_r"] = r_all.where(win_mask, float("nan"))

        for reason, sub in trades.groupby("reason", sort=True):
            reason_class, tp_bucket = _reason_class(str(reason))
            avg_win_r = _safe_mean(sub["win_r"])
            avg_loss_r_abs = _safe_mean(sub["loss_r_abs"])
            rows.append(
                {
                    "symbol": sym_u,
                    "split": str(split).strip(),
                    "profile": str(profile).strip(),
                    "reason_class": reason_class,
                    "tp_bucket": tp_bucket,
                    "reason": str(reason),
                    "n": float(len(sub)),
                    "win_rate": _safe_mean(sub["win"]),
                    "avg_r": _safe_mean(sub["r_mult"]),
                    "median_r": _safe_median(sub["r_mult"]),
                    "avg_win_r": avg_win_r,
                    "avg_loss_r_abs": avg_loss_r_abs,
                    "breakeven_win_rate_est": _breakeven_win_rate(avg_win_r, avg_loss_r_abs),
                }
            )

        for cls, subc in trades.groupby("reason_class", sort=True):
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

    df_by = pd.DataFrame(rows)
    out_by = out_dir / f"b117_rr_minwin_by_reason_{date_tag}_v1.csv"
    if not df_by.empty:
        df_by = df_by.sort_values(
            ["reason_class", "tp_bucket", "reason", "breakeven_win_rate_est", "n"],
            ascending=[True, True, True, True, False],
            kind="mergesort",
        ).reset_index(drop=True)
    df_by.to_csv(out_by, index=False, encoding="utf-8-sig")

    class_rows = [{"split": split_filter, "reason_class": cls, **_finalize_stats(class_stats[cls])} for cls in class_order]
    out_class = out_dir / f"b117_rr_minwin_by_class_{date_tag}_v1.csv"
    pd.DataFrame(class_rows).to_csv(out_class, index=False, encoding="utf-8-sig")

    tp2 = _finalize_stats(class_stats["TP2"])
    tp3 = _finalize_stats(class_stats["TP3"])
    out_tp = out_dir / f"b117_rr_minwin_tp2_vs_tp3_{date_tag}_v1.csv"
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

    print(out_by)
    print(out_class)
    print(out_tp)


if __name__ == "__main__":
    main()
