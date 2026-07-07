from __future__ import annotations

import json
from pathlib import Path

from cross_line_frozen_acceptance_chain_index_v1 import read_manifest_acceptance
from cross_line_frozen_acceptance_compare_v1 import ValidationError, build_expected_blocks, unwrap_line


def read_chain_index_summary(md_path: Path) -> dict[str, object]:
    result: dict[str, object] = {}
    for raw_line in md_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.startswith("- `stage_count = ") and line.endswith("`"):
            result["stage_count"] = int(unwrap_line(line, "- `stage_count = "))
        elif line.startswith("- `all_stage_files_exist = ") and line.endswith("`"):
            result["all_stage_files_exist"] = unwrap_line(line, "- `all_stage_files_exist = ")
        elif line.startswith("- `candidate_count = ") and line.endswith("`"):
            result["candidate_count"] = int(unwrap_line(line, "- `candidate_count = "))
        elif line.startswith("- `artifact_count = ") and line.endswith("`"):
            result["artifact_count"] = int(unwrap_line(line, "- `artifact_count = "))
        elif line.startswith("- `candidate_ids = ") and line.endswith("`"):
            result["candidate_ids"] = json.loads(unwrap_line(line, "- `candidate_ids = "))
        elif line.startswith("- `cross_line_frozen_acceptance_chain_index_passed = ") and line.endswith("`"):
            result["chain_index_passed"] = unwrap_line(
                line, "- `cross_line_frozen_acceptance_chain_index_passed = "
            )
    capture_stage_files = False
    stage_files: list[str] = []
    for raw_line in md_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.strip() == "## 当前总链索引":
            capture_stage_files = True
            continue
        if capture_stage_files:
            if line.startswith("- `") and line.endswith("`"):
                stage_files.append(unwrap_line(line, "- `"))
                continue
            if line.startswith("## "):
                break
    if stage_files:
        result["stage_files"] = stage_files
    if not result:
        raise ValidationError("chain index markdown has no parsed fields")
    return result


def main() -> None:
    runtime_root = Path(__file__).resolve().parent
    chain_index_md = runtime_root / "cross_line_frozen_acceptance_chain_index_v1.md"
    manifest_acceptance_md = runtime_root / "cross_line_frozen_manifest_acceptance_v1.md"

    expected_stage_files = [
        "cross_line_frozen_manifest_index_v1.md",
        "cross_line_frozen_acceptance_compare_v1.md",
        "cross_line_frozen_manifest_acceptance_v1.md",
    ]
    chain_index_summary = read_chain_index_summary(chain_index_md)
    manifest_acceptance = read_manifest_acceptance(manifest_acceptance_md)
    expected_candidate_ids = [item["candidate"] for item in build_expected_blocks(runtime_root)]

    if chain_index_summary.get("stage_count") != len(expected_stage_files):
        raise ValidationError("stage_count mismatch in chain index markdown")
    if chain_index_summary.get("all_stage_files_exist") != "True":
        raise ValidationError("all_stage_files_exist is not True in chain index markdown")
    if chain_index_summary.get("candidate_count") != len(expected_candidate_ids):
        raise ValidationError("candidate_count mismatch in chain index markdown")
    if chain_index_summary.get("artifact_count") != manifest_acceptance.get("artifact_count"):
        raise ValidationError("artifact_count mismatch in chain index markdown")
    if chain_index_summary.get("candidate_ids") != expected_candidate_ids:
        raise ValidationError("candidate_ids mismatch in chain index markdown")
    if chain_index_summary.get("stage_files") != expected_stage_files:
        raise ValidationError("stage_files mismatch in chain index markdown")
    if chain_index_summary.get("chain_index_passed") != "true":
        raise ValidationError("chain index pass flag is not true")

    print("validation_mode=cross_line_frozen_chain_acceptance_compare")
    print("chain_index_md_exists={0}".format(chain_index_md.exists()))
    print("indexed_stage_count={0}".format(chain_index_summary["stage_count"]))
    print("expected_stage_count={0}".format(len(expected_stage_files)))
    print("rows_match=true")
    print("candidate_ids={0}".format(json.dumps(expected_candidate_ids, ensure_ascii=True)))
    print("write_attempted=false")
    print("cross_line_frozen_chain_acceptance_compare_passed=true")


if __name__ == "__main__":
    main()
