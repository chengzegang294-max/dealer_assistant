from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

RUNTIME_DIR = Path(__file__).parent
RELATIVE_INPUT_PATH = RUNTIME_DIR / "n02_ib_or_first_break_relative_p0_sample_v1.csv"
RELATION_INPUT_PATH = RUNTIME_DIR / "n02_ib_or_relation_p0_sample_v1.csv"
BARS_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "n02_first_real_input_bars_v1.csv"
CONFIG_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "n02_or_proof_config_v1.json"
OUTPUT_CSV_PATH = RUNTIME_DIR / "n02_ib_or_break_bar_evidence_p0_sample_v1.csv"
SUMMARY_JSON_PATH = RUNTIME_DIR / "n02_ib_or_break_bar_evidence_p0_summary_v1.json"

RELATIVE_INPUT_COLUMNS = [
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

RELATION_INPUT_COLUMNS = [
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

BARS_INPUT_COLUMNS = [
    "symbol",
    "timeframe",
    "bar_time",
    "open",
    "high",
    "low",
    "close",
]

OUTPUT_COLUMNS = [
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


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, rows: List[Dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


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


def parse_hhmm(value: str) -> Tuple[int, int]:
    parts = value.strip().split(":")
    if len(parts) != 2:
        raise ValueError("invalid hh:mm: {0}".format(value))
    return int(parts[0]), int(parts[1])


def read_bars(path: Path) -> List[Bar]:
    rows = read_csv_rows(path)
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


def build_break_bar_evidence(
    row: Dict[str, str],
    relation_row: Dict[str, str],
    bars_index: Dict[Tuple[str, str, str, str], List[Bar]],
    config: dict,
) -> Dict[str, str]:
    session_id = row["session_id"]
    symbol = row["symbol"]
    timeframe = row["timeframe"]
    session_timezone = row["session_timezone"]
    session_local_date = row["session_local_date"]
    upstream_direction = relation_row["first_break_direction"]
    upstream_mode = relation_row["first_break_mode"]
    session_cfg = config["sessions"][session_id]

    tz = ZoneInfo(session_timezone)
    open_h, open_m = parse_hhmm(str(session_cfg["session_open_local_hhmm"]))
    window_minutes = int(row["opening_range_window_minutes"])
    local_midnight = datetime.strptime(session_local_date, "%Y-%m-%d").replace(tzinfo=tz)
    or_start = local_midnight.replace(hour=open_h, minute=open_m, second=0, microsecond=0)
    or_end = or_start + timedelta(minutes=window_minutes)
    or_end_utc = or_end.astimezone(timezone.utc)

    day_bars = bars_index.get((symbol, timeframe, session_id, session_local_date), [])
    post_or_bars = [bar for bar in day_bars if bar.dt_utc >= or_end_utc]

    or_high = to_decimal(relation_row["opening_range_high"])
    or_low = to_decimal(relation_row["opening_range_low"])
    ib_high = to_decimal(relation_row["ib_high"])
    ib_low = to_decimal(relation_row["ib_low"])
    if or_high is None or or_low is None or ib_high is None or ib_low is None:
        raise ValueError("missing OR/IB values for row {0}".format(row["relative_id"]))

    if upstream_direction == "none" or upstream_mode == "none" or row["first_break_relative_case"] == "no_break":
        return {
            "evidence_id": "IBORB|{0}".format(row["relative_id"]),
            "evidence_family": "IB_OR_BREAK_BAR_EVIDENCE",
            "evidence_level": "RELATION_P0",
            "evidence_status": "no_break_in_upstream_relation",
            "source_relative_id": row["relative_id"],
            "symbol": symbol,
            "timeframe": timeframe,
            "session_id": session_id,
            "session_timezone": session_timezone,
            "session_local_date": session_local_date,
            "ib_window_minutes": row["ib_window_minutes"],
            "opening_range_window_minutes": row["opening_range_window_minutes"],
            "upstream_first_break_direction": upstream_direction,
            "upstream_first_break_mode": upstream_mode,
            "first_break_direction": "none",
            "first_break_mode": "none",
            "direction_mode_match_to_relation": "1",
            "break_bar_time_utc": "",
            "break_bar_open": "",
            "break_bar_high": "",
            "break_bar_low": "",
            "break_bar_close": "",
            "or_break_edge_value": "",
            "ib_same_side_edge_value": "",
            "break_trigger_price": "",
            "break_trigger_source": "",
            "same_side_gap_to_ib_before_break": "",
            "ib_same_side_cross_confirmed": "0",
            "ib_same_side_cross_direction": "none",
            "ib_same_side_cross_distance": "",
            "requires_break_price_for_ib_confirmation_before": row["requires_break_price_for_ib_confirmation"],
            "requires_break_price_for_ib_confirmation_after": row["requires_break_price_for_ib_confirmation"],
            "evidence_scope": "no_break_relation_level",
            "width_error_day": row["width_error_day"],
        }

    matched_bar: Optional[Bar] = None
    direction = "none"
    mode = "none"
    trigger_price: Optional[Decimal] = None
    trigger_source = ""
    for bar in post_or_bars:
        wick_up = bar.high > or_high
        wick_down = bar.low < or_low
        if wick_up and wick_down:
            direction = "none"
            mode = "ambiguous"
            matched_bar = bar
            trigger_price = None
            trigger_source = "ambiguous"
            break
        if bar.close > or_high and bar.low >= or_low:
            direction = "up"
            mode = "close"
            matched_bar = bar
            trigger_price = bar.close
            trigger_source = "close"
            break
        if bar.close < or_low and bar.high <= or_high:
            direction = "down"
            mode = "close"
            matched_bar = bar
            trigger_price = bar.close
            trigger_source = "close"
            break
        if bar.high > or_high and bar.low >= or_low:
            direction = "up"
            mode = "wick"
            matched_bar = bar
            trigger_price = bar.high
            trigger_source = "high"
            break
        if bar.low < or_low and bar.high <= or_high:
            direction = "down"
            mode = "wick"
            matched_bar = bar
            trigger_price = bar.low
            trigger_source = "low"
            break

    if matched_bar is None:
        raise ValueError("no matched break bar for row {0}".format(row["relative_id"]))

    if direction == "up":
        cross_confirmed = trigger_price is not None and trigger_price > ib_high
        cross_distance = (trigger_price - ib_high) if trigger_price is not None else None
        ib_edge = ib_high
        or_edge = or_high
    elif direction == "down":
        cross_confirmed = trigger_price is not None and trigger_price < ib_low
        cross_distance = (ib_low - trigger_price) if trigger_price is not None else None
        ib_edge = ib_low
        or_edge = or_low
    else:
        cross_confirmed = False
        cross_distance = None
        ib_edge = None
        or_edge = None

    direction_mode_match = direction == upstream_direction and mode == upstream_mode
    if direction == "none":
        evidence_status = "ambiguous_break_bar_detected"
    elif cross_confirmed:
        evidence_status = "ib_same_side_cross_confirmed"
    else:
        evidence_status = "or_break_bar_found_but_ib_same_side_not_crossed"
    return {
        "evidence_id": "IBORB|{0}".format(row["relative_id"]),
        "evidence_family": "IB_OR_BREAK_BAR_EVIDENCE",
        "evidence_level": "RELATION_P0",
        "evidence_status": evidence_status,
        "source_relative_id": row["relative_id"],
        "symbol": symbol,
        "timeframe": timeframe,
        "session_id": session_id,
        "session_timezone": session_timezone,
        "session_local_date": session_local_date,
        "ib_window_minutes": row["ib_window_minutes"],
        "opening_range_window_minutes": row["opening_range_window_minutes"],
        "upstream_first_break_direction": upstream_direction,
        "upstream_first_break_mode": upstream_mode,
        "first_break_direction": direction,
        "first_break_mode": mode,
        "direction_mode_match_to_relation": "1" if direction_mode_match else "0",
        "break_bar_time_utc": matched_bar.dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "break_bar_open": str(matched_bar.open),
        "break_bar_high": str(matched_bar.high),
        "break_bar_low": str(matched_bar.low),
        "break_bar_close": str(matched_bar.close),
        "or_break_edge_value": format_decimal(or_edge),
        "ib_same_side_edge_value": format_decimal(ib_edge),
        "break_trigger_price": format_decimal(trigger_price),
        "break_trigger_source": trigger_source,
        "same_side_gap_to_ib_before_break": format_decimal((ib_edge - or_edge) if direction == "up" else (or_edge - ib_edge) if direction == "down" else None),
        "ib_same_side_cross_confirmed": "1" if cross_confirmed else "0",
        "ib_same_side_cross_direction": direction,
        "ib_same_side_cross_distance": format_decimal(cross_distance),
        "requires_break_price_for_ib_confirmation_before": row["requires_break_price_for_ib_confirmation"],
        "requires_break_price_for_ib_confirmation_after": "0",
        "evidence_scope": "first_break_bar_level",
        "width_error_day": row["width_error_day"],
    }


def build_summary(
    relative_input_path: Path,
    relation_input_path: Path,
    bars_input_path: Path,
    output_csv_path: Path,
    summary_json_path: Path,
    input_rows: List[Dict[str, str]],
    output_rows: List[Dict[str, str]],
) -> Dict[str, object]:
    status_counts: Dict[str, int] = defaultdict(int)
    direction_counts: Dict[str, int] = defaultdict(int)
    mode_counts: Dict[str, int] = defaultdict(int)
    trigger_source_counts: Dict[str, int] = defaultdict(int)
    cross_distance_values: List[Decimal] = []
    by_session: Dict[str, Dict[str, object]] = defaultdict(
        lambda: {
            "rows": 0,
            "cross_confirmed_rows": 0,
            "not_crossed_rows": 0,
            "first_local_date": "",
            "last_local_date": "",
        }
    )

    for row in output_rows:
        status_counts[row["evidence_status"]] += 1
        direction_counts[row["first_break_direction"]] += 1
        mode_counts[row["first_break_mode"]] += 1
        trigger_source_counts[row["break_trigger_source"]] += 1
        distance = to_decimal(row["ib_same_side_cross_distance"])
        if distance is not None:
            cross_distance_values.append(distance)
        session_id = row["session_id"]
        stats = by_session[session_id]
        stats["rows"] = int(stats["rows"]) + 1
        if row["ib_same_side_cross_confirmed"] == "1":
            stats["cross_confirmed_rows"] = int(stats["cross_confirmed_rows"]) + 1
        else:
            stats["not_crossed_rows"] = int(stats["not_crossed_rows"]) + 1
        local_date = row["session_local_date"]
        if not stats["first_local_date"] or local_date < stats["first_local_date"]:
            stats["first_local_date"] = local_date
        if not stats["last_local_date"] or local_date > stats["last_local_date"]:
            stats["last_local_date"] = local_date

    summary_by_session: Dict[str, Dict[str, object]] = {}
    for session_id in sorted(by_session.keys()):
        stats = by_session[session_id]
        row_count = int(stats["rows"])
        confirmed_count = int(stats["cross_confirmed_rows"])
        summary_by_session[session_id] = {
            "rows": row_count,
            "cross_confirmed_rows": confirmed_count,
            "not_crossed_rows": int(stats["not_crossed_rows"]),
            "cross_confirmed_ratio": confirmed_count / row_count if row_count else 0.0,
            "first_local_date": stats["first_local_date"],
            "last_local_date": stats["last_local_date"],
        }

    cross_confirmed_rows = sum(1 for row in output_rows if row["ib_same_side_cross_confirmed"] == "1")
    not_crossed_rows = len(output_rows) - cross_confirmed_rows
    return {
        "producer": "n02_ib_or_break_bar_evidence_p0_build_v1.py",
        "scope": "REOPEN_B9_N02_IB_OR_BREAK_BAR_EVIDENCE_P0",
        "status": "fresh_run_break_bar_evidence_sample_summary",
        "evidence_mode": "fresh_run_derived_from_relation_sample_and_real_input_bars",
        "source_path": {
            "relative_sample_csv": str(relative_input_path),
            "relation_sample_csv": str(relation_input_path),
            "bars_csv": str(bars_input_path),
        },
        "repo_path": {
            "break_bar_evidence_sample_csv": str(output_csv_path),
            "summary_json": str(summary_json_path),
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "boundary": {
            "writes_to_n02_p0_runtime_csv": False,
            "writes_to_n02_ib_runtime_csv": False,
            "writes_to_ib_or_relation_csv": False,
            "writes_to_first_break_relative_csv": False,
            "includes_acceptance": False,
            "includes_failed_breakout": False,
            "includes_retest_reject": False,
            "includes_day_type": False,
        },
        "input_rows": len(input_rows),
        "output_rows_written": len(output_rows),
        "ib_same_side_cross_confirmed_rows": cross_confirmed_rows,
        "ib_same_side_not_crossed_rows": not_crossed_rows,
        "ib_same_side_cross_confirmed_ratio": cross_confirmed_rows / len(output_rows) if output_rows else 0.0,
        "evidence_status_counts": dict(sorted(status_counts.items())),
        "direction_mode_match_rows": sum(1 for row in output_rows if row["direction_mode_match_to_relation"] == "1"),
        "direction_mode_mismatch_rows": sum(1 for row in output_rows if row["direction_mode_match_to_relation"] != "1"),
        "first_break_direction_counts": dict(sorted(direction_counts.items())),
        "first_break_mode_counts": dict(sorted(mode_counts.items())),
        "break_trigger_source_counts": dict(sorted(trigger_source_counts.items())),
        "by_session": summary_by_session,
        "ib_same_side_cross_distance_stats": {
            "min": str(min(cross_distance_values)) if cross_distance_values else "",
            "max": str(max(cross_distance_values)) if cross_distance_values else "",
            "avg": str(sum(cross_distance_values) / len(cross_distance_values)) if cross_distance_values else "",
        },
        "output_columns": OUTPUT_COLUMNS,
    }


def write_summary(path: Path, summary: Dict[str, object]) -> None:
    path.write_text(json.dumps(summary, ensure_ascii=True, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(RELATIVE_INPUT_PATH))
    parser.add_argument("--relation-input", default=str(RELATION_INPUT_PATH))
    parser.add_argument("--bars", default=str(BARS_INPUT_PATH))
    parser.add_argument("--config", default=str(CONFIG_INPUT_PATH))
    parser.add_argument("--output-csv", default=str(OUTPUT_CSV_PATH))
    parser.add_argument("--summary-json", default=str(SUMMARY_JSON_PATH))
    args = parser.parse_args()

    relative_input_path = Path(args.input)
    relation_input_path = Path(args.relation_input)
    bars_input_path = Path(args.bars)
    config_input_path = Path(args.config)
    output_csv_path = Path(args.output_csv)
    summary_json_path = Path(args.summary_json)

    assert_header(relative_input_path, RELATIVE_INPUT_COLUMNS)
    assert_header(relation_input_path, RELATION_INPUT_COLUMNS)
    assert_header(bars_input_path, BARS_INPUT_COLUMNS)
    config = load_json(config_input_path)
    input_rows = read_csv_rows(relative_input_path)
    relation_rows = read_csv_rows(relation_input_path)
    relation_index = {row["relation_id"]: row for row in relation_rows}
    bars = read_bars(bars_input_path)

    bars_index: Dict[Tuple[str, str, str, str], List[Bar]] = defaultdict(list)
    for bar in bars:
        for session_id, session_cfg in config["sessions"].items():
            tz = ZoneInfo(str(session_cfg["session_timezone"]))
            local_date = bar.dt_utc.astimezone(tz).strftime("%Y-%m-%d")
            bars_index[(bar.symbol, bar.timeframe, session_id, local_date)].append(bar)

    output_rows = [
        build_break_bar_evidence(
            row=row,
            relation_row=relation_index[row["source_relation_id"]],
            bars_index=bars_index,
            config=config,
        )
        for row in input_rows
    ]
    output_rows.sort(key=lambda row: (row["session_local_date"], row["session_id"], row["symbol"], row["timeframe"]))
    write_rows(output_csv_path, output_rows)
    summary = build_summary(
        relative_input_path=relative_input_path,
        relation_input_path=relation_input_path,
        bars_input_path=bars_input_path,
        output_csv_path=output_csv_path,
        summary_json_path=summary_json_path,
        input_rows=input_rows,
        output_rows=output_rows,
    )
    write_summary(summary_json_path, summary)

    print("relative_input_path={0}".format(relative_input_path))
    print("relation_input_path={0}".format(relation_input_path))
    print("bars_input_path={0}".format(bars_input_path))
    print("config_input_path={0}".format(config_input_path))
    print("output_csv_path={0}".format(output_csv_path))
    print("summary_json_path={0}".format(summary_json_path))
    print("input_rows={0}".format(len(input_rows)))
    print("output_rows_written={0}".format(len(output_rows)))
    print("ib_same_side_cross_confirmed_rows={0}".format(summary["ib_same_side_cross_confirmed_rows"]))
    print("ib_same_side_not_crossed_rows={0}".format(summary["ib_same_side_not_crossed_rows"]))
    print("ib_same_side_cross_confirmed_ratio={0}".format(summary["ib_same_side_cross_confirmed_ratio"]))
    print("direction_mode_match_rows={0}".format(summary["direction_mode_match_rows"]))
    print("direction_mode_mismatch_rows={0}".format(summary["direction_mode_mismatch_rows"]))
    print(
        "evidence_status_counts={0}".format(
            json.dumps(summary["evidence_status_counts"], ensure_ascii=True)
        )
    )
    print(
        "break_trigger_source_counts={0}".format(
            json.dumps(summary["break_trigger_source_counts"], ensure_ascii=True)
        )
    )
    for session_id in sorted(summary["by_session"].keys()):
        stats = summary["by_session"][session_id]
        print(
            "session_id={0} rows={1} cross_confirmed_rows={2} not_crossed_rows={3}".format(
                session_id,
                stats["rows"],
                stats["cross_confirmed_rows"],
                stats["not_crossed_rows"],
            )
        )


if __name__ == "__main__":
    main()
