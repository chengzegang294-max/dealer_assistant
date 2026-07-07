from __future__ import annotations

import csv
import json
import os
from collections import Counter
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
PARAMS_PATH = RUNTIME_DIR / "pv_corr_state_p0_runtime_params_template_v1.json"


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


def compute_mapping_row(row: dict[str, str], corr_threshold: float) -> dict[str, str]:
    trade_id = row["trade_id"].strip()

    try:
        window_bars = int(row["window_bars"].strip())
        pv_corr_score = float(row["pv_corr_score"].strip())
        price_net_change = float(row["price_net_change"].strip())
        volume_net_change = float(row["volume_net_change"].strip())
    except ValueError as exc:
        raise ValidationError(f"failed to parse numeric input for trade_id={trade_id}") from exc

    if window_bars <= 0:
        return {
            "trade_id": trade_id,
            "pv_sync_state": "unknown",
            "pv_pressure_bias": "unknown",
            "pv_extreme_flag": "unknown",
            "pv_model_state": "invalid",
            "proof_basis": "invalid_input_window",
        }

    same_direction = (price_net_change > 0 and volume_net_change > 0) or (
        price_net_change < 0 and volume_net_change < 0
    )
    opposite_direction = (price_net_change > 0 and volume_net_change < 0) or (
        price_net_change < 0 and volume_net_change > 0
    )

    if abs(pv_corr_score) < corr_threshold:
        pv_sync_state = "neutral"
        pv_pressure_bias = "none"
        proof_basis = "low_absolute_corr"
    elif same_direction:
        pv_sync_state = "confirm"
        if price_net_change > 0:
            pv_pressure_bias = "up_confirm"
            proof_basis = "strong_positive_corr_same_direction"
        else:
            pv_pressure_bias = "down_confirm"
            proof_basis = "strong_positive_corr_same_direction_down"
    elif opposite_direction:
        pv_sync_state = "diverge"
        pv_pressure_bias = "mixed"
        proof_basis = "strong_corr_opposite_direction"
    else:
        pv_sync_state = "unknown"
        pv_pressure_bias = "unknown"
        proof_basis = "sign_direction_unknown"

    if price_net_change > 0 and volume_net_change < 0:
        pv_extreme_flag = "price_up_volume_down"
    elif price_net_change < 0 and volume_net_change > 0:
        pv_extreme_flag = "price_down_volume_up"
    else:
        pv_extreme_flag = "none"

    return {
        "trade_id": trade_id,
        "pv_sync_state": pv_sync_state,
        "pv_pressure_bias": pv_pressure_bias,
        "pv_extreme_flag": pv_extreme_flag,
        "pv_model_state": "valid",
        "proof_basis": proof_basis,
    }


def main() -> None:
    ensure_archive_only_run_allowed()
    params = load_params()
    runtime_dir = Path(params["runtime_dir"])
    output_header = read_header(runtime_dir / params["header_file"])
    sample_csv = runtime_dir / params["bar_window_sample_input_csv"]
    rows = read_rows(sample_csv)
    if not rows:
        raise ValidationError("sample csv has no data rows")

    corr_threshold = float(params["pv_config"]["corr_threshold"])
    mapped_rows = [compute_mapping_row(row, corr_threshold) for row in rows]
    mapped_header = list(mapped_rows[0].keys())
    if mapped_header != output_header:
        raise ValidationError(
            "mapped header mismatch: expected={0} actual={1}".format(output_header, mapped_header)
        )

    model_states = Counter(row["pv_model_state"] for row in mapped_rows)
    sync_states = Counter(row["pv_sync_state"] for row in mapped_rows)

    print("mapping_mode=archive_history_to_append_ready")
    print("sample_csv_exists={0}".format(sample_csv.exists()))
    print("output_header_match=true")
    print("rows_mapped={0}".format(len(mapped_rows)))
    print("mapped_trade_ids={0}".format(json.dumps([row["trade_id"] for row in mapped_rows], ensure_ascii=True)))
    print("model_state_counts={0}".format(json.dumps(model_states, ensure_ascii=True, sort_keys=True)))
    print("pv_sync_state_counts={0}".format(json.dumps(sync_states, ensure_ascii=True, sort_keys=True)))
    print("archive_only=true")
    print("path_policy=repo_first")
    print("write_attempted=false")
    print("mapping_passed=true")


if __name__ == "__main__":
    main()
