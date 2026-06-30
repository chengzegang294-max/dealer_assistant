from __future__ import annotations

import csv
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
REAL_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f012_proof_input_sample_v1.csv"
PROOF_OUTPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f012_proof_output_v1.csv"

REQUIRED_COLUMNS = [
    "sample_id",
    "object_id",
    "stock_pool_scope",
    "label_scheme_input",
    "xgboost_mode_input",
    "random_seed_batch_input",
    "benchmark_scope_input",
    "neutralization_scope_input",
    "sample_note",
]

OUTPUT_COLUMNS = [
    "sample_id",
    "object_id",
    "stock_pool_scope",
    "label_scheme_scope",
    "xgbr_combine_flag",
    "random_seed_stability_flag",
    "future_leakage_guard_flag",
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
                non_empty_text(row["label_scheme_input"]),
                non_empty_text(row["xgboost_mode_input"]),
                non_empty_text(row["random_seed_batch_input"]),
                non_empty_text(row["benchmark_scope_input"]),
                non_empty_text(row["neutralization_scope_input"]),
            ]
        )
        mapping_status = "PASS" if text_ok else "FAIL"

        if mapping_status == "PASS":
            label_scheme = row["label_scheme_input"].strip().lower()
            xgboost_mode = row["xgboost_mode_input"].strip().lower()
            seed_batch = row["random_seed_batch_input"].strip().lower()
            benchmark_scope = row["benchmark_scope_input"].strip().lower()

            label_scheme_scope = "f012_label_scope__{0}".format(label_scheme)
            xgbr_combine_flag = str(xgboost_mode == "xgbr_combine").lower()
            random_seed_stability_flag = str("100" in seed_batch).lower()
            future_leakage_guard_flag = str("csi500" in benchmark_scope).lower()
        else:
            label_scheme_scope = "missing_required_input"
            xgbr_combine_flag = "missing_required_input"
            random_seed_stability_flag = "missing_required_input"
            future_leakage_guard_flag = "missing_required_input"

        output_rows.append(
            {
                "sample_id": row["sample_id"],
                "object_id": row["object_id"],
                "stock_pool_scope": row["stock_pool_scope"],
                "label_scheme_scope": label_scheme_scope,
                "xgbr_combine_flag": xgbr_combine_flag,
                "random_seed_stability_flag": random_seed_stability_flag,
                "future_leakage_guard_flag": future_leakage_guard_flag,
                "mapping_status": mapping_status,
                "proof_note": (
                    "supporting_mapping_only__demo_labeling_contract_not_universal_best_label_claim__"
                    "verified_input_presence_for_f012_contract"
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
