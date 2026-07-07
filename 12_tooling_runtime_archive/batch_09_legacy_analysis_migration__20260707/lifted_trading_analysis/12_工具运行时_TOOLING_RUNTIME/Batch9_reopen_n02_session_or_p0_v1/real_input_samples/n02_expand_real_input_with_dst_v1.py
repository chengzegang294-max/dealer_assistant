from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_INPUTS = [
    BASE_DIR / "n02_first_real_input_bars_v1.csv",
    BASE_DIR / "n02_dst_london_spring_20260327_20260331_bars.csv",
    BASE_DIR / "n02_dst_newyork_spring_20260306_20260310_bars.csv",
    BASE_DIR / "n02_dst_london_fall_20251023_20251028_bars.csv",
    BASE_DIR / "n02_dst_newyork_fall_20251031_20251104_bars.csv",
]
DEFAULT_OUTPUT = BASE_DIR / "n02_first_real_input_bars_v1.csv"
DEFAULT_REPORT = BASE_DIR / "n02_expand_real_input_with_dst_report_v1.json"

CSV_COLUMNS = ["symbol", "timeframe", "bar_time", "open", "high", "low", "close"]


def read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return rows


def assert_header(path: Path) -> None:
    with path.open("r", encoding="utf-8", newline="") as f:
        header = next(csv.reader(f))
    if header != CSV_COLUMNS:
        raise ValueError("header mismatch: {0}".format(path))


def row_key(row: Dict[str, str]) -> Tuple[str, str, str]:
    return (row["symbol"], row["timeframe"], row["bar_time"])


def sort_key(row: Dict[str, str]) -> Tuple[str, str, str]:
    return (row["symbol"], row["timeframe"], row["bar_time"])


def write_rows(path: Path, rows: List[Dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", default=[])
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--report-json", default=str(DEFAULT_REPORT))
    args = parser.parse_args()

    input_paths = [Path(p) for p in args.input] if args.input else list(DEFAULT_INPUTS)
    output_path = Path(args.output)
    report_path = Path(args.report_json)

    merged: Dict[Tuple[str, str, str], Dict[str, str]] = {}
    input_reports: List[Dict[str, object]] = []
    duplicate_replacements = 0
    allowed_pairs: set[Tuple[str, str]] = set()
    filtered_out_rows = 0

    for index, path in enumerate(input_paths):
        assert_header(path)
        rows = read_rows(path)
        if index == 0:
            allowed_pairs = {(row["symbol"], row["timeframe"]) for row in rows}
        kept_rows: List[Dict[str, str]] = []
        skipped_rows = 0
        for row in rows:
            if (row["symbol"], row["timeframe"]) not in allowed_pairs:
                skipped_rows += 1
                filtered_out_rows += 1
                continue
            kept_rows.append(row)
        first_bar_time = rows[0]["bar_time"] if rows else ""
        last_bar_time = rows[-1]["bar_time"] if rows else ""
        input_reports.append(
            {
                "path": str(path),
                "rows": len(rows),
                "kept_rows": len(kept_rows),
                "skipped_rows": skipped_rows,
                "first_bar_time": first_bar_time,
                "last_bar_time": last_bar_time,
            }
        )
        for row in kept_rows:
            key = row_key(row)
            if key in merged:
                duplicate_replacements += 1
            merged[key] = row

    merged_rows = [merged[k] for k in sorted(merged.keys(), key=lambda k: (k[0], k[1], k[2]))]
    backup_path = output_path.with_name(
        "{0}.bak_{1}".format(
            output_path.name,
            datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        )
    )

    if output_path.exists():
        shutil.copy2(output_path, backup_path)

    write_rows(output_path, merged_rows)

    report = {
        "producer": "n02_expand_real_input_with_dst_v1.py",
        "scope": "REOPEN_B9_N02_REAL_INPUT_EXPAND_SAMPLE_P0",
        "status": "fresh_run_expand_sample",
        "evidence_mode": "fresh_run_merge_main_bars_and_dst_supplement",
        "source_path": {
            "inputs": [str(p) for p in input_paths],
        },
        "repo_path": {
            "output_csv": str(output_path),
            "backup_csv": str(backup_path) if output_path.exists() else "",
            "report_json": str(report_path),
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "allowed_symbol_timeframes": sorted(["{0}/{1}".format(a, b) for a, b in allowed_pairs]),
        "input_reports": input_reports,
        "duplicate_replacements": duplicate_replacements,
        "filtered_out_rows": filtered_out_rows,
        "output_rows": len(merged_rows),
        "output_first_bar_time": merged_rows[0]["bar_time"] if merged_rows else "",
        "output_last_bar_time": merged_rows[-1]["bar_time"] if merged_rows else "",
    }
    report_path.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding="utf-8")

    print("output_csv={0}".format(output_path))
    print("backup_csv={0}".format(backup_path))
    print("report_json={0}".format(report_path))
    print("input_file_count={0}".format(len(input_paths)))
    print("duplicate_replacements={0}".format(duplicate_replacements))
    print("filtered_out_rows={0}".format(filtered_out_rows))
    print("output_rows={0}".format(len(merged_rows)))
    print("output_first_bar_time={0}".format(report["output_first_bar_time"]))
    print("output_last_bar_time={0}".format(report["output_last_bar_time"]))


if __name__ == "__main__":
    main()
