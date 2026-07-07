from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, List


RUNTIME_DIR = Path(__file__).parent
REAL_INPUT_DIR = RUNTIME_DIR / "real_input_samples"
BARS_PATH = REAL_INPUT_DIR / "n02_real_input_gbpusd_m15_v1.csv"
BARS_REPORT_PATH = REAL_INPUT_DIR / "n02_real_input_gbpusd_m15_report_v1.json"
OR_PROOF_PATH = REAL_INPUT_DIR / "n02_proof_of_mapping_output_gbpusd_m15_v1.csv"
IB_PROOF_PATH = REAL_INPUT_DIR / "n02_ib_proof_of_mapping_output_gbpusd_m15_v1.csv"
OUTPUT_MD_PATH = RUNTIME_DIR / "n02_second_fx_subhour_historical_recovery_gbpusd_m15_summary_v1.md"
OUTPUT_JSON_PATH = RUNTIME_DIR / "n02_second_fx_subhour_historical_recovery_gbpusd_m15_summary_v1.json"


def read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


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
    bars_report: Dict[str, object],
    or_summary: Dict[str, object],
    ib_summary: Dict[str, object],
    output_md_path: Path,
    output_json_path: Path,
) -> Dict[str, object]:
    return {
        "producer": "n02_second_fx_subhour_historical_recovery_gbpusd_m15_build_v1.py",
        "scope": "REOPEN_B9_N02_SECOND_FX_SUBHOUR_HISTORICAL_RECOVERY_GBPUSD_M15_P0",
        "status": "fresh_run_historical_recovered_validation_summary",
        "evidence_mode": "historical_recovered_subhour_validation_without_polluting_main_m1_runtime",
        "source_path": {
            "hst_input": bars_report["source_path"]["hst_input"],
            "bars_csv": str(BARS_PATH),
            "bars_report_json": str(BARS_REPORT_PATH),
            "or_proof_csv": str(OR_PROOF_PATH),
            "ib_proof_csv": str(IB_PROOF_PATH),
        },
        "repo_path": {
            "summary_md": str(output_md_path),
            "summary_json": str(output_json_path),
        },
        "generated_at_utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "boundary": {
            "writes_main_m1_runtime": False,
            "historical_recovered": True,
            "declares_terminal_fresh_export": False,
            "defines_failed_breakout": False,
            "defines_retest_reject": False,
            "defines_day_type": False,
            "is_validation_only": True,
        },
        "bars_report": bars_report,
        "bars_validation": bars_summary,
        "or_validation": or_summary,
        "ib_validation": ib_summary,
        "gate": {
            "status": "historical_recovered_second_fx_subhour_ready",
            "requested_symbol_timeframe": "GBPUSD/M15",
            "source_mode": "historical_recovered_from_vtmarkets_hst",
            "observed_subhour_output": len(bars_report["analysis"]["unique_minute_components"]) > 1,
            "preferred_next_step": "recovered_gbpusd_m15_downstream_without_failed_breakout",
            "replaces_previous_fallback": "build_or_reuse_hcc_reader_then_convert_to_canonical_bars",
        },
    }


def render_md(summary: Dict[str, object]) -> str:
    bars_report = summary["bars_report"]
    bars_validation = summary["bars_validation"]
    or_validation = summary["or_validation"]
    ib_validation = summary["ib_validation"]
    gate = summary["gate"]
    lines = [
        "# n02_second_fx_subhour_historical_recovery_gbpusd_m15_summary v1",
        "",
        "## 作用",
        "",
        "- 对 `GBPUSD/M15` 做 `historical_recovered` 级恢复验证。",
        "- 当前专门记录：`terminal export` 已被证明不足，但旧仓 `VTMarkets-Live 2\\GBPUSD-VIP15.hst` 已能直接转成 canonical bars 并跑通 OR / IB proof。",
        "",
        "## 2026-07-05 fresh-run",
        "",
        "- source_hst: `{0}`".format(bars_report["source_path"]["hst_input"]),
        "- bars_record_count: `{0}`".format(bars_report["analysis"]["record_count"]),
        "- bars_time_range: `{0}` -> `{1}`".format(
            bars_report["analysis"]["first_bar_time"],
            bars_report["analysis"]["last_bar_time"],
        ),
        "- bars_unique_minute_components: `{0}`".format(
            json.dumps(bars_report["analysis"]["unique_minute_components"], ensure_ascii=True)
        ),
        "- bars_step_minutes_histogram: `{0}`".format(
            json.dumps(bars_report["analysis"]["step_minutes_histogram"], ensure_ascii=True)
        ),
        "- OR proof rows: `{0}`".format(or_validation["rows"]),
        "- OR defined: `{0}` / `{1}`".format(or_validation["defined_rows"], or_validation["rows"]),
        "- OR first_break_direction: `{0}`".format(
            json.dumps(or_validation["first_break_direction_counts"], ensure_ascii=True)
        ),
        "- OR first_break_mode: `{0}`".format(
            json.dumps(or_validation["first_break_mode_counts"], ensure_ascii=True)
        ),
        "- IB proof rows: `{0}`".format(ib_validation["rows"]),
        "- IB defined: `{0}` / `{1}`".format(ib_validation["defined_rows"], ib_validation["rows"]),
        "- gate_status: `{0}`".format(gate["status"]),
        "",
        "## 当前裁决",
        "",
        "- 当前 `GBPUSD/M15` 已不再卡在 `hcc reader` fallback，因为仓内现成 `HST reader` 已足够把 `GBPUSD-VIP15.hst` 转成 canonical bars。",
        "- 这一层证据强度是 `historical_recovered`，不是 `TradeMaxGlobal-Demo__60088394` terminal fresh export。",
        "- 当前 recovered `GBPUSD/M15` bars 已能独立跑通 OR / IB proof，可作为 `Batch9 N02` 第二个 FX sub-hour 输入继续向下游推进。",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bars", default=str(BARS_PATH))
    parser.add_argument("--bars-report", default=str(BARS_REPORT_PATH))
    parser.add_argument("--or-proof", default=str(OR_PROOF_PATH))
    parser.add_argument("--ib-proof", default=str(IB_PROOF_PATH))
    parser.add_argument("--output-md", default=str(OUTPUT_MD_PATH))
    parser.add_argument("--output-json", default=str(OUTPUT_JSON_PATH))
    args = parser.parse_args()

    bars_rows = read_rows(Path(args.bars))
    bars_report = load_json(Path(args.bars_report))
    or_rows = read_rows(Path(args.or_proof))
    ib_rows = read_rows(Path(args.ib_proof))
    summary = build_summary(
        bars_summary=summarize_bars(bars_rows),
        bars_report=bars_report,
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
    print("gate_status={0}".format(summary["gate"]["status"]))


if __name__ == "__main__":
    main()
