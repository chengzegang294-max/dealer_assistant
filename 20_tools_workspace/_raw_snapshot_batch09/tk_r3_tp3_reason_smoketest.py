from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import backtest_p0 as m


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Smoketest whether tp_cam_r3/tp_cam_s3 reasons can be produced when cam TP3 is enabled.")
    p.add_argument("--symbol", default="XAUUSD")
    p.add_argument("--csv_dir", default=str(Path("data")))
    p.add_argument("--cam_r3_mult", type=float, default=0.78)
    p.add_argument("--cam_tp3_frac", type=float, default=0.20)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    sym = str(args.symbol).strip().upper()
    csv_dir = Path(args.csv_dir)

    csv_path = m._find_symbol_csv(csv_dir, sym)
    if csv_path is None or not Path(csv_path).exists():
        raise FileNotFoundError(f"symbol csv not found: {sym}")

    df1h = m.load_ohlcv_1h(csv_path, tz=None)
    df4h = m.resample_ohlcv(df1h, "4H")
    df1d = m.resample_ohlcv(df1h, "1D")

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
    trend = m.compute_trend_flags(df1h, df4h, df1d, p)
    trades, metrics, events = m.backtest_one(df1h, trend, p, m.Config())

    reason_s = trades["reason"].astype(str).str.strip() if "reason" in trades.columns else pd.Series(dtype=str)
    counts = reason_s.value_counts(dropna=False).reset_index()
    counts.columns = ["reason", "n"]

    print(f"symbol={sym}")
    print(f"tp_cam_r3={int((reason_s == 'tp_cam_r3').sum())}, tp_cam_s3={int((reason_s == 'tp_cam_s3').sum())}")
    print(counts.head(20).to_string(index=False))


if __name__ == "__main__":
    main()

