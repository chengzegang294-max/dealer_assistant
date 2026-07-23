from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def abort_output(input_json: Path, abort_reason: str, payload: dict) -> dict:
    return {
        "run_id": payload.get("run_id", ""),
        "producer": "generate_adjusted_position_weight_v1.py",
        "scope": "adjusted_position_weight_generation",
        "status": "aborted",
        "evidence_mode": "hard",
        "input_json": str(input_json).replace("\\", "/"),
        "generation_executed": False,
        "observed_abort_reason": abort_reason,
        "payload": payload,
        "generated_weights": [],
    }


def generate(payload: dict, input_json: Path) -> dict:
    target_status = payload.get("target_weight_status", "")
    pte_status = payload.get("portfolio_tracking_error_status", "")
    target_generation_json = payload.get("target_weight_generation_json", "")
    pte_generation_json = payload.get("portfolio_tracking_error_generation_json", "")
    final_size_scalar = payload.get("final_size_scalar", None)
    final_size_scalar_method = payload.get("final_size_scalar_method", "")
    degrade_flags = payload.get("degrade_flags", [])

    if target_status != "verified_with_degraded_risk__upstream_min_integration_verified__not_output_passed":
        return abort_output(input_json, "upstream_target_weight_not_consumable", payload)
    if pte_status != "pass_conditions_frozen__not_output_passed":
        return abort_output(input_json, "upstream_tracking_error_not_consumable", payload)
    if target_generation_json == "":
        return abort_output(input_json, "missing_target_weight_generation_json", payload)
    if pte_generation_json == "":
        return abort_output(input_json, "missing_portfolio_tracking_error_generation_json", payload)
    if final_size_scalar in (None, ""):
        return abort_output(input_json, "missing_final_size_scalar", payload)
    scalar = float(final_size_scalar)
    if scalar <= 0.05:
        return abort_output(input_json, "final_size_scalar_below_abort_threshold", payload)
    if final_size_scalar_method == "":
        return abort_output(input_json, "missing_final_size_scalar_method", payload)
    if not isinstance(degrade_flags, list) or not degrade_flags:
        return abort_output(input_json, "missing_degrade_flags", payload)

    target_generation_path = Path(target_generation_json)
    if not target_generation_path.is_absolute():
        target_generation_path = (Path.cwd() / target_generation_path).resolve()
    if not target_generation_path.exists():
        return abort_output(input_json, "target_weight_generation_json_not_found", payload)

    pte_generation_path = Path(pte_generation_json)
    if not pte_generation_path.is_absolute():
        pte_generation_path = (Path.cwd() / pte_generation_path).resolve()
    if not pte_generation_path.exists():
        return abort_output(input_json, "portfolio_tracking_error_generation_json_not_found", payload)

    target_generation = load_json(target_generation_path)
    if target_generation.get("generation_executed") is not True:
        return abort_output(input_json, "target_weight_generation_not_executed", payload)
    target_weights = target_generation.get("generated_weights", [])
    if not isinstance(target_weights, list) or not target_weights:
        return abort_output(input_json, "empty_target_weight_entries", payload)

    pte_generation = load_json(pte_generation_path)
    if pte_generation.get("generation_executed") is not True:
        return abort_output(input_json, "portfolio_tracking_error_generation_not_executed", payload)
    portfolio_tracking_error = pte_generation.get("portfolio_tracking_error", None)

    adjusted_weights = []
    for item in target_weights:
        target_weight = float(item["target_weight"])
        adjusted_weight = round(target_weight * scalar, 6)
        adjusted_weights.append(
            {
                "ticker": item["ticker"],
                "target_weight": target_weight,
                "final_size_scalar": scalar,
                "adjusted_position_weight": adjusted_weight,
            }
        )

    return {
        "run_id": payload.get("run_id", ""),
        "producer": "generate_adjusted_position_weight_v1.py",
        "scope": "adjusted_position_weight_generation",
        "status": "success",
        "evidence_mode": "hard",
        "input_json": str(input_json).replace("\\", "/"),
        "generation_executed": True,
        "observed_abort_reason": "",
        "payload": payload,
        "generated_weights": adjusted_weights,
        "result_summary": {
            "weight_count": len(adjusted_weights),
            "gross_adjusted_weight": round(sum(item["adjusted_position_weight"] for item in adjusted_weights), 6),
            "formula_traceable": True,
            "final_size_scalar_method": final_size_scalar_method,
            "portfolio_tracking_error": portfolio_tracking_error,
            "target_weight_generation_json": str(target_generation_path).replace("\\", "/"),
            "portfolio_tracking_error_generation_json": str(pte_generation_path).replace("\\", "/"),
        },
        "audit_fields": {
            "success_sample_has_explicit_formula": True,
            "failure_path_has_abort_reason_contract": True,
            "degrade_flags_expanded": True,
            "upstream_generation_consumed": True,
            "forbidden_claim": "output_passed",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate minimal adjusted_position_weight output from degraded-chain real-input template."
    )
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    input_json = Path(args.input_json)
    output_json = Path(args.output_json)
    payload = load_json(input_json)
    output = generate(payload, input_json)

    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
