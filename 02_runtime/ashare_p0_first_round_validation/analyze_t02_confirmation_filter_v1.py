from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT_CSV = ROOT / "artifacts" / "t02_real_input_build" / "t02_real_input_candidate_latest.csv"
DEFAULT_LAYER_TSV = ROOT / "artifacts" / "t02_layer_stability" / "t02_symbol_layer_stability_latest.tsv"
DEFAULT_TUNING_RECOMMEND_TSV = (
    ROOT / "artifacts" / "t02_local_tuning" / "t02_local_tuning_recommendation_latest.tsv"
)
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "t02_confirmation_filter"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Test confirmation filters for watchlist local tuning candidates."
    )
    parser.add_argument("--input-csv", default=str(DEFAULT_INPUT_CSV))
    parser.add_argument("--layer-tsv", default=str(DEFAULT_LAYER_TSV))
    parser.add_argument("--tuning-recommendation-tsv", default=str(DEFAULT_TUNING_RECOMMEND_TSV))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--main-ratio-threshold", type=float, default=0.025)
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


def build_candidate_rows(
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
                    "symbol_name": row.get("symbol_name", ""),
                    "direction": direction,
                    "main_fund_net_inflow_ratio": ratio_value,
                    "northbound_net_inflow": northbound_value,
                    "northbound_direction": sign_label(northbound_value),
                    "market_regime_label": row.get("market_regime_label", ""),
                    "industry_name": row.get("industry_name", ""),
                }
            )
    return result


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


def main() -> int:
    args = parse_args()
    input_csv = Path(args.input_csv)
    layer_tsv = Path(args.layer_tsv)
    tuning_tsv = Path(args.tuning_recommendation_tsv)
    output_dir = Path(args.output_dir)

    summary_path = output_dir / "t02_confirmation_filter_summary_latest.json"
    scenario_path = output_dir / "t02_confirmation_filter_scenario_comparison_latest.tsv"
    recommendation_path = output_dir / "t02_confirmation_filter_recommendation_latest.tsv"

    metadata: dict[str, Any] = {
        "producer": "analyze_t02_confirmation_filter_v1.py",
        "scope": "A股 P0 首轮离线验证 T02 watchlist 确认条件过滤试算",
        "status": "started",
        "input_csv": str(input_csv).replace("\\", "/"),
        "layer_tsv": str(layer_tsv).replace("\\", "/"),
        "tuning_recommendation_tsv": str(tuning_tsv).replace("\\", "/"),
        "main_ratio_threshold": args.main_ratio_threshold,
        "min_consecutive_days": args.min_consecutive_days,
    }

    missing_inputs = [
        str(path).replace("\\", "/") for path in [input_csv, layer_tsv, tuning_tsv] if not path.exists()
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

    watchlist_groups = [
        row["group_label"] for row in tuning_rows if row.get("recommendation", "") == "watchlist"
    ]

    growth_symbols = {
        row["symbol"] for row in layer_rows if row.get("macro_bucket", "") == "成长科技"
    }
    low_vol_symbols = {
        row["symbol"] for row in layer_rows if row.get("flow_volatility_bucket", "") == "low"
    }
    groups = {
        "low_flow_vol": low_vol_symbols,
        "growth_tech_low_flow_vol": growth_symbols & low_vol_symbols,
    }

    candidate_rows = build_candidate_rows(
        input_rows,
        main_ratio_threshold=args.main_ratio_threshold,
        min_consecutive_days=args.min_consecutive_days,
    )

    scenario_names = [
        "candidate_no_filter",
        "candidate_exclude_g03",
        "candidate_require_northbound_align",
        "candidate_exclude_g03_and_northbound_align",
    ]
    scenario_rows: list[dict[str, Any]] = []
    recommendation_rows: list[dict[str, Any]] = []

    for group_label in watchlist_groups:
        group_symbols = groups.get(group_label, set())
        if not group_symbols:
            continue
        group_candidate_rows = [row for row in candidate_rows if row["symbol"] in group_symbols]
        if not group_candidate_rows:
            continue

        baseline_rows = list(group_candidate_rows)
        baseline_count = len(baseline_rows)
        baseline_g03_share = sum(
            1 for row in baseline_rows if row.get("market_regime_label", "") == "G03_震荡"
        ) / baseline_count
        baseline_align_count = sum(
            1
            for row in baseline_rows
            if row.get("northbound_direction", "") == row.get("direction", "")
        )
        baseline_align_share = baseline_align_count / baseline_count

        group_scenario_rows: list[dict[str, Any]] = []
        for scenario_name in scenario_names:
            filter_fn = scenario_filter_builder(scenario_name)
            kept_rows = [row for row in baseline_rows if filter_fn(row)]
            kept_count = len(kept_rows)
            kept_symbols = len({row["symbol"] for row in kept_rows})
            kept_g03_share = (
                sum(1 for row in kept_rows if row.get("market_regime_label", "") == "G03_震荡") / kept_count
                if kept_count
                else 0.0
            )
            kept_align_share = (
                sum(1 for row in kept_rows if row.get("northbound_direction", "") == row.get("direction", "")) / kept_count
                if kept_count
                else 0.0
            )
            row = {
                "group_label": group_label,
                "scenario_label": scenario_name,
                "symbol_count": len(group_symbols),
                "baseline_candidate_rows": baseline_count,
                "kept_rows": kept_count,
                "kept_row_share": round((kept_count / baseline_count) if baseline_count else 0.0, 4),
                "kept_symbols": kept_symbols,
                "g03_share": round(kept_g03_share, 4),
                "northbound_alignment_share": round(kept_align_share, 4),
                "g03_share_improvement": round(baseline_g03_share - kept_g03_share, 4),
                "northbound_alignment_improvement": round(kept_align_share - baseline_align_share, 4),
            }
            group_scenario_rows.append(row)
            scenario_rows.append(row)

        candidate_rows_only = [
            row for row in group_scenario_rows if row["scenario_label"] != "candidate_no_filter"
        ]
        # Prefer filters that preserve at least one third of candidate rows while meaningfully reducing G03 concentration.
        viable_rows = [
            row
            for row in candidate_rows_only
            if float(row["kept_row_share"]) >= 0.33 and float(row["g03_share_improvement"]) >= 0.2
        ]
        best_row = None
        if viable_rows:
            best_row = sorted(
                viable_rows,
                key=lambda row: (
                    -float(row["g03_share_improvement"]),
                    -float(row["northbound_alignment_improvement"]),
                    -float(row["kept_row_share"]),
                    row["scenario_label"],
                ),
            )[0]
        else:
            best_row = sorted(
                candidate_rows_only,
                key=lambda row: (
                    -float(row["northbound_alignment_improvement"]),
                    -float(row["g03_share_improvement"]),
                    -float(row["kept_row_share"]),
                    row["scenario_label"],
                ),
            )[0]

        recommendation = "keep_watchlist_only"
        reason = "filters either remove too much signal or do not improve noise profile enough"
        if (
            float(best_row["kept_row_share"]) >= 0.45
            and float(best_row["g03_share_improvement"]) >= 0.35
            and float(best_row["northbound_alignment_share"]) >= 0.3
        ):
            recommendation = "candidate_filtered_branch"
            reason = "filter keeps enough rows while materially improving regime concentration and alignment"
        elif (
            float(best_row["kept_row_share"]) >= 0.33
            and float(best_row["g03_share_improvement"]) >= 0.2
        ):
            recommendation = "watch_filtered_branch"
            reason = "filter improves noise profile enough for follow-up monitoring, but not for default activation"

        recommendation_rows.append(
            {
                "group_label": group_label,
                "baseline_candidate_rows": baseline_count,
                "best_filter_scenario": best_row["scenario_label"],
                "kept_rows": best_row["kept_rows"],
                "kept_row_share": best_row["kept_row_share"],
                "g03_share_after_filter": best_row["g03_share"],
                "g03_share_improvement": best_row["g03_share_improvement"],
                "northbound_alignment_share_after_filter": best_row["northbound_alignment_share"],
                "northbound_alignment_improvement": best_row["northbound_alignment_improvement"],
                "recommendation": recommendation,
                "reason": reason,
            }
        )

    metadata["status"] = "success"
    metadata["watchlist_groups_reviewed"] = watchlist_groups
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
            "scenario_label",
            "symbol_count",
            "baseline_candidate_rows",
            "kept_rows",
            "kept_row_share",
            "kept_symbols",
            "g03_share",
            "northbound_alignment_share",
            "g03_share_improvement",
            "northbound_alignment_improvement",
        ],
    )
    write_tsv(
        recommendation_path,
        recommendation_rows,
        [
            "group_label",
            "baseline_candidate_rows",
            "best_filter_scenario",
            "kept_rows",
            "kept_row_share",
            "g03_share_after_filter",
            "g03_share_improvement",
            "northbound_alignment_share_after_filter",
            "northbound_alignment_improvement",
            "recommendation",
            "reason",
        ],
    )
    write_json(summary_path, metadata)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
