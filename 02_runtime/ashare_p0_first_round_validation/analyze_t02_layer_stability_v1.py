from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import pstdev
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT_CSV = ROOT / "artifacts" / "t02_real_input_build" / "t02_real_input_candidate_latest.csv"
DEFAULT_SAMPLE_LIST_CSV = ROOT / "data" / "t02_multi_symbol_sample_v3.csv"
DEFAULT_TRIGGER_SYMBOL_TSV = ROOT / "artifacts" / "t02_fund_flow_scan" / "t02_symbol_trigger_counts_latest.tsv"
DEFAULT_TRIGGER_SYMBOL_REGIME_TSV = (
    ROOT / "artifacts" / "t02_fund_flow_scan" / "t02_symbol_regime_trigger_counts_latest.tsv"
)
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "t02_layer_stability"


MACRO_BUCKET_MAP = {
    "银行": "金融",
    "券商": "金融",
    "保险": "金融",
    "地产": "地产链",
    "消费": "消费防御",
    "家电": "消费防御",
    "医药": "消费防御",
    "公用事业": "消费防御",
    "新能源": "成长科技",
    "半导体": "成长科技",
    "通信": "成长科技",
    "军工": "成长科技",
    "汽车": "成长科技",
    "面板电子": "成长科技",
    "光伏": "成长科技",
    "计算机": "成长科技",
    "有色": "资源周期",
    "化工": "资源周期",
    "煤炭": "资源周期",
    "钢铁": "资源周期",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze T02 layer stability by macro bucket and fund-flow volatility."
    )
    parser.add_argument("--input-csv", default=str(DEFAULT_INPUT_CSV))
    parser.add_argument("--sample-list-csv", default=str(DEFAULT_SAMPLE_LIST_CSV))
    parser.add_argument("--trigger-symbol-tsv", default=str(DEFAULT_TRIGGER_SYMBOL_TSV))
    parser.add_argument("--trigger-symbol-regime-tsv", default=str(DEFAULT_TRIGGER_SYMBOL_REGIME_TSV))
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


def percentile_cut(values: list[float], ratio: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, math.ceil(len(ordered) * ratio) - 1))
    return ordered[index]


def classify_flow_vol_bucket(std_value: float, low_cut: float, high_cut: float) -> str:
    if std_value <= low_cut:
        return "low"
    if std_value >= high_cut:
        return "high"
    return "mid"


def dominant_regime(counter: Counter[str]) -> str:
    if not counter:
        return "unavailable"
    return sorted(counter.items(), key=lambda item: (-item[1], item[0]))[0][0]


def macro_bucket_for(sector_bucket: str) -> str:
    return MACRO_BUCKET_MAP.get(sector_bucket, "其他")


def main() -> int:
    args = parse_args()
    input_csv = Path(args.input_csv)
    sample_list_csv = Path(args.sample_list_csv)
    trigger_symbol_tsv = Path(args.trigger_symbol_tsv)
    trigger_symbol_regime_tsv = Path(args.trigger_symbol_regime_tsv)
    output_dir = Path(args.output_dir)

    summary_path = output_dir / "t02_layer_stability_summary_latest.json"
    symbol_path = output_dir / "t02_symbol_layer_stability_latest.tsv"
    macro_path = output_dir / "t02_macro_bucket_stability_latest.tsv"
    flow_vol_path = output_dir / "t02_flow_volatility_bucket_stability_latest.tsv"

    metadata: dict[str, Any] = {
        "producer": "analyze_t02_layer_stability_v1.py",
        "scope": "A股 P0 首轮离线验证 T02 分层稳定性",
        "status": "started",
        "input_csv": str(input_csv).replace("\\", "/"),
        "sample_list_csv": str(sample_list_csv).replace("\\", "/"),
        "trigger_symbol_tsv": str(trigger_symbol_tsv).replace("\\", "/"),
        "trigger_symbol_regime_tsv": str(trigger_symbol_regime_tsv).replace("\\", "/"),
        "output_dir": str(output_dir).replace("\\", "/"),
        "flow_volatility_definition": "stddev(main_fund_net_inflow_ratio) over latest window",
    }

    missing_inputs = [
        str(path).replace("\\", "/")
        for path in [input_csv, sample_list_csv, trigger_symbol_tsv, trigger_symbol_regime_tsv]
        if not path.exists()
    ]
    if missing_inputs:
        metadata["status"] = "failed"
        metadata["failure_reason"] = "missing_input_files"
        metadata["missing_inputs"] = missing_inputs
        write_json(summary_path, metadata)
        return 2

    input_rows = read_csv_rows(input_csv)
    sample_rows = read_csv_rows(sample_list_csv)
    trigger_rows = read_csv_rows(trigger_symbol_tsv, delimiter="\t")
    trigger_regime_rows = read_csv_rows(trigger_symbol_regime_tsv, delimiter="\t")

    sample_meta = {
        row["symbol"]: {
            "symbol_name": row.get("symbol_name", ""),
            "sector_bucket": row.get("sector_bucket", ""),
            "macro_bucket": macro_bucket_for(row.get("sector_bucket", "")),
        }
        for row in sample_rows
    }
    trigger_count_map = {
        row["symbol"]: int(row.get("trigger_count", "0") or 0) for row in trigger_rows
    }
    trigger_regime_counter: dict[str, Counter[str]] = defaultdict(Counter)
    for row in trigger_regime_rows:
        symbol = row.get("symbol", "")
        regime = row.get("market_regime_label", "")
        count = int(row.get("trigger_count", "0") or 0)
        if symbol:
            trigger_regime_counter[symbol][regime] += count

    symbol_stats: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "rows_scanned": 0,
            "ratio_values": [],
            "abs_ratio_values": [],
            "industry_name": "",
        }
    )
    for row in input_rows:
        symbol = row.get("symbol", "")
        if not symbol:
            continue
        ratio_value = safe_float(row.get("main_fund_net_inflow_ratio"))
        if ratio_value is None:
            continue
        symbol_stats[symbol]["rows_scanned"] += 1
        symbol_stats[symbol]["ratio_values"].append(ratio_value)
        symbol_stats[symbol]["abs_ratio_values"].append(abs(ratio_value))
        if not symbol_stats[symbol]["industry_name"]:
            symbol_stats[symbol]["industry_name"] = row.get("industry_name", "")

    std_values: list[float] = []
    for symbol, stats in symbol_stats.items():
        ratio_values = stats["ratio_values"]
        stats["avg_abs_ratio"] = sum(stats["abs_ratio_values"]) / len(stats["abs_ratio_values"])
        stats["ratio_stddev"] = pstdev(ratio_values) if len(ratio_values) > 1 else 0.0
        stats["trigger_count"] = trigger_count_map.get(symbol, 0)
        stats["trigger_density"] = (
            stats["trigger_count"] / stats["rows_scanned"] if stats["rows_scanned"] else 0.0
        )
        stats["regime_coverage_count"] = len(trigger_regime_counter.get(symbol, Counter()))
        stats["dominant_regime"] = dominant_regime(trigger_regime_counter.get(symbol, Counter()))
        stats["sector_bucket"] = sample_meta.get(symbol, {}).get("sector_bucket", "")
        stats["macro_bucket"] = sample_meta.get(symbol, {}).get("macro_bucket", "其他")
        stats["symbol_name"] = sample_meta.get(symbol, {}).get("symbol_name", "")
        std_values.append(stats["ratio_stddev"])

    low_cut = percentile_cut(std_values, 1 / 3)
    high_cut = percentile_cut(std_values, 2 / 3)

    symbol_rows: list[dict[str, Any]] = []
    for symbol, stats in sorted(
        symbol_stats.items(), key=lambda item: (-item[1]["trigger_density"], item[0])
    ):
        flow_vol_bucket = classify_flow_vol_bucket(stats["ratio_stddev"], low_cut, high_cut)
        symbol_rows.append(
            {
                "symbol": symbol,
                "symbol_name": stats["symbol_name"],
                "sector_bucket": stats["sector_bucket"],
                "macro_bucket": stats["macro_bucket"],
                "industry_name": stats["industry_name"],
                "rows_scanned": stats["rows_scanned"],
                "trigger_count": stats["trigger_count"],
                "trigger_density": round(stats["trigger_density"], 4),
                "avg_abs_main_flow_ratio": round(stats["avg_abs_ratio"], 4),
                "flow_ratio_stddev": round(stats["ratio_stddev"], 4),
                "flow_volatility_bucket": flow_vol_bucket,
                "regime_coverage_count": stats["regime_coverage_count"],
                "dominant_regime": stats["dominant_regime"],
            }
        )

    macro_stats: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "symbol_count": 0,
            "rows_scanned": 0,
            "trigger_rows": 0,
            "density_sum": 0.0,
            "avg_abs_ratio_sum": 0.0,
            "ratio_stddev_sum": 0.0,
            "best_symbol": "",
            "best_density": -1.0,
        }
    )
    flow_vol_stats: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "symbol_count": 0,
            "rows_scanned": 0,
            "trigger_rows": 0,
            "density_sum": 0.0,
            "best_symbol": "",
            "best_density": -1.0,
        }
    )

    for row in symbol_rows:
        macro_bucket = row["macro_bucket"]
        macro_stats[macro_bucket]["symbol_count"] += 1
        macro_stats[macro_bucket]["rows_scanned"] += int(row["rows_scanned"])
        macro_stats[macro_bucket]["trigger_rows"] += int(row["trigger_count"])
        macro_stats[macro_bucket]["density_sum"] += float(row["trigger_density"])
        macro_stats[macro_bucket]["avg_abs_ratio_sum"] += float(row["avg_abs_main_flow_ratio"])
        macro_stats[macro_bucket]["ratio_stddev_sum"] += float(row["flow_ratio_stddev"])
        if float(row["trigger_density"]) > macro_stats[macro_bucket]["best_density"]:
            macro_stats[macro_bucket]["best_density"] = float(row["trigger_density"])
            macro_stats[macro_bucket]["best_symbol"] = row["symbol"]

        vol_bucket = row["flow_volatility_bucket"]
        flow_vol_stats[vol_bucket]["symbol_count"] += 1
        flow_vol_stats[vol_bucket]["rows_scanned"] += int(row["rows_scanned"])
        flow_vol_stats[vol_bucket]["trigger_rows"] += int(row["trigger_count"])
        flow_vol_stats[vol_bucket]["density_sum"] += float(row["trigger_density"])
        if float(row["trigger_density"]) > flow_vol_stats[vol_bucket]["best_density"]:
            flow_vol_stats[vol_bucket]["best_density"] = float(row["trigger_density"])
            flow_vol_stats[vol_bucket]["best_symbol"] = row["symbol"]

    macro_rows: list[dict[str, Any]] = []
    for macro_bucket, stats in macro_stats.items():
        symbol_count = stats["symbol_count"]
        trigger_density = stats["trigger_rows"] / stats["rows_scanned"] if stats["rows_scanned"] else 0.0
        avg_symbol_density = stats["density_sum"] / symbol_count if symbol_count else 0.0
        macro_rows.append(
            {
                "macro_bucket": macro_bucket,
                "symbol_count": symbol_count,
                "rows_scanned": stats["rows_scanned"],
                "trigger_rows": stats["trigger_rows"],
                "trigger_density": round(trigger_density, 4),
                "avg_symbol_density": round(avg_symbol_density, 4),
                "avg_abs_main_flow_ratio": round(stats["avg_abs_ratio_sum"] / symbol_count, 4),
                "avg_flow_ratio_stddev": round(stats["ratio_stddev_sum"] / symbol_count, 4),
                "top_symbol": stats["best_symbol"],
            }
        )
    macro_rows.sort(key=lambda row: (-row["trigger_density"], row["macro_bucket"]))

    flow_vol_rows: list[dict[str, Any]] = []
    bucket_order = {"high": 0, "mid": 1, "low": 2}
    for vol_bucket, stats in sorted(flow_vol_stats.items(), key=lambda item: bucket_order.get(item[0], 99)):
        symbol_count = stats["symbol_count"]
        trigger_density = stats["trigger_rows"] / stats["rows_scanned"] if stats["rows_scanned"] else 0.0
        avg_symbol_density = stats["density_sum"] / symbol_count if symbol_count else 0.0
        flow_vol_rows.append(
            {
                "flow_volatility_bucket": vol_bucket,
                "symbol_count": symbol_count,
                "rows_scanned": stats["rows_scanned"],
                "trigger_rows": stats["trigger_rows"],
                "trigger_density": round(trigger_density, 4),
                "avg_symbol_density": round(avg_symbol_density, 4),
                "top_symbol": stats["best_symbol"],
            }
        )

    strongest_macro = macro_rows[0]["macro_bucket"] if macro_rows else ""
    strongest_vol = sorted(flow_vol_rows, key=lambda row: (-row["trigger_density"], row["flow_volatility_bucket"]))[0]["flow_volatility_bucket"] if flow_vol_rows else ""

    metadata["status"] = "success"
    metadata["rows_scanned"] = len(input_rows)
    metadata["symbols_covered"] = len(symbol_rows)
    metadata["trigger_rows"] = sum(int(row["trigger_count"]) for row in symbol_rows)
    metadata["low_stddev_cut"] = round(low_cut, 6)
    metadata["high_stddev_cut"] = round(high_cut, 6)
    metadata["strongest_macro_bucket"] = strongest_macro
    metadata["strongest_flow_volatility_bucket"] = strongest_vol
    metadata["output_files"] = {
        "summary_json": str(summary_path).replace("\\", "/"),
        "symbol_layer_tsv": str(symbol_path).replace("\\", "/"),
        "macro_bucket_tsv": str(macro_path).replace("\\", "/"),
        "flow_volatility_bucket_tsv": str(flow_vol_path).replace("\\", "/"),
    }

    write_tsv(
        symbol_path,
        symbol_rows,
        [
            "symbol",
            "symbol_name",
            "sector_bucket",
            "macro_bucket",
            "industry_name",
            "rows_scanned",
            "trigger_count",
            "trigger_density",
            "avg_abs_main_flow_ratio",
            "flow_ratio_stddev",
            "flow_volatility_bucket",
            "regime_coverage_count",
            "dominant_regime",
        ],
    )
    write_tsv(
        macro_path,
        macro_rows,
        [
            "macro_bucket",
            "symbol_count",
            "rows_scanned",
            "trigger_rows",
            "trigger_density",
            "avg_symbol_density",
            "avg_abs_main_flow_ratio",
            "avg_flow_ratio_stddev",
            "top_symbol",
        ],
    )
    write_tsv(
        flow_vol_path,
        flow_vol_rows,
        [
            "flow_volatility_bucket",
            "symbol_count",
            "rows_scanned",
            "trigger_rows",
            "trigger_density",
            "avg_symbol_density",
            "top_symbol",
        ],
    )
    write_json(summary_path, metadata)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
