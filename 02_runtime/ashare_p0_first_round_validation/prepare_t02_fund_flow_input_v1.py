from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT_CSV = ROOT / "data" / "t02_fund_flow_input_contract_v1.csv"
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "t02_input_prepare"

CANONICAL_COLUMNS = [
    "trade_date",
    "symbol",
    "symbol_name",
    "main_fund_net_inflow",
    "main_fund_net_inflow_ratio",
    "northbound_net_inflow",
    "northbound_holding_change",
    "market_regime_label",
    "open",
    "high",
    "low",
    "close",
    "prev_close",
    "volume",
    "amount",
    "industry_code",
    "industry_name",
    "data_source",
    "asof_date",
    "notes",
]

ALIASES = {
    "trade_date": ["trade_date", "date"],
    "symbol": ["symbol", "ticker", "code"],
    "symbol_name": ["symbol_name", "name"],
    "main_fund_net_inflow": ["main_fund_net_inflow", "main_net_inflow"],
    "main_fund_net_inflow_ratio": [
        "main_fund_net_inflow_ratio",
        "main_net_inflow_ratio",
        "main_flow_ratio",
    ],
    "northbound_net_inflow": ["northbound_net_inflow", "north_net_inflow"],
    "northbound_holding_change": [
        "northbound_holding_change",
        "north_holding_change",
    ],
    "market_regime_label": ["market_regime_label", "market_regime", "regime_label"],
    "open": ["open"],
    "high": ["high"],
    "low": ["low"],
    "close": ["close"],
    "prev_close": ["prev_close"],
    "volume": ["volume"],
    "amount": ["amount"],
    "industry_code": ["industry_code"],
    "industry_name": ["industry_name", "industry"],
    "data_source": ["data_source", "source"],
    "asof_date": ["asof_date"],
    "notes": ["notes", "note"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize candidate T02 fund-flow CSV into canonical contract columns."
    )
    parser.add_argument(
        "--input-csv",
        default=str(DEFAULT_INPUT_CSV),
        help="Candidate CSV to normalize.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for normalized output.",
    )
    return parser.parse_args()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def find_column(fieldnames: list[str], aliases: list[str]) -> str | None:
    lowered = {name.lower(): name for name in fieldnames}
    for alias in aliases:
        if alias.lower() in lowered:
            return lowered[alias.lower()]
    return None


def main() -> int:
    args = parse_args()
    input_csv = Path(args.input_csv)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    normalized_path = output_dir / "t02_fund_flow_input_normalized_latest.csv"
    summary_path = output_dir / "t02_input_prepare_summary_latest.json"

    summary: dict[str, Any] = {
        "producer": "prepare_t02_fund_flow_input_v1.py",
        "scope": "A股 P0 首轮离线验证 T02 输入归一化",
        "status": "started",
        "input_csv": str(input_csv).replace("\\", "/"),
        "output_dir": str(output_dir).replace("\\", "/"),
    }

    if not input_csv.exists():
        summary["status"] = "failed"
        summary["failure_reason"] = "input_csv_not_found"
        write_json(summary_path, summary)
        return 2

    with input_csv.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    selected_columns: dict[str, str] = {}
    normalized_rows: list[dict[str, Any]] = []
    for canonical_name in CANONICAL_COLUMNS:
        column_name = find_column(fieldnames, ALIASES.get(canonical_name, [canonical_name]))
        if column_name is not None:
            selected_columns[canonical_name] = column_name

    for row in rows:
        normalized_rows.append(
            {
                canonical_name: str(row.get(selected_columns.get(canonical_name, ""), "")).strip()
                for canonical_name in CANONICAL_COLUMNS
            }
        )

    write_csv(normalized_path, normalized_rows, CANONICAL_COLUMNS)

    summary["status"] = "success"
    summary["row_count"] = len(normalized_rows)
    summary["selected_columns"] = selected_columns
    summary["missing_columns"] = [
        canonical_name
        for canonical_name in CANONICAL_COLUMNS
        if canonical_name not in selected_columns
    ]
    summary["output_files"] = {
        "normalized_csv": str(normalized_path).replace("\\", "/"),
        "summary_json": str(summary_path).replace("\\", "/"),
    }
    write_json(summary_path, summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
