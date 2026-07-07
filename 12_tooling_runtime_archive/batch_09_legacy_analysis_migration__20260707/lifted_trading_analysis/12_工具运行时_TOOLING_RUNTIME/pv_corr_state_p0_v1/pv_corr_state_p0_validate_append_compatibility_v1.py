from __future__ import annotations

import json
import os
from pathlib import Path

from pv_corr_state_p0_runtime_append_stub_v1 import (
    CSV_COLUMNS,
    assert_header_matches,
    load_params,
    read_rows,
    remove_existing_proof_rows,
    remove_placeholder_rows,
)
from pv_corr_state_p0_validate_bar_window_mapping_v1 import (
    compute_mapping_row,
    read_rows as read_sample_rows,
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
    csv_path = runtime_dir / params["output_csv"]
    sample_csv = runtime_dir / params["bar_window_sample_input_csv"]

    assert_header_matches(csv_path)
    runtime_rows = read_rows(csv_path)
    original_row_count = len(runtime_rows)

    sample_rows = read_sample_rows(sample_csv)
    if not sample_rows:
        raise ValidationError("sample csv has no data rows")

    corr_threshold = float(params["pv_config"]["corr_threshold"])
    mapped_rows = [compute_mapping_row(row, corr_threshold) for row in sample_rows]
    for index, row in enumerate(mapped_rows, start=1):
        if list(row.keys()) != CSV_COLUMNS:
            raise ValidationError(
                "mapped row {0} keys mismatch: expected={1} actual={2}".format(
                    index, CSV_COLUMNS, list(row.keys())
                )
            )

    runtime_rows = remove_placeholder_rows(runtime_rows, params["data_contract"]["placeholder_trade_id"])
    rows_before_append = len(runtime_rows)
    runtime_rows = remove_existing_proof_rows(runtime_rows, mapped_rows)
    rows_after_dedupe = len(runtime_rows)
    runtime_rows.extend(mapped_rows)

    print("compatibility_mode=archive_history_to_append_stub")
    print("runtime_csv_exists={0}".format(csv_path.exists()))
    print("sample_csv_exists={0}".format(sample_csv.exists()))
    print("append_header_match=true")
    print("rows_before_cleanup={0}".format(original_row_count))
    print("mapped_rows_loaded={0}".format(len(mapped_rows)))
    print("rows_before_append={0}".format(rows_before_append))
    print("rows_after_dedupe={0}".format(rows_after_dedupe))
    print("rows_after_append={0}".format(len(runtime_rows)))
    print(
        "mapped_trade_ids={0}".format(
            json.dumps([row["trade_id"] for row in mapped_rows], ensure_ascii=True)
        )
    )
    print(
        "first_compat_row={0}".format(
            json.dumps(mapped_rows[0], ensure_ascii=True, sort_keys=True)
        )
    )
    print("archive_only=true")
    print("path_policy=repo_first")
    print("write_attempted=false")
    print("compatibility_passed=true")


if __name__ == "__main__":
    main()
