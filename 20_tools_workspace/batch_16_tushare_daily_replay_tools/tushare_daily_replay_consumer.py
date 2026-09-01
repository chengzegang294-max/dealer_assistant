from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


EXPECTED_SOURCE_ID = "TUSHARE_A_SHARE_DAILY_SSE_SZSE_V1"
FORMAL_SCOPE = "FORMAL_SCOPE_SSE_AND_SZSE_ACTIVE_STOCKS"
EXCLUDED_BSE_SCOPE = "OUT_OF_SCOPE_OR_UNVERIFIED_BSE"
REPLAY_VALIDATED = "REPLAY_VALIDATED"
QUALITY_GATE_VERSION = "A5-RUNTIME-REPLAY-02"
PCT_CHG_ABS_TOLERANCE = 0.05
CHANGE_ABS_TOLERANCE = 0.011
FORMULA_VERSION = {
    "pct_chg": "change / pre_close * 100",
    "change": "close - pre_close",
}

MANIFEST_REQUIRED_FIELDS = {
    "manifest_key",
    "source_id",
    "snapshot_path",
    "api_name",
    "capture_time_utc",
    "source_response_sha256",
    "snapshot_file_sha256",
    "row_count",
    "field_list",
    "scope",
    "status",
}

REQUIRED_MANIFEST_KEYS = {
    "stock_basic_active",
    "trade_cal_sse",
    "trade_cal_szse",
    "daily_all_market",
    "adj_factor_all_market",
}

REQUIRED_RESPONSE_FIELDS_BY_KEY = {
    "stock_basic_active": [
        "ts_code",
        "symbol",
        "market",
        "exchange",
        "list_status",
        "list_date",
        "delist_date",
    ],
    "trade_cal_sse": ["exchange", "cal_date", "is_open", "pretrade_date"],
    "trade_cal_szse": ["exchange", "cal_date", "is_open", "pretrade_date"],
    "daily_all_market": [
        "ts_code",
        "trade_date",
        "open",
        "high",
        "low",
        "close",
        "pre_close",
        "change",
        "pct_chg",
        "vol",
        "amount",
    ],
    "adj_factor_all_market": ["ts_code", "trade_date", "adj_factor"],
}

RAW_DAILY_REQUIRED_FIELDS = [
    "open",
    "high",
    "low",
    "close",
    "pre_close",
    "change",
    "pct_chg",
    "vol",
    "amount",
]

NORMALIZED_OUTPUT_COLUMNS = [
    "source_id",
    "ts_code",
    "trade_date",
    "capture_time_utc",
    "source_response_sha256",
    "snapshot_file_sha256",
    "scope",
    "freshness_status",
    "replay_status",
    "exclusion_reason",
    "exchange",
    "list_status",
    "market",
    "open",
    "high",
    "low",
    "close",
    "pre_close",
    "change",
    "pct_chg",
    "vol",
    "amount",
    "adj_factor",
    "stock_basic_source_response_sha256",
    "stock_basic_snapshot_file_sha256",
    "adj_factor_source_response_sha256",
    "adj_factor_snapshot_file_sha256",
    "calendar_source_response_sha256",
    "calendar_snapshot_file_sha256",
]

EXCLUSION_COLUMNS = [
    "source_id",
    "manifest_key",
    "ts_code",
    "trade_date",
    "capture_time_utc",
    "source_response_sha256",
    "snapshot_file_sha256",
    "scope",
    "freshness_status",
    "replay_status",
    "exclusion_reason",
    "exchange",
    "list_status",
    "market",
]

PROHIBITED_OUTPUT_COLUMNS = {
    "turnover_rate",
    "qfq_close",
    "hfq_close",
    "qfq_close_end_date_bound",
    "sma5",
    "trange",
    "atr14_wilder",
    "gap",
}


class ReplayValidationError(Exception):
    def __init__(self, message: str, quality_report: dict[str, Any] | None = None):
        super().__init__(message)
        self.quality_report = quality_report


@dataclass(frozen=True)
class ManifestEntry:
    manifest_key: str
    source_id: str
    snapshot_path: str
    api_name: str
    capture_time_utc: str
    source_response_sha256: str
    snapshot_file_sha256: str
    row_count: int
    field_list: list[str]
    scope: str
    status: str


@dataclass
class LoadedSnapshot:
    entry: ManifestEntry
    absolute_path: Path
    file_sha256: str
    source_response_text: str
    response_sha256: str
    response_fields: list[str]
    response_items: list[list[Any]]
    records: list[dict[str, Any]]


@dataclass
class ReplayResult:
    normalized_rows: list[dict[str, Any]]
    exclusion_rows: list[dict[str, Any]]
    quality_report: dict[str, Any]
    summary: dict[str, Any]
    report_markdown: str


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_tsv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def build_quality_check(
    *,
    check_name: str,
    check_type: str,
    sample_row_count: int,
    failed_row_count: int,
    reason_counts: dict[str, int] | Counter[str] | None = None,
    tolerance: dict[str, float] | None = None,
    formula_version: str = "N/A",
) -> dict[str, Any]:
    normalized_reason_counts = dict(sorted((reason_counts or {}).items()))
    return {
        "check_name": check_name,
        "check_type": check_type,
        "status": "PASS" if failed_row_count == 0 else "FAIL",
        "sample_row_count": sample_row_count,
        "failed_row_count": failed_row_count,
        "reason_counts": normalized_reason_counts,
        "tolerance": tolerance or {},
        "formula_version": formula_version,
    }


def build_quality_report(
    *,
    run_status: str,
    checks: list[dict[str, Any]],
    sample_row_count: int,
    passed_row_count: int,
    excluded_row_count: int,
    out_of_scope_exclusion_row_count: int,
    quality_exclusion_row_count: int,
    quality_failed_row_count: int,
    exclusion_reason_counts: Counter[str] | None = None,
    blocking_reason_counts: Counter[str] | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    return {
        "run_status": run_status,
        "quality_gate_version": QUALITY_GATE_VERSION,
        "generated_at_utc": utc_now_iso(),
        "sample_row_count": sample_row_count,
        "passed_row_count": passed_row_count,
        "excluded_row_count": excluded_row_count,
        "out_of_scope_exclusion_row_count": out_of_scope_exclusion_row_count,
        "quality_exclusion_row_count": quality_exclusion_row_count,
        "quality_failed_row_count": quality_failed_row_count,
        "blocking_failure_count": sum((blocking_reason_counts or Counter()).values()),
        "exclusion_reason_counts": dict(sorted((exclusion_reason_counts or Counter()).items())),
        "blocking_reason_counts": dict(sorted((blocking_reason_counts or Counter()).items())),
        "tolerances": {
            "pct_chg_abs_tolerance": PCT_CHG_ABS_TOLERANCE,
            "change_abs_tolerance": CHANGE_ABS_TOLERANCE,
        },
        "formula_version": FORMULA_VERSION,
        "checks": checks,
        "error": error or "",
    }


def ensure_manifest_entry(raw_entry: dict[str, Any]) -> ManifestEntry:
    missing = sorted(MANIFEST_REQUIRED_FIELDS - set(raw_entry))
    if missing:
        raise ReplayValidationError(f"Manifest entry missing required fields: {', '.join(missing)}")
    if not isinstance(raw_entry["field_list"], list) or not raw_entry["field_list"]:
        raise ReplayValidationError("Manifest entry field_list must be a non-empty list.")
    return ManifestEntry(
        manifest_key=str(raw_entry["manifest_key"]),
        source_id=str(raw_entry["source_id"]),
        snapshot_path=str(raw_entry["snapshot_path"]),
        api_name=str(raw_entry["api_name"]),
        capture_time_utc=str(raw_entry["capture_time_utc"]),
        source_response_sha256=str(raw_entry["source_response_sha256"]),
        snapshot_file_sha256=str(raw_entry["snapshot_file_sha256"]),
        row_count=int(raw_entry["row_count"]),
        field_list=[str(item) for item in raw_entry["field_list"]],
        scope=str(raw_entry["scope"]),
        status=str(raw_entry["status"]),
    )


def load_manifest(manifest_path: Path) -> dict[str, ManifestEntry]:
    raw_manifest = read_json(manifest_path)
    raw_entries = raw_manifest.get("entries")
    if not isinstance(raw_entries, list) or not raw_entries:
        raise ReplayValidationError("Manifest must contain a non-empty 'entries' list.")

    entries = [ensure_manifest_entry(item) for item in raw_entries]
    manifest_map: dict[str, ManifestEntry] = {}
    for entry in entries:
        if entry.manifest_key in manifest_map:
            raise ReplayValidationError(f"Duplicate manifest_key detected: {entry.manifest_key}")
        if entry.source_id != EXPECTED_SOURCE_ID:
            raise ReplayValidationError(
                f"Unexpected source_id for {entry.manifest_key}: {entry.source_id}"
            )
        manifest_map[entry.manifest_key] = entry

    missing_keys = sorted(REQUIRED_MANIFEST_KEYS - set(manifest_map))
    if missing_keys:
        raise ReplayValidationError(
            f"Manifest is missing required snapshot keys: {', '.join(missing_keys)}"
        )
    return manifest_map


def resolve_snapshot_path(snapshot_root: Path, snapshot_path: str) -> Path:
    candidate = Path(snapshot_path)
    if candidate.is_absolute():
        raise ReplayValidationError(
            f"snapshot_path must be relative to --snapshot-root: {snapshot_path}"
        )
    resolved = (snapshot_root / candidate).resolve()
    try:
        resolved.relative_to(snapshot_root.resolve())
    except ValueError as exc:
        raise ReplayValidationError(f"snapshot_path escapes snapshot root: {snapshot_path}") from exc
    if not resolved.exists():
        raise ReplayValidationError(f"Snapshot file does not exist: {resolved}")
    return resolved


def validate_snapshot(entry: ManifestEntry, snapshot_root: Path) -> LoadedSnapshot:
    absolute_path = resolve_snapshot_path(snapshot_root, entry.snapshot_path)
    file_sha256 = sha256_file(absolute_path)
    if file_sha256 != entry.snapshot_file_sha256:
        raise ReplayValidationError(
            f"{entry.manifest_key} file SHA mismatch: expected {entry.snapshot_file_sha256}, got {file_sha256}"
        )

    snapshot = read_json(absolute_path)
    if str(snapshot.get("api_name")) != entry.api_name:
        raise ReplayValidationError(
            f"{entry.manifest_key} api_name mismatch: expected {entry.api_name}, got {snapshot.get('api_name')}"
        )
    if str(snapshot.get("capture_time_utc")) != entry.capture_time_utc:
        raise ReplayValidationError(
            f"{entry.manifest_key} capture_time_utc mismatch: expected {entry.capture_time_utc}, got {snapshot.get('capture_time_utc')}"
        )

    source_response_text = snapshot.get("source_response_text")
    if not isinstance(source_response_text, str) or not source_response_text:
        raise ReplayValidationError(f"{entry.manifest_key} is missing source_response_text.")
    response_sha256 = sha256_text(source_response_text)
    if response_sha256 != entry.source_response_sha256:
        raise ReplayValidationError(
            f"{entry.manifest_key} source response SHA mismatch: expected {entry.source_response_sha256}, got {response_sha256}"
        )

    response_json = json.loads(source_response_text)
    data_block = response_json.get("data")
    if not isinstance(data_block, dict):
        raise ReplayValidationError(f"{entry.manifest_key} response text is missing a data block.")

    response_fields = list(data_block.get("fields") or [])
    response_items = list(data_block.get("items") or [])
    if response_fields != entry.field_list:
        raise ReplayValidationError(
            f"{entry.manifest_key} field list mismatch: expected {entry.field_list}, got {response_fields}"
        )
    if len(response_items) != entry.row_count:
        raise ReplayValidationError(
            f"{entry.manifest_key} row_count mismatch: expected {entry.row_count}, got {len(response_items)}"
        )

    required_fields = REQUIRED_RESPONSE_FIELDS_BY_KEY[entry.manifest_key]
    missing_required_fields = [field for field in required_fields if field not in response_fields]
    if missing_required_fields:
        raise ReplayValidationError(
            f"{entry.manifest_key} response is missing required fields: {', '.join(missing_required_fields)}"
        )

    records = [dict(zip(response_fields, row)) for row in response_items]
    return LoadedSnapshot(
        entry=entry,
        absolute_path=absolute_path,
        file_sha256=file_sha256,
        source_response_text=source_response_text,
        response_sha256=response_sha256,
        response_fields=response_fields,
        response_items=response_items,
        records=records,
    )


def derive_latest_complete_trade_date(
    trade_cal_records: list[dict[str, Any]], capture_time_utc: str
) -> str | None:
    capture_date = capture_time_utc[:10].replace("-", "")
    for row in trade_cal_records:
        if str(row.get("cal_date")) == capture_date and str(row.get("is_open")) == "1":
            pretrade_date = str(row.get("pretrade_date") or "")
            return pretrade_date or None
    open_dates = sorted(
        str(row.get("cal_date"))
        for row in trade_cal_records
        if str(row.get("is_open")) == "1" and str(row.get("cal_date")) < capture_date
    )
    return open_dates[-1] if open_dates else None


def count_duplicate_keys(records: list[dict[str, Any]], key_fields: list[str]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for row in records:
        key = "|".join(str(row.get(field) or "") for field in key_fields)
        counter[key] += 1
    return Counter({key: count for key, count in counter.items() if count > 1})


def require_finite_float(value: Any, reason: str) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise ReplayValidationError(reason) from exc
    if not math.isfinite(numeric):
        raise ReplayValidationError(reason)
    return numeric


def build_exclusion_row(
    manifest_key: str,
    ts_code: str,
    trade_date: str,
    capture_time_utc: str,
    source_response_sha256: str,
    snapshot_file_sha256: str,
    scope: str,
    freshness_status: str,
    exclusion_reason: str,
    exchange: str = "",
    list_status: str = "",
    market: str = "",
) -> dict[str, Any]:
    return {
        "source_id": EXPECTED_SOURCE_ID,
        "manifest_key": manifest_key,
        "ts_code": ts_code,
        "trade_date": trade_date,
        "capture_time_utc": capture_time_utc,
        "source_response_sha256": source_response_sha256,
        "snapshot_file_sha256": snapshot_file_sha256,
        "scope": scope,
        "freshness_status": freshness_status,
        "replay_status": REPLAY_VALIDATED,
        "exclusion_reason": exclusion_reason,
        "exchange": exchange,
        "list_status": list_status,
        "market": market,
    }


def ensure_output_columns_are_raw_only(rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    actual_columns = set(rows[0])
    blocked = sorted(PROHIBITED_OUTPUT_COLUMNS & actual_columns)
    if blocked:
        raise ReplayValidationError(
            f"Normalized output contains prohibited columns: {', '.join(blocked)}"
        )


def write_failure_outputs(
    output_dir: Path,
    error_message: str,
    quality_report: dict[str, Any] | None = None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    final_quality_report = quality_report or build_quality_report(
        run_status="FAILED",
        checks=[
            build_quality_check(
                check_name="blocking_failure",
                check_type="blocking",
                sample_row_count=0,
                failed_row_count=1,
                reason_counts={"BLOCKING_FAILURE": 1},
            )
        ],
        sample_row_count=0,
        passed_row_count=0,
        excluded_row_count=0,
        out_of_scope_exclusion_row_count=0,
        quality_exclusion_row_count=0,
        quality_failed_row_count=0,
        blocking_reason_counts=Counter({"BLOCKING_FAILURE": 1}),
        error=error_message,
    )
    write_json(output_dir / "data_quality_report.json", final_quality_report)
    summary = {
        "status": "FAILED",
        "generated_at_utc": utc_now_iso(),
        "error": error_message,
        "normalized_output_row_count": 0,
        "exclusion_row_count": 0,
        "quality_report_file": "data_quality_report.json",
    }
    write_json(output_dir / "summary.json", summary)
    report = "\n".join(
        [
            "# Tushare A-share Daily Replay Validation Report",
            "",
            "- status: `FAILED`",
            f"- error: `{error_message}`",
            "- success output was blocked before normalized rows were written.",
            "- see `data_quality_report.json` for machine-readable check details.",
            "",
        ]
    )
    (output_dir / "replay_validation_report.md").write_text(report, encoding="utf-8")


def build_quality_report_markdown(
    summary: dict[str, Any],
    quality_report: dict[str, Any],
    loaded: dict[str, LoadedSnapshot],
) -> str:
    lines = [
        "# Tushare A-share Daily Replay Validation Report",
        "",
        f"- generated_at_utc: `{summary['generated_at_utc']}`",
        f"- run_status: `{quality_report['run_status']}`",
        f"- source_id: `{EXPECTED_SOURCE_ID}`",
        f"- formal_scope: `{FORMAL_SCOPE}`",
        f"- validated_snapshot_count: `{summary['validated_snapshot_count']}`",
        f"- normalized_output_row_count: `{summary['normalized_output_row_count']}`",
        f"- exclusion_row_count: `{summary['exclusion_row_count']}`",
        f"- out_of_scope_exclusion_row_count: `{quality_report['out_of_scope_exclusion_row_count']}`",
        f"- quality_exclusion_row_count: `{quality_report['quality_exclusion_row_count']}`",
        f"- quality_failed_row_count: `{quality_report['quality_failed_row_count']}`",
        f"- quality_report_file: `data_quality_report.json`",
        "",
        "## Tolerances And Formula Version",
        "",
        f"- pct_chg_abs_tolerance: `{PCT_CHG_ABS_TOLERANCE}`",
        f"- change_abs_tolerance: `{CHANGE_ABS_TOLERANCE}`",
        f"- pct_chg formula: `{FORMULA_VERSION['pct_chg']}`",
        f"- change formula: `{FORMULA_VERSION['change']}`",
        "",
        "## Latest Complete Trade Date",
        "",
        f"- SSE: `{summary['latest_complete_trade_date_by_exchange']['SSE']}`",
        f"- SZSE: `{summary['latest_complete_trade_date_by_exchange']['SZSE']}`",
        "",
        "## Reason Counts",
        "",
        f"- blocking_reason_counts: `{json.dumps(quality_report['blocking_reason_counts'], ensure_ascii=False, sort_keys=True)}`",
        f"- exclusion_reason_counts: `{json.dumps(quality_report['exclusion_reason_counts'], ensure_ascii=False, sort_keys=True)}`",
        "",
        "## Quality Checks",
        "",
    ]
    for check in quality_report["checks"]:
        lines.append(
            "- "
            f"`{check['check_name']}` | type=`{check['check_type']}` | status=`{check['status']}` | "
            f"sample_rows=`{check['sample_row_count']}` | failed_rows=`{check['failed_row_count']}` | "
            f"reason_counts=`{json.dumps(check['reason_counts'], ensure_ascii=False, sort_keys=True)}`"
        )

    lines.extend(["", "## Snapshot Inputs", ""])
    for key in sorted(loaded):
        snapshot = loaded[key]
        lines.append(
            f"- `{key}` | api_name=`{snapshot.entry.api_name}` | rows=`{snapshot.entry.row_count}` | "
            f"snapshot_path=`{snapshot.entry.snapshot_path}` | source_response_sha256=`{snapshot.response_sha256}` | "
            f"snapshot_file_sha256=`{snapshot.file_sha256}`"
        )
    lines.append("")
    return "\n".join(lines)


def write_success_outputs(output_dir: Path, result: ReplayResult) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_tsv(output_dir / "normalized_daily_output.tsv", result.normalized_rows, NORMALIZED_OUTPUT_COLUMNS)
    write_tsv(output_dir / "exclusion_register.tsv", result.exclusion_rows, EXCLUSION_COLUMNS)
    write_json(output_dir / "data_quality_report.json", result.quality_report)
    (output_dir / "replay_validation_report.md").write_text(result.report_markdown, encoding="utf-8")
    write_json(output_dir / "summary.json", result.summary)


def consume_snapshots(manifest_path: Path, snapshot_root: Path) -> ReplayResult:
    manifest = load_manifest(manifest_path)
    loaded = {key: validate_snapshot(entry, snapshot_root) for key, entry in manifest.items()}

    stock_basic = loaded["stock_basic_active"]
    trade_cal_sse = loaded["trade_cal_sse"]
    trade_cal_szse = loaded["trade_cal_szse"]
    daily = loaded["daily_all_market"]
    adj_factor = loaded["adj_factor_all_market"]

    checks: list[dict[str, Any]] = []
    blocking_reason_counts: Counter[str] = Counter()
    blocking_messages: list[str] = []

    stock_duplicates = count_duplicate_keys(stock_basic.records, ["ts_code"])
    checks.append(
        build_quality_check(
            check_name="stock_basic_ts_code_duplicate",
            check_type="blocking",
            sample_row_count=len(stock_basic.records),
            failed_row_count=sum(stock_duplicates.values()),
            reason_counts={"STOCK_BASIC_TS_CODE_DUPLICATE": sum(stock_duplicates.values())} if stock_duplicates else {},
        )
    )
    if stock_duplicates:
        blocking_reason_counts["STOCK_BASIC_TS_CODE_DUPLICATE"] += sum(stock_duplicates.values())
        blocking_messages.append("stock_basic contains duplicate ts_code rows")

    daily_duplicates = count_duplicate_keys(daily.records, ["ts_code", "trade_date"])
    checks.append(
        build_quality_check(
            check_name="daily_primary_key_duplicate",
            check_type="blocking",
            sample_row_count=len(daily.records),
            failed_row_count=sum(daily_duplicates.values()),
            reason_counts={"DAILY_PRIMARY_KEY_DUPLICATE": sum(daily_duplicates.values())} if daily_duplicates else {},
        )
    )
    if daily_duplicates:
        blocking_reason_counts["DAILY_PRIMARY_KEY_DUPLICATE"] += sum(daily_duplicates.values())
        blocking_messages.append("daily contains duplicate (ts_code, trade_date) rows")

    adj_duplicates = count_duplicate_keys(adj_factor.records, ["ts_code", "trade_date"])
    checks.append(
        build_quality_check(
            check_name="adj_factor_primary_key_duplicate",
            check_type="blocking",
            sample_row_count=len(adj_factor.records),
            failed_row_count=sum(adj_duplicates.values()),
            reason_counts={"ADJ_FACTOR_PRIMARY_KEY_DUPLICATE": sum(adj_duplicates.values())} if adj_duplicates else {},
        )
    )
    if adj_duplicates:
        blocking_reason_counts["ADJ_FACTOR_PRIMARY_KEY_DUPLICATE"] += sum(adj_duplicates.values())
        blocking_messages.append("adj_factor contains duplicate (ts_code, trade_date) rows")

    latest_complete_by_exchange = {
        "SSE": derive_latest_complete_trade_date(trade_cal_sse.records, trade_cal_sse.entry.capture_time_utc),
        "SZSE": derive_latest_complete_trade_date(trade_cal_szse.records, trade_cal_szse.entry.capture_time_utc),
    }
    if not latest_complete_by_exchange["SSE"] or not latest_complete_by_exchange["SZSE"]:
        blocking_reason_counts["LATEST_COMPLETE_TRADE_DATE_MISSING"] += 1
        checks.append(
            build_quality_check(
                check_name="latest_complete_trade_date",
                check_type="blocking",
                sample_row_count=2,
                failed_row_count=1,
                reason_counts={"LATEST_COMPLETE_TRADE_DATE_MISSING": 1},
            )
        )
        quality_report = build_quality_report(
            run_status="FAILED",
            checks=checks,
            sample_row_count=len(daily.records),
            passed_row_count=0,
            excluded_row_count=0,
            blocking_reason_counts=blocking_reason_counts,
            error="Unable to derive latest complete trade day for SSE/SZSE.",
        )
        raise ReplayValidationError("Unable to derive latest complete trade day for SSE/SZSE.", quality_report)
    checks.append(
        build_quality_check(
            check_name="latest_complete_trade_date",
            check_type="blocking",
            sample_row_count=2,
            failed_row_count=0,
        )
    )

    stock_by_ts = {str(row["ts_code"]): row for row in stock_basic.records}
    adj_factor_by_key = {
        (str(row["ts_code"]), str(row["trade_date"])): row for row in adj_factor.records
    }

    daily_numeric_failures: Counter[str] = Counter()
    parsed_daily_records: list[dict[str, Any]] = []
    for row in daily.records:
        parsed_row = dict(row)
        ts_code = str(row.get("ts_code") or "")
        trade_date = str(row.get("trade_date") or "")
        for field in RAW_DAILY_REQUIRED_FIELDS:
            value = row.get(field)
            if value in ("", None):
                daily_numeric_failures[f"DAILY_RAW_FIELD_MISSING_{field}"] += 1
                continue
            try:
                parsed_row[field] = require_finite_float(
                    value,
                    f"Daily row has non-finite numeric value for {field}: {ts_code}|{trade_date}",
                )
            except ReplayValidationError:
                daily_numeric_failures[f"DAILY_NON_NUMERIC_{field}"] += 1
        parsed_daily_records.append(parsed_row)

    checks.append(
        build_quality_check(
            check_name="daily_raw_fields_and_numeric_parse",
            check_type="blocking",
            sample_row_count=len(daily.records),
            failed_row_count=sum(daily_numeric_failures.values()),
            reason_counts=daily_numeric_failures,
        )
    )
    if daily_numeric_failures:
        blocking_reason_counts.update(daily_numeric_failures)
        blocking_messages.append("daily raw fields are missing or non-numeric")

    adj_numeric_failures: Counter[str] = Counter()
    parsed_adj_records: list[dict[str, Any]] = []
    for row in adj_factor.records:
        parsed_row = dict(row)
        ts_code = str(row.get("ts_code") or "")
        trade_date = str(row.get("trade_date") or "")
        value = row.get("adj_factor")
        if value in ("", None):
            adj_numeric_failures["ADJ_FACTOR_FIELD_MISSING"] += 1
        else:
            try:
                parsed_row["adj_factor"] = require_finite_float(
                    value,
                    f"Adj factor row has non-finite numeric value: {ts_code}|{trade_date}",
                )
            except ReplayValidationError:
                adj_numeric_failures["ADJ_FACTOR_NON_NUMERIC"] += 1
        parsed_adj_records.append(parsed_row)

    checks.append(
        build_quality_check(
            check_name="adj_factor_numeric_parse",
            check_type="blocking",
            sample_row_count=len(adj_factor.records),
            failed_row_count=sum(adj_numeric_failures.values()),
            reason_counts=adj_numeric_failures,
        )
    )
    if adj_numeric_failures:
        blocking_reason_counts.update(adj_numeric_failures)
        blocking_messages.append("adj_factor contains missing or non-numeric values")

    unmatched_daily_count = 0
    non_active_daily_count = 0
    latest_complete_mismatch_count = 0
    for row in parsed_daily_records:
        ts_code = str(row.get("ts_code") or "")
        trade_date = str(row.get("trade_date") or "")
        stock_row = stock_by_ts.get(ts_code)
        if stock_row is None:
            unmatched_daily_count += 1
            continue
        if str(stock_row.get("list_status") or "") != "L":
            non_active_daily_count += 1
            continue
        exchange = str(stock_row.get("exchange") or "")
        if exchange in latest_complete_by_exchange and trade_date != latest_complete_by_exchange[exchange]:
            latest_complete_mismatch_count += 1

    checks.append(
        build_quality_check(
            check_name="daily_join_to_active_stock_basic",
            check_type="blocking",
            sample_row_count=len(parsed_daily_records),
            failed_row_count=unmatched_daily_count + non_active_daily_count,
            reason_counts={
                **(
                    {"DAILY_TS_CODE_NOT_FOUND_IN_STOCK_BASIC": unmatched_daily_count}
                    if unmatched_daily_count
                    else {}
                ),
                **(
                    {"DAILY_MATCHED_STOCK_BASIC_NOT_ACTIVE_L": non_active_daily_count}
                    if non_active_daily_count
                    else {}
                ),
            },
        )
    )
    if unmatched_daily_count:
        blocking_reason_counts["DAILY_TS_CODE_NOT_FOUND_IN_STOCK_BASIC"] += unmatched_daily_count
    if non_active_daily_count:
        blocking_reason_counts["DAILY_MATCHED_STOCK_BASIC_NOT_ACTIVE_L"] += non_active_daily_count
    if unmatched_daily_count or non_active_daily_count:
        blocking_messages.append("daily rows exist that cannot join to active stock_basic")

    checks.append(
        build_quality_check(
            check_name="latest_complete_trade_date_alignment",
            check_type="blocking",
            sample_row_count=len(parsed_daily_records),
            failed_row_count=latest_complete_mismatch_count,
            reason_counts={"TRADE_DATE_NOT_LATEST_COMPLETE": latest_complete_mismatch_count} if latest_complete_mismatch_count else {},
        )
    )
    if latest_complete_mismatch_count:
        blocking_reason_counts["TRADE_DATE_NOT_LATEST_COMPLETE"] += latest_complete_mismatch_count
        blocking_messages.append("SSE/SZSE daily rows are not aligned to latest complete trade date")

    if blocking_messages:
        quality_report = build_quality_report(
            run_status="FAILED",
            checks=checks,
            sample_row_count=len(parsed_daily_records),
            passed_row_count=0,
            excluded_row_count=0,
            out_of_scope_exclusion_row_count=0,
            quality_exclusion_row_count=0,
            quality_failed_row_count=0,
            blocking_reason_counts=blocking_reason_counts,
            error="; ".join(blocking_messages),
        )
        raise ReplayValidationError("; ".join(blocking_messages), quality_report)

    normalized_rows: list[dict[str, Any]] = []
    exclusion_rows: list[dict[str, Any]] = []
    exclusion_keys: set[tuple[str, str, str, str]] = set()
    exclusion_reason_counts: Counter[str] = Counter()
    out_of_scope_reasons = {
        "BSE_EXCLUDED_BY_FORMAL_SCOPE",
        "EXCHANGE_OUT_OF_FORMAL_SCOPE",
    }

    def add_exclusion(row: dict[str, Any]) -> None:
        key = (
            row["manifest_key"],
            row["ts_code"],
            row["trade_date"],
            row["exclusion_reason"],
        )
        if key not in exclusion_keys:
            exclusion_keys.add(key)
            exclusion_rows.append(row)
            for reason in row["exclusion_reason"].split("|"):
                if reason:
                    exclusion_reason_counts[reason] += 1

    daily_trade_date = ""
    if parsed_daily_records:
        daily_trade_date = str(parsed_daily_records[0].get("trade_date") or "")

    for stock_row in stock_basic.records:
        exchange = str(stock_row.get("exchange") or "")
        list_status = str(stock_row.get("list_status") or "")
        if exchange == "BSE" and list_status == "L":
            add_exclusion(
                build_exclusion_row(
                    manifest_key="stock_basic_active",
                    ts_code=str(stock_row.get("ts_code") or ""),
                    trade_date=daily_trade_date,
                    capture_time_utc=stock_basic.entry.capture_time_utc,
                    source_response_sha256=stock_basic.response_sha256,
                    snapshot_file_sha256=stock_basic.file_sha256,
                    scope=EXCLUDED_BSE_SCOPE,
                    freshness_status="OUT_OF_SCOPE",
                    exclusion_reason="BSE_EXCLUDED_BY_FORMAL_SCOPE",
                    exchange=exchange,
                    list_status=list_status,
                    market=str(stock_row.get("market") or ""),
                )
            )

    ohlc_failures = Counter()
    negative_value_failures = Counter()
    pct_failures = Counter()
    change_failures = Counter()
    adj_factor_failures = Counter()

    scope_candidate_count = 0
    for daily_row in parsed_daily_records:
        ts_code = str(daily_row.get("ts_code") or "")
        trade_date = str(daily_row.get("trade_date") or "")
        stock_row = stock_by_ts[ts_code]
        exchange = str(stock_row.get("exchange") or "")
        list_status = str(stock_row.get("list_status") or "")
        market = str(stock_row.get("market") or "")

        if list_status != "L":
            raise ReplayValidationError(
                "Non-L stock_basic row reached success path after active join gate: "
                f"{ts_code}|{trade_date}|{list_status}"
            )

        if exchange not in latest_complete_by_exchange:
            add_exclusion(
                build_exclusion_row(
                    manifest_key="daily_all_market",
                    ts_code=ts_code,
                    trade_date=trade_date,
                    capture_time_utc=daily.entry.capture_time_utc,
                    source_response_sha256=daily.response_sha256,
                    snapshot_file_sha256=daily.file_sha256,
                    scope=EXCLUDED_BSE_SCOPE,
                    freshness_status="OUT_OF_SCOPE",
                    exclusion_reason="EXCHANGE_OUT_OF_FORMAL_SCOPE",
                    exchange=exchange,
                    list_status=list_status,
                    market=market,
                )
            )
            continue

        scope_candidate_count += 1
        freshness_status = "LATEST_COMPLETE_TRADE_DATE_MATCH"
        adj_row = adj_factor_by_key.get((ts_code, trade_date))

        row_reasons: list[str] = []
        if adj_row is None:
            row_reasons.append("ADJ_FACTOR_MISSING_FOR_DAILY_ROW")
        else:
            adj_factor_value = float(adj_row["adj_factor"])
            if adj_factor_value <= 0:
                row_reasons.append("ADJ_FACTOR_NOT_POSITIVE")
                adj_factor_failures["ADJ_FACTOR_NOT_POSITIVE"] += 1

        open_price = float(daily_row["open"])
        high_price = float(daily_row["high"])
        low_price = float(daily_row["low"])
        close_price = float(daily_row["close"])
        pre_close_price = float(daily_row["pre_close"])
        change_value = float(daily_row["change"])
        pct_chg_value = float(daily_row["pct_chg"])
        vol_value = float(daily_row["vol"])
        amount_value = float(daily_row["amount"])

        if high_price < max(open_price, close_price, low_price):
            row_reasons.append("OHLC_HIGH_RELATION_INVALID")
            ohlc_failures["OHLC_HIGH_RELATION_INVALID"] += 1
        if low_price > min(open_price, close_price, high_price):
            row_reasons.append("OHLC_LOW_RELATION_INVALID")
            ohlc_failures["OHLC_LOW_RELATION_INVALID"] += 1
        if vol_value < 0:
            row_reasons.append("VOL_NEGATIVE")
            negative_value_failures["VOL_NEGATIVE"] += 1
        if amount_value < 0:
            row_reasons.append("AMOUNT_NEGATIVE")
            negative_value_failures["AMOUNT_NEGATIVE"] += 1

        if abs((close_price - pre_close_price) - change_value) > CHANGE_ABS_TOLERANCE:
            row_reasons.append("CHANGE_MISMATCH_EXCEEDS_TOLERANCE")
            change_failures["CHANGE_MISMATCH_EXCEEDS_TOLERANCE"] += 1

        if pre_close_price == 0:
            row_reasons.append("PRE_CLOSE_ZERO_FOR_PCT_CHG")
            pct_failures["PRE_CLOSE_ZERO_FOR_PCT_CHG"] += 1
        else:
            recomputed_pct_chg = change_value / pre_close_price * 100
            if abs(recomputed_pct_chg - pct_chg_value) > PCT_CHG_ABS_TOLERANCE:
                row_reasons.append("PCT_CHG_MISMATCH_EXCEEDS_TOLERANCE")
                pct_failures["PCT_CHG_MISMATCH_EXCEEDS_TOLERANCE"] += 1

        if row_reasons:
            add_exclusion(
                build_exclusion_row(
                    manifest_key="daily_all_market",
                    ts_code=ts_code,
                    trade_date=trade_date,
                    capture_time_utc=daily.entry.capture_time_utc,
                    source_response_sha256=daily.response_sha256,
                    snapshot_file_sha256=daily.file_sha256,
                    scope=FORMAL_SCOPE,
                    freshness_status=freshness_status,
                    exclusion_reason="|".join(row_reasons),
                    exchange=exchange,
                    list_status=list_status,
                    market=market,
                )
            )
            continue

        normalized_rows.append(
            {
                "source_id": EXPECTED_SOURCE_ID,
                "ts_code": ts_code,
                "trade_date": trade_date,
                "capture_time_utc": daily.entry.capture_time_utc,
                "source_response_sha256": daily.response_sha256,
                "snapshot_file_sha256": daily.file_sha256,
                "scope": FORMAL_SCOPE,
                "freshness_status": freshness_status,
                "replay_status": REPLAY_VALIDATED,
                "exclusion_reason": "",
                "exchange": exchange,
                "list_status": list_status,
                "market": market,
                "open": daily_row["open"],
                "high": daily_row["high"],
                "low": daily_row["low"],
                "close": daily_row["close"],
                "pre_close": daily_row["pre_close"],
                "change": daily_row["change"],
                "pct_chg": daily_row["pct_chg"],
                "vol": daily_row["vol"],
                "amount": daily_row["amount"],
                "adj_factor": float(adj_row["adj_factor"]),
                "stock_basic_source_response_sha256": stock_basic.response_sha256,
                "stock_basic_snapshot_file_sha256": stock_basic.file_sha256,
                "adj_factor_source_response_sha256": adj_factor.response_sha256,
                "adj_factor_snapshot_file_sha256": adj_factor.file_sha256,
                "calendar_source_response_sha256": (
                    trade_cal_sse.response_sha256 if exchange == "SSE" else trade_cal_szse.response_sha256
                ),
                "calendar_snapshot_file_sha256": (
                    trade_cal_sse.file_sha256 if exchange == "SSE" else trade_cal_szse.file_sha256
                ),
            }
        )

    ensure_output_columns_are_raw_only(normalized_rows)

    checks.extend(
        [
            build_quality_check(
                check_name="ohlc_relationship",
                check_type="row_quality",
                sample_row_count=scope_candidate_count,
                failed_row_count=sum(ohlc_failures.values()),
                reason_counts=ohlc_failures,
            ),
            build_quality_check(
                check_name="non_negative_volume_and_amount",
                check_type="row_quality",
                sample_row_count=scope_candidate_count,
                failed_row_count=sum(negative_value_failures.values()),
                reason_counts=negative_value_failures,
            ),
            build_quality_check(
                check_name="pct_chg_recompute",
                check_type="row_quality",
                sample_row_count=scope_candidate_count,
                failed_row_count=sum(pct_failures.values()),
                reason_counts=pct_failures,
                tolerance={"pct_chg_abs_tolerance": PCT_CHG_ABS_TOLERANCE},
                formula_version=FORMULA_VERSION["pct_chg"],
            ),
            build_quality_check(
                check_name="change_recompute",
                check_type="row_quality",
                sample_row_count=scope_candidate_count,
                failed_row_count=sum(change_failures.values()),
                reason_counts=change_failures,
                tolerance={"change_abs_tolerance": CHANGE_ABS_TOLERANCE},
                formula_version=FORMULA_VERSION["change"],
            ),
            build_quality_check(
                check_name="adj_factor_positive",
                check_type="row_quality",
                sample_row_count=scope_candidate_count,
                failed_row_count=sum(adj_factor_failures.values())
                + exclusion_reason_counts.get("ADJ_FACTOR_MISSING_FOR_DAILY_ROW", 0),
                reason_counts={
                    **dict(adj_factor_failures),
                    **(
                        {"ADJ_FACTOR_MISSING_FOR_DAILY_ROW": exclusion_reason_counts["ADJ_FACTOR_MISSING_FOR_DAILY_ROW"]}
                        if exclusion_reason_counts.get("ADJ_FACTOR_MISSING_FOR_DAILY_ROW", 0)
                        else {}
                    ),
                },
            ),
        ]
    )

    out_of_scope_exclusion_row_count = sum(
        1
        for row in exclusion_rows
        if all(reason in out_of_scope_reasons for reason in row["exclusion_reason"].split("|") if reason)
    )
    quality_exclusion_row_count = len(exclusion_rows) - out_of_scope_exclusion_row_count
    quality_failed_row_count = quality_exclusion_row_count

    quality_report = build_quality_report(
        run_status="SUCCESS",
        checks=checks,
        sample_row_count=scope_candidate_count,
        passed_row_count=len(normalized_rows),
        excluded_row_count=len(exclusion_rows),
        out_of_scope_exclusion_row_count=out_of_scope_exclusion_row_count,
        quality_exclusion_row_count=quality_exclusion_row_count,
        quality_failed_row_count=quality_failed_row_count,
        exclusion_reason_counts=exclusion_reason_counts,
        blocking_reason_counts=blocking_reason_counts,
    )

    summary = {
        "status": "SUCCESS",
        "generated_at_utc": utc_now_iso(),
        "source_id": EXPECTED_SOURCE_ID,
        "formal_scope": FORMAL_SCOPE,
        "validated_snapshot_count": len(loaded),
        "normalized_output_row_count": len(normalized_rows),
        "exclusion_row_count": len(exclusion_rows),
        "out_of_scope_exclusion_row_count": out_of_scope_exclusion_row_count,
        "quality_exclusion_row_count": quality_exclusion_row_count,
        "quality_failed_row_count": quality_failed_row_count,
        "latest_complete_trade_date_by_exchange": latest_complete_by_exchange,
        "bse_exclusion_count": exclusion_reason_counts.get("BSE_EXCLUDED_BY_FORMAL_SCOPE", 0),
        "unmatched_daily_count": exclusion_reason_counts.get("DAILY_TS_CODE_NOT_FOUND_IN_STOCK_BASIC", 0),
        "duplicate_failure_count": sum(
            blocking_reason_counts.get(key, 0)
            for key in (
                "STOCK_BASIC_TS_CODE_DUPLICATE",
                "DAILY_PRIMARY_KEY_DUPLICATE",
                "ADJ_FACTOR_PRIMARY_KEY_DUPLICATE",
            )
        ),
        "quality_report_file": "data_quality_report.json",
    }

    report_markdown = build_quality_report_markdown(summary, quality_report, loaded)
    return ReplayResult(
        normalized_rows=normalized_rows,
        exclusion_rows=exclusion_rows,
        quality_report=quality_report,
        summary=summary,
        report_markdown=report_markdown,
    )


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read an external Tushare daily replay manifest and produce a contract-driven, read-only normalized output."
    )
    parser.add_argument(
        "--manifest",
        required=True,
        help="Path to the external replay manifest JSON file.",
    )
    parser.add_argument(
        "--snapshot-root",
        required=True,
        help="Directory containing the external snapshot files referenced by the manifest.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory used for replay outputs. This directory is created if needed.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest).resolve()
    snapshot_root = Path(args.snapshot_root).resolve()
    output_dir = Path(args.output_dir).resolve()

    try:
        result = consume_snapshots(manifest_path=manifest_path, snapshot_root=snapshot_root)
    except ReplayValidationError as exc:
        write_failure_outputs(output_dir, str(exc), exc.quality_report)
        return 1

    write_success_outputs(output_dir, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
