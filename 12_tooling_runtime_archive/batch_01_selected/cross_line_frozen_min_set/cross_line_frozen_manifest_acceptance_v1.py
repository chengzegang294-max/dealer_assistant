from __future__ import annotations

import json
from pathlib import Path

from cross_line_frozen_acceptance_compare_v1 import (
    ValidationError,
    build_expected_blocks,
    read_index_blocks,
    unwrap_line,
)


def read_acceptance_compare(md_path: Path) -> dict[str, object]:
    result: dict[str, object] = {}
    for raw_line in md_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.startswith("  - `indexed_candidate_count = ") and line.endswith("`"):
            result["indexed_candidate_count"] = int(
                unwrap_line(line, "- `indexed_candidate_count = ")
            )
        elif line.startswith("  - `expected_candidate_count = ") and line.endswith("`"):
            result["expected_candidate_count"] = int(
                unwrap_line(line, "- `expected_candidate_count = ")
            )
        elif line.startswith("  - `rows_match = ") and line.endswith("`"):
            result["rows_match"] = unwrap_line(line, "- `rows_match = ")
        elif line.startswith("  - `candidate_ids = ") and line.endswith("`"):
            result["candidate_ids"] = json.loads(unwrap_line(line, "- `candidate_ids = "))
        elif line.startswith("  - `cross_line_frozen_acceptance_compare_passed = ") and line.endswith("`"):
            result["compare_passed"] = unwrap_line(
                line, "- `cross_line_frozen_acceptance_compare_passed = "
            )
    if not result:
        raise ValidationError("acceptance compare markdown has no parsed fields")
    return result


def main() -> None:
    runtime_root = Path(__file__).resolve().parent
    index_md = runtime_root / "cross_line_frozen_manifest_index_v1.md"
    compare_md = runtime_root / "cross_line_frozen_acceptance_compare_v1.md"
    rsj_manifest_md = runtime_root / "rsj_state_p0_v1" / "rsj_state_p0_manifest_freeze_v1.md"
    pv_manifest_md = runtime_root / "pv_corr_state_p0_v1" / "pv_corr_state_p0_manifest_freeze_v1.md"

    expected_blocks = build_expected_blocks(runtime_root)
    indexed_blocks = read_index_blocks(index_md)
    if indexed_blocks != expected_blocks:
        raise ValidationError(
            "cross line index mismatch: indexed={0} expected={1}".format(
                indexed_blocks, expected_blocks
            )
        )

    compare_summary = read_acceptance_compare(compare_md)
    expected_candidate_ids = [item["candidate"] for item in expected_blocks]
    expected_candidate_count = len(expected_blocks)
    if compare_summary.get("indexed_candidate_count") != expected_candidate_count:
        raise ValidationError("indexed_candidate_count mismatch in compare acceptance")
    if compare_summary.get("expected_candidate_count") != expected_candidate_count:
        raise ValidationError("expected_candidate_count mismatch in compare acceptance")
    if compare_summary.get("rows_match") != "true":
        raise ValidationError("rows_match is not true in compare acceptance")
    if compare_summary.get("candidate_ids") != expected_candidate_ids:
        raise ValidationError("candidate_ids mismatch in compare acceptance")
    if compare_summary.get("compare_passed") != "true":
        raise ValidationError("compare_passed is not true in compare acceptance")

    artifacts = [
        {"slot": "cross_line_index", "file": str(index_md.relative_to(runtime_root)), "exists": index_md.exists()},
        {
            "slot": "cross_line_acceptance_compare",
            "file": str(compare_md.relative_to(runtime_root)),
            "exists": compare_md.exists(),
        },
        {
            "slot": "rsj_manifest_freeze",
            "file": str(rsj_manifest_md.relative_to(runtime_root)),
            "exists": rsj_manifest_md.exists(),
        },
        {
            "slot": "pv_manifest_freeze",
            "file": str(pv_manifest_md.relative_to(runtime_root)),
            "exists": pv_manifest_md.exists(),
        },
    ]

    print("validation_mode=cross_line_frozen_manifest_acceptance")
    print("artifact_count={0}".format(len(artifacts)))
    print("all_artifacts_exist={0}".format(all(item["exists"] for item in artifacts)))
    print("candidate_count={0}".format(expected_candidate_count))
    print("rows_match=true")
    print("artifact_index={0}".format(json.dumps(artifacts, ensure_ascii=True)))
    print("write_attempted=false")
    print("cross_line_frozen_manifest_acceptance_passed=true")


if __name__ == "__main__":
    main()
