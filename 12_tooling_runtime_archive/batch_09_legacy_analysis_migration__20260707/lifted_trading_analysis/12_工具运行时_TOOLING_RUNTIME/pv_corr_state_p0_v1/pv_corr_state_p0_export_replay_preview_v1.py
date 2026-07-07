from __future__ import annotations

import csv
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
            "01_active_objects/ 02_runtime/ 04_active_main_docs/ before running this legacy exporter."
        )


def write_rows(csv_path: Path, rows: list[dict[str, str]]) -> None:
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ensure_archive_only_run_allowed()
    params = load_params()
    runtime_dir = Path(params["runtime_dir"])
    runtime_csv = runtime_dir / params["output_csv"]
    sample_csv = runtime_dir / params["bar_window_sample_input_csv"]
    preview_csv = runtime_dir / params["replay_preview_csv"]

    assert_header_matches(runtime_csv)
    runtime_rows = read_rows(runtime_csv)
    runtime_rows = remove_placeholder_rows(runtime_rows, params["data_contract"]["placeholder_trade_id"])

    sample_rows = read_sample_rows(sample_csv)
    if not sample_rows:
        raise ValidationError("sample csv has no data rows")

    corr_threshold = float(params["pv_config"]["corr_threshold"])
    mapped_rows = [compute_mapping_row(row, corr_threshold) for row in sample_rows]
    deduped_rows = remove_existing_proof_rows(runtime_rows[:], mapped_rows)
    before_trade_ids = [row["trade_id"] for row in runtime_rows]
    appended_rows = [row for row in mapped_rows if row["trade_id"] not in {item["trade_id"] for item in deduped_rows}]
    replay_rows = deduped_rows + mapped_rows

    if list(mapped_rows[0].keys()) != CSV_COLUMNS:
        raise ValidationError("mapped row keys do not match CSV columns")

    write_rows(preview_csv, appended_rows)

    print("preview_mode=archive_replay_preview_export")
    print("runtime_csv_exists={0}".format(runtime_csv.exists()))
    print("sample_csv_exists={0}".format(sample_csv.exists()))
    print("preview_csv={0}".format(preview_csv.name))
    print("before_row_count={0}".format(len(before_trade_ids)))
    print("preview_row_count={0}".format(len(appended_rows)))
    print("after_replay_row_count={0}".format(len(replay_rows)))
    print(
        "preview_trade_ids={0}".format(
            json.dumps([row["trade_id"] for row in appended_rows], ensure_ascii=True)
        )
    )
    print(
        "first_preview_row={0}".format(
            json.dumps(appended_rows[0], ensure_ascii=True, sort_keys=True)
        )
    )
    print("archive_only=true")
    print("path_policy=repo_first")
    print("runtime_write_attempted=false")
    print("archive_preview_export_passed=true")


if __name__ == "__main__":
    main()
