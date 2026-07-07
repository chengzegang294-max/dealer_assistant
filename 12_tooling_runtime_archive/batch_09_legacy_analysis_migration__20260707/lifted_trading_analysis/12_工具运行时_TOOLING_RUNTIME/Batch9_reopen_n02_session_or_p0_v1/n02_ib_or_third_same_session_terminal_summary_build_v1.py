from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

RUNTIME_DIR = Path(__file__).parent
BEYOND_CARD_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_beyond_third_same_session_persistence_card_summary_v1.json"
NOT_BEYOND_CARD_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_not_beyond_third_same_session_stability_card_summary_v1.json"
OUTPUT_MD_PATH = RUNTIME_DIR / "n02_ib_or_third_same_session_terminal_summary_v1.md"
OUTPUT_JSON_PATH = RUNTIME_DIR / "n02_ib_or_third_same_session_terminal_summary_v1.json"


def load_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_summary(
    beyond_summary: Dict[str, object],
    not_beyond_summary: Dict[str, object],
    beyond_summary_path: Path,
    not_beyond_summary_path: Path,
    output_md_path: Path,
    output_json_path: Path,
) -> Dict[str, object]:
    beyond_rows = int(beyond_summary["rows"])
    not_beyond_rows = int(not_beyond_summary["rows"])
    beyond_status_counts = dict(beyond_summary["status_counts"])
    not_beyond_status_counts = dict(not_beyond_summary["status_counts"])
    beyond_persistent_rows = int(
        beyond_status_counts.get("third_next_session_first_30m_all_closes_beyond_prior_ib", 0)
    )
    beyond_failed_rows = int(
        beyond_status_counts.get("third_next_session_first_30m_not_all_closes_beyond_prior_ib", 0)
    )
    beyond_missing_rows = int(beyond_status_counts.get("missing_third_next_session_first_30m_data", 0))
    not_beyond_stable_rows = int(
        not_beyond_status_counts.get("third_next_session_first_30m_all_closes_inside_prior_ib", 0)
    )
    not_beyond_unstable_rows = int(
        not_beyond_status_counts.get("third_next_session_first_30m_not_all_closes_inside_prior_ib", 0)
    )
    not_beyond_missing_rows = int(not_beyond_status_counts.get("missing_third_next_session_first_30m_data", 0))
    total_rows = beyond_rows + not_beyond_rows
    resolved_rows = total_rows - beyond_missing_rows - not_beyond_missing_rows
    missing_rows = beyond_missing_rows + not_beyond_missing_rows

    return {
        "producer": "n02_ib_or_third_same_session_terminal_summary_build_v1.py",
        "scope": "REOPEN_B9_N02_IB_OR_THIRD_SAME_SESSION_TERMINAL_SUMMARY_P0",
        "status": "fresh_run_terminal_summary",
        "evidence_mode": "fresh_run_derived_from_third_same_session_branch_cards",
        "source_path": {
            "beyond_card_summary_json": str(beyond_summary_path),
            "not_beyond_card_summary_json": str(not_beyond_summary_path),
        },
        "repo_path": {
            "terminal_summary_md": str(output_md_path),
            "terminal_summary_json": str(output_json_path),
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "boundary": {
            "defines_failed_breakout": False,
            "defines_retest_reject": False,
            "defines_day_type": False,
            "is_terminal_summary_only": True,
        },
        "total_rows": total_rows,
        "resolved_rows": resolved_rows,
        "missing_rows": missing_rows,
        "beyond_rows": beyond_rows,
        "beyond_persistent_rows": beyond_persistent_rows,
        "beyond_failed_rows": beyond_failed_rows,
        "beyond_missing_rows": beyond_missing_rows,
        "not_beyond_rows": not_beyond_rows,
        "not_beyond_stable_rows": not_beyond_stable_rows,
        "not_beyond_unstable_rows": not_beyond_unstable_rows,
        "not_beyond_missing_rows": not_beyond_missing_rows,
        "beyond_status_counts": beyond_status_counts,
        "not_beyond_status_counts": not_beyond_status_counts,
    }


def render_md(summary: Dict[str, object]) -> str:
    lines = [
        "# n02_ib_or_third_same_session_terminal_summary v1",
        "",
        "## 作用",
        "",
        "- 把 `third same-session` 两支 branch card 汇总成 terminal summary。",
        "- 当前只收口 `beyond persistence` 与 `not_beyond stability` 到第三个同类 `session` 的 terminal state，不升级成 `failed breakout / retest / reject / day type`。",
        "",
        "## 2026-07-04 fresh-run",
        "",
        "- `total_rows`：`{0}`".format(summary["total_rows"]),
        "- `resolved_rows`：`{0}`".format(summary["resolved_rows"]),
        "- `missing_rows`：`{0}`".format(summary["missing_rows"]),
        "- `beyond_rows`：`{0}`".format(summary["beyond_rows"]),
        "- `beyond_status_counts`：`{0}`".format(json.dumps(summary["beyond_status_counts"], ensure_ascii=True)),
        "- `not_beyond_rows`：`{0}`".format(summary["not_beyond_rows"]),
        "- `not_beyond_status_counts`：`{0}`".format(json.dumps(summary["not_beyond_status_counts"], ensure_ascii=True)),
        "",
        "## 当前裁决",
        "",
        "- `beyond third same-session persistence` 当前 `{0}/{1}` 行保持外侧，`{2}/{1}` 行未保持外侧，`{3}/{1}` 行缺第三同类 `session` 数据。".format(
            summary["beyond_persistent_rows"],
            summary["beyond_rows"],
            summary["beyond_failed_rows"],
            summary["beyond_missing_rows"],
        ),
        "- `not_beyond third same-session stability` 当前 `{0}/{1}` 行保持内侧稳定，`{2}/{1}` 行失稳，`{3}/{1}` 行缺第三同类 `session` 数据。".format(
            summary["not_beyond_stable_rows"],
            summary["not_beyond_rows"],
            summary["not_beyond_unstable_rows"],
            summary["not_beyond_missing_rows"],
        ),
        "- 这层 terminal summary 当前只给出链路收口：`beyond` 与 `not_beyond` 两支都停在第三同类 `session` terminal state，不升级为更高层标签。",
        "- 当前仍不把任何一支改写成 `failed breakout`。",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--beyond-card-summary", default=str(BEYOND_CARD_SUMMARY_PATH))
    parser.add_argument("--not-beyond-card-summary", default=str(NOT_BEYOND_CARD_SUMMARY_PATH))
    parser.add_argument("--output-md", default=str(OUTPUT_MD_PATH))
    parser.add_argument("--output-json", default=str(OUTPUT_JSON_PATH))
    args = parser.parse_args()

    beyond_summary_path = Path(args.beyond_card_summary)
    not_beyond_summary_path = Path(args.not_beyond_card_summary)
    beyond_summary = load_json(beyond_summary_path)
    not_beyond_summary = load_json(not_beyond_summary_path)
    output_md_path = Path(args.output_md)
    output_json_path = Path(args.output_json)

    summary = build_summary(
        beyond_summary=beyond_summary,
        not_beyond_summary=not_beyond_summary,
        beyond_summary_path=beyond_summary_path,
        not_beyond_summary_path=not_beyond_summary_path,
        output_md_path=output_md_path,
        output_json_path=output_json_path,
    )
    output_json_path.write_text(json.dumps(summary, ensure_ascii=True, indent=2), encoding="utf-8")
    output_md_path.write_text(render_md(summary), encoding="utf-8")

    print("output_md={0}".format(output_md_path))
    print("output_json={0}".format(output_json_path))
    print("total_rows={0}".format(summary["total_rows"]))
    print("resolved_rows={0}".format(summary["resolved_rows"]))
    print("missing_rows={0}".format(summary["missing_rows"]))
    print("beyond_status_counts={0}".format(json.dumps(summary["beyond_status_counts"], ensure_ascii=True)))
    print("not_beyond_status_counts={0}".format(json.dumps(summary["not_beyond_status_counts"], ensure_ascii=True)))


if __name__ == "__main__":
    main()
