from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def require_fields(payload: dict, required_fields: list[str]) -> list[str]:
    return [field for field in required_fields if field not in payload]


def validate_success_case(payload: dict) -> tuple[bool, list[str]]:
    errors: list[str] = []
    missing = require_fields(
        payload,
        [
            "run_id",
            "input_assumption",
            "risk_handling_mode",
            "weights",
            "result_summary",
            "checks",
            "abort_reason",
        ],
    )
    if missing:
        errors.append(f"missing fields: {missing}")
        return False, errors

    weights = payload["weights"]
    summary = payload["result_summary"]
    if not isinstance(weights, list) or not weights:
        errors.append("weights must be a non-empty list")
    if summary.get("non_empty") is not True:
        errors.append("result_summary.non_empty must be true")
    if summary.get("within_bounds") is not True:
        errors.append("result_summary.within_bounds must be true")
    if summary.get("weight_sum_traceable") is not True:
        errors.append("result_summary.weight_sum_traceable must be true")
    if payload.get("abort_reason", "") != "":
        errors.append("abort_reason must be empty for success case")

    return not errors, errors


def validate_failure_case(payload: dict) -> tuple[bool, list[str]]:
    errors: list[str] = []
    missing = require_fields(
        payload,
        [
            "run_id",
            "failure_trigger",
            "input_assumption",
            "weights",
            "observed_abort_reason",
            "path_consistency_note",
        ],
    )
    if missing:
        errors.append(f"missing fields: {missing}")
        return False, errors

    if payload.get("weights") != []:
        errors.append("weights must be an empty list for failure case")
    if payload.get("failure_trigger") != payload.get("observed_abort_reason"):
        errors.append("failure_trigger must match observed_abort_reason")
    if payload.get("path_consistency_note") != "failure_sample_and_abort_reason_are_consistent":
        errors.append("path_consistency_note must use the fixed consistency label")

    return not errors, errors


def validate_real_input_success_case(payload: dict) -> tuple[bool, list[str]]:
    errors: list[str] = []
    missing = require_fields(
        payload,
        [
            "run_id",
            "input_template_json",
            "input_contract",
            "alpha_vector",
            "generated_weights",
            "result_summary",
            "abort_reason",
        ],
    )
    if missing:
        errors.append(f"missing fields: {missing}")
        return False, errors

    input_contract = payload["input_contract"]
    summary = payload["result_summary"]
    alpha_vector = payload["alpha_vector"]
    generated_weights = payload["generated_weights"]

    if not payload["input_template_json"].endswith("target_weight_real_input_template_v1.json"):
        errors.append("input_template_json must point to target_weight_real_input_template_v1.json")
    if input_contract.get("constraint_set_id", "") == "":
        errors.append("constraint_set_id must not be empty for real input success case")
    if input_contract.get("alpha_source_type") != "contract_frozen_proxy":
        errors.append("alpha_source_type must be contract_frozen_proxy")
    if not isinstance(alpha_vector, list) or not alpha_vector:
        errors.append("alpha_vector must be a non-empty list")
    if not isinstance(generated_weights, list) or not generated_weights:
        errors.append("generated_weights must be a non-empty list")
    if summary.get("non_empty") is not True:
        errors.append("result_summary.non_empty must be true")
    if summary.get("within_bounds") is not True:
        errors.append("result_summary.within_bounds must be true")
    if summary.get("weight_sum_traceable") is not True:
        errors.append("result_summary.weight_sum_traceable must be true")
    if summary.get("generated_from_real_input_template") is not True:
        errors.append("result_summary.generated_from_real_input_template must be true")
    if payload.get("abort_reason", "") != "":
        errors.append("abort_reason must be empty for real input success case")

    return not errors, errors


def validate_real_input_failure_case(payload: dict) -> tuple[bool, list[str]]:
    errors: list[str] = []
    missing = require_fields(
        payload,
        [
            "run_id",
            "input_template_json",
            "failure_trigger",
            "input_contract",
            "alpha_vector",
            "generated_weights",
            "observed_abort_reason",
            "path_consistency_note",
        ],
    )
    if missing:
        errors.append(f"missing fields: {missing}")
        return False, errors

    input_contract = payload["input_contract"]
    if not payload["input_template_json"].endswith("target_weight_real_input_template_v1.json"):
        errors.append("input_template_json must point to target_weight_real_input_template_v1.json")
    if payload.get("generated_weights") != []:
        errors.append("generated_weights must be an empty list for real input failure case")
    if payload.get("failure_trigger") != payload.get("observed_abort_reason"):
        errors.append("failure_trigger must match observed_abort_reason")
    if payload.get("path_consistency_note") != "real_input_failure_path_is_consistent":
        errors.append("path_consistency_note must use the fixed real-input consistency label")
    if input_contract.get("constraint_set_id", "") != "":
        errors.append("constraint_set_id must be empty for the default real input failure case")
    if not isinstance(payload.get("alpha_vector"), list) or not payload["alpha_vector"]:
        errors.append("alpha_vector must still be non-empty for the default real input failure case")

    return not errors, errors


def build_output(case_name: str, payload: dict, passed: bool, errors: list[str], template_json: Path) -> dict:
    return {
        "run_id": payload.get("run_id", ""),
        "producer": "run_target_weight_validation_v1.py",
        "scope": "target_weight_validation",
        "status": "success" if passed else "failed_validation",
        "evidence_mode": "hard",
        "case_name": case_name,
        "template_json": str(template_json).replace("\\", "/"),
        "validation_passed": passed,
        "validation_errors": errors,
        "payload": payload,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run target_weight minimal validation from a JSON template.")
    parser.add_argument(
        "--case",
        required=True,
        choices=["success", "failure", "real_input_success", "real_input_failure"],
    )
    parser.add_argument("--template-json", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    template_json = Path(args.template_json)
    output_json = Path(args.output_json)
    payload = load_json(template_json)

    if args.case == "success":
        passed, errors = validate_success_case(payload)
    elif args.case == "failure":
        passed, errors = validate_failure_case(payload)
    elif args.case == "real_input_success":
        passed, errors = validate_real_input_success_case(payload)
    else:
        passed, errors = validate_real_input_failure_case(payload)

    output = build_output(args.case, payload, passed, errors, template_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
