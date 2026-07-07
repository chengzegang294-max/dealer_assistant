from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
PARAMS_PATH = RUNTIME_DIR / "n02_p0_runtime_params_template_v1.json"
CSV_PATH = RUNTIME_DIR / "n02_p0_fields_runtime_v1.csv"
PLACEHOLDER_SYMBOL = "__PLACEHOLDER__"
EXAMPLE_SYMBOL = "EURUSD"

CSV_COLUMNS = [
    "symbol",
    "timeframe",
    "bar_time",
    "session_id",
    "session_timezone",
    "opening_range_window_minutes",
    "opening_range_high",
    "opening_range_low",
    "opening_range_mid",
    "opening_range_width",
    "opening_range_width_pct_open",
    "session_open_price",
    "opening_range_defined",
    "first_break_direction",
    "width_error_day",
]


def load_params() -> dict:
    with PARAMS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def assert_header_matches() -> None:
    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
    if header != CSV_COLUMNS:
        raise ValueError("runtime csv header does not match expected v1 contract")


def remove_placeholder_rows(rows: list[dict]) -> list[dict]:
    return [row for row in rows if row.get("symbol") != PLACEHOLDER_SYMBOL]


def remove_existing_example_rows(rows: list[dict]) -> list[dict]:
    return [
        row
        for row in rows
        if not (
            row.get("symbol") == EXAMPLE_SYMBOL
            and row.get("timeframe") == "H1"
            and row.get("bar_time") == "2026-06-12T08:30:00Z"
        )
    ]


def read_rows() -> list[dict]:
    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_rows(rows: list[dict]) -> None:
    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def example_real_row(params: dict) -> dict:
    session_cfg = params["session_config"]
    return {
        "symbol": EXAMPLE_SYMBOL,
        "timeframe": "H1",
        "bar_time": "2026-06-12T08:30:00Z",
        "session_id": session_cfg["session_id"],
        "session_timezone": session_cfg["session_timezone"],
        "opening_range_window_minutes": session_cfg["opening_range_window_minutes"],
        "opening_range_high": "na",
        "opening_range_low": "na",
        "opening_range_mid": "na",
        "opening_range_width": "na",
        "opening_range_width_pct_open": "na",
        "session_open_price": "1.2730",
        "opening_range_defined": "0",
        "first_break_direction": "none",
        "width_error_day": "0",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--persist",
        action="store_true",
        help="replace placeholder rows and persist one example row",
    )
    args = parser.parse_args()

    params = load_params()
    assert_header_matches()
    rows = read_rows()
    original_row_count = len(rows)
    rows = remove_placeholder_rows(rows)
    rows = remove_existing_example_rows(rows)
    rows_before_append = len(rows)
    new_row = example_real_row(params)
    rows.append(new_row)

    print("stub_mode={0}".format("persist" if args.persist else "dry_run"))
    print("rows_before_cleanup={0}".format(original_row_count))
    print("rows_before_append={0}".format(rows_before_append))
    print("rows_after_append={0}".format(len(rows)))
    print("example_row={0}".format(json.dumps(new_row, ensure_ascii=True)))

    if args.persist:
        write_rows(rows)
        print("persisted_to={0}".format(CSV_PATH))
    else:
        print("dry_run_only=true")


if __name__ == "__main__":
    main()
