from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo
import re


OFFICIAL_API_URL = "https://api.tushare.pro"
REPO_ROOT = Path(r"D:\Stock\dealer_assistant").resolve()
EXPECTED_SOURCE_ID = "TUSHARE_A_SHARE_DAILY_SSE_SZSE_V1"
SUCCESS_STATUS = "SUCCESS"
INCOMPLETE_STATUS = "INCOMPLETE"
WAITING_STATUS = "WAITING_FOR_POST_CLOSE_AVAILABILITY"
RAW_PAGE_ROLE = "RAW_PAGE_RESPONSE"
DERIVED_AGGREGATE_ROLE = "DERIVED_PAGE_AGGREGATE"
DERIVED_AGGREGATE_ORIGIN = "DERIVED_PAGE_AGGREGATE_NOT_VENDOR_RAW"
TOKEN_MISSING_REASON = "TOKEN_ENV_VAR_MISSING"
EMPTY_RESPONSE_REASON = "EMPTY_RESPONSE"
PERMISSION_REASON = "PERMISSION_DENIED"
RATE_LIMIT_REASON = "RATE_LIMITED"
TRANSIENT_REASON = "TRANSIENT_ERROR"
REDIRECT_REASON = "HTTP_REDIRECT_BLOCKED"

CONSUMER_SPEC = spec_from_file_location(
    "tushare_daily_replay_consumer",
    Path(__file__).resolve().parents[1]
    / "batch_16_tushare_daily_replay_tools"
    / "tushare_daily_replay_consumer.py",
)
CONSUMER_MODULE = module_from_spec(CONSUMER_SPEC)
assert CONSUMER_SPEC and CONSUMER_SPEC.loader
sys.modules[CONSUMER_SPEC.name] = CONSUMER_MODULE
CONSUMER_SPEC.loader.exec_module(CONSUMER_MODULE)


class CollectorError(Exception):
    pass


class PermissionDeniedError(CollectorError):
    pass


class RateLimitError(CollectorError):
    pass


class TransportTransientError(CollectorError):
    pass


class RedirectBlockedError(CollectorError):
    pass


@dataclass(frozen=True)
class CollectorConfig:
    snapshot_root: Path
    output_dir: Path
    token_env_var: str
    run_id: str
    timezone_name: str
    post_close_cutoff_local: str
    reference_time_utc: str
    page_limit: int
    max_retries: int
    api_url: str = OFFICIAL_API_URL


@dataclass(frozen=True)
class ApiSpec:
    manifest_key: str
    api_name: str
    fields: list[str]


@dataclass(frozen=True)
class PageFetchResult:
    response_text: str
    response_json: dict[str, Any]
    capture_time_utc: str


@dataclass
class SnapshotManifestEntry:
    manifest_key: str
    api_name: str
    snapshot_path: str
    capture_time_utc: str
    source_response_sha256: str
    snapshot_file_sha256: str
    row_count: int
    field_list: list[str]
    scope: str
    status: str = "ready"
    snapshot_role: str = DERIVED_AGGREGATE_ROLE
    source_response_origin: str = DERIVED_AGGREGATE_ORIGIN
    page_response_chain: list[dict[str, Any]] = field(default_factory=list)


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RedirectBlockedError(f"Redirect blocked: {code} -> {newurl}")


class TushareTransport:
    def fetch_page(
        self,
        *,
        api_name: str,
        params: dict[str, Any],
        fields: list[str],
        offset: int,
        limit: int,
        token: str,
        api_url: str,
    ) -> PageFetchResult:
        validate_official_api_url(api_url)
        payload = {
            "api_name": api_name,
            "token": token,
            "params": {**params, "limit": str(limit), "offset": str(offset)},
            "fields": ",".join(fields),
        }
        request = urllib.request.Request(
            api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        opener = urllib.request.build_opener(NoRedirectHandler)
        capture_time_utc = utc_now_iso()
        try:
            with opener.open(request, timeout=30) as response:
                text = response.read().decode("utf-8")
                return PageFetchResult(
                    response_text=text,
                    response_json=json.loads(text),
                    capture_time_utc=capture_time_utc,
                )
        except RedirectBlockedError:
            raise
        except urllib.error.HTTPError as exc:
            if 300 <= exc.code < 400:
                raise RedirectBlockedError(f"Redirect blocked: {exc.code}") from exc
            if exc.code in (401, 403):
                raise PermissionDeniedError(f"{api_name} permission denied") from exc
            if exc.code == 429:
                raise RateLimitError(f"{api_name} rate limited") from exc
            raise TransportTransientError(f"{api_name} transient http error {exc.code}") from exc
        except urllib.error.URLError as exc:
            raise TransportTransientError(f"{api_name} transient network error") from exc


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_text(text: str) -> str:
    return CONSUMER_MODULE.sha256_text(text)


def sha256_file(path: Path) -> str:
    return CONSUMER_MODULE.sha256_file(path)


def validate_official_api_url(api_url: str) -> None:
    parsed = urllib.parse.urlsplit(api_url)
    if parsed.scheme != "https" or parsed.netloc != "api.tushare.pro" or parsed.path not in ("", "/"):
        raise CollectorError(f"Only the official HTTPS Tushare origin is allowed: {OFFICIAL_API_URL}")
    if api_url.rstrip("/") != OFFICIAL_API_URL:
        raise CollectorError(f"Only the official HTTPS Tushare origin is allowed: {OFFICIAL_API_URL}")


def ensure_external_dir(path: Path) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(REPO_ROOT)
    except ValueError:
        return resolved
    raise CollectorError(f"Path must stay outside dealer_assistant: {resolved}")


SAFE_RUN_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def validate_run_id(run_id: str) -> str:
    normalized = str(run_id).strip()
    if not normalized:
        raise CollectorError("run_id must be a non-empty single-segment identifier.")
    if normalized in {".", ".."}:
        raise CollectorError("run_id must not be '.' or '..'.")
    if not SAFE_RUN_ID_PATTERN.fullmatch(normalized):
        raise CollectorError(
            "run_id must be a single safe path segment containing only letters, digits, '.', '_' or '-'."
        )
    if any(marker in normalized for marker in ("/", "\\", ":")):
        raise CollectorError("run_id must not contain path separators or drive markers.")
    if Path(normalized).is_absolute():
        raise CollectorError("run_id must not be an absolute path.")
    return normalized


def ensure_external_run_dir(root: Path, run_id: str) -> Path:
    root_resolved = ensure_external_dir(root)
    run_dir = (root_resolved / run_id).resolve()
    try:
        run_dir.relative_to(root_resolved)
    except ValueError as exc:
        raise CollectorError(f"run_id escapes validated root: {run_id}") from exc
    return run_dir


def write_json_immutable(path: Path, payload: dict[str, Any]) -> bool:
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing_text = path.read_text(encoding="utf-8")
        if existing_text != serialized:
            raise CollectorError(f"Immutable output already exists with different content: {path}")
        return False
    with path.open("x", encoding="utf-8", newline="") as handle:
        handle.write(serialized)
    return True


def write_text_immutable(path: Path, text: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing_text = path.read_text(encoding="utf-8")
        if existing_text != text:
            raise CollectorError(f"Immutable output already exists with different content: {path}")
        return False
    with path.open("x", encoding="utf-8", newline="") as handle:
        handle.write(text)
    return True


def get_env_token(token_env_var: str) -> str:
    token = os.environ.get(token_env_var, "")
    if not token:
        raise CollectorError(f"Missing token environment variable: {token_env_var}")
    return token


def parse_cutoff_time(raw_value: str) -> tuple[int, int]:
    hour_text, minute_text = raw_value.split(":", maxsplit=1)
    return int(hour_text), int(minute_text)


def parse_reference_time(reference_time_utc: str) -> datetime:
    normalized = reference_time_utc.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized).astimezone(UTC)


def get_api_specs() -> dict[str, ApiSpec]:
    return {
        "trade_cal_sse": ApiSpec(
            manifest_key="trade_cal_sse",
            api_name="trade_cal",
            fields=["exchange", "cal_date", "is_open", "pretrade_date"],
        ),
        "trade_cal_szse": ApiSpec(
            manifest_key="trade_cal_szse",
            api_name="trade_cal",
            fields=["exchange", "cal_date", "is_open", "pretrade_date"],
        ),
        "stock_basic_active": ApiSpec(
            manifest_key="stock_basic_active",
            api_name="stock_basic",
            fields=[
                "ts_code",
                "symbol",
                "market",
                "exchange",
                "list_status",
                "list_date",
                "delist_date",
            ],
        ),
        "daily_all_market": ApiSpec(
            manifest_key="daily_all_market",
            api_name="daily",
            fields=[
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
        ),
        "adj_factor_all_market": ApiSpec(
            manifest_key="adj_factor_all_market",
            api_name="adj_factor",
            fields=["ts_code", "trade_date", "adj_factor"],
        ),
    }


def aggregate_page_payload(fields: list[str], items: list[list[Any]]) -> dict[str, Any]:
    return {
        "code": 0,
        "message": "",
        "data": {
            "fields": fields,
            "items": items,
            "has_more": False,
            "count": len(items),
        },
        "request_id": "derived-page-aggregate",
        "chart": None,
    }


def build_raw_page_snapshot(
    *,
    spec: ApiSpec,
    page_index: int,
    page_result: PageFetchResult,
    params: dict[str, Any],
    offset: int,
    limit: int,
) -> tuple[dict[str, Any], str]:
    data_block = page_result.response_json.get("data") or {}
    page_fields = list(data_block.get("fields") or [])
    page_items = list(data_block.get("items") or [])
    page_payload = {
        "snapshot_id": f"{spec.manifest_key}__page_{page_index:04d}",
        "snapshot_role": RAW_PAGE_ROLE,
        "api_name": spec.api_name,
        "capture_time_utc": page_result.capture_time_utc,
        "source_id": EXPECTED_SOURCE_ID,
        "request_params_redacted": {**params, "limit": str(limit), "offset": str(offset)},
        "source_response_text": page_result.response_text,
        "source_response_sha256": sha256_text(page_result.response_text),
        "snapshot_file_sha256": "AUTHORITATIVE_FILE_SHA256_IS_RECORDED_IN_PAGE_CHAIN",
        "snapshot_file_sha256_basis": "page_chain_actual_file_sha256",
        "row_count": len(page_items),
        "field_list": page_fields,
        "fields": page_fields,
        "source_response_json": page_result.response_json,
    }
    return page_payload, json.dumps(page_payload, ensure_ascii=False, indent=2) + "\n"


def collect_paginated(
    *,
    spec: ApiSpec,
    params: dict[str, Any],
    scope: str,
    config: CollectorConfig,
    transport: TushareTransport,
    token: str,
    collection_report: dict[str, Any],
) -> tuple[str | None, SnapshotManifestEntry | None]:
    all_items: list[list[Any]] = []
    response_fields: list[str] = []
    page_index = 0
    retry_counter = 0
    offset = 0
    reason_counts: Counter[str] = Counter()
    page_chain: list[dict[str, Any]] = []

    while True:
        page_index += 1
        for attempt in range(config.max_retries + 1):
            try:
                page_result = transport.fetch_page(
                    api_name=spec.api_name,
                    params=params,
                    fields=spec.fields,
                    offset=offset,
                    limit=config.page_limit,
                    token=token,
                    api_url=config.api_url,
                )
                break
            except RedirectBlockedError:
                reason_counts[REDIRECT_REASON] += 1
                collection_report["api_results"][spec.manifest_key] = {
                    "status": INCOMPLETE_STATUS,
                    "api_name": spec.api_name,
                    "scope": scope,
                    "page_count": page_index,
                    "row_count": len(all_items),
                    "retry_count": retry_counter,
                    "reason_counts": dict(reason_counts),
                }
                return REDIRECT_REASON, None
            except PermissionDeniedError:
                reason_counts[PERMISSION_REASON] += 1
                collection_report["api_results"][spec.manifest_key] = {
                    "status": INCOMPLETE_STATUS,
                    "api_name": spec.api_name,
                    "scope": scope,
                    "page_count": page_index,
                    "row_count": len(all_items),
                    "retry_count": retry_counter,
                    "reason_counts": dict(reason_counts),
                }
                return PERMISSION_REASON, None
            except RateLimitError:
                retry_counter += 1
                reason_counts[RATE_LIMIT_REASON] += 1
                if attempt >= config.max_retries:
                    collection_report["api_results"][spec.manifest_key] = {
                        "status": INCOMPLETE_STATUS,
                        "api_name": spec.api_name,
                        "scope": scope,
                        "page_count": page_index,
                        "row_count": len(all_items),
                        "retry_count": retry_counter,
                        "reason_counts": dict(reason_counts),
                    }
                    return RATE_LIMIT_REASON, None
                time.sleep(0)
            except TransportTransientError:
                retry_counter += 1
                reason_counts[TRANSIENT_REASON] += 1
                if attempt >= config.max_retries:
                    collection_report["api_results"][spec.manifest_key] = {
                        "status": INCOMPLETE_STATUS,
                        "api_name": spec.api_name,
                        "scope": scope,
                        "page_count": page_index,
                        "row_count": len(all_items),
                        "retry_count": retry_counter,
                        "reason_counts": dict(reason_counts),
                    }
                    return TRANSIENT_REASON, None
                time.sleep(0)
        else:
            collection_report["api_results"][spec.manifest_key] = {
                "status": INCOMPLETE_STATUS,
                "api_name": spec.api_name,
                "scope": scope,
                "page_count": page_index,
                "row_count": len(all_items),
                "retry_count": retry_counter,
                "reason_counts": dict(reason_counts),
            }
            return TRANSIENT_REASON, None

        data_block = page_result.response_json.get("data") or {}
        page_fields = list(data_block.get("fields") or [])
        page_items = list(data_block.get("items") or [])

        raw_page_payload, raw_page_text = build_raw_page_snapshot(
            spec=spec,
            page_index=page_index,
            page_result=page_result,
            params=params,
            offset=offset,
            limit=config.page_limit,
        )
        raw_page_path = (
            ensure_external_run_dir(config.snapshot_root, config.run_id)
            / "raw_pages"
            / spec.manifest_key
            / f"page_{page_index:04d}.json"
        )
        write_text_immutable(raw_page_path, raw_page_text)
        raw_page_file_sha256 = sha256_file(raw_page_path)
        page_chain.append(
            {
                "page_index": page_index,
                "raw_page_path": str(
                    Path(config.run_id)
                    / "raw_pages"
                    / spec.manifest_key
                    / f"page_{page_index:04d}.json"
                ).replace("\\", "/"),
                "capture_time_utc": raw_page_payload["capture_time_utc"],
                "source_response_sha256": raw_page_payload["source_response_sha256"],
                "snapshot_file_sha256": raw_page_file_sha256,
                "row_count": raw_page_payload["row_count"],
                "field_list": raw_page_payload["field_list"],
            }
        )

        if not page_items:
            reason_counts[EMPTY_RESPONSE_REASON] += 1
            collection_report["api_results"][spec.manifest_key] = {
                "status": INCOMPLETE_STATUS,
                "api_name": spec.api_name,
                "scope": scope,
                "page_count": page_index,
                "row_count": len(all_items),
                "retry_count": retry_counter,
                "reason_counts": dict(reason_counts),
                "page_response_chain": page_chain,
            }
            return EMPTY_RESPONSE_REASON, None

        if not response_fields:
            response_fields = page_fields
        elif response_fields != page_fields:
            reason_counts["FIELD_LIST_CHANGED_BETWEEN_PAGES"] += 1
            collection_report["api_results"][spec.manifest_key] = {
                "status": INCOMPLETE_STATUS,
                "api_name": spec.api_name,
                "scope": scope,
                "page_count": page_index,
                "row_count": len(all_items),
                "retry_count": retry_counter,
                "reason_counts": dict(reason_counts),
                "page_response_chain": page_chain,
            }
            return "FIELD_LIST_CHANGED_BETWEEN_PAGES", None

        all_items.extend(page_items)
        if not bool(data_block.get("has_more")):
            break
        offset += config.page_limit

    aggregate_capture_time_utc = utc_now_iso()
    aggregate_payload = aggregate_page_payload(response_fields, all_items)
    derived_snapshot_payload = {
        "snapshot_id": spec.manifest_key,
        "snapshot_role": DERIVED_AGGREGATE_ROLE,
        "source_response_origin": DERIVED_AGGREGATE_ORIGIN,
        "api_name": spec.api_name,
        "capture_time_utc": aggregate_capture_time_utc,
        "source_id": EXPECTED_SOURCE_ID,
        "reference_time_utc": config.reference_time_utc,
        "request_params_redacted": params,
        "source_response_text": json.dumps(
            aggregate_payload,
            ensure_ascii=False,
            separators=(",", ":"),
        ),
        "source_response_sha256": "",
        "snapshot_file_sha256": "AUTHORITATIVE_FILE_SHA256_IS_IN_MANIFEST",
        "snapshot_file_sha256_basis": "manifest_actual_file_sha256",
        "row_count": len(all_items),
        "field_list": response_fields,
        "fields": response_fields,
        "source_response_json": aggregate_payload,
        "derived_from_page_responses": page_chain,
    }
    derived_snapshot_payload["source_response_sha256"] = sha256_text(
        derived_snapshot_payload["source_response_text"]
    )

    aggregate_path = ensure_external_run_dir(config.snapshot_root, config.run_id) / f"{spec.manifest_key}.json"
    write_json_immutable(aggregate_path, derived_snapshot_payload)
    aggregate_file_sha256 = sha256_file(aggregate_path)
    entry = SnapshotManifestEntry(
        manifest_key=spec.manifest_key,
        api_name=spec.api_name,
        snapshot_path=str(Path(config.run_id) / f"{spec.manifest_key}.json").replace("\\", "/"),
        capture_time_utc=aggregate_capture_time_utc,
        source_response_sha256=derived_snapshot_payload["source_response_sha256"],
        snapshot_file_sha256=aggregate_file_sha256,
        row_count=len(all_items),
        field_list=response_fields,
        scope=scope,
        page_response_chain=page_chain,
    )
    collection_report["api_results"][spec.manifest_key] = {
        "status": SUCCESS_STATUS,
        "api_name": spec.api_name,
        "scope": scope,
        "page_count": page_index,
        "row_count": len(all_items),
        "retry_count": retry_counter,
        "reason_counts": dict(reason_counts),
        "snapshot_path": entry.snapshot_path,
        "snapshot_role": DERIVED_AGGREGATE_ROLE,
        "page_response_chain": page_chain,
    }
    return None, entry


def derive_latest_complete_from_trade_cal(
    records: list[dict[str, Any]], capture_time_utc: str
) -> str | None:
    return CONSUMER_MODULE.derive_latest_complete_trade_date(records, capture_time_utc)


def parse_records_from_manifest_entry(
    entry: SnapshotManifestEntry, snapshot_root: Path
) -> list[dict[str, Any]]:
    snapshot = json.loads((snapshot_root / entry.snapshot_path).read_text(encoding="utf-8"))
    data_block = snapshot["source_response_json"]["data"]
    fields = list(data_block.get("fields") or [])
    items = list(data_block.get("items") or [])
    return [dict(zip(fields, row)) for row in items]


def should_wait_for_post_close(
    *,
    trade_cal_sse: SnapshotManifestEntry,
    trade_cal_szse: SnapshotManifestEntry,
    snapshot_root: Path,
    timezone_name: str,
    post_close_cutoff_local: str,
    reference_time_utc: str,
) -> bool:
    zone = ZoneInfo(timezone_name)
    reference_dt_utc = parse_reference_time(reference_time_utc)
    reference_local = reference_dt_utc.astimezone(zone)
    cutoff_hour, cutoff_minute = parse_cutoff_time(post_close_cutoff_local)
    if (reference_local.hour, reference_local.minute) >= (cutoff_hour, cutoff_minute):
        return False

    reference_date = reference_local.strftime("%Y%m%d")
    for entry in (trade_cal_sse, trade_cal_szse):
        for row in parse_records_from_manifest_entry(entry, snapshot_root):
            if str(row.get("cal_date")) == reference_date and str(row.get("is_open")) == "1":
                return True
    return False


def build_manifest(
    *,
    config: CollectorConfig,
    run_status: str,
    entries: list[SnapshotManifestEntry],
    latest_complete_trade_date: str | None,
) -> dict[str, Any]:
    safe_run_id = validate_run_id(config.run_id)
    return {
        "manifest_name": f"tushare_daily_collection_manifest__{safe_run_id}",
        "source_id": EXPECTED_SOURCE_ID,
        "run_id": safe_run_id,
        "run_status": run_status,
        "generated_at_utc": utc_now_iso(),
        "config": {
            "token_env_var": config.token_env_var,
            "timezone_name": config.timezone_name,
            "post_close_cutoff_local": config.post_close_cutoff_local,
            "reference_time_utc": config.reference_time_utc,
            "page_limit": config.page_limit,
            "max_retries": config.max_retries,
            "api_origin": OFFICIAL_API_URL,
        },
        "latest_complete_trade_date": latest_complete_trade_date or "",
        "entries": [
            {
                "manifest_key": entry.manifest_key,
                "source_id": EXPECTED_SOURCE_ID,
                "snapshot_path": entry.snapshot_path,
                "api_name": entry.api_name,
                "capture_time_utc": entry.capture_time_utc,
                "source_response_sha256": entry.source_response_sha256,
                "snapshot_file_sha256": entry.snapshot_file_sha256,
                "row_count": entry.row_count,
                "field_list": entry.field_list,
                "scope": entry.scope,
                "status": entry.status,
                "snapshot_role": entry.snapshot_role,
                "source_response_origin": entry.source_response_origin,
            }
            for entry in entries
        ],
    }


def collect_run(
    config: CollectorConfig,
    transport: TushareTransport | None = None,
) -> dict[str, Any]:
    validate_official_api_url(config.api_url)
    safe_run_id = validate_run_id(config.run_id)
    snapshot_root = ensure_external_dir(config.snapshot_root)
    output_dir = ensure_external_dir(config.output_dir)
    snapshot_run_dir = ensure_external_run_dir(snapshot_root, safe_run_id)
    output_run_dir = ensure_external_run_dir(output_dir, safe_run_id)
    transport = transport or TushareTransport()
    specs = get_api_specs()
    collection_report: dict[str, Any] = {
        "run_id": config.run_id,
        "source_id": EXPECTED_SOURCE_ID,
        "run_status": INCOMPLETE_STATUS,
        "generated_at_utc": utc_now_iso(),
        "token_env_var": config.token_env_var,
        "timezone_name": config.timezone_name,
        "post_close_cutoff_local": config.post_close_cutoff_local,
        "reference_time_utc": config.reference_time_utc,
        "page_limit": config.page_limit,
        "max_retries": config.max_retries,
        "api_origin": OFFICIAL_API_URL,
        "snapshot_root_run_dir": str(snapshot_run_dir),
        "output_run_dir": str(output_run_dir),
        "api_results": {},
        "reason_counts": {},
        "latest_complete_trade_date_by_exchange": {},
    }
    entries: list[SnapshotManifestEntry] = []
    reason_counts: Counter[str] = Counter()

    try:
        token = get_env_token(config.token_env_var)
    except CollectorError:
        reason_counts[TOKEN_MISSING_REASON] += 1
        collection_report["reason_counts"] = dict(reason_counts)
        manifest = build_manifest(
            config=config,
            run_status=INCOMPLETE_STATUS,
            entries=[],
            latest_complete_trade_date=None,
        )
        collection_report["run_status"] = INCOMPLETE_STATUS
        return {"manifest": manifest, "collection_report": collection_report, "run_status": INCOMPLETE_STATUS}

    reference_dt = parse_reference_time(config.reference_time_utc).astimezone(
        ZoneInfo(config.timezone_name)
    )
    window_start = (reference_dt.date() - timedelta(days=5)).strftime("%Y%m%d")
    window_end = (reference_dt.date() + timedelta(days=1)).strftime("%Y%m%d")

    collect_order = [
        ("trade_cal_sse", {"exchange": "SSE", "start_date": window_start, "end_date": window_end}, "SSE_CALENDAR"),
        ("trade_cal_szse", {"exchange": "SZSE", "start_date": window_start, "end_date": window_end}, "SZSE_CALENDAR"),
    ]
    for spec_key, params, scope in collect_order:
        error_reason, entry = collect_paginated(
            spec=specs[spec_key],
            params=params,
            scope=scope,
            config=CollectorConfig(
                snapshot_root=snapshot_root,
                output_dir=output_dir,
                token_env_var=config.token_env_var,
                run_id=safe_run_id,
                timezone_name=config.timezone_name,
                post_close_cutoff_local=config.post_close_cutoff_local,
                reference_time_utc=config.reference_time_utc,
                page_limit=config.page_limit,
                max_retries=config.max_retries,
                api_url=config.api_url,
            ),
            transport=transport,
            token=token,
            collection_report=collection_report,
        )
        if error_reason:
            reason_counts[error_reason] += 1
        if entry:
            entries.append(entry)

    trade_cal_entries = {entry.manifest_key: entry for entry in entries}
    latest_complete_trade_date = None
    if "trade_cal_sse" in trade_cal_entries and "trade_cal_szse" in trade_cal_entries:
        sse_records = parse_records_from_manifest_entry(trade_cal_entries["trade_cal_sse"], snapshot_root)
        szse_records = parse_records_from_manifest_entry(trade_cal_entries["trade_cal_szse"], snapshot_root)
        latest_complete_sse = derive_latest_complete_from_trade_cal(
            sse_records, trade_cal_entries["trade_cal_sse"].capture_time_utc
        )
        latest_complete_szse = derive_latest_complete_from_trade_cal(
            szse_records, trade_cal_entries["trade_cal_szse"].capture_time_utc
        )
        collection_report["latest_complete_trade_date_by_exchange"] = {
            "SSE": latest_complete_sse or "",
            "SZSE": latest_complete_szse or "",
        }
        if latest_complete_sse and latest_complete_szse and latest_complete_sse == latest_complete_szse:
            latest_complete_trade_date = latest_complete_sse

    if not latest_complete_trade_date:
        reason_counts["LATEST_COMPLETE_TRADE_DATE_UNAVAILABLE"] += 1
        manifest = build_manifest(
            config=config,
            run_status=INCOMPLETE_STATUS,
            entries=entries,
            latest_complete_trade_date=None,
        )
        collection_report["run_status"] = INCOMPLETE_STATUS
        collection_report["reason_counts"] = dict(reason_counts)
        return {"manifest": manifest, "collection_report": collection_report, "run_status": INCOMPLETE_STATUS}

    if (
        "trade_cal_sse" in trade_cal_entries
        and "trade_cal_szse" in trade_cal_entries
        and should_wait_for_post_close(
            trade_cal_sse=trade_cal_entries["trade_cal_sse"],
            trade_cal_szse=trade_cal_entries["trade_cal_szse"],
            snapshot_root=snapshot_root,
            timezone_name=config.timezone_name,
            post_close_cutoff_local=config.post_close_cutoff_local,
            reference_time_utc=config.reference_time_utc,
        )
    ):
        reason_counts[WAITING_STATUS] += 1
        manifest = build_manifest(
            config=config,
            run_status=WAITING_STATUS,
            entries=entries,
            latest_complete_trade_date=latest_complete_trade_date,
        )
        collection_report["run_status"] = WAITING_STATUS
        collection_report["reason_counts"] = dict(reason_counts)
        return {"manifest": manifest, "collection_report": collection_report, "run_status": WAITING_STATUS}

    collect_specs = [
        ("stock_basic_active", {"list_status": "L"}, "ACTIVE_STOCKS_L"),
        ("daily_all_market", {"trade_date": latest_complete_trade_date}, "ALL_MARKET_DAILY"),
        ("adj_factor_all_market", {"trade_date": latest_complete_trade_date}, "ALL_MARKET_ADJ_FACTOR"),
    ]
    for spec_key, params, scope in collect_specs:
        error_reason, entry = collect_paginated(
            spec=specs[spec_key],
            params=params,
            scope=scope,
            config=CollectorConfig(
                snapshot_root=snapshot_root,
                output_dir=output_dir,
                token_env_var=config.token_env_var,
                run_id=safe_run_id,
                timezone_name=config.timezone_name,
                post_close_cutoff_local=config.post_close_cutoff_local,
                reference_time_utc=config.reference_time_utc,
                page_limit=config.page_limit,
                max_retries=config.max_retries,
                api_url=config.api_url,
            ),
            transport=transport,
            token=token,
            collection_report=collection_report,
        )
        if error_reason:
            reason_counts[error_reason] += 1
        if entry:
            entries.append(entry)

    run_status = SUCCESS_STATUS if len(entries) == 5 and not reason_counts else INCOMPLETE_STATUS
    manifest = build_manifest(
        config=config,
        run_status=run_status,
        entries=entries,
        latest_complete_trade_date=latest_complete_trade_date,
    )
    collection_report["run_status"] = run_status
    collection_report["reason_counts"] = dict(reason_counts)
    return {"manifest": manifest, "collection_report": collection_report, "run_status": run_status}


def write_collection_outputs(result: dict[str, Any], output_dir: Path) -> dict[str, Path]:
    output_root = ensure_external_dir(output_dir)
    run_id = validate_run_id(str(result["manifest"]["run_id"]))
    run_output_dir = ensure_external_run_dir(output_root, run_id)
    run_output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = run_output_dir / "collector_manifest.json"
    report_path = run_output_dir / "collection_report.json"
    write_json_immutable(manifest_path, result["manifest"])
    write_json_immutable(report_path, result["collection_report"])
    return {"manifest_path": manifest_path, "report_path": report_path}


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Collect Tushare A-share daily research snapshots into an external immutable snapshot root."
    )
    parser.add_argument("--snapshot-root", required=True, help="External snapshot root directory.")
    parser.add_argument("--output-dir", required=True, help="External output directory for manifest and report.")
    parser.add_argument(
        "--token-env-var",
        default="TUSHARE_TOKEN",
        help="Environment variable holding the runtime token.",
    )
    parser.add_argument("--run-id", required=True, help="Unique run identifier used for immutable snapshot paths.")
    parser.add_argument("--timezone-name", default="Asia/Shanghai", help="Timezone used for post-close cutoff.")
    parser.add_argument("--post-close-cutoff-local", default="18:00", help="Local post-close cutoff, HH:MM.")
    parser.add_argument(
        "--reference-time-utc",
        default=utc_now_iso(),
        help="Reference UTC time used only to evaluate the post-close window.",
    )
    parser.add_argument("--page-limit", type=int, default=2000, help="Page size for paginated collection.")
    parser.add_argument("--max-retries", type=int, default=2, help="Maximum retries for rate limit and transient errors.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)
    config = CollectorConfig(
        snapshot_root=Path(args.snapshot_root).resolve(),
        output_dir=Path(args.output_dir).resolve(),
        token_env_var=args.token_env_var,
        run_id=args.run_id,
        timezone_name=args.timezone_name,
        post_close_cutoff_local=args.post_close_cutoff_local,
        reference_time_utc=args.reference_time_utc,
        page_limit=args.page_limit,
        max_retries=args.max_retries,
    )
    result = collect_run(config)
    write_collection_outputs(result, config.output_dir)
    return 0 if result["run_status"] == SUCCESS_STATUS else 1


if __name__ == "__main__":
    raise SystemExit(main())
