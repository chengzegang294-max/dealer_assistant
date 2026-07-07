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
OUTPUT_MD_PATH = RUNTIME_DIR / "n02_second_fx_subhour_input_gate_summary_v1.md"
OUTPUT_JSON_PATH = RUNTIME_DIR / "n02_second_fx_subhour_input_gate_summary_v1.json"
DATA_ROOT = Path(os.environ.get("TRADING_ANALYSIS_DATA_ROOT", str(REPO_ROOT / "data")))

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

FX_SUBHOUR_FILE_RE = re.compile(r"(?i)^([A-Z]{6})_(M1|M5|M15|M30)\.csv$")


def detect_subhour_fx_inventory(data_root: Path) -> Dict[str, object]:
    matched_files: List[Dict[str, str]] = []
    detected_symbols: List[str] = []
    detected_timeframes: List[str] = []
    for path in sorted(data_root.rglob("*.csv")):
        match = FX_SUBHOUR_FILE_RE.match(path.name)
        if match is None:
            continue
        symbol = match.group(1).upper()
        timeframe = match.group(2).upper()
        if symbol[:3] not in KNOWN_CURRENCIES or symbol[3:] not in KNOWN_CURRENCIES:
            continue
        matched_files.append(
            {
                "symbol": symbol,
                "timeframe": timeframe,
                "relative_path": str(path.relative_to(data_root)),
            }
        )
        detected_symbols.append(symbol)
        detected_timeframes.append(timeframe)

    unique_symbols = sorted(set(detected_symbols))
    unique_timeframes = sorted(set(detected_timeframes), key=timeframe_sort_key)
    second_fx_symbols = [symbol for symbol in unique_symbols if symbol != "EURUSD"]
    return {
        "inventory_root": str(data_root),
        "fx_subhour_file_count": len(matched_files),
        "fx_subhour_symbols": unique_symbols,
        "fx_subhour_symbol_count": len(unique_symbols),
        "fx_subhour_timeframes": unique_timeframes,
        "second_fx_subhour_symbols_excluding_eurusd": second_fx_symbols,
        "second_fx_subhour_symbol_count": len(second_fx_symbols),
        "matched_files": matched_files,
    }


def timeframe_sort_key(timeframe: str) -> int:
    return int(timeframe[1:]) if timeframe.startswith("M") else 10_000


def analyze_gate(inventory: Dict[str, object]) -> Dict[str, object]:
    second_fx_symbols = inventory["second_fx_subhour_symbols_excluding_eurusd"]
    if second_fx_symbols:
        return {
            "status": "second_fx_subhour_input_found",
            "blocked_reason": "",
            "candidate_symbols": second_fx_symbols,
        }
    return {
        "status": "blocked_by_missing_second_fx_subhour_input",
        "blocked_reason": "data_root_has_fx_subhour_files_but_only_eurusd_is_present",
        "candidate_symbols": second_fx_symbols,
    }


def build_summary(
    inventory: Dict[str, object],
    gate: Dict[str, object],
    output_md_path: Path,
    output_json_path: Path,
) -> Dict[str, object]:
    return {
        "producer": "n02_second_fx_subhour_input_gate_build_v1.py",
        "scope": "REOPEN_B9_N02_SECOND_FX_SUBHOUR_INPUT_GATE_P0",
        "status": "fresh_run_second_fx_subhour_input_gate_summary",
        "evidence_mode": "fresh_run_inventory_gate_without_polluting_main_m1_runtime",
        "source_path": {
            "data_root": str(DATA_ROOT),
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
            "is_input_gate_only": True,
        },
        "inventory": inventory,
        "gate": gate,
    }


def render_md(summary: Dict[str, object]) -> str:
    inventory = summary["inventory"]
    gate = summary["gate"]
    lines = [
        "# n02_second_fx_subhour_input_gate_summary v1",
        "",
        "## Role",
        "",
        "- Scan `D:\\Stock\\trading_analysis\\data` for `FX + sub-hour` real-input candidates.",
        "- Keep this layer as `input gate` only, without writing any main runtime fields.",
        "",
        "## 2026-07-05 fresh-run",
        "",
        "- fx_subhour_file_count: `{0}`".format(inventory["fx_subhour_file_count"]),
        "- fx_subhour_symbols: `{0}`".format(
            json.dumps(inventory["fx_subhour_symbols"], ensure_ascii=True)
        ),
        "- fx_subhour_timeframes: `{0}`".format(
            json.dumps(inventory["fx_subhour_timeframes"], ensure_ascii=True)
        ),
        "- second_fx_subhour_symbols_excluding_eurusd: `{0}`".format(
            json.dumps(inventory["second_fx_subhour_symbols_excluding_eurusd"], ensure_ascii=True)
        ),
        "- gate_status: `{0}`".format(gate["status"]),
        "- blocked_reason: `{0}`".format(gate["blocked_reason"]),
        "",
        "## Current Decision",
        "",
        "- The current `data` root does contain `FX + sub-hour` inputs, but they are still limited to `EURUSD`.",
        "- No second FX symbol sub-hour sample was found under the current naming contract.",
        "- Therefore the next stop contracts to `second FX sub-hour input acquisition`, rather than forcing `validation` on a non-existent sample.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", default=str(DATA_ROOT))
    parser.add_argument("--output-md", default=str(OUTPUT_MD_PATH))
    parser.add_argument("--output-json", default=str(OUTPUT_JSON_PATH))
    args = parser.parse_args()

    inventory = detect_subhour_fx_inventory(Path(args.data_root))
    gate = analyze_gate(inventory)
    summary = build_summary(
        inventory=inventory,
        gate=gate,
        output_md_path=Path(args.output_md),
        output_json_path=Path(args.output_json),
    )
    Path(args.output_json).write_text(json.dumps(summary, ensure_ascii=True, indent=2), encoding="utf-8")
    Path(args.output_md).write_text(render_md(summary), encoding="utf-8")

    print("output_md={0}".format(args.output_md))
    print("output_json={0}".format(args.output_json))
    print("fx_subhour_file_count={0}".format(summary["inventory"]["fx_subhour_file_count"]))
    print("fx_subhour_symbol_count={0}".format(summary["inventory"]["fx_subhour_symbol_count"]))
    print(
        "second_fx_subhour_symbol_count={0}".format(
            summary["inventory"]["second_fx_subhour_symbol_count"]
        )
    )
    print("gate_status={0}".format(summary["gate"]["status"]))


if __name__ == "__main__":
    main()
