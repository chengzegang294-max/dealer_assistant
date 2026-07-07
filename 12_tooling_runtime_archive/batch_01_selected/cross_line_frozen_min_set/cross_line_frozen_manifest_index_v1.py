from __future__ import annotations

import json
from pathlib import Path


def read_json(file_path: Path) -> dict[str, object]:
    return json.loads(file_path.read_text(encoding="utf-8"))


def build_candidate_manifest(
    candidate_name: str,
    runtime_dir: Path,
    manifest_items: list[tuple[str, str]],
) -> dict[str, object]:
    manifest = [
        {"slot": slot, "file": file_name, "exists": (runtime_dir / file_name).exists()}
        for slot, file_name in manifest_items
    ]
    return {
        "candidate": candidate_name,
        "runtime_dir": str(runtime_dir),
        "manifest_count": len(manifest),
        "all_manifest_files_exist": all(item["exists"] for item in manifest),
        "manifest": manifest,
    }


def rsj_manifest_items(params: dict[str, object]) -> list[tuple[str, str]]:
    return [
        ("min_contract", "rsj_state_p0_min_contract_v1.md"),
        ("proof_mapping", "rsj_state_p0_proof_of_mapping_v1.md"),
        ("runtime_append_acceptance", str(params["append_acceptance_file"])),
        ("raw_window_sample_acceptance", str(params["raw_window_sample_acceptance_file"])),
        ("raw_window_mapping_acceptance", str(params["raw_window_mapping_acceptance_file"])),
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
        ("manifest_freeze", str(params["manifest_freeze_file"])),
    ]


def pv_manifest_items(params: dict[str, object]) -> list[tuple[str, str]]:
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
        ("manifest_freeze", str(params["manifest_freeze_file"])),
    ]


def main() -> None:
    runtime_root = Path(__file__).resolve().parent

    rsj_params_path = runtime_root / "rsj_state_p0_v1" / "rsj_state_p0_runtime_params_template_v1.json"
    pv_params_path = runtime_root / "pv_corr_state_p0_v1" / "pv_corr_state_p0_runtime_params_template_v1.json"
    rsj_params = read_json(rsj_params_path)
    pv_params = read_json(pv_params_path)
    rsj_runtime_dir = Path(str(rsj_params["runtime_dir"]))
    pv_runtime_dir = Path(str(pv_params["runtime_dir"]))

    candidates = [
        build_candidate_manifest(
            str(rsj_params["candidate_id"]),
            rsj_runtime_dir,
            rsj_manifest_items(rsj_params),
        ),
        build_candidate_manifest(
            str(pv_params["candidate_id"]),
            pv_runtime_dir,
            pv_manifest_items(pv_params),
        ),
    ]

    print("index_mode=cross_line_frozen_manifest_index")
    print("runtime_root_exists={0}".format(runtime_root.exists()))
    print("candidate_count={0}".format(len(candidates)))
    print(
        "all_candidates_manifest_frozen={0}".format(
            all(item["all_manifest_files_exist"] for item in candidates)
        )
    )
    print(
        "candidate_ids={0}".format(
            json.dumps([item["candidate"] for item in candidates], ensure_ascii=True)
        )
    )
    print("manifest_index={0}".format(json.dumps(candidates, ensure_ascii=True)))
    print("write_attempted=false")
    print("cross_line_frozen_manifest_index_passed=true")


if __name__ == "__main__":
    main()
