from __future__ import annotations

import json
from pathlib import Path

from cross_line_frozen_acceptance_compare_v1 import ValidationError, build_expected_blocks, unwrap_line


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
    stage_files = [
        "cross_line_frozen_manifest_index_v1.md",
        "cross_line_frozen_acceptance_compare_v1.md",
        "cross_line_frozen_manifest_acceptance_v1.md",
    ]
    stage_paths = [runtime_root / file_name for file_name in stage_files]
    if not all(path.exists() for path in stage_paths):
        missing = [str(path.relative_to(runtime_root)) for path in stage_paths if not path.exists()]
        raise ValidationError("missing stage files: {0}".format(missing))

    expected_blocks = build_expected_blocks(runtime_root)
    candidate_ids = [item["candidate"] for item in expected_blocks]
    manifest_acceptance = read_manifest_acceptance(runtime_root / stage_files[2])
    if manifest_acceptance.get("artifact_count") != 4:
        raise ValidationError("artifact_count mismatch in manifest acceptance")
    if manifest_acceptance.get("all_artifacts_exist") != "True":
        raise ValidationError("all_artifacts_exist is not True in manifest acceptance")
    if manifest_acceptance.get("candidate_count") != len(candidate_ids):
        raise ValidationError("candidate_count mismatch in manifest acceptance")
    if manifest_acceptance.get("rows_match") != "true":
        raise ValidationError("rows_match is not true in manifest acceptance")
    if manifest_acceptance.get("manifest_acceptance_passed") != "true":
        raise ValidationError("manifest acceptance pass flag is not true")

    print("index_mode=cross_line_frozen_acceptance_chain_index")
    print("stage_count={0}".format(len(stage_files)))
    print("all_stage_files_exist={0}".format(all(path.exists() for path in stage_paths)))
    print("candidate_count={0}".format(len(candidate_ids)))
    print("artifact_count={0}".format(manifest_acceptance["artifact_count"]))
    print("candidate_ids={0}".format(json.dumps(candidate_ids, ensure_ascii=True)))
    print("stage_files={0}".format(json.dumps(stage_files, ensure_ascii=True)))
    print("write_attempted=false")
    print("cross_line_frozen_acceptance_chain_index_passed=true")


if __name__ == "__main__":
    main()
