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
BARS_REPORT_PATH = REAL_INPUT_DIR / "n02_real_input_eurusd_m5_fall_dst_report_v1.json"
OR_PROOF_PATH = REAL_INPUT_DIR / "n02_proof_of_mapping_output_eurusd_m5_fall_dst_v1.csv"
IB_PROOF_PATH = REAL_INPUT_DIR / "n02_ib_proof_of_mapping_output_eurusd_m5_fall_dst_v1.csv"
OUTPUT_MD_PATH = RUNTIME_DIR / "n02_other_timeframe_validation_eurusd_m5_fall_dst_summary_v1.md"
OUTPUT_JSON_PATH = RUNTIME_DIR / "n02_other_timeframe_validation_eurusd_m5_fall_dst_summary_v1.json"


def load_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def summarize_or(rows: List[Dict[str, str]]) -> Dict[str, object]:
    status_counts: Dict[str, int] = defaultdict(int)
    session_counts: Dict[str, int] = defaultdict(int)
    break_direction_counts: Dict[str, int] = defaultdict(int)
    break_mode_counts: Dict[str, int] = defaultdict(int)
    for row in rows:
        defined = row["opening_range_defined"]
        session_id = row["session_id"]
        status_counts[defined] += 1
        session_counts[session_id] += 1
        break_direction_counts[row["first_break_direction"]] += 1
        break_mode_counts[row["first_break_mode"]] += 1
    return {
        "rows": len(rows),
        "defined_rows": int(status_counts.get("1", 0)),
        "undefined_rows": int(status_counts.get("0", 0)),
        "defined_ratio": float(status_counts.get("1", 0)) / len(rows) if rows else 0.0,
        "by_session": dict(sorted(session_counts.items())),
        "first_break_direction_counts": dict(sorted(break_direction_counts.items())),
        "first_break_mode_counts": dict(sorted(break_mode_counts.items())),
    }


def summarize_ib(rows: List[Dict[str, str]]) -> Dict[str, object]:
    status_counts: Dict[str, int] = defaultdict(int)
    session_counts: Dict[str, int] = defaultdict(int)
    for row in rows:
        defined = row["ib_defined"]
        session_id = row["session_id"]
        status_counts[defined] += 1
        session_counts[session_id] += 1
    return {
        "rows": len(rows),
        "defined_rows": int(status_counts.get("1", 0)),
        "undefined_rows": int(status_counts.get("0", 0)),
        "defined_ratio": float(status_counts.get("1", 0)) / len(rows) if rows else 0.0,
        "by_session": dict(sorted(session_counts.items())),
    }


def build_summary(
    bars_report: Dict[str, object],
    or_summary: Dict[str, object],
    ib_summary: Dict[str, object],
    output_md_path: Path,
    output_json_path: Path,
) -> Dict[str, object]:
    return {
        "producer": "n02_other_timeframe_validation_eurusd_m5_fall_dst_build_v1.py",
        "scope": "REOPEN_B9_N02_OTHER_TIMEFRAME_VALIDATION_EURUSD_M5_FALL_DST_P0",
        "status": "fresh_run_validation_summary",
        "evidence_mode": "fresh_run_validation_without_polluting_main_m1_runtime",
        "source_path": {
            "bars_report_json": str(BARS_REPORT_PATH),
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
        "bars_report": bars_report,
        "or_validation": or_summary,
        "ib_validation": ib_summary,
    }


def render_md(summary: Dict[str, object]) -> str:
    bars_report = summary["bars_report"]
    or_validation = summary["or_validation"]
    ib_validation = summary["ib_validation"]
    lines = [
        "# n02_other_timeframe_validation_eurusd_m5_fall_dst_summary v1",
        "",
        "## 作用",
        "",
        "- 对 `EURUSD / M5 / fall DST sample` 做最小 OR/IB 口径验证。",
        "- 当前只验证 `other timeframe` 可跑性，不写回主 `M1` runtime，不升级成行为标签。",
        "",
        "## 2026-07-04 fresh-run",
        "",
        "- bars 行数：`{0}`".format(bars_report["output_rows"]),
        "- bars 时间范围：`{0}` -> `{1}`".format(bars_report["output_first_bar_time"], bars_report["output_last_bar_time"]),
        "- OR proof 行数：`{0}`".format(or_validation["rows"]),
        "- OR defined：`{0}` / `{1}`".format(or_validation["defined_rows"], or_validation["rows"]),
        "- OR first_break_direction：`{0}`".format(json.dumps(or_validation["first_break_direction_counts"], ensure_ascii=True)),
        "- OR first_break_mode：`{0}`".format(json.dumps(or_validation["first_break_mode_counts"], ensure_ascii=True)),
        "- IB proof 行数：`{0}`".format(ib_validation["rows"]),
        "- IB defined：`{0}` / `{1}`".format(ib_validation["defined_rows"], ib_validation["rows"]),
        "",
        "## 当前裁决",
        "",
        "- `EURUSD/M5` 秋季 DST 样本已能独立跑通 OR/IB proof。",
        "- OR proof 当前 `10/15` 行已定义，`5/15` 行未定义；IB proof 当前 `10/10` 行已定义。",
        "- 当前验证层只说明 `other timeframe` 可跑性，不把 `M5` 混入主 `M1` 行为链。",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bars-report", default=str(BARS_REPORT_PATH))
    parser.add_argument("--or-proof", default=str(OR_PROOF_PATH))
    parser.add_argument("--ib-proof", default=str(IB_PROOF_PATH))
    parser.add_argument("--output-md", default=str(OUTPUT_MD_PATH))
    parser.add_argument("--output-json", default=str(OUTPUT_JSON_PATH))
    args = parser.parse_args()

    bars_report = load_json(Path(args.bars_report))
    or_rows = read_rows(Path(args.or_proof))
    ib_rows = read_rows(Path(args.ib_proof))
    summary = build_summary(
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
    print("bars_rows={0}".format(bars_report["output_rows"]))
    print("or_rows={0}".format(summary["or_validation"]["rows"]))
    print("or_defined_rows={0}".format(summary["or_validation"]["defined_rows"]))
    print("ib_rows={0}".format(summary["ib_validation"]["rows"]))
    print("ib_defined_rows={0}".format(summary["ib_validation"]["defined_rows"]))


if __name__ == "__main__":
    main()
