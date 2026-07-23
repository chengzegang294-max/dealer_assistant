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
        "producer": "generate_target_weight_v1.py",
        "scope": "target_weight_generation",
        "status": "aborted",
        "evidence_mode": "hard",
        "input_json": str(input_json).replace("\\", "/"),
        "generation_executed": False,
        "observed_abort_reason": abort_reason,
        "payload": payload,
        "generated_weights": [],
    }


def normalize_scores(alpha_vector: list[dict]) -> list[dict]:
    cleaned = []
    for item in alpha_vector:
        score = float(item["alpha_score"])
        if score < 0:
            score = 0.0
        cleaned.append(
            {
                "ticker": item["ticker"],
                "alpha_score": score,
                "rank": item["rank"],
            }
        )
    return cleaned


def build_weights(alpha_vector: list[dict], weight_upper_bound: float) -> list[dict]:
    cleaned = normalize_scores(alpha_vector)
    score_sum = sum(item["alpha_score"] for item in cleaned)
    if score_sum <= 0:
        raise ValueError("non_positive_alpha_sum")

    max_gross = min(1.0, weight_upper_bound * len(cleaned))
    weights: list[dict] = []
    for item in cleaned:
        raw_weight = (item["alpha_score"] / score_sum) * max_gross
        target_weight = min(weight_upper_bound, round(raw_weight, 6))
        weights.append(
            {
                "ticker": item["ticker"],
                "target_weight": target_weight,
                "alpha_score": item["alpha_score"],
                "rank": item["rank"],
            }
        )
    return weights


def generate(payload: dict, input_json: Path) -> dict:
    input_contract = payload.get("input_contract", {})
    alpha_vector = payload.get("alpha_vector", [])
    constraint_set = payload.get("constraint_set", {})

    if input_contract.get("constraint_set_id", "") == "":
        return abort_output(input_json, "missing_constraint_set", payload)
    if input_contract.get("alpha_source_type") != "contract_frozen_proxy":
        return abort_output(input_json, "untraceable_alpha_source", payload)
    if not isinstance(alpha_vector, list) or not alpha_vector:
        return abort_output(input_json, "empty_alpha_vector", payload)
    if not isinstance(constraint_set, dict) or not constraint_set:
        return abort_output(input_json, "missing_constraint_set_body", payload)
    if constraint_set.get("long_only_flag") is not True:
        return abort_output(input_json, "long_only_not_enforced", payload)

    weight_upper_bound = float(constraint_set.get("weight_upper_bound", 0.0))
    if weight_upper_bound <= 0:
        return abort_output(input_json, "invalid_weight_upper_bound", payload)

    weights = build_weights(alpha_vector, weight_upper_bound)
    return {
        "run_id": payload.get("run_id", ""),
        "producer": "generate_target_weight_v1.py",
        "scope": "target_weight_generation",
        "status": "success",
        "evidence_mode": "hard",
        "input_json": str(input_json).replace("\\", "/"),
        "generation_executed": True,
        "observed_abort_reason": "",
        "payload": payload,
        "generated_weights": weights,
        "result_summary": {
            "weight_count": len(weights),
            "non_empty": len(weights) > 0,
            "within_bounds": all(0.0 <= item["target_weight"] <= weight_upper_bound for item in weights),
            "weight_sum_traceable": True,
            "gross_weight": round(sum(item["target_weight"] for item in weights), 6),
            "allocation_method": "alpha_proportional_with_single_name_cap",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate minimal target_weight output from real-input template.")
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
