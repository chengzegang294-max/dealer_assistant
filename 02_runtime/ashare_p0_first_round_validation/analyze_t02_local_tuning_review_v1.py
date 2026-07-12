from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT_CSV = ROOT / "artifacts" / "t02_real_input_build" / "t02_real_input_candidate_latest.csv"
DEFAULT_LAYER_TSV = ROOT / "artifacts" / "t02_layer_stability" / "t02_symbol_layer_stability_latest.tsv"
DEFAULT_TUNING_RECOMMEND_TSV = (
    ROOT / "artifacts" / "t02_local_tuning" / "t02_local_tuning_recommendation_latest.tsv"
)
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "t02_local_tuning_review"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Review noise risk for watchlist local tuning groups."
    )
    parser.add_argument("--input-csv", default=str(DEFAULT_INPUT_CSV))
    parser.add_argument("--layer-tsv", default=str(DEFAULT_LAYER_TSV))
    parser.add_argument("--tuning-recommendation-tsv", default=str(DEFAULT_TUNING_RECOMMEND_TSV))
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


def build_trigger_rows(
    rows: list[dict[str, str]],
    main_ratio_threshold: float,
    min_consecutive_days: int,
) -> list[dict[str, Any]]:
    sorted_rows = sorted(rows, key=lambda row: (row["trade_date"], row["symbol"]))
    streak_by_symbol: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"direction": "neutral", "count": 0}
    )
    trigger_rows: list[dict[str, Any]] = []

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
            trigger_rows.append(
                {
                    "trade_date": row["trade_date"],
                    "symbol": symbol,
                    "symbol_name": row.get("symbol_name", ""),
                    "direction": direction,
                    "main_fund_net_inflow": flow_value,
                    "main_fund_net_inflow_ratio": ratio_value,
                    "consecutive_days": streak["count"],
                    "northbound_net_inflow": northbound_value,
                    "northbound_direction": sign_label(northbound_value),
                    "market_regime_label": row.get("market_regime_label", ""),
                    "industry_name": row.get("industry_name", ""),
                }
            )

    return trigger_rows


def main() -> int:
    args = parse_args()
    input_csv = Path(args.input_csv)
    layer_tsv = Path(args.layer_tsv)
    tuning_tsv = Path(args.tuning_recommendation_tsv)
    output_dir = Path(args.output_dir)

    summary_path = output_dir / "t02_local_tuning_review_summary_latest.json"
    review_path = output_dir / "t02_local_tuning_group_review_latest.tsv"
    added_detail_path = output_dir / "t02_local_tuning_added_trigger_detail_latest.tsv"

    metadata: dict[str, Any] = {
        "producer": "analyze_t02_local_tuning_review_v1.py",
        "scope": "A股 P0 首轮离线验证 T02 局部阈值微调噪声风险复核",
        "status": "started",
        "input_csv": str(input_csv).replace("\\", "/"),
        "layer_tsv": str(layer_tsv).replace("\\", "/"),
        "tuning_recommendation_tsv": str(tuning_tsv).replace("\\", "/"),
        "baseline_threshold": args.baseline_threshold,
        "candidate_threshold": args.candidate_threshold,
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

    symbol_meta = {row["symbol"]: row for row in layer_rows}
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

    baseline_triggers = build_trigger_rows(
        input_rows, args.baseline_threshold, args.min_consecutive_days
    )
    candidate_triggers = build_trigger_rows(
        input_rows, args.candidate_threshold, args.min_consecutive_days
    )
    baseline_keys = {
        (row["trade_date"], row["symbol"], row["direction"]) for row in baseline_triggers
    }

    added_detail_rows: list[dict[str, Any]] = []
    review_rows: list[dict[str, Any]] = []

    for group_label in watchlist_groups:
        group_symbols = groups.get(group_label, set())
        if not group_symbols:
            continue

        candidate_group_rows = [row for row in candidate_triggers if row["symbol"] in group_symbols]
        baseline_group_rows = [row for row in baseline_triggers if row["symbol"] in group_symbols]
        added_group_rows = [
            row
            for row in candidate_group_rows
            if (row["trade_date"], row["symbol"], row["direction"]) not in baseline_keys
        ]

        symbol_counter: Counter[str] = Counter()
        regime_counter: Counter[str] = Counter()
        marginal_band_count = 0
        northbound_available = 0
        northbound_aligned = 0

        for row in added_group_rows:
            symbol_counter[row["symbol"]] += 1
            regime_counter[row["market_regime_label"]] += 1
            if args.candidate_threshold <= abs(float(row["main_fund_net_inflow_ratio"])) < args.baseline_threshold:
                marginal_band_count += 1
            north_direction = row["northbound_direction"]
            if north_direction in {"inflow", "outflow"}:
                northbound_available += 1
                if north_direction == row["direction"]:
                    northbound_aligned += 1
            meta = symbol_meta.get(row["symbol"], {})
            added_detail_rows.append(
                {
                    "group_label": group_label,
                    "trade_date": row["trade_date"],
                    "symbol": row["symbol"],
                    "symbol_name": row["symbol_name"],
                    "sector_bucket": meta.get("sector_bucket", ""),
                    "macro_bucket": meta.get("macro_bucket", ""),
                    "flow_volatility_bucket": meta.get("flow_volatility_bucket", ""),
                    "direction": row["direction"],
                    "main_fund_net_inflow_ratio": round(float(row["main_fund_net_inflow_ratio"]), 6),
                    "consecutive_days": row["consecutive_days"],
                    "northbound_net_inflow": (
                        round(float(row["northbound_net_inflow"]), 6)
                        if row["northbound_net_inflow"] is not None
                        else ""
                    ),
                    "northbound_direction": north_direction,
                    "northbound_aligned": (
                        "yes" if north_direction in {"inflow", "outflow"} and north_direction == row["direction"] else "no"
                    ),
                    "market_regime_label": row["market_regime_label"],
                    "industry_name": row["industry_name"],
                }
            )

        added_count = len(added_group_rows)
        top_symbol = ""
        top_symbol_share = 0.0
        if symbol_counter:
            top_symbol, top_symbol_count = sorted(
                symbol_counter.items(), key=lambda item: (-item[1], item[0])
            )[0]
            top_symbol_share = top_symbol_count / added_count if added_count else 0.0

        dominant_regime = ""
        dominant_regime_share = 0.0
        if regime_counter:
            dominant_regime, dominant_regime_count = sorted(
                regime_counter.items(), key=lambda item: (-item[1], item[0])
            )[0]
            dominant_regime_share = dominant_regime_count / added_count if added_count else 0.0

        marginal_band_share = marginal_band_count / added_count if added_count else 0.0
        northbound_alignment_rate = (
            northbound_aligned / northbound_available if northbound_available else 0.0
        )

        risk_flags: list[str] = []
        if marginal_band_share >= 0.9:
            risk_flags.append("mostly_marginal_band")
        if top_symbol_share >= 0.45:
            risk_flags.append("single_symbol_concentration")
        if dominant_regime_share >= 0.8:
            risk_flags.append("single_regime_dominance")
        if northbound_available > 0 and northbound_alignment_rate < 0.35:
            risk_flags.append("weak_northbound_alignment")

        review_verdict = "watchlist_keep"
        if len(risk_flags) >= 3:
            review_verdict = "watchlist_high_noise_risk"
        elif len(risk_flags) == 0 and added_count >= 8:
            review_verdict = "watchlist_keep_priority"

        review_rows.append(
            {
                "group_label": group_label,
                "symbol_count": len(group_symbols),
                "baseline_trigger_rows": len(baseline_group_rows),
                "candidate_trigger_rows": len(candidate_group_rows),
                "added_trigger_rows": added_count,
                "marginal_band_share": round(marginal_band_share, 4),
                "top_symbol": top_symbol,
                "top_symbol_share": round(top_symbol_share, 4),
                "dominant_regime": dominant_regime,
                "dominant_regime_share": round(dominant_regime_share, 4),
                "northbound_alignment_rate": round(northbound_alignment_rate, 4),
                "risk_flags": "|".join(risk_flags),
                "review_verdict": review_verdict,
            }
        )

    metadata["status"] = "success"
    metadata["watchlist_groups_reviewed"] = watchlist_groups
    metadata["output_files"] = {
        "summary_json": str(summary_path).replace("\\", "/"),
        "group_review_tsv": str(review_path).replace("\\", "/"),
        "added_trigger_detail_tsv": str(added_detail_path).replace("\\", "/"),
    }

    write_tsv(
        review_path,
        review_rows,
        [
            "group_label",
            "symbol_count",
            "baseline_trigger_rows",
            "candidate_trigger_rows",
            "added_trigger_rows",
            "marginal_band_share",
            "top_symbol",
            "top_symbol_share",
            "dominant_regime",
            "dominant_regime_share",
            "northbound_alignment_rate",
            "risk_flags",
            "review_verdict",
        ],
    )
    write_tsv(
        added_detail_path,
        added_detail_rows,
        [
            "group_label",
            "trade_date",
            "symbol",
            "symbol_name",
            "sector_bucket",
            "macro_bucket",
            "flow_volatility_bucket",
            "direction",
            "main_fund_net_inflow_ratio",
            "consecutive_days",
            "northbound_net_inflow",
            "northbound_direction",
            "northbound_aligned",
            "market_regime_label",
            "industry_name",
        ],
    )
    write_json(summary_path, metadata)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
