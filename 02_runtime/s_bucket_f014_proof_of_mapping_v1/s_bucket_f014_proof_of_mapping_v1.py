from __future__ import annotations

import csv
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
REAL_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f014_proof_input_sample_v1.csv"
PROOF_OUTPUT_PATH = RUNTIME_DIR / "real_input_samples" / "f014_proof_output_v1.csv"

REQUIRED_COLUMNS = [
    "sample_id",
    "object_id",
    "symbol",
    "timeframe",
    "turnover_proxy",
    "momentum_proxy",
    "mfd_sellord_raw",
    "mfd_volinflowrate_open_m_raw",
    "sample_note",
]

OUTPUT_COLUMNS = [
    "sample_id",
    "object_id",
    "symbol",
    "timeframe",
    "turnover_proxy_present",
    "momentum_proxy_present",
    "primary_component_source",
    "secondary_component_source",
    "residualize_target_columns",
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
        turnover_ok = non_empty_numeric(row["turnover_proxy"])
        momentum_ok = non_empty_numeric(row["momentum_proxy"])
        primary_ok = non_empty_numeric(row["mfd_sellord_raw"])
        secondary_ok = non_empty_numeric(row["mfd_volinflowrate_open_m_raw"])
        mapping_status = "PASS" if turnover_ok and momentum_ok and primary_ok and secondary_ok else "FAIL"
        proof_note = (
            "mapping_only__residualize_formula_not_implemented__"
            "verified_input_presence_for_f014_contract"
        )
        output_rows.append(
            {
                "sample_id": row["sample_id"],
                "object_id": row["object_id"],
                "symbol": row["symbol"],
                "timeframe": row["timeframe"],
                "turnover_proxy_present": str(turnover_ok).lower(),
                "momentum_proxy_present": str(momentum_ok).lower(),
                "primary_component_source": "mfd_sellord_raw",
                "secondary_component_source": "mfd_volinflowrate_open_m_raw",
                "residualize_target_columns": "mfd_sellord_resid_tm|mfd_volinflowrate_open_m_resid_tm",
                "combo_output_column": "f014_two_factor_min_combo",
                "mapping_status": mapping_status,
                "proof_note": proof_note,
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
