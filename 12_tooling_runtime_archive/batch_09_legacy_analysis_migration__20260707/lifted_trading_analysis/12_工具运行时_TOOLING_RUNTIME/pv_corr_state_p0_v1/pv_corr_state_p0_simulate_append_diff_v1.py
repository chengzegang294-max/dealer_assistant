from __future__ import annotations

import json
import os
from pathlib import Path

from pv_corr_state_p0_runtime_append_stub_v1 import (
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
    runtime_rows = remove_placeholder_rows(runtime_rows, params["data_contract"]["placeholder_trade_id"])
    sample_rows = read_sample_rows(sample_csv)
    if not sample_rows:
        raise ValidationError("sample csv has no data rows")

    corr_threshold = float(params["pv_config"]["corr_threshold"])
    mapped_rows = [compute_mapping_row(row, corr_threshold) for row in sample_rows]
    before_trade_ids = [row["trade_id"] for row in runtime_rows]
    mapped_trade_ids = [row["trade_id"] for row in mapped_rows]
    overlapping_trade_ids = sorted(set(before_trade_ids) & set(mapped_trade_ids))

    deduped_rows = remove_existing_proof_rows(runtime_rows[:], mapped_rows)
    after_dedupe_trade_ids = [row["trade_id"] for row in deduped_rows]
    replay_rows = deduped_rows + mapped_rows
    after_replay_trade_ids = [row["trade_id"] for row in replay_rows]
    newly_appended_trade_ids = [trade_id for trade_id in after_replay_trade_ids if trade_id not in before_trade_ids]
    removed_trade_ids = [trade_id for trade_id in before_trade_ids if trade_id not in after_dedupe_trade_ids]

    print("replay_mode=archive_simulate_append_diff")
    print("runtime_csv_exists={0}".format(csv_path.exists()))
    print("sample_csv_exists={0}".format(sample_csv.exists()))
    print("before_row_count={0}".format(len(before_trade_ids)))
    print("mapped_row_count={0}".format(len(mapped_trade_ids)))
    print("after_replay_row_count={0}".format(len(after_replay_trade_ids)))
    print("before_trade_ids={0}".format(json.dumps(before_trade_ids, ensure_ascii=True)))
    print("mapped_trade_ids={0}".format(json.dumps(mapped_trade_ids, ensure_ascii=True)))
    print("overlapping_trade_ids={0}".format(json.dumps(overlapping_trade_ids, ensure_ascii=True)))
    print("removed_trade_ids={0}".format(json.dumps(removed_trade_ids, ensure_ascii=True)))
    print("newly_appended_trade_ids={0}".format(json.dumps(newly_appended_trade_ids, ensure_ascii=True)))
    print(
        "first_replay_append_row={0}".format(
            json.dumps(mapped_rows[0], ensure_ascii=True, sort_keys=True)
        )
    )
    print("archive_only=true")
    print("path_policy=repo_first")
    print("write_attempted=false")
    print("archive_replay_passed=true")


if __name__ == "__main__":
    main()
