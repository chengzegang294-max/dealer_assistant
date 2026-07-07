from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

RUNTIME_DIR = Path(__file__).parent
SLICE_SUMMARY_PATH = RUNTIME_DIR / "n02_gbpusd_m15_candidate_slice_summary_v1.json"
RELATION_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_relation_p0_summary_gbpusd_m15_slice_v1.json"
FIRST_BREAK_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_first_break_relative_p0_summary_gbpusd_m15_slice_v1.json"
BREAK_BAR_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_break_bar_evidence_p0_summary_gbpusd_m15_slice_v1.json"
CROSS_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_cross_outcome_split_p0_summary_gbpusd_m15_slice_v1.json"
POST_CROSS_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_post_cross_path_observation_p0_summary_gbpusd_m15_slice_v1.json"
NEXT_BEYOND_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_beyond_continuation_observation_p0_summary_gbpusd_m15_slice_v1.json"
NEXT_NOT_BEYOND_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_not_beyond_pullback_stability_observation_p0_summary_gbpusd_m15_slice_v1.json"
MULTI_BEYOND_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_beyond_multi_session_persistence_observation_p0_summary_gbpusd_m15_slice_v1.json"
MULTI_NOT_BEYOND_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_not_beyond_multi_session_stability_observation_p0_summary_gbpusd_m15_slice_v1.json"
TERMINAL_SUMMARY_PATH = RUNTIME_DIR / "n02_ib_or_third_same_session_terminal_summary_gbpusd_m15_slice_v1.json"
OR_ONLY_SESSION_CLOSE_SUMMARY_PATH = (
    RUNTIME_DIR / "n02_ib_or_or_break_only_same_day_session_close_split_p0_summary_gbpusd_m15_slice_v1.json"
)
OR_ONLY_BEYOND_CARD_SUMMARY_PATH = (
    RUNTIME_DIR / "n02_ib_or_or_break_only_session_close_beyond_or_summary_gbpusd_m15_slice_v1.json"
)
OR_ONLY_NOT_BEYOND_CARD_SUMMARY_PATH = (
    RUNTIME_DIR / "n02_ib_or_or_break_only_session_close_not_beyond_or_summary_gbpusd_m15_slice_v1.json"
)
OR_ONLY_BEYOND_NEXT_SESSION_SUMMARY_PATH = (
    RUNTIME_DIR
    / "n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_p0_summary_gbpusd_m15_slice_v1.json"
)
OR_ONLY_BEYOND_NEXT_SESSION_CARD_SUMMARY_PATH = (
    RUNTIME_DIR
    / "n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_card_summary_gbpusd_m15_slice_v1.json"
)
OR_ONLY_BEYOND_MULTI_SESSION_SUMMARY_PATH = (
    RUNTIME_DIR
    / "n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_p0_summary_gbpusd_m15_slice_v1.json"
)
OR_ONLY_BEYOND_MULTI_SESSION_CARD_SUMMARY_PATH = (
    RUNTIME_DIR
    / "n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_card_summary_gbpusd_m15_slice_v1.json"
)
OUTPUT_MD_PATH = RUNTIME_DIR / "n02_gbpusd_m15_slice_downstream_summary_v1.md"
OUTPUT_JSON_PATH = RUNTIME_DIR / "n02_gbpusd_m15_slice_downstream_summary_v1.json"


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_summary(paths: Dict[str, Path]) -> Dict[str, Any]:
    slice_summary = load_json(paths["slice"])
    relation_summary = load_json(paths["relation"])
    first_break_summary = load_json(paths["first_break"])
    break_bar_summary = load_json(paths["break_bar"])
    cross_summary = load_json(paths["cross"])
    post_cross_summary = load_json(paths["post_cross"])
    next_beyond_summary = load_json(paths["next_beyond"])
    next_not_beyond_summary = load_json(paths["next_not_beyond"])
    multi_beyond_summary = load_json(paths["multi_beyond"])
    multi_not_beyond_summary = load_json(paths["multi_not_beyond"])
    terminal_summary = load_json(paths["terminal"])
    or_only_session_close_summary = load_json(paths["or_only_session_close"])
    or_only_beyond_card_summary = load_json(paths["or_only_beyond_card"])
    or_only_not_beyond_card_summary = load_json(paths["or_only_not_beyond_card"])
    or_only_beyond_next_session_summary = load_json(paths["or_only_beyond_next_session"])
    or_only_beyond_next_session_card_summary = load_json(paths["or_only_beyond_next_session_card"])
    or_only_beyond_multi_session_summary = load_json(paths["or_only_beyond_multi_session"])
    or_only_beyond_multi_session_card_summary = load_json(paths["or_only_beyond_multi_session_card"])

    return {
        "producer": "n02_gbpusd_m15_slice_downstream_summary_build_v1.py",
        "scope": "REOPEN_B9_N02_GBPUSD_M15_SLICE_DOWNSTREAM_WITHOUT_FAILED_BREAKOUT_P0",
        "status": "fresh_run_gbpusd_m15_slice_downstream_terminal_summary",
        "evidence_mode": "fresh_run_derived_from_slice_runtime_and_downstream_summaries",
        "source_path": {key: str(value) for key, value in paths.items()},
        "repo_path": {
            "summary_md": str(OUTPUT_MD_PATH),
            "summary_json": str(OUTPUT_JSON_PATH),
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "boundary": {
            "symbol": "GBPUSD",
            "timeframe": "M15",
            "source_mode": "historical_recovered_slice_from_candidate_runtime",
            "writes_main_runtime": False,
            "includes_failed_breakout": False,
        },
        "slice": {
            "or_rows": slice_summary["or_slice_rows"],
            "or_defined_rows": slice_summary["or_defined_rows"],
            "ib_rows": slice_summary["ib_slice_rows"],
            "ib_defined_rows": slice_summary["ib_defined_rows"],
            "session_ids": slice_summary["session_ids"],
        },
        "relation": {
            "rows": relation_summary["relation_rows_written"],
            "ib_equals_or_rows": relation_summary["ib_equals_or_rows"],
            "first_break_direction_counts": relation_summary["first_break_direction_counts"],
            "first_break_mode_counts": relation_summary["first_break_mode_counts"],
        },
        "first_break_relative": {
            "rows": first_break_summary["output_rows_written"],
            "case_counts": first_break_summary["first_break_relative_case_counts"],
            "shared_edge_break_rows": first_break_summary["shared_edge_break_rows"],
            "gap_remaining_rows": first_break_summary["gap_remaining_rows"],
            "requires_break_price_rows": first_break_summary["requires_break_price_rows"],
        },
        "break_bar_evidence": {
            "rows": break_bar_summary["output_rows_written"],
            "cross_confirmed_rows": break_bar_summary["ib_same_side_cross_confirmed_rows"],
            "not_crossed_rows": break_bar_summary["ib_same_side_not_crossed_rows"],
            "evidence_status_counts": break_bar_summary["evidence_status_counts"],
        },
        "cross_outcome_split": {
            "confirmed_cross_rows": cross_summary["confirmed_cross_rows"],
            "or_break_only_rows": cross_summary["or_break_only_rows"],
            "no_break_rows": cross_summary["no_break_rows"],
        },
        "post_cross": {
            "rows": post_cross_summary["rows"],
            "return_inside_rows": post_cross_summary["return_inside_ib_observed_same_day_rows"],
            "session_close_beyond_ib_rows": post_cross_summary["session_close_beyond_ib_rows"],
        },
        "next_session": {
            "beyond_rows": next_beyond_summary["rows"],
            "beyond_status_counts": next_beyond_summary["status_counts"],
            "not_beyond_rows": next_not_beyond_summary["rows"],
            "not_beyond_status_counts": next_not_beyond_summary["status_counts"],
        },
        "multi_session": {
            "beyond_rows": multi_beyond_summary["rows"],
            "beyond_status_counts": multi_beyond_summary["status_counts"],
            "not_beyond_rows": multi_not_beyond_summary["rows"],
            "not_beyond_status_counts": multi_not_beyond_summary["status_counts"],
        },
        "terminal": {
            "total_rows": terminal_summary["total_rows"],
            "resolved_rows": terminal_summary["resolved_rows"],
            "missing_rows": terminal_summary["missing_rows"],
            "beyond_status_counts": terminal_summary["beyond_status_counts"],
            "not_beyond_status_counts": terminal_summary["not_beyond_status_counts"],
        },
        "or_break_only_same_day_session_close": {
            "rows": or_only_session_close_summary["rows"],
            "return_inside_or_rows": or_only_session_close_summary["return_inside_or_observed_same_day_rows"],
            "session_close_beyond_or_rows": or_only_session_close_summary["session_close_beyond_or_rows"],
            "session_close_not_beyond_or_rows": or_only_session_close_summary["session_close_not_beyond_or_rows"],
            "by_session": or_only_session_close_summary["by_session"],
        },
        "or_break_only_branch_cards": {
            "session_close_beyond_or_rows": or_only_beyond_card_summary["rows"],
            "session_close_beyond_or_direction_counts": or_only_beyond_card_summary["direction_counts"],
            "session_close_not_beyond_or_rows": or_only_not_beyond_card_summary["rows"],
            "session_close_not_beyond_or_direction_counts": or_only_not_beyond_card_summary["direction_counts"],
        },
        "or_break_only_beyond_next_session_continuation": {
            "rows": or_only_beyond_next_session_summary["rows"],
            "status_counts": or_only_beyond_next_session_summary["status_counts"],
            "by_session": or_only_beyond_next_session_summary["by_session"],
        },
        "or_break_only_beyond_next_session_continuation_card": {
            "rows": or_only_beyond_next_session_card_summary["rows"],
            "status_counts": or_only_beyond_next_session_card_summary["status_counts"],
            "direction_counts": or_only_beyond_next_session_card_summary["direction_counts"],
        },
        "or_break_only_beyond_multi_session_persistence": {
            "rows": or_only_beyond_multi_session_summary["rows"],
            "status_counts": or_only_beyond_multi_session_summary["status_counts"],
            "by_session": or_only_beyond_multi_session_summary["by_session"],
        },
        "or_break_only_beyond_multi_session_persistence_card": {
            "rows": or_only_beyond_multi_session_card_summary["rows"],
            "status_counts": or_only_beyond_multi_session_card_summary["status_counts"],
            "direction_counts": or_only_beyond_multi_session_card_summary["direction_counts"],
        },
        "gate": {
            "status": "gbpusd_m15_slice_downstream_plus_or_break_only_beyond_multi_session_persistence_done_without_failed_breakout",
            "preferred_next_step": "hold_or_expand_or_break_only_beyond_multi_session_all_closes_branch_only_if_needed",
        },
    }


def render_md(summary: Dict[str, Any]) -> str:
    lines = [
        "# n02_gbpusd_m15_slice_downstream_summary v1",
        "",
        "## 作用",
        "",
        "- 把 `GBPUSD/M15 historical recovered -> slice runtime -> downstream terminal summary` 收口成一份总览。",
        "- 当前只覆盖 `without_failed_breakout` 范围，不把任何分支升级成 `failed breakout / retest / reject / day type`。",
        "",
        "## 2026-07-06 fresh-run",
        "",
        "- `slice_or_rows`：`{0}`".format(summary["slice"]["or_rows"]),
        "- `slice_or_defined_rows`：`{0}`".format(summary["slice"]["or_defined_rows"]),
        "- `slice_ib_rows`：`{0}`".format(summary["slice"]["ib_rows"]),
        "- `slice_ib_defined_rows`：`{0}`".format(summary["slice"]["ib_defined_rows"]),
        "- `relation_rows`：`{0}`".format(summary["relation"]["rows"]),
        "- `first_break_relative_case_counts`：`{0}`".format(json.dumps(summary["first_break_relative"]["case_counts"], ensure_ascii=True)),
        "- `break_bar_evidence_status_counts`：`{0}`".format(json.dumps(summary["break_bar_evidence"]["evidence_status_counts"], ensure_ascii=True)),
        "- `cross_outcome_split`：`{0}`".format(json.dumps(summary["cross_outcome_split"], ensure_ascii=True)),
        "- `post_cross`：`{0}`".format(json.dumps(summary["post_cross"], ensure_ascii=True)),
        "- `next_session`：`{0}`".format(json.dumps(summary["next_session"], ensure_ascii=True)),
        "- `multi_session`：`{0}`".format(json.dumps(summary["multi_session"], ensure_ascii=True)),
        "- `terminal`：`{0}`".format(json.dumps(summary["terminal"], ensure_ascii=True)),
        "- `or_break_only_same_day_session_close`：`{0}`".format(
            json.dumps(summary["or_break_only_same_day_session_close"], ensure_ascii=True)
        ),
        "- `or_break_only_branch_cards`：`{0}`".format(
            json.dumps(summary["or_break_only_branch_cards"], ensure_ascii=True)
        ),
        "- `or_break_only_beyond_next_session_continuation`：`{0}`".format(
            json.dumps(summary["or_break_only_beyond_next_session_continuation"], ensure_ascii=True)
        ),
        "- `or_break_only_beyond_next_session_continuation_card`：`{0}`".format(
            json.dumps(summary["or_break_only_beyond_next_session_continuation_card"], ensure_ascii=True)
        ),
        "- `or_break_only_beyond_multi_session_persistence`：`{0}`".format(
            json.dumps(summary["or_break_only_beyond_multi_session_persistence"], ensure_ascii=True)
        ),
        "- `or_break_only_beyond_multi_session_persistence_card`：`{0}`".format(
            json.dumps(summary["or_break_only_beyond_multi_session_persistence_card"], ensure_ascii=True)
        ),
        "",
        "## 当前裁决",
        "",
        "- `GBPUSD/M15` recovered downstream 已完成 slice 化与 terminal summary 收口。",
        "- `or_break_only` 分支已继续推进到 same-day `session_close_beyond_or / session_close_not_beyond_or`，并对 beyond_or 分支补到 next-session continuation 与 multi-session persistence。",
        "- 这条链当前固定停在 `gbpusd_m15_slice_downstream_plus_or_break_only_beyond_multi_session_persistence_done_without_failed_breakout`。",
        "- `no_break_rows` 与缺失后续 session 数据都已显式保留，不再混入 `confirmed cross` 或 `or break only`。",
        "- 当前仍不把任何结果改写成 `failed breakout`。",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-md", default=str(OUTPUT_MD_PATH))
    parser.add_argument("--output-json", default=str(OUTPUT_JSON_PATH))
    args = parser.parse_args()

    output_md_path = Path(args.output_md)
    output_json_path = Path(args.output_json)
    paths = {
        "slice": SLICE_SUMMARY_PATH,
        "relation": RELATION_SUMMARY_PATH,
        "first_break": FIRST_BREAK_SUMMARY_PATH,
        "break_bar": BREAK_BAR_SUMMARY_PATH,
        "cross": CROSS_SUMMARY_PATH,
        "post_cross": POST_CROSS_SUMMARY_PATH,
        "next_beyond": NEXT_BEYOND_SUMMARY_PATH,
        "next_not_beyond": NEXT_NOT_BEYOND_SUMMARY_PATH,
        "multi_beyond": MULTI_BEYOND_SUMMARY_PATH,
        "multi_not_beyond": MULTI_NOT_BEYOND_SUMMARY_PATH,
        "terminal": TERMINAL_SUMMARY_PATH,
        "or_only_session_close": OR_ONLY_SESSION_CLOSE_SUMMARY_PATH,
        "or_only_beyond_card": OR_ONLY_BEYOND_CARD_SUMMARY_PATH,
        "or_only_not_beyond_card": OR_ONLY_NOT_BEYOND_CARD_SUMMARY_PATH,
        "or_only_beyond_next_session": OR_ONLY_BEYOND_NEXT_SESSION_SUMMARY_PATH,
        "or_only_beyond_next_session_card": OR_ONLY_BEYOND_NEXT_SESSION_CARD_SUMMARY_PATH,
        "or_only_beyond_multi_session": OR_ONLY_BEYOND_MULTI_SESSION_SUMMARY_PATH,
        "or_only_beyond_multi_session_card": OR_ONLY_BEYOND_MULTI_SESSION_CARD_SUMMARY_PATH,
    }
    summary = build_summary(paths)
    output_json_path.write_text(json.dumps(summary, ensure_ascii=True, indent=2), encoding="utf-8")
    output_md_path.write_text(render_md(summary), encoding="utf-8")

    print("output_md={0}".format(output_md_path))
    print("output_json={0}".format(output_json_path))
    print("gate_status={0}".format(summary["gate"]["status"]))
    print("terminal_total_rows={0}".format(summary["terminal"]["total_rows"]))
    print("terminal_resolved_rows={0}".format(summary["terminal"]["resolved_rows"]))
    print("terminal_missing_rows={0}".format(summary["terminal"]["missing_rows"]))


if __name__ == "__main__":
    main()
