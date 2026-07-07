from __future__ import annotations

import argparse
import csv
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

CONTRACT_VERSION = "purchased_csv_contract_v1"
BATCH_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BATCH_DIR.parents[2]
DEFAULT_OUTPUT_ROOT = BATCH_DIR / "artifacts" / "purchased_csv_contract_preview"
DEFAULT_PURCHASED_DATA_ROOT = PROJECT_ROOT / "00_assets" / "purchased_market_data"

REQUIRED_INPUT_COLUMNS = ("date", "time", "open", "high", "low", "close")
OPTIONAL_VOLUME_COLUMNS = ("tick_volume", "volume")
NORMALIZED_COLUMNS = (
    "bar_time",
    "symbol",
    "timeframe",
    "open",
    "high",
    "low",
    "close",
    "tick_volume",
    "source_path",
    "source_row_number",
    "contract_version",
)

BROKER_ALIAS_BY_STEM = {
    "_xau_test_1h": "XAUUSD",
    "dollaridxusd_1h": "USIDX",
    "gbridxgbp_1h": "UK100",
    "ger30_1h": "GER40",
    "ukoil_1h": "XBRUSD",
    "usoil_1h": "XTIUSD",
    "xtiusd_1h": "XTIUSD",
}

PRESET_INPUTS = {
    "p1_core": (
        "@purchased:eurusd_1h.csv",
        "@purchased:gbpusd_1h.csv",
        "@purchased:usdjpy_1h.csv",
        "@purchased:xauusd_1h.csv",
        "@purchased:xagusd_1h.csv",
        "@purchased:_xau_test_1h.csv",
        "@purchased:US30_1h.csv",
        "@purchased:nas100_1h.csv",
        "@purchased:usoil_1h.csv",
        "@purchased:xtiusd_1h.csv",
    ),
    "p2_ohlc_fx": (
        "@purchased:audusd_1h.csv",
        "@purchased:nzdusd_1h.csv",
        "@purchased:usdcad_1h.csv",
        "@purchased:usdchf_1h.csv",
        "@purchased:eurjpy_1h.csv",
        "@purchased:gbpjpy_1h.csv",
        "@purchased:AUDJPY_1h.csv",
        "@purchased:AUDNZD_1h.csv",
        "@purchased:CADJPY_1h.csv",
        "@purchased:CHFJPY_1h.csv",
        "@purchased:EURAUD_1h.csv",
        "@purchased:EURCHF_1h.csv",
        "@purchased:EURGBP_1h.csv",
        "@purchased:EURNZD_1h.csv",
        "@purchased:GBPCHF_1h.csv",
        "@purchased:NZDJPY_1h.csv",
    ),
    "p2_ohlc_indices": (
        "@purchased:ger40_1h.csv",
        "@purchased:us500_1h.csv",
        "@purchased:GER30_1h.csv",
        "@purchased:GBRIDXGBP_1h.csv",
    ),
    "p2_ohlc_commodity_macro": (
        "@purchased:UKOIL_1h.csv",
        "@purchased:XCUUSD_1h.csv",
        "@purchased:dollaridxusd_1h.csv",
    ),
    "p2_ohlc_all": (
        "@purchased:audusd_1h.csv",
        "@purchased:nzdusd_1h.csv",
        "@purchased:usdcad_1h.csv",
        "@purchased:usdchf_1h.csv",
        "@purchased:eurjpy_1h.csv",
        "@purchased:gbpjpy_1h.csv",
        "@purchased:AUDJPY_1h.csv",
        "@purchased:AUDNZD_1h.csv",
        "@purchased:CADJPY_1h.csv",
        "@purchased:CHFJPY_1h.csv",
        "@purchased:EURAUD_1h.csv",
        "@purchased:EURCHF_1h.csv",
        "@purchased:EURGBP_1h.csv",
        "@purchased:EURNZD_1h.csv",
        "@purchased:GBPCHF_1h.csv",
        "@purchased:NZDJPY_1h.csv",
        "@purchased:ger40_1h.csv",
        "@purchased:us500_1h.csv",
        "@purchased:GER30_1h.csv",
        "@purchased:GBRIDXGBP_1h.csv",
        "@purchased:UKOIL_1h.csv",
        "@purchased:XCUUSD_1h.csv",
        "@purchased:dollaridxusd_1h.csv",
    ),
}


@dataclass(frozen=True)
class NormalizedRow:
    bar_time: str
    symbol: str
    timeframe: str
    open: str
    high: str
    low: str
    close: str
    tick_volume: str
    source_path: str
    source_row_number: str
    contract_version: str


@dataclass(frozen=True)
class SampleSummary:
    input_path: str
    output_path: str
    file_stem: str
    inferred_symbol: str
    broker_symbol: str
    timeframe: str
    row_count: int
    source_columns: list[str]
    normalized_columns: list[str]
    first_bar_time: Optional[str]
    last_bar_time: Optional[str]
    volume_source_column: Optional[str]

@dataclass(frozen=True)
class SampleError:
    input_path: str
    error_type: str
    error_message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        dest="inputs",
        action="append",
        help="absolute or repo-relative CSV path; may be passed multiple times",
    )
    parser.add_argument(
        "--preset",
        choices=tuple(sorted(PRESET_INPUTS.keys())),
        help="expand a built-in input set such as p1_core",
    )
    parser.add_argument(
        "--archive-tag",
        default="p1_contract_preview_20260702T0428",
        help="archive tag under artifacts/purchased_csv_contract_preview",
    )
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help="root directory for persisted preview archives",
    )
    parser.add_argument(
        "--persist",
        action="store_true",
        help="write normalized csv files, run_summary.json and ingest_manifest.json",
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="print JSON summary only",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="skip a bad input and record its error instead of aborting the whole run",
    )
    args = parser.parse_args()
    if not args.inputs and not args.preset:
        parser.error("at least one --input or one --preset is required")
    return args


def purchased_data_root() -> Path:
    override = os.environ.get("PURCHASED_MARKET_DATA_ROOT", "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return DEFAULT_PURCHASED_DATA_ROOT


def resolve_input_path(raw_value: str) -> Path:
    if raw_value.startswith("@purchased:"):
        name = raw_value.split(":", 1)[1].strip()
        if not name:
            raise ValueError(f"invalid purchased csv selector: {raw_value}")
        return purchased_data_root() / name
    candidate = Path(raw_value)
    if candidate.is_absolute():
        return candidate
    return PROJECT_ROOT / candidate


def infer_symbol_and_timeframe(path: Path) -> tuple[str, str, str]:
    stem_lower = path.stem.lower()
    parts = stem_lower.split("_")
    if len(parts) < 2:
        raise ValueError(f"cannot infer symbol/timeframe from filename: {path.name}")
    timeframe = parts[-1].upper()
    inferred_symbol = "_".join(parts[:-1]).upper()
    broker_symbol = BROKER_ALIAS_BY_STEM.get(stem_lower, inferred_symbol)
    if stem_lower in BROKER_ALIAS_BY_STEM:
        inferred_symbol = broker_symbol
    return inferred_symbol, broker_symbol, timeframe


def detect_volume_column(fieldnames: list[str]) -> Optional[str]:
    normalized = {name.strip().lower(): name for name in fieldnames}
    for candidate in OPTIONAL_VOLUME_COLUMNS:
        if candidate in normalized:
            return normalized[candidate]
    return None


def build_bar_time(date_value: str, time_value: str) -> str:
    combined = f"{date_value.strip()} {time_value.strip()}"
    parsed = datetime.strptime(combined, "%Y.%m.%d %H:%M")
    return parsed.strftime("%Y-%m-%dT%H:%M:%S")


def normalize_one_file(input_path: Path, output_dir: Path) -> tuple[SampleSummary, list[NormalizedRow]]:
    inferred_symbol, broker_symbol, timeframe = infer_symbol_and_timeframe(input_path)
    with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        missing = [name for name in REQUIRED_INPUT_COLUMNS if name not in fieldnames]
        if missing:
            raise ValueError(f"{input_path} missing required columns: {missing}")
        volume_column = detect_volume_column(fieldnames)
        normalized_rows: list[NormalizedRow] = []
        for index, row in enumerate(reader, start=2):
            bar_time = build_bar_time(row["date"], row["time"])
            tick_volume = ""
            if volume_column:
                tick_volume = row.get(volume_column, "").strip()
            normalized_rows.append(
                NormalizedRow(
                    bar_time=bar_time,
                    symbol=broker_symbol,
                    timeframe=timeframe,
                    open=row["open"].strip(),
                    high=row["high"].strip(),
                    low=row["low"].strip(),
                    close=row["close"].strip(),
                    tick_volume=tick_volume,
                    source_path=str(input_path),
                    source_row_number=str(index),
                    contract_version=CONTRACT_VERSION,
                )
            )

    output_path = output_dir / f"{input_path.stem}__normalized.csv"
    summary = SampleSummary(
        input_path=str(input_path),
        output_path=str(output_path),
        file_stem=input_path.stem,
        inferred_symbol=inferred_symbol,
        broker_symbol=broker_symbol,
        timeframe=timeframe,
        row_count=len(normalized_rows),
        source_columns=fieldnames,
        normalized_columns=list(NORMALIZED_COLUMNS),
        first_bar_time=normalized_rows[0].bar_time if normalized_rows else None,
        last_bar_time=normalized_rows[-1].bar_time if normalized_rows else None,
        volume_source_column=volume_column,
    )
    return summary, normalized_rows


def write_normalized_csv(path: Path, rows: list[NormalizedRow]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(NORMALIZED_COLUMNS))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_json(path: Path, payload: object) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def build_run_summary(
    archive_tag: str,
    archive_root: Path,
    output_dir: Path,
    summaries: list[SampleSummary],
    errors: list[SampleError],
) -> dict[str, object]:
    return {
        "format": "purchased_csv_contract_run_summary_v1",
        "archive_tag": archive_tag,
        "archive_root": str(archive_root),
        "script_path": str(Path(__file__).resolve()),
        "contract_version": CONTRACT_VERSION,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "normalized_output_dir": str(output_dir),
        "sample_count": len(summaries),
        "samples": [asdict(item) for item in summaries],
        "error_count": len(errors),
        "errors": [asdict(item) for item in errors],
    }


def build_ingest_manifest(archive_tag: str, archive_root: Path, summaries: list[SampleSummary]) -> dict[str, object]:
    records: list[dict[str, object]] = []
    for item in summaries:
        records.append(
            {
                "family": "purchased_csv_contract_preview",
                "kind": "csv",
                "archive_tag": archive_tag,
                "copied_at": datetime.now().isoformat(timespec="seconds"),
                "selection_mode": "historical_recovered",
                "source_path": item.input_path,
                "repo_path": item.output_path,
                "repo_target_dir": str(Path(item.output_path).parent),
                "evidence_mode": "historical_recovered",
                "note": "normalized from legacy purchased csv into preview contract",
            }
        )
    return {
        "format": "probe_artifact_ingest_manifest_v1",
        "family": "purchased_csv_contract_preview",
        "archive_tag": archive_tag,
        "archive_root": str(archive_root),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "records": records,
    }


def main() -> None:
    args = parse_args()
    archive_root = Path(args.output_root)
    if not archive_root.is_absolute():
        archive_root = PROJECT_ROOT / archive_root
    archive_dir = archive_root / args.archive_tag
    normalized_dir = archive_dir / "normalized"

    raw_inputs: list[str] = []
    if args.preset:
        raw_inputs.extend(PRESET_INPUTS[args.preset])
    if args.inputs:
        raw_inputs.extend(args.inputs)
    deduped_inputs = list(dict.fromkeys(raw_inputs))
    input_paths = [resolve_input_path(item) for item in deduped_inputs]
    summaries: list[SampleSummary] = []
    normalized_data: list[tuple[SampleSummary, list[NormalizedRow]]] = []
    errors: list[SampleError] = []

    for input_path in input_paths:
        try:
            summary, rows = normalize_one_file(input_path, normalized_dir)
        except Exception as exc:
            if not args.continue_on_error:
                raise
            errors.append(
                SampleError(
                    input_path=str(input_path),
                    error_type=type(exc).__name__,
                    error_message=str(exc),
                )
            )
            continue
        summaries.append(summary)
        normalized_data.append((summary, rows))

    run_summary = build_run_summary(args.archive_tag, archive_dir, normalized_dir, summaries, errors)
    ingest_manifest = build_ingest_manifest(args.archive_tag, archive_dir, summaries)

    if args.persist:
        normalized_dir.mkdir(parents=True, exist_ok=True)
        for summary, rows in normalized_data:
            write_normalized_csv(Path(summary.output_path), rows)
        write_json(archive_dir / "run_summary.json", run_summary)
        write_json(archive_dir / "ingest_manifest.json", ingest_manifest)

    payload = {
        "run_summary": run_summary,
        "ingest_manifest": ingest_manifest,
    }
    if args.json_only or not args.persist:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"archive_dir={archive_dir}")
        print(f"run_summary={archive_dir / 'run_summary.json'}")
        print(f"ingest_manifest={archive_dir / 'ingest_manifest.json'}")


if __name__ == "__main__":
    main()
