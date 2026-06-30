from __future__ import annotations

import csv
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
REAL_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f007_proof_input_sample_v1.csv"
PROOF_OUTPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f007_proof_output_v1.csv"

REQUIRED_COLUMNS = [
    "sample_id",
    "object_id",
    "quarter_end",
    "disclosure_lag_days",
    "fund_top10_holdings_input",
    "fund_quality_bucket_input",
    "barra_style_regime_input",
    "fund_size_bucket_input",
    "delta_to_float_ashare_input",
    "sample_note",
]

OUTPUT_COLUMNS = [
    "sample_id",
    "object_id",
    "quarter_end",
    "style_match_flag",
    "small_fund_exclusion_flag",
    "holding_feature_signal",
    "filter_pool_decision",
    "weight_constraint_bucket",
    "cross_check_ready_flag",
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
                non_empty_text(row["fund_top10_holdings_input"]),
                non_empty_text(row["fund_quality_bucket_input"]),
                non_empty_text(row["barra_style_regime_input"]),
                non_empty_text(row["fund_size_bucket_input"]),
            ]
        )
        numeric_ok = all(
            [
                non_empty_numeric(row["disclosure_lag_days"]),
                non_empty_numeric(row["delta_to_float_ashare_input"]),
            ]
        )
        mapping_status = "PASS" if text_ok and numeric_ok else "FAIL"

        if mapping_status == "PASS":
            lag_days = float(row["disclosure_lag_days"])
            delta_to_float = float(row["delta_to_float_ashare_input"])
            fund_quality = row["fund_quality_bucket_input"].strip().lower()
            style_regime = row["barra_style_regime_input"].strip().lower()
            fund_size = row["fund_size_bucket_input"].strip().lower()

            style_match_flag = str(
                "2017_plus" in style_regime or "2017_minus" in style_regime
            ).lower()
            small_fund_exclusion_flag = str("small_fund" in fund_size).lower()
            holding_feature_signal = (
                "delta_to_float_ashare_supporting_positive"
                if delta_to_float >= 0.10
                else "delta_to_float_ashare_supporting_weak"
            )

            if (
                lag_days <= 15
                and "top20" in fund_quality
                and small_fund_exclusion_flag == "false"
            ):
                filter_pool_decision = "f007_filter_pool__style_match_required"
                weight_constraint_bucket = "f007_weight_constraint__eligible"
            else:
                filter_pool_decision = "f007_filter_pool__observe_only"
                weight_constraint_bucket = "f007_weight_constraint__blocked"

            cross_check_ready_flag = str(
                lag_days <= 15 and style_match_flag == "true"
            ).lower()
        else:
            style_match_flag = "missing_required_input"
            small_fund_exclusion_flag = "missing_required_input"
            holding_feature_signal = "missing_required_input"
            filter_pool_decision = "missing_required_input"
            weight_constraint_bucket = "missing_required_input"
            cross_check_ready_flag = "missing_required_input"

        output_rows.append(
            {
                "sample_id": row["sample_id"],
                "object_id": row["object_id"],
                "quarter_end": row["quarter_end"],
                "style_match_flag": style_match_flag,
                "small_fund_exclusion_flag": small_fund_exclusion_flag,
                "holding_feature_signal": holding_feature_signal,
                "filter_pool_decision": filter_pool_decision,
                "weight_constraint_bucket": weight_constraint_bucket,
                "cross_check_ready_flag": cross_check_ready_flag,
                "mapping_status": mapping_status,
                "proof_note": (
                    "supporting_mapping_only__demo_style_boundary_not_real_portfolio_logic__"
                    "verified_input_presence_for_f007_contract"
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
