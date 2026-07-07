from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

RUNTIME_DIR = Path(__file__).parent
BEYOND_INPUT_PATH = RUNTIME_DIR / "n02_ib_or_session_close_beyond_ib_candidates_p0_sample_v1.csv"
NOT_BEYOND_INPUT_PATH = RUNTIME_DIR / "n02_ib_or_session_close_not_beyond_ib_candidates_p0_sample_v1.csv"
POST_CROSS_INPUT_PATH = RUNTIME_DIR / "n02_ib_or_post_cross_path_observation_p0_sample_v1.csv"
BARS_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "n02_first_real_input_bars_v1.csv"
CONFIG_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "n02_or_proof_config_v1.json"
BEYOND_OUTPUT_PATH = RUNTIME_DIR / "n02_ib_or_beyond_continuation_observation_p0_sample_v1.csv"
BEYOND_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_beyond_continuation_observation_p0_summary_v1.json"
NOT_BEYOND_OUTPUT_PATH = RUNTIME_DIR / "n02_ib_or_not_beyond_pullback_stability_observation_p0_sample_v1.csv"
NOT_BEYOND_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_not_beyond_pullback_stability_observation_p0_summary_v1.json"

SESSION_CLOSE_COLUMNS = [
    "candidate_id",
    "candidate_family",
    "candidate_level",
    "candidate_status",
    "source_observation_id",
    "symbol",
    "timeframe",
    "session_id",
    "session_timezone",
    "session_local_date",
    "cross_direction",
    "cross_mode",
    "cross_bar_time_utc",
    "first_return_inside_ib_bar_time_utc",
    "session_close_price",
    "session_close_beyond_ib",
    "max_extension_distance_over_ib",
    "split_scope",
]

POST_CROSS_COLUMNS = [
    "observation_id",
    "observation_family",
    "observation_level",
    "observation_status",
    "source_outcome_shell_id",
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
    "ib_same_side_edge_value",
    "bars_after_cross_count",
    "return_inside_ib_observed_same_day",
    "first_return_inside_ib_bar_time_utc",
    "max_extension_price_same_day",
    "max_extension_distance_over_ib",
    "session_close_price",
    "session_close_beyond_ib",
    "observation_scope",
]

BARS_COLUMNS = [
    "symbol",
    "timeframe",
    "bar_time",
    "open",
    "high",
    "low",
    "close",
]

OBSERVATION_COLUMNS = [
    "observation_id",
    "observation_family",
    "observation_level",
    "observation_status",
    "source_candidate_id",
    "source_post_cross_observation_id",
    "symbol",
    "timeframe",
    "session_id",
    "session_timezone",
    "prior_session_local_date",
    "next_session_local_date",
    "cross_direction",
    "cross_mode",
    "prior_ib_same_side_edge_value",
    "next_session_open_utc",
    "next_session_first_bar_open",
    "next_session_first_bar_close",
    "next_session_first_30m_bar_count",
    "next_session_first_bar_expected_side",
    "next_session_first_30m_all_closes_expected_side",
    "next_session_first_30m_any_close_opposite_or_at_boundary",
    "observation_scope",
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


def parse_iso_utc(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def fmt_dt(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_config(path: Path) -> Dict[str, Dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["sessions"]


def load_bars(path: Path) -> List[Dict[str, str]]:
    return read_rows(path)


def sort_key(row: Dict[str, str]) -> Tuple[str, str, str, str]:
    return (
        row.get("next_session_local_date", row.get("prior_session_local_date", "")),
        row.get("session_id", ""),
        row.get("symbol", ""),
        row.get("timeframe", ""),
    )


def next_session_date(date_text: str) -> str:
    return (datetime.strptime(date_text, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")


def local_open_utc(local_date: str, session_timezone: str, open_hhmm: str) -> datetime:
    hour, minute = [int(part) for part in open_hhmm.split(":")]
    dt_local = datetime.strptime(local_date, "%Y-%m-%d").replace(hour=hour, minute=minute, tzinfo=ZoneInfo(session_timezone))
    return dt_local.astimezone(timezone.utc)


def build_window_bars(
    bars: List[Dict[str, str]],
    symbol: str,
    timeframe: str,
    start_utc: datetime,
    minutes: int,
) -> List[Dict[str, str]]:
    end_utc = start_utc + timedelta(minutes=minutes)
    rows: List[Dict[str, str]] = []
    for row in bars:
        if row["symbol"] != symbol or row["timeframe"] != timeframe:
            continue
        bar_dt = parse_iso_utc(row["bar_time"])
        if start_utc <= bar_dt < end_utc:
            rows.append(row)
    rows.sort(key=lambda item: item["bar_time"])
    return rows


def close_on_expected_side(direction: str, close_value: Decimal, ib_edge: Decimal, expected: str) -> bool:
    if expected == "beyond":
        return close_value > ib_edge if direction == "up" else close_value < ib_edge
    return close_value <= ib_edge if direction == "up" else close_value >= ib_edge


def build_observation_row(
    candidate_row: Dict[str, str],
    post_cross_row: Dict[str, str],
    bars: List[Dict[str, str]],
    config: Dict[str, Dict[str, str]],
    family: str,
    expected: str,
) -> Dict[str, str]:
    session_id = candidate_row["session_id"]
    session_cfg = config[session_id]
    prior_date = candidate_row["session_local_date"]
    next_date = next_session_date(prior_date)
    open_utc = local_open_utc(next_date, candidate_row["session_timezone"], session_cfg["session_open_local_hhmm"])
    window_bars = build_window_bars(
        bars=bars,
        symbol=candidate_row["symbol"],
        timeframe=candidate_row["timeframe"],
        start_utc=open_utc,
        minutes=30,
    )
    ib_edge = Decimal(post_cross_row["ib_same_side_edge_value"])
    first_bar = window_bars[0] if window_bars else None

    if not window_bars:
        status = "missing_next_session_first_30m_data"
        first_bar_expected = ""
        all_expected = ""
        any_opposite = ""
        first_open = ""
        first_close = ""
    else:
        first_close_value = Decimal(first_bar["close"])
        first_bar_expected_bool = close_on_expected_side(candidate_row["cross_direction"], first_close_value, ib_edge, expected)
        all_expected_bool = all(
            close_on_expected_side(candidate_row["cross_direction"], Decimal(bar["close"]), ib_edge, expected)
            for bar in window_bars
        )
        any_opposite_bool = not all_expected_bool
        status = (
            "next_session_first_30m_all_closes_{0}_prior_ib".format(expected)
            if all_expected_bool
            else "next_session_first_30m_not_all_closes_{0}_prior_ib".format(expected)
        )
        first_bar_expected = "1" if first_bar_expected_bool else "0"
        all_expected = "1" if all_expected_bool else "0"
        any_opposite = "1" if any_opposite_bool else "0"
        first_open = first_bar["open"]
        first_close = first_bar["close"]

    return {
        "observation_id": "{0}|{1}".format(
            "IBORBCT" if expected == "beyond" else "IBORPBS",
            candidate_row["candidate_id"],
        ),
        "observation_family": family,
        "observation_level": "RELATION_P0",
        "observation_status": status,
        "source_candidate_id": candidate_row["candidate_id"],
        "source_post_cross_observation_id": candidate_row["source_observation_id"],
        "symbol": candidate_row["symbol"],
        "timeframe": candidate_row["timeframe"],
        "session_id": session_id,
        "session_timezone": candidate_row["session_timezone"],
        "prior_session_local_date": prior_date,
        "next_session_local_date": next_date,
        "cross_direction": candidate_row["cross_direction"],
        "cross_mode": candidate_row["cross_mode"],
        "prior_ib_same_side_edge_value": post_cross_row["ib_same_side_edge_value"],
        "next_session_open_utc": fmt_dt(open_utc),
        "next_session_first_bar_open": first_open,
        "next_session_first_bar_close": first_close,
        "next_session_first_30m_bar_count": str(len(window_bars)),
        "next_session_first_bar_expected_side": first_bar_expected,
        "next_session_first_30m_all_closes_expected_side": all_expected,
        "next_session_first_30m_any_close_opposite_or_at_boundary": any_opposite,
        "observation_scope": "next_same_session_first_30m_relative_to_prior_ib",
    }


def build_summary(
    scope: str,
    input_path: Path,
    post_cross_path: Path,
    bars_path: Path,
    output_path: Path,
    summary_path: Path,
    rows: List[Dict[str, str]],
) -> Dict[str, object]:
    by_session: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    status_counts: Dict[str, int] = defaultdict(int)
    for row in rows:
        session = row["session_id"]
        by_session[session]["rows"] += 1
        by_session[session]["status_" + row["observation_status"]] += 1
        status_counts[row["observation_status"]] += 1
    return {
        "producer": "n02_ib_or_beyond_continuation_and_not_beyond_stability_p0_build_v1.py",
        "scope": scope,
        "status": "fresh_run_next_session_first_30m_observation",
        "evidence_mode": "fresh_run_derived_from_session_close_candidates_and_next_session_bars",
        "source_path": {
            "input_candidates_csv": str(input_path),
            "post_cross_observation_csv": str(post_cross_path),
            "bars_csv": str(bars_path),
        },
        "repo_path": {
            "output_csv": str(output_path),
            "summary_json": str(summary_path),
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "boundary": {
            "defines_failed_breakout": False,
            "defines_retest_reject": False,
            "defines_day_type": False,
            "observation_scope_next_session_first_30m_only": True,
        },
        "rows": len(rows),
        "status_counts": dict(sorted(status_counts.items())),
        "by_session": {k: dict(v) for k, v in sorted(by_session.items())},
        "output_columns": OBSERVATION_COLUMNS,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--beyond-input", default=str(BEYOND_INPUT_PATH))
    parser.add_argument("--not-beyond-input", default=str(NOT_BEYOND_INPUT_PATH))
    parser.add_argument("--post-cross-input", default=str(POST_CROSS_INPUT_PATH))
    parser.add_argument("--bars-input", default=str(BARS_INPUT_PATH))
    parser.add_argument("--config-input", default=str(CONFIG_INPUT_PATH))
    parser.add_argument("--beyond-output", default=str(BEYOND_OUTPUT_PATH))
    parser.add_argument("--beyond-summary", default=str(BEYOND_SUMMARY_PATH))
    parser.add_argument("--not-beyond-output", default=str(NOT_BEYOND_OUTPUT_PATH))
    parser.add_argument("--not-beyond-summary", default=str(NOT_BEYOND_SUMMARY_PATH))
    args = parser.parse_args()

    beyond_input_path = Path(args.beyond_input)
    not_beyond_input_path = Path(args.not_beyond_input)
    post_cross_input_path = Path(args.post_cross_input)
    bars_input_path = Path(args.bars_input)
    config_input_path = Path(args.config_input)
    beyond_output_path = Path(args.beyond_output)
    beyond_summary_path = Path(args.beyond_summary)
    not_beyond_output_path = Path(args.not_beyond_output)
    not_beyond_summary_path = Path(args.not_beyond_summary)

    assert_header(beyond_input_path, SESSION_CLOSE_COLUMNS)
    assert_header(not_beyond_input_path, SESSION_CLOSE_COLUMNS)
    assert_header(post_cross_input_path, POST_CROSS_COLUMNS)
    assert_header(bars_input_path, BARS_COLUMNS)

    beyond_rows = read_rows(beyond_input_path)
    not_beyond_rows = read_rows(not_beyond_input_path)
    post_cross_rows = read_rows(post_cross_input_path)
    post_cross_index = {row["observation_id"]: row for row in post_cross_rows}
    bars = load_bars(bars_input_path)
    config = load_config(config_input_path)

    beyond_observations = sorted(
        [
            build_observation_row(
                candidate_row=row,
                post_cross_row=post_cross_index[row["source_observation_id"]],
                bars=bars,
                config=config,
                family="IB_OR_BEYOND_CONTINUATION_OBSERVATION",
                expected="beyond",
            )
            for row in beyond_rows
        ],
        key=sort_key,
    )
    not_beyond_observations = sorted(
        [
            build_observation_row(
                candidate_row=row,
                post_cross_row=post_cross_index[row["source_observation_id"]],
                bars=bars,
                config=config,
                family="IB_OR_NOT_BEYOND_PULLBACK_STABILITY_OBSERVATION",
                expected="inside",
            )
            for row in not_beyond_rows
        ],
        key=sort_key,
    )

    write_rows(beyond_output_path, OBSERVATION_COLUMNS, beyond_observations)
    write_rows(not_beyond_output_path, OBSERVATION_COLUMNS, not_beyond_observations)

    beyond_summary = build_summary(
        scope="REOPEN_B9_N02_IB_OR_BEYOND_CONTINUATION_P0",
        input_path=beyond_input_path,
        post_cross_path=post_cross_input_path,
        bars_path=bars_input_path,
        output_path=beyond_output_path,
        summary_path=beyond_summary_path,
        rows=beyond_observations,
    )
    beyond_summary_path.write_text(json.dumps(beyond_summary, ensure_ascii=True, indent=2), encoding="utf-8")

    not_beyond_summary = build_summary(
        scope="REOPEN_B9_N02_IB_OR_NOT_BEYOND_PULLBACK_STABILITY_P0",
        input_path=not_beyond_input_path,
        post_cross_path=post_cross_input_path,
        bars_path=bars_input_path,
        output_path=not_beyond_output_path,
        summary_path=not_beyond_summary_path,
        rows=not_beyond_observations,
    )
    not_beyond_summary_path.write_text(json.dumps(not_beyond_summary, ensure_ascii=True, indent=2), encoding="utf-8")

    print("beyond_output_path={0}".format(beyond_output_path))
    print("beyond_summary_path={0}".format(beyond_summary_path))
    print("not_beyond_output_path={0}".format(not_beyond_output_path))
    print("not_beyond_summary_path={0}".format(not_beyond_summary_path))
    print("beyond_rows={0}".format(len(beyond_observations)))
    print("beyond_status_counts={0}".format(json.dumps(beyond_summary["status_counts"], ensure_ascii=True)))
    print("not_beyond_rows={0}".format(len(not_beyond_observations)))
    print("not_beyond_status_counts={0}".format(json.dumps(not_beyond_summary["status_counts"], ensure_ascii=True)))


if __name__ == "__main__":
    main()
