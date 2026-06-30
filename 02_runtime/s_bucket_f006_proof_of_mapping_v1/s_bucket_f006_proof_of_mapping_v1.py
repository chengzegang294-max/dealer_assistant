from __future__ import annotations

import csv
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
REAL_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f006_proof_input_sample_v1.csv"
PROOF_OUTPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f006_proof_output_v1.csv"

REQUIRED_COLUMNS = [
    "sample_id",
    "object_id",
    "symbol",
    "timeframe",
    "daily_ohlcv_base",
    "industry_mv_neutralizer",
    "id2_std_3m_raw",
    "hml_r_std_5m_raw",
    "sample_note",
]

OUTPUT_COLUMNS = [
    "sample_id",
    "object_id",
    "symbol",
    "timeframe",
    "base_input_source",
    "neutralizer_source",
    "primary_factor_source",
    "secondary_factor_source",
    "primary_factor_output",
    "secondary_factor_output",
    "combo_output_column",
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
    if text is None:
        return False
    return bool(text.strip())


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
        base_ok = non_empty_text(row["daily_ohlcv_base"])
        neutralizer_ok = non_empty_text(row["industry_mv_neutralizer"])
        primary_ok = non_empty_numeric(row["id2_std_3m_raw"])
        secondary_ok = non_empty_numeric(row["hml_r_std_5m_raw"])
        mapping_status = "PASS" if base_ok and neutralizer_ok and primary_ok and secondary_ok else "FAIL"
        output_rows.append(
            {
                "sample_id": row["sample_id"],
                "object_id": row["object_id"],
                "symbol": row["symbol"],
                "timeframe": row["timeframe"],
                "base_input_source": "daily_ohlcv_base",
                "neutralizer_source": "industry_mv_neutralizer",
                "primary_factor_source": "id2_std_3m_raw",
                "secondary_factor_source": "hml_r_std_5m_raw",
                "primary_factor_output": "id2_std_3m_neutralized",
                "secondary_factor_output": "hml_r_std_5m_neutralized",
                "combo_output_column": "f006_two_factor_min_combo",
                "mapping_status": mapping_status,
                "proof_note": "mapping_only__neutralization_formula_not_implemented__verified_input_presence_for_f006_contract",
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
