from __future__ import annotations

import json
import os
from pathlib import Path

from pv_corr_state_p0_runtime_append_stub_v1 import load_params


class ValidationError(RuntimeError):
    pass


def ensure_archive_only_run_allowed() -> None:
    if os.environ.get("ALLOW_ARCHIVE_ONLY_RUN") != "1":
        raise SystemExit(
            "ARCHIVE_ONLY: set ALLOW_ARCHIVE_ONLY_RUN=1 and use repo-first entry points under "
            "01_active_objects/ 02_runtime/ 04_active_main_docs/ before running this legacy validator."
        )


def expected_index_rows(params: dict[str, object]) -> list[str]:
    return [
        "pv_corr_state_p0_min_contract_v1.md",
        "pv_corr_state_p0_proof_of_mapping_v1.md",
        str(params["append_acceptance_file"]),
        str(params["bar_window_sample_acceptance_file"]),
        str(params["bar_window_mapping_acceptance_file"]),
        str(params["append_compatibility_acceptance_file"]),
        str(params["simulate_append_diff_acceptance_file"]),
        str(params["replay_preview_acceptance_file"]),
        str(params["replay_preview_acceptance_validation_file"]),
        str(params["replay_chain_acceptance_file"]),
    ]


def read_index_rows(chain_summary_md: Path) -> list[str]:
    rows: list[str] = []
    capture = False
    for raw_line in chain_summary_md.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.strip() == "## 历史链路索引":
            capture = True
            continue
        if capture:
            if line.startswith("  - `") and line.endswith("`"):
                rows.append(line.strip()[3:-1])
                continue
            if line.startswith("## "):
                break
    if not rows:
        raise ValidationError("chain summary markdown has no index rows")
    return rows


def main() -> None:
    ensure_archive_only_run_allowed()
    params = load_params()
    runtime_dir = Path(params["runtime_dir"])
    chain_summary_md = runtime_dir / params["chain_summary_index_file"]

    expected_rows = expected_index_rows(params)
    indexed_rows = read_index_rows(chain_summary_md)
    if indexed_rows != expected_rows:
        raise ValidationError(
            "chain summary index rows mismatch: indexed={0} expected={1}".format(
                indexed_rows, expected_rows
            )
        )

    print("validation_mode=chain_summary_acceptance_compare")
    print("chain_summary_md_exists={0}".format(chain_summary_md.exists()))
    print("indexed_stage_count={0}".format(len(indexed_rows)))
    print("expected_stage_count={0}".format(len(expected_rows)))
    print("rows_match=true")
    print("indexed_rows={0}".format(json.dumps(indexed_rows, ensure_ascii=True)))
    print("archive_only=true")
    print("path_policy=repo_first")
    print("write_attempted=false")
    print("chain_summary_acceptance_compare_passed=true")


if __name__ == "__main__":
    main()
