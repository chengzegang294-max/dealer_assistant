from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

RUNTIME_DIR = Path(__file__).parent
INPUT_PATH = RUNTIME_DIR / "n02_ib_or_or_break_only_candidates_p0_sample_v1.csv"
BARS_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "n02_first_real_input_bars_v1.csv"
RETURN_INSIDE_OUTPUT_PATH = RUNTIME_DIR / "n02_ib_or_or_break_only_return_inside_or_same_day_candidates_p0_sample_v1.csv"
SESSION_CLOSE_BEYOND_OUTPUT_PATH = RUNTIME_DIR / "n02_ib_or_or_break_only_session_close_beyond_or_candidates_p0_sample_v1.csv"
SESSION_CLOSE_NOT_BEYOND_OUTPUT_PATH = RUNTIME_DIR / "n02_ib_or_or_break_only_session_close_not_beyond_or_candidates_p0_sample_v1.csv"
SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_or_break_only_same_day_session_close_split_p0_summary_v1.json"
BEYOND_CARD_PATH = RUNTIME_DIR / "n02_ib_or_or_break_only_session_close_beyond_or_card_v1.md"
BEYOND_CARD_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_or_break_only_session_close_beyond_or_summary_v1.json"
NOT_BEYOND_CARD_PATH = RUNTIME_DIR / "n02_ib_or_or_break_only_session_close_not_beyond_or_card_v1.md"
NOT_BEYOND_CARD_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_or_break_only_session_close_not_beyond_or_summary_v1.json"

INPUT_COLUMNS = [
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

OUTPUT_COLUMNS = [
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


def parse_iso_utc(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def format_decimal(value: Optional[Decimal]) -> str:
    return "" if value is None else str(value)


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


def bucket_extension(value: str) -> str:
    try:
        extension = float(value)
    except ValueError:
        return "unknown"
    if extension < 0.00010:
        return "lt_0.00010"
    if extension < 0.00050:
        return "0.00010_to_0.00049"
    return "ge_0.00050"


def build_observation(
    row: Dict[str, str],
    bars_index: Dict[Tuple[str, str, str, str], List[Bar]],
) -> Dict[str, str]:
    symbol = row["symbol"]
    timeframe = row["timeframe"]
    session_id = row["session_id"]
    session_local_date = row["session_local_date"]
    direction = row["first_break_direction"]
    break_time = parse_iso_utc(row["break_bar_time_utc"])
    break_trigger_price = Decimal(row["break_trigger_price"])
    or_edge = Decimal(row["or_break_edge_value"])

    day_bars = bars_index.get((symbol, timeframe, session_id, session_local_date), [])
    future_bars = [bar for bar in day_bars if bar.dt_utc > break_time]

    return_inside = False
    first_return_time = ""
    max_extension_price: Optional[Decimal] = None

    if direction == "up":
        for bar in future_bars:
            if bar.low <= or_edge and not return_inside:
                return_inside = True
                first_return_time = bar.dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
            if max_extension_price is None or bar.high > max_extension_price:
                max_extension_price = bar.high
        session_close_price = future_bars[-1].close if future_bars else break_trigger_price
        session_close_beyond_or = session_close_price > or_edge
        extension_distance = (
            (max_extension_price - or_edge) if max_extension_price is not None else (break_trigger_price - or_edge)
        )
    else:
        for bar in future_bars:
            if bar.high >= or_edge and not return_inside:
                return_inside = True
                first_return_time = bar.dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
            if max_extension_price is None or bar.low < max_extension_price:
                max_extension_price = bar.low
        session_close_price = future_bars[-1].close if future_bars else break_trigger_price
        session_close_beyond_or = session_close_price < or_edge
        extension_distance = (
            (or_edge - max_extension_price) if max_extension_price is not None else (or_edge - break_trigger_price)
        )

    return {
        "candidate_id": "IBORONLYSC|{0}".format(row["candidate_id"]),
        "candidate_family": "IB_OR_BREAK_ONLY_SAME_DAY_SESSION_CLOSE",
        "candidate_level": "RELATION_P0",
        "candidate_status": "or_break_only_same_day_session_close_observed",
        "source_candidate_id": row["candidate_id"],
        "symbol": symbol,
        "timeframe": timeframe,
        "session_id": session_id,
        "session_timezone": row["session_timezone"],
        "session_local_date": session_local_date,
        "first_break_direction": direction,
        "first_break_mode": row["first_break_mode"],
        "break_bar_time_utc": row["break_bar_time_utc"],
        "break_trigger_price": row["break_trigger_price"],
        "or_break_edge_value": row["or_break_edge_value"],
        "ib_same_side_edge_value": row["ib_same_side_edge_value"],
        "same_side_gap_to_ib_before_break": row["same_side_gap_to_ib_before_break"],
        "bars_after_break_count": str(len(future_bars)),
        "return_inside_or_observed_same_day": "1" if return_inside else "0",
        "first_return_inside_or_bar_time_utc": first_return_time,
        "max_extension_price_same_day": format_decimal(max_extension_price if max_extension_price is not None else break_trigger_price),
        "max_extension_distance_over_or": format_decimal(extension_distance),
        "session_close_price": format_decimal(session_close_price),
        "session_close_beyond_or": "1" if session_close_beyond_or else "0",
        "observation_scope": "same_local_date_after_or_break_only",
    }


def summarize_rows(
    rows: List[Dict[str, str]],
    scope: str,
    input_path: Path,
    card_path: Path,
    summary_path: Path,
) -> Dict[str, object]:
    by_session: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    direction_counts: Dict[str, int] = defaultdict(int)
    mode_counts: Dict[str, int] = defaultdict(int)
    extension_bucket_counts: Dict[str, int] = defaultdict(int)

    for row in rows:
        session = row["session_id"]
        direction = row["first_break_direction"]
        mode = row["first_break_mode"]
        bucket = bucket_extension(row["max_extension_distance_over_or"])
        by_session[session]["rows"] += 1
        by_session[session]["direction_" + direction] += 1
        by_session[session]["mode_" + mode] += 1
        direction_counts[direction] += 1
        mode_counts[mode] += 1
        extension_bucket_counts[bucket] += 1

    return {
        "producer": "n02_ib_or_or_break_only_same_day_session_close_split_p0_build_v1.py",
        "scope": scope,
        "status": "fresh_run_branch_card_summary",
        "evidence_mode": "fresh_run_derived_from_or_break_only_same_day_session_close_candidates",
        "source_path": {
            "input_csv": str(input_path),
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
        "by_session": {k: dict(v) for k, v in sorted(by_session.items())},
        "direction_counts": dict(sorted(direction_counts.items())),
        "mode_counts": dict(sorted(mode_counts.items())),
        "extension_bucket_counts": dict(sorted(extension_bucket_counts.items())),
        "input_columns": OUTPUT_COLUMNS,
    }


def build_split_summary(
    input_path: Path,
    bars_input_path: Path,
    return_inside_output_path: Path,
    beyond_output_path: Path,
    not_beyond_output_path: Path,
    summary_path: Path,
    rows: List[Dict[str, str]],
) -> Dict[str, object]:
    by_session: Dict[str, Dict[str, int]] = defaultdict(
        lambda: {
            "rows": 0,
            "return_inside_or_rows": 0,
            "session_close_beyond_or_rows": 0,
            "session_close_not_beyond_or_rows": 0,
        }
    )
    return_inside_rows = 0
    session_close_beyond_rows = 0
    session_close_not_beyond_rows = 0
    for row in rows:
        session = row["session_id"]
        by_session[session]["rows"] += 1
        if row["return_inside_or_observed_same_day"] == "1":
            by_session[session]["return_inside_or_rows"] += 1
            return_inside_rows += 1
        if row["session_close_beyond_or"] == "1":
            by_session[session]["session_close_beyond_or_rows"] += 1
            session_close_beyond_rows += 1
        else:
            by_session[session]["session_close_not_beyond_or_rows"] += 1
            session_close_not_beyond_rows += 1

    return {
        "producer": "n02_ib_or_or_break_only_same_day_session_close_split_p0_build_v1.py",
        "scope": "REOPEN_B9_N02_IB_OR_BREAK_ONLY_SAME_DAY_SESSION_CLOSE_SPLIT_P0",
        "status": "fresh_run_or_break_only_same_day_session_close_split",
        "evidence_mode": "fresh_run_derived_from_or_break_only_candidates_and_same_day_bars",
        "source_path": {
            "or_break_only_candidates_csv": str(input_path),
            "bars_csv": str(bars_input_path),
        },
        "repo_path": {
            "return_inside_or_candidates_csv": str(return_inside_output_path),
            "session_close_beyond_or_candidates_csv": str(beyond_output_path),
            "session_close_not_beyond_or_candidates_csv": str(not_beyond_output_path),
            "summary_json": str(summary_path),
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "boundary": {
            "defines_failed_breakout": False,
            "defines_retest_reject": False,
            "defines_day_type": False,
            "same_day_only": True,
        },
        "rows": len(rows),
        "return_inside_or_observed_same_day_rows": return_inside_rows,
        "return_inside_or_observed_same_day_ratio": return_inside_rows / len(rows) if rows else 0.0,
        "session_close_beyond_or_rows": session_close_beyond_rows,
        "session_close_beyond_or_ratio": session_close_beyond_rows / len(rows) if rows else 0.0,
        "session_close_not_beyond_or_rows": session_close_not_beyond_rows,
        "session_close_not_beyond_or_ratio": session_close_not_beyond_rows / len(rows) if rows else 0.0,
        "by_session": dict(sorted(by_session.items())),
        "output_columns": OUTPUT_COLUMNS,
    }


def render_card(title: str, purpose: str, summary: Dict[str, object], conclusion_lines: List[str]) -> str:
    lines = [
        "# {0}".format(title),
        "",
        "## 作用",
        "",
        "- {0}".format(purpose),
        "- 当前不表达：`failed breakout / retest / reject / day type`。",
        "",
        "## 2026-07-06 fresh-run",
        "",
        "- 总行数：`{0}`".format(summary["rows"]),
        "- 方向分布：`{0}`".format(json.dumps(summary["direction_counts"], ensure_ascii=True)),
        "- mode 分布：`{0}`".format(json.dumps(summary["mode_counts"], ensure_ascii=True)),
        "- extension bucket 分布：`{0}`".format(json.dumps(summary["extension_bucket_counts"], ensure_ascii=True)),
        "",
        "## Session 分布",
        "",
    ]
    by_session = summary["by_session"]
    for session_id in sorted(by_session.keys()):
        lines.append("- `{0}`: `{1}`".format(session_id, json.dumps(by_session[session_id], ensure_ascii=True)))
    lines.extend(["", "## 当前裁决", ""])
    for line in conclusion_lines:
        lines.append("- {0}".format(line))
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(INPUT_PATH))
    parser.add_argument("--bars-input", default=str(BARS_INPUT_PATH))
    parser.add_argument("--return-inside-output", default=str(RETURN_INSIDE_OUTPUT_PATH))
    parser.add_argument("--session-close-beyond-output", default=str(SESSION_CLOSE_BEYOND_OUTPUT_PATH))
    parser.add_argument("--session-close-not-beyond-output", default=str(SESSION_CLOSE_NOT_BEYOND_OUTPUT_PATH))
    parser.add_argument("--summary-json", default=str(SUMMARY_PATH))
    parser.add_argument("--beyond-card", default=str(BEYOND_CARD_PATH))
    parser.add_argument("--beyond-summary", default=str(BEYOND_CARD_SUMMARY_PATH))
    parser.add_argument("--not-beyond-card", default=str(NOT_BEYOND_CARD_PATH))
    parser.add_argument("--not-beyond-summary", default=str(NOT_BEYOND_CARD_SUMMARY_PATH))
    args = parser.parse_args()

    input_path = Path(args.input)
    bars_input_path = Path(args.bars_input)
    return_inside_output_path = Path(args.return_inside_output)
    beyond_output_path = Path(args.session_close_beyond_output)
    not_beyond_output_path = Path(args.session_close_not_beyond_output)
    summary_path = Path(args.summary_json)
    beyond_card_path = Path(args.beyond_card)
    beyond_summary_path = Path(args.beyond_summary)
    not_beyond_card_path = Path(args.not_beyond_card)
    not_beyond_summary_path = Path(args.not_beyond_summary)

    assert_header(input_path, INPUT_COLUMNS)
    assert_header(bars_input_path, BARS_COLUMNS)

    input_rows = read_rows(input_path)
    bars = read_bars(bars_input_path)

    bars_index: Dict[Tuple[str, str, str, str], List[Bar]] = defaultdict(list)
    for bar in bars:
        for session_id, tz_name in (("london", "Europe/London"), ("new_york", "America/New_York")):
            local_date = bar.dt_utc.astimezone(ZoneInfo(tz_name)).strftime("%Y-%m-%d")
            bars_index[(bar.symbol, bar.timeframe, session_id, local_date)].append(bar)

    observation_rows = sorted(
        [build_observation(row=row, bars_index=bars_index) for row in input_rows],
        key=sort_key,
    )
    return_inside_rows = [row for row in observation_rows if row["return_inside_or_observed_same_day"] == "1"]
    beyond_rows = [row for row in observation_rows if row["session_close_beyond_or"] == "1"]
    not_beyond_rows = [row for row in observation_rows if row["session_close_beyond_or"] != "1"]

    write_rows(return_inside_output_path, OUTPUT_COLUMNS, return_inside_rows)
    write_rows(beyond_output_path, OUTPUT_COLUMNS, beyond_rows)
    write_rows(not_beyond_output_path, OUTPUT_COLUMNS, not_beyond_rows)

    summary = build_split_summary(
        input_path=input_path,
        bars_input_path=bars_input_path,
        return_inside_output_path=return_inside_output_path,
        beyond_output_path=beyond_output_path,
        not_beyond_output_path=not_beyond_output_path,
        summary_path=summary_path,
        rows=observation_rows,
    )
    summary_path.write_text(json.dumps(summary, ensure_ascii=True, indent=2), encoding="utf-8")

    beyond_summary = summarize_rows(
        rows=beyond_rows,
        scope="REOPEN_B9_N02_IB_OR_BREAK_ONLY_SESSION_CLOSE_BEYOND_OR_CARD_P0",
        input_path=beyond_output_path,
        card_path=beyond_card_path,
        summary_path=beyond_summary_path,
    )
    beyond_summary_path.write_text(json.dumps(beyond_summary, ensure_ascii=True, indent=2), encoding="utf-8")
    beyond_card_path.write_text(
        render_card(
            title="n02_ib_or_or_break_only_session_close_beyond_or_card v1",
            purpose="把 `OR break only + session_close_beyond_or` 固定成独立说明卡。",
            summary=beyond_summary,
            conclusion_lines=[
                "`session_close_beyond_or` 当前只说明：同日本地收盘仍位于 `OR` 首破同侧外侧。",
                "后续若继续推进，应从这些样本再拆 same-side continuation / persistence，而不是直接改名成 `failed breakout`。",
            ],
        ),
        encoding="utf-8",
    )

    not_beyond_summary = summarize_rows(
        rows=not_beyond_rows,
        scope="REOPEN_B9_N02_IB_OR_BREAK_ONLY_SESSION_CLOSE_NOT_BEYOND_OR_CARD_P0",
        input_path=not_beyond_output_path,
        card_path=not_beyond_card_path,
        summary_path=not_beyond_summary_path,
    )
    not_beyond_summary_path.write_text(json.dumps(not_beyond_summary, ensure_ascii=True, indent=2), encoding="utf-8")
    not_beyond_card_path.write_text(
        render_card(
            title="n02_ib_or_or_break_only_session_close_not_beyond_or_card v1",
            purpose="把 `OR break only + session_close_not_beyond_or` 固定成回落说明卡。",
            summary=not_beyond_summary,
            conclusion_lines=[
                "`session_close_not_beyond_or` 当前只说明：同日本地收盘已回到 `OR` 内侧或边界。",
                "后续若继续推进，应从这些样本再拆 same-day pullback stability，而不是直接改名成 `failed breakout`。",
            ],
        ),
        encoding="utf-8",
    )

    print("input_path={0}".format(input_path))
    print("bars_input_path={0}".format(bars_input_path))
    print("return_inside_output_path={0}".format(return_inside_output_path))
    print("session_close_beyond_output_path={0}".format(beyond_output_path))
    print("session_close_not_beyond_output_path={0}".format(not_beyond_output_path))
    print("summary_path={0}".format(summary_path))
    print("beyond_card_path={0}".format(beyond_card_path))
    print("beyond_summary_path={0}".format(beyond_summary_path))
    print("not_beyond_card_path={0}".format(not_beyond_card_path))
    print("not_beyond_summary_path={0}".format(not_beyond_summary_path))
    print("rows={0}".format(summary["rows"]))
    print("return_inside_or_observed_same_day_rows={0}".format(summary["return_inside_or_observed_same_day_rows"]))
    print("session_close_beyond_or_rows={0}".format(summary["session_close_beyond_or_rows"]))
    print("session_close_not_beyond_or_rows={0}".format(summary["session_close_not_beyond_or_rows"]))


if __name__ == "__main__":
    main()
