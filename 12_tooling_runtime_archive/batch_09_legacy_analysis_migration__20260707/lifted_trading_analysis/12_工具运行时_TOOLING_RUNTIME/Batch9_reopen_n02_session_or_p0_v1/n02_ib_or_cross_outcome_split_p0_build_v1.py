from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

RUNTIME_DIR = Path(__file__).parent
INPUT_PATH = RUNTIME_DIR / "n02_ib_or_break_bar_evidence_p0_sample_v1.csv"
CONFIRMED_OUTPUT_PATH = RUNTIME_DIR / "n02_ib_or_confirmed_cross_candidates_p0_sample_v1.csv"
OR_ONLY_OUTPUT_PATH = RUNTIME_DIR / "n02_ib_or_or_break_only_candidates_p0_sample_v1.csv"
OUTCOME_SHELL_OUTPUT_PATH = RUNTIME_DIR / "n02_ib_or_confirmed_cross_outcome_shell_p0_sample_v1.csv"
SUMMARY_OUTPUT_PATH = RUNTIME_DIR / "n02_ib_or_cross_outcome_split_p0_summary_v1.json"

INPUT_COLUMNS = [
    "evidence_id",
    "evidence_family",
    "evidence_level",
    "evidence_status",
    "source_relative_id",
    "symbol",
    "timeframe",
    "session_id",
    "session_timezone",
    "session_local_date",
    "ib_window_minutes",
    "opening_range_window_minutes",
    "upstream_first_break_direction",
    "upstream_first_break_mode",
    "first_break_direction",
    "first_break_mode",
    "direction_mode_match_to_relation",
    "break_bar_time_utc",
    "break_bar_open",
    "break_bar_high",
    "break_bar_low",
    "break_bar_close",
    "or_break_edge_value",
    "ib_same_side_edge_value",
    "break_trigger_price",
    "break_trigger_source",
    "same_side_gap_to_ib_before_break",
    "ib_same_side_cross_confirmed",
    "ib_same_side_cross_direction",
    "ib_same_side_cross_distance",
    "requires_break_price_for_ib_confirmation_before",
    "requires_break_price_for_ib_confirmation_after",
    "evidence_scope",
    "width_error_day",
]

CONFIRMED_COLUMNS = [
    "candidate_id",
    "candidate_family",
    "candidate_level",
    "candidate_status",
    "source_evidence_id",
    "symbol",
    "timeframe",
    "session_id",
    "session_timezone",
    "session_local_date",
    "break_bar_time_utc",
    "first_break_direction",
    "first_break_mode",
    "break_trigger_price",
    "ib_same_side_edge_value",
    "ib_same_side_cross_distance",
    "break_trigger_source",
    "direction_mode_match_to_relation",
    "post_cross_tracking_scope",
]

OR_ONLY_COLUMNS = [
    "candidate_id",
    "candidate_family",
    "candidate_level",
    "candidate_status",
    "source_evidence_id",
    "symbol",
    "timeframe",
    "session_id",
    "session_timezone",
    "session_local_date",
    "break_bar_time_utc",
    "first_break_direction",
    "first_break_mode",
    "break_trigger_price",
    "or_break_edge_value",
    "ib_same_side_edge_value",
    "same_side_gap_to_ib_before_break",
    "break_trigger_source",
    "direction_mode_match_to_relation",
    "split_scope",
]

OUTCOME_SHELL_COLUMNS = [
    "outcome_shell_id",
    "outcome_family",
    "outcome_level",
    "outcome_status",
    "source_confirmed_candidate_id",
    "symbol",
    "timeframe",
    "session_id",
    "session_timezone",
    "session_local_date",
    "cross_direction",
    "cross_mode",
    "cross_bar_time_utc",
    "cross_trigger_price",
    "cross_distance_over_ib",
    "next_required_evidence",
    "failed_breakout_defined",
    "retest_defined",
    "reject_defined",
    "day_type_defined",
]


def assert_header(path: Path, expected: List[str]) -> None:
    with path.open("r", encoding="utf-8", newline="") as f:
        header = next(csv.reader(f))
    if header != expected:
        raise ValueError("header mismatch: {0}".format(path))


def read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, fieldnames: List[str], rows: List[Dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_confirmed_row(row: Dict[str, str]) -> Dict[str, str]:
    return {
        "candidate_id": "IBORCROSS|{0}".format(row["evidence_id"]),
        "candidate_family": "IB_OR_CONFIRMED_CROSS_CANDIDATE",
        "candidate_level": "RELATION_P0",
        "candidate_status": "confirmed_cross_candidate",
        "source_evidence_id": row["evidence_id"],
        "symbol": row["symbol"],
        "timeframe": row["timeframe"],
        "session_id": row["session_id"],
        "session_timezone": row["session_timezone"],
        "session_local_date": row["session_local_date"],
        "break_bar_time_utc": row["break_bar_time_utc"],
        "first_break_direction": row["first_break_direction"],
        "first_break_mode": row["first_break_mode"],
        "break_trigger_price": row["break_trigger_price"],
        "ib_same_side_edge_value": row["ib_same_side_edge_value"],
        "ib_same_side_cross_distance": row["ib_same_side_cross_distance"],
        "break_trigger_source": row["break_trigger_source"],
        "direction_mode_match_to_relation": row["direction_mode_match_to_relation"],
        "post_cross_tracking_scope": "post_cross_path_pending_definition",
    }


def build_or_only_row(row: Dict[str, str]) -> Dict[str, str]:
    return {
        "candidate_id": "IBORONLY|{0}".format(row["evidence_id"]),
        "candidate_family": "IB_OR_BREAK_ONLY_CANDIDATE",
        "candidate_level": "RELATION_P0",
        "candidate_status": "or_break_only_not_ib_cross",
        "source_evidence_id": row["evidence_id"],
        "symbol": row["symbol"],
        "timeframe": row["timeframe"],
        "session_id": row["session_id"],
        "session_timezone": row["session_timezone"],
        "session_local_date": row["session_local_date"],
        "break_bar_time_utc": row["break_bar_time_utc"],
        "first_break_direction": row["first_break_direction"],
        "first_break_mode": row["first_break_mode"],
        "break_trigger_price": row["break_trigger_price"],
        "or_break_edge_value": row["or_break_edge_value"],
        "ib_same_side_edge_value": row["ib_same_side_edge_value"],
        "same_side_gap_to_ib_before_break": row["same_side_gap_to_ib_before_break"],
        "break_trigger_source": row["break_trigger_source"],
        "direction_mode_match_to_relation": row["direction_mode_match_to_relation"],
        "split_scope": "or_break_only_branch",
    }


def build_outcome_shell_row(row: Dict[str, str]) -> Dict[str, str]:
    return {
        "outcome_shell_id": "IBOROUT|{0}".format(row["candidate_id"]),
        "outcome_family": "IB_OR_CONFIRMED_CROSS_OUTCOME_SHELL",
        "outcome_level": "RELATION_P0",
        "outcome_status": "post_cross_tracking_not_started",
        "source_confirmed_candidate_id": row["candidate_id"],
        "symbol": row["symbol"],
        "timeframe": row["timeframe"],
        "session_id": row["session_id"],
        "session_timezone": row["session_timezone"],
        "session_local_date": row["session_local_date"],
        "cross_direction": row["first_break_direction"],
        "cross_mode": row["first_break_mode"],
        "cross_bar_time_utc": row["break_bar_time_utc"],
        "cross_trigger_price": row["break_trigger_price"],
        "cross_distance_over_ib": row["ib_same_side_cross_distance"],
        "next_required_evidence": "post_cross_return_inside_ib_or_continuation_path",
        "failed_breakout_defined": "0",
        "retest_defined": "0",
        "reject_defined": "0",
        "day_type_defined": "0",
    }


def sort_key(row: Dict[str, str]) -> tuple[str, str, str, str]:
    return (
        row.get("session_local_date", ""),
        row.get("session_id", ""),
        row.get("symbol", ""),
        row.get("timeframe", ""),
    )


def build_summary(
    input_path: Path,
    confirmed_path: Path,
    or_only_path: Path,
    outcome_shell_path: Path,
    summary_path: Path,
    input_rows: List[Dict[str, str]],
    confirmed_rows: List[Dict[str, str]],
    or_only_rows: List[Dict[str, str]],
    outcome_shell_rows: List[Dict[str, str]],
) -> Dict[str, object]:
    by_session: Dict[str, Dict[str, int]] = defaultdict(
        lambda: {
            "confirmed_cross_rows": 0,
            "or_break_only_rows": 0,
            "no_break_rows": 0,
            "direction_mode_mismatch_rows": 0,
        }
    )
    for row in input_rows:
        session = row["session_id"]
        if row["first_break_direction"] == "none" or row["first_break_mode"] == "none":
            by_session[session]["no_break_rows"] += 1
        elif row["ib_same_side_cross_confirmed"] == "1":
            by_session[session]["confirmed_cross_rows"] += 1
        else:
            by_session[session]["or_break_only_rows"] += 1
        if row["direction_mode_match_to_relation"] != "1":
            by_session[session]["direction_mode_mismatch_rows"] += 1

    mismatch_rows = [row for row in input_rows if row["direction_mode_match_to_relation"] != "1"]
    no_break_rows = [
        row for row in input_rows if row["first_break_direction"] == "none" or row["first_break_mode"] == "none"
    ]
    return {
        "producer": "n02_ib_or_cross_outcome_split_p0_build_v1.py",
        "scope": "REOPEN_B9_N02_IB_OR_CROSS_OUTCOME_SPLIT_P0",
        "status": "fresh_run_cross_split_and_outcome_shell",
        "evidence_mode": "fresh_run_derived_from_break_bar_evidence",
        "source_path": {
            "break_bar_evidence_sample_csv": str(input_path),
        },
        "repo_path": {
            "confirmed_cross_candidates_csv": str(confirmed_path),
            "or_break_only_candidates_csv": str(or_only_path),
            "confirmed_cross_outcome_shell_csv": str(outcome_shell_path),
            "summary_json": str(summary_path),
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "boundary": {
            "writes_to_n02_p0_runtime_csv": False,
            "writes_to_n02_ib_runtime_csv": False,
            "writes_to_break_bar_evidence_csv": False,
            "defines_failed_breakout": False,
            "defines_retest_reject": False,
            "defines_day_type": False,
        },
        "input_rows": len(input_rows),
        "confirmed_cross_rows": len(confirmed_rows),
        "or_break_only_rows": len(or_only_rows),
        "no_break_rows": len(no_break_rows),
        "confirmed_cross_ratio": len(confirmed_rows) / len(input_rows) if input_rows else 0.0,
        "or_break_only_ratio": len(or_only_rows) / len(input_rows) if input_rows else 0.0,
        "no_break_ratio": len(no_break_rows) / len(input_rows) if input_rows else 0.0,
        "outcome_shell_rows": len(outcome_shell_rows),
        "direction_mode_mismatch_rows": len(mismatch_rows),
        "direction_mode_mismatch_samples": [
            {
                "session_id": row["session_id"],
                "session_local_date": row["session_local_date"],
                "upstream_first_break_direction": row["upstream_first_break_direction"],
                "upstream_first_break_mode": row["upstream_first_break_mode"],
                "recheck_first_break_direction": row["first_break_direction"],
                "recheck_first_break_mode": row["first_break_mode"],
            }
            for row in mismatch_rows
        ],
        "by_session": dict(sorted(by_session.items())),
        "confirmed_cross_output_columns": CONFIRMED_COLUMNS,
        "or_break_only_output_columns": OR_ONLY_COLUMNS,
        "outcome_shell_output_columns": OUTCOME_SHELL_COLUMNS,
    }


def write_summary(path: Path, summary: Dict[str, object]) -> None:
    path.write_text(json.dumps(summary, ensure_ascii=True, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(INPUT_PATH))
    parser.add_argument("--confirmed-output", default=str(CONFIRMED_OUTPUT_PATH))
    parser.add_argument("--or-only-output", default=str(OR_ONLY_OUTPUT_PATH))
    parser.add_argument("--outcome-shell-output", default=str(OUTCOME_SHELL_OUTPUT_PATH))
    parser.add_argument("--summary-json", default=str(SUMMARY_OUTPUT_PATH))
    args = parser.parse_args()

    input_path = Path(args.input)
    confirmed_path = Path(args.confirmed_output)
    or_only_path = Path(args.or_only_output)
    outcome_shell_path = Path(args.outcome_shell_output)
    summary_path = Path(args.summary_json)

    assert_header(input_path, INPUT_COLUMNS)
    input_rows = read_rows(input_path)
    confirmed_rows = sorted(
        [
            build_confirmed_row(row)
            for row in input_rows
            if row["ib_same_side_cross_confirmed"] == "1"
            and row["first_break_direction"] != "none"
            and row["first_break_mode"] != "none"
        ],
        key=sort_key,
    )
    or_only_rows = sorted(
        [
            build_or_only_row(row)
            for row in input_rows
            if row["ib_same_side_cross_confirmed"] != "1"
            and row["first_break_direction"] != "none"
            and row["first_break_mode"] != "none"
        ],
        key=sort_key,
    )
    outcome_shell_rows = sorted([build_outcome_shell_row(row) for row in confirmed_rows], key=sort_key)

    write_rows(confirmed_path, CONFIRMED_COLUMNS, confirmed_rows)
    write_rows(or_only_path, OR_ONLY_COLUMNS, or_only_rows)
    write_rows(outcome_shell_path, OUTCOME_SHELL_COLUMNS, outcome_shell_rows)
    summary = build_summary(
        input_path=input_path,
        confirmed_path=confirmed_path,
        or_only_path=or_only_path,
        outcome_shell_path=outcome_shell_path,
        summary_path=summary_path,
        input_rows=input_rows,
        confirmed_rows=confirmed_rows,
        or_only_rows=or_only_rows,
        outcome_shell_rows=outcome_shell_rows,
    )
    write_summary(summary_path, summary)

    print("input_path={0}".format(input_path))
    print("confirmed_output_path={0}".format(confirmed_path))
    print("or_only_output_path={0}".format(or_only_path))
    print("outcome_shell_output_path={0}".format(outcome_shell_path))
    print("summary_json_path={0}".format(summary_path))
    print("input_rows={0}".format(len(input_rows)))
    print("confirmed_cross_rows={0}".format(len(confirmed_rows)))
    print("or_break_only_rows={0}".format(len(or_only_rows)))
    print("no_break_rows={0}".format(summary["no_break_rows"]))
    print("outcome_shell_rows={0}".format(len(outcome_shell_rows)))
    print("direction_mode_mismatch_rows={0}".format(summary["direction_mode_mismatch_rows"]))
    for session_id, stats in summary["by_session"].items():
        print(
            "session_id={0} confirmed_cross_rows={1} or_break_only_rows={2} mismatch_rows={3}".format(
                session_id,
                stats["confirmed_cross_rows"],
                stats["or_break_only_rows"],
                stats["direction_mode_mismatch_rows"],
            )
        )


if __name__ == "__main__":
    main()
