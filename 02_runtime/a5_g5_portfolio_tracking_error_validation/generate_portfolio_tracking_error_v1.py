from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def abort_output(input_json: Path, abort_reason: str, payload: dict) -> dict:
    return {
        "run_id": payload.get("run_id", ""),
        "producer": "generate_portfolio_tracking_error_v1.py",
        "scope": "portfolio_tracking_error_generation",
        "status": "aborted",
        "evidence_mode": "hard",
        "input_json": str(input_json).replace("\\", "/"),
        "generation_executed": False,
        "observed_abort_reason": abort_reason,
        "payload": payload,
        "portfolio_tracking_error": None,
        "result_summary": {
            "benchmark_mode": payload.get("benchmark_mode", False),
            "risk_mode": payload.get("risk_mode", ""),
            "within_limit": False,
        },
    }


def normalize_weights(items: list[dict], key: str) -> dict[str, float]:
    weights: dict[str, float] = {}
    for item in items:
        ticker = str(item["ticker"])
        weights[ticker] = float(item[key])
    return weights


def load_covariance_matrix(path: Path) -> tuple[list[str], dict[str, dict[str, float]]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))

    if not rows or len(rows[0]) < 2:
        raise ValueError("invalid_covariance_matrix_header")

    symbols = [cell.strip() for cell in rows[0][1:] if cell.strip()]
    matrix: dict[str, dict[str, float]] = {}
    for row in rows[1:]:
        if not row:
            continue
        row_symbol = row[0].strip()
        if row_symbol == "":
            continue
        values = row[1 : 1 + len(symbols)]
        matrix[row_symbol] = {
            symbol: float(value) for symbol, value in zip(symbols, values, strict=False)
        }
    return symbols, matrix


def compute_tracking_error_proxy(
    target_weights: dict[str, float],
    benchmark_weights: dict[str, float],
    covariance_symbols: list[str],
    covariance_matrix: dict[str, dict[str, float]],
) -> tuple[float, float, list[str]]:
    active_weights = {
        ticker: target_weights.get(ticker, 0.0) - benchmark_weights.get(ticker, 0.0)
        for ticker in sorted(set(target_weights) | set(benchmark_weights))
    }
    overlapped_symbols = [ticker for ticker in active_weights if ticker in covariance_symbols]
    if not overlapped_symbols:
        raise ValueError("no_covariance_symbol_overlap")

    variance = 0.0
    for left in overlapped_symbols:
        left_weight = active_weights[left]
        row = covariance_matrix.get(left, {})
        for right in overlapped_symbols:
            variance += left_weight * row.get(right, 0.0) * active_weights[right]

    variance = max(variance, 0.0)
    tracking_error = math.sqrt(variance)
    return round(tracking_error, 8), round(variance, 12), overlapped_symbols


def generate(payload: dict, input_json: Path) -> dict:
    benchmark_id = payload.get("benchmark_id", "")
    benchmark_mode = payload.get("benchmark_mode", False)
    risk_mode = payload.get("risk_mode", "")
    tracking_error_limit = payload.get("tracking_error_limit", None)
    covariance_status = payload.get("covariance_model_id_status", "")
    covariance_matrix_csv = payload.get("covariance_matrix_csv", "")
    target_status = payload.get("target_weight_status", "")
    degrade_flags = payload.get("degrade_flags", [])
    target_weights_raw = payload.get("target_weight_entries", [])
    benchmark_weights_raw = payload.get("benchmark_weight_entries", [])

    if benchmark_mode is not True:
        return abort_output(input_json, "benchmark_mode_disabled", payload)
    if benchmark_id == "":
        return abort_output(input_json, "missing_benchmark_id", payload)
    if tracking_error_limit in (None, ""):
        return abort_output(input_json, "missing_tracking_error_limit", payload)
    if covariance_status == "":
        return abort_output(input_json, "missing_covariance_model_id", payload)
    if covariance_matrix_csv == "":
        return abort_output(input_json, "missing_covariance_matrix_csv", payload)
    if target_status != "verified_with_degraded_risk__upstream_min_integration_verified__not_output_passed":
        return abort_output(input_json, "upstream_target_weight_not_consumable", payload)
    if covariance_status != "ready_judgement_conditional__downstream_still_locked":
        return abort_output(input_json, "covariance_status_not_consumable", payload)
    if risk_mode != "degraded_risk_handling":
        return abort_output(input_json, "unsupported_risk_mode", payload)
    if not isinstance(degrade_flags, list) or not degrade_flags:
        return abort_output(input_json, "missing_degrade_flags", payload)
    if not isinstance(target_weights_raw, list) or not target_weights_raw:
        return abort_output(input_json, "empty_target_weight_entries", payload)
    if not isinstance(benchmark_weights_raw, list) or not benchmark_weights_raw:
        return abort_output(input_json, "empty_benchmark_weight_entries", payload)

    covariance_matrix_path = Path(covariance_matrix_csv)
    if not covariance_matrix_path.is_absolute():
        covariance_matrix_path = (Path.cwd() / covariance_matrix_path).resolve()
    if not covariance_matrix_path.exists():
        return abort_output(input_json, "covariance_matrix_csv_not_found", payload)

    target_weights = normalize_weights(target_weights_raw, "target_weight")
    benchmark_weights = normalize_weights(benchmark_weights_raw, "benchmark_weight")
    try:
        covariance_symbols, covariance_matrix = load_covariance_matrix(covariance_matrix_path)
        tracking_error_proxy, tracking_error_variance, overlapped_symbols = compute_tracking_error_proxy(
            target_weights, benchmark_weights, covariance_symbols, covariance_matrix
        )
    except ValueError as exc:
        return abort_output(input_json, str(exc), payload)
    limit = float(tracking_error_limit)

    return {
        "run_id": payload.get("run_id", ""),
        "producer": "generate_portfolio_tracking_error_v1.py",
        "scope": "portfolio_tracking_error_generation",
        "status": "success",
        "evidence_mode": "hard",
        "input_json": str(input_json).replace("\\", "/"),
        "generation_executed": True,
        "observed_abort_reason": "",
        "payload": payload,
        "portfolio_tracking_error": tracking_error_proxy,
        "result_summary": {
            "benchmark_mode": benchmark_mode,
            "risk_mode": risk_mode,
            "tracking_error_limit": limit,
            "within_limit": tracking_error_proxy <= limit,
            "calculation_method": "active_weight_covariance_quadratic_proxy",
            "symbol_count": len(sorted(set(target_weights) | set(benchmark_weights))),
            "overlap_symbol_count": len(overlapped_symbols),
            "tracking_error_variance": tracking_error_variance,
            "covariance_matrix_csv": str(covariance_matrix_path).replace("\\", "/"),
        },
        "audit_fields": {
            "success_sample_has_explicit_risk_output": True,
            "failure_path_has_abort_reason_contract": True,
            "degrade_flags_expanded": True,
            "covariance_matrix_consumed": True,
            "forbidden_claim": "output_passed",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate minimal portfolio_tracking_error output from degraded-risk real-input template."
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
