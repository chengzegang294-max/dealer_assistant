from __future__ import annotations

import argparse
import csv
from pathlib import Path


FIELDNAMES = [
    "input_pack_id",
    "sample_date",
    "source_family",
    "source_root",
    "required_files",
    "optional_files",
    "acceptance_output_json",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return [dict(row) for row in reader]


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, delimiter="\t", fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def parse_row_text(row_text: str) -> dict[str, str]:
    parts = row_text.rstrip("\n").split("\t")
    if len(parts) != len(FIELDNAMES):
        raise ValueError(f"row must have {len(FIELDNAMES)} tab-separated fields, got {len(parts)}")
    return dict(zip(FIELDNAMES, parts))


def main() -> int:
    parser = argparse.ArgumentParser(description="Upsert A5 input-pack plan row into sample-plan TSV.")
    parser.add_argument("--sample-plan", required=True)
    parser.add_argument("--row-text", required=True)
    args = parser.parse_args()

    sample_plan = Path(args.sample_plan).resolve()
    row = parse_row_text(args.row_text)
    rows = read_rows(sample_plan)

    replaced = False
    filtered_rows: list[dict[str, str]] = []
    placeholder_id = "NEED_EVIDENCE_SECOND_DATE_INPUT_PACK_V1"

    for existing in rows:
        existing_id = str(existing.get("input_pack_id", "")).strip()
        if existing_id == row["input_pack_id"]:
            filtered_rows.append(row)
            replaced = True
            continue
        if existing_id == placeholder_id and str(row.get("sample_date", "")).strip() != "NEED_EVIDENCE":
            continue
        filtered_rows.append(existing)

    if not replaced:
        filtered_rows.append(row)

    write_rows(sample_plan, filtered_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
