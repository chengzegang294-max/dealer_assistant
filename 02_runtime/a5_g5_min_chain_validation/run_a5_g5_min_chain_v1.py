from __future__ import annotations

import argparse
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
    }
    if output_json.exists():
        payload = load_json(output_json)
        result["status"] = payload.get("status", "")
        result["generation_executed"] = payload.get("generation_executed", False)
        result["observed_abort_reason"] = payload.get("observed_abort_reason", "")
        result["result_summary"] = payload.get("result_summary", {})
    else:
        result["status"] = "missing_output"
        result["generation_executed"] = False
        result["observed_abort_reason"] = "output_json_not_created"
        result["result_summary"] = {}
    return result


def build_paths(chain_case: str) -> dict[str, Path]:
    pte_input_name = "portfolio_tracking_error_real_input_template_v1.json"
    pte_output_name = "pte_actual_generation_success_latest.json"
    apw_input_name = "adjusted_position_weight_real_input_template_v1.json"
    apw_output_name = "apw_actual_generation_success_latest.json"

    if chain_case == "pte_failure":
        pte_input_name = "portfolio_tracking_error_real_input_failure_template_v1.json"
        pte_output_name = "pte_actual_generation_failure_latest.json"
    if chain_case == "apw_failure":
        apw_input_name = "adjusted_position_weight_real_input_formula_failure_template_v1.json"
        apw_output_name = "apw_actual_generation_failure_formula_latest.json"

    return {
        "tw_input": ROOT / "02_runtime" / "a5_g5_target_weight_validation" / "data" / "target_weight_real_input_template_v1.json",
        "tw_output": ROOT / "02_runtime" / "a5_g5_target_weight_validation" / "artifacts" / "target_weight_validation" / "tw_actual_generation_success_latest.json",
        "pte_input": ROOT / "02_runtime" / "a5_g5_portfolio_tracking_error_validation" / "data" / pte_input_name,
        "pte_output": ROOT / "02_runtime" / "a5_g5_portfolio_tracking_error_validation" / "artifacts" / "portfolio_tracking_error_validation" / pte_output_name,
        "apw_input": ROOT / "02_runtime" / "a5_g5_adjusted_position_weight_validation" / "data" / apw_input_name,
        "apw_output": ROOT / "02_runtime" / "a5_g5_adjusted_position_weight_validation" / "artifacts" / "adjusted_position_weight_validation" / apw_output_name,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run minimal chained G5 execution for target_weight -> portfolio_tracking_error -> adjusted_position_weight.")
    parser.add_argument("--chain-case", choices=["success", "pte_failure", "apw_failure"], required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    output_json = Path(args.output_json)
    paths = build_paths(args.chain_case)
    python = sys.executable
    steps: list[dict] = []

    tw_result = run_step(
        "target_weight_success",
        [
            python,
            str(ROOT / "02_runtime" / "a5_g5_target_weight_validation" / "generate_target_weight_v1.py"),
            "--input-json",
            rel(paths["tw_input"]),
            "--output-json",
            rel(paths["tw_output"]),
        ],
        paths["tw_output"],
    )
    steps.append(tw_result)

    pte_result = run_step(
        "portfolio_tracking_error_" + ("failure" if args.chain_case == "pte_failure" else "success"),
        [
            python,
            str(ROOT / "02_runtime" / "a5_g5_portfolio_tracking_error_validation" / "generate_portfolio_tracking_error_v1.py"),
            "--input-json",
            rel(paths["pte_input"]),
            "--output-json",
            rel(paths["pte_output"]),
        ],
        paths["pte_output"],
    )
    steps.append(pte_result)

    chain_completed = False
    final_step = "portfolio_tracking_error"
    final_status = pte_result.get("status", "")
    observed_abort_reason = pte_result.get("observed_abort_reason", "")

    if args.chain_case in {"success", "apw_failure"} and pte_result.get("generation_executed") is True:
        apw_result = run_step(
            "adjusted_position_weight_" + ("failure" if args.chain_case == "apw_failure" else "success"),
            [
                python,
                str(ROOT / "02_runtime" / "a5_g5_adjusted_position_weight_validation" / "generate_adjusted_position_weight_v1.py"),
                "--input-json",
                rel(paths["apw_input"]),
                "--output-json",
                rel(paths["apw_output"]),
            ],
            paths["apw_output"],
        )
        steps.append(apw_result)
        chain_completed = apw_result.get("generation_executed") is True and args.chain_case == "success"
        final_step = "adjusted_position_weight"
        final_status = apw_result.get("status", "")
        observed_abort_reason = apw_result.get("observed_abort_reason", "")

    summary = {
        "run_id": "A5_G5_MIN_CHAIN_" + args.chain_case.upper(),
        "producer": "run_a5_g5_min_chain_v1.py",
        "scope": "a5_g5_min_chain_validation",
        "chain_case": args.chain_case,
        "status": "success" if chain_completed else "partial",
        "chain_completed": chain_completed,
        "final_step": final_step,
        "final_status": final_status,
        "observed_abort_reason": observed_abort_reason,
        "steps": steps,
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
