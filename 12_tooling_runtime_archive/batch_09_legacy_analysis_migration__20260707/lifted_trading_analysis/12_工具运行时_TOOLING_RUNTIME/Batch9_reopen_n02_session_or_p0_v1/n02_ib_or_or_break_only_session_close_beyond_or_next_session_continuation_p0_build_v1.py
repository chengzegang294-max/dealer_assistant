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
INPUT_PATH = (
    RUNTIME_DIR / "n02_ib_or_or_break_only_session_close_beyond_or_candidates_p0_sample_gbpusd_m15_slice_v1.csv"
)
BARS_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "n02_real_input_gbpusd_m15_v1.csv"
CONFIG_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "n02_or_proof_config_v1.json"
OUTPUT_PATH = (
    RUNTIME_DIR
    / "n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_observation_p0_sample_gbpusd_m15_slice_v1.csv"
)
SUMMARY_PATH = (
    RUNTIME_DIR / "n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_p0_summary_gbpusd_m15_slice_v1.json"
)
CARD_PATH = (
    RUNTIME_DIR / "n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_card_gbpusd_m15_slice_v1.md"
)
CARD_SUMMARY_PATH = (
    RUNTIME_DIR
    / "n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_card_summary_gbpusd_m15_slice_v1.json"
)

INPUT_COLUMNS = [
    "candidate_id",
    "candidate_family",
    "candidate_level",
    "candidate_status",
    "source_candidate_id",
    "symbol",
    "timeframe",
    "session_id",
    "session_timezone",
    "session_local_date",
    "first_break_direction",
    "first_break_mode",
    "break_bar_time_utc",
    "break_trigger_price",
    "or_break_edge_value",
    "ib_same_side_edge_value",
    "same_side_gap_to_ib_before_break",
    "bars_after_break_count",
    "return_inside_or_observed_same_day",
    "first_return_inside_or_bar_time_utc",
    "max_extension_price_same_day",
    "max_extension_distance_over_or",
    "session_close_price",
    "session_close_beyond_or",
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
    "symbol",
    "timeframe",
    "session_id",
    "session_timezone",
    "prior_session_local_date",
    "next_session_local_date",
    "first_break_direction",
    "first_break_mode",
    "prior_or_break_edge_value",
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


def timeframe_minutes(timeframe: str) -> int:
    if timeframe.startswith("M"):
        return int(timeframe[1:])
    raise ValueError("unsupported timeframe: {0}".format(timeframe))


def expected_bar_count(window_minutes: int, timeframe: str) -> int:
    minutes = timeframe_minutes(timeframe)
    if minutes <= 0:
        raise ValueError("invalid timeframe minutes: {0}".format(timeframe))
    return window_minutes // minutes


def next_session_date(date_text: str) -> str:
    return (datetime.strptime(date_text, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")


def local_open_utc(local_date: str, session_timezone: str, open_hhmm: str) -> datetime:
    hour, minute = [int(part) for part in open_hhmm.split(":")]
    dt_local = datetime.strptime(local_date, "%Y-%m-%d").replace(
        hour=hour, minute=minute, tzinfo=ZoneInfo(session_timezone)
    )
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


def close_on_expected_side(direction: str, close_value: Decimal, or_edge: Decimal) -> bool:
    if direction == "up":
        return close_value > or_edge
    return close_value < or_edge


def sort_key(row: Dict[str, str]) -> Tuple[str, str, str, str]:
    return (
        row["next_session_local_date"],
        row["session_id"],
        row["symbol"],
        row["timeframe"],
    )


def build_observation_row(
    candidate_row: Dict[str, str],
    bars: List[Dict[str, str]],
    config: Dict[str, Dict[str, str]],
) -> Dict[str, str]:
    session_id = candidate_row["session_id"]
    session_cfg = config[session_id]
    prior_date = candidate_row["session_local_date"]
    next_date = next_session_date(prior_date)
    window_minutes = int(session_cfg["opening_range_window_minutes"])
    open_utc = local_open_utc(next_date, candidate_row["session_timezone"], session_cfg["session_open_local_hhmm"])
    window_bars = build_window_bars(
        bars=bars,
        symbol=candidate_row["symbol"],
        timeframe=candidate_row["timeframe"],
        start_utc=open_utc,
        minutes=window_minutes,
    )
    or_edge = Decimal(candidate_row["or_break_edge_value"])
    first_bar: Optional[Dict[str, str]] = window_bars[0] if window_bars else None

    if not window_bars:
        status = "missing_next_session_first_30m_data"
        first_bar_expected = ""
        all_expected = ""
        any_opposite = ""
        first_open = ""
        first_close = ""
    else:
        first_close_value = Decimal(first_bar["close"])
        first_bar_expected_bool = close_on_expected_side(
            candidate_row["first_break_direction"], first_close_value, or_edge
        )
        all_expected_bool = all(
            close_on_expected_side(candidate_row["first_break_direction"], Decimal(bar["close"]), or_edge)
            for bar in window_bars
        )
        status = (
            "next_session_first_30m_all_closes_beyond_prior_or"
            if all_expected_bool
            else "next_session_first_30m_not_all_closes_beyond_prior_or"
        )
        first_bar_expected = "1" if first_bar_expected_bool else "0"
        all_expected = "1" if all_expected_bool else "0"
        any_opposite = "0" if all_expected_bool else "1"
        first_open = first_bar["open"]
        first_close = first_bar["close"]

    return {
        "observation_id": "IBORONLYNXT|{0}".format(candidate_row["candidate_id"]),
        "observation_family": "IB_OR_BREAK_ONLY_BEYOND_OR_NEXT_SESSION_CONTINUATION_OBSERVATION",
        "observation_level": "RELATION_P0",
        "observation_status": status,
        "source_candidate_id": candidate_row["candidate_id"],
        "symbol": candidate_row["symbol"],
        "timeframe": candidate_row["timeframe"],
        "session_id": session_id,
        "session_timezone": candidate_row["session_timezone"],
        "prior_session_local_date": prior_date,
        "next_session_local_date": next_date,
        "first_break_direction": candidate_row["first_break_direction"],
        "first_break_mode": candidate_row["first_break_mode"],
        "prior_or_break_edge_value": candidate_row["or_break_edge_value"],
        "next_session_open_utc": fmt_dt(open_utc),
        "next_session_first_bar_open": first_open,
        "next_session_first_bar_close": first_close,
        "next_session_first_30m_bar_count": str(len(window_bars)),
        "next_session_first_bar_expected_side": first_bar_expected,
        "next_session_first_30m_all_closes_expected_side": all_expected,
        "next_session_first_30m_any_close_opposite_or_at_boundary": any_opposite,
        "observation_scope": "next_same_session_first_30m_relative_to_prior_or",
    }


def build_observation_summary(
    input_path: Path,
    bars_path: Path,
    output_path: Path,
    summary_path: Path,
    rows: List[Dict[str, str]],
) -> Dict[str, object]:
    by_session: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    status_counts: Dict[str, int] = defaultdict(int)
    for row in rows:
        session = row["session_id"]
        status = row["observation_status"]
        by_session[session]["rows"] += 1
        by_session[session]["status_" + status] += 1
        status_counts[status] += 1

    return {
        "producer": "n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_p0_build_v1.py",
        "scope": "REOPEN_B9_N02_IB_OR_BREAK_ONLY_SESSION_CLOSE_BEYOND_OR_NEXT_SESSION_CONTINUATION_P0",
        "status": "fresh_run_next_session_first_30m_observation",
        "evidence_mode": "fresh_run_derived_from_or_break_only_beyond_or_candidates_and_next_session_bars",
        "source_path": {
            "input_candidates_csv": str(input_path),
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


def build_card_summary(
    input_path: Path,
    card_path: Path,
    summary_path: Path,
    rows: List[Dict[str, str]],
    full_window_expected_count: int,
) -> Dict[str, object]:
    by_session: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    status_counts: Dict[str, int] = defaultdict(int)
    direction_counts: Dict[str, int] = defaultdict(int)
    mode_counts: Dict[str, int] = defaultdict(int)
    full_window_rows = 0
    first_bar_expected_rows = 0

    for row in rows:
        session = row["session_id"]
        status = row["observation_status"]
        direction = row["first_break_direction"]
        mode = row["first_break_mode"]
        by_session[session]["rows"] += 1
        by_session[session]["status_" + status] += 1
        status_counts[status] += 1
        direction_counts[direction] += 1
        mode_counts[mode] += 1
        if row["next_session_first_30m_bar_count"] == str(full_window_expected_count):
            full_window_rows += 1
        if row["next_session_first_bar_expected_side"] == "1":
            first_bar_expected_rows += 1

    return {
        "producer": "n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_p0_build_v1.py",
        "scope": "REOPEN_B9_N02_IB_OR_BREAK_ONLY_SESSION_CLOSE_BEYOND_OR_NEXT_SESSION_CONTINUATION_CARD_P0",
        "status": "fresh_run_branch_card_summary",
        "evidence_mode": "fresh_run_derived_from_or_break_only_beyond_or_next_session_first_30m_observation",
        "source_path": {
            "observation_csv": str(input_path),
        },
        "repo_path": {
            "card_md": str(card_path),
            "summary_json": str(summary_path),
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "boundary": {
            "defines_failed_breakout": False,
            "defines_retest_reject": False,
            "defines_day_type": False,
            "is_branch_card_only": True,
        },
        "rows": len(rows),
        "status_counts": dict(sorted(status_counts.items())),
        "direction_counts": dict(sorted(direction_counts.items())),
        "mode_counts": dict(sorted(mode_counts.items())),
        "next_session_first_30m_full_window_rows": full_window_rows,
        "next_session_first_bar_expected_side_rows": first_bar_expected_rows,
        "by_session": {k: dict(v) for k, v in sorted(by_session.items())},
    }


def render_card(summary: Dict[str, object]) -> str:
    rows = int(summary["rows"])
    status_counts = summary["status_counts"]
    all_closes_rows = int(status_counts.get("next_session_first_30m_all_closes_beyond_prior_or", 0))
    not_all_rows = int(status_counts.get("next_session_first_30m_not_all_closes_beyond_prior_or", 0))
    missing_rows = int(status_counts.get("missing_next_session_first_30m_data", 0))

    lines = [
        "# n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_card v1",
        "",
        "## 作用",
        "",
        "- 把 `or_break_only + session_close_beyond_or + next same-session first 30m continuation` 固定成独立说明卡。",
        "- 当前不表达：`failed breakout / retest / reject / day type`。",
        "",
        "## 2026-07-06 fresh-run",
        "",
        "- 总行数：`{0}`".format(summary["rows"]),
        "- status 分布：`{0}`".format(json.dumps(summary["status_counts"], ensure_ascii=True)),
        "- direction 分布：`{0}`".format(json.dumps(summary["direction_counts"], ensure_ascii=True)),
        "- mode 分布：`{0}`".format(json.dumps(summary["mode_counts"], ensure_ascii=True)),
        "- `next_session_first_30m_full_window_rows`：`{0}`".format(summary["next_session_first_30m_full_window_rows"]),
        "- `next_session_first_bar_expected_side_rows`：`{0}`".format(summary["next_session_first_bar_expected_side_rows"]),
        "",
        "## Session 分布",
        "",
    ]

    by_session = summary["by_session"]
    for session_id in sorted(by_session.keys()):
        lines.append("- `{0}`: `{1}`".format(session_id, json.dumps(by_session[session_id], ensure_ascii=True)))

    lines.extend(
        [
            "",
            "## 当前裁决",
            "",
            "- `session_close_beyond_or` 当前只说明：下一同类 session 首 30 分钟是否整体仍在前一日 `OR` 外侧同方向。",
            "- 当前 `{0}/{1}` 行满足持续外侧，`{2}/{1}` 行不满足，`{3}/{1}` 行缺下一同类 session 数据。".format(
                all_closes_rows,
                rows,
                not_all_rows,
                missing_rows,
            ),
            "- 后续若继续推进，应只从满足持续外侧的样本再拆 continuation persistence，不直接改名成 `failed breakout`。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(INPUT_PATH))
    parser.add_argument("--bars-input", default=str(BARS_INPUT_PATH))
    parser.add_argument("--config-input", default=str(CONFIG_INPUT_PATH))
    parser.add_argument("--output", default=str(OUTPUT_PATH))
    parser.add_argument("--summary-json", default=str(SUMMARY_PATH))
    parser.add_argument("--card-md", default=str(CARD_PATH))
    parser.add_argument("--card-summary-json", default=str(CARD_SUMMARY_PATH))
    args = parser.parse_args()

    input_path = Path(args.input)
    bars_input_path = Path(args.bars_input)
    config_input_path = Path(args.config_input)
    output_path = Path(args.output)
    summary_path = Path(args.summary_json)
    card_path = Path(args.card_md)
    card_summary_path = Path(args.card_summary_json)

    assert_header(input_path, INPUT_COLUMNS)
    assert_header(bars_input_path, BARS_COLUMNS)

    input_rows = read_rows(input_path)
    bars_rows = read_rows(bars_input_path)
    config = load_config(config_input_path)

    observation_rows = sorted(
        [build_observation_row(candidate_row=row, bars=bars_rows, config=config) for row in input_rows],
        key=sort_key,
    )
    write_rows(output_path, OBSERVATION_COLUMNS, observation_rows)

    observation_summary = build_observation_summary(
        input_path=input_path,
        bars_path=bars_input_path,
        output_path=output_path,
        summary_path=summary_path,
        rows=observation_rows,
    )
    summary_path.write_text(json.dumps(observation_summary, ensure_ascii=True, indent=2), encoding="utf-8")

    sample_session_id = input_rows[0]["session_id"] if input_rows else "london"
    sample_timeframe = input_rows[0]["timeframe"] if input_rows else "M15"
    full_window_expected_count = expected_bar_count(
        int(config[sample_session_id]["opening_range_window_minutes"]), sample_timeframe
    )
    card_summary = build_card_summary(
        input_path=output_path,
        card_path=card_path,
        summary_path=card_summary_path,
        rows=observation_rows,
        full_window_expected_count=full_window_expected_count,
    )
    card_summary_path.write_text(json.dumps(card_summary, ensure_ascii=True, indent=2), encoding="utf-8")
    card_path.write_text(render_card(card_summary), encoding="utf-8")

    print("output_csv={0}".format(output_path))
    print("summary_json={0}".format(summary_path))
    print("card_md={0}".format(card_path))
    print("card_summary_json={0}".format(card_summary_path))
    print("rows={0}".format(observation_summary["rows"]))
    print("status_counts={0}".format(json.dumps(observation_summary["status_counts"], ensure_ascii=True)))


if __name__ == "__main__":
    main()
