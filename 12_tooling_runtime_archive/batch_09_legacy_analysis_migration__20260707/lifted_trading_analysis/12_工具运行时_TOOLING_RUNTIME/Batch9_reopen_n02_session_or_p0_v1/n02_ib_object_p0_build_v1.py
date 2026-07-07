from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Dict, List, Optional, Tuple

RUNTIME_DIR = Path(__file__).parent
INPUT_PATH = RUNTIME_DIR / "n02_ib_fields_runtime_v1.csv"
OUTPUT_CSV_PATH = RUNTIME_DIR / "n02_ib_object_p0_sample_v1.csv"
SUMMARY_JSON_PATH = RUNTIME_DIR / "n02_ib_object_p0_summary_v1.json"

INPUT_COLUMNS = [
    "symbol",
    "timeframe",
    "session_id",
    "session_timezone",
    "session_local_date",
    "ib_window_minutes",
    "ib_start_utc",
    "ib_end_utc",
    "ib_high",
    "ib_low",
    "ib_range",
    "ib_mid",
    "bars_in_ib_window",
    "ib_defined",
]

OUTPUT_COLUMNS = [
    "object_id",
    "object_family",
    "object_level",
    "object_status",
    "source_runtime_row_key",
    "symbol",
    "timeframe",
    "session_id",
    "session_timezone",
    "session_local_date",
    "ib_window_minutes",
    "ib_start_utc",
    "ib_end_utc",
    "ib_high",
    "ib_low",
    "ib_range",
    "ib_mid",
    "bars_in_ib_window",
]


def assert_header(path: Path, expected: List[str]) -> None:
    with path.open("r", encoding="utf-8", newline="") as f:
        header = next(csv.reader(f))
    if header != expected:
        raise ValueError("header mismatch: {0}".format(path))


def read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, rows: List[Dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def row_key(row: Dict[str, str]) -> Tuple[str, str, str, str, str]:
    return (
        row.get("symbol", ""),
        row.get("timeframe", ""),
        row.get("session_id", ""),
        row.get("session_local_date", ""),
        row.get("ib_window_minutes", ""),
    )


def to_decimal(value: str) -> Optional[Decimal]:
    if not value:
        return None
    try:
        return Decimal(value)
    except InvalidOperation:
        return None


def build_object_row(row: Dict[str, str]) -> Dict[str, str]:
    source_key = "|".join(row_key(row))
    return {
        "object_id": "IB|{0}".format(source_key),
        "object_family": "IB",
        "object_level": "OBJECT_P0",
        "object_status": "defined_from_ib_runtime_v1",
        "source_runtime_row_key": source_key,
        "symbol": row.get("symbol", ""),
        "timeframe": row.get("timeframe", ""),
        "session_id": row.get("session_id", ""),
        "session_timezone": row.get("session_timezone", ""),
        "session_local_date": row.get("session_local_date", ""),
        "ib_window_minutes": row.get("ib_window_minutes", ""),
        "ib_start_utc": row.get("ib_start_utc", ""),
        "ib_end_utc": row.get("ib_end_utc", ""),
        "ib_high": row.get("ib_high", ""),
        "ib_low": row.get("ib_low", ""),
        "ib_range": row.get("ib_range", ""),
        "ib_mid": row.get("ib_mid", ""),
        "bars_in_ib_window": row.get("bars_in_ib_window", ""),
    }


def sort_key(row: Dict[str, str]) -> Tuple[str, str, str, str, str]:
    return (
        row.get("session_local_date", ""),
        row.get("session_id", ""),
        row.get("ib_window_minutes", ""),
        row.get("symbol", ""),
        row.get("timeframe", ""),
    )


def dedupe_rows(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    seen: Dict[str, Dict[str, str]] = {}
    for row in rows:
        seen[row.get("object_id", "")] = row
    return [seen[key] for key in sorted(seen.keys())]


def build_summary(
    input_path: Path,
    output_csv_path: Path,
    summary_json_path: Path,
    source_rows: List[Dict[str, str]],
    object_rows: List[Dict[str, str]],
) -> Dict[str, object]:
    source_defined_rows = [row for row in source_rows if row.get("ib_defined") == "1"]
    source_undefined_rows = len(source_rows) - len(source_defined_rows)
    ib_ranges = [value for value in (to_decimal(row.get("ib_range", "")) for row in object_rows) if value is not None]

    object_by_session: Dict[str, Dict[str, object]] = defaultdict(
        lambda: {
            "object_rows": 0,
            "first_local_date": "",
            "last_local_date": "",
            "min_ib_range": None,
            "max_ib_range": None,
        }
    )
    for row in object_rows:
        session_id = row.get("session_id", "")
        stats = object_by_session[session_id]
        stats["object_rows"] = int(stats["object_rows"]) + 1
        local_date = row.get("session_local_date", "")
        if not stats["first_local_date"] or local_date < stats["first_local_date"]:
            stats["first_local_date"] = local_date
        if not stats["last_local_date"] or local_date > stats["last_local_date"]:
            stats["last_local_date"] = local_date
        range_value = to_decimal(row.get("ib_range", ""))
        if range_value is not None:
            min_value = stats["min_ib_range"]
            max_value = stats["max_ib_range"]
            if min_value is None or range_value < min_value:
                stats["min_ib_range"] = range_value
            if max_value is None or range_value > max_value:
                stats["max_ib_range"] = range_value

    session_coverage: Dict[str, Dict[str, object]] = defaultdict(
        lambda: {"source_rows": 0, "defined_rows": 0, "undefined_rows": 0}
    )
    for row in source_rows:
        session_id = row.get("session_id", "")
        session_coverage[session_id]["source_rows"] = int(session_coverage[session_id]["source_rows"]) + 1
        if row.get("ib_defined") == "1":
            session_coverage[session_id]["defined_rows"] = int(session_coverage[session_id]["defined_rows"]) + 1
        else:
            session_coverage[session_id]["undefined_rows"] = int(session_coverage[session_id]["undefined_rows"]) + 1

    summary_by_session: Dict[str, Dict[str, object]] = {}
    for session_id in sorted(session_coverage.keys()):
        coverage_stats = session_coverage[session_id]
        object_stats = object_by_session.get(session_id, {})
        source_rows_count = int(coverage_stats["source_rows"])
        defined_rows_count = int(coverage_stats["defined_rows"])
        summary_by_session[session_id] = {
            "source_rows": source_rows_count,
            "defined_rows": defined_rows_count,
            "undefined_rows": int(coverage_stats["undefined_rows"]),
            "defined_ratio": defined_rows_count / source_rows_count if source_rows_count else 0.0,
            "object_rows": int(object_stats.get("object_rows", 0)),
            "first_local_date": object_stats.get("first_local_date", ""),
            "last_local_date": object_stats.get("last_local_date", ""),
            "min_ib_range": str(object_stats["min_ib_range"]) if object_stats.get("min_ib_range") is not None else "",
            "max_ib_range": str(object_stats["max_ib_range"]) if object_stats.get("max_ib_range") is not None else "",
        }

    unique_symbols = sorted({row.get("symbol", "") for row in object_rows if row.get("symbol", "")})
    unique_timeframes = sorted({row.get("timeframe", "") for row in object_rows if row.get("timeframe", "")})

    return {
        "producer": "n02_ib_object_p0_build_v1.py",
        "scope": "REOPEN_B9_N02_IB_OBJECT_P0",
        "status": "fresh_run_object_sample_summary",
        "evidence_mode": "fresh_run_derived_from_ib_runtime_csv",
        "source_path": str(input_path),
        "repo_path": {
            "sample_csv": str(output_csv_path),
            "summary_json": str(summary_json_path),
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "boundary": {
            "writes_to_n02_p0_runtime_csv": False,
            "includes_acceptance": False,
            "includes_failed_breakout": False,
            "includes_retest_reject": False,
            "includes_day_type": False,
        },
        "source_rows": len(source_rows),
        "source_defined_rows": len(source_defined_rows),
        "source_undefined_rows": source_undefined_rows,
        "object_rows_written": len(object_rows),
        "symbol_values": unique_symbols,
        "timeframe_values": unique_timeframes,
        "by_session": summary_by_session,
        "ib_range_stats": {
            "min": str(min(ib_ranges)) if ib_ranges else "",
            "max": str(max(ib_ranges)) if ib_ranges else "",
            "avg": str(sum(ib_ranges) / len(ib_ranges)) if ib_ranges else "",
        },
        "first_object_id": object_rows[0]["object_id"] if object_rows else "",
        "last_object_id": object_rows[-1]["object_id"] if object_rows else "",
        "output_columns": OUTPUT_COLUMNS,
    }


def write_summary(path: Path, summary: Dict[str, object]) -> None:
    path.write_text(json.dumps(summary, ensure_ascii=True, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(INPUT_PATH))
    parser.add_argument("--output-csv", default=str(OUTPUT_CSV_PATH))
    parser.add_argument("--summary-json", default=str(SUMMARY_JSON_PATH))
    args = parser.parse_args()

    input_path = Path(args.input)
    output_csv_path = Path(args.output_csv)
    summary_json_path = Path(args.summary_json)

    assert_header(input_path, INPUT_COLUMNS)
    source_rows = read_rows(input_path)
    object_rows = dedupe_rows(
        [
            build_object_row(row)
            for row in source_rows
            if row.get("ib_defined") == "1"
        ]
    )
    object_rows = sorted(object_rows, key=sort_key)

    write_rows(output_csv_path, object_rows)
    summary = build_summary(input_path, output_csv_path, summary_json_path, source_rows, object_rows)
    write_summary(summary_json_path, summary)

    print("input_path={0}".format(input_path))
    print("output_csv_path={0}".format(output_csv_path))
    print("summary_json_path={0}".format(summary_json_path))
    print("source_rows={0}".format(len(source_rows)))
    print("source_defined_rows={0}".format(len([row for row in source_rows if row.get('ib_defined') == '1'])))
    print("source_undefined_rows={0}".format(len([row for row in source_rows if row.get('ib_defined') != '1'])))
    print("object_rows_written={0}".format(len(object_rows)))
    for session_id in sorted(summary["by_session"].keys()):
        session_stats = summary["by_session"][session_id]
        print(
            "session_id={0} object_rows={1} defined_ratio={2} first_local_date={3} last_local_date={4}".format(
                session_id,
                session_stats["object_rows"],
                session_stats["defined_ratio"],
                session_stats["first_local_date"],
                session_stats["last_local_date"],
            )
        )


if __name__ == "__main__":
    main()
