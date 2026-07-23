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
    if name == "covariance_target_weight_same_batch":
        return (
            payload.get("covariance_chain_passed") is True
            and payload.get("target_weight_chain_passed") is True
        ), "covariance_chain_passed_and_target_weight_chain_passed"
    if name == "pte_same_batch_success":
        return (
            payload.get("generation_executed") is True
            and payload.get("audit_fields", {}).get("covariance_matrix_consumed") is True
        ), "generation_executed_true_with_covariance_consumed"
    if name == "pte_same_batch_failure":
        return (
            payload.get("generation_executed") is False
            and payload.get("observed_abort_reason") == "missing_covariance_matrix_csv"
        ), "generation_executed_false_with_expected_abort_reason"
    return False, "unknown_step"


def convert_generated_weights(generated_weights: list[dict]) -> list[dict]:
    return [
        {
            "ticker": item["ticker"],
            "target_weight": item["target_weight"],
        }
        for item in generated_weights
    ]


def build_pte_input(
    template_payload: dict,
    generated_weights: list[dict],
    covariance_matrix_csv: str,
    audit_note: str,
) -> dict:
    payload = dict(template_payload)
    payload["target_weight_entries"] = convert_generated_weights(generated_weights)
    payload["covariance_matrix_csv"] = covariance_matrix_csv
    payload["audit_note"] = audit_note
    return payload


def main() -> None:
    python = sys.executable
    pte_root = ROOT / "02_runtime" / "a5_g5_portfolio_tracking_error_validation"
    summary_json = pte_root / "artifacts" / "portfolio_tracking_error_validation" / "covariance_target_weight_pte_same_batch_latest.json"
    tw_same_batch_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_target_weight_validation"
        / "artifacts"
        / "target_weight_validation"
        / "covariance_target_weight_same_batch_latest.json"
    )
    tw_generation_success_json = (
        ROOT
        / "02_runtime"
        / "a5_g5_target_weight_validation"
        / "artifacts"
        / "target_weight_validation"
        / "tw_actual_generation_success_latest.json"
    )
    pte_success_input_json = pte_root / "artifacts" / "portfolio_tracking_error_validation" / "pte_same_batch_success_input_latest.json"
    pte_failure_input_json = pte_root / "artifacts" / "portfolio_tracking_error_validation" / "pte_same_batch_failure_input_latest.json"
    pte_success_output_json = pte_root / "artifacts" / "portfolio_tracking_error_validation" / "pte_same_batch_success_latest.json"
    pte_failure_output_json = pte_root / "artifacts" / "portfolio_tracking_error_validation" / "pte_same_batch_failure_latest.json"

    steps: list[dict] = []

    tw_step = run_step(
        "covariance_target_weight_same_batch",
        [
            python,
            str(ROOT / "02_runtime" / "a5_g5_target_weight_validation" / "run_covariance_target_weight_same_batch_v1.py"),
        ],
        tw_same_batch_json,
    )
    steps.append(tw_step)

    if tw_step["step_passed"] is not True:
        summary = {
            "run_id": "COVARIANCE_TARGET_WEIGHT_PTE_SAME_BATCH_V1",
            "producer": "run_covariance_target_weight_pte_same_batch_v1.py",
            "scope": "covariance_target_weight_pte_same_batch",
            "status": "partial",
            "evidence_mode": "hard",
            "covariance_target_weight_chain_passed": False,
            "pte_chain_passed": False,
            "steps": steps,
        }
        write_json(summary_json, summary)
        return

    tw_generation_success = load_json(tw_generation_success_json)
    generated_weights = tw_generation_success.get("generated_weights", [])
    if not generated_weights:
        raise ValueError("missing_generated_weights_from_target_weight_same_batch")

    success_template = load_json(pte_root / "data" / "portfolio_tracking_error_real_input_template_v1.json")
    failure_template = load_json(pte_root / "data" / "portfolio_tracking_error_real_input_failure_template_v1.json")

    success_input_payload = build_pte_input(
        success_template,
        generated_weights,
        "02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_fresh/covariance_matrix_latest.csv",
        "same_batch_consumes_target_weight_generated_weights",
    )
    failure_input_payload = build_pte_input(
        failure_template,
        generated_weights,
        "",
        "same_batch_failure_consumes_target_weight_generated_weights",
    )
    write_json(pte_success_input_json, success_input_payload)
    write_json(pte_failure_input_json, failure_input_payload)

    steps.append(
        run_step(
            "pte_same_batch_success",
            [
                python,
                str(pte_root / "generate_portfolio_tracking_error_v1.py"),
                "--input-json",
                rel(pte_success_input_json),
                "--output-json",
                rel(pte_success_output_json),
            ],
            pte_success_output_json,
        )
    )
    steps.append(
        run_step(
            "pte_same_batch_failure",
            [
                python,
                str(pte_root / "generate_portfolio_tracking_error_v1.py"),
                "--input-json",
                rel(pte_failure_input_json),
                "--output-json",
                rel(pte_failure_output_json),
            ],
            pte_failure_output_json,
        )
    )

    summary = {
        "run_id": "COVARIANCE_TARGET_WEIGHT_PTE_SAME_BATCH_V1",
        "producer": "run_covariance_target_weight_pte_same_batch_v1.py",
        "scope": "covariance_target_weight_pte_same_batch",
        "status": "success" if all(step["step_passed"] is True for step in steps) else "partial",
        "evidence_mode": "hard",
        "covariance_target_weight_chain_passed": steps[0]["step_passed"] is True,
        "pte_chain_passed": all(step["step_passed"] is True for step in steps[1:]),
        "same_batch_target_weight_source": rel(tw_generation_success_json),
        "same_batch_generated_weight_count": len(generated_weights),
        "same_batch_failure_alignment": {
            "pte_failure_reason": steps[2]["payload_summary"].get("observed_abort_reason", ""),
            "expected_reason": "missing_covariance_matrix_csv",
        },
        "steps": steps,
    }
    write_json(summary_json, summary)


if __name__ == "__main__":
    main()
