from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT)).replace("\\", "/")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    output_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_min_chain_validation"
        / "artifacts"
        / "a5_g5_same_batch_boundary_audit_latest.json"
    )

    tw_same_batch_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_target_weight_validation"
        / "artifacts"
        / "target_weight_validation"
        / "covariance_target_weight_same_batch_latest.json"
    )
    pte_same_batch_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_portfolio_tracking_error_validation"
        / "artifacts"
        / "portfolio_tracking_error_validation"
        / "covariance_target_weight_pte_same_batch_latest.json"
    )
    apw_same_batch_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_adjusted_position_weight_validation"
        / "artifacts"
        / "adjusted_position_weight_validation"
        / "covariance_target_weight_pte_apw_same_batch_latest.json"
    )
    tw_real_input_success_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_target_weight_validation"
        / "artifacts"
        / "target_weight_validation"
        / "tw_real_input_success_latest.json"
    )
    tw_real_input_failure_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_target_weight_validation"
        / "artifacts"
        / "target_weight_validation"
        / "tw_real_input_failure_latest.json"
    )
    tw_actual_generation_success_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_target_weight_validation"
        / "artifacts"
        / "target_weight_validation"
        / "tw_actual_generation_success_latest.json"
    )
    tw_actual_generation_failure_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_target_weight_validation"
        / "artifacts"
        / "target_weight_validation"
        / "tw_actual_generation_failure_latest.json"
    )
    pte_same_batch_success_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_portfolio_tracking_error_validation"
        / "artifacts"
        / "portfolio_tracking_error_validation"
        / "pte_same_batch_success_latest.json"
    )
    pte_same_batch_failure_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_portfolio_tracking_error_validation"
        / "artifacts"
        / "portfolio_tracking_error_validation"
        / "pte_same_batch_failure_latest.json"
    )
    apw_same_batch_success_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_adjusted_position_weight_validation"
        / "artifacts"
        / "adjusted_position_weight_validation"
        / "apw_same_batch_success_latest.json"
    )
    apw_same_batch_formula_failure_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_adjusted_position_weight_validation"
        / "artifacts"
        / "adjusted_position_weight_validation"
        / "apw_same_batch_formula_failure_latest.json"
    )

    tw_same_batch = load_json(tw_same_batch_json)
    pte_same_batch = load_json(pte_same_batch_json)
    apw_same_batch = load_json(apw_same_batch_json)
    tw_real_input_success = load_json(tw_real_input_success_json)
    tw_real_input_failure = load_json(tw_real_input_failure_json)
    tw_actual_generation_success = load_json(tw_actual_generation_success_json)
    tw_actual_generation_failure = load_json(tw_actual_generation_failure_json)
    pte_same_batch_success = load_json(pte_same_batch_success_json)
    pte_same_batch_failure = load_json(pte_same_batch_failure_json)
    apw_same_batch_success = load_json(apw_same_batch_success_json)
    apw_same_batch_formula_failure = load_json(apw_same_batch_formula_failure_json)

    target_weight_boundary = {
        "boundary_name": "explicit_validation_run_plus_failure_path_consistency",
        "same_batch_chain_passed": (
            tw_same_batch.get("covariance_chain_passed") is True
            and tw_same_batch.get("target_weight_chain_passed") is True
        ),
        "real_input_success_passed": tw_real_input_success.get("validation_passed") is True,
        "real_input_failure_reason": tw_real_input_failure.get("payload", {}).get("observed_abort_reason", ""),
        "actual_generation_success_executed": tw_actual_generation_success.get("generation_executed") is True,
        "actual_generation_failure_reason": tw_actual_generation_failure.get("observed_abort_reason", ""),
        "failure_reason_alignment_passed": (
            tw_same_batch.get("failure_reason_alignment", {}).get("real_input_and_generation_aligned") is True
        ),
    }
    target_weight_boundary["runtime_backed"] = all(
        [
            target_weight_boundary["same_batch_chain_passed"],
            target_weight_boundary["real_input_success_passed"],
            target_weight_boundary["actual_generation_success_executed"],
            target_weight_boundary["failure_reason_alignment_passed"],
            target_weight_boundary["real_input_failure_reason"] == "missing_constraint_set",
            target_weight_boundary["actual_generation_failure_reason"] == "missing_constraint_set",
        ]
    )

    pte_boundary = {
        "boundary_name": "explicit_success_risk_output_plus_failure_abort_reason_consistency",
        "same_batch_chain_passed": (
            pte_same_batch.get("covariance_target_weight_chain_passed") is True
            and pte_same_batch.get("pte_chain_passed") is True
        ),
        "success_generation_executed": pte_same_batch_success.get("generation_executed") is True,
        "success_has_explicit_risk_output": (
            pte_same_batch_success.get("audit_fields", {}).get("success_sample_has_explicit_risk_output") is True
        ),
        "success_consumes_covariance_matrix": (
            pte_same_batch_success.get("audit_fields", {}).get("covariance_matrix_consumed") is True
        ),
        "failure_abort_reason": pte_same_batch_failure.get("observed_abort_reason", ""),
    }
    pte_boundary["runtime_backed"] = all(
        [
            pte_boundary["same_batch_chain_passed"],
            pte_boundary["success_generation_executed"],
            pte_boundary["success_has_explicit_risk_output"],
            pte_boundary["success_consumes_covariance_matrix"],
            pte_boundary["failure_abort_reason"] == "missing_covariance_matrix_csv",
        ]
    )

    apw_boundary = {
        "boundary_name": "explicit_adjusted_position_weight_formula_plus_failure_abort_reason_and_degrade_flags_consistency",
        "same_batch_chain_passed": (
            apw_same_batch.get("covariance_target_weight_pte_chain_passed") is True
            and apw_same_batch.get("apw_chain_passed") is True
        ),
        "success_generation_executed": apw_same_batch_success.get("generation_executed") is True,
        "success_formula_traceable": (
            apw_same_batch_success.get("result_summary", {}).get("formula_traceable") is True
        ),
        "success_consumes_same_batch_pte": (
            apw_same_batch_success.get("payload", {}).get("portfolio_tracking_error_generation_json", "").endswith(
                "pte_same_batch_success_latest.json"
            )
        ),
        "failure_abort_reason": apw_same_batch_formula_failure.get("observed_abort_reason", ""),
        "failure_degrade_flag_present": (
            "final_size_scalar_below_threshold"
            in apw_same_batch_formula_failure.get("payload", {}).get("degrade_flags", [])
        ),
    }
    apw_boundary["runtime_backed"] = all(
        [
            apw_boundary["same_batch_chain_passed"],
            apw_boundary["success_generation_executed"],
            apw_boundary["success_formula_traceable"],
            apw_boundary["success_consumes_same_batch_pte"],
            apw_boundary["failure_abort_reason"] == "final_size_scalar_below_abort_threshold",
            apw_boundary["failure_degrade_flag_present"],
        ]
    )

    all_boundaries_runtime_backed = all(
        [
            target_weight_boundary["runtime_backed"],
            pte_boundary["runtime_backed"],
            apw_boundary["runtime_backed"],
        ]
    )

    summary = {
        "run_id": "A5_G5_SAME_BATCH_BOUNDARY_AUDIT_V1",
        "producer": "run_g5_same_batch_boundary_audit_v1.py",
        "scope": "a5_g5_same_batch_boundary_audit",
        "status": "success",
        "evidence_mode": "hard",
        "covariance_downstream_lock_reason": "downstream_single_segment_not_output_passed_boundary_not_formally_released",
        "all_segment_boundaries_runtime_backed": all_boundaries_runtime_backed,
        "covariance_lock_reason_now_has_runtime_backing": all_boundaries_runtime_backed,
        "target_weight_boundary": target_weight_boundary,
        "portfolio_tracking_error_boundary": pte_boundary,
        "adjusted_position_weight_boundary": apw_boundary,
        "artifact_sources": {
            "target_weight_same_batch_json": rel(tw_same_batch_json),
            "portfolio_tracking_error_same_batch_json": rel(pte_same_batch_json),
            "adjusted_position_weight_same_batch_json": rel(apw_same_batch_json),
        },
        "forbidden_claim": [
            "output_passed",
            "implementation_ready",
            "covariance_model_id_ready",
        ],
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
