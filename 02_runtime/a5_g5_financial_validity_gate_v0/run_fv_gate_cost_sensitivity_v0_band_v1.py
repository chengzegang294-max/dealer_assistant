from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MINIMAL_BACKTEST = ROOT / "02_runtime" / "a5_g5_financial_validity_gate_v0" / "run_fv_gate_v0_minimal_backtest_v1.py"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=True, indent=2)
        f.write("\n")


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT)).replace("\\", "/")


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["scenario_id", "cost_bps", "metric", "value"]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def set_scenario_paths(base_params: dict, scenario_tag: str) -> dict:
    params = json.loads(json.dumps(base_params))
    params["run_id"] = f"A5_G5_{scenario_tag.upper()}"
    params["scope"] = "a5_g5_financial_validity_gate_cost_sensitivity_v0"
    params["stage_tag"] = scenario_tag
    params["entry_shape"] = "v1_sample_boundary_frozen_contract_cost_band_replay"

    output_dir = (
        f"02_runtime/a5_g5_financial_validity_gate_v0/artifacts/"
        f"fv_gate_cost_sensitivity_v0/{scenario_tag}"
    )
    params["output_paths"] = {
        "round2_target_weight_input_json": f"{output_dir}/{scenario_tag}_target_weight_input_latest.json",
        "round2_target_weight_generation_json": f"{output_dir}/{scenario_tag}_target_weight_generation_latest.json",
        "round2_pte_input_json": f"{output_dir}/{scenario_tag}_pte_input_latest.json",
        "round2_pte_generation_json": f"{output_dir}/{scenario_tag}_pte_generation_latest.json",
        "round2_apw_input_json": f"{output_dir}/{scenario_tag}_apw_input_latest.json",
        "round2_apw_generation_json": f"{output_dir}/{scenario_tag}_apw_generation_latest.json",
        "scorecard_json": f"{output_dir}/{scenario_tag}_scorecard_latest.json",
        "scorecard_tsv": f"{output_dir}/{scenario_tag}_scorecard_latest.tsv",
    }
    return params


def summarize_scenario(scorecard: dict, cost_bps: float, scenario_id: str) -> dict:
    return {
        "scenario_id": scenario_id,
        "cost_bps": cost_bps,
        "net_total_return": scorecard["net_metrics"]["total_return"],
        "holdout_net_total_return": scorecard["holdout_metrics"]["net"]["total_return"],
        "net_active_total_return": scorecard["net_metrics"]["active_total_return"],
        "net_max_drawdown": scorecard["net_metrics"]["max_drawdown"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--band-template-json",
        default="02_runtime/a5_g5_financial_validity_gate_v0/fv_gate_cost_sensitivity_v0_band_template_v1.json",
    )
    args = parser.parse_args()

    band_template_path = (ROOT / args.band_template_json).resolve()
    band = load_json(band_template_path)
    base_params_path = (ROOT / band["base_runtime_params_json"]).resolve()
    base_params = load_json(base_params_path)

    scenario_params_dir = (ROOT / band["output_paths"]["scenario_params_dir"]).resolve()
    scenario_params_dir.mkdir(parents=True, exist_ok=True)

    scenarios: list[dict[str, object]] = []
    tsv_rows: list[dict[str, object]] = []
    scenario_scorecard_paths: list[str] = []

    for raw_cost in band["cost_bps_band"]:
        cost_bps = float(raw_cost)
        scenario_suffix = str(int(cost_bps)) if cost_bps.is_integer() else str(cost_bps).replace(".", "p")
        scenario_tag = f"{band['scenario_tag_prefix']}_{scenario_suffix}bps"
        scenario_params = set_scenario_paths(base_params, scenario_tag)
        scenario_params["cost_model"]["one_way_cost_bps"] = cost_bps
        scenario_params["evaluation"]["evaluation_card_id"] = f"cost_sensitivity_v0_{scenario_suffix}bps"

        scenario_params_path = scenario_params_dir / f"{scenario_tag}_params_latest.json"
        dump_json(scenario_params_path, scenario_params)

        subprocess.run(
            [
                sys.executable,
                str(MINIMAL_BACKTEST),
                "--runtime-params-json",
                rel(scenario_params_path),
            ],
            cwd=ROOT,
            check=True,
        )

        scorecard_path = (ROOT / scenario_params["output_paths"]["scorecard_json"]).resolve()
        scorecard = load_json(scorecard_path)
        scenario_scorecard_paths.append(rel(scorecard_path))

        summary = summarize_scenario(scorecard, cost_bps, scenario_tag)
        scenarios.append(summary)
        for metric_name in [
            "net_total_return",
            "holdout_net_total_return",
            "net_active_total_return",
            "net_max_drawdown",
        ]:
            tsv_rows.append(
                {
                    "scenario_id": scenario_tag,
                    "cost_bps": cost_bps,
                    "metric": metric_name,
                    "value": summary[metric_name],
                }
            )

    net_totals = [float(row["net_total_return"]) for row in scenarios]
    holdout_totals = [float(row["holdout_net_total_return"]) for row in scenarios]
    active_totals = [float(row["net_active_total_return"]) for row in scenarios]
    drawdowns = [float(row["net_max_drawdown"]) for row in scenarios]

    if min(net_totals) > 0 and min(holdout_totals) > 0 and min(active_totals) > 0:
        band_label = "cost_band_stable__still_need_evidence"
    else:
        band_label = "cost_band_fragile__still_need_evidence"

    summary_payload = {
        "run_id": band["run_id"],
        "producer": "run_fv_gate_cost_sensitivity_v0_band_v1.py",
        "scope": band["scope"],
        "status": "success",
        "evidence_mode": "hard",
        "selected_window_label": band["window_label"],
        "base_runtime_params_json": band["base_runtime_params_json"],
        "cost_bps_band": band["cost_bps_band"],
        "scenario_count": len(scenarios),
        "band_label": band_label,
        "scenarios": scenarios,
        "band_summary": {
            "min_net_total_return": round(min(net_totals), 8),
            "max_net_total_return": round(max(net_totals), 8),
            "min_holdout_net_total_return": round(min(holdout_totals), 8),
            "max_holdout_net_total_return": round(max(holdout_totals), 8),
            "min_net_active_total_return": round(min(active_totals), 8),
            "max_net_active_total_return": round(max(active_totals), 8),
            "worst_net_max_drawdown": round(min(drawdowns), 8),
            "best_net_max_drawdown": round(max(drawdowns), 8),
        },
        "forbidden_claim_check": {
            "financial_valid_claimed": False,
            "output_passed_claimed": False,
            "ready_to_deploy_claimed": False,
        },
        "need_evidence_items": [
            "financial-valid",
            "output_passed",
            "strict_out_of_time_generalization",
            "full_impact_model",
            "robustness_suite",
        ],
        "input_trace": {
            "band_template_json": rel(band_template_path),
            "scenario_scorecard_paths": scenario_scorecard_paths,
        },
    }

    summary_json_path = (ROOT / band["output_paths"]["summary_json"]).resolve()
    summary_tsv_path = (ROOT / band["output_paths"]["summary_tsv"]).resolve()
    dump_json(summary_json_path, summary_payload)
    write_tsv(summary_tsv_path, tsv_rows)


if __name__ == "__main__":
    main()
