from __future__ import annotations

import argparse
import csv
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

RUNTIME_DIR = Path(__file__).parent
TOOLING_ROOT = RUNTIME_DIR.parent
REPO_ROOT = TOOLING_ROOT.parent
REAL_INPUT_DIR = RUNTIME_DIR / "real_input_samples"
CONFIG_PATH = REAL_INPUT_DIR / "n02_or_proof_config_v1.json"
BARS_PATH = REAL_INPUT_DIR / "n02_real_input_gbpusd_h1_v1.csv"
IB_PROOF_PATH = REAL_INPUT_DIR / "n02_ib_proof_of_mapping_output_gbpusd_h1_v1.csv"
OUTPUT_MD_PATH = RUNTIME_DIR / "n02_second_fx_symbol_input_gate_gbpusd_h1_summary_v1.md"
OUTPUT_JSON_PATH = RUNTIME_DIR / "n02_second_fx_symbol_input_gate_gbpusd_h1_summary_v1.json"
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

PAIR_TOKEN_RE = re.compile(r"(?i)([A-Z]{6})[_-](M1|M5|M15|M30|H1|H4|1H)$")


def load_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def timeframe_to_minutes(timeframe: str) -> int:
    tf = timeframe.strip().upper()
    if tf.startswith("M") and tf[1:].isdigit():
        return int(tf[1:])
    if tf.startswith("H") and tf[1:].isdigit():
        return int(tf[1:]) * 60
    raise ValueError("unsupported timeframe: {0}".format(timeframe))


def detect_h1_fx_inventory(data_root: Path) -> Dict[str, object]:
    csv_paths = sorted(data_root.glob("*_1h.csv"))
    detected_symbols: List[str] = []
    for path in csv_paths:
        stem = path.stem.upper()
        pair = stem.split("_")[0]
        if len(pair) != 6 or not pair.isalpha():
            continue
        if pair[:3] in KNOWN_CURRENCIES and pair[3:] in KNOWN_CURRENCIES:
            detected_symbols.append(pair)
    detected_symbols = sorted(set(detected_symbols))
    return {
        "inventory_root": str(data_root),
        "fx_h1_symbols": detected_symbols,
        "fx_h1_symbol_count": len(detected_symbols),
        "second_fx_symbols_excluding_eurusd": [s for s in detected_symbols if s != "EURUSD"],
    }


def summarize_bars(rows: List[Dict[str, str]]) -> Dict[str, object]:
    first_bar_time = rows[0]["bar_time"] if rows else ""
    last_bar_time = rows[-1]["bar_time"] if rows else ""
    symbol = rows[0]["symbol"] if rows else ""
    timeframe = rows[0]["timeframe"] if rows else ""
    timezone_heuristic = (
        "first_bar_utc_like_sunday_reopen"
        if first_bar_time.endswith("T22:00:00Z")
        else "not_checked"
    )
    return {
        "rows": len(rows),
        "symbol": symbol,
        "timeframe": timeframe,
        "first_bar_time": first_bar_time,
        "last_bar_time": last_bar_time,
        "timezone_heuristic": timezone_heuristic,
    }


def summarize_ib(rows: List[Dict[str, str]]) -> Dict[str, object]:
    defined_rows = sum(1 for row in rows if row["ib_defined"] == "1")
    by_session: Dict[str, int] = {}
    for row in rows:
        by_session[row["session_id"]] = by_session.get(row["session_id"], 0) + 1
    return {
        "rows": len(rows),
        "defined_rows": defined_rows,
        "undefined_rows": len(rows) - defined_rows,
        "defined_ratio": defined_rows / len(rows) if rows else 0.0,
        "by_session": dict(sorted(by_session.items())),
    }


def analyze_or_gate(config: Dict[str, object], timeframe: str) -> Dict[str, object]:
    timeframe_minutes = timeframe_to_minutes(timeframe)
    blocked_sessions: List[Dict[str, object]] = []
    sessions = config.get("sessions", {})
    for session_id, session in sessions.items():
        window_minutes = int(session["opening_range_window_minutes"])
        open_hhmm = str(session["session_open_local_hhmm"])
        open_minute = int(open_hhmm.split(":")[1])
        blocked_sessions.append(
            {
                "session_id": str(session_id),
                "session_open_local_hhmm": open_hhmm,
                "opening_range_window_minutes": window_minutes,
                "timeframe_minutes": timeframe_minutes,
                "window_shorter_than_timeframe": window_minutes < timeframe_minutes,
                "session_open_not_aligned_to_timeframe": (open_minute % timeframe_minutes) != 0,
            }
        )
    return {
        "status": "blocked_by_timeframe_granularity",
        "timeframe": timeframe,
        "timeframe_minutes": timeframe_minutes,
        "observed_command_failure": "ValueError: max() iterable argument is empty",
        "blocked_sessions": blocked_sessions,
    }


def build_summary(
    inventory_summary: Dict[str, object],
    bars_summary: Dict[str, object],
    ib_summary: Dict[str, object],
    or_gate_summary: Dict[str, object],
    output_md_path: Path,
    output_json_path: Path,
) -> Dict[str, object]:
    return {
        "producer": "n02_second_fx_symbol_input_gate_gbpusd_h1_build_v1.py",
        "scope": "REOPEN_B9_N02_SECOND_FX_SYMBOL_INPUT_GATE_GBPUSD_H1_P0",
        "status": "fresh_run_second_fx_input_gate_summary",
        "evidence_mode": "fresh_run_input_gate_without_polluting_main_m1_runtime",
        "source_path": {
            "data_root": str(DATA_ROOT),
            "bars_csv": str(BARS_PATH),
            "ib_proof_csv": str(IB_PROOF_PATH),
            "config_json": str(CONFIG_PATH),
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
        "inventory": inventory_summary,
        "bars_validation": bars_summary,
        "ib_validation": ib_summary,
        "or_gate": or_gate_summary,
    }


def render_md(summary: Dict[str, object]) -> str:
    inventory = summary["inventory"]
    bars_validation = summary["bars_validation"]
    ib_validation = summary["ib_validation"]
    or_gate = summary["or_gate"]
    lines = [
        "# n02_second_fx_symbol_input_gate_gbpusd_h1_summary v1",
        "",
        "## 作用",
        "",
        "- 对 `GBPUSD/H1` 做 `second fx symbol input gate` 级验证。",
        "- 当前只确认第二个 FX 原始输入是否存在、是否能 ingest、以及是否满足当前 `30m OR` 粒度要求。",
        "",
        "## 2026-07-05 fresh-run",
        "",
        "- 发现的 `FX H1` 原始样本：`{0}`".format(json.dumps(inventory["fx_h1_symbols"], ensure_ascii=True)),
        "- 第二个 FX 候选（排除 `EURUSD`）：`{0}`".format(
            json.dumps(inventory["second_fx_symbols_excluding_eurusd"], ensure_ascii=True)
        ),
        "- 当前选定样本：`GBPUSD/H1`",
        "- bars 行数：`{0}`".format(bars_validation["rows"]),
        "- bars 时间范围：`{0}` -> `{1}`".format(
            bars_validation["first_bar_time"], bars_validation["last_bar_time"]
        ),
        "- timezone heuristic：`{0}`".format(bars_validation["timezone_heuristic"]),
        "- IB proof 行数：`{0}`".format(ib_validation["rows"]),
        "- IB defined：`{0}` / `{1}`".format(ib_validation["defined_rows"], ib_validation["rows"]),
        "- OR gate 状态：`{0}`".format(or_gate["status"]),
        "- OR 观察到的命令失败：`{0}`".format(or_gate["observed_command_failure"]),
        "",
        "## 当前裁决",
        "",
        "- 第二个 FX 原始输入已经存在，且不止一个候选；当前首个落地样本固定为 `GBPUSD/H1`。",
        "- `GBPUSD/H1` 的 ingest 与 IB proof 可跑，但当前 `H1` 粒度不满足 `30m opening range` 口径。",
        "- 因此这层当前收口为 `input gate`，下一步应切到 `second FX sub-hour input validation`，不把 `H1` 强行写成 OR validation 成功。",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", default=str(DATA_ROOT))
    parser.add_argument("--bars", default=str(BARS_PATH))
    parser.add_argument("--ib-proof", default=str(IB_PROOF_PATH))
    parser.add_argument("--config", default=str(CONFIG_PATH))
    parser.add_argument("--output-md", default=str(OUTPUT_MD_PATH))
    parser.add_argument("--output-json", default=str(OUTPUT_JSON_PATH))
    args = parser.parse_args()

    inventory_summary = detect_h1_fx_inventory(Path(args.data_root))
    bars_rows = read_rows(Path(args.bars))
    ib_rows = read_rows(Path(args.ib_proof))
    config = load_json(Path(args.config))
    bars_summary = summarize_bars(bars_rows)
    summary = build_summary(
        inventory_summary=inventory_summary,
        bars_summary=bars_summary,
        ib_summary=summarize_ib(ib_rows),
        or_gate_summary=analyze_or_gate(config, bars_summary["timeframe"]),
        output_md_path=Path(args.output_md),
        output_json_path=Path(args.output_json),
    )
    Path(args.output_json).write_text(json.dumps(summary, ensure_ascii=True, indent=2), encoding="utf-8")
    Path(args.output_md).write_text(render_md(summary), encoding="utf-8")

    print("output_md={0}".format(args.output_md))
    print("output_json={0}".format(args.output_json))
    print("fx_h1_symbol_count={0}".format(summary["inventory"]["fx_h1_symbol_count"]))
    print("bars_rows={0}".format(summary["bars_validation"]["rows"]))
    print("ib_rows={0}".format(summary["ib_validation"]["rows"]))
    print("ib_defined_rows={0}".format(summary["ib_validation"]["defined_rows"]))
    print("or_gate_status={0}".format(summary["or_gate"]["status"]))


if __name__ == "__main__":
    main()
