from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

RUNTIME_DIR = Path(__file__).parent
BEYOND_INPUT_PATH = RUNTIME_DIR / "n02_ib_or_beyond_continuation_observation_p0_sample_v1.csv"
NOT_BEYOND_INPUT_PATH = RUNTIME_DIR / "n02_ib_or_not_beyond_pullback_stability_observation_p0_sample_v1.csv"
BEYOND_CARD_PATH = RUNTIME_DIR / "n02_ib_or_beyond_continuation_card_v1.md"
BEYOND_CARD_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_beyond_continuation_card_summary_v1.json"
NOT_BEYOND_CARD_PATH = RUNTIME_DIR / "n02_ib_or_not_beyond_stability_card_v1.md"
NOT_BEYOND_CARD_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_not_beyond_stability_card_summary_v1.json"

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


def assert_header(path: Path) -> None:
    with path.open("r", encoding="utf-8", newline="") as f:
        header = next(csv.reader(f))
    if header != OBSERVATION_COLUMNS:
        raise ValueError("header mismatch: {0}".format(path))


def read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def summarize_rows(
    rows: List[Dict[str, str]],
    scope: str,
    input_path: Path,
    card_path: Path,
    summary_path: Path,
) -> Dict[str, object]:
    by_session: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    status_counts: Dict[str, int] = defaultdict(int)
    direction_counts: Dict[str, int] = defaultdict(int)
    mode_counts: Dict[str, int] = defaultdict(int)
    bar_count_30_rows = 0
    first_bar_expected_rows = 0

    for row in rows:
        session_id = row["session_id"]
        status = row["observation_status"]
        direction = row["cross_direction"]
        mode = row["cross_mode"]
        by_session[session_id]["rows"] += 1
        by_session[session_id]["status_" + status] += 1
        status_counts[status] += 1
        direction_counts[direction] += 1
        mode_counts[mode] += 1
        if row["next_session_first_30m_bar_count"] == "30":
            bar_count_30_rows += 1
        if row["next_session_first_bar_expected_side"] == "1":
            first_bar_expected_rows += 1

    return {
        "producer": "n02_ib_or_beyond_continuation_and_not_beyond_stability_cards_p0_build_v1.py",
        "scope": scope,
        "status": "fresh_run_branch_card_summary",
        "evidence_mode": "fresh_run_derived_from_next_session_first_30m_observation",
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
        "next_session_first_30m_bar_count_30_rows": bar_count_30_rows,
        "next_session_first_bar_expected_side_rows": first_bar_expected_rows,
        "by_session": {k: dict(v) for k, v in sorted(by_session.items())},
    }


def render_card(
    title: str,
    purpose_line: str,
    summary: Dict[str, object],
    decision_lines: List[str],
) -> str:
    lines = [
        "# {0}".format(title),
        "",
        "## 作用",
        "",
        "- {0}".format(purpose_line),
        "- 当前不表达：`failed breakout / retest / reject / day type`。",
        "",
        "## 2026-07-03 fresh-run",
        "",
        "- 总行数：`{0}`".format(summary["rows"]),
        "- status 分布：`{0}`".format(json.dumps(summary["status_counts"], ensure_ascii=True)),
        "- direction 分布：`{0}`".format(json.dumps(summary["direction_counts"], ensure_ascii=True)),
        "- mode 分布：`{0}`".format(json.dumps(summary["mode_counts"], ensure_ascii=True)),
        "- `next_session_first_30m_bar_count_30_rows`：`{0}`".format(summary["next_session_first_30m_bar_count_30_rows"]),
        "- `next_session_first_bar_expected_side_rows`：`{0}`".format(summary["next_session_first_bar_expected_side_rows"]),
        "",
        "## Session 分布",
        "",
    ]
    by_session = summary["by_session"]
    for session_id in sorted(by_session.keys()):
        lines.append("- `{0}`: `{1}`".format(session_id, json.dumps(by_session[session_id], ensure_ascii=True)))
    lines.extend(["", "## 当前裁决", ""])
    for line in decision_lines:
        lines.append("- {0}".format(line))
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--beyond-input", default=str(BEYOND_INPUT_PATH))
    parser.add_argument("--not-beyond-input", default=str(NOT_BEYOND_INPUT_PATH))
    parser.add_argument("--beyond-card", default=str(BEYOND_CARD_PATH))
    parser.add_argument("--beyond-card-summary", default=str(BEYOND_CARD_SUMMARY_PATH))
    parser.add_argument("--not-beyond-card", default=str(NOT_BEYOND_CARD_PATH))
    parser.add_argument("--not-beyond-card-summary", default=str(NOT_BEYOND_CARD_SUMMARY_PATH))
    args = parser.parse_args()

    beyond_input_path = Path(args.beyond_input)
    not_beyond_input_path = Path(args.not_beyond_input)
    beyond_card_path = Path(args.beyond_card)
    beyond_card_summary_path = Path(args.beyond_card_summary)
    not_beyond_card_path = Path(args.not_beyond_card)
    not_beyond_card_summary_path = Path(args.not_beyond_card_summary)

    assert_header(beyond_input_path)
    assert_header(not_beyond_input_path)
    beyond_rows = read_rows(beyond_input_path)
    not_beyond_rows = read_rows(not_beyond_input_path)

    beyond_summary = summarize_rows(
        rows=beyond_rows,
        scope="REOPEN_B9_N02_IB_OR_BEYOND_CONTINUATION_CARD_P0",
        input_path=beyond_input_path,
        card_path=beyond_card_path,
        summary_path=beyond_card_summary_path,
    )
    beyond_card_summary_path.write_text(json.dumps(beyond_summary, ensure_ascii=True, indent=2), encoding="utf-8")
    beyond_card_path.write_text(
        render_card(
            title="n02_ib_or_beyond_continuation_card v1",
            purpose_line="把 `beyond continuation` 观察固定成独立说明卡。",
            summary=beyond_summary,
            decision_lines=[
                "`beyond continuation` 当前只说明：下一同类 session 首 30 分钟是否整体仍在前一日 `IB` 外侧。",
                "当前 `2/9` 行满足持续外侧，`5/9` 行不满足，`2/9` 行缺下一同类 session 数据。",
                "后续若继续推进，应从满足持续外侧的样本再拆 continuation persistence，不直接改名成 `failed breakout`。",
            ],
        ),
        encoding="utf-8",
    )

    not_beyond_summary = summarize_rows(
        rows=not_beyond_rows,
        scope="REOPEN_B9_N02_IB_OR_NOT_BEYOND_STABILITY_CARD_P0",
        input_path=not_beyond_input_path,
        card_path=not_beyond_card_path,
        summary_path=not_beyond_card_summary_path,
    )
    not_beyond_card_summary_path.write_text(json.dumps(not_beyond_summary, ensure_ascii=True, indent=2), encoding="utf-8")
    not_beyond_card_path.write_text(
        render_card(
            title="n02_ib_or_not_beyond_stability_card v1",
            purpose_line="把 `not_beyond pullback stability` 观察固定成独立说明卡。",
            summary=not_beyond_summary,
            decision_lines=[
                "`not_beyond stability` 当前只说明：下一同类 session 首 30 分钟是否整体仍在前一日 `IB` 内侧或边界。",
                "当前 `2/6` 行满足稳定内侧，`2/6` 行不满足，`2/6` 行缺下一同类 session 数据。",
                "后续若继续推进，应从满足稳定内侧的样本再拆 stability persistence，不直接改名成 `failed breakout`。",
            ],
        ),
        encoding="utf-8",
    )

    print("beyond_card_path={0}".format(beyond_card_path))
    print("beyond_card_summary_path={0}".format(beyond_card_summary_path))
    print("not_beyond_card_path={0}".format(not_beyond_card_path))
    print("not_beyond_card_summary_path={0}".format(not_beyond_card_summary_path))
    print("beyond_rows={0}".format(len(beyond_rows)))
    print("beyond_status_counts={0}".format(json.dumps(beyond_summary["status_counts"], ensure_ascii=True)))
    print("not_beyond_rows={0}".format(len(not_beyond_rows)))
    print("not_beyond_status_counts={0}".format(json.dumps(not_beyond_summary["status_counts"], ensure_ascii=True)))


if __name__ == "__main__":
    main()
