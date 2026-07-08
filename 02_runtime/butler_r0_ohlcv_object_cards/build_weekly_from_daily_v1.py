from __future__ import annotations

import argparse
import csv
import datetime as dt
from decimal import Decimal
from pathlib import Path


REQUIRED_COLUMNS = {"date", "open", "high", "low", "close", "volume"}
OUTPUT_COLUMNS = ["date", "open", "high", "low", "close", "volume", "amount", "symbol", "source_timeframe"]


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        raise ValueError(f"input csv has no rows: {csv_path}")
    missing = REQUIRED_COLUMNS - set(rows[0].keys())
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")
    return rows


def parse_date(value: str) -> dt.date:
    return dt.datetime.strptime(value, "%Y-%m-%d").date()


def to_float(row: dict[str, str], key: str) -> float:
    raw = (row.get(key) or "").strip()
    return float(raw) if raw else 0.0


def to_decimal(row: dict[str, str], key: str) -> Decimal:
    raw = (row.get(key) or "").strip()
    return Decimal(raw) if raw else Decimal("0")


def aggregate_weekly(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    ordered = sorted(rows, key=lambda r: parse_date(r["date"]))
    buckets: dict[tuple[int, int], list[dict[str, str]]] = {}
    for row in ordered:
        trade_date = parse_date(row["date"])
        iso_year, iso_week, _ = trade_date.isocalendar()
        buckets.setdefault((iso_year, iso_week), []).append(row)

    weekly_rows: list[dict[str, str]] = []
    for _, bucket in sorted(buckets.items()):
        first_row = bucket[0]
        last_row = bucket[-1]
        weekly_rows.append(
            {
                "date": last_row["date"],
                "open": first_row["open"],
                "high": f"{max(to_float(r, 'high') for r in bucket):.10f}".rstrip("0").rstrip("."),
                "low": f"{min(to_float(r, 'low') for r in bucket):.10f}".rstrip("0").rstrip("."),
                "close": last_row["close"],
                "volume": str(int(round(sum(to_float(r, "volume") for r in bucket)))),
                "amount": format(sum(to_decimal(r, "amount") for r in bucket), "f"),
                "symbol": last_row.get("symbol", ""),
                "source_timeframe": "1d_to_1w",
            }
        )
    return weekly_rows


def write_rows(csv_path: Path, rows: list[dict[str, str]]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build weekly OHLCV sample from daily OHLCV sample.")
    parser.add_argument("--input-csv", required=True, help="Daily OHLCV csv")
    parser.add_argument("--output-csv", required=True, help="Weekly OHLCV csv")
    args = parser.parse_args()

    input_csv = Path(args.input_csv)
    output_csv = Path(args.output_csv)
    rows = load_rows(input_csv)
    weekly_rows = aggregate_weekly(rows)
    if not weekly_rows:
        raise ValueError("no weekly rows generated")
    write_rows(output_csv, weekly_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
