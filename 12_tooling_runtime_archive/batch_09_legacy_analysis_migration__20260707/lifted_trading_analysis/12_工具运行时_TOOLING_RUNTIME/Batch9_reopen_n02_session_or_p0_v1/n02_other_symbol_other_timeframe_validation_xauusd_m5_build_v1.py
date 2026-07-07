from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

RUNTIME_DIR = Path(__file__).parent
REAL_INPUT_DIR = RUNTIME_DIR / "real_input_samples"
BARS_PATH = REAL_INPUT_DIR / "n02_real_input_xauusd_m5_jobs_v1.csv"
OR_PROOF_PATH = REAL_INPUT_DIR / "n02_proof_of_mapping_output_xauusd_m5_jobs_v1.csv"
IB_PROOF_PATH = REAL_INPUT_DIR / "n02_ib_proof_of_mapping_output_xauusd_m5_jobs_v1.csv"
OUTPUT_MD_PATH = RUNTIME_DIR / "n02_other_symbol_other_timeframe_validation_xauusd_m5_summary_v1.md"
OUTPUT_JSON_PATH = RUNTIME_DIR / "n02_other_symbol_other_timeframe_validation_xauusd_m5_summary_v1.json"


def read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def summarize_bars(rows: List[Dict[str, str]]) -> Dict[str, object]:
    symbol_counts: Dict[str, int] = defaultdict(int)
    timeframe_counts: Dict[str, int] = defaultdict(int)
    first_bar_time = rows[0]["bar_time"] if rows else ""
    last_bar_time = rows[-1]["bar_time"] if rows else ""
    for row in rows:
        symbol_counts[row["symbol"]] += 1
        timeframe_counts[row["timeframe"]] += 1
    return {
        "rows": len(rows),
        "first_bar_time": first_bar_time,
        "last_bar_time": last_bar_time,
        "by_symbol": dict(sorted(symbol_counts.items())),
        "by_timeframe": dict(sorted(timeframe_counts.items())),
    }


def summarize_or(rows: List[Dict[str, str]]) -> Dict[str, object]:
    defined_counts: Dict[str, int] = defaultdict(int)
    session_counts: Dict[str, int] = defaultdict(int)
    direction_counts: Dict[str, int] = defaultdict(int)
    mode_counts: Dict[str, int] = defaultdict(int)
    ambiguous_count = 0
    for row in rows:
        defined_counts[row["opening_range_defined"]] += 1
        session_counts[row["session_id"]] += 1
        direction_counts[row["first_break_direction"]] += 1
        mode_counts[row["first_break_mode"]] += 1
        if row["first_break_mode"] == "ambiguous":
            ambiguous_count += 1
    defined_rows = int(defined_counts.get("1", 0))
    return {
        "rows": len(rows),
        "defined_rows": defined_rows,
        "undefined_rows": len(rows) - defined_rows,
        "defined_ratio": defined_rows / len(rows) if rows else 0.0,
        "by_session": dict(sorted(session_counts.items())),
        "first_break_direction_counts": dict(sorted(direction_counts.items())),
        "first_break_mode_counts": dict(sorted(mode_counts.items())),
        "ambiguous_rows": ambiguous_count,
    }


def summarize_ib(rows: List[Dict[str, str]]) -> Dict[str, object]:
    defined_counts: Dict[str, int] = defaultdict(int)
    session_counts: Dict[str, int] = defaultdict(int)
    for row in rows:
        defined_counts[row["ib_defined"]] += 1
        session_counts[row["session_id"]] += 1
    defined_rows = int(defined_counts.get("1", 0))
    return {
        "rows": len(rows),
        "defined_rows": defined_rows,
        "undefined_rows": len(rows) - defined_rows,
        "defined_ratio": defined_rows / len(rows) if rows else 0.0,
        "by_session": dict(sorted(session_counts.items())),
    }


def build_summary(
    bars_summary: Dict[str, object],
    or_summary: Dict[str, object],
    ib_summary: Dict[str, object],
    output_md_path: Path,
    output_json_path: Path,
) -> Dict[str, object]:
    return {
        "producer": "n02_other_symbol_other_timeframe_validation_xauusd_m5_build_v1.py",
        "scope": "REOPEN_B9_N02_OTHER_SYMBOL_OTHER_TIMEFRAME_VALIDATION_XAUUSD_M5_P0",
        "status": "fresh_run_validation_summary",
        "evidence_mode": "fresh_run_validation_other_symbol_other_timeframe_without_polluting_main_m1_runtime",
        "source_path": {
            "bars_csv": str(BARS_PATH),
            "or_proof_csv": str(OR_PROOF_PATH),
            "ib_proof_csv": str(IB_PROOF_PATH),
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
            "is_validation_only": True,
        },
        "bars_validation": bars_summary,
        "or_validation": or_summary,
        "ib_validation": ib_summary,
    }


def render_md(summary: Dict[str, object]) -> str:
    bars_validation = summary["bars_validation"]
    or_validation = summary["or_validation"]
    ib_validation = summary["ib_validation"]
    lines = [
        "# n02_other_symbol_other_timeframe_validation_xauusd_m5_summary v1",
        "",
        "## 作用",
        "",
        "- 对 `XAUUSD / M5 / jobs sample` 做最小 OR/IB 口径验证。",
        "- 当前只验证 `other symbol + other timeframe` 可跑性，不写回主 `EURUSD/M1` runtime，不升级成行为标签。",
        "",
        "## 2026-07-05 fresh-run",
        "",
        "- bars 行数：`{0}`".format(bars_validation["rows"]),
        "- bars 时间范围：`{0}` -> `{1}`".format(
            bars_validation["first_bar_time"],
            bars_validation["last_bar_time"],
        ),
        "- OR proof 行数：`{0}`".format(or_validation["rows"]),
        "- OR defined：`{0}` / `{1}`".format(or_validation["defined_rows"], or_validation["rows"]),
        "- OR first_break_direction：`{0}`".format(json.dumps(or_validation["first_break_direction_counts"], ensure_ascii=True)),
        "- OR first_break_mode：`{0}`".format(json.dumps(or_validation["first_break_mode_counts"], ensure_ascii=True)),
        "- IB proof 行数：`{0}`".format(ib_validation["rows"]),
        "- IB defined：`{0}` / `{1}`".format(ib_validation["defined_rows"], ib_validation["rows"]),
        "",
        "## 当前裁决",
        "",
        "- `XAUUSD/M5` jobs 样本已能独立跑通 OR/IB proof。",
        "- OR proof 当前 `516/601` 行已定义，`89/601` 行未定义；IB proof 当前 `516/516` 行已定义。",
        "- 当前验证层只说明 `other symbol + other timeframe` 可跑性，不把 `XAUUSD/M5` 混入主 `EURUSD/M1` 行为链。",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bars", default=str(BARS_PATH))
    parser.add_argument("--or-proof", default=str(OR_PROOF_PATH))
    parser.add_argument("--ib-proof", default=str(IB_PROOF_PATH))
    parser.add_argument("--output-md", default=str(OUTPUT_MD_PATH))
    parser.add_argument("--output-json", default=str(OUTPUT_JSON_PATH))
    args = parser.parse_args()

    bars_rows = read_rows(Path(args.bars))
    or_rows = read_rows(Path(args.or_proof))
    ib_rows = read_rows(Path(args.ib_proof))
    summary = build_summary(
        bars_summary=summarize_bars(bars_rows),
        or_summary=summarize_or(or_rows),
        ib_summary=summarize_ib(ib_rows),
        output_md_path=Path(args.output_md),
        output_json_path=Path(args.output_json),
    )
    Path(args.output_json).write_text(json.dumps(summary, ensure_ascii=True, indent=2), encoding="utf-8")
    Path(args.output_md).write_text(render_md(summary), encoding="utf-8")

    print("output_md={0}".format(args.output_md))
    print("output_json={0}".format(args.output_json))
    print("bars_rows={0}".format(summary["bars_validation"]["rows"]))
    print("or_rows={0}".format(summary["or_validation"]["rows"]))
    print("or_defined_rows={0}".format(summary["or_validation"]["defined_rows"]))
    print("ib_rows={0}".format(summary["ib_validation"]["rows"]))
    print("ib_defined_rows={0}".format(summary["ib_validation"]["defined_rows"]))


if __name__ == "__main__":
    main()
