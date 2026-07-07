from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

RUNTIME_DIR = Path(__file__).parent
OR_INPUT_PATH = RUNTIME_DIR / "n02_p0_fields_runtime_gbpusd_m15_candidate_v1.csv"
IB_INPUT_PATH = RUNTIME_DIR / "n02_ib_fields_runtime_gbpusd_m15_candidate_v1.csv"
OR_OUTPUT_PATH = RUNTIME_DIR / "n02_p0_fields_runtime_gbpusd_m15_slice_v1.csv"
IB_OUTPUT_PATH = RUNTIME_DIR / "n02_ib_fields_runtime_gbpusd_m15_slice_v1.csv"
SUMMARY_PATH = RUNTIME_DIR / "n02_gbpusd_m15_candidate_slice_summary_v1.json"


def read_csv(path: Path) -> tuple[List[str], List[Dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fieldnames: List[str], rows: List[Dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def filter_rows(rows: List[Dict[str, str]], symbol: str, timeframe: str) -> List[Dict[str, str]]:
    filtered = [row for row in rows if row.get("symbol") == symbol and row.get("timeframe") == timeframe]
    return sorted(
        filtered,
        key=lambda row: (
            row.get("session_local_date", ""),
            row.get("bar_time", ""),
            row.get("session_id", ""),
            row.get("ib_window_minutes", ""),
            row.get("opening_range_window_minutes", ""),
        ),
    )


def build_summary(
    symbol: str,
    timeframe: str,
    or_input_path: Path,
    ib_input_path: Path,
    or_output_path: Path,
    ib_output_path: Path,
    or_input_rows: List[Dict[str, str]],
    ib_input_rows: List[Dict[str, str]],
    or_output_rows: List[Dict[str, str]],
    ib_output_rows: List[Dict[str, str]],
) -> Dict[str, object]:
    return {
        "producer": "n02_gbpusd_m15_candidate_slice_build_v1.py",
        "scope": "REOPEN_B9_N02_GBPUSD_M15_CANDIDATE_SLICE",
        "status": "fresh_run_candidate_slice_from_mixed_runtime",
        "evidence_mode": "fresh_run_filtered_from_candidate_runtime_copy_plus_append",
        "source_path": {
            "or_candidate_runtime_csv": str(or_input_path),
            "ib_candidate_runtime_csv": str(ib_input_path),
        },
        "repo_path": {
            "or_slice_runtime_csv": str(or_output_path),
            "ib_slice_runtime_csv": str(ib_output_path),
            "summary_json": str(SUMMARY_PATH),
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "boundary": {
            "symbol": symbol,
            "timeframe": timeframe,
            "writes_main_runtime": False,
            "is_slice_only": True,
            "includes_failed_breakout": False,
        },
        "or_input_rows": len(or_input_rows),
        "or_slice_rows": len(or_output_rows),
        "or_defined_rows": sum(1 for row in or_output_rows if row.get("opening_range_defined") == "1"),
        "ib_input_rows": len(ib_input_rows),
        "ib_slice_rows": len(ib_output_rows),
        "ib_defined_rows": sum(1 for row in ib_output_rows if row.get("ib_defined") == "1"),
        "session_ids": sorted({row.get("session_id", "") for row in ib_output_rows if row.get("session_id", "")}),
        "or_date_range": {
            "first_bar_time": or_output_rows[0].get("bar_time", "") if or_output_rows else "",
            "last_bar_time": or_output_rows[-1].get("bar_time", "") if or_output_rows else "",
        },
        "ib_date_range": {
            "first_local_date": ib_output_rows[0].get("session_local_date", "") if ib_output_rows else "",
            "last_local_date": ib_output_rows[-1].get("session_local_date", "") if ib_output_rows else "",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="GBPUSD")
    parser.add_argument("--timeframe", default="M15")
    parser.add_argument("--or-input", default=str(OR_INPUT_PATH))
    parser.add_argument("--ib-input", default=str(IB_INPUT_PATH))
    parser.add_argument("--or-output", default=str(OR_OUTPUT_PATH))
    parser.add_argument("--ib-output", default=str(IB_OUTPUT_PATH))
    parser.add_argument("--summary-json", default=str(SUMMARY_PATH))
    args = parser.parse_args()

    or_input_path = Path(args.or_input)
    ib_input_path = Path(args.ib_input)
    or_output_path = Path(args.or_output)
    ib_output_path = Path(args.ib_output)
    summary_path = Path(args.summary_json)

    or_fieldnames, or_input_rows = read_csv(or_input_path)
    ib_fieldnames, ib_input_rows = read_csv(ib_input_path)
    or_output_rows = filter_rows(or_input_rows, args.symbol, args.timeframe)
    ib_output_rows = filter_rows(ib_input_rows, args.symbol, args.timeframe)

    write_csv(or_output_path, or_fieldnames, or_output_rows)
    write_csv(ib_output_path, ib_fieldnames, ib_output_rows)

    summary = build_summary(
        symbol=args.symbol,
        timeframe=args.timeframe,
        or_input_path=or_input_path,
        ib_input_path=ib_input_path,
        or_output_path=or_output_path,
        ib_output_path=ib_output_path,
        or_input_rows=or_input_rows,
        ib_input_rows=ib_input_rows,
        or_output_rows=or_output_rows,
        ib_output_rows=ib_output_rows,
    )
    summary_path.write_text(json.dumps(summary, ensure_ascii=True, indent=2), encoding="utf-8")

    print("or_input_path={0}".format(or_input_path))
    print("ib_input_path={0}".format(ib_input_path))
    print("or_output_path={0}".format(or_output_path))
    print("ib_output_path={0}".format(ib_output_path))
    print("summary_path={0}".format(summary_path))
    print("or_slice_rows={0}".format(summary["or_slice_rows"]))
    print("or_defined_rows={0}".format(summary["or_defined_rows"]))
    print("ib_slice_rows={0}".format(summary["ib_slice_rows"]))
    print("ib_defined_rows={0}".format(summary["ib_defined_rows"]))


if __name__ == "__main__":
    main()
