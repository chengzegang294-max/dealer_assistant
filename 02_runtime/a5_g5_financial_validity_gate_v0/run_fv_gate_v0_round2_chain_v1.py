from __future__ import annotations

import argparse
import csv
import json
import statistics
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=True, indent=2)
        f.write("\n")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT)).replace("\\", "/")


def build_symbol_series(asset_rows: list[dict[str, str]], selected_symbols: list[str]) -> dict[str, list[dict[str, str]]]:
    by_symbol = {symbol: [] for symbol in selected_symbols}
    for row in asset_rows:
        symbol = row["symbol"]
        if symbol in by_symbol:
            by_symbol[symbol].append(row)
    for symbol, rows in by_symbol.items():
        rows.sort(key=lambda item: item["trade_date"])
        if len(rows) < 20:
            raise ValueError(f"insufficient_history_for_{symbol}")
    return by_symbol


def compute_trend_pullback_score(rows: list[dict[str, str]]) -> float:
    closes = [float(row["close"]) for row in rows]
    latest = closes[-1]
    prev = closes[-2]
    avg20 = statistics.fmean(closes[-20:])
    peak5 = max(closes[-5:])
    pullback_depth = (peak5 - latest) / peak5 if peak5 > 0 else 0.0
    rebound = latest / prev - 1.0 if prev > 0 else 0.0
    trend_strength = latest / avg20 - 1.0 if avg20 > 0 else 0.0

    raw_score = max(0.01, 0.6 * max(trend_strength, 0.0) + 0.3 * max(0.08 - pullback_depth, 0.0) + 0.1 * max(rebound, 0.0))
    return round(raw_score, 6)


def compute_breakout_score(rows: list[dict[str, str]]) -> float:
    closes = [float(row["close"]) for row in rows]
    highs = [float(row["high"]) for row in rows]
    volumes = [float(row["volume"]) for row in rows]
    latest = closes[-1]
    prev = closes[-2]
    breakout_base = max(highs[-20:-1])
    breakout_strength = latest / breakout_base - 1.0 if breakout_base > 0 else 0.0
    volume_base = statistics.fmean(volumes[-5:-1])
    volume_confirmation = volumes[-1] / volume_base - 1.0 if volume_base > 0 else 0.0
    trend_bias = latest / statistics.fmean(closes[-10:]) - 1.0
    close_change = latest / prev - 1.0 if prev > 0 else 0.0

    raw_score = max(
        0.01,
        0.5 * max(breakout_strength, 0.0)
        + 0.25 * max(volume_confirmation, 0.0)
        + 0.15 * max(trend_bias, 0.0)
        + 0.10 * max(close_change, 0.0),
    )
    return round(raw_score, 6)


def apply_filter_layer(rows: list[dict[str, str]], raw_score: float, filter_layer_id: str) -> float:
    closes = [float(row["close"]) for row in rows]
    highs = [float(row["high"]) for row in rows]
    volumes = [float(row["volume"]) for row in rows]
    latest = closes[-1]
    prev = closes[-2]
    avg20 = statistics.fmean(closes[-20:])
    avg5 = statistics.fmean(closes[-5:])
    peak5 = max(highs[-5:])
    pullback_depth = (peak5 - latest) / peak5 if peak5 > 0 else 0.0
    rebound = latest / prev - 1.0 if prev > 0 else 0.0
    trend_strength = latest / avg20 - 1.0 if avg20 > 0 else 0.0
    short_bias = latest / avg5 - 1.0 if avg5 > 0 else 0.0
    volume_base = statistics.fmean(volumes[-10:])
    volume_bias = volumes[-1] / volume_base - 1.0 if volume_base > 0 else 0.0

    if filter_layer_id in ("none", "", None):
        return round(raw_score, 6)

    if filter_layer_id == "basic_trend_stability_filter_v1":
        if trend_strength <= 0 or pullback_depth > 0.08:
            return 0.0
        return round(raw_score, 6)

    if filter_layer_id == "strict_trend_stability_filter_v2":
        if trend_strength <= 0.01:
            return 0.0
        if short_bias <= -0.01:
            return 0.0
        if pullback_depth > 0.05:
            return 0.0
        if rebound <= -0.005:
            return 0.0
        if volume_bias < -0.35:
            return 0.0
        return round(raw_score * 1.05, 6)

    if filter_layer_id == "strict_trend_stability_filter_v2_soft":
        penalty = 1.0
        if trend_strength <= 0.01:
            penalty *= 0.35
        if short_bias <= -0.01:
            penalty *= 0.55
        if pullback_depth > 0.05:
            penalty *= 0.45
        if rebound <= -0.005:
            penalty *= 0.65
        if volume_bias < -0.35:
            penalty *= 0.75
        if trend_strength <= -0.01:
            return 0.0
        return round(max(raw_score * penalty, 0.001), 6)

    if filter_layer_id == "basic_breakout_false_break_filter_v1":
        return round(raw_score, 6)

    raise ValueError(f"unsupported_filter_layer_id::{filter_layer_id}")


def apply_weight_logic(scored: list[dict[str, float | int | str]], weight_logic_id: str) -> list[dict[str, float | int | str]]:
    if weight_logic_id in ("alpha_rank_to_target_weight_proxy_v1", "filtered_alpha_rank_to_target_weight_proxy_v1"):
        return scored

    if weight_logic_id == "filtered_alpha_rank_to_target_weight_rank_decay_v2":
        decay_map = {1: 1.0, 2: 0.72, 3: 0.45}
        updated = []
        for item in scored:
            rank = int(item["rank"])
            updated_item = dict(item)
            updated_item["alpha_score_raw"] = item["alpha_score"]
            updated_item["alpha_score"] = round(float(item["alpha_score"]) * decay_map.get(rank, 0.35), 6)
            updated_item["rank_decay_factor"] = decay_map.get(rank, 0.35)
            updated.append(updated_item)
        return updated

    raise ValueError(f"unsupported_weight_logic_id::{weight_logic_id}")


def build_stage_prefix(params: dict) -> str:
    stage_tag = str(params.get("stage_tag", "fv_gate_v0")).upper()
    normalized = stage_tag.replace("-", "_")
    return normalized


def build_target_weight_input(params: dict, asset_rows: list[dict[str, str]], output_json: Path) -> dict:
    selected_symbols = ["000001.SZ", "600519.SH", "300750.SZ"]
    by_symbol = build_symbol_series(asset_rows, selected_symbols)
    signal_id = params["signal_combo"]["signal_hypothesis_id"]
    filter_layer_id = params["signal_combo"].get("filter_layer_id", "none")
    weight_logic_id = params["signal_combo"].get("weight_logic_id", "alpha_rank_to_target_weight_proxy_v1")
    stage_prefix = build_stage_prefix(params)

    scored = []
    for symbol in selected_symbols:
        if signal_id == "trend_pullback_confirmation_v1":
            score = compute_trend_pullback_score(by_symbol[symbol])
            if filter_layer_id == "strict_trend_stability_filter_v2":
                run_id = f"TW_{stage_prefix}_TREND_PULLBACK_FILTERED_V1"
            elif weight_logic_id == "filtered_alpha_rank_to_target_weight_rank_decay_v2":
                run_id = f"TW_{stage_prefix}_TREND_PULLBACK_RANK_DECAY_V2"
            else:
                run_id = f"TW_{stage_prefix}_TREND_PULLBACK_V1"
        elif signal_id == "breakout_close_volume_confirmation_v1":
            score = compute_breakout_score(by_symbol[symbol])
            run_id = f"TW_{stage_prefix}_BREAKOUT_CONFIRMATION_V1"
        else:
            raise ValueError(f"unsupported_signal_hypothesis_id::{signal_id}")
        filtered_score = apply_filter_layer(by_symbol[symbol], score, filter_layer_id)
        scored.append({"ticker": symbol, "alpha_score": filtered_score})
    scored.sort(key=lambda item: item["alpha_score"], reverse=True)
    for rank, item in enumerate(scored, start=1):
        item["rank"] = rank
    scored = apply_weight_logic(scored, weight_logic_id)

    payload = {
        "run_id": run_id,
        "producer": "run_fv_gate_v0_round2_chain_v1.py",
        "scope": "target_weight_real_input",
        "status": "template",
        "evidence_mode": "template",
        "as_of_date": max(row["trade_date"] for row in asset_rows),
        "input_contract": {
            "alpha_input_mode": "ranked_scores",
            "alpha_source_type": "contract_frozen_proxy",
            "alpha_source_id": params["signal_combo"]["signal_hypothesis_id"],
            "weight_logic_id": weight_logic_id,
            "constraint_set_id": "TW_MIN_CONSTRAINT_SET_V1",
            "risk_handling_mode": "degraded_risk_handling",
            "benchmark_id": "CSI300_PROXY",
            "universe_id": "ASHARE_TOP3_SAMPLE_V1",
        },
        "alpha_vector": scored,
        "constraint_set": {
            "weight_lower_bound": 0.0,
            "weight_upper_bound": 0.1,
            "long_only_flag": True,
            "turnover_limit": 0.25,
        },
        "expected_checks": {
            "non_empty": True,
            "within_bounds": True,
            "weight_sum_traceable": True,
            "abort_reason_empty": True,
        },
        "forbidden_claim": [
            "output_passed",
            "formalized_risk_model_ready",
            "implementation_ready",
        ],
    }
    dump_json(output_json, payload)
    return payload


def run_python(command: list[str]) -> None:
    subprocess.run([sys.executable, *command], check=True, cwd=ROOT)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--runtime-params-json",
        default="02_runtime/a5_g5_financial_validity_gate_v0/fv_gate_v0_runtime_params_round2_template_v1.json",
    )
    args = parser.parse_args()

    params_path = (ROOT / args.runtime_params_json).resolve()
    params = load_json(params_path)
    input_paths = params["input_paths"]
    output_paths = params["output_paths"]

    asset_rows = read_csv_rows((ROOT / input_paths["asset_ohlcv_csv"]).resolve())
    baseline_pte_input = load_json((ROOT / input_paths["baseline_pte_input_json"]).resolve())
    baseline_apw_input = load_json((ROOT / input_paths["baseline_apw_input_json"]).resolve())
    signal_id = params["signal_combo"]["signal_hypothesis_id"]
    stage_prefix = build_stage_prefix(params)

    round2_tw_input_json = (ROOT / output_paths["round2_target_weight_input_json"]).resolve()
    round2_tw_generation_json = (ROOT / output_paths["round2_target_weight_generation_json"]).resolve()
    round2_pte_input_json = (ROOT / output_paths["round2_pte_input_json"]).resolve()
    round2_pte_generation_json = (ROOT / output_paths["round2_pte_generation_json"]).resolve()
    round2_apw_input_json = (ROOT / output_paths["round2_apw_input_json"]).resolve()
    round2_apw_generation_json = (ROOT / output_paths["round2_apw_generation_json"]).resolve()

    build_target_weight_input(params, asset_rows, round2_tw_input_json)
    run_python(
        [
            "02_runtime/a5_g5_target_weight_validation/generate_target_weight_v1.py",
            "--input-json",
            rel(round2_tw_input_json),
            "--output-json",
            rel(round2_tw_generation_json),
        ]
    )

    tw_generation = load_json(round2_tw_generation_json)
    pte_input = dict(baseline_pte_input)
    if signal_id == "trend_pullback_confirmation_v1":
        pte_input["run_id"] = f"PTE_{stage_prefix}_TREND_PULLBACK_V1"
        pte_input["audit_note"] = f"{stage_prefix.lower()}_consumes_trend_pullback_target_weight"
        apw_run_id = f"APW_{stage_prefix}_TREND_PULLBACK_V1"
        apw_audit_note = f"{stage_prefix.lower()}_consumes_pte_output"
    else:
        pte_input["run_id"] = f"PTE_{stage_prefix}_BREAKOUT_CONFIRMATION_V1"
        pte_input["audit_note"] = f"{stage_prefix.lower()}_consumes_breakout_target_weight"
        apw_run_id = f"APW_{stage_prefix}_BREAKOUT_CONFIRMATION_V1"
        apw_audit_note = f"{stage_prefix.lower()}_consumes_pte_output"
    pte_input["target_weight_entries"] = [
        {"ticker": item["ticker"], "target_weight": item["target_weight"]} for item in tw_generation["generated_weights"]
    ]
    dump_json(round2_pte_input_json, pte_input)

    run_python(
        [
            "02_runtime/a5_g5_portfolio_tracking_error_validation/generate_portfolio_tracking_error_v1.py",
            "--input-json",
            rel(round2_pte_input_json),
            "--output-json",
            rel(round2_pte_generation_json),
        ]
    )

    apw_input = dict(baseline_apw_input)
    apw_input["run_id"] = apw_run_id
    apw_input["audit_note"] = apw_audit_note
    apw_input["target_weight_generation_json"] = rel(round2_tw_generation_json)
    apw_input["portfolio_tracking_error_generation_json"] = rel(round2_pte_generation_json)
    apw_override = params.get("apw_override", {})
    if apw_override:
        if "final_size_scalar" in apw_override:
            apw_input["final_size_scalar"] = apw_override["final_size_scalar"]
        if "final_size_scalar_method" in apw_override:
            apw_input["final_size_scalar_method"] = apw_override["final_size_scalar_method"]
        if "degrade_flags_append" in apw_override:
            base_flags = list(apw_input.get("degrade_flags", []))
            for flag in apw_override["degrade_flags_append"]:
                if flag not in base_flags:
                    base_flags.append(flag)
            apw_input["degrade_flags"] = base_flags
    dump_json(round2_apw_input_json, apw_input)

    run_python(
        [
            "02_runtime/a5_g5_adjusted_position_weight_validation/generate_adjusted_position_weight_v1.py",
            "--input-json",
            rel(round2_apw_input_json),
            "--output-json",
            rel(round2_apw_generation_json),
        ]
    )

    round2_params = json.loads(json.dumps(params))
    round2_params["input_paths"]["same_batch_apw_json"] = rel(round2_apw_generation_json)
    round2_params["input_paths"]["apw_success_json"] = rel(round2_apw_generation_json)
    dump_json(params_path, round2_params)

    run_python(
        [
            "02_runtime/a5_g5_financial_validity_gate_v0/run_fv_gate_v0_minimal_backtest_v1.py",
            "--runtime-params-json",
            rel(params_path),
        ]
    )


if __name__ == "__main__":
    main()
