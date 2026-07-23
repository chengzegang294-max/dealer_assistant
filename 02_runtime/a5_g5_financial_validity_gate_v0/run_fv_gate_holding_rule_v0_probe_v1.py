from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HOLDING_RULE_BACKTEST = (
    ROOT
    / "02_runtime"
    / "a5_g5_financial_validity_gate_v0"
    / "run_fv_gate_holding_rule_minimal_backtest_v1.py"
)


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
    fieldnames = ["side", "metric", "value"]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def scenario_suffix(holding_rule: dict) -> str:
    holding_rule_id = str(holding_rule["holding_rule_id"])
    if holding_rule_id == "fixed_period_rebalance_v0":
        return f"{holding_rule_id}_{int(holding_rule['rebalance_every_trade_days'])}d"
    return holding_rule_id


def set_scenario_params(template: dict, base_params: dict) -> dict:
    params = json.loads(json.dumps(base_params))
    suffix = scenario_suffix(template["holding_rule"])
    scenario_tag = f"{template['scenario_tag_prefix']}_{suffix}"
    output_dir = f"02_runtime/a5_g5_financial_validity_gate_v0/artifacts/fv_gate_holding_rule_v0/{scenario_tag}"

    params["run_id"] = f"A5_G5_{scenario_tag.upper()}"
    params["scope"] = "a5_g5_financial_validity_gate_holding_rule_v0"
    params["stage_tag"] = scenario_tag
    params["entry_shape"] = "v1_sample_boundary_frozen_contract_holding_rule_probe"
    params["evaluation"]["evaluation_card_id"] = f"holding_rule_v0_{suffix}"
    params["evaluation"]["baseline_scorecard_json"] = template["baseline_scorecard_json"]
    params["holding_rule"] = template["holding_rule"]
    params["output_paths"] = {
        "scorecard_json": f"{output_dir}/{scenario_tag}_scorecard_latest.json",
        "scorecard_tsv": f"{output_dir}/{scenario_tag}_scorecard_latest.tsv",
    }
    return params


def pick_label(scorecard: dict) -> str:
    net_total = float(scorecard["net_metrics"]["total_return"])
    holdout_total = float(scorecard["holdout_metrics"]["net"]["total_return"])
    active_total = float(scorecard["net_metrics"]["active_total_return"])
    if net_total > 0 and holdout_total > 0 and active_total > 0:
        return "holding_rule_stable__still_need_evidence"
    return "holding_rule_fragile__still_need_evidence"


def build_summary(template: dict, baseline: dict, scenario: dict, scenario_scorecard_path: Path) -> dict:
    baseline_metrics = {
        "net_total_return": baseline["net_metrics"]["total_return"],
        "holdout_net_total_return": baseline["holdout_metrics"]["net"]["total_return"],
        "net_active_total_return": baseline["net_metrics"]["active_total_return"],
        "net_max_drawdown": baseline["net_metrics"]["max_drawdown"],
        "entry_turnover": baseline["turnover"]["entry_turnover"],
    }
    scenario_metrics = {
        "net_total_return": scenario["net_metrics"]["total_return"],
        "holdout_net_total_return": scenario["holdout_metrics"]["net"]["total_return"],
        "net_active_total_return": scenario["net_metrics"]["active_total_return"],
        "net_max_drawdown": scenario["net_metrics"]["max_drawdown"],
        "entry_turnover": scenario["turnover"]["entry_turnover"],
        "rebalance_turnover_total": scenario["turnover"]["rebalance_turnover_total"],
        "rebalance_event_count": scenario["turnover"]["rebalance_event_count"],
    }
    deltas = {
        "delta_net_total_return": round(
            float(scenario_metrics["net_total_return"]) - float(baseline_metrics["net_total_return"]), 8
        ),
        "delta_holdout_net_total_return": round(
            float(scenario_metrics["holdout_net_total_return"])
            - float(baseline_metrics["holdout_net_total_return"]),
            8,
        ),
        "delta_net_active_total_return": round(
            float(scenario_metrics["net_active_total_return"])
            - float(baseline_metrics["net_active_total_return"]),
            8,
        ),
        "delta_net_max_drawdown": round(
            float(scenario_metrics["net_max_drawdown"]) - float(baseline_metrics["net_max_drawdown"]), 8
        ),
    }
    label = pick_label(scenario)
    return {
        "run_id": template["run_id"],
        "producer": "run_fv_gate_holding_rule_v0_probe_v1.py",
        "scope": template["scope"],
        "status": "success",
        "evidence_mode": "hard",
        "window_label": template["window_label"],
        "baseline_scorecard_json": template["baseline_scorecard_json"],
        "holding_rule": template["holding_rule"],
        "scenario_count": 1,
        "holding_rule_label": label,
        "baseline_metrics": baseline_metrics,
        "scenario_metrics": scenario_metrics,
        "delta_vs_baseline": deltas,
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
            "probe_template_json": template["input_trace"]["probe_template_json"],
            "scenario_scorecard_json": rel(scenario_scorecard_path),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--probe-template-json",
        default="02_runtime/a5_g5_financial_validity_gate_v0/fv_gate_holding_rule_v0_probe_template_v1.json",
    )
    args = parser.parse_args()

    probe_template_path = (ROOT / args.probe_template_json).resolve()
    template = load_json(probe_template_path)
    base_params_path = (ROOT / template["base_runtime_params_json"]).resolve()
    base_params = load_json(base_params_path)
    baseline_scorecard_path = (ROOT / template["baseline_scorecard_json"]).resolve()
    baseline = load_json(baseline_scorecard_path)

    scenario_params = set_scenario_params(template, base_params)
    scenario_params_dir = (ROOT / template["output_paths"]["scenario_params_dir"]).resolve()
    scenario_params_dir.mkdir(parents=True, exist_ok=True)
    suffix = scenario_suffix(template["holding_rule"])
    scenario_params_path = scenario_params_dir / f"fv_gate_holding_rule_v0_{suffix}_params_latest.json"
    dump_json(scenario_params_path, scenario_params)

    subprocess.run(
        [
            sys.executable,
            str(HOLDING_RULE_BACKTEST),
            "--runtime-params-json",
            rel(scenario_params_path),
        ],
        cwd=ROOT,
        check=True,
    )

    scenario_scorecard_path = (ROOT / scenario_params["output_paths"]["scorecard_json"]).resolve()
    scenario = load_json(scenario_scorecard_path)

    template["input_trace"] = {"probe_template_json": rel(probe_template_path)}
    summary_payload = build_summary(template, baseline, scenario, scenario_scorecard_path)

    summary_json_path = (ROOT / template["output_paths"]["summary_json"]).resolve()
    summary_tsv_path = (ROOT / template["output_paths"]["summary_tsv"]).resolve()
    dump_json(summary_json_path, summary_payload)

    tsv_rows: list[dict[str, object]] = []
    for metric, value in summary_payload["baseline_metrics"].items():
        tsv_rows.append({"side": "baseline", "metric": metric, "value": value})
    for metric, value in summary_payload["scenario_metrics"].items():
        tsv_rows.append({"side": "scenario", "metric": metric, "value": value})
    for metric, value in summary_payload["delta_vs_baseline"].items():
        tsv_rows.append({"side": "delta", "metric": metric, "value": value})
    tsv_rows.append(
        {
            "side": "label",
            "metric": "holding_rule_label",
            "value": summary_payload["holding_rule_label"],
        }
    )
    write_tsv(summary_tsv_path, tsv_rows)


if __name__ == "__main__":
    main()
