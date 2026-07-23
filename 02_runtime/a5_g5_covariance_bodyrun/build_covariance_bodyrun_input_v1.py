from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def require_fields(payload: dict, required_fields: list[str]) -> list[str]:
    return [field for field in required_fields if field not in payload]


def validate_success_payload(payload: dict) -> tuple[bool, list[str]]:
    errors: list[str] = []
    missing = require_fields(
        payload,
        [
            "run_id",
            "candidate_model_family",
            "portfolio_date",
            "benchmark_id",
            "asset_universe_id",
            "returns_window_spec",
            "tracking_error_limit",
            "active_risk_aversion",
        ],
    )
    if missing:
        return False, [f"missing fields: {missing}"]

    if payload["candidate_model_family"] != "benchmark_relative_sample_covariance":
        errors.append("candidate_model_family must be benchmark_relative_sample_covariance")
    if payload.get("benchmark_id", "") == "":
        errors.append("benchmark_id must not be empty for success assembly")

    window_spec = payload["returns_window_spec"]
    if window_spec.get("lookback_days", 0) <= 0:
        errors.append("returns_window_spec.lookback_days must be > 0")
    if window_spec.get("frequency", "") == "":
        errors.append("returns_window_spec.frequency must not be empty")
    if payload.get("asset_universe_id", "") == "":
        errors.append("asset_universe_id must not be empty")

    return not errors, errors


def validate_failure_payload(payload: dict) -> tuple[bool, list[str]]:
    errors: list[str] = []
    missing = require_fields(
        payload,
        [
            "run_id",
            "candidate_model_family",
            "portfolio_date",
            "benchmark_id",
            "asset_universe_id",
            "returns_window_spec",
            "tracking_error_limit",
            "active_risk_aversion",
        ],
    )
    if missing:
        return False, [f"missing fields: {missing}"]

    if payload["candidate_model_family"] != "benchmark_relative_sample_covariance":
        errors.append("candidate_model_family must be benchmark_relative_sample_covariance")
    if payload.get("benchmark_id", "") != "":
        errors.append("benchmark_id must be empty for the default failure assembly")

    window_spec = payload["returns_window_spec"]
    if window_spec.get("lookback_days", 0) <= 0:
        errors.append("returns_window_spec.lookback_days must be > 0 even for failure assembly")
    if window_spec.get("frequency", "") == "":
        errors.append("returns_window_spec.frequency must not be empty")

    return not errors, errors


def build_success_output(payload: dict) -> dict:
    return {
        "run_id": payload["run_id"],
        "producer": "build_covariance_bodyrun_input_v1.py",
        "scope": "covariance_bodyrun_input",
        "status": "success",
        "evidence_mode": "hard",
        "assembly_passed": True,
        "abort_reason": "",
        "assembled_input": {
            "candidate_model_family": payload["candidate_model_family"],
            "portfolio_date": payload["portfolio_date"],
            "benchmark_id": payload["benchmark_id"],
            "asset_universe_id": payload["asset_universe_id"],
            "returns_window_spec": payload["returns_window_spec"],
            "tracking_error_limit": payload["tracking_error_limit"],
            "active_risk_aversion": payload["active_risk_aversion"],
        },
        "audit_note": "template_level_input_assembly_only__not_body_matrix_fresh_run",
    }


def build_failure_output(payload: dict) -> dict:
    return {
        "run_id": payload["run_id"],
        "producer": "build_covariance_bodyrun_input_v1.py",
        "scope": "covariance_bodyrun_input",
        "status": "success",
        "evidence_mode": "hard",
        "assembly_passed": True,
        "abort_reason": "invalid_benchmark_context",
        "assembled_input": {
            "candidate_model_family": payload["candidate_model_family"],
            "portfolio_date": payload["portfolio_date"],
            "benchmark_id": payload["benchmark_id"],
            "asset_universe_id": payload["asset_universe_id"],
            "returns_window_spec": payload["returns_window_spec"],
            "tracking_error_limit": payload["tracking_error_limit"],
            "active_risk_aversion": payload["active_risk_aversion"],
        },
        "audit_note": "failure_input_assembly_and_abort_reason_are_consistent",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build covariance body-run minimal input assembly from a JSON template.")
    parser.add_argument("--case", required=True, choices=["success", "failure"])
    parser.add_argument("--template-json", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    template_json = Path(args.template_json)
    output_json = Path(args.output_json)
    payload = load_json(template_json)

    if args.case == "success":
        passed, errors = validate_success_payload(payload)
        output = build_success_output(payload) if passed else {"assembly_passed": False, "validation_errors": errors}
    else:
        passed, errors = validate_failure_payload(payload)
        output = build_failure_output(payload) if passed else {"assembly_passed": False, "validation_errors": errors}

    if passed:
        output["validation_errors"] = []
        output["template_json"] = str(template_json).replace("\\", "/")

    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
