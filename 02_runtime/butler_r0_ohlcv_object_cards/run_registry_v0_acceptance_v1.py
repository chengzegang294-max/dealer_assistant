from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def read_plan_row(path: Path, registry_id: str) -> dict[str, str]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            if row.get("registry_id") == registry_id:
                return row
    raise ValueError(f"registry_id not found in sample plan: {registry_id}")


def read_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("acceptance output must be a json object")
    return payload


def normalize_blockers(value: object) -> str:
    if isinstance(value, list):
        return "|".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate registry_v0 output against minimal acceptance expectations.")
    parser.add_argument("--sample-plan", required=True)
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    output_payload = read_json(Path(args.input_json))
    registry_id = str(output_payload.get("registry_id", ""))
    if not registry_id:
        raise ValueError("registry_id missing in input json")
    plan_row = read_plan_row(Path(args.sample_plan), registry_id)

    final_card = output_payload.get("final_decision_card", {})
    size_card = output_payload.get("size_policy_card", {})
    summary = output_payload.get("aggregate_summary", {})
    if not isinstance(final_card, dict) or not isinstance(size_card, dict) or not isinstance(summary, dict):
        raise ValueError("registry output missing expected card objects")

    checks = [
        {
            "field": "final_signal",
            "expected": plan_row["expected_final_signal"],
            "actual": str(final_card.get("final_signal", "")),
        },
        {
            "field": "trade_gate",
            "expected": plan_row["expected_trade_gate"],
            "actual": str(final_card.get("trade_gate", "")),
        },
        {
            "field": "blockers",
            "expected": plan_row["expected_blockers"],
            "actual": normalize_blockers(final_card.get("blockers", [])),
        },
        {
            "field": "permission",
            "expected": plan_row["expected_permission"],
            "actual": str(final_card.get("permission", "")),
        },
        {
            "field": "hard_block",
            "expected": plan_row["expected_hard_block"].lower(),
            "actual": str(final_card.get("hard_block", "")).lower(),
        },
        {
            "field": "size_policy",
            "expected": plan_row["expected_size_policy"],
            "actual": str(size_card.get("size_policy", "")),
        },
        {
            "field": "recommended_size_scalar",
            "expected": "0.0" if plan_row["expected_size_policy"] == "blocked_to_zero" else "nonzero",
            "actual": str(size_card.get("recommended_size_scalar", "")),
        },
    ]

    failed = []
    for check in checks:
        if check["field"] == "recommended_size_scalar":
            passed = float(check["actual"]) == 0.0 if check["expected"] == "0.0" else float(check["actual"]) > 0.0
        else:
            passed = check["expected"] == check["actual"]
        check["passed"] = passed
        if not passed:
            failed.append(check["field"])

    result = {
        "registry_id": registry_id,
        "input_json": str(Path(args.input_json)).replace("\\", "/"),
        "sample_plan": str(Path(args.sample_plan)).replace("\\", "/"),
        "as_of_date": output_payload.get("as_of_date", ""),
        "summary_snapshot": {
            "final_signal": final_card.get("final_signal", ""),
            "trade_gate": final_card.get("trade_gate", ""),
            "permission": final_card.get("permission", ""),
            "blockers": final_card.get("blockers", []),
            "hard_block": final_card.get("hard_block", False),
            "size_policy": size_card.get("size_policy", ""),
            "recommended_size_scalar": size_card.get("recommended_size_scalar", None),
            "aggregate_final_signal": summary.get("final_signal", ""),
        },
        "checks": checks,
        "acceptance_status": "pass" if not failed else "fail",
        "failed_fields": failed,
    }

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
