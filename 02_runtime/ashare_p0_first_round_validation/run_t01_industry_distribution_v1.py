from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_TRIGGER_COUNTS = (
    ROOT / "artifacts" / "t01_volume_price_scan" / "t01_symbol_trigger_counts_latest.tsv"
)
DEFAULT_MAPPING_CSV = (
    ROOT.parent
    / "butler_r0_ohlcv_object_cards"
    / "data"
    / "raw"
    / "watchlist_inputs"
    / "batch09_promoted"
    / "structured_inputs"
    / "factors_ladder_20260508.csv"
)
DEFAULT_WATCHLIST_CSV = (
    ROOT.parent
    / "butler_r0_ohlcv_object_cards"
    / "data"
    / "raw"
    / "watchlist_inputs"
    / "batch09_promoted"
    / "structured_inputs"
    / "watchlist_screen_20260508.csv"
)
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "t01_industry_distribution"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize T01 symbol trigger counts by industry mapping."
    )
    parser.add_argument(
        "--trigger-counts-tsv",
        default=str(DEFAULT_TRIGGER_COUNTS),
        help="TSV produced by run_t01_volume_price_scan_v1.py",
    )
    parser.add_argument(
        "--mapping-csv",
        default=str(DEFAULT_MAPPING_CSV),
        help="CSV with ticker/code/name/industry columns.",
    )
    parser.add_argument(
        "--watchlist-csv",
        default=str(DEFAULT_WATCHLIST_CSV),
        help="Optional watchlist CSV for enrichment.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for industry distribution artifacts.",
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


def load_mapping(mapping_csv: Path) -> dict[str, dict[str, str]]:
    mapping: dict[str, dict[str, str]] = {}
    with mapping_csv.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ticker = str(row.get("ticker", "")).strip()
            code = str(row.get("code", "")).strip()
            if ticker:
                mapping[ticker] = {
                    "ticker": ticker,
                    "code": code,
                    "name": str(row.get("name", "")).strip(),
                    "industry": str(row.get("industry", "")).strip(),
                    "source": str(row.get("source", "")).strip() or "factors_ladder_20260508",
                }
    return mapping


def load_watchlist(watchlist_csv: Path) -> dict[str, dict[str, str]]:
    if not watchlist_csv.exists():
        return {}
    watchlist: dict[str, dict[str, str]] = {}
    with watchlist_csv.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ticker = str(row.get("ticker", "")).strip()
            if ticker:
                watchlist[ticker] = {
                    "ticker": ticker,
                    "code": str(row.get("code", "")).strip(),
                    "name": str(row.get("name", "")).strip(),
                    "board": str(row.get("board", "")).strip(),
                }
    return watchlist


def main() -> int:
    args = parse_args()
    trigger_counts_tsv = Path(args.trigger_counts_tsv)
    mapping_csv = Path(args.mapping_csv)
    watchlist_csv = Path(args.watchlist_csv)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_path = output_dir / "t01_industry_distribution_summary_latest.json"
    industry_counts_path = output_dir / "t01_industry_trigger_counts_latest.tsv"
    joined_path = output_dir / "t01_symbol_industry_join_latest.tsv"
    unmatched_path = output_dir / "t01_unmatched_symbols_latest.tsv"

    metadata: dict[str, Any] = {
        "producer": "run_t01_industry_distribution_v1.py",
        "scope": "A股 P0 首轮离线验证 T01 行业分布",
        "status": "started",
        "trigger_counts_tsv": str(trigger_counts_tsv).replace("\\", "/"),
        "mapping_csv": str(mapping_csv).replace("\\", "/"),
        "watchlist_csv": str(watchlist_csv).replace("\\", "/"),
        "output_dir": str(output_dir).replace("\\", "/"),
    }

    if not trigger_counts_tsv.exists():
        metadata["status"] = "failed"
        metadata["failure_reason"] = "trigger_counts_missing"
        write_json(summary_path, metadata)
        return 2
    if not mapping_csv.exists():
        metadata["status"] = "failed"
        metadata["failure_reason"] = "mapping_csv_missing"
        write_json(summary_path, metadata)
        return 3

    mapping = load_mapping(mapping_csv)
    watchlist = load_watchlist(watchlist_csv)

    joined_rows: list[dict[str, Any]] = []
    unmatched_rows: list[dict[str, Any]] = []
    industry_counter: Counter[str] = Counter()
    matched_symbol_count = 0
    matched_trigger_weight = 0
    total_trigger_weight = 0

    with trigger_counts_tsv.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            symbol = str(row.get("symbol", "")).strip()
            trigger_count = int(float(str(row.get("trigger_count", "0")).strip() or "0"))
            total_trigger_weight += trigger_count
            mapping_row = mapping.get(symbol)
            watchlist_row = watchlist.get(symbol, {})
            industry = mapping_row["industry"] if mapping_row else "UNKNOWN"
            name = (
                (mapping_row or {}).get("name")
                or watchlist_row.get("name", "")
            )
            board = watchlist_row.get("board", "")
            code = (mapping_row or {}).get("code") or watchlist_row.get("code", "")
            joined_rows.append(
                {
                    "symbol": symbol,
                    "code": code,
                    "name": name,
                    "board": board,
                    "industry": industry,
                    "trigger_count": trigger_count,
                    "mapping_status": "matched" if mapping_row else "unmatched",
                }
            )
            industry_counter[industry] += trigger_count
            if mapping_row:
                matched_symbol_count += 1
                matched_trigger_weight += trigger_count
            else:
                unmatched_rows.append(
                    {
                        "symbol": symbol,
                        "code": code,
                        "name": name,
                        "board": board,
                        "trigger_count": trigger_count,
                    }
                )

    joined_rows.sort(key=lambda row: (-int(row["trigger_count"]), str(row["symbol"])))
    unmatched_rows.sort(key=lambda row: (-int(row["trigger_count"]), str(row["symbol"])))
    industry_rows = [
        {
            "industry": industry,
            "trigger_count": count,
            "trigger_weight_share": round(count / total_trigger_weight, 6)
            if total_trigger_weight
            else 0.0,
        }
        for industry, count in sorted(
            industry_counter.items(), key=lambda item: (-item[1], item[0])
        )
    ]

    metadata["status"] = "success"
    metadata["matched_symbols"] = matched_symbol_count
    metadata["unmatched_symbols"] = len(unmatched_rows)
    metadata["match_ratio"] = (
        round(matched_symbol_count / len(joined_rows), 6) if joined_rows else 0.0
    )
    metadata["matched_trigger_weight"] = matched_trigger_weight
    metadata["total_trigger_weight"] = total_trigger_weight
    metadata["matched_trigger_weight_ratio"] = (
        round(matched_trigger_weight / total_trigger_weight, 6)
        if total_trigger_weight
        else 0.0
    )
    metadata["top_industries"] = industry_rows[:5]
    metadata["output_files"] = {
        "summary_json": str(summary_path).replace("\\", "/"),
        "industry_counts_tsv": str(industry_counts_path).replace("\\", "/"),
        "symbol_join_tsv": str(joined_path).replace("\\", "/"),
        "unmatched_tsv": str(unmatched_path).replace("\\", "/"),
    }

    write_tsv(
        industry_counts_path,
        industry_rows,
        ["industry", "trigger_count", "trigger_weight_share"],
    )
    write_tsv(
        joined_path,
        joined_rows,
        ["symbol", "code", "name", "board", "industry", "trigger_count", "mapping_status"],
    )
    write_tsv(
        unmatched_path,
        unmatched_rows,
        ["symbol", "code", "name", "board", "trigger_count"],
    )
    write_json(summary_path, metadata)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
