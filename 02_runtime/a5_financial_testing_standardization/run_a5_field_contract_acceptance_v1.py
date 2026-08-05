from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def read_contract_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return [dict(row) for row in reader]


def is_present(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) > 0
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate A5 field contract sample against required fields and downgrade discipline.")
    parser.add_argument("--contract-tsv", required=True)
    parser.add_argument("--sample-json", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    contract_rows = read_contract_rows(Path(args.contract_tsv))
    sample = json.loads(Path(args.sample_json).read_text(encoding="utf-8"))
    if not isinstance(sample, dict):
        raise ValueError("sample-json must be a JSON object")

    checks: list[dict[str, object]] = []
    missing_required: list[str] = []

    for row in contract_rows:
        field_name = str(row.get("field_name", "")).strip()
        required_flag = str(row.get("required_flag", "")).strip().lower()
        if not field_name:
            continue
        if required_flag == "yes":
            actual_present = is_present(sample.get(field_name))
            if not actual_present:
                missing_required.append(field_name)
            checks.append(
                {
                    "field": f"required::{field_name}",
                    "expected": True,
                    "actual": actual_present,
                }
            )

    candidate_mode = any(
        is_present(sample.get(field_name))
        for field_name in ["candidate_background_objects", "candidate_trigger_objects"]
    ) or "candidate" in str(sample.get("maturity_level", "")).lower()

    candidate_discipline_ok = True
    if candidate_mode:
        for field_name in ["maturity_level", "degrade_flags", "still_need_evidence"]:
            if not is_present(sample.get(field_name)):
                candidate_discipline_ok = False

    checks.append(
        {
            "field": "candidate_mode_requires_downgrade_fields",
            "expected": True,
            "actual": candidate_discipline_ok,
        }
    )

    truth_flag_ok = str(sample.get("not_financial_truth", "")).strip().lower() == "yes"
    trade_flag_ok = str(sample.get("not_trade_ready", "")).strip().lower() == "yes"
    checks.append({"field": "not_financial_truth_is_yes", "expected": True, "actual": truth_flag_ok})
    checks.append({"field": "not_trade_ready_is_yes", "expected": True, "actual": trade_flag_ok})

    passed = not missing_required and candidate_discipline_ok and truth_flag_ok and trade_flag_ok

    payload = {
        "acceptance_id": "A5_FIN_STD_FIELD_CONTRACT_ACCEPTANCE_V1",
        "sample_json": str(Path(args.sample_json).resolve()),
        "contract_tsv": str(Path(args.contract_tsv).resolve()),
        "missing_required_fields": missing_required,
        "checks": checks,
        "passed": passed,
    }
    Path(args.output_json).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
