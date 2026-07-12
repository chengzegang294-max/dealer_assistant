from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "t02_fund_flow_scan"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan fund-flow style CSV for A-share P0 T02 validation."
    )
    parser.add_argument("--input-csv", required=True, help="CSV containing fund flow fields.")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for summary JSON/TSV artifacts.",
    )
    parser.add_argument(
        "--main-flow-ratio-threshold",
        type=float,
        default=0.03,
        help="Absolute main fund inflow ratio threshold.",
    )
    parser.add_argument(
        "--min-consecutive-days",
        type=int,
        default=2,
        help="Minimum same-direction consecutive days above threshold.",
    )
    return parser.parse_args()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_tsv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def find_column(fieldnames: list[str], candidates: list[str]) -> str | None:
    fieldname_map = {name.lower(): name for name in fieldnames}
    for candidate in candidates:
        if candidate.lower() in fieldname_map:
            return fieldname_map[candidate.lower()]
    return None


def safe_float(raw: str | None) -> float | None:
    if raw is None or raw == "":
        return None
    return float(raw)


def normalize_ratio(value: float) -> float:
    return value / 100.0 if abs(value) > 1 else value


def main() -> int:
    args = parse_args()
    input_csv = Path(args.input_csv)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    metadata_path = output_dir / "t02_fund_flow_scan_summary_latest.json"
    detail_path = output_dir / "t02_trigger_detail_latest.tsv"
    symbol_path = output_dir / "t02_symbol_trigger_counts_latest.tsv"
    regime_path = output_dir / "t02_regime_trigger_counts_latest.tsv"
    symbol_regime_path = output_dir / "t02_symbol_regime_trigger_counts_latest.tsv"

    metadata: dict[str, Any] = {
        "producer": "run_t02_fund_flow_scan_v1.py",
        "scope": "A股 P0 首轮离线验证 T02",
        "status": "started",
        "input_csv": str(input_csv).replace("\\", "/"),
        "output_dir": str(output_dir).replace("\\", "/"),
        "main_flow_ratio_threshold": args.main_flow_ratio_threshold,
        "min_consecutive_days": args.min_consecutive_days,
    }

    if not input_csv.exists():
        metadata["status"] = "failed"
        metadata["failure_reason"] = "input_csv_not_found"
        write_json(metadata_path, metadata)
        return 2

    with input_csv.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        date_col = find_column(fieldnames, ["trade_date", "date"])
        symbol_col = find_column(fieldnames, ["symbol", "ticker", "code"])
        main_flow_col = find_column(
            fieldnames, ["main_fund_net_inflow", "main_net_inflow"]
        )
        main_ratio_col = find_column(
            fieldnames,
            ["main_fund_net_inflow_ratio", "main_net_inflow_ratio", "main_flow_ratio"],
        )
        northbound_col = find_column(
            fieldnames, ["northbound_net_inflow", "north_net_inflow"]
        )
        regime_col = find_column(
            fieldnames, ["market_regime_label", "market_regime", "regime_label"]
        )

        missing_required = [
            label
            for label, column_name in {
                "trade_date": date_col,
                "symbol": symbol_col,
                "main_fund_net_inflow": main_flow_col,
                "main_fund_net_inflow_ratio": main_ratio_col,
            }.items()
            if column_name is None
        ]
        if missing_required:
            metadata["status"] = "failed"
            metadata["failure_reason"] = "missing_required_columns"
            metadata["missing_required_columns"] = missing_required
            metadata["available_columns"] = fieldnames
            write_json(metadata_path, metadata)
            return 3

        rows = list(reader)

    rows.sort(key=lambda row: (str(row[date_col]), str(row[symbol_col])))  # type: ignore[index]

    trigger_rows: list[dict[str, Any]] = []
    streak_by_symbol: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"direction": "neutral", "count": 0}
    )
    regime_counter: Counter[str] = Counter()
    symbol_counter: Counter[str] = Counter()
    symbol_regime_counter: Counter[tuple[str, str]] = Counter()

    for row in rows:
        trade_date = str(row[date_col])  # type: ignore[index]
        symbol = str(row[symbol_col])  # type: ignore[index]
        flow_value = safe_float(row.get(main_flow_col))  # type: ignore[arg-type]
        ratio_value_raw = safe_float(row.get(main_ratio_col))  # type: ignore[arg-type]
        if flow_value is None or ratio_value_raw is None:
            continue

        ratio_value = normalize_ratio(ratio_value_raw)
        if abs(ratio_value) < args.main_flow_ratio_threshold or flow_value == 0:
            streak_by_symbol[symbol] = {"direction": "neutral", "count": 0}
            continue

        direction = "inflow" if flow_value > 0 else "outflow"
        streak = streak_by_symbol[symbol]
        if streak["direction"] == direction:
            streak["count"] += 1
        else:
            streak["direction"] = direction
            streak["count"] = 1

        if streak["count"] >= args.min_consecutive_days:
            regime_value = (
                str(row.get(regime_col, "")) if regime_col is not None else "unavailable"
            )
            northbound_value = (
                safe_float(row.get(northbound_col)) if northbound_col is not None else None
            )
            trigger_rows.append(
                {
                    "trade_date": trade_date,
                    "symbol": symbol,
                    "direction": direction,
                    "main_fund_net_inflow": round(flow_value, 6),
                    "main_fund_net_inflow_ratio": round(ratio_value, 6),
                    "consecutive_days": streak["count"],
                    "northbound_net_inflow": (
                        round(northbound_value, 6) if northbound_value is not None else ""
                    ),
                    "market_regime_label": regime_value,
                }
            )
            symbol_counter[symbol] += 1
            regime_counter[regime_value] += 1
            symbol_regime_counter[(symbol, regime_value)] += 1

    symbol_rows = [
        {"symbol": symbol, "trigger_count": count}
        for symbol, count in sorted(
            symbol_counter.items(), key=lambda item: (-item[1], item[0])
        )
    ]
    regime_rows = [
        {"market_regime_label": label, "trigger_count": count}
        for label, count in sorted(regime_counter.items())
    ]
    symbol_regime_rows = [
        {
            "symbol": symbol,
            "market_regime_label": regime_label,
            "trigger_count": count,
        }
        for (symbol, regime_label), count in sorted(
            symbol_regime_counter.items(), key=lambda item: (-item[1], item[0][0], item[0][1])
        )
    ]

    write_tsv(
        detail_path,
        trigger_rows,
        [
            "trade_date",
            "symbol",
            "direction",
            "main_fund_net_inflow",
            "main_fund_net_inflow_ratio",
            "consecutive_days",
            "northbound_net_inflow",
            "market_regime_label",
        ],
    )
    write_tsv(symbol_path, symbol_rows, ["symbol", "trigger_count"])
    write_tsv(regime_path, regime_rows, ["market_regime_label", "trigger_count"])
    write_tsv(
        symbol_regime_path,
        symbol_regime_rows,
        ["symbol", "market_regime_label", "trigger_count"],
    )

    metadata["status"] = "success"
    metadata["rows_scanned"] = len(rows)
    metadata["trigger_rows"] = len(trigger_rows)
    metadata["trigger_symbols"] = len(symbol_rows)
    metadata["optional_columns"] = {
        "northbound_net_inflow": northbound_col or "",
        "market_regime_label": regime_col or "",
    }
    metadata["output_files"] = {
        "summary_json": str(metadata_path).replace("\\", "/"),
        "trigger_detail_tsv": str(detail_path).replace("\\", "/"),
        "symbol_counts_tsv": str(symbol_path).replace("\\", "/"),
        "regime_counts_tsv": str(regime_path).replace("\\", "/"),
        "symbol_regime_counts_tsv": str(symbol_regime_path).replace("\\", "/"),
    }
    write_json(metadata_path, metadata)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
