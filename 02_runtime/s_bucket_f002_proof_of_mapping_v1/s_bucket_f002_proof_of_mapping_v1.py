from __future__ import annotations

import csv
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
REAL_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f002_proof_input_sample_v1.csv"
PROOF_OUTPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f002_proof_output_v1.csv"

REQUIRED_COLUMNS = [
    "sample_id",
    "object_id",
    "symbol",
    "timeframe",
    "return_quantile_input",
    "active_trade_ratio_input",
    "sample_note",
]

OUTPUT_COLUMNS = [
    "sample_id",
    "object_id",
    "symbol",
    "timeframe",
    "short_filter_output",
    "long_short_filter_output",
    "guard_decision_output",
    "residualize_required_flag",
    "long_only_block_flag",
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


def build_guard_outputs(return_quantile: float, active_trade_ratio: float) -> tuple[str, str, str, str]:
    short_filter_output = "f002_short_filter_signal__mapped"
    long_short_filter_output = "f002_long_short_filter_signal__mapped"

    if return_quantile <= 0.35 or active_trade_ratio <= 0.30:
        guard_decision_output = "f002_guard_decision__short_only_preferred"
    else:
        guard_decision_output = "f002_guard_decision__long_short_filter_allowed"

    residualize_required_flag = str(
        return_quantile >= 0.75 or active_trade_ratio >= 0.70
    ).lower()
    return (
        short_filter_output,
        long_short_filter_output,
        guard_decision_output,
        residualize_required_flag,
    )


def build_output_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output_rows: list[dict[str, str]] = []
    for row in rows:
        return_ok = non_empty_numeric(row["return_quantile_input"])
        active_ok = non_empty_numeric(row["active_trade_ratio_input"])
        mapping_status = "PASS" if return_ok and active_ok else "FAIL"

        if mapping_status == "PASS":
            guard_outputs = build_guard_outputs(
                float(row["return_quantile_input"]),
                float(row["active_trade_ratio_input"]),
            )
            short_filter_output, long_short_filter_output, guard_decision_output, residualize_required_flag = guard_outputs
        else:
            short_filter_output = "missing_required_input"
            long_short_filter_output = "missing_required_input"
            guard_decision_output = "missing_required_input"
            residualize_required_flag = "missing_required_input"

        output_rows.append(
            {
                "sample_id": row["sample_id"],
                "object_id": row["object_id"],
                "symbol": row["symbol"],
                "timeframe": row["timeframe"],
                "short_filter_output": short_filter_output,
                "long_short_filter_output": long_short_filter_output,
                "guard_decision_output": guard_decision_output,
                "residualize_required_flag": residualize_required_flag,
                "long_only_block_flag": "true",
                "mapping_status": mapping_status,
                "proof_note": (
                    "mapping_only__demo_guard_thresholds_not_real_trading_logic__"
                    "verified_input_presence_for_f002_contract"
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
