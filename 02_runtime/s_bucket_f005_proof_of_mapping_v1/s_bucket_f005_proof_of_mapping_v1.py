from __future__ import annotations

import csv
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
REAL_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f005_proof_input_sample_v1.csv"
PROOF_OUTPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f005_proof_output_v1.csv"

REQUIRED_COLUMNS = [
    "sample_id",
    "object_id",
    "universe_scope",
    "raw_ohlcv_universe_input",
    "genetic_programming_factor_input",
    "random_forest_selection_input",
    "shap_explanation_input",
    "neutralization_scope_input",
    "sample_note",
]

OUTPUT_COLUMNS = [
    "sample_id",
    "object_id",
    "universe_scope",
    "factor_mining_stage",
    "feature_selection_stage",
    "explanation_stage",
    "blueprint_scope_label",
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
                non_empty_text(row["raw_ohlcv_universe_input"]),
                non_empty_text(row["genetic_programming_factor_input"]),
                non_empty_text(row["random_forest_selection_input"]),
                non_empty_text(row["shap_explanation_input"]),
                non_empty_text(row["neutralization_scope_input"]),
            ]
        )
        mapping_status = "PASS" if text_ok else "FAIL"

        if mapping_status == "PASS":
            neutralization_scope = row["neutralization_scope_input"].strip().lower()
            factor_mining_stage = "f005_stage__genetic_programming_factor_mining"
            feature_selection_stage = "f005_stage__random_forest_feature_selection"
            explanation_stage = "f005_stage__shap_explainability"
            if "industry_mv_neutralization" in neutralization_scope:
                blueprint_scope_label = "f005_blueprint_scope__needs_downstream_portfolio_layer"
            else:
                blueprint_scope_label = "f005_blueprint_scope__review_required"
        else:
            factor_mining_stage = "missing_required_input"
            feature_selection_stage = "missing_required_input"
            explanation_stage = "missing_required_input"
            blueprint_scope_label = "missing_required_input"

        output_rows.append(
            {
                "sample_id": row["sample_id"],
                "object_id": row["object_id"],
                "universe_scope": row["universe_scope"],
                "factor_mining_stage": factor_mining_stage,
                "feature_selection_stage": feature_selection_stage,
                "explanation_stage": explanation_stage,
                "blueprint_scope_label": blueprint_scope_label,
                "mapping_status": mapping_status,
                "proof_note": (
                    "supporting_mapping_only__demo_blueprint_stage_linkage_not_real_end_to_end_system__"
                    "verified_input_presence_for_f005_contract"
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
