from __future__ import annotations

import csv
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
REAL_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f009_proof_input_sample_v1.csv"
PROOF_OUTPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f009_proof_output_v1.csv"

REQUIRED_COLUMNS = [
    "sample_id",
    "object_id",
    "symbol",
    "quarter_end",
    "excess_return_input",
    "large_order_buy_ratio_input",
    "net_main_buy_ratio_input",
    "prior_holding_change_input",
    "high_holding_bucket_input",
    "disclosure_lag_days",
    "sample_note",
]

OUTPUT_COLUMNS = [
    "sample_id",
    "object_id",
    "symbol",
    "quarter_end",
    "holding_change_estimate_signal",
    "style_deviation_monitor_flag",
    "high_holding_strength_flag",
    "low_freq_cross_check_flag",
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


def non_empty_numeric(text: str) -> bool:
    if text is None:
        return False
    text = text.strip()
    if not text:
        return False
    float(text)
    return True


def non_empty_text(text: str) -> bool:
    return bool(text and text.strip())


def build_output_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output_rows: list[dict[str, str]] = []
    for row in rows:
        numeric_ok = all(
            [
                non_empty_numeric(row["excess_return_input"]),
                non_empty_numeric(row["large_order_buy_ratio_input"]),
                non_empty_numeric(row["net_main_buy_ratio_input"]),
                non_empty_numeric(row["prior_holding_change_input"]),
                non_empty_numeric(row["disclosure_lag_days"]),
            ]
        )
        text_ok = non_empty_text(row["high_holding_bucket_input"])
        mapping_status = "PASS" if numeric_ok and text_ok else "FAIL"

        if mapping_status == "PASS":
            excess_return = float(row["excess_return_input"])
            large_order_buy_ratio = float(row["large_order_buy_ratio_input"])
            net_main_buy_ratio = float(row["net_main_buy_ratio_input"])
            prior_holding_change = float(row["prior_holding_change_input"])
            lag_days = float(row["disclosure_lag_days"])
            high_holding_bucket = row["high_holding_bucket_input"].strip().lower()

            if (
                high_holding_bucket == "high_holding"
                and large_order_buy_ratio >= 0.25
                and net_main_buy_ratio >= 0.15
            ):
                holding_change_estimate_signal = "f009_holding_change_estimate__strong"
                high_holding_strength_flag = "true"
            else:
                holding_change_estimate_signal = "f009_holding_change_estimate__weak"
                high_holding_strength_flag = "false"

            style_deviation_monitor_flag = str(
                excess_return >= 0.08 and prior_holding_change >= 0.05
            ).lower()
            low_freq_cross_check_flag = str(
                lag_days <= 15 and high_holding_bucket == "high_holding"
            ).lower()
        else:
            holding_change_estimate_signal = "missing_required_input"
            style_deviation_monitor_flag = "missing_required_input"
            high_holding_strength_flag = "missing_required_input"
            low_freq_cross_check_flag = "missing_required_input"

        output_rows.append(
            {
                "sample_id": row["sample_id"],
                "object_id": row["object_id"],
                "symbol": row["symbol"],
                "quarter_end": row["quarter_end"],
                "holding_change_estimate_signal": holding_change_estimate_signal,
                "style_deviation_monitor_flag": style_deviation_monitor_flag,
                "high_holding_strength_flag": high_holding_strength_flag,
                "low_freq_cross_check_flag": low_freq_cross_check_flag,
                "mapping_status": mapping_status,
                "proof_note": (
                    "supporting_mapping_only__demo_holding_inference_thresholds_not_real_prediction_logic__"
                    "verified_input_presence_for_f009_contract"
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
