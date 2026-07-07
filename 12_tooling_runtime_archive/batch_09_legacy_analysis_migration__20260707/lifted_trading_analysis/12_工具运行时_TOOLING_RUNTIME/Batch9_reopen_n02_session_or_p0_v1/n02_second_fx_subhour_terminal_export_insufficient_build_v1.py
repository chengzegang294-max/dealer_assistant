from __future__ import annotations

import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


RUNTIME_DIR = Path(__file__).parent
REPO_ROOT = Path(r"D:\Stock\trading_assistant")

ARCHIVE_ROOT = (
    REPO_ROOT
    / "02_runtime"
    / "mt_indicator_probes"
    / "batch_01_volty_xbreaking"
    / "artifacts"
    / "mt5_bar_export"
    / "fix2_gbpusd_m15_short_tmgm_20260705T1737"
)
RUN_SUMMARY_PATH = ARCHIVE_ROOT / "run_summary.json"
TESTER_LOG_PATH = ARCHIVE_ROOT / "log" / "20260705.log"
COMPILE_LOG_PATH = (
    REPO_ROOT
    / "12_tooling_runtime_archive"
    / "batch_02_mt_indicator_family"
    / "metaeditor_compile_MT5BarExportProbe.log"
)
MQ5_PATH = (
    REPO_ROOT
    / "12_tooling_runtime_archive"
    / "batch_02_mt_indicator_family"
    / "MT5BarExportProbe.mq5"
)
INI_PATH = (
    REPO_ROOT
    / "12_tooling_runtime_archive"
    / "batch_02_mt_indicator_family"
    / "MT5BarExportProbe.ini"
)
RUN_PS1_PATH = (
    REPO_ROOT
    / "02_runtime"
    / "mt_indicator_probes"
    / "batch_01_volty_xbreaking"
    / "run_mt5_bar_export_once.ps1"
)

OUTPUT_MD_PATH = RUNTIME_DIR / "n02_second_fx_subhour_terminal_export_insufficient_summary_v1.md"
OUTPUT_JSON_PATH = RUNTIME_DIR / "n02_second_fx_subhour_terminal_export_insufficient_summary_v1.json"

_DONE_RE = re.compile(
    r"MT5BarExportProbe: DONE file=(?P<file>\S+) copied=(?P<copied>\d+) bars=(?P<bars>\d+) export_tf=(?P<export_tf>\S+) chart_tf=(?P<chart_tf>\S+)"
)
_GENERATED_RE = re.compile(r": (?P<ticks>\d+) ticks, (?P<bars_generated>\d+) bars generated\.")
_INPUT_RE = re.compile(r"InpExportTf=(?P<value>\d+)")
_ONDEINIT_RE = re.compile(r"MT5BarExportProbe: OnDeinit reason=(?P<reason>\d+)")


def load_json(path: Path) -> Dict[str, object]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_tab_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def parse_bar_dt(row: Dict[str, str]) -> datetime:
    return datetime.strptime(
        "{0} {1}".format(row["Date"].strip(), row["Time"].strip()),
        "%Y.%m.%d %H:%M",
    ).replace(tzinfo=timezone.utc)


def parse_tester_log(path: Path, from_date: str, to_date: str) -> Dict[str, object]:
    lines = path.read_text(encoding="utf-16").splitlines()
    marker = "testing of Experts\\MT5BarExportProbe.ex5 from {0} 00:00 to {1} 00:00".format(from_date, to_date)
    start_idx: Optional[int] = None
    for idx, line in enumerate(lines):
        if marker in line:
            start_idx = idx
    if start_idx is None:
        raise RuntimeError("tester log block not found: {0}".format(marker))

    block = lines[start_idx : min(len(lines), start_idx + 32)]
    done_match = None
    generated_match = None
    input_match = None
    ondeinit_match = None
    for line in block:
        if input_match is None:
            input_match = _INPUT_RE.search(line)
        if ondeinit_match is None:
            ondeinit_match = _ONDEINIT_RE.search(line)
        if done_match is None:
            done_match = _DONE_RE.search(line)
        if generated_match is None:
            generated_match = _GENERATED_RE.search(line)

    if done_match is None:
        raise RuntimeError("MT5BarExportProbe DONE line not found in tester block")
    if generated_match is None:
        raise RuntimeError("bars generated line not found in tester block")

    return {
        "block_marker": marker,
        "input_export_tf_value": int(input_match.group("value")) if input_match else None,
        "ondeinit_reason": int(ondeinit_match.group("reason")) if ondeinit_match else None,
        "done_file_name": done_match.group("file"),
        "copied_bars": int(done_match.group("copied")),
        "bars_value": int(done_match.group("bars")),
        "export_tf": done_match.group("export_tf"),
        "chart_tf": done_match.group("chart_tf"),
        "ticks_generated": int(generated_match.group("ticks")),
        "bars_generated": int(generated_match.group("bars_generated")),
    }


def analyze_csv(path: Path) -> Dict[str, object]:
    rows = read_tab_csv(path)
    dts = [parse_bar_dt(row) for row in rows]
    step_counter: Counter[int] = Counter()
    for idx in range(len(dts) - 1):
        step_minutes = int(abs((dts[idx] - dts[idx + 1]).total_seconds()) // 60)
        step_counter[step_minutes] += 1

    minute_components = sorted({dt.strftime("%M") for dt in dts})
    return {
        "csv_path": str(path),
        "row_count": len(rows),
        "line_count": len(rows) + 1,
        "latest_bar_time_utc": dts[0].strftime("%Y-%m-%dT%H:%M:%SZ"),
        "earliest_bar_time_utc": dts[-1].strftime("%Y-%m-%dT%H:%M:%SZ"),
        "step_minutes_histogram": {str(k): v for k, v in sorted(step_counter.items())},
        "unique_minute_components": minute_components,
        "has_subhour_minute_component": any(component != "00" for component in minute_components),
        "has_15m_spacing": "15" in {str(k) for k in step_counter.keys()},
        "has_hourly_spacing": "60" in {str(k) for k in step_counter.keys()},
    }


def build_summary() -> Dict[str, object]:
    run_summary = load_json(RUN_SUMMARY_PATH)
    csv_source = Path(str(run_summary["files"]["csv"]["source"]))
    csv_analysis = analyze_csv(csv_source)
    tester_observation = parse_tester_log(
        TESTER_LOG_PATH,
        from_date=str(run_summary["from_date"]),
        to_date=str(run_summary["to_date"]),
    )

    has_subhour_output = bool(csv_analysis["has_subhour_minute_component"]) or bool(csv_analysis["has_15m_spacing"])
    status = "terminal_export_completed_but_subhour_not_observed"
    if has_subhour_output:
        status = "terminal_export_subhour_observed"

    return {
        "producer": "n02_second_fx_subhour_terminal_export_insufficient_build_v1.py",
        "scope": "REOPEN_B9_N02_SECOND_FX_SUBHOUR_TERMINAL_EXPORT_INSUFFICIENT_P0",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "inputs": {
            "archive_root": str(ARCHIVE_ROOT),
            "run_summary_json": str(RUN_SUMMARY_PATH),
            "tester_log": str(TESTER_LOG_PATH),
            "compile_log": str(COMPILE_LOG_PATH),
            "mq5": str(MQ5_PATH),
            "ini": str(INI_PATH),
            "run_ps1": str(RUN_PS1_PATH),
        },
        "output_paths": {
            "summary_md": str(OUTPUT_MD_PATH),
            "summary_json": str(OUTPUT_JSON_PATH),
        },
        "terminal_export_run": {
            "archive_tag": run_summary["archive_tag"],
            "environment_label": run_summary["environment"]["environment_label"],
            "chart_period": run_summary["chart_period"],
            "from_date": run_summary["from_date"],
            "to_date": run_summary["to_date"],
            "process_exited": run_summary["process_exited"],
            "report_fallback_attempted": run_summary["report_fallback_attempted"],
            "runtime_set_write_mode": run_summary.get("runtime_set_write_mode", ""),
        },
        "tester_observation": tester_observation,
        "csv_analysis": csv_analysis,
        "gate": {
            "status": status,
            "terminal_export_run_succeeded": bool(run_summary["process_exited"]),
            "requested_symbol": "GBPUSD",
            "requested_timeframe": "M15",
            "do_not_ingest_current_export": not has_subhour_output,
            "observed_subhour_output": has_subhour_output,
            "observed_output_is_hourly_only": bool(csv_analysis["has_hourly_spacing"]) and not has_subhour_output,
            "preferred_next_step": "build_or_reuse_hcc_reader_then_convert_to_canonical_bars",
            "blocked_reason": "terminal_export_csv_for_requested_m15_still_contains_hourly_only_timestamps",
            "writes_main_m1_runtime": False,
            "is_acquisition_only": True,
            "declares_canonical_export_done": False,
        },
    }


def render_md(summary: Dict[str, object]) -> str:
    gate = summary["gate"]
    run_info = summary["terminal_export_run"]
    tester = summary["tester_observation"]
    csv_analysis = summary["csv_analysis"]
    lines = [
        "# n02_second_fx_subhour_terminal_export_insufficient_summary v1",
        "",
        "## 目的",
        "",
        "- 对 `TradeMaxGlobal-Demo__60088394` 的 `GBPUSD/M15 terminal export` 做真实结果收口。",
        "- 明确当前 terminal export 是否已经足够进入 `n02_mt5_export_ingest_v1.py`。",
        "",
        "## 2026-07-05 fresh-run 结论",
        "",
        "- `status`: `{0}`".format(gate["status"]),
        "- `environment_label`: `{0}`".format(run_info["environment_label"]),
        "- `requested_symbol_timeframe`: `GBPUSD/M15`",
        "- `process_exited`: `{0}`".format(str(run_info["process_exited"]).lower()),
        "- `report_fallback_attempted`: `{0}`".format(str(run_info["report_fallback_attempted"]).lower()),
        "- `input_export_tf_value`: `{0}`".format(tester["input_export_tf_value"]),
        "- `tester_chart_tf`: `{0}`".format(tester["chart_tf"]),
        "- `tester_export_tf`: `{0}`".format(tester["export_tf"]),
        "- `tester_bars_generated`: `{0}`".format(tester["bars_generated"]),
        "- `csv_row_count`: `{0}`".format(csv_analysis["row_count"]),
        "- `csv_latest_bar_time_utc`: `{0}`".format(csv_analysis["latest_bar_time_utc"]),
        "- `csv_earliest_bar_time_utc`: `{0}`".format(csv_analysis["earliest_bar_time_utc"]),
        "- `csv_step_minutes_histogram`: `{0}`".format(json.dumps(csv_analysis["step_minutes_histogram"], ensure_ascii=True)),
        "- `csv_unique_minute_components`: `{0}`".format(json.dumps(csv_analysis["unique_minute_components"], ensure_ascii=True)),
        "- `observed_subhour_output`: `{0}`".format(str(gate["observed_subhour_output"]).lower()),
        "- `do_not_ingest_current_export`: `{0}`".format(str(gate["do_not_ingest_current_export"]).lower()),
        "",
        "## 当前裁决",
        "",
        "- 当前 terminal export 已真实跑通，并已归档 `csv / tester_log / terminal_log / report / runtime_set / runtime_ini`。",
        "- 但导出的 `GBPUSD/M15` csv 仍只出现整点时间戳，未观察到 `:15/:30/:45` 子小时时间点。",
        "- 因此当前不能把该 csv 直接送入 `n02_mt5_export_ingest_v1.py` 作为 `GBPUSD/M15` canonical bars。",
        "- 主线下一步从 `terminal export -> ingest` 收紧为：`build_or_reuse_hcc_reader_then_convert_to_canonical_bars`。",
        "",
        "## provenance",
        "",
        "- `archive_root`: `{0}`".format(summary["inputs"]["archive_root"]),
        "- `run_summary_json`: `{0}`".format(summary["inputs"]["run_summary_json"]),
        "- `tester_log`: `{0}`".format(summary["inputs"]["tester_log"]),
        "- `mq5`: `{0}`".format(summary["inputs"]["mq5"]),
        "- `run_ps1`: `{0}`".format(summary["inputs"]["run_ps1"]),
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    summary = build_summary()
    OUTPUT_MD_PATH.write_text(render_md(summary), encoding="utf-8")
    OUTPUT_JSON_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("status={0}".format(summary["gate"]["status"]))
    print("csv_row_count={0}".format(summary["csv_analysis"]["row_count"]))
    print("observed_subhour_output={0}".format(str(summary["gate"]["observed_subhour_output"]).lower()))
    print("preferred_next_step={0}".format(summary["gate"]["preferred_next_step"]))


if __name__ == "__main__":
    main()
