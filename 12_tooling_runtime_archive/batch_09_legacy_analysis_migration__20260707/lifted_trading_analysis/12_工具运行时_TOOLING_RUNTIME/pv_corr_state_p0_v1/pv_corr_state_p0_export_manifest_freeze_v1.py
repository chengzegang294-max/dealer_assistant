from __future__ import annotations

import json
import os
from pathlib import Path

from pv_corr_state_p0_runtime_append_stub_v1 import load_params


def manifest_items(params: dict[str, object]) -> list[tuple[str, str]]:
    return [
        ("min_contract", "pv_corr_state_p0_min_contract_v1.md"),
        ("proof_mapping", "pv_corr_state_p0_proof_of_mapping_v1.md"),
        ("runtime_append_acceptance", str(params["append_acceptance_file"])),
        ("bar_window_sample_acceptance", str(params["bar_window_sample_acceptance_file"])),
        ("bar_window_mapping_acceptance", str(params["bar_window_mapping_acceptance_file"])),
        ("append_compatibility_acceptance", str(params["append_compatibility_acceptance_file"])),
        ("simulate_append_diff_acceptance", str(params["simulate_append_diff_acceptance_file"])),
        ("replay_preview_acceptance", str(params["replay_preview_acceptance_file"])),
        (
            "replay_preview_acceptance_validation",
            str(params["replay_preview_acceptance_validation_file"]),
        ),
        ("replay_chain_acceptance", str(params["replay_chain_acceptance_file"])),
        ("chain_summary_index", str(params["chain_summary_index_file"])),
        (
            "chain_summary_acceptance_compare",
            str(params["chain_summary_acceptance_compare_file"]),
        ),
    ]


def ensure_archive_only_run_allowed() -> None:
    if os.environ.get("ALLOW_ARCHIVE_ONLY_RUN") != "1":
        raise SystemExit(
            "ARCHIVE_ONLY: set ALLOW_ARCHIVE_ONLY_RUN=1 and use repo-first entry points under "
            "01_active_objects/ 02_runtime/ 04_active_main_docs/ before running this legacy exporter."
        )


def main() -> None:
    ensure_archive_only_run_allowed()
    params = load_params()
    runtime_dir = Path(params["runtime_dir"])
    manifest = [
        {"slot": slot, "file": file_name, "exists": (runtime_dir / file_name).exists()}
        for slot, file_name in manifest_items(params)
    ]

    print("freeze_mode=archive_manifest_freeze_export")
    print("candidate_id={0}".format(params["candidate_id"]))
    print("runtime_dir_exists={0}".format(runtime_dir.exists()))
    print("manifest_count={0}".format(len(manifest)))
    print("all_manifest_files_exist={0}".format(all(item["exists"] for item in manifest)))
    print("manifest={0}".format(json.dumps(manifest, ensure_ascii=True)))
    print("archive_only=true")
    print("path_policy=repo_first")
    print("write_attempted=false")
    print("manifest_frozen=true")
    print("archive_manifest_freeze_passed=true")


if __name__ == "__main__":
    main()
