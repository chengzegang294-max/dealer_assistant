from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

RUNTIME_DIR = Path(__file__).parent
CONFIRMED_INPUT_PATH = RUNTIME_DIR / "n02_ib_or_confirmed_cross_candidates_p0_sample_v1.csv"
OUTCOME_SHELL_INPUT_PATH = RUNTIME_DIR / "n02_ib_or_confirmed_cross_outcome_shell_p0_sample_v1.csv"
OR_ONLY_INPUT_PATH = RUNTIME_DIR / "n02_ib_or_or_break_only_candidates_p0_sample_v1.csv"
BARS_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "n02_first_real_input_bars_v1.csv"
POST_CROSS_OUTPUT_PATH = RUNTIME_DIR / "n02_ib_or_post_cross_path_observation_p0_sample_v1.csv"
POST_CROSS_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_post_cross_path_observation_p0_summary_v1.json"
OR_ONLY_CARD_PATH = RUNTIME_DIR / "n02_ib_or_or_break_only_branch_card_v1.md"
OR_ONLY_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_or_break_only_branch_summary_v1.json"

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

BARS_COLUMNS = [
    "symbol",
    "timeframe",
    "bar_time",
    "open",
    "high",
    "low",
    "close",
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


@dataclass(frozen=True)
class Bar:
    symbol: str
    timeframe: str
    dt_utc: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal


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


def to_decimal(value: str) -> Optional[Decimal]:
    if value in ("", "na", "NA", None):
        return None
    try:
        return Decimal(value)
    except InvalidOperation:
        return None


def format_decimal(value: Optional[Decimal]) -> str:
    return "" if value is None else str(value)


def parse_iso_utc(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def read_bars(path: Path) -> List[Bar]:
    rows = read_rows(path)
    bars: List[Bar] = []
    for row in rows:
        bars.append(
            Bar(
                symbol=row["symbol"],
                timeframe=row["timeframe"],
                dt_utc=parse_iso_utc(row["bar_time"]),
                open=Decimal(row["open"]),
                high=Decimal(row["high"]),
                low=Decimal(row["low"]),
                close=Decimal(row["close"]),
            )
        )
    bars.sort(key=lambda item: item.dt_utc)
    return bars


def sort_key(row: Dict[str, str]) -> Tuple[str, str, str, str]:
    return (
        row.get("session_local_date", ""),
        row.get("session_id", ""),
        row.get("symbol", ""),
        row.get("timeframe", ""),
    )


def gap_bucket(gap_text: str) -> str:
    gap = to_decimal(gap_text)
    if gap is None:
        return "unknown"
    if gap < Decimal("0.00010"):
        return "lt_0.00010"
    if gap < Decimal("0.00050"):
        return "0.00010_to_0.00049"
    return "ge_0.00050"


def build_post_cross_observation(
    outcome_row: Dict[str, str],
    confirmed_row: Dict[str, str],
    bars_index: Dict[Tuple[str, str, str, str], List[Bar]],
) -> Dict[str, str]:
    symbol = outcome_row["symbol"]
    timeframe = outcome_row["timeframe"]
    session_id = outcome_row["session_id"]
    session_timezone = outcome_row["session_timezone"]
    session_local_date = outcome_row["session_local_date"]
    cross_direction = outcome_row["cross_direction"]
    cross_time = parse_iso_utc(outcome_row["cross_bar_time_utc"])
    cross_trigger_price = Decimal(outcome_row["cross_trigger_price"])
    ib_edge = Decimal(confirmed_row["ib_same_side_edge_value"])

    day_bars = bars_index.get((symbol, timeframe, session_id, session_local_date), [])
    future_bars = [bar for bar in day_bars if bar.dt_utc > cross_time]

    first_return_time = ""
    return_inside = False
    max_extension_price: Optional[Decimal] = None

    if cross_direction == "up":
        for bar in future_bars:
            if bar.low <= ib_edge and not return_inside:
                return_inside = True
                first_return_time = bar.dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
            if max_extension_price is None or bar.high > max_extension_price:
                max_extension_price = bar.high
        session_close_price = future_bars[-1].close if future_bars else cross_trigger_price
        session_close_beyond_ib = session_close_price > ib_edge
        extension_distance = (
            (max_extension_price - ib_edge) if max_extension_price is not None else (cross_trigger_price - ib_edge)
        )
    else:
        for bar in future_bars:
            if bar.high >= ib_edge and not return_inside:
                return_inside = True
                first_return_time = bar.dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
            if max_extension_price is None or bar.low < max_extension_price:
                max_extension_price = bar.low
        session_close_price = future_bars[-1].close if future_bars else cross_trigger_price
        session_close_beyond_ib = session_close_price < ib_edge
        extension_distance = (
            (ib_edge - max_extension_price) if max_extension_price is not None else (ib_edge - cross_trigger_price)
        )

    if not future_bars:
        observation_status = "no_future_bars_same_day"
    elif return_inside:
        observation_status = "return_inside_ib_observed_same_day"
    else:
        observation_status = "no_return_inside_ib_observed_same_day"

    return {
        "observation_id": "IBORPOST|{0}".format(outcome_row["outcome_shell_id"]),
        "observation_family": "IB_OR_POST_CROSS_PATH_OBSERVATION",
        "observation_level": "RELATION_P0",
        "observation_status": observation_status,
        "source_outcome_shell_id": outcome_row["outcome_shell_id"],
        "source_confirmed_candidate_id": outcome_row["source_confirmed_candidate_id"],
        "symbol": symbol,
        "timeframe": timeframe,
        "session_id": session_id,
        "session_timezone": session_timezone,
        "session_local_date": session_local_date,
        "cross_direction": cross_direction,
        "cross_mode": outcome_row["cross_mode"],
        "cross_bar_time_utc": outcome_row["cross_bar_time_utc"],
        "cross_trigger_price": outcome_row["cross_trigger_price"],
        "ib_same_side_edge_value": confirmed_row["ib_same_side_edge_value"],
        "bars_after_cross_count": str(len(future_bars)),
        "return_inside_ib_observed_same_day": "1" if return_inside else "0",
        "first_return_inside_ib_bar_time_utc": first_return_time,
        "max_extension_price_same_day": format_decimal(max_extension_price if max_extension_price is not None else cross_trigger_price),
        "max_extension_distance_over_ib": format_decimal(extension_distance),
        "session_close_price": format_decimal(session_close_price),
        "session_close_beyond_ib": "1" if session_close_beyond_ib else "0",
        "observation_scope": "same_local_date_after_confirmed_cross",
    }


def build_post_cross_summary(
    confirmed_input_path: Path,
    outcome_input_path: Path,
    bars_input_path: Path,
    output_csv_path: Path,
    summary_path: Path,
    rows: List[Dict[str, str]],
) -> Dict[str, object]:
    by_session: Dict[str, Dict[str, int]] = defaultdict(
        lambda: {
            "rows": 0,
            "return_inside_ib_rows": 0,
            "session_close_beyond_ib_rows": 0,
        }
    )
    return_rows = 0
    close_beyond_rows = 0
    for row in rows:
        session = row["session_id"]
        by_session[session]["rows"] += 1
        if row["return_inside_ib_observed_same_day"] == "1":
            by_session[session]["return_inside_ib_rows"] += 1
            return_rows += 1
        if row["session_close_beyond_ib"] == "1":
            by_session[session]["session_close_beyond_ib_rows"] += 1
            close_beyond_rows += 1

    return {
        "producer": "n02_ib_or_post_cross_path_and_or_break_only_card_p0_build_v1.py",
        "scope": "REOPEN_B9_N02_IB_OR_POST_CROSS_PATH_P0",
        "status": "fresh_run_post_cross_observation",
        "evidence_mode": "fresh_run_derived_from_outcome_shell_and_same_day_bars",
        "source_path": {
            "confirmed_cross_candidates_csv": str(confirmed_input_path),
            "confirmed_cross_outcome_shell_csv": str(outcome_input_path),
            "bars_csv": str(bars_input_path),
        },
        "repo_path": {
            "post_cross_observation_csv": str(output_csv_path),
            "summary_json": str(summary_path),
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "boundary": {
            "defines_failed_breakout": False,
            "defines_retest_reject": False,
            "defines_day_type": False,
            "observation_scope_same_day_only": True,
        },
        "rows": len(rows),
        "return_inside_ib_observed_same_day_rows": return_rows,
        "return_inside_ib_observed_same_day_ratio": return_rows / len(rows) if rows else 0.0,
        "session_close_beyond_ib_rows": close_beyond_rows,
        "session_close_beyond_ib_ratio": close_beyond_rows / len(rows) if rows else 0.0,
        "by_session": dict(sorted(by_session.items())),
        "output_columns": POST_CROSS_COLUMNS,
    }


def build_or_only_summary(
    input_path: Path,
    card_path: Path,
    summary_path: Path,
    rows: List[Dict[str, str]],
) -> Dict[str, object]:
    by_session: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    direction_counts: Dict[str, int] = defaultdict(int)
    mode_counts: Dict[str, int] = defaultdict(int)
    trigger_counts: Dict[str, int] = defaultdict(int)
    gap_bucket_counts: Dict[str, int] = defaultdict(int)

    for row in rows:
        session = row["session_id"]
        direction = row["first_break_direction"]
        mode = row["first_break_mode"]
        trigger = row["break_trigger_source"]
        bucket = gap_bucket(row["same_side_gap_to_ib_before_break"])
        by_session[session]["rows"] += 1
        by_session[session]["direction_" + direction] += 1
        by_session[session]["mode_" + mode] += 1
        direction_counts[direction] += 1
        mode_counts[mode] += 1
        trigger_counts[trigger] += 1
        gap_bucket_counts[bucket] += 1

    return {
        "producer": "n02_ib_or_post_cross_path_and_or_break_only_card_p0_build_v1.py",
        "scope": "REOPEN_B9_N02_IB_OR_BREAK_ONLY_CARD_P0",
        "status": "fresh_run_or_break_only_card_summary",
        "evidence_mode": "fresh_run_derived_from_or_break_only_candidates",
        "source_path": {
            "or_break_only_candidates_csv": str(input_path),
        },
        "repo_path": {
            "branch_card_md": str(card_path),
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
        "by_session": {k: dict(v) for k, v in sorted(by_session.items())},
        "direction_counts": dict(sorted(direction_counts.items())),
        "mode_counts": dict(sorted(mode_counts.items())),
        "trigger_source_counts": dict(sorted(trigger_counts.items())),
        "gap_bucket_counts": dict(sorted(gap_bucket_counts.items())),
    }


def render_or_only_card(summary: Dict[str, object]) -> str:
    lines = [
        "# n02_ib_or_or_break_only_branch_card v1",
        "",
        "## 作用",
        "",
        "- 把 `OR break only` 分支固定为独立说明卡。",
        "- 当前只表达：`OR` 已首破，但首破当根未穿过 `IB` 同侧边界。",
        "- 当前不表达：`failed breakout / retest / reject / day type`。",
        "",
        "## 2026-07-03 fresh-run",
        "",
        "- 总行数：`{0}`".format(summary["rows"]),
        "- 方向分布：`{0}`".format(json.dumps(summary["direction_counts"], ensure_ascii=True)),
        "- mode 分布：`{0}`".format(json.dumps(summary["mode_counts"], ensure_ascii=True)),
        "- trigger_source 分布：`{0}`".format(json.dumps(summary["trigger_source_counts"], ensure_ascii=True)),
        "- gap bucket 分布：`{0}`".format(json.dumps(summary["gap_bucket_counts"], ensure_ascii=True)),
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
            "- 这张卡只说明 `OR break only` 是一条独立分支。",
            "- 后续若继续推进，应优先补这条分支的稳定说明或结果观察，而不是把它并回 `confirmed cross`。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--confirmed-input", default=str(CONFIRMED_INPUT_PATH))
    parser.add_argument("--outcome-shell-input", default=str(OUTCOME_SHELL_INPUT_PATH))
    parser.add_argument("--or-only-input", default=str(OR_ONLY_INPUT_PATH))
    parser.add_argument("--bars-input", default=str(BARS_INPUT_PATH))
    parser.add_argument("--post-cross-output", default=str(POST_CROSS_OUTPUT_PATH))
    parser.add_argument("--post-cross-summary", default=str(POST_CROSS_SUMMARY_PATH))
    parser.add_argument("--or-only-card", default=str(OR_ONLY_CARD_PATH))
    parser.add_argument("--or-only-summary", default=str(OR_ONLY_SUMMARY_PATH))
    args = parser.parse_args()

    confirmed_input_path = Path(args.confirmed_input)
    outcome_input_path = Path(args.outcome_shell_input)
    or_only_input_path = Path(args.or_only_input)
    bars_input_path = Path(args.bars_input)
    post_cross_output_path = Path(args.post_cross_output)
    post_cross_summary_path = Path(args.post_cross_summary)
    or_only_card_path = Path(args.or_only_card)
    or_only_summary_path = Path(args.or_only_summary)

    assert_header(confirmed_input_path, CONFIRMED_COLUMNS)
    assert_header(outcome_input_path, OUTCOME_SHELL_COLUMNS)
    assert_header(or_only_input_path, OR_ONLY_COLUMNS)
    assert_header(bars_input_path, BARS_COLUMNS)

    confirmed_rows = read_rows(confirmed_input_path)
    outcome_rows = read_rows(outcome_input_path)
    or_only_rows = read_rows(or_only_input_path)
    bars = read_bars(bars_input_path)

    confirmed_index = {row["candidate_id"]: row for row in confirmed_rows}
    bars_index: Dict[Tuple[str, str, str, str], List[Bar]] = defaultdict(list)
    for bar in bars:
        for session_id, tz_name in (("london", "Europe/London"), ("new_york", "America/New_York")):
            local_date = bar.dt_utc.astimezone(ZoneInfo(tz_name)).strftime("%Y-%m-%d")
            bars_index[(bar.symbol, bar.timeframe, session_id, local_date)].append(bar)

    post_cross_rows = sorted(
        [
            build_post_cross_observation(
                outcome_row=row,
                confirmed_row=confirmed_index[row["source_confirmed_candidate_id"]],
                bars_index=bars_index,
            )
            for row in outcome_rows
        ],
        key=sort_key,
    )
    write_rows(post_cross_output_path, POST_CROSS_COLUMNS, post_cross_rows)
    post_cross_summary = build_post_cross_summary(
        confirmed_input_path=confirmed_input_path,
        outcome_input_path=outcome_input_path,
        bars_input_path=bars_input_path,
        output_csv_path=post_cross_output_path,
        summary_path=post_cross_summary_path,
        rows=post_cross_rows,
    )
    post_cross_summary_path.write_text(json.dumps(post_cross_summary, ensure_ascii=True, indent=2), encoding="utf-8")

    or_only_summary = build_or_only_summary(
        input_path=or_only_input_path,
        card_path=or_only_card_path,
        summary_path=or_only_summary_path,
        rows=or_only_rows,
    )
    or_only_summary_path.write_text(json.dumps(or_only_summary, ensure_ascii=True, indent=2), encoding="utf-8")
    or_only_card_path.write_text(render_or_only_card(or_only_summary), encoding="utf-8")

    print("confirmed_input_path={0}".format(confirmed_input_path))
    print("outcome_input_path={0}".format(outcome_input_path))
    print("or_only_input_path={0}".format(or_only_input_path))
    print("post_cross_output_path={0}".format(post_cross_output_path))
    print("post_cross_summary_path={0}".format(post_cross_summary_path))
    print("or_only_card_path={0}".format(or_only_card_path))
    print("or_only_summary_path={0}".format(or_only_summary_path))
    print("post_cross_rows={0}".format(len(post_cross_rows)))
    print("or_break_only_rows={0}".format(len(or_only_rows)))
    print(
        "post_cross_return_inside_ib_observed_same_day_rows={0}".format(
            post_cross_summary["return_inside_ib_observed_same_day_rows"]
        )
    )
    print(
        "post_cross_session_close_beyond_ib_rows={0}".format(
            post_cross_summary["session_close_beyond_ib_rows"]
        )
    )
    print("or_break_only_gap_bucket_counts={0}".format(json.dumps(or_only_summary["gap_bucket_counts"], ensure_ascii=True)))


if __name__ == "__main__":
    main()
