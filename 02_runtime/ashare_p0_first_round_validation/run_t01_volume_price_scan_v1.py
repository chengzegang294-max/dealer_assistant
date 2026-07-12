from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT_DIR = (
    ROOT.parent
    / "butler_r0_ohlcv_object_cards"
    / "data"
    / "raw"
    / "daily_ohlcv"
    / "batch09_promoted"
    / "ashare_clean"
)
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "t01_volume_price_scan"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan A-share daily CSVs for T01 volume/price anomaly triggers."
    )
    parser.add_argument(
        "--input-dir",
        default=str(DEFAULT_INPUT_DIR),
        help="Directory containing per-symbol daily CSV files.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for summary JSON/TSV artifacts.",
    )
    parser.add_argument(
        "--volume-ratio-threshold",
        type=float,
        default=1.8,
        help="Minimum current volume / trailing 20-day average volume ratio.",
    )
    parser.add_argument(
        "--pct-change-threshold",
        type=float,
        default=4.5,
        help="Minimum absolute day-over-day percent change.",
    )
    parser.add_argument(
        "--start-date",
        default="",
        help="Optional inclusive lower bound in YYYY-MM-DD.",
    )
    parser.add_argument(
        "--end-date",
        default="",
        help="Optional inclusive upper bound in YYYY-MM-DD.",
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


def safe_float(raw: str | None) -> float | None:
    if raw is None or raw == "":
        return None
    return float(raw)


def scan_symbol_csv(
    csv_path: Path,
    volume_ratio_threshold: float,
    pct_change_threshold: float,
    start_date: str,
    end_date: str,
) -> list[dict[str, Any]]:
    triggered_rows: list[dict[str, Any]] = []
    volume_window: deque[float] = deque(maxlen=20)
    prev_close: float | None = None

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required_columns = {"date", "close", "volume"}
        missing = required_columns - set(reader.fieldnames or [])
        if missing:
            raise ValueError(
                f"{csv_path.name} missing required columns: {', '.join(sorted(missing))}"
            )

        for row in reader:
            trade_date = row["date"]
            symbol = row.get("symbol", csv_path.stem.replace("_1d", ""))
            close = safe_float(row.get("close"))
            volume = safe_float(row.get("volume"))
            amount = safe_float(row.get("amount"))
            if close is None or volume is None:
                continue

            avg_volume = None
            pct_change = None
            if len(volume_window) == 20 and prev_close not in (None, 0):
                avg_volume = sum(volume_window) / 20.0
                pct_change = ((close - prev_close) / prev_close) * 100.0
                volume_ratio = volume / avg_volume if avg_volume else 0.0
                within_window = True
                if start_date and trade_date < start_date:
                    within_window = False
                if end_date and trade_date > end_date:
                    within_window = False
                if (
                    within_window
                    and
                    volume_ratio >= volume_ratio_threshold
                    and abs(pct_change) > pct_change_threshold
                ):
                    triggered_rows.append(
                        {
                            "trade_date": trade_date,
                            "symbol": symbol,
                            "close": round(close, 6),
                            "prev_close": round(prev_close, 6),
                            "pct_change": round(pct_change, 6),
                            "volume": round(volume, 6),
                            "ma20_volume": round(avg_volume, 6),
                            "volume_ratio": round(volume_ratio, 6),
                            "amount": round(amount, 6) if amount is not None else "",
                        }
                    )

            volume_window.append(volume)
            prev_close = close

    return triggered_rows


def main() -> int:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    metadata_path = output_dir / "t01_volume_price_scan_summary_latest.json"
    detail_path = output_dir / "t01_trigger_detail_latest.tsv"
    daily_path = output_dir / "t01_daily_trigger_counts_latest.tsv"
    symbol_path = output_dir / "t01_symbol_trigger_counts_latest.tsv"

    metadata: dict[str, Any] = {
        "producer": "run_t01_volume_price_scan_v1.py",
        "scope": "A股 P0 首轮离线验证 T01",
        "status": "started",
        "input_dir": str(input_dir).replace("\\", "/"),
        "output_dir": str(output_dir).replace("\\", "/"),
        "volume_ratio_threshold": args.volume_ratio_threshold,
        "pct_change_threshold": args.pct_change_threshold,
        "start_date": args.start_date,
        "end_date": args.end_date,
    }

    csv_files = sorted(input_dir.glob("*_1d.csv"))
    if not csv_files:
        metadata["status"] = "failed"
        metadata["failure_reason"] = "no_csv_found"
        write_json(metadata_path, metadata)
        return 2

    all_triggered_rows: list[dict[str, Any]] = []
    failed_files: list[str] = []
    scanned_rows = 0

    for csv_path in csv_files:
        try:
            triggered_rows = scan_symbol_csv(
                csv_path=csv_path,
                volume_ratio_threshold=args.volume_ratio_threshold,
                pct_change_threshold=args.pct_change_threshold,
                start_date=args.start_date,
                end_date=args.end_date,
            )
            all_triggered_rows.extend(triggered_rows)
            with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
                scanned_rows += sum(1 for _ in csv.DictReader(f))
        except Exception:
            failed_files.append(csv_path.name)

    daily_counter: Counter[str] = Counter()
    symbol_counter: Counter[str] = Counter()
    for row in all_triggered_rows:
        daily_counter[str(row["trade_date"])] += 1
        symbol_counter[str(row["symbol"])] += 1

    daily_rows = [
        {"trade_date": trade_date, "trigger_count": count}
        for trade_date, count in sorted(daily_counter.items())
    ]
    symbol_rows = [
        {"symbol": symbol, "trigger_count": count}
        for symbol, count in sorted(
            symbol_counter.items(), key=lambda item: (-item[1], item[0])
        )
    ]

    write_tsv(
        detail_path,
        all_triggered_rows,
        [
            "trade_date",
            "symbol",
            "close",
            "prev_close",
            "pct_change",
            "volume",
            "ma20_volume",
            "volume_ratio",
            "amount",
        ],
    )
    write_tsv(daily_path, daily_rows, ["trade_date", "trigger_count"])
    write_tsv(symbol_path, symbol_rows, ["symbol", "trigger_count"])

    daily_counts = [row["trigger_count"] for row in daily_rows]
    metadata["status"] = "success"
    metadata["files_scanned"] = len(csv_files)
    metadata["files_failed"] = failed_files
    metadata["rows_scanned"] = scanned_rows
    metadata["trigger_rows"] = len(all_triggered_rows)
    metadata["trigger_days"] = len(daily_rows)
    metadata["trigger_symbols"] = len(symbol_rows)
    metadata["daily_avg_trigger_count"] = (
        round(sum(daily_counts) / len(daily_counts), 6) if daily_counts else 0.0
    )
    metadata["daily_peak_trigger_count"] = max(daily_counts) if daily_counts else 0
    metadata["daily_median_like_trigger_count"] = (
        sorted(daily_counts)[len(daily_counts) // 2] if daily_counts else 0
    )
    metadata["output_files"] = {
        "summary_json": str(metadata_path).replace("\\", "/"),
        "trigger_detail_tsv": str(detail_path).replace("\\", "/"),
        "daily_counts_tsv": str(daily_path).replace("\\", "/"),
        "symbol_counts_tsv": str(symbol_path).replace("\\", "/"),
    }
    write_json(metadata_path, metadata)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
