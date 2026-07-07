from __future__ import annotations

import json
import os
from pathlib import Path

from rsj_state_p0_runtime_append_stub_v1 import load_params, read_rows as read_runtime_rows
from rsj_state_p0_validate_replay_preview_acceptance_v1 import read_preview_rows


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
    runtime_csv = runtime_dir / params["output_csv"]
    preview_csv = runtime_dir / params["replay_preview_csv"]

    stages = [
        ("min_contract", "rsj_state_p0_min_contract_v1.md"),
        ("proof_mapping", "rsj_state_p0_proof_of_mapping_v1.md"),
        ("runtime_append_acceptance", params["append_acceptance_file"]),
        ("raw_window_sample_acceptance", params["raw_window_sample_acceptance_file"]),
        ("raw_window_mapping_acceptance", params["raw_window_mapping_acceptance_file"]),
        ("append_compatibility_acceptance", params["append_compatibility_acceptance_file"]),
        ("simulate_append_diff_acceptance", params["simulate_append_diff_acceptance_file"]),
        ("replay_preview_acceptance", params["replay_preview_acceptance_file"]),
        (
            "replay_preview_acceptance_validation",
            params["replay_preview_acceptance_validation_file"],
        ),
        ("replay_chain_acceptance", params["replay_chain_acceptance_file"]),
    ]
    stage_status = [
        {"stage": stage_name, "file": file_name, "exists": (runtime_dir / file_name).exists()}
        for stage_name, file_name in stages
    ]
    runtime_row_count = len(read_runtime_rows(runtime_csv))
    preview_row_count = len(read_preview_rows(preview_csv))

    print("summary_mode=archive_chain_summary_index_export")
    print("candidate_id={0}".format(params["candidate_id"]))
    print("runtime_dir_exists={0}".format(runtime_dir.exists()))
    print("runtime_csv_exists={0}".format(runtime_csv.exists()))
    print("preview_csv_exists={0}".format(preview_csv.exists()))
    print("runtime_row_count={0}".format(runtime_row_count))
    print("preview_row_count={0}".format(preview_row_count))
    print("stage_count={0}".format(len(stage_status)))
    print("all_stage_files_exist={0}".format(all(item["exists"] for item in stage_status)))
    print("stage_status={0}".format(json.dumps(stage_status, ensure_ascii=True)))
    print("archive_only=true")
    print("path_policy=repo_first")
    print("write_attempted=false")
    print("archive_chain_summary_export_passed=true")


if __name__ == "__main__":
    main()
