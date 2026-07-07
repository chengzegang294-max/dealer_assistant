from __future__ import annotations

import json
from pathlib import Path

from cross_line_frozen_acceptance_compare_v1 import ValidationError, build_expected_blocks, unwrap_line


def read_chain_compare(md_path: Path) -> dict[str, object]:
    result: dict[str, object] = {}
    for raw_line in md_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.startswith("  - `chain_index_md_exists = ") and line.endswith("`"):
            result["chain_index_md_exists"] = unwrap_line(line, "- `chain_index_md_exists = ")
        elif line.startswith("  - `indexed_stage_count = ") and line.endswith("`"):
            result["indexed_stage_count"] = int(unwrap_line(line, "- `indexed_stage_count = "))
        elif line.startswith("  - `expected_stage_count = ") and line.endswith("`"):
            result["expected_stage_count"] = int(unwrap_line(line, "- `expected_stage_count = "))
        elif line.startswith("  - `rows_match = ") and line.endswith("`"):
            result["rows_match"] = unwrap_line(line, "- `rows_match = ")
        elif line.startswith("  - `candidate_ids = ") and line.endswith("`"):
            result["candidate_ids"] = json.loads(unwrap_line(line, "- `candidate_ids = "))
        elif line.startswith("  - `cross_line_frozen_chain_acceptance_compare_passed = ") and line.endswith("`"):
            result["chain_compare_passed"] = unwrap_line(
                line, "- `cross_line_frozen_chain_acceptance_compare_passed = "
            )
    if not result:
        raise ValidationError("chain acceptance compare markdown has no parsed fields")
    return result


def read_manifest_acceptance(md_path: Path) -> dict[str, object]:
    result: dict[str, object] = {}
    for raw_line in md_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.startswith("  - `artifact_count = ") and line.endswith("`"):
            result["artifact_count"] = int(unwrap_line(line, "- `artifact_count = "))
        elif line.startswith("  - `all_artifacts_exist = ") and line.endswith("`"):
            result["all_artifacts_exist"] = unwrap_line(line, "- `all_artifacts_exist = ")
        elif line.startswith("  - `candidate_count = ") and line.endswith("`"):
            result["candidate_count"] = int(unwrap_line(line, "- `candidate_count = "))
        elif line.startswith("  - `rows_match = ") and line.endswith("`"):
            result["rows_match"] = unwrap_line(line, "- `rows_match = ")
        elif line.startswith("  - `cross_line_frozen_manifest_acceptance_passed = ") and line.endswith("`"):
            result["manifest_acceptance_passed"] = unwrap_line(
                line, "- `cross_line_frozen_manifest_acceptance_passed = "
            )
    if not result:
        raise ValidationError("manifest acceptance markdown has no parsed fields")
    return result


def main() -> None:
    runtime_root = Path(__file__).resolve().parent
    chain_index_md = runtime_root / "cross_line_frozen_acceptance_chain_index_v1.md"
    chain_compare_md = runtime_root / "cross_line_frozen_chain_acceptance_compare_v1.md"
    manifest_acceptance_md = runtime_root / "cross_line_frozen_manifest_acceptance_v1.md"

    expected_candidate_ids = [item["candidate"] for item in build_expected_blocks(runtime_root)]
    expected_stage_count = 3

    chain_compare = read_chain_compare(chain_compare_md)
    if chain_compare.get("chain_index_md_exists") != "True":
        raise ValidationError("chain_index_md_exists is not True in chain compare acceptance")
    if chain_compare.get("indexed_stage_count") != expected_stage_count:
        raise ValidationError("indexed_stage_count mismatch in chain compare acceptance")
    if chain_compare.get("expected_stage_count") != expected_stage_count:
        raise ValidationError("expected_stage_count mismatch in chain compare acceptance")
    if chain_compare.get("rows_match") != "true":
        raise ValidationError("rows_match is not true in chain compare acceptance")
    if chain_compare.get("candidate_ids") != expected_candidate_ids:
        raise ValidationError("candidate_ids mismatch in chain compare acceptance")
    if chain_compare.get("chain_compare_passed") != "true":
        raise ValidationError("chain compare pass flag is not true")

    manifest_acceptance = read_manifest_acceptance(manifest_acceptance_md)
    if manifest_acceptance.get("artifact_count") != 4:
        raise ValidationError("artifact_count mismatch in manifest acceptance")
    if manifest_acceptance.get("all_artifacts_exist") != "True":
        raise ValidationError("all_artifacts_exist is not True in manifest acceptance")
    if manifest_acceptance.get("candidate_count") != len(expected_candidate_ids):
        raise ValidationError("candidate_count mismatch in manifest acceptance")
    if manifest_acceptance.get("rows_match") != "true":
        raise ValidationError("rows_match is not true in manifest acceptance")
    if manifest_acceptance.get("manifest_acceptance_passed") != "true":
        raise ValidationError("manifest acceptance pass flag is not true")

    artifacts = [
        {"slot": "chain_index", "file": str(chain_index_md.relative_to(runtime_root)), "exists": chain_index_md.exists()},
        {"slot": "chain_compare", "file": str(chain_compare_md.relative_to(runtime_root)), "exists": chain_compare_md.exists()},
        {
            "slot": "manifest_acceptance",
            "file": str(manifest_acceptance_md.relative_to(runtime_root)),
            "exists": manifest_acceptance_md.exists(),
        },
    ]

    print("validation_mode=cross_line_frozen_chain_manifest_acceptance")
    print("artifact_count={0}".format(len(artifacts)))
    print("all_artifacts_exist={0}".format(all(item["exists"] for item in artifacts)))
    print("candidate_count={0}".format(len(expected_candidate_ids)))
    print("rows_match=true")
    print("artifact_index={0}".format(json.dumps(artifacts, ensure_ascii=True)))
    print("write_attempted=false")
    print("cross_line_frozen_chain_manifest_acceptance_passed=true")


if __name__ == "__main__":
    main()
