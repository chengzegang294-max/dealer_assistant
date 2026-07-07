from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

RUNTIME_DIR = Path(__file__).parent
INPUT_PATH = RUNTIME_DIR / "n02_ib_or_post_cross_path_observation_p0_sample_v1.csv"
RETURN_INSIDE_OUTPUT_PATH = RUNTIME_DIR / "n02_ib_or_return_inside_ib_same_day_candidates_p0_sample_v1.csv"
RETURN_INSIDE_CARD_PATH = RUNTIME_DIR / "n02_ib_or_return_inside_ib_same_day_card_v1.md"
RETURN_INSIDE_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_return_inside_ib_same_day_summary_v1.json"
SESSION_CLOSE_BEYOND_OUTPUT_PATH = RUNTIME_DIR / "n02_ib_or_session_close_beyond_ib_candidates_p0_sample_v1.csv"
SESSION_CLOSE_NOT_BEYOND_OUTPUT_PATH = RUNTIME_DIR / "n02_ib_or_session_close_not_beyond_ib_candidates_p0_sample_v1.csv"
SESSION_CLOSE_SPLIT_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_session_close_beyond_split_p0_summary_v1.json"

INPUT_COLUMNS = [
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

RETURN_INSIDE_COLUMNS = [
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
    "bars_after_cross_count",
    "max_extension_distance_over_ib",
    "session_close_price",
    "session_close_beyond_ib",
    "card_scope",
]

SESSION_CLOSE_SPLIT_COLUMNS = [
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


def sort_key(row: Dict[str, str]) -> tuple[str, str, str, str]:
    return (
        row.get("session_local_date", ""),
        row.get("session_id", ""),
        row.get("symbol", ""),
        row.get("timeframe", ""),
    )


def build_return_inside_row(row: Dict[str, str]) -> Dict[str, str]:
    return {
        "candidate_id": "IBORRET|{0}".format(row["observation_id"]),
        "candidate_family": "IB_OR_RETURN_INSIDE_IB_SAME_DAY",
        "candidate_level": "RELATION_P0",
        "candidate_status": "return_inside_ib_observed_same_day",
        "source_observation_id": row["observation_id"],
        "symbol": row["symbol"],
        "timeframe": row["timeframe"],
        "session_id": row["session_id"],
        "session_timezone": row["session_timezone"],
        "session_local_date": row["session_local_date"],
        "cross_direction": row["cross_direction"],
        "cross_mode": row["cross_mode"],
        "cross_bar_time_utc": row["cross_bar_time_utc"],
        "first_return_inside_ib_bar_time_utc": row["first_return_inside_ib_bar_time_utc"],
        "bars_after_cross_count": row["bars_after_cross_count"],
        "max_extension_distance_over_ib": row["max_extension_distance_over_ib"],
        "session_close_price": row["session_close_price"],
        "session_close_beyond_ib": row["session_close_beyond_ib"],
        "card_scope": "same_day_return_inside_observation_only",
    }


def build_session_close_row(row: Dict[str, str], status: str) -> Dict[str, str]:
    return {
        "candidate_id": "IBORSC|{0}".format(row["observation_id"]),
        "candidate_family": "IB_OR_SESSION_CLOSE_SPLIT",
        "candidate_level": "RELATION_P0",
        "candidate_status": status,
        "source_observation_id": row["observation_id"],
        "symbol": row["symbol"],
        "timeframe": row["timeframe"],
        "session_id": row["session_id"],
        "session_timezone": row["session_timezone"],
        "session_local_date": row["session_local_date"],
        "cross_direction": row["cross_direction"],
        "cross_mode": row["cross_mode"],
        "cross_bar_time_utc": row["cross_bar_time_utc"],
        "first_return_inside_ib_bar_time_utc": row["first_return_inside_ib_bar_time_utc"],
        "session_close_price": row["session_close_price"],
        "session_close_beyond_ib": row["session_close_beyond_ib"],
        "max_extension_distance_over_ib": row["max_extension_distance_over_ib"],
        "split_scope": "same_day_session_close_position_relative_to_ib",
    }


def build_return_inside_summary(
    input_path: Path,
    output_csv_path: Path,
    card_path: Path,
    summary_path: Path,
    rows: List[Dict[str, str]],
) -> Dict[str, object]:
    by_session: Dict[str, Dict[str, int]] = defaultdict(
        lambda: {
            "rows": 0,
            "session_close_beyond_ib_rows": 0,
            "session_close_not_beyond_ib_rows": 0,
        }
    )
    direction_counts: Dict[str, int] = defaultdict(int)
    mode_counts: Dict[str, int] = defaultdict(int)
    for row in rows:
        session = row["session_id"]
        by_session[session]["rows"] += 1
        if row["session_close_beyond_ib"] == "1":
            by_session[session]["session_close_beyond_ib_rows"] += 1
        else:
            by_session[session]["session_close_not_beyond_ib_rows"] += 1
        direction_counts[row["cross_direction"]] += 1
        mode_counts[row["cross_mode"]] += 1

    return {
        "producer": "n02_ib_or_return_inside_and_session_close_split_p0_build_v1.py",
        "scope": "REOPEN_B9_N02_IB_OR_RETURN_INSIDE_CARD_P0",
        "status": "fresh_run_return_inside_card_summary",
        "evidence_mode": "fresh_run_derived_from_post_cross_observation",
        "source_path": {
            "post_cross_observation_csv": str(input_path),
        },
        "repo_path": {
            "return_inside_candidates_csv": str(output_csv_path),
            "return_inside_card_md": str(card_path),
            "summary_json": str(summary_path),
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "boundary": {
            "defines_failed_breakout": False,
            "defines_retest_reject": False,
            "defines_day_type": False,
            "is_return_inside_card_only": True,
        },
        "rows": len(rows),
        "by_session": dict(sorted(by_session.items())),
        "direction_counts": dict(sorted(direction_counts.items())),
        "mode_counts": dict(sorted(mode_counts.items())),
        "session_close_beyond_ib_rows": sum(1 for row in rows if row["session_close_beyond_ib"] == "1"),
        "session_close_not_beyond_ib_rows": sum(1 for row in rows if row["session_close_beyond_ib"] != "1"),
        "output_columns": RETURN_INSIDE_COLUMNS,
    }


def build_session_close_summary(
    input_path: Path,
    beyond_path: Path,
    not_beyond_path: Path,
    summary_path: Path,
    beyond_rows: List[Dict[str, str]],
    not_beyond_rows: List[Dict[str, str]],
) -> Dict[str, object]:
    by_session: Dict[str, Dict[str, int]] = defaultdict(
        lambda: {
            "beyond_rows": 0,
            "not_beyond_rows": 0,
        }
    )
    for row in beyond_rows:
        by_session[row["session_id"]]["beyond_rows"] += 1
    for row in not_beyond_rows:
        by_session[row["session_id"]]["not_beyond_rows"] += 1

    direction_counts_beyond: Dict[str, int] = defaultdict(int)
    direction_counts_not_beyond: Dict[str, int] = defaultdict(int)
    for row in beyond_rows:
        direction_counts_beyond[row["cross_direction"]] += 1
    for row in not_beyond_rows:
        direction_counts_not_beyond[row["cross_direction"]] += 1

    return {
        "producer": "n02_ib_or_return_inside_and_session_close_split_p0_build_v1.py",
        "scope": "REOPEN_B9_N02_IB_OR_SESSION_CLOSE_BEYOND_SPLIT_P0",
        "status": "fresh_run_session_close_split_summary",
        "evidence_mode": "fresh_run_derived_from_post_cross_observation",
        "source_path": {
            "post_cross_observation_csv": str(input_path),
        },
        "repo_path": {
            "session_close_beyond_candidates_csv": str(beyond_path),
            "session_close_not_beyond_candidates_csv": str(not_beyond_path),
            "summary_json": str(summary_path),
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "boundary": {
            "defines_failed_breakout": False,
            "defines_retest_reject": False,
            "defines_day_type": False,
            "is_session_close_position_split_only": True,
        },
        "input_rows": len(beyond_rows) + len(not_beyond_rows),
        "session_close_beyond_ib_rows": len(beyond_rows),
        "session_close_not_beyond_ib_rows": len(not_beyond_rows),
        "session_close_beyond_ib_ratio": len(beyond_rows) / (len(beyond_rows) + len(not_beyond_rows))
        if (len(beyond_rows) + len(not_beyond_rows))
        else 0.0,
        "by_session": dict(sorted(by_session.items())),
        "direction_counts_beyond": dict(sorted(direction_counts_beyond.items())),
        "direction_counts_not_beyond": dict(sorted(direction_counts_not_beyond.items())),
        "output_columns": SESSION_CLOSE_SPLIT_COLUMNS,
    }


def render_return_inside_card(summary: Dict[str, object]) -> str:
    lines = [
        "# n02_ib_or_return_inside_ib_same_day_card v1",
        "",
        "## 作用",
        "",
        "- 把 `return_inside_ib_observed_same_day` 固定为独立说明卡。",
        "- 当前只表达：confirmed cross 之后，同日本地日内观察到价格回到 `IB` 边界内侧。",
        "- 当前不表达：`failed breakout / retest / reject / day type`。",
        "",
        "## 2026-07-03 fresh-run",
        "",
        "- 总行数：`{0}`".format(summary["rows"]),
        "- 方向分布：`{0}`".format(json.dumps(summary["direction_counts"], ensure_ascii=True)),
        "- mode 分布：`{0}`".format(json.dumps(summary["mode_counts"], ensure_ascii=True)),
        "- `session_close_beyond_ib_rows`：`{0}`".format(summary["session_close_beyond_ib_rows"]),
        "- `session_close_not_beyond_ib_rows`：`{0}`".format(summary["session_close_not_beyond_ib_rows"]),
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
            "- 这张卡只固定 `return_inside` 观测事实。",
            "- 后续若继续推进，应从 `session_close_beyond_ib` 的二次分桶或更细的 return-inside 说明继续展开。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(INPUT_PATH))
    parser.add_argument("--return-inside-output", default=str(RETURN_INSIDE_OUTPUT_PATH))
    parser.add_argument("--return-inside-card", default=str(RETURN_INSIDE_CARD_PATH))
    parser.add_argument("--return-inside-summary", default=str(RETURN_INSIDE_SUMMARY_PATH))
    parser.add_argument("--session-close-beyond-output", default=str(SESSION_CLOSE_BEYOND_OUTPUT_PATH))
    parser.add_argument("--session-close-not-beyond-output", default=str(SESSION_CLOSE_NOT_BEYOND_OUTPUT_PATH))
    parser.add_argument("--session-close-summary", default=str(SESSION_CLOSE_SPLIT_SUMMARY_PATH))
    args = parser.parse_args()

    input_path = Path(args.input)
    return_inside_output_path = Path(args.return_inside_output)
    return_inside_card_path = Path(args.return_inside_card)
    return_inside_summary_path = Path(args.return_inside_summary)
    session_close_beyond_output_path = Path(args.session_close_beyond_output)
    session_close_not_beyond_output_path = Path(args.session_close_not_beyond_output)
    session_close_summary_path = Path(args.session_close_summary)

    assert_header(input_path, INPUT_COLUMNS)
    input_rows = read_rows(input_path)

    return_inside_rows = sorted(
        [build_return_inside_row(row) for row in input_rows if row["return_inside_ib_observed_same_day"] == "1"],
        key=sort_key,
    )
    session_close_beyond_rows = sorted(
        [build_session_close_row(row, "session_close_beyond_ib") for row in input_rows if row["session_close_beyond_ib"] == "1"],
        key=sort_key,
    )
    session_close_not_beyond_rows = sorted(
        [build_session_close_row(row, "session_close_not_beyond_ib") for row in input_rows if row["session_close_beyond_ib"] != "1"],
        key=sort_key,
    )

    write_rows(return_inside_output_path, RETURN_INSIDE_COLUMNS, return_inside_rows)
    write_rows(session_close_beyond_output_path, SESSION_CLOSE_SPLIT_COLUMNS, session_close_beyond_rows)
    write_rows(session_close_not_beyond_output_path, SESSION_CLOSE_SPLIT_COLUMNS, session_close_not_beyond_rows)

    return_inside_summary = build_return_inside_summary(
        input_path=input_path,
        output_csv_path=return_inside_output_path,
        card_path=return_inside_card_path,
        summary_path=return_inside_summary_path,
        rows=return_inside_rows,
    )
    return_inside_summary_path.write_text(json.dumps(return_inside_summary, ensure_ascii=True, indent=2), encoding="utf-8")
    return_inside_card_path.write_text(render_return_inside_card(return_inside_summary), encoding="utf-8")

    session_close_summary = build_session_close_summary(
        input_path=input_path,
        beyond_path=session_close_beyond_output_path,
        not_beyond_path=session_close_not_beyond_output_path,
        summary_path=session_close_summary_path,
        beyond_rows=session_close_beyond_rows,
        not_beyond_rows=session_close_not_beyond_rows,
    )
    session_close_summary_path.write_text(json.dumps(session_close_summary, ensure_ascii=True, indent=2), encoding="utf-8")

    print("input_path={0}".format(input_path))
    print("return_inside_output_path={0}".format(return_inside_output_path))
    print("return_inside_card_path={0}".format(return_inside_card_path))
    print("return_inside_summary_path={0}".format(return_inside_summary_path))
    print("session_close_beyond_output_path={0}".format(session_close_beyond_output_path))
    print("session_close_not_beyond_output_path={0}".format(session_close_not_beyond_output_path))
    print("session_close_summary_path={0}".format(session_close_summary_path))
    print("return_inside_rows={0}".format(len(return_inside_rows)))
    print("session_close_beyond_ib_rows={0}".format(len(session_close_beyond_rows)))
    print("session_close_not_beyond_ib_rows={0}".format(len(session_close_not_beyond_rows)))
    print("session_close_beyond_ib_ratio={0}".format(session_close_summary["session_close_beyond_ib_ratio"]))


if __name__ == "__main__":
    main()
