from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_SYMBOL_LIST_CSV = ROOT / "data" / "t02_multi_symbol_sample_v1.csv"
DEFAULT_OUTPUT_DIR = ROOT / "data" / "t02_sources" / "daily_tushare"


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


def read_symbol_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def fetch_one_symbol(
    pro: Any,
    symbol: str,
    symbol_name: str,
    start_date: str,
    end_date: str,
) -> list[dict[str, Any]]:
    daily_df = pro.daily(ts_code=symbol, start_date=start_date, end_date=end_date)

    if daily_df is None or daily_df.empty:
        raise RuntimeError("daily_empty")

    keep_cols = [
        c
        for c in ["ts_code", "trade_date", "open", "high", "low", "close", "pre_close", "vol", "amount"]
        if c in daily_df.columns
    ]
    daily_df = daily_df.loc[:, keep_cols].copy()
    missing = [c for c in ["open", "high", "low", "close", "pre_close", "vol", "amount"] if c not in keep_cols]
    if missing:
        raise RuntimeError(f"daily_missing_columns:{','.join(missing)}")

    daily_df["symbol"] = daily_df["ts_code"]
    daily_df["symbol_name"] = symbol_name or symbol
    daily_df["volume"] = daily_df["vol"]
    daily_df["data_source"] = "tushare:daily"
    daily_df["asof_date"] = daily_df["trade_date"]
    daily_df["notes"] = "daily_ohlcv_raw_from_tushare"

    output_df = daily_df.loc[
        :,
        [
            "trade_date",
            "symbol",
            "symbol_name",
            "open",
            "high",
            "low",
            "close",
            "pre_close",
            "volume",
            "amount",
            "data_source",
            "asof_date",
            "notes",
        ],
    ].sort_values(["trade_date", "symbol"])
    return output_df.to_dict("records")


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch T02 daily OHLCV source tables for a multi-symbol sample.")
    parser.add_argument("--start-date", required=True, help="YYYYMMDD")
    parser.add_argument("--end-date", required=True, help="YYYYMMDD")
    parser.add_argument(
        "--symbol-list-csv",
        default=str(DEFAULT_SYMBOL_LIST_CSV),
        help="CSV containing symbol, symbol_name, and optional notes.",
    )
    parser.add_argument(
        "--batch-label",
        default="sample5",
        help="Short label embedded in output file names.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for combined source CSV and metadata.",
    )
    args = parser.parse_args()

    symbol_list_csv = Path(args.symbol_list_csv)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    date_tag = f"{args.start_date}_{args.end_date}"
    base_name = f"t02_daily_tushare_batch__{args.batch_label}__{date_tag}"
    csv_path = output_dir / f"{base_name}.csv"
    metadata_path = output_dir / f"{base_name}__metadata.json"

    metadata: dict[str, Any] = {
        "producer": "fetch_t02_daily_batch_tushare_v1.py",
        "scope": "A股 P0 首轮离线验证 T02 多标的日线 OHLCV 真实源表",
        "status": "started",
        "start_date": args.start_date,
        "end_date": args.end_date,
        "symbol_list_csv": str(symbol_list_csv).replace("\\", "/"),
        "batch_label": args.batch_label,
        "token_source": None,
        "output_csv": str(csv_path).replace("\\", "/"),
        "unit_note": "amount uses 千元; volume uses 手; open/high/low/close/pre_close uses 元",
        "columns": [
            "trade_date",
            "symbol",
            "symbol_name",
            "open",
            "high",
            "low",
            "close",
            "pre_close",
            "volume",
            "amount",
            "data_source",
            "asof_date",
            "notes",
        ],
    }

    if not symbol_list_csv.exists():
        metadata["status"] = "failed"
        metadata["failure_reason"] = "symbol_list_csv_not_found"
        write_json(metadata_path, metadata)
        return 2

    token, token_source = load_tushare_token()
    metadata["token_source"] = token_source
    if not token:
        metadata["status"] = "failed"
        metadata["failure_reason"] = "tushare_token_missing"
        write_json(metadata_path, metadata)
        return 3

    try:
        import pandas as pd  # type: ignore
        import tushare as ts  # type: ignore
    except Exception as e:  # pragma: no cover
        metadata["status"] = "failed"
        metadata["failure_reason"] = "dependency_import_failed"
        metadata["failure_detail"] = str(e)
        write_json(metadata_path, metadata)
        return 4

    symbol_rows = read_symbol_rows(symbol_list_csv)
    if not symbol_rows:
        metadata["status"] = "failed"
        metadata["failure_reason"] = "symbol_list_empty"
        write_json(metadata_path, metadata)
        return 5

    pro = ts.pro_api(token)
    combined_rows: list[dict[str, Any]] = []
    per_symbol_results: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    for symbol_row in symbol_rows:
        symbol = (symbol_row.get("symbol") or "").strip()
        symbol_name = (symbol_row.get("symbol_name") or symbol).strip()
        if not symbol:
            continue
        try:
            rows = fetch_one_symbol(pro, symbol, symbol_name, args.start_date, args.end_date)
            combined_rows.extend(rows)
            per_symbol_results.append(
                {
                    "symbol": symbol,
                    "symbol_name": symbol_name,
                    "status": "success",
                    "rows": len(rows),
                    "first_trade_date": str(rows[0]["trade_date"]) if rows else "",
                    "last_trade_date": str(rows[-1]["trade_date"]) if rows else "",
                }
            )
        except Exception as e:  # pragma: no cover
            failure_detail = str(e)
            failures.append(
                {
                    "symbol": symbol,
                    "symbol_name": symbol_name,
                    "failure_detail": failure_detail,
                }
            )
            per_symbol_results.append(
                {
                    "symbol": symbol,
                    "symbol_name": symbol_name,
                    "status": "failed",
                    "rows": 0,
                    "first_trade_date": "",
                    "last_trade_date": "",
                }
            )

    if not combined_rows:
        metadata["status"] = "failed"
        metadata["failure_reason"] = "all_symbols_failed"
        metadata["per_symbol_results"] = per_symbol_results
        metadata["failures"] = failures
        write_json(metadata_path, metadata)
        return 6

    combined_rows.sort(key=lambda row: (str(row["trade_date"]), str(row["symbol"])))
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=metadata["columns"])
        writer.writeheader()
        for row in combined_rows:
            writer.writerow(row)

    metadata["status"] = "partial_success" if failures else "success"
    metadata["rows"] = len(combined_rows)
    metadata["symbols_requested"] = len([row for row in symbol_rows if (row.get("symbol") or "").strip()])
    metadata["symbols_succeeded"] = len([row for row in per_symbol_results if row["status"] == "success"])
    metadata["symbols_failed"] = len(failures)
    metadata["per_symbol_results"] = per_symbol_results
    metadata["failures"] = failures
    metadata["first_trade_date"] = str(combined_rows[0]["trade_date"])
    metadata["last_trade_date"] = str(combined_rows[-1]["trade_date"])
    write_json(metadata_path, metadata)
    return 0 if not failures else 7


if __name__ == "__main__":
    raise SystemExit(main())

