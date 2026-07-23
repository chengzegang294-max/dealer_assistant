from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT)).replace("\\", "/")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def run_step(name: str, command: list[str], output_json: Path) -> dict:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    result = {
        "step": name,
        "command": command,
        "exit_code": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
        "output_json": rel(output_json),
        "output_exists": output_json.exists(),
        "step_passed": False,
        "expected_mode": "",
    }
    if output_json.exists():
        payload = load_json(output_json)
        result["status"] = payload.get("status", "")
        result["payload_summary"] = payload
        result["step_passed"], result["expected_mode"] = evaluate_step(name, payload)
    else:
        result["status"] = "missing_output"
        result["payload_summary"] = {}
        result["expected_mode"] = "missing_output"
    return result


def evaluate_step(name: str, payload: dict) -> tuple[bool, str]:
    if name == "covariance_target_weight_pte_same_batch":
        return (
            payload.get("covariance_target_weight_chain_passed") is True
            and payload.get("pte_chain_passed") is True
        ), "covariance_target_weight_chain_passed_and_pte_chain_passed"
    if name == "apw_same_batch_success":
        return (
            payload.get("generation_executed") is True
            and payload.get("audit_fields", {}).get("upstream_generation_consumed") is True
        ), "generation_executed_true_with_upstream_generation_consumed"
    if name == "apw_same_batch_formula_failure":
        return (
            payload.get("generation_executed") is False
            and payload.get("observed_abort_reason") == "final_size_scalar_below_abort_threshold"
        ), "generation_executed_false_with_formula_threshold_abort"
    return False, "unknown_step"


def build_apw_input(
    template_payload: dict,
    target_generation_json: str,
    pte_generation_json: str,
    audit_note: str,
) -> dict:
    payload = dict(template_payload)
    payload["target_weight_generation_json"] = target_generation_json
    payload["portfolio_tracking_error_generation_json"] = pte_generation_json
    payload["audit_note"] = audit_note
    return payload


def main() -> None:
    python = sys.executable
    apw_root = ROOT / "02_runtime" / "a5_g5_adjusted_position_weight_validation"
    pte_same_batch_summary_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_portfolio_tracking_error_validation"
        / "artifacts"
        / "portfolio_tracking_error_validation"
        / "covariance_target_weight_pte_same_batch_latest.json"
    )
    tw_generation_success_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_target_weight_validation"
        / "artifacts"
        / "target_weight_validation"
        / "tw_actual_generation_success_latest.json"
    )
    pte_same_batch_success_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_portfolio_tracking_error_validation"
        / "artifacts"
        / "portfolio_tracking_error_validation"
        / "pte_same_batch_success_latest.json"
    )
    apw_success_input_json = apw_root / "artifacts" / "adjusted_position_weight_validation" / "apw_same_batch_success_input_latest.json"
    apw_formula_failure_input_json = apw_root / "artifacts" / "adjusted_position_weight_validation" / "apw_same_batch_formula_failure_input_latest.json"
    apw_success_output_json = apw_root / "artifacts" / "adjusted_position_weight_validation" / "apw_same_batch_success_latest.json"
    apw_formula_failure_output_json = apw_root / "artifacts" / "adjusted_position_weight_validation" / "apw_same_batch_formula_failure_latest.json"
    summary_json = apw_root / "artifacts" / "adjusted_position_weight_validation" / "covariance_target_weight_pte_apw_same_batch_latest.json"

    steps: list[dict] = []

    pte_step = run_step(
        "covariance_target_weight_pte_same_batch",
        [
            python,
            str(ROOT / "02_runtime" / "a5_g5_portfolio_tracking_error_validation" / "run_covariance_target_weight_pte_same_batch_v1.py"),
        ],
        pte_same_batch_summary_json,
    )
    steps.append(pte_step)

    if pte_step["step_passed"] is not True:
        summary = {
            "run_id": "COVARIANCE_TARGET_WEIGHT_PTE_APW_SAME_BATCH_V1",
            "producer": "run_covariance_target_weight_pte_apw_same_batch_v1.py",
            "scope": "covariance_target_weight_pte_apw_same_batch",
            "status": "partial",
            "evidence_mode": "hard",
            "covariance_target_weight_pte_chain_passed": False,
            "apw_chain_passed": False,
            "steps": steps,
        }
        write_json(summary_json, summary)
        return

    success_template = load_json(apw_root / "data" / "adjusted_position_weight_real_input_template_v1.json")
    formula_failure_template = load_json(apw_root / "data" / "adjusted_position_weight_real_input_formula_failure_template_v1.json")

    success_input_payload = build_apw_input(
        success_template,
        rel(tw_generation_success_json),
        rel(pte_same_batch_success_json),
        "same_batch_consumes_pte_same_batch_success_output",
    )
    formula_failure_input_payload = build_apw_input(
        formula_failure_template,
        rel(tw_generation_success_json),
        rel(pte_same_batch_success_json),
        "same_batch_formula_failure_consumes_pte_same_batch_success_output",
    )
    write_json(apw_success_input_json, success_input_payload)
    write_json(apw_formula_failure_input_json, formula_failure_input_payload)

    steps.append(
        run_step(
            "apw_same_batch_success",
            [
                python,
                str(apw_root / "generate_adjusted_position_weight_v1.py"),
                "--input-json",
                rel(apw_success_input_json),
                "--output-json",
                rel(apw_success_output_json),
            ],
            apw_success_output_json,
        )
    )
    steps.append(
        run_step(
            "apw_same_batch_formula_failure",
            [
                python,
                str(apw_root / "generate_adjusted_position_weight_v1.py"),
                "--input-json",
                rel(apw_formula_failure_input_json),
                "--output-json",
                rel(apw_formula_failure_output_json),
            ],
            apw_formula_failure_output_json,
        )
    )

    summary = {
        "run_id": "COVARIANCE_TARGET_WEIGHT_PTE_APW_SAME_BATCH_V1",
        "producer": "run_covariance_target_weight_pte_apw_same_batch_v1.py",
        "scope": "covariance_target_weight_pte_apw_same_batch",
        "status": "success" if all(step["step_passed"] is True for step in steps) else "partial",
        "evidence_mode": "hard",
        "covariance_target_weight_pte_chain_passed": steps[0]["step_passed"] is True,
        "apw_chain_passed": all(step["step_passed"] is True for step in steps[1:]),
        "same_batch_sources": {
            "target_weight_generation_json": rel(tw_generation_success_json),
            "portfolio_tracking_error_generation_json": rel(pte_same_batch_success_json),
        },
        "same_batch_formula_failure_alignment": {
            "apw_formula_failure_reason": steps[2]["payload_summary"].get("observed_abort_reason", ""),
            "expected_reason": "final_size_scalar_below_abort_threshold",
        },
        "steps": steps,
    }
    write_json(summary_json, summary)


if __name__ == "__main__":
    main()
