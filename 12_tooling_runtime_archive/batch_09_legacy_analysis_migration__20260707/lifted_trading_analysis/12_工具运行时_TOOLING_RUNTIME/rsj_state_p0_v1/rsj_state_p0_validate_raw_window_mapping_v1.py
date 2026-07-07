from __future__ import annotations

import csv
import json
import os
from collections import Counter
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
PARAMS_PATH = RUNTIME_DIR / "rsj_state_p0_runtime_params_template_v1.json"


class ValidationError(RuntimeError):
    pass


def ensure_archive_only_run_allowed() -> None:
    if os.environ.get("ALLOW_ARCHIVE_ONLY_RUN") != "1":
        raise SystemExit(
            "ARCHIVE_ONLY: set ALLOW_ARCHIVE_ONLY_RUN=1 and use repo-first entry points under "
            "01_active_objects/ 02_runtime/ 04_active_main_docs/ before running this legacy validator."
        )


def load_params() -> dict:
    with PARAMS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_header(header_path: Path) -> list[str]:
    line = header_path.read_text(encoding="utf-8").strip()
    if not line:
        raise ValidationError("output header file is empty")
    return line.split(",")


def read_rows(sample_csv: Path) -> list[dict[str, str]]:
    with sample_csv.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def compute_rsjt_row(row: dict[str, str]) -> dict[str, str]:
    trade_id = row["trade_id"].strip()

    try:
        window_bars = int(row["window_bars"].strip())
        rv_up = float(row["rv_up"].strip())
        rv_down = float(row["rv_down"].strip())
    except ValueError as exc:
        raise ValidationError(f"failed to parse numeric input for trade_id={trade_id}") from exc

    if window_bars <= 0 or rv_up < 0 or rv_down < 0 or (rv_up + rv_down) <= 0:
        return {
            "trade_id": trade_id,
            "rsj_score": "unknown",
            "rsj_state": "unknown",
            "rsj_extreme_flag": "unknown",
            "rsj_timing_bias": "unknown",
            "rsj_model_state": "invalid",
            "proof_basis": "invalid_input_window",
        }

    rsj_score = (rv_up - rv_down) / (rv_up + rv_down)

    if rsj_score >= 0.20:
        rsj_state = "warm"
        rsj_timing_bias = "risk_on"
    elif rsj_score <= -0.20:
        rsj_state = "cold"
        rsj_timing_bias = "risk_off"
    else:
        rsj_state = "neutral"
        rsj_timing_bias = "wait"

    if rsj_score >= 0.50:
        rsj_extreme_flag = "extreme_high"
        proof_basis = "rv_up_gt_rv_down_strong"
    elif rsj_score <= -0.50:
        rsj_extreme_flag = "extreme_low"
        proof_basis = "rv_down_gt_rv_up_strong"
    else:
        rsj_extreme_flag = "none"
        if rsj_state == "warm":
            proof_basis = "rv_up_gt_rv_down"
        elif rsj_state == "cold":
            proof_basis = "rv_down_gt_rv_up"
        else:
            proof_basis = "balanced_window"

    return {
        "trade_id": trade_id,
        "rsj_score": "{0:.4f}".format(rsj_score),
        "rsj_state": rsj_state,
        "rsj_extreme_flag": rsj_extreme_flag,
        "rsj_timing_bias": rsj_timing_bias,
        "rsj_model_state": "valid",
        "proof_basis": proof_basis,
    }


def main() -> None:
    ensure_archive_only_run_allowed()
    params = load_params()
    runtime_dir = Path(params["runtime_dir"])
    output_header = read_header(runtime_dir / params["header_file"])
    sample_csv = runtime_dir / params["raw_window_sample_input_csv"]
    rows = read_rows(sample_csv)
    if not rows:
        raise ValidationError("sample csv has no data rows")

    mapped_rows = [compute_rsjt_row(row) for row in rows]
    mapped_header = list(mapped_rows[0].keys())
    if mapped_header != output_header:
        raise ValidationError(
            "mapped header mismatch: expected={0} actual={1}".format(output_header, mapped_header)
        )

    model_states = Counter(row["rsj_model_state"] for row in mapped_rows)
    rsj_states = Counter(row["rsj_state"] for row in mapped_rows)

    print("mapping_mode=archive_history_to_append_ready")
    print("sample_csv_exists={0}".format(sample_csv.exists()))
    print("output_header_match=true")
    print("rows_mapped={0}".format(len(mapped_rows)))
    print("mapped_trade_ids={0}".format(json.dumps([row["trade_id"] for row in mapped_rows], ensure_ascii=True)))
    print("model_state_counts={0}".format(json.dumps(model_states, ensure_ascii=True, sort_keys=True)))
    print("rsj_state_counts={0}".format(json.dumps(rsj_states, ensure_ascii=True, sort_keys=True)))
    print("archive_only=true")
    print("path_policy=repo_first")
    print("write_attempted=false")
    print("mapping_passed=true")


if __name__ == "__main__":
    main()
