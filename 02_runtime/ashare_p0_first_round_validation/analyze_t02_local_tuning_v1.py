from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT_CSV = ROOT / "artifacts" / "t02_real_input_build" / "t02_real_input_candidate_latest.csv"
DEFAULT_LAYER_TSV = ROOT / "artifacts" / "t02_layer_stability" / "t02_symbol_layer_stability_latest.tsv"
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "t02_local_tuning"


SCENARIOS: list[dict[str, Any]] = [
    {
        "scenario_label": "baseline_3pct_2d",
        "main_flow_ratio_threshold": 0.03,
        "min_consecutive_days": 2,
    },
    {
        "scenario_label": "looser_ratio_2_5pct_2d",
        "main_flow_ratio_threshold": 0.025,
        "min_consecutive_days": 2,
    },
    {
        "scenario_label": "looser_days_3pct_1d",
        "main_flow_ratio_threshold": 0.03,
        "min_consecutive_days": 1,
    },
    {
        "scenario_label": "tighter_ratio_3_5pct_2d",
        "main_flow_ratio_threshold": 0.035,
        "min_consecutive_days": 2,
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run local threshold tuning scenarios for T02 weak-penetration layers."
    )
    parser.add_argument("--input-csv", default=str(DEFAULT_INPUT_CSV))
    parser.add_argument("--layer-tsv", default=str(DEFAULT_LAYER_TSV))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    return parser.parse_args()


def read_csv_rows(path: Path, delimiter: str = ",") -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=delimiter))


def write_tsv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def safe_float(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def normalize_ratio(value: float) -> float:
    return value / 100.0 if abs(value) > 1 else value


def scan_rows(
    rows: list[dict[str, str]],
    main_ratio_threshold: float,
    min_consecutive_days: int,
) -> dict[str, Any]:
    sorted_rows = sorted(rows, key=lambda row: (row["trade_date"], row["symbol"]))
    streak_by_symbol: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"direction": "neutral", "count": 0}
    )
    trigger_rows = 0
    trigger_symbols: set[str] = set()

    for row in sorted_rows:
        symbol = row["symbol"]
        flow_value = safe_float(row.get("main_fund_net_inflow"))
        ratio_value_raw = safe_float(row.get("main_fund_net_inflow_ratio"))
        if flow_value is None or ratio_value_raw is None:
            continue
        ratio_value = normalize_ratio(ratio_value_raw)
        if abs(ratio_value) < main_ratio_threshold or flow_value == 0:
            streak_by_symbol[symbol] = {"direction": "neutral", "count": 0}
            continue

        direction = "inflow" if flow_value > 0 else "outflow"
        streak = streak_by_symbol[symbol]
        if streak["direction"] == direction:
            streak["count"] += 1
        else:
            streak["direction"] = direction
            streak["count"] = 1

        if streak["count"] >= min_consecutive_days:
            trigger_rows += 1
            trigger_symbols.add(symbol)

    rows_scanned = len(sorted_rows)
    return {
        "rows_scanned": rows_scanned,
        "trigger_rows": trigger_rows,
        "trigger_symbols": len(trigger_symbols),
        "trigger_density": (trigger_rows / rows_scanned) if rows_scanned else 0.0,
    }


def main() -> int:
    args = parse_args()
    input_csv = Path(args.input_csv)
    layer_tsv = Path(args.layer_tsv)
    output_dir = Path(args.output_dir)

    summary_path = output_dir / "t02_local_tuning_summary_latest.json"
    scenario_path = output_dir / "t02_local_tuning_scenario_comparison_latest.tsv"
    recommendation_path = output_dir / "t02_local_tuning_recommendation_latest.tsv"

    metadata: dict[str, Any] = {
        "producer": "analyze_t02_local_tuning_v1.py",
        "scope": "A股 P0 首轮离线验证 T02 局部阈值微调试算",
        "status": "started",
        "input_csv": str(input_csv).replace("\\", "/"),
        "layer_tsv": str(layer_tsv).replace("\\", "/"),
        "output_dir": str(output_dir).replace("\\", "/"),
        "scenario_labels": [scenario["scenario_label"] for scenario in SCENARIOS],
    }

    missing_inputs = [
        str(path).replace("\\", "/") for path in [input_csv, layer_tsv] if not path.exists()
    ]
    if missing_inputs:
        metadata["status"] = "failed"
        metadata["failure_reason"] = "missing_input_files"
        metadata["missing_inputs"] = missing_inputs
        write_json(summary_path, metadata)
        return 2

    input_rows = read_csv_rows(input_csv)
    layer_rows = read_csv_rows(layer_tsv, delimiter="\t")

    symbol_meta = {row["symbol"]: row for row in layer_rows}
    growth_symbols = {
        row["symbol"] for row in layer_rows if row.get("macro_bucket", "") == "成长科技"
    }
    low_vol_symbols = {
        row["symbol"] for row in layer_rows if row.get("flow_volatility_bucket", "") == "low"
    }
    finance_symbols = {
        row["symbol"] for row in layer_rows if row.get("macro_bucket", "") == "金融"
    }
    weak_intersection_symbols = growth_symbols & low_vol_symbols
    all_symbols = set(symbol_meta.keys())

    groups = [
        {
            "group_label": "all_sample",
            "group_type": "reference",
            "symbols": all_symbols,
        },
        {
            "group_label": "finance_reference",
            "group_type": "reference",
            "symbols": finance_symbols,
        },
        {
            "group_label": "growth_tech",
            "group_type": "focus",
            "symbols": growth_symbols,
        },
        {
            "group_label": "low_flow_vol",
            "group_type": "focus",
            "symbols": low_vol_symbols,
        },
        {
            "group_label": "growth_tech_low_flow_vol",
            "group_type": "focus",
            "symbols": weak_intersection_symbols,
        },
    ]

    rows_by_symbol: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in input_rows:
        symbol = row.get("symbol", "")
        if symbol:
            rows_by_symbol[symbol].append(row)

    group_result_map: dict[str, list[dict[str, Any]]] = {}
    scenario_rows: list[dict[str, Any]] = []
    recommendation_rows: list[dict[str, Any]] = []

    for group in groups:
        group_symbols = sorted(group["symbols"])
        group_rows: list[dict[str, str]] = []
        for symbol in group_symbols:
            group_rows.extend(rows_by_symbol.get(symbol, []))

        baseline_density = None
        best_focus_row: dict[str, Any] | None = None
        scenario_results_for_group: list[dict[str, Any]] = []
        for scenario in SCENARIOS:
            result = scan_rows(
                group_rows,
                main_ratio_threshold=float(scenario["main_flow_ratio_threshold"]),
                min_consecutive_days=int(scenario["min_consecutive_days"]),
            )
            row = {
                "group_label": group["group_label"],
                "group_type": group["group_type"],
                "symbol_count": len(group_symbols),
                "scenario_label": scenario["scenario_label"],
                "main_flow_ratio_threshold": scenario["main_flow_ratio_threshold"],
                "min_consecutive_days": scenario["min_consecutive_days"],
                "rows_scanned": result["rows_scanned"],
                "trigger_rows": result["trigger_rows"],
                "trigger_symbols": result["trigger_symbols"],
                "trigger_density": round(result["trigger_density"], 4),
                "density_delta_vs_baseline": 0.0,
            }
            if scenario["scenario_label"] == "baseline_3pct_2d":
                baseline_density = result["trigger_density"]
            scenario_results_for_group.append(row)

        if baseline_density is None:
            baseline_density = 0.0

        for row in scenario_results_for_group:
            delta = float(row["trigger_density"]) - baseline_density
            row["density_delta_vs_baseline"] = round(delta, 4)
        group_result_map[group["group_label"]] = scenario_results_for_group

    global_delta_by_scenario = {
        row["scenario_label"]: float(row["density_delta_vs_baseline"])
        for row in group_result_map.get("all_sample", [])
    }

    for group in groups:
        scenario_results_for_group = group_result_map[group["group_label"]]
        baseline_row = next(
            row for row in scenario_results_for_group if row["scenario_label"] == "baseline_3pct_2d"
        )
        baseline_density = float(baseline_row["trigger_density"])
        best_focus_row = None

        for row in scenario_results_for_group:
            global_delta = global_delta_by_scenario.get(row["scenario_label"], 0.0)
            excess_delta = float(row["density_delta_vs_baseline"]) - global_delta
            row["global_density_delta"] = round(global_delta, 4)
            row["excess_delta_vs_global"] = round(excess_delta, 4)
            scenario_rows.append(row)

        focus_candidates = []
        for row in scenario_results_for_group:
            if row["scenario_label"] == "baseline_3pct_2d":
                continue
            if float(row["global_density_delta"]) > 0.1:
                continue
            focus_candidates.append(row)

        if focus_candidates:
            best_focus_row = sorted(
                focus_candidates,
                key=lambda row: (
                    -float(row["excess_delta_vs_global"]),
                    -float(row["density_delta_vs_baseline"]),
                    row["scenario_label"],
                ),
            )[0]

        recommendation = "keep_baseline"
        reason = "baseline remains default"
        if group["group_type"] == "focus" and best_focus_row is not None:
            delta = float(best_focus_row["density_delta_vs_baseline"])
            excess_delta = float(best_focus_row["excess_delta_vs_global"])
            if excess_delta >= 0.03 and delta >= 0.04:
                recommendation = "candidate_branch"
                reason = "group lift is meaningful and remains stronger than all-sample uplift"
            elif excess_delta >= 0.015 and delta >= 0.03:
                recommendation = "watchlist"
                reason = "group lift is somewhat better than all-sample uplift, but not decisive yet"
            else:
                recommendation = "keep_baseline"
                reason = "local lift is not sufficiently better than the all-sample uplift"
        elif group["group_type"] == "focus":
            reason = "all non-baseline scenarios over-loosen the full sample too much"

        recommendation_rows.append(
            {
                "group_label": group["group_label"],
                "group_type": group["group_type"],
                "symbol_count": int(baseline_row["symbol_count"]),
                "baseline_density": round(baseline_density, 4),
                "best_scenario_label": (
                    best_focus_row["scenario_label"] if best_focus_row is not None else "baseline_3pct_2d"
                ),
                "best_scenario_density": (
                    best_focus_row["trigger_density"] if best_focus_row is not None else round(baseline_density, 4)
                ),
                "density_delta_vs_baseline": (
                    best_focus_row["density_delta_vs_baseline"] if best_focus_row is not None else 0.0
                ),
                "excess_delta_vs_global": (
                    best_focus_row["excess_delta_vs_global"] if best_focus_row is not None else 0.0
                ),
                "recommendation": recommendation,
                "reason": reason,
            }
        )

    metadata["status"] = "success"
    metadata["rows_scanned"] = len(input_rows)
    metadata["symbols_covered"] = len(symbol_meta)
    metadata["groups_tested"] = [group["group_label"] for group in groups]
    metadata["focus_groups"] = [group["group_label"] for group in groups if group["group_type"] == "focus"]
    metadata["output_files"] = {
        "summary_json": str(summary_path).replace("\\", "/"),
        "scenario_comparison_tsv": str(scenario_path).replace("\\", "/"),
        "recommendation_tsv": str(recommendation_path).replace("\\", "/"),
    }

    write_tsv(
        scenario_path,
        scenario_rows,
        [
            "group_label",
            "group_type",
            "symbol_count",
            "scenario_label",
            "main_flow_ratio_threshold",
            "min_consecutive_days",
            "rows_scanned",
            "trigger_rows",
            "trigger_symbols",
            "trigger_density",
            "density_delta_vs_baseline",
            "global_density_delta",
            "excess_delta_vs_global",
        ],
    )
    write_tsv(
        recommendation_path,
        recommendation_rows,
        [
            "group_label",
            "group_type",
            "symbol_count",
            "baseline_density",
            "best_scenario_label",
            "best_scenario_density",
            "density_delta_vs_baseline",
            "excess_delta_vs_global",
            "recommendation",
            "reason",
        ],
    )
    write_json(summary_path, metadata)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
