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
    if name in {"covariance_current_fresh", "covariance_adjacent_fresh"}:
        return payload.get("fresh_run_passed") is True, "fresh_run_passed"
    if name == "covariance_stability":
        return payload.get("stability_check_passed") is True, "stability_check_passed"
    if name in {
        "target_weight_validation_success",
        "target_weight_validation_failure",
        "target_weight_real_input_success",
        "target_weight_real_input_failure",
    }:
        return payload.get("validation_passed") is True, "validation_passed"
    if name == "target_weight_actual_generation_success":
        return payload.get("generation_executed") is True, "generation_executed_true"
    if name == "target_weight_actual_generation_failure":
        return (
            payload.get("generation_executed") is False
            and payload.get("observed_abort_reason") == "missing_constraint_set"
        ), "generation_executed_false_with_expected_abort_reason"
    return False, "unknown_step"


def main() -> None:
    output_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_target_weight_validation"
        / "artifacts"
        / "target_weight_validation"
        / "covariance_target_weight_same_batch_latest.json"
    )
    python = sys.executable
    steps: list[dict] = []

    current_fresh_json = ROOT / "02_runtime" / "a5_g5_covariance_bodyrun" / "artifacts" / "covariance_bodyrun_fresh" / "covariance_bodyrun_fresh_latest.json"
    current_matrix_csv = ROOT / "02_runtime" / "a5_g5_covariance_bodyrun" / "artifacts" / "covariance_bodyrun_fresh" / "covariance_matrix_latest.csv"
    adjacent_fresh_json = ROOT / "02_runtime" / "a5_g5_covariance_bodyrun" / "artifacts" / "covariance_adjacent_window" / "fresh" / "covariance_bodyrun_fresh_adjacent_latest.json"
    adjacent_matrix_csv = ROOT / "02_runtime" / "a5_g5_covariance_bodyrun" / "artifacts" / "covariance_adjacent_window" / "fresh" / "covariance_matrix_adjacent_latest.csv"
    stability_json = ROOT / "02_runtime" / "a5_g5_covariance_bodyrun" / "artifacts" / "covariance_stability" / "covariance_stability_check_latest.json"

    commands = [
        (
            "covariance_current_fresh",
            [
                python,
                str(ROOT / "02_runtime" / "a5_g5_covariance_bodyrun" / "run_covariance_bodyrun_fresh_v1.py"),
                "--runtime-params-json",
                "02_runtime/a5_g5_covariance_bodyrun/covariance_bodyrun_runtime_params_template_v1.json",
                "--active-returns-csv",
                "02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_returns_input/active_returns_panel_latest.csv",
                "--output-json",
                rel(current_fresh_json),
                "--matrix-csv",
                rel(current_matrix_csv),
            ],
            current_fresh_json,
        ),
        (
            "covariance_adjacent_fresh",
            [
                python,
                str(ROOT / "02_runtime" / "a5_g5_covariance_bodyrun" / "run_covariance_bodyrun_fresh_v1.py"),
                "--runtime-params-json",
                "02_runtime/a5_g5_covariance_bodyrun/covariance_bodyrun_runtime_params_template_v1.json",
                "--active-returns-csv",
                "02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/returns/active_returns_panel_adjacent_latest.csv",
                "--output-json",
                rel(adjacent_fresh_json),
                "--matrix-csv",
                rel(adjacent_matrix_csv),
            ],
            adjacent_fresh_json,
        ),
        (
            "covariance_stability",
            [
                python,
                str(ROOT / "02_runtime" / "a5_g5_covariance_bodyrun" / "run_covariance_stability_check_v1.py"),
                "--current-fresh-json",
                rel(current_fresh_json),
                "--current-matrix-csv",
                rel(current_matrix_csv),
                "--adjacent-fresh-json",
                rel(adjacent_fresh_json),
                "--adjacent-matrix-csv",
                rel(adjacent_matrix_csv),
                "--output-json",
                rel(stability_json),
            ],
            stability_json,
        ),
        (
            "target_weight_validation_success",
            [
                python,
                str(ROOT / "02_runtime" / "a5_g5_target_weight_validation" / "run_target_weight_validation_v1.py"),
                "--case",
                "success",
                "--template-json",
                "02_runtime/a5_g5_target_weight_validation/data/target_weight_validation_success_template_v1.json",
                "--output-json",
                "02_runtime/a5_g5_target_weight_validation/artifacts/target_weight_validation/tw_validation_success_latest.json",
            ],
            ROOT / "02_runtime" / "a5_g5_target_weight_validation" / "artifacts" / "target_weight_validation" / "tw_validation_success_latest.json",
        ),
        (
            "target_weight_validation_failure",
            [
                python,
                str(ROOT / "02_runtime" / "a5_g5_target_weight_validation" / "run_target_weight_validation_v1.py"),
                "--case",
                "failure",
                "--template-json",
                "02_runtime/a5_g5_target_weight_validation/data/target_weight_validation_failure_template_v1.json",
                "--output-json",
                "02_runtime/a5_g5_target_weight_validation/artifacts/target_weight_validation/tw_validation_failure_latest.json",
            ],
            ROOT / "02_runtime" / "a5_g5_target_weight_validation" / "artifacts" / "target_weight_validation" / "tw_validation_failure_latest.json",
        ),
        (
            "target_weight_real_input_success",
            [
                python,
                str(ROOT / "02_runtime" / "a5_g5_target_weight_validation" / "run_target_weight_validation_v1.py"),
                "--case",
                "real_input_success",
                "--template-json",
                "02_runtime/a5_g5_target_weight_validation/data/target_weight_real_input_success_case_template_v1.json",
                "--output-json",
                "02_runtime/a5_g5_target_weight_validation/artifacts/target_weight_validation/tw_real_input_success_latest.json",
            ],
            ROOT / "02_runtime" / "a5_g5_target_weight_validation" / "artifacts" / "target_weight_validation" / "tw_real_input_success_latest.json",
        ),
        (
            "target_weight_real_input_failure",
            [
                python,
                str(ROOT / "02_runtime" / "a5_g5_target_weight_validation" / "run_target_weight_validation_v1.py"),
                "--case",
                "real_input_failure",
                "--template-json",
                "02_runtime/a5_g5_target_weight_validation/data/target_weight_real_input_failure_case_template_v1.json",
                "--output-json",
                "02_runtime/a5_g5_target_weight_validation/artifacts/target_weight_validation/tw_real_input_failure_latest.json",
            ],
            ROOT / "02_runtime" / "a5_g5_target_weight_validation" / "artifacts" / "target_weight_validation" / "tw_real_input_failure_latest.json",
        ),
        (
            "target_weight_actual_generation_success",
            [
                python,
                str(ROOT / "02_runtime" / "a5_g5_target_weight_validation" / "generate_target_weight_v1.py"),
                "--input-json",
                "02_runtime/a5_g5_target_weight_validation/data/target_weight_real_input_template_v1.json",
                "--output-json",
                "02_runtime/a5_g5_target_weight_validation/artifacts/target_weight_validation/tw_actual_generation_success_latest.json",
            ],
            ROOT / "02_runtime" / "a5_g5_target_weight_validation" / "artifacts" / "target_weight_validation" / "tw_actual_generation_success_latest.json",
        ),
        (
            "target_weight_actual_generation_failure",
            [
                python,
                str(ROOT / "02_runtime" / "a5_g5_target_weight_validation" / "generate_target_weight_v1.py"),
                "--input-json",
                "02_runtime/a5_g5_target_weight_validation/data/target_weight_real_input_failure_template_v1.json",
                "--output-json",
                "02_runtime/a5_g5_target_weight_validation/artifacts/target_weight_validation/tw_actual_generation_failure_latest.json",
            ],
            ROOT / "02_runtime" / "a5_g5_target_weight_validation" / "artifacts" / "target_weight_validation" / "tw_actual_generation_failure_latest.json",
        ),
    ]

    for name, command, step_output_json in commands:
        steps.append(run_step(name, command, step_output_json))

    covariance_chain_passed = all(
        step["step_passed"] is True
        for step in steps
        if step["step"].startswith("covariance_")
    )
    target_weight_chain_passed = all(
        step["step_passed"] is True
        for step in steps
        if step["step"].startswith("target_weight_")
    )
    template_failure_reason = steps[4]["payload_summary"].get("payload", {}).get("observed_abort_reason", "")
    real_input_failure_reason = steps[6]["payload_summary"].get("payload", {}).get("observed_abort_reason", "")
    actual_generation_failure_reason = steps[8]["payload_summary"].get("observed_abort_reason", "")
    failure_reason_alignment = {
        "template_level_reason": template_failure_reason,
        "real_input_reason": real_input_failure_reason,
        "actual_generation_reason": actual_generation_failure_reason,
        "real_input_and_generation_aligned": real_input_failure_reason == actual_generation_failure_reason == "missing_constraint_set",
    }

    summary = {
        "run_id": "COVARIANCE_TARGET_WEIGHT_SAME_BATCH_V1",
        "producer": "run_covariance_target_weight_same_batch_v1.py",
        "scope": "covariance_target_weight_same_batch",
        "status": "success" if covariance_chain_passed and target_weight_chain_passed else "partial",
        "evidence_mode": "hard",
        "covariance_chain_passed": covariance_chain_passed,
        "target_weight_chain_passed": target_weight_chain_passed,
        "failure_reason_alignment": failure_reason_alignment,
        "steps": steps,
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
