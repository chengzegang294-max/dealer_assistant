from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

RUNTIME_DIR = Path(__file__).parent
BEYOND_INPUT_PATH = RUNTIME_DIR / "n02_ib_or_session_close_beyond_ib_candidates_p0_sample_v1.csv"
NOT_BEYOND_INPUT_PATH = RUNTIME_DIR / "n02_ib_or_session_close_not_beyond_ib_candidates_p0_sample_v1.csv"
BEYOND_CARD_PATH = RUNTIME_DIR / "n02_ib_or_session_close_beyond_ib_card_v1.md"
BEYOND_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_session_close_beyond_ib_summary_v1.json"
NOT_BEYOND_CARD_PATH = RUNTIME_DIR / "n02_ib_or_session_close_not_beyond_pullback_card_v1.md"
NOT_BEYOND_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_session_close_not_beyond_pullback_summary_v1.json"

INPUT_COLUMNS = [
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


def assert_header(path: Path) -> None:
    with path.open("r", encoding="utf-8", newline="") as f:
        header = next(csv.reader(f))
    if header != INPUT_COLUMNS:
        raise ValueError("header mismatch: {0}".format(path))


def read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def bucket_extension(value: str) -> str:
    try:
        extension = float(value)
    except ValueError:
        return "unknown"
    if extension < 0.001:
        return "lt_0.001"
    if extension < 0.003:
        return "0.001_to_0.00299"
    return "ge_0.003"


def summarize(rows: List[Dict[str, str]], scope: str, input_path: Path, card_path: Path, summary_path: Path) -> Dict[str, object]:
    by_session: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    direction_counts: Dict[str, int] = defaultdict(int)
    mode_counts: Dict[str, int] = defaultdict(int)
    extension_bucket_counts: Dict[str, int] = defaultdict(int)
    for row in rows:
        session = row["session_id"]
        direction = row["cross_direction"]
        mode = row["cross_mode"]
        bucket = bucket_extension(row["max_extension_distance_over_ib"])
        by_session[session]["rows"] += 1
        by_session[session]["direction_" + direction] += 1
        by_session[session]["mode_" + mode] += 1
        direction_counts[direction] += 1
        mode_counts[mode] += 1
        extension_bucket_counts[bucket] += 1
    return {
        "producer": "n02_ib_or_session_close_beyond_and_not_beyond_cards_p0_build_v1.py",
        "scope": scope,
        "status": "fresh_run_branch_card_summary",
        "evidence_mode": "fresh_run_derived_from_session_close_split_candidates",
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
        "input_columns": INPUT_COLUMNS,
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
        "## 2026-07-03 fresh-run",
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
    parser.add_argument("--beyond-input", default=str(BEYOND_INPUT_PATH))
    parser.add_argument("--not-beyond-input", default=str(NOT_BEYOND_INPUT_PATH))
    parser.add_argument("--beyond-card", default=str(BEYOND_CARD_PATH))
    parser.add_argument("--beyond-summary", default=str(BEYOND_SUMMARY_PATH))
    parser.add_argument("--not-beyond-card", default=str(NOT_BEYOND_CARD_PATH))
    parser.add_argument("--not-beyond-summary", default=str(NOT_BEYOND_SUMMARY_PATH))
    args = parser.parse_args()

    beyond_input_path = Path(args.beyond_input)
    not_beyond_input_path = Path(args.not_beyond_input)
    beyond_card_path = Path(args.beyond_card)
    beyond_summary_path = Path(args.beyond_summary)
    not_beyond_card_path = Path(args.not_beyond_card)
    not_beyond_summary_path = Path(args.not_beyond_summary)

    assert_header(beyond_input_path)
    assert_header(not_beyond_input_path)
    beyond_rows = read_rows(beyond_input_path)
    not_beyond_rows = read_rows(not_beyond_input_path)

    beyond_summary = summarize(
        rows=beyond_rows,
        scope="REOPEN_B9_N02_IB_OR_SESSION_CLOSE_BEYOND_CARD_P0",
        input_path=beyond_input_path,
        card_path=beyond_card_path,
        summary_path=beyond_summary_path,
    )
    beyond_summary_path.write_text(json.dumps(beyond_summary, ensure_ascii=True, indent=2), encoding="utf-8")
    beyond_card_path.write_text(
        render_card(
            title="n02_ib_or_session_close_beyond_ib_card v1",
            purpose="把 `session_close_beyond_ib` 固定成独立说明卡。",
            summary=beyond_summary,
            conclusion_lines=[
                "`session_close_beyond_ib` 当前只说明：同日本地收盘仍位于 `IB` 边界外侧。",
                "后续若继续推进，应从这些样本再拆 continuation/persistence 观察，而不是直接改名成 `failed breakout`。",
            ],
        ),
        encoding="utf-8",
    )

    not_beyond_summary = summarize(
        rows=not_beyond_rows,
        scope="REOPEN_B9_N02_IB_OR_SESSION_CLOSE_NOT_BEYOND_PULLBACK_CARD_P0",
        input_path=not_beyond_input_path,
        card_path=not_beyond_card_path,
        summary_path=not_beyond_summary_path,
    )
    not_beyond_summary_path.write_text(json.dumps(not_beyond_summary, ensure_ascii=True, indent=2), encoding="utf-8")
    not_beyond_card_path.write_text(
        render_card(
            title="n02_ib_or_session_close_not_beyond_pullback_card v1",
            purpose="把 `session_close_not_beyond_ib` 固定成回落分支说明卡。",
            summary=not_beyond_summary,
            conclusion_lines=[
                "`session_close_not_beyond_ib` 当前只说明：同日本地收盘已回到 `IB` 边界内侧或边界处。",
                "后续若继续推进，应从这些样本再拆 pullback stability 观察，而不是直接改名成 `failed breakout`。",
            ],
        ),
        encoding="utf-8",
    )

    print("beyond_input_path={0}".format(beyond_input_path))
    print("not_beyond_input_path={0}".format(not_beyond_input_path))
    print("beyond_card_path={0}".format(beyond_card_path))
    print("beyond_summary_path={0}".format(beyond_summary_path))
    print("not_beyond_card_path={0}".format(not_beyond_card_path))
    print("not_beyond_summary_path={0}".format(not_beyond_summary_path))
    print("session_close_beyond_ib_rows={0}".format(len(beyond_rows)))
    print("session_close_not_beyond_ib_rows={0}".format(len(not_beyond_rows)))


if __name__ == "__main__":
    main()
