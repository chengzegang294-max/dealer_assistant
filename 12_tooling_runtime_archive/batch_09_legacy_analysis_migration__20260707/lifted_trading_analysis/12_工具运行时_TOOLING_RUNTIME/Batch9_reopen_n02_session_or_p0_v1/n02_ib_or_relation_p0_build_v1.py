from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

RUNTIME_DIR = Path(__file__).parent
IB_OBJECT_PATH = RUNTIME_DIR / "n02_ib_object_p0_sample_v1.csv"
OR_RUNTIME_PATH = RUNTIME_DIR / "n02_p0_fields_runtime_v2.csv"
OUTPUT_CSV_PATH = RUNTIME_DIR / "n02_ib_or_relation_p0_sample_v1.csv"
SUMMARY_JSON_PATH = RUNTIME_DIR / "n02_ib_or_relation_p0_summary_v1.json"

IB_OBJECT_COLUMNS = [
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

OR_RUNTIME_COLUMNS = [
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
    "first_break_mode",
    "width_error_day",
]

OUTPUT_COLUMNS = [
    "relation_id",
    "relation_family",
    "relation_level",
    "relation_status",
    "source_ib_object_id",
    "source_or_row_key",
    "symbol",
    "timeframe",
    "session_id",
    "session_timezone",
    "session_local_date",
    "ib_window_minutes",
    "opening_range_window_minutes",
    "ib_start_utc",
    "ib_end_utc",
    "or_bar_time_utc",
    "ib_high",
    "ib_low",
    "ib_range",
    "opening_range_high",
    "opening_range_low",
    "opening_range_width",
    "or_inside_ib",
    "ib_equals_or",
    "ib_width_minus_or_width",
    "ib_width_to_or_width_ratio",
    "or_high_to_ib_high_gap",
    "or_low_to_ib_low_gap",
    "first_break_direction",
    "first_break_mode",
    "width_error_day",
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


def to_decimal(value: str) -> Optional[Decimal]:
    if value in ("", "na", "NA", "None", None):
        return None
    try:
        return Decimal(value)
    except InvalidOperation:
        return None


def parse_utc_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def format_decimal(value: Optional[Decimal]) -> str:
    return "" if value is None else str(value)


def make_or_local_date(row: Dict[str, str]) -> str:
    dt_utc = parse_utc_iso(row.get("bar_time", ""))
    tz = ZoneInfo(row.get("session_timezone", "UTC"))
    return dt_utc.astimezone(tz).date().isoformat()


def ib_key(row: Dict[str, str]) -> Tuple[str, str, str, str, str]:
    return (
        row.get("symbol", ""),
        row.get("timeframe", ""),
        row.get("session_id", ""),
        row.get("session_local_date", ""),
        row.get("session_timezone", ""),
    )


def or_key(row: Dict[str, str]) -> Tuple[str, str, str, str, str]:
    return (
        row.get("symbol", ""),
        row.get("timeframe", ""),
        row.get("session_id", ""),
        make_or_local_date(row),
        row.get("session_timezone", ""),
    )


def build_or_row_key(row: Dict[str, str]) -> str:
    return "OR|{0}|{1}|{2}|{3}|{4}".format(
        row.get("symbol", ""),
        row.get("timeframe", ""),
        row.get("session_id", ""),
        make_or_local_date(row),
        row.get("opening_range_window_minutes", ""),
    )


def build_relation_row(ib_row: Dict[str, str], or_row: Dict[str, str]) -> Dict[str, str]:
    ib_high = to_decimal(ib_row.get("ib_high", ""))
    ib_low = to_decimal(ib_row.get("ib_low", ""))
    ib_range = to_decimal(ib_row.get("ib_range", ""))
    or_high = to_decimal(or_row.get("opening_range_high", ""))
    or_low = to_decimal(or_row.get("opening_range_low", ""))
    or_width = to_decimal(or_row.get("opening_range_width", ""))

    or_inside_ib = (
        ib_high is not None
        and ib_low is not None
        and or_high is not None
        and or_low is not None
        and or_high <= ib_high
        and or_low >= ib_low
    )
    ib_equals_or = (
        ib_high is not None
        and ib_low is not None
        and or_high is not None
        and or_low is not None
        and ib_high == or_high
        and ib_low == or_low
    )
    width_minus = ib_range - or_width if ib_range is not None and or_width is not None else None
    width_ratio = ib_range / or_width if ib_range is not None and or_width not in (None, Decimal("0")) else None
    high_gap = ib_high - or_high if ib_high is not None and or_high is not None else None
    low_gap = or_low - ib_low if ib_low is not None and or_low is not None else None

    relation_key = "{0}|IB{1}|OR{2}".format(
        ib_row.get("source_runtime_row_key", ""),
        ib_row.get("ib_window_minutes", ""),
        or_row.get("opening_range_window_minutes", ""),
    )
    return {
        "relation_id": "IBOR|{0}".format(relation_key),
        "relation_family": "IB_OR_RELATION",
        "relation_level": "RELATION_P0",
        "relation_status": "aligned_defined_pair",
        "source_ib_object_id": ib_row.get("object_id", ""),
        "source_or_row_key": build_or_row_key(or_row),
        "symbol": ib_row.get("symbol", ""),
        "timeframe": ib_row.get("timeframe", ""),
        "session_id": ib_row.get("session_id", ""),
        "session_timezone": ib_row.get("session_timezone", ""),
        "session_local_date": ib_row.get("session_local_date", ""),
        "ib_window_minutes": ib_row.get("ib_window_minutes", ""),
        "opening_range_window_minutes": or_row.get("opening_range_window_minutes", ""),
        "ib_start_utc": ib_row.get("ib_start_utc", ""),
        "ib_end_utc": ib_row.get("ib_end_utc", ""),
        "or_bar_time_utc": or_row.get("bar_time", ""),
        "ib_high": ib_row.get("ib_high", ""),
        "ib_low": ib_row.get("ib_low", ""),
        "ib_range": ib_row.get("ib_range", ""),
        "opening_range_high": or_row.get("opening_range_high", ""),
        "opening_range_low": or_row.get("opening_range_low", ""),
        "opening_range_width": or_row.get("opening_range_width", ""),
        "or_inside_ib": "1" if or_inside_ib else "0",
        "ib_equals_or": "1" if ib_equals_or else "0",
        "ib_width_minus_or_width": format_decimal(width_minus),
        "ib_width_to_or_width_ratio": format_decimal(width_ratio),
        "or_high_to_ib_high_gap": format_decimal(high_gap),
        "or_low_to_ib_low_gap": format_decimal(low_gap),
        "first_break_direction": or_row.get("first_break_direction", ""),
        "first_break_mode": or_row.get("first_break_mode", ""),
        "width_error_day": or_row.get("width_error_day", ""),
    }


def sort_key(row: Dict[str, str]) -> Tuple[str, str, str, str]:
    return (
        row.get("session_local_date", ""),
        row.get("session_id", ""),
        row.get("symbol", ""),
        row.get("timeframe", ""),
    )


def build_summary(
    ib_input_path: Path,
    or_input_path: Path,
    output_csv_path: Path,
    summary_json_path: Path,
    ib_rows: List[Dict[str, str]],
    or_rows: List[Dict[str, str]],
    relation_rows: List[Dict[str, str]],
    missing_or_rows: List[Dict[str, str]],
) -> Dict[str, object]:
    by_session: Dict[str, Dict[str, object]] = defaultdict(
        lambda: {
            "relation_rows": 0,
            "or_inside_ib_rows": 0,
            "ib_equals_or_rows": 0,
            "width_error_day_rows": 0,
            "first_local_date": "",
            "last_local_date": "",
        }
    )
    first_break_direction_counts: Dict[str, int] = defaultdict(int)
    first_break_mode_counts: Dict[str, int] = defaultdict(int)
    width_ratios: List[Decimal] = []

    for row in relation_rows:
        session_id = row.get("session_id", "")
        stats = by_session[session_id]
        stats["relation_rows"] = int(stats["relation_rows"]) + 1
        stats["or_inside_ib_rows"] = int(stats["or_inside_ib_rows"]) + (1 if row.get("or_inside_ib") == "1" else 0)
        stats["ib_equals_or_rows"] = int(stats["ib_equals_or_rows"]) + (1 if row.get("ib_equals_or") == "1" else 0)
        stats["width_error_day_rows"] = int(stats["width_error_day_rows"]) + (1 if row.get("width_error_day") == "1" else 0)
        local_date = row.get("session_local_date", "")
        if not stats["first_local_date"] or local_date < stats["first_local_date"]:
            stats["first_local_date"] = local_date
        if not stats["last_local_date"] or local_date > stats["last_local_date"]:
            stats["last_local_date"] = local_date
        first_break_direction_counts[row.get("first_break_direction", "")] += 1
        first_break_mode_counts[row.get("first_break_mode", "")] += 1
        ratio_value = to_decimal(row.get("ib_width_to_or_width_ratio", ""))
        if ratio_value is not None:
            width_ratios.append(ratio_value)

    summary_by_session: Dict[str, Dict[str, object]] = {}
    for session_id in sorted(by_session.keys()):
        stats = by_session[session_id]
        relation_count = int(stats["relation_rows"])
        summary_by_session[session_id] = {
            "relation_rows": relation_count,
            "or_inside_ib_rows": int(stats["or_inside_ib_rows"]),
            "or_inside_ib_ratio": int(stats["or_inside_ib_rows"]) / relation_count if relation_count else 0.0,
            "ib_equals_or_rows": int(stats["ib_equals_or_rows"]),
            "width_error_day_rows": int(stats["width_error_day_rows"]),
            "first_local_date": stats["first_local_date"],
            "last_local_date": stats["last_local_date"],
        }

    return {
        "producer": "n02_ib_or_relation_p0_build_v1.py",
        "scope": "REOPEN_B9_N02_IB_OR_RELATION_P0",
        "status": "fresh_run_relation_sample_summary",
        "evidence_mode": "fresh_run_join_of_ib_object_and_or_runtime",
        "source_path": {
            "ib_object_sample_csv": str(ib_input_path),
            "or_runtime_csv": str(or_input_path),
        },
        "repo_path": {
            "relation_sample_csv": str(output_csv_path),
            "summary_json": str(summary_json_path),
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "boundary": {
            "writes_to_n02_p0_runtime_csv": False,
            "writes_to_n02_ib_runtime_csv": False,
            "includes_acceptance": False,
            "includes_failed_breakout": False,
            "includes_retest_reject": False,
            "includes_day_type": False,
        },
        "ib_object_rows_input": len(ib_rows),
        "or_runtime_rows_input": len(or_rows),
        "relation_rows_written": len(relation_rows),
        "missing_or_match_rows": len(missing_or_rows),
        "or_inside_ib_rows": sum(1 for row in relation_rows if row.get("or_inside_ib") == "1"),
        "or_inside_ib_ratio": (
            sum(1 for row in relation_rows if row.get("or_inside_ib") == "1") / len(relation_rows)
            if relation_rows
            else 0.0
        ),
        "ib_equals_or_rows": sum(1 for row in relation_rows if row.get("ib_equals_or") == "1"),
        "width_error_day_rows": sum(1 for row in relation_rows if row.get("width_error_day") == "1"),
        "first_break_direction_counts": dict(sorted(first_break_direction_counts.items())),
        "first_break_mode_counts": dict(sorted(first_break_mode_counts.items())),
        "by_session": summary_by_session,
        "ib_width_to_or_width_ratio_stats": {
            "min": str(min(width_ratios)) if width_ratios else "",
            "max": str(max(width_ratios)) if width_ratios else "",
            "avg": str(sum(width_ratios) / len(width_ratios)) if width_ratios else "",
        },
        "missing_or_match_keys": [
            "{0}|{1}|{2}|{3}|{4}".format(
                row.get("symbol", ""),
                row.get("timeframe", ""),
                row.get("session_id", ""),
                row.get("session_local_date", ""),
                row.get("session_timezone", ""),
            )
            for row in missing_or_rows
        ],
        "output_columns": OUTPUT_COLUMNS,
    }


def write_summary(path: Path, summary: Dict[str, object]) -> None:
    path.write_text(json.dumps(summary, ensure_ascii=True, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ib-object", default=str(IB_OBJECT_PATH))
    parser.add_argument("--or-runtime", default=str(OR_RUNTIME_PATH))
    parser.add_argument("--output-csv", default=str(OUTPUT_CSV_PATH))
    parser.add_argument("--summary-json", default=str(SUMMARY_JSON_PATH))
    args = parser.parse_args()

    ib_input_path = Path(args.ib_object)
    or_input_path = Path(args.or_runtime)
    output_csv_path = Path(args.output_csv)
    summary_json_path = Path(args.summary_json)

    assert_header(ib_input_path, IB_OBJECT_COLUMNS)
    assert_header(or_input_path, OR_RUNTIME_COLUMNS)

    ib_rows = read_rows(ib_input_path)
    or_rows = read_rows(or_input_path)
    defined_or_rows = [row for row in or_rows if row.get("opening_range_defined") == "1"]
    or_index = {or_key(row): row for row in defined_or_rows}

    relation_rows: List[Dict[str, str]] = []
    missing_or_rows: List[Dict[str, str]] = []
    for ib_row in ib_rows:
        matched_or_row = or_index.get(ib_key(ib_row))
        if matched_or_row is None:
            missing_or_rows.append(ib_row)
            continue
        relation_rows.append(build_relation_row(ib_row, matched_or_row))

    relation_rows = sorted(relation_rows, key=sort_key)
    write_rows(output_csv_path, relation_rows)
    summary = build_summary(
        ib_input_path,
        or_input_path,
        output_csv_path,
        summary_json_path,
        ib_rows,
        or_rows,
        relation_rows,
        missing_or_rows,
    )
    write_summary(summary_json_path, summary)

    print("ib_input_path={0}".format(ib_input_path))
    print("or_input_path={0}".format(or_input_path))
    print("output_csv_path={0}".format(output_csv_path))
    print("summary_json_path={0}".format(summary_json_path))
    print("ib_object_rows_input={0}".format(len(ib_rows)))
    print("or_runtime_rows_input={0}".format(len(or_rows)))
    print("relation_rows_written={0}".format(len(relation_rows)))
    print("missing_or_match_rows={0}".format(len(missing_or_rows)))
    print("or_inside_ib_rows={0}".format(summary["or_inside_ib_rows"]))
    print("or_inside_ib_ratio={0}".format(summary["or_inside_ib_ratio"]))
    print("ib_equals_or_rows={0}".format(summary["ib_equals_or_rows"]))
    print("width_error_day_rows={0}".format(summary["width_error_day_rows"]))
    print(
        "first_break_direction_counts={0}".format(
            json.dumps(summary["first_break_direction_counts"], ensure_ascii=True)
        )
    )
    print(
        "first_break_mode_counts={0}".format(
            json.dumps(summary["first_break_mode_counts"], ensure_ascii=True)
        )
    )
    for session_id in sorted(summary["by_session"].keys()):
        stats = summary["by_session"][session_id]
        print(
            "session_id={0} relation_rows={1} or_inside_ib_rows={2} first_local_date={3} last_local_date={4}".format(
                session_id,
                stats["relation_rows"],
                stats["or_inside_ib_rows"],
                stats["first_local_date"],
                stats["last_local_date"],
            )
        )


if __name__ == "__main__":
    main()
