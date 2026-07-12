from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT_CSV = ROOT / "artifacts" / "t02_real_input_build" / "t02_real_input_candidate_latest.csv"
DEFAULT_LAYER_TSV = ROOT / "artifacts" / "t02_layer_stability" / "t02_symbol_layer_stability_latest.tsv"
DEFAULT_TUNING_RECOMMEND_TSV = (
    ROOT / "artifacts" / "t02_local_tuning" / "t02_local_tuning_recommendation_latest.tsv"
)
DEFAULT_CONFIRM_FILTER_TSV = (
    ROOT / "artifacts" / "t02_confirmation_filter" / "t02_confirmation_filter_recommendation_latest.tsv"
)
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "t02_candidate_branch"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Decide whether the watchlist candidate branch should remain watchlist or upgrade to micro-adjust."
    )
    parser.add_argument("--input-csv", default=str(DEFAULT_INPUT_CSV))
    parser.add_argument("--layer-tsv", default=str(DEFAULT_LAYER_TSV))
    parser.add_argument("--tuning-recommendation-tsv", default=str(DEFAULT_TUNING_RECOMMEND_TSV))
    parser.add_argument("--confirmation-filter-tsv", default=str(DEFAULT_CONFIRM_FILTER_TSV))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--baseline-threshold", type=float, default=0.03)
    parser.add_argument("--candidate-threshold", type=float, default=0.025)
    parser.add_argument("--min-consecutive-days", type=int, default=2)
    return parser.parse_args()


def read_rows(path: Path, delimiter: str = ",") -> list[dict[str, str]]:
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


def sign_label(value: float | None) -> str:
    if value is None:
        return "missing"
    if value > 0:
        return "inflow"
    if value < 0:
        return "outflow"
    return "flat"


def scenario_filter_builder(name: str) -> Callable[[dict[str, Any]], bool]:
    if name == "candidate_no_filter":
        return lambda row: True
    if name == "candidate_exclude_g03":
        return lambda row: row.get("market_regime_label", "") != "G03_震荡"
    if name == "candidate_require_northbound_align":
        return lambda row: row.get("northbound_direction", "") == row.get("direction", "")
    if name == "candidate_exclude_g03_and_northbound_align":
        return lambda row: (
            row.get("market_regime_label", "") != "G03_震荡"
            and row.get("northbound_direction", "") == row.get("direction", "")
        )
    raise ValueError(f"Unsupported scenario: {name}")


def build_trigger_rows(
    rows: list[dict[str, str]],
    main_ratio_threshold: float,
    min_consecutive_days: int,
) -> list[dict[str, Any]]:
    sorted_rows = sorted(rows, key=lambda row: (row["trade_date"], row["symbol"]))
    streak_by_symbol: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"direction": "neutral", "count": 0}
    )
    result: list[dict[str, Any]] = []

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
            northbound_value = safe_float(row.get("northbound_net_inflow"))
            result.append(
                {
                    "trade_date": row["trade_date"],
                    "symbol": symbol,
                    "direction": direction,
                    "market_regime_label": row.get("market_regime_label", ""),
                    "northbound_direction": sign_label(northbound_value),
                }
            )
    return result


def main() -> int:
    args = parse_args()
    input_csv = Path(args.input_csv)
    layer_tsv = Path(args.layer_tsv)
    tuning_tsv = Path(args.tuning_recommendation_tsv)
    filter_tsv = Path(args.confirmation_filter_tsv)
    output_dir = Path(args.output_dir)

    summary_path = output_dir / "t02_candidate_branch_summary_latest.json"
    decision_path = output_dir / "t02_candidate_branch_decision_latest.tsv"

    metadata: dict[str, Any] = {
        "producer": "analyze_t02_candidate_branch_v1.py",
        "scope": "A股 P0 首轮离线验证 T02 watchlist 候选分支裁决",
        "status": "started",
        "input_csv": str(input_csv).replace("\\", "/"),
        "layer_tsv": str(layer_tsv).replace("\\", "/"),
        "tuning_recommendation_tsv": str(tuning_tsv).replace("\\", "/"),
        "confirmation_filter_tsv": str(filter_tsv).replace("\\", "/"),
        "baseline_threshold": args.baseline_threshold,
        "candidate_threshold": args.candidate_threshold,
        "min_consecutive_days": args.min_consecutive_days,
    }

    missing_inputs = [
        str(path).replace("\\", "/")
        for path in [input_csv, layer_tsv, tuning_tsv, filter_tsv]
        if not path.exists()
    ]
    if missing_inputs:
        metadata["status"] = "failed"
        metadata["failure_reason"] = "missing_input_files"
        metadata["missing_inputs"] = missing_inputs
        write_json(summary_path, metadata)
        return 2

    input_rows = read_rows(input_csv)
    layer_rows = read_rows(layer_tsv, delimiter="\t")
    tuning_rows = read_rows(tuning_tsv, delimiter="\t")
    filter_rows = read_rows(filter_tsv, delimiter="\t")

    growth_symbols = {
        row["symbol"] for row in layer_rows if row.get("macro_bucket", "") == "成长科技"
    }
    low_vol_symbols = {
        row["symbol"] for row in layer_rows if row.get("flow_volatility_bucket", "") == "low"
    }
    group_symbols_map = {
        "low_flow_vol": low_vol_symbols,
        "growth_tech_low_flow_vol": growth_symbols & low_vol_symbols,
    }

    tuning_map = {row["group_label"]: row for row in tuning_rows}
    filter_map = {row["group_label"]: row for row in filter_rows}
    watchlist_groups = [
        row["group_label"] for row in tuning_rows if row.get("recommendation", "") == "watchlist"
    ]

    baseline_trigger_rows = build_trigger_rows(
        input_rows,
        main_ratio_threshold=args.baseline_threshold,
        min_consecutive_days=args.min_consecutive_days,
    )
    candidate_trigger_rows = build_trigger_rows(
        input_rows,
        main_ratio_threshold=args.candidate_threshold,
        min_consecutive_days=args.min_consecutive_days,
    )

    baseline_by_symbol: dict[str, list[dict[str, Any]]] = defaultdict(list)
    candidate_by_symbol: dict[str, list[dict[str, Any]]] = defaultdict(list)
    input_count_by_symbol: Counter[str] = defaultdict(int)  # type: ignore[assignment]

    for row in baseline_trigger_rows:
        baseline_by_symbol[row["symbol"]].append(row)
    for row in candidate_trigger_rows:
        candidate_by_symbol[row["symbol"]].append(row)
    for row in input_rows:
        symbol = row.get("symbol", "")
        if symbol:
            input_count_by_symbol[symbol] += 1

    decision_rows: list[dict[str, Any]] = []
    candidate_micro_adjust_groups: list[str] = []

    for group_label in watchlist_groups:
        group_symbols = group_symbols_map.get(group_label, set())
        if not group_symbols:
            continue
        filter_meta = filter_map.get(group_label, {})
        best_filter = filter_meta.get("best_filter_scenario", "candidate_no_filter")
        filter_fn = scenario_filter_builder(best_filter)

        baseline_group_rows = []
        candidate_group_rows = []
        for symbol in group_symbols:
            baseline_group_rows.extend(baseline_by_symbol.get(symbol, []))
            candidate_group_rows.extend(candidate_by_symbol.get(symbol, []))

        filtered_candidate_rows = [row for row in candidate_group_rows if filter_fn(row)]
        rows_scanned = sum(input_count_by_symbol.get(symbol, 0) for symbol in group_symbols)
        baseline_density = len(baseline_group_rows) / rows_scanned if rows_scanned else 0.0
        candidate_density = len(filtered_candidate_rows) / rows_scanned if rows_scanned else 0.0
        candidate_no_filter_density = len(candidate_group_rows) / rows_scanned if rows_scanned else 0.0
        retention_vs_looser = (
            len(filtered_candidate_rows) / len(candidate_group_rows) if candidate_group_rows else 0.0
        )
        northbound_alignment_share = (
            sum(1 for row in filtered_candidate_rows if row.get("northbound_direction", "") == row.get("direction", ""))
            / len(filtered_candidate_rows)
            if filtered_candidate_rows
            else 0.0
        )

        verdict = "keep_watchlist"
        decision_reason = "candidate branch loses too much coverage relative to baseline"
        if (
            candidate_density >= baseline_density * 0.9
            and retention_vs_looser >= 0.45
            and northbound_alignment_share >= 0.25
        ):
            verdict = "micro_adjust_candidate"
            decision_reason = "candidate branch preserves most baseline coverage while improving confirmation quality"
            candidate_micro_adjust_groups.append(group_label)
        elif (
            candidate_density >= baseline_density * 0.75
            and retention_vs_looser >= 0.35
        ):
            verdict = "watchlist_strong"
            decision_reason = "candidate branch improves confirmation profile but still sits below baseline coverage"

        decision_rows.append(
            {
                "group_label": group_label,
                "symbol_count": len(group_symbols),
                "rows_scanned": rows_scanned,
                "baseline_density": round(baseline_density, 4),
                "candidate_no_filter_density": round(candidate_no_filter_density, 4),
                "best_filter_scenario": best_filter,
                "candidate_filtered_density": round(candidate_density, 4),
                "density_delta_vs_baseline": round(candidate_density - baseline_density, 4),
                "retention_vs_looser_candidate": round(retention_vs_looser, 4),
                "northbound_alignment_share": round(northbound_alignment_share, 4),
                "decision": verdict,
                "decision_reason": decision_reason,
            }
        )

    metadata["status"] = "success"
    metadata["watchlist_groups_reviewed"] = watchlist_groups
    metadata["micro_adjust_candidate_groups"] = candidate_micro_adjust_groups
    metadata["output_files"] = {
        "summary_json": str(summary_path).replace("\\", "/"),
        "decision_tsv": str(decision_path).replace("\\", "/"),
    }

    write_tsv(
        decision_path,
        decision_rows,
        [
            "group_label",
            "symbol_count",
            "rows_scanned",
            "baseline_density",
            "candidate_no_filter_density",
            "best_filter_scenario",
            "candidate_filtered_density",
            "density_delta_vs_baseline",
            "retention_vs_looser_candidate",
            "northbound_alignment_share",
            "decision",
            "decision_reason",
        ],
    )
    write_json(summary_path, metadata)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
