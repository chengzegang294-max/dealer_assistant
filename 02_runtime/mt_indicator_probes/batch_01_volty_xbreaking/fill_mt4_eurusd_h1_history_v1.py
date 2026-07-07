from __future__ import annotations

import argparse
import json
import shutil
import struct
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Optional

HEADER_SIZE = 148
RECORD_SIZE = 60
RECORD_STRUCT = struct.Struct("<Qddddqiq")

BATCH_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BATCH_DIR.parents[2]
_PORTABLE_ROOT_OVERRIDE = str(__import__("os").environ.get("MT4_PORTABLE_ROOT", "")).strip()
PORTABLE_ROOT = (
    Path(_PORTABLE_ROOT_OVERRIDE).expanduser()
    if _PORTABLE_ROOT_OVERRIDE
    else PROJECT_ROOT
    / "12_tooling_runtime_archive"
    / "batch_05_legacy_mt4_probe_assets__20260706"
    / "03_MT4便携探针实例"
)
ARTIFACT_ROOT = BATCH_DIR / "artifacts" / "volty" / "history_patch"
BACKUP_ROOT = ARTIFACT_ROOT / "backups"
SUMMARY_PATH = ARTIFACT_ROOT / "fill_mt4_eurusd_h1_history_latest.json"

TARGET_FILES = (
    PORTABLE_ROOT / "history" / "ICMarketsSC-Demo03" / "EURUSD60.hst",
    PORTABLE_ROOT / "history" / "default" / "EURUSD60.hst",
)
SOURCE_FILE = PORTABLE_ROOT / "history" / "VTMarkets-Live 2" / "EURUSD-VIP60.hst"
TARGET_FXT = PORTABLE_ROOT / "tester" / "history" / "EURUSD60_0.fxt"

WINDOW_START_TS = int(datetime(2025, 1, 1, tzinfo=UTC).timestamp())
WINDOW_END_TS = int(datetime(2025, 1, 15, tzinfo=UTC).timestamp())


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
            timestamp=unpacked[0],
            open_price=unpacked[1],
            high_price=unpacked[2],
            low_price=unpacked[3],
            close_price=unpacked[4],
            tick_volume=unpacked[5],
            spread=unpacked[6],
            real_volume=unpacked[7],
        )

    def to_bytes(self) -> bytes:
        return RECORD_STRUCT.pack(
            self.timestamp,
            self.open_price,
            self.high_price,
            self.low_price,
            self.close_price,
            self.tick_volume,
            self.spread,
            self.real_volume,
        )


@dataclass(frozen=True)
class HstFile:
    path: Path
    header: bytes
    records: list[HstRecord]

    @property
    def record_count(self) -> int:
        return len(self.records)

    def first_timestamp(self) -> Optional[int]:
        if not self.records:
            return None
        return self.records[0].timestamp

    def last_timestamp(self) -> Optional[int]:
        if not self.records:
            return None
        return self.records[-1].timestamp


def dt_from_ts(ts: Optional[int]) -> Optional[str]:
    if ts is None:
        return None
    return datetime.fromtimestamp(ts, UTC).isoformat()


def load_hst(path: Path) -> HstFile:
    raw = path.read_bytes()
    if len(raw) < HEADER_SIZE:
        raise ValueError(f"hst too small: {path}")
    body = raw[HEADER_SIZE:]
    if len(body) % RECORD_SIZE != 0:
        raise ValueError(f"hst body size mismatch: {path}")
    header = raw[:HEADER_SIZE]
    records = [
        HstRecord.from_bytes(body[offset : offset + RECORD_SIZE])
        for offset in range(0, len(body), RECORD_SIZE)
    ]
    return HstFile(path=path, header=header, records=records)


def write_hst(target_path: Path, header: bytes, records: list[HstRecord]) -> None:
    body = b"".join(record.to_bytes() for record in records)
    target_path.write_bytes(header + body)


def backup_file(path: Path, stamp: str) -> Optional[Path]:
    if not path.exists():
        return None
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_ROOT / f"{path.name}.{stamp}.bak"
    shutil.copy2(path, backup_path)
    return backup_path


def ts_in_window(ts: int) -> bool:
    return WINDOW_START_TS <= ts <= WINDOW_END_TS


def window_stats(records: list[HstRecord]) -> dict[str, Any]:
    hits = [record.timestamp for record in records if ts_in_window(record.timestamp)]
    return {
        "window_count": len(hits),
        "window_first": dt_from_ts(hits[0] if hits else None),
        "window_last": dt_from_ts(hits[-1] if hits else None),
    }


def merge_records(target_records: list[HstRecord], source_records: list[HstRecord]) -> tuple[list[HstRecord], int]:
    merged: dict[int, HstRecord] = {record.timestamp: record for record in target_records}
    inserted = 0
    for record in source_records:
        if record.timestamp not in merged:
            merged[record.timestamp] = record
            inserted += 1
    merged_records = [merged[timestamp] for timestamp in sorted(merged)]
    return merged_records, inserted


def build_summary_entry(label: str, path: Path, before_records: list[HstRecord], after_records: list[HstRecord], backup_path: Optional[Path], inserted: int) -> dict[str, Any]:
    return {
        "label": label,
        "path": str(path),
        "backup_path": str(backup_path) if backup_path else None,
        "before_record_count": len(before_records),
        "after_record_count": len(after_records),
        "before_first": dt_from_ts(before_records[0].timestamp if before_records else None),
        "before_last": dt_from_ts(before_records[-1].timestamp if before_records else None),
        "after_first": dt_from_ts(after_records[0].timestamp if after_records else None),
        "after_last": dt_from_ts(after_records[-1].timestamp if after_records else None),
        "inserted_records": inserted,
        "before_window": window_stats(before_records),
        "after_window": window_stats(after_records),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fill EURUSD/H1 history gap for MT4 portable Volty rerun.")
    parser.add_argument("--dry-run", action="store_true", help="Inspect merge result without writing files.")
    parser.add_argument("--keep-fxt", action="store_true", help="Do not delete the existing tester FXT file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)

    if not PORTABLE_ROOT.exists():
        raise FileNotFoundError(f"portable root not found: {PORTABLE_ROOT}")
    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f"source hst not found: {SOURCE_FILE}")

    source_hst = load_hst(SOURCE_FILE)
    summary: dict[str, Any] = {
        "format": "fill_mt4_eurusd_h1_history_v1",
        "run_mode": "dry_run" if args.dry_run else "write",
        "portable_root": str(PORTABLE_ROOT),
        "source_file": str(SOURCE_FILE),
        "source_record_count": source_hst.record_count,
        "source_window": window_stats(source_hst.records),
        "targets": [],
        "fxt": {},
    }

    for target_path in TARGET_FILES:
        if not target_path.exists():
            raise FileNotFoundError(f"target hst not found: {target_path}")

        target_hst = load_hst(target_path)
        merged_records, inserted = merge_records(target_hst.records, source_hst.records)
        backup_path: Optional[Path] = None

        if not args.dry_run:
            backup_path = backup_file(target_path, stamp)
            write_hst(target_path, target_hst.header, merged_records)

        summary["targets"].append(
            build_summary_entry(
                label=target_path.parent.name,
                path=target_path,
                before_records=target_hst.records,
                after_records=merged_records,
                backup_path=backup_path,
                inserted=inserted,
            )
        )

    fxt_backup_path: Optional[Path] = None
    fxt_deleted = False
    if TARGET_FXT.exists() and not args.keep_fxt and not args.dry_run:
        fxt_backup_path = backup_file(TARGET_FXT, stamp)
        TARGET_FXT.unlink()
        fxt_deleted = True
    summary["fxt"] = {
        "path": str(TARGET_FXT),
        "exists_before": TARGET_FXT.exists() if args.dry_run else bool(fxt_backup_path) or TARGET_FXT.exists(),
        "backup_path": str(fxt_backup_path) if fxt_backup_path else None,
        "deleted": fxt_deleted,
    }

    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
