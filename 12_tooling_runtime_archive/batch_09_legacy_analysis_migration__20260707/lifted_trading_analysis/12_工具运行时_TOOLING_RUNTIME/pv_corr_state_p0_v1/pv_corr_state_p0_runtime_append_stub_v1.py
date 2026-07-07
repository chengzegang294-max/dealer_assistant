from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
PARAMS_PATH = RUNTIME_DIR / "pv_corr_state_p0_runtime_params_template_v1.json"

CSV_COLUMNS = [
    "trade_id",
    "pv_sync_state",
    "pv_pressure_bias",
    "pv_extreme_flag",
    "pv_model_state",
    "proof_basis",
]


def load_params() -> dict:
    with PARAMS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def ensure_archive_only_run_allowed() -> None:
    if os.environ.get("ALLOW_ARCHIVE_ONLY_RUN") != "1":
        raise SystemExit(
            "ARCHIVE_ONLY: set ALLOW_ARCHIVE_ONLY_RUN=1 and use repo-first entry points under "
            "01_active_objects/ 02_runtime/ 04_active_main_docs/ before running this legacy stub."
        )


def resolve_runtime_paths(params: dict) -> tuple[Path, Path]:
    runtime_dir = Path(params["runtime_dir"])
    csv_path = runtime_dir / params["output_csv"]
    proof_path = runtime_dir / params["proof_output_csv"]
    return csv_path, proof_path


def assert_header_matches(csv_path: Path) -> None:
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        header = next(csv.reader(f))
    if header != CSV_COLUMNS:
        raise ValueError("runtime csv header does not match expected v1 contract")


def read_rows(csv_path: Path) -> list[dict]:
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_proof_rows(proof_path: Path) -> list[dict]:
    with proof_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    normalized = []
    for row in rows:
        normalized.append({col: row.get(col, "unknown") for col in CSV_COLUMNS})
    return normalized


def remove_placeholder_rows(rows: list[dict], placeholder_trade_id: str) -> list[dict]:
    return [row for row in rows if row.get("trade_id") != placeholder_trade_id]


def remove_existing_proof_rows(rows: list[dict], proof_rows: list[dict]) -> list[dict]:
    proof_keys = {row["trade_id"] for row in proof_rows}
    return [row for row in rows if row.get("trade_id") not in proof_keys]


def write_rows(csv_path: Path, rows: list[dict]) -> None:
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--persist",
        action="store_true",
        help="replace placeholder rows and persist proof rows",
    )
    args = parser.parse_args()
    ensure_archive_only_run_allowed()

    params = load_params()
    csv_path, proof_path = resolve_runtime_paths(params)
    assert_header_matches(csv_path)

    rows = read_rows(csv_path)
    original_row_count = len(rows)
    proof_rows = read_proof_rows(proof_path)
    rows = remove_placeholder_rows(rows, params["data_contract"]["placeholder_trade_id"])
    rows = remove_existing_proof_rows(rows, proof_rows)
    rows_before_append = len(rows)
    rows.extend(proof_rows)

    print("stub_mode={0}".format("persist" if args.persist else "dry_run"))
    print("rows_before_cleanup={0}".format(original_row_count))
    print("proof_rows_loaded={0}".format(len(proof_rows)))
    print("rows_before_append={0}".format(rows_before_append))
    print("rows_after_append={0}".format(len(rows)))
    print(
        "pv_config={0}".format(
            json.dumps(params["pv_config"], ensure_ascii=True, sort_keys=True)
        )
    )
    if proof_rows:
        print("first_proof_row={0}".format(json.dumps(proof_rows[0], ensure_ascii=True)))
    if args.persist:
        write_rows(csv_path, rows)
        print("persisted_to={0}".format(csv_path))
    else:
        print("dry_run_only=true")


if __name__ == "__main__":
    main()
