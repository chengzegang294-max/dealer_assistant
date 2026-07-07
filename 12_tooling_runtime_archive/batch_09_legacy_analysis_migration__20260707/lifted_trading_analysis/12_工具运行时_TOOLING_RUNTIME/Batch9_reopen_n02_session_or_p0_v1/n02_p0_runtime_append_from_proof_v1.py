from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
CSV_PATH = RUNTIME_DIR / "n02_p0_fields_runtime_v1.csv"
PROOF_PATH = RUNTIME_DIR / "real_input_samples" / "n02_proof_of_mapping_output_v1.csv"

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

EXAMPLE_ROW = {
    "symbol": "EURUSD",
    "timeframe": "H1",
    "bar_time": "2026-06-12T08:30:00Z",
    "session_id": "london",
    "session_timezone": "Europe/London",
    "opening_range_window_minutes": "30",
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


def assert_header(path: Path) -> None:
    with path.open("r", encoding="utf-8", newline="") as f:
        header = next(csv.reader(f))
    if header != CSV_COLUMNS:
        raise ValueError("header mismatch: {0}".format(path))


def read_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def row_key(row: dict) -> tuple[str, str, str, str]:
    return (
        row.get("symbol", ""),
        row.get("timeframe", ""),
        row.get("bar_time", ""),
        row.get("session_id", ""),
    )


def is_example_row(row: dict) -> bool:
    return all(str(row.get(k, "")) == v for k, v in EXAMPLE_ROW.items())


def remove_seed_rows(rows: list[dict]) -> list[dict]:
    cleaned: list[dict] = []
    for row in rows:
        if row.get("symbol") == "__PLACEHOLDER__":
            continue
        if is_example_row(row):
            continue
        cleaned.append(row)
    return cleaned


def dedupe_rows(rows: list[dict]) -> list[dict]:
    seen: dict[tuple[str, str, str, str], dict] = {}
    for row in rows:
        seen[row_key(row)] = row
    return [seen[k] for k in sorted(seen.keys(), key=lambda x: (x[2], x[3]))]


def write_rows(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proof", default=str(PROOF_PATH))
    parser.add_argument("--dest", default=str(CSV_PATH))
    parser.add_argument("--persist", action="store_true")
    args = parser.parse_args()

    proof_path = Path(args.proof)
    dest_path = Path(args.dest)

    assert_header(proof_path)
    assert_header(dest_path)

    runtime_rows = remove_seed_rows(read_rows(dest_path))
    proof_rows = read_rows(proof_path)
    merged_rows = dedupe_rows(runtime_rows + proof_rows)

    print("mode={0}".format("persist" if args.persist else "dry_run"))
    print("proof_path={0}".format(proof_path))
    print("dest_path={0}".format(dest_path))
    print("runtime_rows_before_cleanup={0}".format(len(read_rows(dest_path))))
    print("runtime_rows_after_cleanup={0}".format(len(runtime_rows)))
    print("proof_rows={0}".format(len(proof_rows)))
    print("runtime_rows_after_append={0}".format(len(merged_rows)))
    if merged_rows:
        print("first_runtime_row={0}".format(json.dumps(merged_rows[0], ensure_ascii=True)))
        print("last_runtime_row={0}".format(json.dumps(merged_rows[-1], ensure_ascii=True)))

    if args.persist:
        write_rows(dest_path, merged_rows)
        print("persisted_to={0}".format(dest_path))
    else:
        print("dry_run_only=true")


if __name__ == "__main__":
    main()
