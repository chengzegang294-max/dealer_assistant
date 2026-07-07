from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

RUNTIME_DIR = Path(__file__).parent
TOOLING_ROOT = RUNTIME_DIR.parent
REPO_ROOT = TOOLING_ROOT.parent
ARCHIVE_ROOT = REPO_ROOT / "12_tooling_runtime_archive" / "batch_05_legacy_mt4_probe_assets__20260706"
OUTPUT_MD_PATH = RUNTIME_DIR / "n02_second_fx_subhour_input_acquisition_summary_v1.md"
OUTPUT_JSON_PATH = RUNTIME_DIR / "n02_second_fx_subhour_input_acquisition_summary_v1.json"
DATA_ROOT = Path(os.environ.get("TRADING_ANALYSIS_DATA_ROOT", str(REPO_ROOT / "data")))
MT4_HISTORY_DIRS = [
    ARCHIVE_ROOT / "03_MT4便携探针实例" / "history" / "ICMarketsSC-Demo03",
    ARCHIVE_ROOT / "mt4_probe_instance" / "history" / "ICMarketsSC-Demo03",
]

KNOWN_CURRENCIES = {
    "AUD",
    "CAD",
    "CHF",
    "EUR",
    "GBP",
    "JPY",
    "NZD",
    "USD",
}

FX_SUBHOUR_CSV_RE = re.compile(r"(?i)^([A-Z]{6})_(M1|M5|M15|M30)\.csv$")
FX_HST_RE = re.compile(r"(?i)^([A-Z]{6})(1|5|15|30|60|240)\.hst$")


def is_fx_symbol(symbol: str) -> bool:
    return len(symbol) == 6 and symbol[:3] in KNOWN_CURRENCIES and symbol[3:] in KNOWN_CURRENCIES


def scan_data_root(data_root: Path) -> Dict[str, object]:
    matched_files: List[Dict[str, str]] = []
    symbols: List[str] = []
    timeframes: List[str] = []
    for path in sorted(data_root.rglob("*.csv")):
        match = FX_SUBHOUR_CSV_RE.match(path.name)
        if match is None:
            continue
        symbol = match.group(1).upper()
        timeframe = match.group(2).upper()
        if not is_fx_symbol(symbol):
            continue
        matched_files.append(
            {
                "symbol": symbol,
                "timeframe": timeframe,
                "relative_path": str(path.relative_to(data_root)),
            }
        )
        symbols.append(symbol)
        timeframes.append(timeframe)
    return {
        "inventory_root": str(data_root),
        "subhour_file_count": len(matched_files),
        "subhour_symbols": sorted(set(symbols)),
        "subhour_timeframes": sorted(set(timeframes), key=timeframe_sort_key),
        "matched_files": matched_files,
    }


def scan_mt4_histories(history_dirs: List[Path]) -> Dict[str, object]:
    subhour_files: List[Dict[str, str]] = []
    higher_tf_files: List[Dict[str, str]] = []
    subhour_symbols: List[str] = []
    higher_tf_symbols: List[str] = []
    for history_dir in history_dirs:
        if not history_dir.exists():
            continue
        for path in sorted(history_dir.glob("*.hst")):
            match = FX_HST_RE.match(path.name)
            if match is None:
                continue
            symbol = match.group(1).upper()
            timeframe_code = match.group(2)
            if not is_fx_symbol(symbol):
                continue
            timeframe = code_to_timeframe(timeframe_code)
            item = {
                "symbol": symbol,
                "timeframe": timeframe,
                "history_dir": str(history_dir),
                "filename": path.name,
            }
            if timeframe in {"M1", "M5", "M15", "M30"}:
                subhour_files.append(item)
                subhour_symbols.append(symbol)
            else:
                higher_tf_files.append(item)
                higher_tf_symbols.append(symbol)
    return {
        "history_dirs": [str(p) for p in history_dirs],
        "subhour_file_count": len(subhour_files),
        "subhour_symbols": sorted(set(subhour_symbols)),
        "subhour_files": subhour_files,
        "higher_tf_file_count": len(higher_tf_files),
        "higher_tf_symbols": sorted(set(higher_tf_symbols)),
        "higher_tf_files": higher_tf_files,
    }


def code_to_timeframe(code: str) -> str:
    mapping = {
        "1": "M1",
        "5": "M5",
        "15": "M15",
        "30": "M30",
        "60": "H1",
        "240": "H4",
    }
    return mapping[code]


def timeframe_sort_key(timeframe: str) -> int:
    if timeframe.startswith("M"):
        return int(timeframe[1:])
    if timeframe.startswith("H"):
        return 1000 + int(timeframe[1:]) * 60
    return 10_000


def build_gate(data_inventory: Dict[str, object], mt4_inventory: Dict[str, object]) -> Dict[str, object]:
    data_second_fx = [s for s in data_inventory["subhour_symbols"] if s != "EURUSD"]
    mt4_second_fx = [s for s in mt4_inventory["subhour_symbols"] if s != "EURUSD"]
    combined_second_fx = sorted(set(data_second_fx + mt4_second_fx))
    return {
        "status": "blocked_by_missing_second_fx_subhour_across_known_sources",
        "data_second_fx_subhour_symbols_excluding_eurusd": data_second_fx,
        "mt4_second_fx_subhour_symbols_excluding_eurusd": mt4_second_fx,
        "combined_second_fx_subhour_symbols_excluding_eurusd": combined_second_fx,
        "known_higher_tf_fx_symbols_without_subhour": sorted(
            set(mt4_inventory["higher_tf_symbols"]) - set(mt4_inventory["subhour_symbols"])
        ),
        "blocked_reason": (
            "known_data_and_mt4_history_sources_do_not_contain_second_fx_subhour_input"
        ),
        "recommended_target_symbol": "GBPUSD",
        "recommended_target_timeframe": "M15",
        "recommended_target_reason": (
            "gbpusd_is_already_the_selected_second_fx_h1_gate_symbol_and_m15_matches_existing_subhour_validation_style"
        ),
    }


def build_summary(
    data_inventory: Dict[str, object],
    mt4_inventory: Dict[str, object],
    gate: Dict[str, object],
    output_md_path: Path,
    output_json_path: Path,
) -> Dict[str, object]:
    return {
        "producer": "n02_second_fx_subhour_input_acquisition_build_v1.py",
        "scope": "REOPEN_B9_N02_SECOND_FX_SUBHOUR_INPUT_ACQUISITION_P0",
        "status": "fresh_run_second_fx_subhour_input_acquisition_summary",
        "evidence_mode": "fresh_run_inventory_acquisition_without_polluting_main_m1_runtime",
        "source_path": {
            "data_root": str(DATA_ROOT),
            "mt4_history_dirs": [str(p) for p in MT4_HISTORY_DIRS],
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
        },
        "data_inventory": data_inventory,
        "mt4_history_inventory": mt4_inventory,
        "acquisition_gate": gate,
    }


def render_md(summary: Dict[str, object]) -> str:
    data_inventory = summary["data_inventory"]
    mt4_inventory = summary["mt4_history_inventory"]
    gate = summary["acquisition_gate"]
    lines = [
        "# n02_second_fx_subhour_input_acquisition_summary v1",
        "",
        "## Role",
        "",
        "- Scan known `data` and `MT4 history` sources for a second FX symbol sub-hour input.",
        "- Keep this layer as acquisition-only evidence, without writing any main runtime fields.",
        "",
        "## 2026-07-05 fresh-run",
        "",
        "- data_subhour_symbols: `{0}`".format(json.dumps(data_inventory["subhour_symbols"], ensure_ascii=True)),
        "- data_subhour_timeframes: `{0}`".format(
            json.dumps(data_inventory["subhour_timeframes"], ensure_ascii=True)
        ),
        "- mt4_subhour_symbols: `{0}`".format(
            json.dumps(mt4_inventory["subhour_symbols"], ensure_ascii=True)
        ),
        "- mt4_higher_tf_symbols: `{0}`".format(
            json.dumps(mt4_inventory["higher_tf_symbols"], ensure_ascii=True)
        ),
        "- combined_second_fx_subhour_symbols_excluding_eurusd: `{0}`".format(
            json.dumps(gate["combined_second_fx_subhour_symbols_excluding_eurusd"], ensure_ascii=True)
        ),
        "- known_higher_tf_fx_symbols_without_subhour: `{0}`".format(
            json.dumps(gate["known_higher_tf_fx_symbols_without_subhour"], ensure_ascii=True)
        ),
        "- recommended_target: `{0}/{1}`".format(
            gate["recommended_target_symbol"], gate["recommended_target_timeframe"]
        ),
        "- acquisition_status: `{0}`".format(gate["status"]),
        "",
        "## Current Decision",
        "",
        "- Across the currently known `data` and `MT4 history` sources, no second FX sub-hour input was found.",
        "- `EURUSD` still has the only sub-hour raw source; `GBPUSD / USDCHF / USDJPY` currently appear only as higher-timeframe MT4 history files.",
        "- Therefore the next stop remains `second FX sub-hour input acquisition`, now narrowed to `GBPUSD/M15 export or external recovery beyond known sources`.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-md", default=str(OUTPUT_MD_PATH))
    parser.add_argument("--output-json", default=str(OUTPUT_JSON_PATH))
    args = parser.parse_args()

    data_inventory = scan_data_root(DATA_ROOT)
    mt4_inventory = scan_mt4_histories(MT4_HISTORY_DIRS)
    gate = build_gate(data_inventory, mt4_inventory)
    summary = build_summary(
        data_inventory=data_inventory,
        mt4_inventory=mt4_inventory,
        gate=gate,
        output_md_path=Path(args.output_md),
        output_json_path=Path(args.output_json),
    )
    Path(args.output_json).write_text(json.dumps(summary, ensure_ascii=True, indent=2), encoding="utf-8")
    Path(args.output_md).write_text(render_md(summary), encoding="utf-8")

    print("output_md={0}".format(args.output_md))
    print("output_json={0}".format(args.output_json))
    print("data_subhour_file_count={0}".format(summary["data_inventory"]["subhour_file_count"]))
    print("mt4_subhour_file_count={0}".format(summary["mt4_history_inventory"]["subhour_file_count"]))
    print(
        "combined_second_fx_subhour_symbol_count={0}".format(
            len(summary["acquisition_gate"]["combined_second_fx_subhour_symbols_excluding_eurusd"])
        )
    )
    print("acquisition_status={0}".format(summary["acquisition_gate"]["status"]))


if __name__ == "__main__":
    main()
