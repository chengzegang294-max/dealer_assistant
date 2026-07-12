from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT_CSV = ROOT / "data" / "t02_fund_flow_input_contract_v1.csv"
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "t02_input_audit"

REQUIRED_COLUMNS = [
    "trade_date",
    "symbol",
    "main_fund_net_inflow",
    "main_fund_net_inflow_ratio",
]

OPTIONAL_COLUMNS = [
    "symbol_name",
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit a CSV against the T02 fund-flow input contract."
    )
    parser.add_argument(
        "--input-csv",
        default=str(DEFAULT_INPUT_CSV),
        help="Candidate CSV to audit.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for audit artifacts.",
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


def main() -> int:
    args = parse_args()
    input_csv = Path(args.input_csv)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_path = output_dir / "t02_input_audit_summary_latest.json"
    missing_path = output_dir / "t02_missing_columns_latest.tsv"

    summary: dict[str, Any] = {
        "producer": "audit_t02_fund_flow_input_v1.py",
        "scope": "A股 P0 首轮离线验证 T02 输入审计",
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

    fieldname_set = set(fieldnames)
    missing_required = [col for col in REQUIRED_COLUMNS if col not in fieldname_set]
    missing_optional = [col for col in OPTIONAL_COLUMNS if col not in fieldname_set]

    missing_rows = (
        [{"column_name": col, "column_type": "required"} for col in missing_required]
        + [{"column_name": col, "column_type": "optional"} for col in missing_optional]
    )
    write_tsv(missing_path, missing_rows, ["column_name", "column_type"])

    summary["status"] = "success"
    summary["row_count"] = len(rows)
    summary["available_columns"] = fieldnames
    summary["missing_required_columns"] = missing_required
    summary["missing_optional_columns"] = missing_optional
    summary["contract_ready"] = len(missing_required) == 0
    summary["output_files"] = {
        "summary_json": str(summary_path).replace("\\", "/"),
        "missing_columns_tsv": str(missing_path).replace("\\", "/"),
    }
    write_json(summary_path, summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
