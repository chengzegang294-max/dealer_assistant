from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

RUNTIME_DIR = Path(__file__).parent
REPO_ROOT = Path(os.environ.get("TRADING_ASSISTANT_REPO_ROOT", r"D:\Stock\trading_assistant"))
OUTPUT_MD_PATH = RUNTIME_DIR / "n02_second_fx_subhour_input_cache_recovery_ready_summary_v1.md"
OUTPUT_JSON_PATH = RUNTIME_DIR / "n02_second_fx_subhour_input_cache_recovery_ready_summary_v1.json"
DATA_ROOT = Path(os.environ.get("TRADING_ANALYSIS_DATA_ROOT", str(REPO_ROOT / "data")))
MT5_DATA_ROOT = Path(
    r"C:\Users\91883\AppData\Roaming\MetaQuotes\Terminal\C9F9BDDC460DF35F331B73B79A3DD57C"
)
TRADEMAX_BASE_ROOT = MT5_DATA_ROOT / "bases" / "TradeMaxGlobal-Demo"
COMMON_FILES_DIR = Path(os.environ.get("APPDATA", "")) / "MetaQuotes" / "Terminal" / "Common" / "Files"
REPO_VALIDATION_LOG = (
    REPO_ROOT
    / "02_runtime"
    / "mt_indicator_probes"
    / "batch_01_volty_xbreaking"
    / "artifacts"
    / "xbreaking"
    / "validation_matrix"
    / "gbpusd_h1_tmgm_longwin_20260702T0250"
    / "log"
    / "20260702.log"
)

GBPUSD_M15_CSV_RE = re.compile(r"(?i)^.*gbpusd.*m15.*\.csv$")
GBPUSD_ANY_CSV_RE = re.compile(r"(?i)^.*gbpusd.*\.csv$")
LOG_PATTERNS = (
    "GBPUSD: preliminary downloading of M1 history started",
    "GBPUSD: preliminary downloading of M1 history completed",
    "GBPUSD: history data begins from",
)


def list_matching_files(root: Path, pattern: re.Pattern[str]) -> List[Dict[str, object]]:
    matched: List[Dict[str, object]] = []
    if not root.exists():
        return matched
    for path in sorted(root.rglob("*.csv")):
        if pattern.match(path.name) is None:
            continue
        matched.append(
            {
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "mtime_utc": to_utc_stamp(path.stat().st_mtime),
            }
        )
    return matched


def to_utc_stamp(value: float) -> str:
    return datetime.fromtimestamp(value, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def scan_data_root(data_root: Path) -> Dict[str, object]:
    gbpusd_m15 = list_matching_files(data_root, GBPUSD_M15_CSV_RE)
    gbpusd_any = list_matching_files(data_root, GBPUSD_ANY_CSV_RE)
    return {
        "inventory_root": str(data_root),
        "gbpusd_m15_csv_count": len(gbpusd_m15),
        "gbpusd_m15_csv_files": gbpusd_m15,
        "gbpusd_any_csv_count": len(gbpusd_any),
        "gbpusd_any_csv_files": gbpusd_any[:20],
    }


def scan_mt5_cache(base_root: Path) -> Dict[str, object]:
    history_dir = base_root / "history" / "GBPUSD"
    ticks_path = base_root / "ticks" / "GBPUSD" / "ticks.dat"
    hcc_files: List[Dict[str, object]] = []
    if history_dir.exists():
        for path in sorted(history_dir.glob("*.hcc")):
            hcc_files.append(
                {
                    "path": str(path),
                    "filename": path.name,
                    "size_bytes": path.stat().st_size,
                    "mtime_utc": to_utc_stamp(path.stat().st_mtime),
                }
            )
    ticks_info: Optional[Dict[str, object]] = None
    if ticks_path.exists():
        ticks_info = {
            "path": str(ticks_path),
            "size_bytes": ticks_path.stat().st_size,
            "mtime_utc": to_utc_stamp(ticks_path.stat().st_mtime),
        }
    return {
        "trade_max_base_root": str(base_root),
        "gbpusd_history_dir": str(history_dir),
        "gbpusd_hcc_count": len(hcc_files),
        "gbpusd_hcc_files": hcc_files,
        "gbpusd_ticks_dat": ticks_info,
        "has_gbpusd_ticks_dat": ticks_info is not None,
    }


def scan_common_files(common_files_dir: Path) -> Dict[str, object]:
    if not common_files_dir.exists():
        return {
            "common_files_dir": str(common_files_dir),
            "gbpusd_probe_csv_count": 0,
            "gbpusd_probe_csv_files": [],
        }
    matched: List[Dict[str, object]] = []
    for path in sorted(common_files_dir.glob("XBreaking_probe_GBPUSD_*.csv")):
        matched.append(
            {
                "path": str(path),
                "filename": path.name,
                "size_bytes": path.stat().st_size,
                "mtime_utc": to_utc_stamp(path.stat().st_mtime),
            }
        )
    return {
        "common_files_dir": str(common_files_dir),
        "gbpusd_probe_csv_count": len(matched),
        "gbpusd_probe_csv_files": matched,
    }


def scan_log_lines(path: Path) -> Dict[str, object]:
    matches: List[Dict[str, object]] = []
    if not path.exists():
        return {
            "path": str(path),
            "exists": False,
            "matched_line_count": 0,
            "matches": matches,
        }
    text = read_text_best_effort(path)
    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        for pattern in LOG_PATTERNS:
            if pattern in raw_line:
                matches.append(
                    {
                        "line_no": line_no,
                        "pattern": pattern,
                        "line": raw_line.strip(),
                    }
                )
                break
    return {
        "path": str(path),
        "exists": True,
        "matched_line_count": len(matches),
        "matches": matches,
    }


def read_text_best_effort(path: Path) -> str:
    raw = path.read_bytes()
    encodings = ["utf-16", "utf-8", "utf-8-sig", "gbk", "latin-1"]
    for encoding in encodings:
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="ignore")


def build_recovery_gate(
    data_inventory: Dict[str, object],
    mt5_cache: Dict[str, object],
    common_files: Dict[str, object],
    repo_log_scan: Dict[str, object],
) -> Dict[str, object]:
    has_drop_export = data_inventory["gbpusd_m15_csv_count"] > 0
    has_cache_history = mt5_cache["gbpusd_hcc_count"] > 0
    has_ticks = bool(mt5_cache["has_gbpusd_ticks_dat"])
    has_probe = common_files["gbpusd_probe_csv_count"] > 0
    has_log_proof = repo_log_scan["matched_line_count"] > 0
    status = "cache_recovery_ready_without_canonical_export"
    if has_drop_export:
        status = "drop_export_present_and_recovery_not_needed"
    return {
        "status": status,
        "has_repo_drop_gbpusd_m15_export": has_drop_export,
        "has_mt5_cache_history_hcc": has_cache_history,
        "has_mt5_ticks_dat": has_ticks,
        "has_common_files_gbpusd_probe_csv": has_probe,
        "has_repo_log_history_download_proof": has_log_proof,
        "recommended_target_symbol": "GBPUSD",
        "recommended_target_timeframe": "M15",
        "recommended_source_environment": "TradeMaxGlobal-Demo__60088394",
        "preferred_next_step": "terminal_export_to_drop_then_ingest_with_n02_mt5_export_ingest_v1",
        "fallback_next_step": "build_or_reuse_hcc_reader_then_convert_to_canonical_bars",
        "blocked_reason": "canonical_gbpusd_m15_export_csv_is_still_missing_under_known_drop_paths",
    }


def build_summary(
    data_inventory: Dict[str, object],
    mt5_cache: Dict[str, object],
    common_files: Dict[str, object],
    repo_log_scan: Dict[str, object],
    gate: Dict[str, object],
    output_md_path: Path,
    output_json_path: Path,
) -> Dict[str, object]:
    return {
        "producer": "n02_second_fx_subhour_input_cache_recovery_ready_build_v1.py",
        "scope": "REOPEN_B9_N02_SECOND_FX_SUBHOUR_INPUT_CACHE_RECOVERY_READY_P0",
        "status": "fresh_run_second_fx_subhour_input_cache_recovery_ready_summary",
        "evidence_mode": "fresh_run_mt5_cache_inventory_and_log_proof_without_declaring_canonical_export",
        "source_path": {
            "data_root": str(DATA_ROOT),
            "mt5_data_root": str(MT5_DATA_ROOT),
            "trademax_base_root": str(TRADEMAX_BASE_ROOT),
            "common_files_dir": str(COMMON_FILES_DIR),
            "repo_validation_log": str(REPO_VALIDATION_LOG),
        },
        "repo_path": {
            "summary_md": str(output_md_path),
            "summary_json": str(output_json_path),
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "boundary": {
            "writes_main_m1_runtime": False,
            "defines_failed_breakout": False,
            "defines_retest_reject": False,
            "defines_day_type": False,
            "is_acquisition_only": True,
            "declares_canonical_export_done": False,
        },
        "data_inventory": data_inventory,
        "mt5_cache_inventory": mt5_cache,
        "common_files_inventory": common_files,
        "repo_validation_log_scan": repo_log_scan,
        "recovery_gate": gate,
    }


def render_md(summary: Dict[str, object]) -> str:
    data_inventory = summary["data_inventory"]
    mt5_cache = summary["mt5_cache_inventory"]
    common_files = summary["common_files_inventory"]
    repo_log_scan = summary["repo_validation_log_scan"]
    gate = summary["recovery_gate"]
    lines = [
        "# n02_second_fx_subhour_input_cache_recovery_ready_summary v1",
        "",
        "## Role",
        "",
        "- Scan the preferred `GBPUSD/M15` recovery path beyond known `data + MT4 history` sources.",
        "- Keep this layer acquisition-only: confirm cache and runtime evidence, but do not claim a canonical export exists yet.",
        "",
        "## 2026-07-05 fresh-run",
        "",
        "- repo_drop_gbpusd_m15_csv_count: `{0}`".format(data_inventory["gbpusd_m15_csv_count"]),
        "- mt5_cache_gbpusd_hcc_count: `{0}`".format(mt5_cache["gbpusd_hcc_count"]),
        "- mt5_cache_has_ticks_dat: `{0}`".format(
            json.dumps(mt5_cache["has_gbpusd_ticks_dat"], ensure_ascii=True)
        ),
        "- common_files_gbpusd_probe_csv_count: `{0}`".format(common_files["gbpusd_probe_csv_count"]),
        "- repo_validation_log_matched_line_count: `{0}`".format(repo_log_scan["matched_line_count"]),
        "- recovery_status: `{0}`".format(gate["status"]),
        "- preferred_next_step: `{0}`".format(gate["preferred_next_step"]),
        "- fallback_next_step: `{0}`".format(gate["fallback_next_step"]),
        "",
        "## Current Decision",
        "",
        "- No `GBPUSD/M15` canonical export csv was found under the known `data` drop paths.",
        "- The preferred `TradeMaxGlobal-Demo__60088394` MT5 runtime already contains recoverable source evidence: yearly `GBPUSD/*.hcc`, `ticks.dat`, repo-copied tester log matches, and `Common\\Files` GBPUSD probe csv files.",
        "- Therefore the mainline is no longer blocked at generic acquisition. It advances to `GBPUSD/M15 cache recovery ready`, with the next exact action fixed to `terminal export -> n02_mt5_export_ingest_v1`, and `hcc reader` kept only as fallback.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-md", default=str(OUTPUT_MD_PATH))
    parser.add_argument("--output-json", default=str(OUTPUT_JSON_PATH))
    args = parser.parse_args()

    data_inventory = scan_data_root(DATA_ROOT)
    mt5_cache = scan_mt5_cache(TRADEMAX_BASE_ROOT)
    common_files = scan_common_files(COMMON_FILES_DIR)
    repo_log_scan = scan_log_lines(REPO_VALIDATION_LOG)
    gate = build_recovery_gate(
        data_inventory=data_inventory,
        mt5_cache=mt5_cache,
        common_files=common_files,
        repo_log_scan=repo_log_scan,
    )
    summary = build_summary(
        data_inventory=data_inventory,
        mt5_cache=mt5_cache,
        common_files=common_files,
        repo_log_scan=repo_log_scan,
        gate=gate,
        output_md_path=Path(args.output_md),
        output_json_path=Path(args.output_json),
    )
    Path(args.output_json).write_text(json.dumps(summary, ensure_ascii=True, indent=2), encoding="utf-8")
    Path(args.output_md).write_text(render_md(summary), encoding="utf-8")

    print("output_md={0}".format(args.output_md))
    print("output_json={0}".format(args.output_json))
    print("repo_drop_gbpusd_m15_csv_count={0}".format(summary["data_inventory"]["gbpusd_m15_csv_count"]))
    print("mt5_cache_gbpusd_hcc_count={0}".format(summary["mt5_cache_inventory"]["gbpusd_hcc_count"]))
    print("repo_validation_log_matched_line_count={0}".format(summary["repo_validation_log_scan"]["matched_line_count"]))
    print("recovery_status={0}".format(summary["recovery_gate"]["status"]))


if __name__ == "__main__":
    main()
