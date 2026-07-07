from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
PARAMS_PATH = RUNTIME_DIR / "n01_p0_runtime_params_template_v1.json"
CSV_PATH = RUNTIME_DIR / "n01_p0_fields_runtime_v1.csv"
PLACEHOLDER_SYMBOL = "__PLACEHOLDER__"
EXAMPLE_SYMBOL = "EURUSD"

CSV_COLUMNS = [
    "symbol",
    "timeframe",
    "bar_time",
    "atr_value",
    "atr_ratio",
    "atr_percentile",
    "atr_percentile_regime",
    "squeeze_is_on",
    "squeeze_tier",
    "squeeze_fired",
    "compression_quality_score",
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
            and row.get("bar_time") == "2026-06-12T08:00:00Z"
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


def example_real_row() -> dict:
    return {
        "symbol": EXAMPLE_SYMBOL,
        "timeframe": "H1",
        "bar_time": "2026-06-12T08:00:00Z",
        "atr_value": "0.0021",
        "atr_ratio": "1.34",
        "atr_percentile": "84.7",
        "atr_percentile_regime": "elevated",
        "squeeze_is_on": "1",
        "squeeze_tier": "medium",
        "squeeze_fired": "0",
        "compression_quality_score": "72.5",
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
    new_row = example_real_row()
    rows.append(new_row)

    print("stub_mode={0}".format("persist" if args.persist else "dry_run"))
    print("rows_before_cleanup={0}".format(original_row_count))
    print("rows_before_append={0}".format(rows_before_append))
    print("rows_after_append={0}".format(len(rows)))
    print(
        "atr_config={0}".format(
            json.dumps(params["atr_config"], ensure_ascii=True, sort_keys=True)
        )
    )
    print("example_row={0}".format(json.dumps(new_row, ensure_ascii=True)))
    if args.persist:
        write_rows(rows)
        print("persisted_to={0}".format(CSV_PATH))
    else:
        print("dry_run_only=true")


if __name__ == "__main__":
    main()
