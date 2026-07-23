from __future__ import annotations

import argparse
import json
from pathlib import Path


ALLOWED_FAMILIES = {
    "benchmark_relative_sample_covariance",
    "shrinkage_structured_covariance",
    "factor_implied_covariance",
}


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
            "candidate_family",
            "portfolio_date",
            "benchmark_id",
            "asset_universe_id",
            "returns_window_spec",
            "tracking_error_limit",
            "active_risk_aversion",
            "matrix_summary",
            "covariance_model_id",
            "abort_reason",
            "audit_note",
        ],
    )
    if missing:
        return False, [f"missing fields: {missing}"]

    if payload["candidate_family"] not in ALLOWED_FAMILIES:
        errors.append("candidate_family must be in the frozen candidate family set")
    if payload["candidate_family"] != "benchmark_relative_sample_covariance":
        errors.append("current first body-run prep must use benchmark_relative_sample_covariance")
    if payload.get("benchmark_id", "") == "":
        errors.append("benchmark_id must not be empty for success case")
    matrix_summary = payload["matrix_summary"]
    if matrix_summary.get("matrix_shape") != [20, 20]:
        errors.append("matrix_shape must be [20, 20] for the default success prep template")
    if matrix_summary.get("diagonal_positive") is not True:
        errors.append("diagonal_positive must be true")
    if matrix_summary.get("is_psd") is not True:
        errors.append("is_psd must be true")
    if not isinstance(payload.get("covariance_model_id"), str) or payload["covariance_model_id"] == "":
        errors.append("covariance_model_id must be a non-empty string for success case")
    if payload.get("abort_reason", "") != "":
        errors.append("abort_reason must be empty for success case")
    if payload.get("audit_note") != "template_level_only__not_body_matrix_fresh_run":
        errors.append("audit_note must use the fixed template-level label")

    return not errors, errors


def validate_failure_case(payload: dict) -> tuple[bool, list[str]]:
    errors: list[str] = []
    missing = require_fields(
        payload,
        [
            "run_id",
            "candidate_family",
            "portfolio_date",
            "benchmark_id",
            "asset_universe_id",
            "returns_window_spec",
            "tracking_error_limit",
            "active_risk_aversion",
            "matrix_summary",
            "covariance_model_id",
            "abort_reason",
            "audit_note",
        ],
    )
    if missing:
        return False, [f"missing fields: {missing}"]

    if payload["candidate_family"] not in ALLOWED_FAMILIES:
        errors.append("candidate_family must be in the frozen candidate family set")
    if payload["candidate_family"] != "benchmark_relative_sample_covariance":
        errors.append("current first body-run prep must use benchmark_relative_sample_covariance")
    if payload.get("benchmark_id", "") != "":
        errors.append("benchmark_id must be empty for the default failure case")
    matrix_summary = payload["matrix_summary"]
    if matrix_summary.get("matrix_shape") != [0, 0]:
        errors.append("matrix_shape must be [0, 0] for the default failure prep template")
    if matrix_summary.get("diagonal_positive") is not False:
        errors.append("diagonal_positive must be false for failure case")
    if matrix_summary.get("is_psd") is not False:
        errors.append("is_psd must be false for failure case")
    if payload.get("covariance_model_id") is not None:
        errors.append("covariance_model_id must be null for failure case")
    if payload.get("abort_reason") != "invalid_benchmark_context":
        errors.append("abort_reason must be invalid_benchmark_context for the default failure case")
    if payload.get("audit_note") != "failure_template_and_abort_reason_are_consistent":
        errors.append("audit_note must use the fixed failure consistency label")

    return not errors, errors


def build_output(case_name: str, payload: dict, passed: bool, errors: list[str], template_json: Path) -> dict:
    return {
        "run_id": payload.get("run_id", ""),
        "producer": "run_covariance_bodyrun_prep_v1.py",
        "scope": "covariance_bodyrun",
        "status": "success" if passed else "failed_validation",
        "evidence_mode": "hard",
        "case_name": case_name,
        "template_json": str(template_json).replace("\\", "/"),
        "validation_passed": passed,
        "validation_errors": errors,
        "payload": payload,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run covariance_model_id minimal body-run prep validation from a JSON template.")
    parser.add_argument("--case", required=True, choices=["success", "failure"])
    parser.add_argument("--template-json", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    template_json = Path(args.template_json)
    output_json = Path(args.output_json)
    payload = load_json(template_json)

    if args.case == "success":
        passed, errors = validate_success_case(payload)
    else:
        passed, errors = validate_failure_case(payload)

    output = build_output(args.case, payload, passed, errors, template_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
