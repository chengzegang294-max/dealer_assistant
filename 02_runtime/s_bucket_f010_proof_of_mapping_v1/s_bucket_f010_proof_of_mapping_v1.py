from __future__ import annotations

import csv
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
REAL_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f010_proof_input_sample_v1.csv"
PROOF_OUTPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f010_proof_output_v1.csv"

REQUIRED_COLUMNS = [
    "sample_id",
    "object_id",
    "symbol",
    "trading_date",
    "snapshot_3s_input",
    "order_queue_input",
    "dft_volume_signal_input",
    "peak_ratio_input",
    "b_plus_s_input",
    "b_minus_s_input",
    "b_div_s_input",
    "sample_note",
]

OUTPUT_COLUMNS = [
    "sample_id",
    "object_id",
    "symbol",
    "trading_date",
    "b_plus_s_monitor_signal",
    "b_minus_s_stability_flag",
    "b_div_s_direction_flag",
    "f009_cross_check_ready_flag",
    "mapping_status",
    "proof_note",
]


def load_rows() -> list[dict[str, str]]:
    with REAL_INPUT_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("real_input_csv is empty")
    missing = [column for column in REQUIRED_COLUMNS if column not in rows[0]]
    if missing:
        raise ValueError("missing required columns: {0}".format(", ".join(missing)))
    return rows


def non_empty_text(text: str) -> bool:
    return bool(text and text.strip())


def non_empty_numeric(text: str) -> bool:
    if text is None:
        return False
    text = text.strip()
    if not text:
        return False
    float(text)
    return True


def build_output_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output_rows: list[dict[str, str]] = []
    for row in rows:
        text_ok = all(
            [
                non_empty_text(row["snapshot_3s_input"]),
                non_empty_text(row["order_queue_input"]),
            ]
        )
        numeric_ok = all(
            [
                non_empty_numeric(row["dft_volume_signal_input"]),
                non_empty_numeric(row["peak_ratio_input"]),
                non_empty_numeric(row["b_plus_s_input"]),
                non_empty_numeric(row["b_minus_s_input"]),
                non_empty_numeric(row["b_div_s_input"]),
            ]
        )
        mapping_status = "PASS" if text_ok and numeric_ok else "FAIL"

        if mapping_status == "PASS":
            peak_ratio = float(row["peak_ratio_input"])
            b_plus_s = float(row["b_plus_s_input"])
            b_minus_s = float(row["b_minus_s_input"])
            b_div_s = float(row["b_div_s_input"])

            if b_plus_s >= 0.60:
                b_plus_s_monitor_signal = "f010_b_plus_s_monitor__observe_negative_correlation"
            else:
                b_plus_s_monitor_signal = "f010_b_plus_s_monitor__weak_activity"

            b_minus_s_stability_flag = str(b_minus_s >= 0.50).lower()
            b_div_s_direction_flag = str(b_div_s >= 1.00 and peak_ratio >= 0.40).lower()
            f009_cross_check_ready_flag = str(
                b_div_s_direction_flag == "true" or b_minus_s_stability_flag == "true"
            ).lower()
        else:
            b_plus_s_monitor_signal = "missing_required_input"
            b_minus_s_stability_flag = "missing_required_input"
            b_div_s_direction_flag = "missing_required_input"
            f009_cross_check_ready_flag = "missing_required_input"

        output_rows.append(
            {
                "sample_id": row["sample_id"],
                "object_id": row["object_id"],
                "symbol": row["symbol"],
                "trading_date": row["trading_date"],
                "b_plus_s_monitor_signal": b_plus_s_monitor_signal,
                "b_minus_s_stability_flag": b_minus_s_stability_flag,
                "b_div_s_direction_flag": b_div_s_direction_flag,
                "f009_cross_check_ready_flag": f009_cross_check_ready_flag,
                "mapping_status": mapping_status,
                "proof_note": (
                    "supporting_mapping_only__demo_institution_monitor_thresholds_not_real_signal_logic__"
                    "verified_input_presence_for_f010_contract"
                ),
            }
        )
    return output_rows


def write_rows(rows: list[dict[str, str]]) -> None:
    with PROOF_OUTPUT_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    input_rows = load_rows()
    output_rows = build_output_rows(input_rows)
    write_rows(output_rows)
    print("proof_output_path={0}".format(PROOF_OUTPUT_PATH))
    print("row_count={0}".format(len(output_rows)))


if __name__ == "__main__":
    main()
