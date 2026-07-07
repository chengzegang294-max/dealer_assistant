from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Callable, Optional, cast


BATCH_DIR = Path(__file__).resolve().parent
ARTIFACT_ROOT = BATCH_DIR / "artifacts"

NormalizeVoltyFn = Callable[[Path], dict[str, Any]]
ValidationMatrixIndexFn = Callable[[str], dict[str, Any]]


def load_ingest_helpers() -> tuple[NormalizeVoltyFn, NormalizeVoltyFn, ValidationMatrixIndexFn]:
    module_path = BATCH_DIR / "probe_artifact_ingest_v1.py"
    spec = importlib.util.spec_from_file_location("probe_artifact_ingest_v1", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"failed to load ingest module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    normalize_series = cast(NormalizeVoltyFn, getattr(module, "normalize_volty_probe_series"))
    normalize_summary = cast(NormalizeVoltyFn, getattr(module, "normalize_volty_probe_summary"))
    build_matrix_index = cast(ValidationMatrixIndexFn, getattr(module, "build_validation_matrix_index_for_family"))
    return normalize_series, normalize_summary, build_matrix_index


normalize_volty_probe_series, normalize_volty_probe_summary, build_validation_matrix_index_for_family = (
    load_ingest_helpers()
)


def latest_file(path: Path, pattern: str) -> Optional[Path]:
    candidates = [p for p in path.glob(pattern) if p.is_file()]
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0]


def parse_optional_int(raw: str) -> Optional[int]:
    s = str(raw).strip()
    if not s:
        return None
    try:
        return int(float(s))
    except Exception:
        return None


def parse_optional_float(raw: str) -> Optional[float]:
    s = str(raw).strip()
    if not s:
        return None
    try:
        value = float(s)
    except Exception:
        return None
    if value > 1e100:
        return None
    return value


def parse_xbreaking_probe_csv(csv_path: Path) -> dict[str, Any]:
    text = csv_path.read_text(encoding="utf-8", errors="ignore")
    header: dict[str, str] = {}
    buffers: dict[int, dict[str, str]] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = [x.strip() for x in line.split("\t") if x.strip() != ""]
        if not parts:
            continue
        if parts[0] == "buffer" and len(parts) >= 3:
            buffer_id = parse_optional_int(parts[1])
            if buffer_id is None:
                continue
            stats: dict[str, str] = {}
            i = 2
            while i + 1 < len(parts):
                stats[parts[i]] = parts[i + 1]
                i += 2
            buffers[buffer_id] = stats
            continue
        if len(parts) >= 2:
            header[parts[0]] = parts[1]

    out: dict[str, Any] = {
        "probe_source_csv": csv_path.name,
        "symbol": header.get("symbol", ""),
        "chart_tf": header.get("chart_tf", ""),
        "indicator_tf": header.get("indicator_tf", ""),
        "indicator_name": header.get("indicator_name", ""),
        "bars_to_probe": parse_optional_int(header.get("bars_to_probe", "")),
        "max_buffers": parse_optional_int(header.get("max_buffers", "")),
        "handle": parse_optional_int(header.get("handle", "")),
        "init_err": parse_optional_int(header.get("init_err", "")),
        "status": header.get("status", ""),
        "buffer_count": len(buffers),
        "buffer0_copied": None,
        "buffer0_non_empty": None,
        "buffer0_last_valid": None,
        "copy_failed_buffers": [],
    }

    copy_failed_buffers: list[int] = []
    for buffer_id in sorted(buffers):
        stats = buffers[buffer_id]
        copied = parse_optional_int(stats.get("copied", ""))
        err = parse_optional_int(stats.get("err", ""))
        non_empty = parse_optional_int(stats.get("non_empty", ""))
        last_valid = parse_optional_float(stats.get("last_valid", ""))
        if buffer_id == 0:
            out["buffer0_copied"] = copied
            out["buffer0_non_empty"] = non_empty
            out["buffer0_last_valid"] = last_valid
        if copied is not None and copied < 0:
            copy_failed_buffers.append(buffer_id)
        out[f"buffer{buffer_id}_copied"] = copied
        out[f"buffer{buffer_id}_err"] = err
        out[f"buffer{buffer_id}_non_empty"] = non_empty
        out[f"buffer{buffer_id}_last_valid"] = last_valid

    out["copy_failed_buffers"] = copy_failed_buffers
    out["buffer_activity_profile"] = (
        "buffer0_only"
        if out["buffer0_copied"] and len(copy_failed_buffers) >= 1
        else "unknown"
    )
    return out


def dir_snapshot(path: Path, pattern: str) -> dict[str, Any]:
    files = [
        p.name
        for p in sorted(path.glob(pattern))
        if p.is_file() and p.name.lower() != "readme.md"
    ]
    return {
        "dir": str(path),
        "exists": path.exists() and path.is_dir(),
        "file_count": len(files),
        "files": files,
    }


def quote_ps(value: str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def build_cross_environment_seed(matrix: Optional[dict[str, Any]]) -> dict[str, str]:
    defaults = {
        "symbol": "EURUSD",
        "chart_period": "H4",
        "indicator_period": "H4",
        "from_date": "2024.12.01",
        "to_date": "2025.03.01",
        "report_stem": "xbreaking_probe_eurusd_h4_second_env",
        "archive_tag": "eurusd_h4_secondenv_YYYYMMDDTHHMM",
    }
    if not isinstance(matrix, dict):
        return defaults
    recommended_archive_tag = str(matrix.get("recommended_cross_environment_seed_archive_tag", "")).strip()
    if recommended_archive_tag:
        recommended_symbol = str(matrix.get("recommended_cross_environment_seed_symbol", "")).strip()
        recommended_chart_period = str(matrix.get("recommended_cross_environment_seed_chart_period", "")).strip()
        recommended_indicator_period = str(matrix.get("recommended_cross_environment_seed_indicator_period", "")).strip()
        recommended_from_date = str(matrix.get("recommended_cross_environment_seed_from_date", "")).strip()
        recommended_to_date = str(matrix.get("recommended_cross_environment_seed_to_date", "")).strip()
        recommended_report_stem = str(matrix.get("recommended_cross_environment_seed_report_stem", "")).strip()
        return {
            "symbol": recommended_symbol or defaults["symbol"],
            "chart_period": recommended_chart_period or defaults["chart_period"],
            "indicator_period": recommended_indicator_period or defaults["indicator_period"],
            "from_date": recommended_from_date or defaults["from_date"],
            "to_date": recommended_to_date or defaults["to_date"],
            "report_stem": (recommended_report_stem + "_second_env") if recommended_report_stem else defaults["report_stem"],
            "archive_tag": recommended_archive_tag + "_secondenv",
        }
    archives_obj = matrix.get("archives")
    if not isinstance(archives_obj, list) or not archives_obj:
        return defaults
    first = archives_obj[0]
    if not isinstance(first, dict):
        return defaults
    archive = cast(dict[str, Any], first)
    symbol = str(archive.get("symbol", "")).strip() or defaults["symbol"]
    chart_period = str(archive.get("chart_period", "")).strip() or defaults["chart_period"]
    indicator_period = str(archive.get("indicator_period", "")).strip() or defaults["indicator_period"]
    from_date = str(archive.get("from_date", "")).strip() or defaults["from_date"]
    to_date = str(archive.get("to_date", "")).strip() or defaults["to_date"]
    report_stem = str(archive.get("report_stem", "")).strip()
    if report_stem:
        report_stem = report_stem + "_second_env"
    else:
        report_stem = defaults["report_stem"]
    archive_tag = str(archive.get("archive_tag", "")).strip()
    if archive_tag:
        archive_tag = archive_tag + "_secondenv"
    else:
        archive_tag = defaults["archive_tag"]
    return {
        "symbol": symbol,
        "chart_period": chart_period,
        "indicator_period": indicator_period,
        "from_date": from_date,
        "to_date": to_date,
        "report_stem": report_stem,
        "archive_tag": archive_tag,
    }


def build_cross_environment_commands(seed: dict[str, str]) -> dict[str, str]:
    inventory_json = (
        "02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\environment_snapshots\\mt_environment_inventory_latest.json"
    )
    probe_script = "02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\run_xbreaking_probe_once.ps1"
    args = (
        f"-Symbol {seed['symbol']} "
        f"-ChartPeriod {seed['chart_period']} "
        f"-IndicatorPeriod {seed['indicator_period']} "
        f"-FromDate {seed['from_date']} "
        f"-ToDate {seed['to_date']} "
        f"-ReportStem {quote_ps(seed['report_stem'])} "
        f"-ArchiveTag {quote_ps(seed['archive_tag'])}"
    )
    return {
        "inventory_refresh": (
            "powershell -ExecutionPolicy Bypass -File "
            "02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_mt_environment_inventory.ps1 "
            f"-OutputJson {inventory_json}"
        ),
        "selector_rerun": (
            f"powershell -ExecutionPolicy Bypass -File {probe_script} "
            f"-EnvironmentInventoryJson {inventory_json} "
            f"-EnvironmentSelector <second_environment_label> {args}"
        ),
        "override_rerun": (
            f"powershell -ExecutionPolicy Bypass -File {probe_script} "
            f"-InstallRoot <mt5_install_root> -DataRootOverride <second_data_root> {args}"
        ),
    }


def build_operator_shortcuts(matrix: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    cross_env_seed = build_cross_environment_seed(matrix)
    cross_env_commands = build_cross_environment_commands(cross_env_seed)
    return {
        "volty_dumpseries": {
            "batch_entry_files": [
                "MT4Probe_Volty_dumpseries_0_6.ini",
                "mt4probe_volty_dumpseries_portable.ini",
            ],
            "copy_targets": [
                {
                    "source": "MT4Probe_Volty_dumpseries_0_6.ini",
                    "target": "portable_terminal\\tester\\MT4Probe_Volty.ini",
                },
                {
                    "source": "mt4probe_volty_dumpseries_portable.ini",
                    "target": "portable_terminal\\config\\mt4probe_volty_dumpseries_portable.ini",
                },
            ],
            "post_run_commands": [
                "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_artifact_ingest_v1.py --family volty --kind csv --copy-latest",
                "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_artifact_ingest_v1.py --family volty --kind csv --normalize-volty-series",
                "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_batch_acceptance_v1.py --json-only",
            ],
        },
        "xbreaking_probe": {
            "batch_entry_files": [
                "run_xbreaking_probe_once.ps1",
                "environment_snapshots\\mt_environment_inventory_latest.json",
                "12_tooling_runtime_archive\\batch_02_mt_indicator_family\\XBreakingProbe.ini",
            ],
            "post_run_commands": [
                "powershell -ExecutionPolicy Bypass -File 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\run_xbreaking_probe_once.ps1",
                "powershell -ExecutionPolicy Bypass -File 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\run_xbreaking_probe_once.ps1 -EnvironmentInventoryJson 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\environment_snapshots\\mt_environment_inventory_latest.json -EnvironmentSelector ICMarketsSC-Demo__52886989 -ChartPeriod H4 -IndicatorPeriod H4 -ReportStem xbreaking_probe_eurusd_h4_envselect -ArchiveTag eurusd_h4_envselect_20260701T1305",
                "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_artifact_ingest_v1.py --family xbreaking --kind csv --archive-tag eurusd_h4_envselect_20260701T1305 --source C:\\Users\\91883\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\XBreaking_probe_EURUSD_H4_20250103_000000.csv",
                "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_artifact_ingest_v1.py --family xbreaking --kind report --archive-tag eurusd_h4_envselect_20260701T1305 --source C:\\Users\\91883\\AppData\\Roaming\\MetaQuotes\\Terminal\\AC48B16F101CC6359ADC4B870ED6B744\\xbreaking_probe_eurusd_h4_envselect.htm",
                "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_artifact_ingest_v1.py --family xbreaking --kind log --archive-tag eurusd_h4_envselect_20260701T1305 --source C:\\Users\\91883\\AppData\\Roaming\\MetaQuotes\\Terminal\\AC48B16F101CC6359ADC4B870ED6B744\\Tester\\logs\\20260701.log --log-keyword XBreakingProbe --log-keyword DONE --log-tail-lines 400",
                "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_artifact_ingest_v1.py --family xbreaking --kind csv --copy-latest",
                "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_artifact_ingest_v1.py --family xbreaking --kind report --copy-latest",
                "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_artifact_ingest_v1.py --family xbreaking --kind log --copy-latest --log-tail-lines 400",
                "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_batch_acceptance_v1.py --json-only",
            ],
        },
        "xbreaking_matrix": {
            "batch_entry_files": [
                "run_xbreaking_validation_matrix.ps1",
                "run_xbreaking_probe_once.ps1",
                "environment_snapshots\\mt_environment_inventory_latest.json",
                "12_tooling_runtime_archive\\batch_02_mt_indicator_family\\XBreakingProbe.ini",
            ],
            "post_run_commands": [
                "powershell -ExecutionPolicy Bypass -File 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\run_xbreaking_validation_matrix.ps1 -Symbols GBPUSD -Periods H4 -TagSuffix matrix_sample",
                "powershell -ExecutionPolicy Bypass -File 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\run_xbreaking_validation_matrix.ps1 -EnvironmentInventoryJson 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\environment_snapshots\\mt_environment_inventory_latest.json -EnvironmentSelector ICMarketsSC-Demo__52886989 -Symbols EURUSD -Periods H4 -TagSuffix envselect_sample",
                "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_batch_acceptance_v1.py --json-only",
            ],
        },
        "xbreaking_cross_environment_bootstrap": {
            "batch_entry_files": [
                "probe_mt_environment_inventory.ps1",
                "run_xbreaking_probe_once.ps1",
                "environment_snapshots\\mt_environment_inventory_latest.json",
            ],
            "seed_archive_tag": cross_env_seed["archive_tag"],
            "seed_symbol": cross_env_seed["symbol"],
            "seed_chart_period": cross_env_seed["chart_period"],
            "seed_indicator_period": cross_env_seed["indicator_period"],
            "seed_from_date": cross_env_seed["from_date"],
            "seed_to_date": cross_env_seed["to_date"],
            "seed_source": "recommended_cross_environment_seed",
            "operator_steps": [
                "launch or register the second MT5 data_root so it appears under MetaQuotes\\Terminal",
                "refresh environment inventory and confirm a new mt5 environment_label or structure_only candidate appears",
                "rerun one representative XBreaking sample with the second environment selector or explicit DataRootOverride",
                "rerun batch acceptance and confirm cross_environment_verified=true",
            ],
            "recommended_commands": [
                cross_env_commands["inventory_refresh"],
                cross_env_commands["selector_rerun"],
                cross_env_commands["override_rerun"],
                "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_batch_acceptance_v1.py --json-only",
            ],
        },
    }


def build_next_actions(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    acceptance = snapshot.get("acceptance", {})
    matrix = snapshot.get("xbreaking_validation_matrix", {})
    cross_env_seed = build_cross_environment_seed(cast(Optional[dict[str, Any]], matrix))
    cross_env_commands = build_cross_environment_commands(cross_env_seed)

    if acceptance.get("volty_csv_present") and snapshot.get("volty_series", {}).get("series_row_count", 0) == 0:
        actions.append(
            {
                "id": "volty_dumpseries_rerun",
                "priority": "high",
                "family": "volty",
                "status": "pending_fresh_run",
                "why": "current historical csv has no series rows, so field-row normalization cannot close",
                "batch_entry_files": [
                    "MT4Probe_Volty_dumpseries_0_6.ini",
                    "mt4probe_volty_dumpseries_portable.ini",
                ],
                "copy_targets": [
                    "portable_terminal\\tester\\MT4Probe_Volty.ini",
                    "portable_terminal\\config\\mt4probe_volty_dumpseries_portable.ini",
                ],
                "operator_steps": [
                    "copy the batch-local DumpSeries templates into the MT4 portable tester",
                    "run MT4 Probe\\MT4Probe_Volty with EURUSD/H1/Open prices only",
                    "keep DumpSeries=1, DumpModeStart=0, DumpModeEnd=6",
                    "copy new csv into artifacts\\volty\\csv",
                ],
                "recommended_commands": [
                    "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_artifact_ingest_v1.py --family volty --kind csv --copy-latest",
                    "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_artifact_ingest_v1.py --family volty --kind csv --normalize-volty-series",
                ],
            }
        )

    if not acceptance.get("volty_tester_report_present"):
        actions.append(
            {
                "id": "volty_report_backfill",
                "priority": "medium",
                "family": "volty",
                "status": "pending_report_recovery",
                "why": "volty tester report is missing from the batch artifacts",
                "operator_steps": [
                    "export MT4 tester report as .htm",
                    "copy report into artifacts\\volty\\tester_report",
                ],
                "recommended_commands": [
                    "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_batch_acceptance_v1.py --json-only",
                ],
            }
        )

    if acceptance.get("xbreaking_csv_present") and not acceptance.get("xbreaking_tester_report_present"):
        actions.append(
            {
                "id": "xbreaking_report_recovery",
                "priority": "high",
                "family": "xbreaking",
                "status": "pending_report_recovery",
                "why": "xbreaking semantics cannot upgrade beyond probe_verified without tester .htm report",
                "operator_steps": [
                    "run the batch-local MT5 helper script to execute XBreakingProbe once",
                    "recover the new csv, tester report and tester log into artifacts\\xbreaking\\*",
                ],
                "recommended_commands": [
                    "powershell -ExecutionPolicy Bypass -File 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\run_xbreaking_probe_once.ps1",
                    "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_artifact_ingest_v1.py --family xbreaking --kind csv --copy-latest",
                    "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_artifact_ingest_v1.py --family xbreaking --kind report --copy-latest",
                    "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_artifact_ingest_v1.py --family xbreaking --kind log --copy-latest --log-tail-lines 400",
                    "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_batch_acceptance_v1.py --json-only",
                ],
            }
        )

    if snapshot.get("artifacts", {}).get("volty_log", {}).get("file_count", 0) == 0:
        actions.append(
            {
                "id": "volty_log_recovery",
                "priority": "medium",
                "family": "volty",
                "status": "pending_log_recovery",
                "why": "volty currently has no tester or terminal log evidence in batch artifacts",
                "operator_steps": [
                    "export tester journal or terminal journal excerpt with Volty probe markers",
                    "copy the log or excerpt into artifacts\\volty\\log",
                ],
                "recommended_commands": [
                    "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_batch_acceptance_v1.py --json-only",
                ],
            }
        )

    if matrix.get("summary_archive_count", 0) >= 1 and not matrix.get("latest_ingest_manifest_present"):
        actions.append(
            {
                "id": "xbreaking_matrix_ingest_manifest_backfill",
                "priority": "medium",
                "family": "xbreaking",
                "status": "pending_archive_ingest_trace",
                "why": "latest validation_matrix archive has run_summary.json but no ingest_manifest.json trace",
                "operator_steps": [
                    "pick the latest validation_matrix archive tag from the acceptance snapshot",
                    "recover csv / report / tester log with --archive-tag so the archive writes ingest_manifest.json",
                    "rerun batch acceptance to confirm latest_ingest_manifest_present=true",
                ],
                "recommended_commands": [
                    "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_batch_acceptance_v1.py --json-only",
                ],
            }
        )

    if matrix.get("summary_archive_count", 0) >= 1 and matrix.get("latest_ingest_manifest_present"):
        latest_archive = {}
        archives_obj = matrix.get("archives")
        if isinstance(archives_obj, list) and archives_obj:
            first = archives_obj[0]
            if isinstance(first, dict):
                latest_archive = cast(dict[str, Any], first)
        if latest_archive.get("manifest_is_repo_existing_only"):
            actions.append(
                {
                    "id": "xbreaking_matrix_latest_provenance_upgrade",
                    "priority": "medium",
                    "family": "xbreaking",
                    "status": "pending_source_trace_upgrade",
                    "why": "latest validation_matrix archive manifest is repo_existing_only, so source_path cannot yet trace back to run_summary files",
                    "operator_steps": [
                        "rerun the latest validation_matrix sample through the batch-local MT5 helper instead of repo-only backfill",
                        "ensure run_summary.json keeps files.*.source populated for csv / report / terminal log / tester log",
                        "rerun probe_artifact_ingest_v1.py --archive-tag <tag> --backfill-ingest-manifest-from-archive and verify manifest_source_record_count > 0",
                    ],
                    "recommended_commands": [
                        "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_artifact_ingest_v1.py --family xbreaking --write-validation-matrix-index",
                        "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_batch_acceptance_v1.py --json-only",
                    ],
                }
            )

    if matrix.get("summary_archive_count", 0) >= 1 and not matrix.get("cross_environment_ready", False):
        actions.append(
            {
                "id": "xbreaking_second_mt5_environment_needed",
                "priority": "high",
                "family": "xbreaking",
                "status": "blocked_by_environment_inventory",
                "why": "current MT5 inventory still exposes only one environment, so cross-environment validation cannot start",
                "operator_steps": [
                    "prepare or register a second MT5 data_root under MetaQuotes\\Terminal",
                    "rerun probe_mt_environment_inventory.ps1 and refresh environment_snapshots\\mt_environment_inventory_latest.json",
                    "confirm inventory_mt5_environment_count >= 2 before launching the next XBreaking rerun",
                ],
                "recommended_commands": [
                    cross_env_commands["inventory_refresh"],
                    cross_env_commands["override_rerun"],
                    "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_batch_acceptance_v1.py --json-only",
                ],
            }
        )
    elif matrix.get("summary_archive_count", 0) >= 1 and not matrix.get("cross_environment_verified", False):
        actions.append(
            {
                "id": "xbreaking_cross_environment_rerun",
                "priority": "high",
                "family": "xbreaking",
                "status": "pending_cross_environment_validation",
                "why": "a second MT5 environment is available, but validation_matrix still covers only one environment label",
                "operator_steps": [
                    "pick a representative XBreaking sample and rerun it with the second EnvironmentSelector",
                    "backfill ingest_manifest for the new archive and refresh validation_matrix_index_latest.json",
                    "rerun batch acceptance and confirm cross_environment_verified=true",
                ],
                "recommended_commands": [
                    cross_env_commands["selector_rerun"],
                    "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_artifact_ingest_v1.py --family xbreaking --write-validation-matrix-index",
                    "python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_batch_acceptance_v1.py --json-only",
                ],
            }
        )

    return actions


def build_acceptance_snapshot() -> dict[str, Any]:
    volty_csv_dir = ARTIFACT_ROOT / "volty" / "csv"
    volty_log_dir = ARTIFACT_ROOT / "volty" / "log"
    volty_report_dir = ARTIFACT_ROOT / "volty" / "tester_report"
    xbreaking_csv_dir = ARTIFACT_ROOT / "xbreaking" / "csv"
    xbreaking_log_dir = ARTIFACT_ROOT / "xbreaking" / "log"
    xbreaking_report_dir = ARTIFACT_ROOT / "xbreaking" / "tester_report"
    xbreaking_validation_matrix_dir = ARTIFACT_ROOT / "xbreaking" / "validation_matrix"

    volty_csv = latest_file(volty_csv_dir, "MT4_probe_Volty_*.csv")
    xbreaking_csv = latest_file(xbreaking_csv_dir, "XBreaking_probe_*.csv")

    out: dict[str, Any] = {
        "format": "probe_batch_01_acceptance_v1",
        "batch_dir": str(BATCH_DIR),
        "artifacts": {
            "volty_csv": dir_snapshot(volty_csv_dir, "*.csv"),
            "volty_log": dir_snapshot(volty_log_dir, "*"),
            "volty_tester_report": dir_snapshot(volty_report_dir, "*.htm*"),
            "xbreaking_csv": dir_snapshot(xbreaking_csv_dir, "*.csv"),
            "xbreaking_log": dir_snapshot(xbreaking_log_dir, "*"),
            "xbreaking_tester_report": dir_snapshot(xbreaking_report_dir, "*.htm*"),
            "xbreaking_validation_matrix": dir_snapshot(xbreaking_validation_matrix_dir, "*"),
        },
    }

    if volty_csv is not None:
        out["volty_summary"] = normalize_volty_probe_summary(volty_csv)
        out["volty_series"] = normalize_volty_probe_series(volty_csv)
    else:
        out["volty_summary"] = {"found": False}
        out["volty_series"] = {"found": False}

    if xbreaking_csv is not None:
        out["xbreaking_summary"] = parse_xbreaking_probe_csv(xbreaking_csv)
    else:
        out["xbreaking_summary"] = {"found": False}

    out["xbreaking_validation_matrix"] = build_validation_matrix_index_for_family("xbreaking")
    out["operator_shortcuts"] = build_operator_shortcuts(out["xbreaking_validation_matrix"])
    out["acceptance"] = {
        "volty_csv_present": volty_csv is not None,
        "volty_summary_status_done": out["volty_summary"].get("status") == "DONE",
        "volty_series_row_count": out["volty_series"].get("series_row_count"),
        "volty_tester_report_present": out["artifacts"]["volty_tester_report"]["file_count"] >= 1,
        "xbreaking_csv_present": xbreaking_csv is not None,
        "xbreaking_status_done": out["xbreaking_summary"].get("status") == "DONE",
        "xbreaking_handle_ok": out["xbreaking_summary"].get("handle", -1) is not None
        and out["xbreaking_summary"].get("handle", -1) >= 0,
        "xbreaking_init_err_ok": out["xbreaking_summary"].get("init_err") == 0,
        "xbreaking_tester_report_present": out["artifacts"]["xbreaking_tester_report"]["file_count"] >= 1,
        "xbreaking_validation_matrix_present": out["xbreaking_validation_matrix"].get("archive_count", 0) >= 1,
        "xbreaking_validation_matrix_latest_summary_present": out["xbreaking_validation_matrix"].get(
            "latest_run_summary_present"
        ),
        "xbreaking_validation_matrix_latest_manifest_present": out["xbreaking_validation_matrix"].get(
            "latest_ingest_manifest_present"
        ),
        "xbreaking_validation_matrix_manifest_source_backed_archive_count": out["xbreaking_validation_matrix"].get(
            "manifest_source_backed_archive_count", 0
        ),
        "xbreaking_validation_matrix_inventory_mt5_environment_count": out["xbreaking_validation_matrix"].get(
            "inventory_mt5_environment_count", 0
        ),
        "xbreaking_validation_matrix_inventory_mt5_environment_labels": out["xbreaking_validation_matrix"].get(
            "inventory_mt5_environment_labels", []
        ),
        "xbreaking_validation_matrix_environment_label_count": out["xbreaking_validation_matrix"].get(
            "validation_matrix_environment_label_count", 0
        ),
        "xbreaking_validation_matrix_environment_labels": out["xbreaking_validation_matrix"].get(
            "validation_matrix_environment_labels", []
        ),
        "xbreaking_validation_matrix_cross_environment_ready": out["xbreaking_validation_matrix"].get(
            "cross_environment_ready", False
        ),
        "xbreaking_validation_matrix_cross_environment_verified": out["xbreaking_validation_matrix"].get(
            "cross_environment_verified", False
        ),
        "xbreaking_validation_matrix_manifest_full_source_backed_archive_count": out[
            "xbreaking_validation_matrix"
        ].get("manifest_full_source_backed_archive_count", 0),
        "xbreaking_validation_matrix_manifest_mixed_provenance_archive_count": out[
            "xbreaking_validation_matrix"
        ].get("manifest_mixed_provenance_archive_count", 0),
        "xbreaking_validation_matrix_manifest_repo_existing_only_archive_count": out[
            "xbreaking_validation_matrix"
        ].get("manifest_repo_existing_only_archive_count", 0),
        "xbreaking_validation_matrix_latest_manifest_source_record_count": out["xbreaking_validation_matrix"].get(
            "latest_manifest_source_record_count", 0
        ),
        "xbreaking_validation_matrix_latest_manifest_repo_existing_record_count": out[
            "xbreaking_validation_matrix"
        ].get("latest_manifest_repo_existing_record_count", 0),
        "xbreaking_validation_matrix_latest_manifest_fresh_run_index_record_count": out[
            "xbreaking_validation_matrix"
        ].get("latest_manifest_fresh_run_index_record_count", 0),
        "xbreaking_validation_matrix_latest_manifest_historical_recovered_record_count": out[
            "xbreaking_validation_matrix"
        ].get("latest_manifest_historical_recovered_record_count", 0),
        "xbreaking_validation_matrix_latest_manifest_has_source_backed_records": out[
            "xbreaking_validation_matrix"
        ].get("latest_manifest_has_source_backed_records", False),
        "xbreaking_validation_matrix_latest_manifest_is_full_source_backed": out["xbreaking_validation_matrix"].get(
            "latest_manifest_is_full_source_backed", False
        ),
        "xbreaking_validation_matrix_latest_manifest_is_mixed_provenance": out["xbreaking_validation_matrix"].get(
            "latest_manifest_is_mixed_provenance", False
        ),
        "xbreaking_validation_matrix_latest_manifest_is_repo_existing_only": out["xbreaking_validation_matrix"].get(
            "latest_manifest_is_repo_existing_only", False
        ),
    }
    out["next_actions"] = build_next_actions(out)
    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-only", action="store_true", help="print json only")
    parser.add_argument(
        "--write-json",
        action="store_true",
        help="write the latest acceptance snapshot into batch acceptance_snapshots",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    snapshot = build_acceptance_snapshot()
    if args.write_json:
        snapshot_dir = BATCH_DIR / "acceptance_snapshots"
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        latest_path = snapshot_dir / "probe_batch_01_acceptance_latest.json"
        latest_path.write_text(json.dumps(snapshot, ensure_ascii=True, indent=2), encoding="utf-8")
    if not args.json_only:
        print("format=probe_batch_01_acceptance_v1")
    print(json.dumps(snapshot, ensure_ascii=True))


if __name__ == "__main__":
    main()
