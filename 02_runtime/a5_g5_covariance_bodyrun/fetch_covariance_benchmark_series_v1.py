from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "covariance_benchmark_series"


def load_tushare_token() -> tuple[str | None, str]:
    env_token = (os.environ.get("TUSHARE_TOKEN") or "").strip()
    if env_token:
        return env_token, "env:TUSHARE_TOKEN"

    home_token = Path.home() / ".tushare" / "token"
    if home_token.exists():
        token = home_token.read_text(encoding="utf-8").strip()
        if token:
            return token, str(home_token)

    return None, "missing"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch benchmark daily series for covariance_model_id first fresh-run."
    )
    parser.add_argument("--benchmark-id", default="CSI300")
    parser.add_argument("--index-code", default="000300.SH")
    parser.add_argument("--start-date", required=True, help="YYYYMMDD")
    parser.add_argument("--end-date", required=True, help="YYYYMMDD")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    date_tag = f"{args.start_date}_{args.end_date}"
    safe_index_code = args.index_code.replace(".", "_")
    base_name = f"covariance_benchmark_series__{safe_index_code}__{date_tag}"
    output_csv = output_dir / f"{base_name}.csv"
    metadata_json = output_dir / f"{base_name}__metadata.json"

    metadata: dict[str, Any] = {
        "producer": "fetch_covariance_benchmark_series_v1.py",
        "scope": "covariance benchmark daily series for first fresh-run",
        "status": "started",
        "benchmark_id": args.benchmark_id,
        "index_code": args.index_code,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "token_source": None,
        "output_csv": str(output_csv).replace("\\", "/"),
    }

    token, token_source = load_tushare_token()
    metadata["token_source"] = token_source
    if not token:
        metadata["status"] = "failed"
        metadata["failure_reason"] = "tushare_token_missing"
        write_json(metadata_json, metadata)
        return 2

    try:
        import pandas as pd  # type: ignore
        import tushare as ts  # type: ignore
    except Exception as exc:  # pragma: no cover
        metadata["status"] = "failed"
        metadata["failure_reason"] = "dependency_import_failed"
        metadata["failure_detail"] = str(exc)
        write_json(metadata_json, metadata)
        return 3

    try:
        pro = ts.pro_api(token)
        df = pro.index_daily(ts_code=args.index_code, start_date=args.start_date, end_date=args.end_date)
        if df is None or df.empty:
            metadata["status"] = "failed"
            metadata["failure_reason"] = "index_daily_empty"
            write_json(metadata_json, metadata)
            return 4

        required_cols = ["trade_date", "close", "pct_chg"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            metadata["status"] = "failed"
            metadata["failure_reason"] = "index_daily_missing_columns"
            metadata["missing_columns"] = missing_cols
            write_json(metadata_json, metadata)
            return 5

        df = df.loc[:, required_cols].copy()
        df["trade_date"] = df["trade_date"].astype(str)
        df["close"] = df["close"].astype(float)
        df["pct_chg"] = df["pct_chg"].astype(float)
        df = df.sort_values("trade_date").reset_index(drop=True)
        df["benchmark_id"] = args.benchmark_id
        df["benchmark_index_code"] = args.index_code
        df["benchmark_return_1d"] = df["pct_chg"] / 100.0
        df["data_source"] = f"tushare:index_daily:{args.index_code}"
        df["asof_date"] = df["trade_date"]
        df["notes"] = "raw_benchmark_daily_series_for_covariance_first_fresh_run"

        output_columns = [
            "trade_date",
            "benchmark_id",
            "benchmark_index_code",
            "close",
            "pct_chg",
            "benchmark_return_1d",
            "data_source",
            "asof_date",
            "notes",
        ]
        df.to_csv(output_csv, columns=output_columns, index=False, encoding="utf-8")

        metadata["status"] = "success"
        metadata["rows"] = int(len(df))
        metadata["columns"] = output_columns
        metadata["first_trade_date"] = str(df.iloc[0]["trade_date"])
        metadata["last_trade_date"] = str(df.iloc[-1]["trade_date"])
        write_json(metadata_json, metadata)
        return 0
    except Exception as exc:  # pragma: no cover
        metadata["status"] = "failed"
        metadata["failure_reason"] = "tushare_api_error"
        metadata["failure_detail"] = str(exc)
        write_json(metadata_json, metadata)
        return 6


if __name__ == "__main__":
    raise SystemExit(main())
