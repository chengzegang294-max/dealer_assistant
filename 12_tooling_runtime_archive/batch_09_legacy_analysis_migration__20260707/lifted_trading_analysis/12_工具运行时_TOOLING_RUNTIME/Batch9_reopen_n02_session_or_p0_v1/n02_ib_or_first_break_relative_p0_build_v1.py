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
INPUT_PATH = RUNTIME_DIR / "n02_ib_or_relation_p0_sample_v1.csv"
OUTPUT_CSV_PATH = RUNTIME_DIR / "n02_ib_or_first_break_relative_p0_sample_v1.csv"
SUMMARY_JSON_PATH = RUNTIME_DIR / "n02_ib_or_first_break_relative_p0_summary_v1.json"

INPUT_COLUMNS = [
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

OUTPUT_COLUMNS = [
    "relative_id",
    "relative_family",
    "relative_level",
    "relative_status",
    "source_relation_id",
    "symbol",
    "timeframe",
    "session_id",
    "session_timezone",
    "session_local_date",
    "ib_window_minutes",
    "opening_range_window_minutes",
    "first_break_direction",
    "first_break_mode",
    "break_side",
    "or_break_edge_value",
    "ib_same_side_edge_value",
    "same_side_gap_to_ib",
    "shared_boundary_on_break_side",
    "first_break_relative_case",
    "can_confirm_ib_break_from_current_fields",
    "requires_break_price_for_ib_confirmation",
    "inference_scope",
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
    if value in ("", "na", "NA", None):
        return None
    try:
        return Decimal(value)
    except InvalidOperation:
        return None


def format_decimal(value: Optional[Decimal]) -> str:
    return "" if value is None else str(value)


def build_relative_row(row: Dict[str, str]) -> Dict[str, str]:
    direction = row.get("first_break_direction", "")
    break_side = direction if direction in ("up", "down") else "none"
    if break_side == "up":
        or_edge = to_decimal(row.get("opening_range_high", ""))
        ib_edge = to_decimal(row.get("ib_high", ""))
        gap = to_decimal(row.get("or_high_to_ib_high_gap", ""))
    elif break_side == "down":
        or_edge = to_decimal(row.get("opening_range_low", ""))
        ib_edge = to_decimal(row.get("ib_low", ""))
        gap = to_decimal(row.get("or_low_to_ib_low_gap", ""))
    else:
        or_edge = None
        ib_edge = None
        gap = None

    shared_boundary = gap is not None and gap == 0
    if break_side == "none":
        relative_case = "no_break"
        can_confirm_ib_break = False
        requires_break_price = False
        status = "no_break_relative_inference"
    elif shared_boundary:
        relative_case = "shared_edge_break"
        can_confirm_ib_break = True
        requires_break_price = False
        status = "shared_edge_confirmed_from_current_fields"
    else:
        relative_case = "or_break_with_ib_same_side_gap_remaining"
        can_confirm_ib_break = False
        requires_break_price = True
        status = "conservative_gap_remaining_inference"

    return {
        "relative_id": "IBORFB|{0}".format(row.get("relation_id", "")),
        "relative_family": "IB_OR_FIRST_BREAK_RELATIVE",
        "relative_level": "RELATION_P0",
        "relative_status": status,
        "source_relation_id": row.get("relation_id", ""),
        "symbol": row.get("symbol", ""),
        "timeframe": row.get("timeframe", ""),
        "session_id": row.get("session_id", ""),
        "session_timezone": row.get("session_timezone", ""),
        "session_local_date": row.get("session_local_date", ""),
        "ib_window_minutes": row.get("ib_window_minutes", ""),
        "opening_range_window_minutes": row.get("opening_range_window_minutes", ""),
        "first_break_direction": direction,
        "first_break_mode": row.get("first_break_mode", ""),
        "break_side": break_side,
        "or_break_edge_value": format_decimal(or_edge),
        "ib_same_side_edge_value": format_decimal(ib_edge),
        "same_side_gap_to_ib": format_decimal(gap),
        "shared_boundary_on_break_side": "1" if shared_boundary else "0",
        "first_break_relative_case": relative_case,
        "can_confirm_ib_break_from_current_fields": "1" if can_confirm_ib_break else "0",
        "requires_break_price_for_ib_confirmation": "1" if requires_break_price else "0",
        "inference_scope": "edge_alignment_only",
        "width_error_day": row.get("width_error_day", ""),
    }


def sort_key(row: Dict[str, str]) -> Tuple[str, str, str, str]:
    return (
        row.get("session_local_date", ""),
        row.get("session_id", ""),
        row.get("symbol", ""),
        row.get("timeframe", ""),
    )


def build_summary(
    input_path: Path,
    output_csv_path: Path,
    summary_json_path: Path,
    input_rows: List[Dict[str, str]],
    output_rows: List[Dict[str, str]],
) -> Dict[str, object]:
    case_counts: Dict[str, int] = defaultdict(int)
    direction_counts: Dict[str, int] = defaultdict(int)
    mode_counts: Dict[str, int] = defaultdict(int)
    gaps: List[Decimal] = []
    by_session: Dict[str, Dict[str, object]] = defaultdict(
        lambda: {
            "rows": 0,
            "shared_edge_break_rows": 0,
            "gap_remaining_rows": 0,
            "requires_break_price_rows": 0,
            "first_local_date": "",
            "last_local_date": "",
        }
    )

    for row in output_rows:
        case_counts[row.get("first_break_relative_case", "")] += 1
        direction_counts[row.get("first_break_direction", "")] += 1
        mode_counts[row.get("first_break_mode", "")] += 1
        gap = to_decimal(row.get("same_side_gap_to_ib", ""))
        if gap is not None:
            gaps.append(gap)
        session_id = row.get("session_id", "")
        stats = by_session[session_id]
        stats["rows"] = int(stats["rows"]) + 1
        if row.get("first_break_relative_case") == "shared_edge_break":
            stats["shared_edge_break_rows"] = int(stats["shared_edge_break_rows"]) + 1
        if row.get("first_break_relative_case") == "or_break_with_ib_same_side_gap_remaining":
            stats["gap_remaining_rows"] = int(stats["gap_remaining_rows"]) + 1
        if row.get("requires_break_price_for_ib_confirmation") == "1":
            stats["requires_break_price_rows"] = int(stats["requires_break_price_rows"]) + 1
        local_date = row.get("session_local_date", "")
        if not stats["first_local_date"] or local_date < stats["first_local_date"]:
            stats["first_local_date"] = local_date
        if not stats["last_local_date"] or local_date > stats["last_local_date"]:
            stats["last_local_date"] = local_date

    summary_by_session: Dict[str, Dict[str, object]] = {}
    for session_id in sorted(by_session.keys()):
        stats = by_session[session_id]
        row_count = int(stats["rows"])
        summary_by_session[session_id] = {
            "rows": row_count,
            "shared_edge_break_rows": int(stats["shared_edge_break_rows"]),
            "gap_remaining_rows": int(stats["gap_remaining_rows"]),
            "requires_break_price_rows": int(stats["requires_break_price_rows"]),
            "shared_edge_break_ratio": int(stats["shared_edge_break_rows"]) / row_count if row_count else 0.0,
            "first_local_date": stats["first_local_date"],
            "last_local_date": stats["last_local_date"],
        }

    shared_edge_rows = sum(1 for row in output_rows if row.get("first_break_relative_case") == "shared_edge_break")
    gap_remaining_rows = sum(
        1 for row in output_rows if row.get("first_break_relative_case") == "or_break_with_ib_same_side_gap_remaining"
    )
    requires_break_price_rows = sum(
        1 for row in output_rows if row.get("requires_break_price_for_ib_confirmation") == "1"
    )
    can_confirm_rows = sum(
        1 for row in output_rows if row.get("can_confirm_ib_break_from_current_fields") == "1"
    )

    return {
        "producer": "n02_ib_or_first_break_relative_p0_build_v1.py",
        "scope": "REOPEN_B9_N02_IB_OR_FIRST_BREAK_RELATIVE_P0",
        "status": "fresh_run_first_break_relative_sample_summary",
        "evidence_mode": "fresh_run_derived_from_ib_or_relation_sample",
        "source_path": {
            "ib_or_relation_sample_csv": str(input_path),
        },
        "repo_path": {
            "first_break_relative_sample_csv": str(output_csv_path),
            "summary_json": str(summary_json_path),
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "boundary": {
            "writes_to_n02_p0_runtime_csv": False,
            "writes_to_n02_ib_runtime_csv": False,
            "writes_to_ib_or_relation_csv": False,
            "includes_acceptance": False,
            "includes_failed_breakout": False,
            "includes_retest_reject": False,
            "includes_day_type": False,
            "confirms_ib_break_only_when_shared_edge": True,
        },
        "input_rows": len(input_rows),
        "output_rows_written": len(output_rows),
        "first_break_relative_case_counts": dict(sorted(case_counts.items())),
        "first_break_direction_counts": dict(sorted(direction_counts.items())),
        "first_break_mode_counts": dict(sorted(mode_counts.items())),
        "shared_edge_break_rows": shared_edge_rows,
        "gap_remaining_rows": gap_remaining_rows,
        "can_confirm_ib_break_rows": can_confirm_rows,
        "requires_break_price_rows": requires_break_price_rows,
        "requires_break_price_ratio": requires_break_price_rows / len(output_rows) if output_rows else 0.0,
        "by_session": summary_by_session,
        "same_side_gap_to_ib_stats": {
            "min": str(min(gaps)) if gaps else "",
            "max": str(max(gaps)) if gaps else "",
            "avg": str(sum(gaps) / len(gaps)) if gaps else "",
        },
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
    input_rows = read_rows(input_path)
    output_rows = sorted([build_relative_row(row) for row in input_rows], key=sort_key)

    write_rows(output_csv_path, output_rows)
    summary = build_summary(input_path, output_csv_path, summary_json_path, input_rows, output_rows)
    write_summary(summary_json_path, summary)

    print("input_path={0}".format(input_path))
    print("output_csv_path={0}".format(output_csv_path))
    print("summary_json_path={0}".format(summary_json_path))
    print("input_rows={0}".format(len(input_rows)))
    print("output_rows_written={0}".format(len(output_rows)))
    print(
        "first_break_relative_case_counts={0}".format(
            json.dumps(summary["first_break_relative_case_counts"], ensure_ascii=True)
        )
    )
    print("shared_edge_break_rows={0}".format(summary["shared_edge_break_rows"]))
    print("gap_remaining_rows={0}".format(summary["gap_remaining_rows"]))
    print("can_confirm_ib_break_rows={0}".format(summary["can_confirm_ib_break_rows"]))
    print("requires_break_price_rows={0}".format(summary["requires_break_price_rows"]))
    print("requires_break_price_ratio={0}".format(summary["requires_break_price_ratio"]))
    for session_id in sorted(summary["by_session"].keys()):
        stats = summary["by_session"][session_id]
        print(
            "session_id={0} rows={1} shared_edge_break_rows={2} gap_remaining_rows={3} requires_break_price_rows={4}".format(
                session_id,
                stats["rows"],
                stats["shared_edge_break_rows"],
                stats["gap_remaining_rows"],
                stats["requires_break_price_rows"],
            )
        )


if __name__ == "__main__":
    main()
