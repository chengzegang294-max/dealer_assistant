from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def require_fields(payload: dict, required_fields: list[str]) -> list[str]:
    return [field for field in required_fields if field not in payload]


def validate_runtime_params(payload: dict) -> tuple[bool, list[str]]:
    errors: list[str] = []
    missing = require_fields(
        payload,
        [
            "candidate_model_family",
            "portfolio_date",
            "benchmark_id",
            "asset_universe_id",
            "returns_window_spec",
            "tracking_error_limit",
            "active_risk_aversion",
            "entry_mode",
            "notes",
        ],
    )
    if missing:
        return False, [f"missing fields: {missing}"]

    if payload["candidate_model_family"] != "benchmark_relative_sample_covariance":
        errors.append("candidate_model_family must be benchmark_relative_sample_covariance")
    if payload.get("benchmark_id", "") == "":
        errors.append("benchmark_id must not be empty")
    if payload.get("asset_universe_id", "") == "":
        errors.append("asset_universe_id must not be empty")
    window_spec = payload["returns_window_spec"]
    if window_spec.get("lookback_days", 0) <= 0:
        errors.append("returns_window_spec.lookback_days must be > 0")
    if window_spec.get("frequency", "") == "":
        errors.append("returns_window_spec.frequency must not be empty")
    if payload.get("tracking_error_limit", 0) <= 0:
        errors.append("tracking_error_limit must be > 0")
    if payload.get("active_risk_aversion", 0) <= 0:
        errors.append("active_risk_aversion must be > 0")
    if payload.get("entry_mode") != "first_fresh_run_prep_only":
        errors.append("entry_mode must stay first_fresh_run_prep_only")
    if payload.get("notes") != "not_ready__do_not_claim_body_matrix_run_completed":
        errors.append("notes must keep the fixed not_ready label")

    return not errors, errors


def validate_success_assembly(payload: dict, runtime_params: dict) -> tuple[bool, list[str]]:
    errors: list[str] = []
    missing = require_fields(
        payload,
        [
            "run_id",
            "producer",
            "scope",
            "status",
            "evidence_mode",
            "assembly_passed",
            "abort_reason",
            "assembled_input",
            "audit_note",
            "validation_errors",
            "template_json",
        ],
    )
    if missing:
        return False, [f"missing fields: {missing}"]

    if payload.get("assembly_passed") is not True:
        errors.append("assembly_passed must be true")
    if payload.get("status") != "success":
        errors.append("status must be success")
    if payload.get("abort_reason", "") != "":
        errors.append("abort_reason must be empty for success assembly")
    if payload.get("audit_note") != "template_level_input_assembly_only__not_body_matrix_fresh_run":
        errors.append("audit_note must use the fixed input assembly label")
    if payload.get("validation_errors") != []:
        errors.append("validation_errors must be empty")

    assembled_input = payload["assembled_input"]
    expected_fields = [
        "candidate_model_family",
        "portfolio_date",
        "benchmark_id",
        "asset_universe_id",
        "tracking_error_limit",
        "active_risk_aversion",
    ]
    for field in expected_fields:
        if assembled_input.get(field) != runtime_params.get(field):
            errors.append(f"assembled_input.{field} must match runtime params")

    assembled_window = assembled_input.get("returns_window_spec", {})
    runtime_window = runtime_params.get("returns_window_spec", {})
    if assembled_window.get("lookback_days") != runtime_window.get("lookback_days"):
        errors.append("assembled_input.returns_window_spec.lookback_days must match runtime params")
    if assembled_window.get("frequency") != runtime_window.get("frequency"):
        errors.append("assembled_input.returns_window_spec.frequency must match runtime params")

    return not errors, errors


def validate_failure_assembly(payload: dict) -> tuple[bool, list[str]]:
    errors: list[str] = []
    missing = require_fields(
        payload,
        [
            "run_id",
            "producer",
            "scope",
            "status",
            "evidence_mode",
            "assembly_passed",
            "abort_reason",
            "assembled_input",
            "audit_note",
            "validation_errors",
            "template_json",
        ],
    )
    if missing:
        return False, [f"missing fields: {missing}"]

    if payload.get("assembly_passed") is not True:
        errors.append("assembly_passed must be true")
    if payload.get("status") != "success":
        errors.append("status must be success")
    if payload.get("abort_reason") != "invalid_benchmark_context":
        errors.append("abort_reason must be invalid_benchmark_context")
    if payload.get("audit_note") != "failure_input_assembly_and_abort_reason_are_consistent":
        errors.append("audit_note must use the fixed failure label")
    if payload.get("validation_errors") != []:
        errors.append("validation_errors must be empty")

    assembled_input = payload["assembled_input"]
    if assembled_input.get("candidate_model_family") != "benchmark_relative_sample_covariance":
        errors.append("failure assembled_input.candidate_model_family must stay on the frozen first family")
    if assembled_input.get("benchmark_id", "") != "":
        errors.append("failure assembled_input.benchmark_id must be empty")

    return not errors, errors


def validate_prep_artifact(payload: dict, case_name: str) -> tuple[bool, list[str]]:
    errors: list[str] = []
    missing = require_fields(
        payload,
        [
            "run_id",
            "producer",
            "scope",
            "status",
            "evidence_mode",
            "case_name",
            "template_json",
            "validation_passed",
            "validation_errors",
            "payload",
        ],
    )
    if missing:
        return False, [f"missing fields: {missing}"]

    if payload.get("status") != "success":
        errors.append("status must be success")
    if payload.get("case_name") != case_name:
        errors.append(f"case_name must be {case_name}")
    if payload.get("validation_passed") is not True:
        errors.append("validation_passed must be true")
    if payload.get("validation_errors") != []:
        errors.append("validation_errors must be empty")

    return not errors, errors


def build_check_result(check_name: str, passed: bool, details: list[str], source_path: Path) -> dict:
    return {
        "check_name": check_name,
        "passed": passed,
        "details": details,
        "source_path": str(source_path).replace("\\", "/"),
    }


def build_output(args: argparse.Namespace, checks: list[dict], runtime_params: dict) -> dict:
    preflight_passed = all(check["passed"] for check in checks)
    return {
        "run_id": "covariance_bodyrun_preflight_latest",
        "producer": "run_covariance_bodyrun_preflight_v1.py",
        "scope": "covariance_bodyrun_preflight",
        "status": "success" if preflight_passed else "failed_validation",
        "evidence_mode": "hard",
        "preflight_passed": preflight_passed,
        "candidate_model_family": runtime_params["candidate_model_family"],
        "entry_mode": runtime_params["entry_mode"],
        "notes": "preflight_only__still_not_body_matrix_fresh_run",
        "checks": checks,
        "next_step_if_passed": "prepare_first_fresh_run_execution_for_benchmark_relative_sample_covariance",
        "forbidden_claim": "risk_model_ready",
        "runtime_params_json": str(Path(args.runtime_params_json)).replace("\\", "/"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the first fresh-run preflight boundary for covariance_model_id.")
    parser.add_argument("--runtime-params-json", required=True)
    parser.add_argument("--success-assembly-json", required=True)
    parser.add_argument("--failure-assembly-json", required=True)
    parser.add_argument("--success-prep-json", required=True)
    parser.add_argument("--failure-prep-json", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    runtime_params_path = Path(args.runtime_params_json)
    success_assembly_path = Path(args.success_assembly_json)
    failure_assembly_path = Path(args.failure_assembly_json)
    success_prep_path = Path(args.success_prep_json)
    failure_prep_path = Path(args.failure_prep_json)
    output_path = Path(args.output_json)

    runtime_params = load_json(runtime_params_path)
    success_assembly = load_json(success_assembly_path)
    failure_assembly = load_json(failure_assembly_path)
    success_prep = load_json(success_prep_path)
    failure_prep = load_json(failure_prep_path)

    checks: list[dict] = []

    passed, errors = validate_runtime_params(runtime_params)
    checks.append(build_check_result("runtime_params_boundary", passed, errors, runtime_params_path))

    passed, errors = validate_success_assembly(success_assembly, runtime_params)
    checks.append(build_check_result("success_input_assembly_latest", passed, errors, success_assembly_path))

    passed, errors = validate_failure_assembly(failure_assembly)
    checks.append(build_check_result("failure_input_assembly_latest", passed, errors, failure_assembly_path))

    passed, errors = validate_prep_artifact(success_prep, "success")
    checks.append(build_check_result("success_prep_smoke_run", passed, errors, success_prep_path))

    passed, errors = validate_prep_artifact(failure_prep, "failure")
    checks.append(build_check_result("failure_prep_smoke_run", passed, errors, failure_prep_path))

    output = build_output(args, checks, runtime_params)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
