from __future__ import annotations

import argparse
import csv
import json
import math
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


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT)).replace("\\", "/")


def safe_float(value: object, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    return float(value)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def max_drawdown(daily_returns: list[float]) -> float:
    equity = 1.0
    peak = 1.0
    worst = 0.0
    for value in daily_returns:
        equity *= 1.0 + value
        peak = max(peak, equity)
        if peak > 0:
            worst = min(worst, equity / peak - 1.0)
    return worst


def summarize_metrics(daily_returns: list[float], benchmark_returns: list[float]) -> dict:
    if not daily_returns:
        raise ValueError("no_daily_returns_for_metric_summary")

    equity = 1.0
    positive_days = 0
    for value in daily_returns:
        equity *= 1.0 + value
        if value > 0:
            positive_days += 1

    benchmark_equity = 1.0
    for value in benchmark_returns:
        benchmark_equity *= 1.0 + value

    avg_daily = sum(daily_returns) / len(daily_returns)
    variance = sum((value - avg_daily) ** 2 for value in daily_returns) / len(daily_returns)
    volatility = math.sqrt(variance)

    return {
        "trade_days": len(daily_returns),
        "positive_days": positive_days,
        "avg_daily_return": round(avg_daily, 8),
        "volatility": round(volatility, 8),
        "total_return": round(equity - 1.0, 8),
        "max_drawdown": round(max_drawdown(daily_returns), 8),
        "benchmark_total_return": round(benchmark_equity - 1.0, 8),
        "active_total_return": round((equity - 1.0) - (benchmark_equity - 1.0), 8),
    }


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["section", "metric", "value"]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def build_daily_series(
    asset_rows: list[dict[str, str]],
    benchmark_rows: list[dict[str, str]],
    weights: dict[str, float],
) -> list[dict[str, float | str]]:
    per_date: dict[str, dict[str, float]] = {}
    for row in asset_rows:
        symbol = row["symbol"]
        if symbol not in weights:
            continue
        trade_date = row["trade_date"]
        entry = per_date.setdefault(trade_date, {"portfolio_return": 0.0})
        pre_close = safe_float(row.get("pre_close"))
        close = safe_float(row.get("close"))
        if pre_close == 0:
            raise ValueError(f"invalid_pre_close_for_{symbol}_{trade_date}")
        asset_return = close / pre_close - 1.0
        entry["portfolio_return"] += weights[symbol] * asset_return

    benchmark_map = {
        row["trade_date"]: safe_float(row.get("benchmark_return_1d")) for row in benchmark_rows
    }

    series: list[dict[str, float | str]] = []
    for trade_date in sorted(per_date.keys()):
        if trade_date not in benchmark_map:
            raise ValueError(f"missing_benchmark_return_for_{trade_date}")
        series.append(
            {
                "trade_date": trade_date,
                "portfolio_return": round(per_date[trade_date]["portfolio_return"], 10),
                "benchmark_return": round(benchmark_map[trade_date], 10),
            }
        )
    return series


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--runtime-params-json",
        default="02_runtime/a5_g5_financial_validity_gate_v0/fv_gate_v0_runtime_params_template_v1.json",
    )
    args = parser.parse_args()

    params_path = (ROOT / args.runtime_params_json).resolve()
    params = load_json(params_path)

    if params.get("cost_model", {}).get("model_id") != "degraded_fixed_cost":
        raise ValueError("only_degraded_fixed_cost_is_allowed_for_fv_gate_v0")

    input_paths = params["input_paths"]
    output_paths = params["output_paths"]

    same_batch_json = load_json((ROOT / input_paths["same_batch_apw_json"]).resolve())
    apw_success_json = load_json((ROOT / input_paths["apw_success_json"]).resolve())
    benchmark_json = load_json((ROOT / input_paths["covariance_fresh_json"]).resolve())
    asset_rows = read_csv_rows((ROOT / input_paths["asset_ohlcv_csv"]).resolve())
    benchmark_rows = read_csv_rows((ROOT / input_paths["benchmark_series_csv"]).resolve())

    generated_weights = apw_success_json.get("generated_weights", [])
    if not generated_weights:
        raise ValueError("missing_generated_weights_in_apw_success_json")

    weights = {
        row["ticker"]: safe_float(row["adjusted_position_weight"])
        for row in generated_weights
    }
    gross_exposure = sum(weights.values())
    if gross_exposure <= 0:
        raise ValueError("non_positive_gross_exposure")

    daily_series = build_daily_series(asset_rows, benchmark_rows, weights)
    if len(daily_series) < 10:
        raise ValueError("insufficient_trade_days_for_fv_gate_v0")

    holdout_days = int(params["holdout_rule"]["holdout_trade_days"])
    if holdout_days <= 0 or holdout_days >= len(daily_series):
        raise ValueError("invalid_holdout_trade_days")

    in_sample_series = daily_series[:-holdout_days]
    holdout_series = daily_series[-holdout_days:]

    gross_daily_returns = [float(row["portfolio_return"]) for row in daily_series]
    gross_benchmark_returns = [float(row["benchmark_return"]) for row in daily_series]
    net_daily_returns = gross_daily_returns.copy()

    one_way_cost_bps = safe_float(params["cost_model"]["one_way_cost_bps"])
    entry_cost = gross_exposure * (one_way_cost_bps / 10000.0)
    net_daily_returns[0] = round(net_daily_returns[0] - entry_cost, 10)

    in_sample_gross = [float(row["portfolio_return"]) for row in in_sample_series]
    in_sample_benchmark = [float(row["benchmark_return"]) for row in in_sample_series]
    holdout_gross = [float(row["portfolio_return"]) for row in holdout_series]
    holdout_benchmark = [float(row["benchmark_return"]) for row in holdout_series]

    in_sample_net = net_daily_returns[: len(in_sample_series)]
    holdout_net = net_daily_returns[len(in_sample_series) :]

    scorecard = {
        "run_id": params["run_id"],
        "producer": "run_fv_gate_v0_minimal_backtest_v1.py",
        "scope": params["scope"],
        "status": "success",
        "evidence_mode": "hard",
        "signal_combo": params.get("signal_combo", {}),
        "evaluation": params.get("evaluation", {}),
        "consumed_artifact_id": same_batch_json["run_id"],
        "window_start": daily_series[0]["trade_date"],
        "window_end": daily_series[-1]["trade_date"],
        "benchmark_id": benchmark_json["benchmark_id"],
        "holdout_split_rule": {
            "mode": params["holdout_rule"]["mode"],
            "holdout_trade_days": holdout_days,
            "in_sample_trade_days": len(in_sample_series),
        },
        "cost_model": params["cost_model"],
        "gross_metrics": summarize_metrics(gross_daily_returns, gross_benchmark_returns),
        "net_metrics": summarize_metrics(net_daily_returns, gross_benchmark_returns),
        "in_sample_metrics": {
            "gross": summarize_metrics(in_sample_gross, in_sample_benchmark),
            "net": summarize_metrics(in_sample_net, in_sample_benchmark),
        },
        "holdout_metrics": {
            "gross": summarize_metrics(holdout_gross, holdout_benchmark),
            "net": summarize_metrics(holdout_net, holdout_benchmark),
        },
        "turnover": {
            "entry_turnover": round(gross_exposure, 8),
            "exit_turnover": 0.0,
            "turnover_assumption": "single_entry_static_weight_minimal_backtest",
        },
        "run_status": "success",
        "abort_reason": "",
        "gate_result": "FV_gate_v0_evidence_produced",
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
            "runtime_params_json": rel(params_path),
            "same_batch_apw_json": input_paths["same_batch_apw_json"],
            "apw_success_json": input_paths["apw_success_json"],
            "asset_ohlcv_csv": input_paths["asset_ohlcv_csv"],
            "benchmark_series_csv": input_paths["benchmark_series_csv"],
            "covariance_fresh_json": input_paths["covariance_fresh_json"],
        },
    }

    scorecard_json_path = (ROOT / output_paths["scorecard_json"]).resolve()
    scorecard_tsv_path = (ROOT / output_paths["scorecard_tsv"]).resolve()
    dump_json(scorecard_json_path, scorecard)

    tsv_rows: list[dict[str, object]] = []
    for section_name, section_payload in [
        ("gross_metrics", scorecard["gross_metrics"]),
        ("net_metrics", scorecard["net_metrics"]),
        ("in_sample_gross", scorecard["in_sample_metrics"]["gross"]),
        ("in_sample_net", scorecard["in_sample_metrics"]["net"]),
        ("holdout_gross", scorecard["holdout_metrics"]["gross"]),
        ("holdout_net", scorecard["holdout_metrics"]["net"]),
        ("turnover", scorecard["turnover"]),
    ]:
        for metric, value in section_payload.items():
            tsv_rows.append({"section": section_name, "metric": metric, "value": value})
    write_tsv(scorecard_tsv_path, tsv_rows)


if __name__ == "__main__":
    main()
