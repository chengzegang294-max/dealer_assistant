from __future__ import annotations

import csv
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
REAL_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f004_proof_input_sample_v1.csv"
PROOF_OUTPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f004_proof_output_v1.csv"

REQUIRED_COLUMNS = [
    "sample_id",
    "object_id",
    "training_window_label",
    "monthly_factor_pool_input",
    "annual_rolling_window_input",
    "group_time_series_split_input",
    "base_model_input",
    "frequency_scope_input",
    "sample_note",
]

OUTPUT_COLUMNS = [
    "sample_id",
    "object_id",
    "training_window_label",
    "cv_protocol_decision",
    "leakage_control_flag",
    "underfit_risk_flag",
    "method_scope_label",
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


def build_output_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output_rows: list[dict[str, str]] = []
    for row in rows:
        text_ok = all(
            [
                non_empty_text(row["monthly_factor_pool_input"]),
                non_empty_text(row["annual_rolling_window_input"]),
                non_empty_text(row["group_time_series_split_input"]),
                non_empty_text(row["base_model_input"]),
                non_empty_text(row["frequency_scope_input"]),
            ]
        )
        mapping_status = "PASS" if text_ok else "FAIL"

        if mapping_status == "PASS":
            frequency_scope = row["frequency_scope_input"].strip().lower()
            base_model = row["base_model_input"].strip().lower()

            cv_protocol_decision = "f004_cv_protocol__group_time_series_split"
            leakage_control_flag = "true"
            underfit_risk_flag = str(base_model in {"logistic_regression", "xgboost"}).lower()
            if frequency_scope == "monthly":
                method_scope_label = "f004_method_scope__monthly_supported"
            else:
                method_scope_label = "f004_method_scope__cross_frequency_review_required"
        else:
            cv_protocol_decision = "missing_required_input"
            leakage_control_flag = "missing_required_input"
            underfit_risk_flag = "missing_required_input"
            method_scope_label = "missing_required_input"

        output_rows.append(
            {
                "sample_id": row["sample_id"],
                "object_id": row["object_id"],
                "training_window_label": row["training_window_label"],
                "cv_protocol_decision": cv_protocol_decision,
                "leakage_control_flag": leakage_control_flag,
                "underfit_risk_flag": underfit_risk_flag,
                "method_scope_label": method_scope_label,
                "mapping_status": mapping_status,
                "proof_note": (
                    "supporting_mapping_only__demo_training_protocol_not_real_model_pipeline__"
                    "verified_input_presence_for_f004_contract"
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
