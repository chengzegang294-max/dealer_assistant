from __future__ import annotations

import argparse
import csv
import json
import struct
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Optional


HEADER_SIZE = 148
RECORD_SIZE = 60
RECORD_STRUCT = struct.Struct("<Qddddqiq")

DEFAULT_INPUT = Path(
    r"D:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\VTMarkets-Live 2\GBPUSD-VIP15.hst"
)
DEFAULT_DEST = Path(__file__).resolve().parent / "n02_real_input_gbpusd_m15_v1.csv"
DEFAULT_REPORT = Path(__file__).resolve().parent / "n02_real_input_gbpusd_m15_report_v1.json"
CANONICAL_COLUMNS = ["symbol", "timeframe", "bar_time", "open", "high", "low", "close"]


@dataclass(frozen=True)
class HstRecord:
    timestamp: int
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    tick_volume: int
    spread: int
    real_volume: int

    @classmethod
    def from_bytes(cls, raw: bytes) -> "HstRecord":
        unpacked = RECORD_STRUCT.unpack(raw)
        return cls(
            timestamp=int(unpacked[0]),
            open_price=float(unpacked[1]),
            high_price=float(unpacked[2]),
            low_price=float(unpacked[3]),
            close_price=float(unpacked[4]),
            tick_volume=int(unpacked[5]),
            spread=int(unpacked[6]),
            real_volume=int(unpacked[7]),
        )


@dataclass(frozen=True)
class HstFile:
    path: Path
    header: bytes
    records: list[HstRecord]


def dt_from_ts(ts: Optional[int]) -> Optional[str]:
    if ts is None:
        return None
    return datetime.fromtimestamp(ts, UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_hst(path: Path) -> HstFile:
    raw = path.read_bytes()
    if len(raw) < HEADER_SIZE:
        raise ValueError(f"hst too small: {path}")
    body = raw[HEADER_SIZE:]
    if len(body) % RECORD_SIZE != 0:
        raise ValueError(f"hst body size mismatch: {path}")
    records = [
        HstRecord.from_bytes(body[offset : offset + RECORD_SIZE])
        for offset in range(0, len(body), RECORD_SIZE)
    ]
    return HstFile(path=path, header=raw[:HEADER_SIZE], records=records)


def timeframe_to_minutes(timeframe: str) -> int:
    tf = timeframe.strip().upper()
    if tf.startswith("M") and tf[1:].isdigit():
        return int(tf[1:])
    if tf.startswith("H") and tf[1:].isdigit():
        return int(tf[1:]) * 60
    raise ValueError(f"unsupported timeframe: {timeframe}")


def to_iso_utc(ts: int) -> str:
    return datetime.fromtimestamp(ts, UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def backup_if_exists(path: Path) -> Optional[Path]:
    if not path.exists():
        return None
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    backup_path = path.with_name(f"{path.name}.bak_{stamp}")
    path.replace(backup_path)
    return backup_path


def analyze_records(records: list[HstRecord]) -> dict[str, Any]:
    unique_minute_components = sorted(
        {
            datetime.fromtimestamp(record.timestamp, UTC).strftime("%M")
            for record in records
        }
    )
    step_histogram: dict[str, int] = {}
    for previous, current in zip(records, records[1:]):
        minutes = int((current.timestamp - previous.timestamp) / 60)
        key = str(minutes)
        step_histogram[key] = step_histogram.get(key, 0) + 1
    return {
        "record_count": len(records),
        "first_bar_time": dt_from_ts(records[0].timestamp if records else None),
        "last_bar_time": dt_from_ts(records[-1].timestamp if records else None),
        "unique_minute_components": unique_minute_components,
        "step_minutes_histogram": dict(sorted(step_histogram.items(), key=lambda item: int(item[0]))),
    }


def write_canonical(dest: Path, symbol: str, timeframe: str, records: list[HstRecord]) -> Optional[Path]:
    backup_path = backup_if_exists(dest)
    with dest.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CANONICAL_COLUMNS)
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "bar_time": to_iso_utc(record.timestamp),
                    "open": str(record.open_price),
                    "high": str(record.high_price),
                    "low": str(record.low_price),
                    "close": str(record.close_price),
                }
            )
    return backup_path


def build_report(
    source_path: Path,
    dest_path: Path,
    dest_backup_path: Optional[Path],
    report_path: Path,
    symbol: str,
    timeframe: str,
    timeframe_minutes: int,
    hst: HstFile,
) -> dict[str, Any]:
    analysis = analyze_records(hst.records)
    return {
        "producer": "n02_mt4_hst_ingest_v1.py",
        "scope": "REOPEN_B9_N02_SECOND_FX_SUBHOUR_HISTORICAL_RECOVERY_GBPUSD_M15_P0",
        "status": "historical_recovered_mt4_hst_to_canonical_bars",
        "evidence_mode": "historical_recovered_mt4_hst_to_canonical_bars_without_touching_main_m1_runtime",
        "generated_at_utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_path": {
            "hst_input": str(source_path),
        },
        "repo_path": {
            "canonical_bars_csv": str(dest_path),
            "canonical_bars_backup": str(dest_backup_path) if dest_backup_path else None,
            "report_json": str(report_path),
        },
        "boundary": {
            "writes_main_m1_runtime": False,
            "historical_recovered": True,
            "declares_terminal_fresh_export": False,
            "declares_failed_breakout": False,
        },
        "contract": {
            "symbol": symbol,
            "timeframe": timeframe,
            "timeframe_minutes": timeframe_minutes,
            "timezone_assumption": "utc_direct_from_mt4_hst_epoch_timestamps",
            "header_size": HEADER_SIZE,
            "record_size": RECORD_SIZE,
        },
        "analysis": analysis,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--timeframe", required=True)
    parser.add_argument("--dest", default=str(DEFAULT_DEST))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.input)
    dest_path = Path(args.dest)
    report_path = Path(args.report)
    timeframe_minutes = timeframe_to_minutes(args.timeframe)

    if not input_path.exists():
        raise FileNotFoundError(str(input_path))

    hst = load_hst(input_path)
    dest_backup_path: Optional[Path] = None
    if not args.dry_run:
        dest_backup_path = write_canonical(
            dest=dest_path,
            symbol=args.symbol,
            timeframe=args.timeframe,
            records=hst.records,
        )

    report = build_report(
        source_path=input_path,
        dest_path=dest_path,
        dest_backup_path=dest_backup_path,
        report_path=report_path,
        symbol=args.symbol,
        timeframe=args.timeframe,
        timeframe_minutes=timeframe_minutes,
        hst=hst,
    )
    if not args.dry_run:
        report_path.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding="utf-8")

    print(f"input={input_path}")
    print(f"dest={dest_path}")
    print(f"report={report_path}")
    print(f"record_count={report['analysis']['record_count']}")
    print(f"first_bar_time={report['analysis']['first_bar_time']}")
    print(f"last_bar_time={report['analysis']['last_bar_time']}")
    print(f"unique_minute_components={json.dumps(report['analysis']['unique_minute_components'], ensure_ascii=True)}")


if __name__ == "__main__":
    main()
