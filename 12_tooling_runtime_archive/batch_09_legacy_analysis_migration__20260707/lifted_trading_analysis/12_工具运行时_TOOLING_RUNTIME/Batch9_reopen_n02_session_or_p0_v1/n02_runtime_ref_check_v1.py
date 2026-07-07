from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

RUNTIME_DIR = Path(__file__).parent
REPO_ROOT = RUNTIME_DIR.parents[2]

DOWNSTREAM_SUMMARY_PATH = RUNTIME_DIR / "n02_gbpusd_m15_slice_downstream_summary_v1.json"
OR_ONLY_BEYOND_MULTI_SESSION_SUMMARY_PATH = (
    RUNTIME_DIR
    / "n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_p0_summary_gbpusd_m15_slice_v1.json"
)
OR_ONLY_BEYOND_MULTI_SESSION_CARD_SUMMARY_PATH = (
    RUNTIME_DIR
    / "n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_card_summary_gbpusd_m15_slice_v1.json"
)
MAIN_INDEX_PATH = REPO_ROOT / "04_active_main_docs" / "batch_01_selected" / "00_主线检索索引.md"
MIGRATION_MAP_PATH = REPO_ROOT / "00_entry" / "FULL_REPO_MIGRATION_MAP.md"

DEFAULT_REPORT_PATH = RUNTIME_DIR / "n02_runtime_ref_check_report_v1.json"
DEFAULT_EXPECTED_GATE_STATUS = (
    "gbpusd_m15_slice_downstream_plus_or_break_only_beyond_multi_session_persistence_done_without_failed_breakout"
)


def utc_now_iso_z() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_stat_size(path: Path) -> Optional[int]:
    if not path.exists():
        return None
    return path.stat().st_size


def check_file(path: Path) -> Dict[str, Any]:
    return {
        "path": str(path),
        "exists": path.exists(),
        "size_bytes": safe_stat_size(path),
    }


def sum_status_counts(status_counts: Any) -> Optional[int]:
    if not isinstance(status_counts, dict):
        return None
    status_counts_any = cast(Dict[Any, Any], status_counts)
    typed_counts: Dict[str, int] = {}
    for key_any, value_any in status_counts_any.items():
        if not isinstance(key_any, str):
            return None
        if not isinstance(value_any, int):
            return None
        typed_counts[key_any] = value_any
    return sum(typed_counts.values())


def check_status_counts_match_rows(summary: Dict[str, Any]) -> Dict[str, Any]:
    rows = summary.get("rows")
    status_counts = summary.get("status_counts")
    status_sum = sum_status_counts(status_counts)
    ok = isinstance(rows, int) and status_sum is not None and rows == status_sum
    return {
        "rows": rows,
        "status_counts_sum": status_sum,
        "ok": ok,
    }


def check_gate_status(summary: Dict[str, Any], expected_gate_status: str) -> Dict[str, Any]:
    gate = summary.get("gate")
    observed: Optional[str] = None
    if isinstance(gate, dict):
        gate_any = cast(Dict[Any, Any], gate)
        observed_any = gate_any.get("status")
        if isinstance(observed_any, str):
            observed = observed_any
    ok = observed == expected_gate_status
    return {
        "expected": expected_gate_status,
        "observed": observed,
        "ok": ok,
    }


def contains_text(path: Path, needle: str) -> Dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "exists": False, "needle": needle, "contains": False}
    text = path.read_text(encoding="utf-8", errors="replace")
    return {
        "path": str(path),
        "exists": True,
        "needle": needle,
        "contains": needle in text,
    }


def contains_text_fallback(path: Path, primary: str, fallback: str) -> Dict[str, Any]:
    primary_check = contains_text(path, primary)
    fallback_check = contains_text(path, fallback)
    contains_any = bool(primary_check.get("contains")) or bool(fallback_check.get("contains"))
    matched: List[str] = []
    if primary_check.get("contains"):
        matched.append(primary)
    if fallback_check.get("contains") and fallback != primary:
        matched.append(fallback)
    return {
        "path": str(path),
        "exists": bool(primary_check.get("exists")),
        "primary": primary_check,
        "fallback": fallback_check,
        "contains": contains_any,
        "matched": matched,
    }


def build_report(expected_gate_status: str) -> Dict[str, Any]:
    files: List[Path] = [
        DOWNSTREAM_SUMMARY_PATH,
        OR_ONLY_BEYOND_MULTI_SESSION_SUMMARY_PATH,
        OR_ONLY_BEYOND_MULTI_SESSION_CARD_SUMMARY_PATH,
        MAIN_INDEX_PATH,
        MIGRATION_MAP_PATH,
        Path(__file__),
    ]

    file_checks = {path.name: check_file(path) for path in files}

    downstream_summary: Optional[Dict[str, Any]] = None
    downstream_gate_check: Optional[Dict[str, Any]] = None
    if DOWNSTREAM_SUMMARY_PATH.exists():
        downstream_summary = load_json(DOWNSTREAM_SUMMARY_PATH)
        downstream_gate_check = check_gate_status(downstream_summary, expected_gate_status)

    or_only_multi_summary: Optional[Dict[str, Any]] = None
    or_only_multi_status_counts_check: Optional[Dict[str, Any]] = None
    if OR_ONLY_BEYOND_MULTI_SESSION_SUMMARY_PATH.exists():
        or_only_multi_summary = load_json(OR_ONLY_BEYOND_MULTI_SESSION_SUMMARY_PATH)
        or_only_multi_status_counts_check = check_status_counts_match_rows(or_only_multi_summary)

    or_only_multi_card_summary: Optional[Dict[str, Any]] = None
    or_only_multi_card_status_counts_check: Optional[Dict[str, Any]] = None
    if OR_ONLY_BEYOND_MULTI_SESSION_CARD_SUMMARY_PATH.exists():
        or_only_multi_card_summary = load_json(OR_ONLY_BEYOND_MULTI_SESSION_CARD_SUMMARY_PATH)
        or_only_multi_card_status_counts_check = check_status_counts_match_rows(or_only_multi_card_summary)

    main_index_gate_contains = contains_text_fallback(
        MAIN_INDEX_PATH,
        expected_gate_status,
        expected_gate_status.replace("_without_failed_breakout", ""),
    )
    migration_map_gate_contains = contains_text(MIGRATION_MAP_PATH, expected_gate_status)

    ok_checks = [bool(v.get("exists")) for v in file_checks.values()]
    if downstream_gate_check is not None:
        ok_checks.append(bool(downstream_gate_check.get("ok")))
    if or_only_multi_status_counts_check is not None:
        ok_checks.append(bool(or_only_multi_status_counts_check.get("ok")))
    if or_only_multi_card_status_counts_check is not None:
        ok_checks.append(bool(or_only_multi_card_status_counts_check.get("ok")))
    ok_checks.append(bool(main_index_gate_contains.get("contains")))
    ok_checks.append(bool(migration_map_gate_contains.get("contains")))

    overall_ok = all(ok_checks)

    return {
        "producer": Path(__file__).name,
        "scope": "REOPEN_B9_N02_RUNTIME_REF_CHECK_V1",
        "status": "ref_check_no_rebuild",
        "evidence_mode": "check_only_no_rebuild",
        "generated_at_utc": utc_now_iso_z(),
        "source_path": {
            "runtime_dir": str(RUNTIME_DIR),
            "repo_root": str(REPO_ROOT),
            "downstream_summary_json": str(DOWNSTREAM_SUMMARY_PATH),
            "or_only_beyond_multi_session_summary_json": str(OR_ONLY_BEYOND_MULTI_SESSION_SUMMARY_PATH),
            "or_only_beyond_multi_session_card_summary_json": str(OR_ONLY_BEYOND_MULTI_SESSION_CARD_SUMMARY_PATH),
            "main_index_md": str(MAIN_INDEX_PATH),
            "full_repo_migration_map_md": str(MIGRATION_MAP_PATH),
            "ref_check_py": str(Path(__file__)),
        },
        "repo_path": {
            "report_json": str(DEFAULT_REPORT_PATH),
        },
        "expected_gate_status": expected_gate_status,
        "files": file_checks,
        "checks": {
            "downstream_gate_status": downstream_gate_check,
            "or_only_beyond_multi_session_status_counts_match_rows": or_only_multi_status_counts_check,
            "or_only_beyond_multi_session_card_status_counts_match_rows": or_only_multi_card_status_counts_check,
            "main_index_contains_expected_gate": main_index_gate_contains,
            "full_repo_migration_map_contains_expected_gate": migration_map_gate_contains,
        },
        "ok": overall_ok,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-gate-status", default=DEFAULT_EXPECTED_GATE_STATUS)
    parser.add_argument("--output-json", default=str(DEFAULT_REPORT_PATH))
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    expected_gate_status = str(args.expected_gate_status)
    output_json_path = Path(args.output_json)

    report = build_report(expected_gate_status)
    output_json_path.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding="utf-8")

    print("output_json={0}".format(output_json_path))
    print("ok={0}".format(report["ok"]))
    print("expected_gate_status={0}".format(expected_gate_status))

    if args.strict and not report["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
