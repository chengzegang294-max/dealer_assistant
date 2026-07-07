from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = BASE_DIR / "n02_first_real_input_bars_v1.csv"
DEFAULT_OUTPUT = BASE_DIR / "n02_real_input_eurusd_m5_from_m1_main_v1.csv"
DEFAULT_REPORT = BASE_DIR / "n02_real_input_eurusd_m5_from_m1_main_report_v1.json"
CSV_COLUMNS = ["symbol", "timeframe", "bar_time", "open", "high", "low", "close"]


def parse_iso_utc(value: str) -> datetime:
    return datetime.strptime(value.strip(), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def fmt_iso_utc(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_float(value: str) -> float:
    return float(value.strip())


def fmt_price(value: float, decimals: int = 5) -> str:
    return ("{0:0." + str(decimals) + "f}").format(value)


def read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return rows


def assert_header(path: Path) -> None:
    with path.open("r", encoding="utf-8", newline="") as f:
        header = next(csv.reader(f))
    if header != CSV_COLUMNS:
        raise ValueError("header mismatch: {0}".format(path))


def floor_to_5m(dt: datetime) -> datetime:
    minute = (dt.minute // 5) * 5
    return dt.replace(minute=minute, second=0, microsecond=0)


def write_rows(path: Path, rows: List[Dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--report-json", default=str(DEFAULT_REPORT))
    parser.add_argument("--symbol", default="EURUSD")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    report_path = Path(args.report_json)
    assert_header(input_path)
    rows = read_rows(input_path)

    grouped: Dict[Tuple[str, datetime], List[Dict[str, str]]] = defaultdict(list)
    filtered_input_rows = 0
    for row in rows:
        if row["symbol"] != args.symbol or row["timeframe"] != "M1":
            continue
        filtered_input_rows += 1
        dt = parse_iso_utc(row["bar_time"])
        grouped[(row["symbol"], floor_to_5m(dt))].append(row)

    out_rows: List[Dict[str, str]] = []
    dropped_partial_groups = 0
    for (symbol, bucket_start), bucket_rows in sorted(grouped.items(), key=lambda x: (x[0][0], x[0][1])):
        bucket_rows.sort(key=lambda r: r["bar_time"])
        if len(bucket_rows) != 5:
            dropped_partial_groups += 1
            continue
        prices_open = parse_float(bucket_rows[0]["open"])
        prices_close = parse_float(bucket_rows[-1]["close"])
        prices_high = max(parse_float(r["high"]) for r in bucket_rows)
        prices_low = min(parse_float(r["low"]) for r in bucket_rows)
        out_rows.append(
            {
                "symbol": symbol,
                "timeframe": "M5",
                "bar_time": fmt_iso_utc(bucket_start),
                "open": fmt_price(prices_open),
                "high": fmt_price(prices_high),
                "low": fmt_price(prices_low),
                "close": fmt_price(prices_close),
            }
        )

    write_rows(output_path, out_rows)
    report = {
        "producer": "n02_aggregate_bars_to_m5_v1.py",
        "scope": "REOPEN_B9_N02_REAL_INPUT_AGGREGATE_EURUSD_M5_FROM_MAIN_M1_P0",
        "status": "fresh_run_aggregate_main_m1_to_m5",
        "evidence_mode": "fresh_run_from_main_canonical_bars",
        "source_path": {
            "input_csv": str(input_path),
        },
        "repo_path": {
            "output_csv": str(output_path),
            "report_json": str(report_path),
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "symbol": args.symbol,
        "input_rows_filtered": filtered_input_rows,
        "bucket_groups_total": len(grouped),
        "bucket_groups_dropped_partial": dropped_partial_groups,
        "output_rows": len(out_rows),
        "output_first_bar_time": out_rows[0]["bar_time"] if out_rows else "",
        "output_last_bar_time": out_rows[-1]["bar_time"] if out_rows else "",
    }
    report_path.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding="utf-8")

    print("output_csv={0}".format(output_path))
    print("report_json={0}".format(report_path))
    print("input_rows_filtered={0}".format(filtered_input_rows))
    print("bucket_groups_total={0}".format(len(grouped)))
    print("bucket_groups_dropped_partial={0}".format(dropped_partial_groups))
    print("output_rows={0}".format(len(out_rows)))
    print("output_first_bar_time={0}".format(report["output_first_bar_time"]))
    print("output_last_bar_time={0}".format(report["output_last_bar_time"]))


if __name__ == "__main__":
    main()
