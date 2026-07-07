from __future__ import annotations

import json
import os
from pathlib import Path

from rsj_state_p0_runtime_append_stub_v1 import (
    assert_header_matches,
    load_params,
    read_rows as read_runtime_rows,
    remove_existing_proof_rows,
    remove_placeholder_rows,
)
from rsj_state_p0_validate_raw_window_mapping_v1 import (
    compute_rsjt_row,
    read_rows as read_sample_rows,
)
from rsj_state_p0_validate_replay_preview_acceptance_v1 import (
    read_acceptance_rows,
    read_preview_rows,
)


class ValidationError(RuntimeError):
    pass


def ensure_archive_only_run_allowed() -> None:
    if os.environ.get("ALLOW_ARCHIVE_ONLY_RUN") != "1":
        raise SystemExit(
            "ARCHIVE_ONLY: set ALLOW_ARCHIVE_ONLY_RUN=1 and use repo-first entry points under "
            "01_active_objects/ 02_runtime/ 04_active_main_docs/ before running this legacy validator."
        )


def main() -> None:
    ensure_archive_only_run_allowed()
    params = load_params()
    runtime_dir = Path(params["runtime_dir"])
    runtime_csv = runtime_dir / params["output_csv"]
    sample_csv = runtime_dir / params["raw_window_sample_input_csv"]
    preview_csv = runtime_dir / params["replay_preview_csv"]
    preview_acceptance_md = runtime_dir / params["replay_preview_acceptance_file"]

    assert_header_matches(runtime_csv)
    runtime_rows = read_runtime_rows(runtime_csv)
    runtime_rows = remove_placeholder_rows(
        runtime_rows, params["data_contract"]["placeholder_trade_id"]
    )

    sample_rows = read_sample_rows(sample_csv)
    if not sample_rows:
        raise ValidationError("sample csv has no data rows")

    mapped_rows = [compute_rsjt_row(row) for row in sample_rows]
    deduped_rows = remove_existing_proof_rows(runtime_rows[:], mapped_rows)
    appended_rows = [
        row
        for row in mapped_rows
        if row["trade_id"] not in {item["trade_id"] for item in deduped_rows}
    ]
    replay_rows = deduped_rows + mapped_rows

    preview_rows = read_preview_rows(preview_csv)
    acceptance_rows = read_acceptance_rows(preview_acceptance_md)
    expected_preview_rows = [
        ",".join([row[key] for key in row.keys()]) for row in appended_rows
    ]

    if preview_rows != expected_preview_rows:
        raise ValidationError(
            "preview csv does not match expected appended rows: preview={0} expected={1}".format(
                preview_rows, expected_preview_rows
            )
        )
    if acceptance_rows != preview_rows:
        raise ValidationError(
            "preview acceptance does not match preview csv: acceptance={0} preview={1}".format(
                acceptance_rows, preview_rows
            )
        )

    preview_trade_ids = [row["trade_id"] for row in appended_rows]
    print("validation_mode=archive_replay_chain_validation")
    print("runtime_csv_exists={0}".format(runtime_csv.exists()))
    print("sample_csv_exists={0}".format(sample_csv.exists()))
    print("preview_csv_exists={0}".format(preview_csv.exists()))
    print("preview_acceptance_md_exists={0}".format(preview_acceptance_md.exists()))
    print("runtime_row_count={0}".format(len(runtime_rows)))
    print("mapped_row_count={0}".format(len(mapped_rows)))
    print("appended_row_count={0}".format(len(appended_rows)))
    print("after_replay_row_count={0}".format(len(replay_rows)))
    print("preview_row_count={0}".format(len(preview_rows)))
    print("acceptance_row_count={0}".format(len(acceptance_rows)))
    print("preview_trade_ids={0}".format(json.dumps(preview_trade_ids, ensure_ascii=True)))
    print("rows_match=true")
    print("archive_only=true")
    print("path_policy=repo_first")
    print("write_attempted=false")
    print("archive_replay_chain_passed=true")


if __name__ == "__main__":
    main()
