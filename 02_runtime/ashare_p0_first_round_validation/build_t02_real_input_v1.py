from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_BASE_CSV = ROOT / "artifacts" / "t02_input_prepare" / "t02_fund_flow_input_normalized_latest.csv"
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "t02_real_input_build"

FINAL_COLUMNS = [
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

JOINABLE_DATASETS = {
    "moneyflow": [
        "main_fund_net_inflow",
        "main_fund_net_inflow_ratio",
        "data_source",
        "asof_date",
        "notes",
    ],
    "northbound": [
        "northbound_net_inflow",
        "northbound_holding_change",
        "data_source",
        "asof_date",
        "notes",
    ],
    "regime": [
        "market_regime_label",
        "data_source",
        "asof_date",
        "notes",
    ],
    "industry": [
        "industry_code",
        "industry_name",
        "data_source",
        "asof_date",
        "notes",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a candidate real T02 wide table from base rows plus optional join tables."
    )
    parser.add_argument(
        "--base-csv",
        default=str(DEFAULT_BASE_CSV),
        help="Base OHLCV-like table with trade_date and symbol.",
    )
    parser.add_argument("--moneyflow-csv", help="Optional moneyflow join table.", default="")
    parser.add_argument("--northbound-csv", help="Optional northbound join table.", default="")
    parser.add_argument("--regime-csv", help="Optional regime join table.", default="")
    parser.add_argument("--industry-csv", help="Optional industry join table.", default="")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for build artifacts.",
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


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def build_key(row: dict[str, str], fields: list[str]) -> str:
    return "|".join(str(row.get(field, "")).strip() for field in fields)


def load_join_map(path: Path, key_fields: list[str]) -> dict[str, dict[str, str]]:
    _, rows = read_csv(path)
    return {build_key(row, key_fields): row for row in rows}


def append_note(existing_note: str, fragment: str) -> str:
    parts = [part.strip() for part in [existing_note, fragment] if part and part.strip()]
    return " | ".join(parts)


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    base_csv = Path(args.base_csv)
    summary_path = output_dir / "t02_real_input_build_summary_latest.json"
    output_csv = output_dir / "t02_real_input_candidate_latest.csv"

    summary: dict[str, Any] = {
        "producer": "build_t02_real_input_v1.py",
        "scope": "A股 P0 首轮离线验证 T02 真实宽表拼接",
        "status": "started",
        "base_csv": str(base_csv).replace("\\", "/"),
        "output_dir": str(output_dir).replace("\\", "/"),
    }

    if not base_csv.exists():
        summary["status"] = "failed"
        summary["failure_reason"] = "base_csv_not_found"
        write_json(summary_path, summary)
        return 2

    _, base_rows = read_csv(base_csv)
    join_sources = {
        "moneyflow": Path(args.moneyflow_csv) if args.moneyflow_csv else None,
        "northbound": Path(args.northbound_csv) if args.northbound_csv else None,
        "regime": Path(args.regime_csv) if args.regime_csv else None,
        "industry": Path(args.industry_csv) if args.industry_csv else None,
    }
    join_maps: dict[str, dict[str, dict[str, str]]] = {}
    join_hit_counts = {name: 0 for name in join_sources}

    for name, path in join_sources.items():
        if path and path.exists():
            key_fields = ["symbol"] if name == "industry" else ["trade_date", "symbol"]
            join_maps[name] = load_join_map(path, key_fields)
        else:
            join_maps[name] = {}

    built_rows: list[dict[str, str]] = []
    for row in base_rows:
        built_row = {column: str(row.get(column, "")).strip() for column in FINAL_COLUMNS}
        base_note = built_row.get("notes", "")
        for join_name, columns in JOINABLE_DATASETS.items():
            key_fields = ["symbol"] if join_name == "industry" else ["trade_date", "symbol"]
            key = build_key(row, key_fields)
            join_row = join_maps[join_name].get(key)
            if join_row:
                join_hit_counts[join_name] += 1
                for column in columns:
                    join_value = str(join_row.get(column, "")).strip()
                    if join_value:
                        if column == "notes":
                            built_row[column] = append_note(built_row.get(column, ""), join_value)
                        elif column == "data_source":
                            built_row[column] = join_value if not built_row.get(column) else built_row[column]
                        elif column == "asof_date":
                            built_row[column] = join_value if not built_row.get(column) else built_row[column]
                        else:
                            built_row[column] = join_value
        if not built_row.get("data_source"):
            built_row["data_source"] = "base_only"
        if not built_row.get("notes"):
            built_row["notes"] = "candidate_built_from_available_sources"
        built_rows.append(built_row)

    write_csv(output_csv, built_rows, FINAL_COLUMNS)

    summary["status"] = "success"
    summary["row_count"] = len(built_rows)
    summary["join_sources"] = {
        name: (str(path).replace("\\", "/") if path else "")
        for name, path in join_sources.items()
    }
    summary["join_hit_counts"] = join_hit_counts
    summary["missing_join_sources"] = [
        name for name, path in join_sources.items() if not path or not path.exists()
    ]
    summary["output_files"] = {
        "candidate_csv": str(output_csv).replace("\\", "/"),
        "summary_json": str(summary_path).replace("\\", "/"),
    }
    write_json(summary_path, summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
