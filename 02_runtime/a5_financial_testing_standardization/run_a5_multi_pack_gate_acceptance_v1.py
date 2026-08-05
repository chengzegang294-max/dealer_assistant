from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def read_tsv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return [dict(row) for row in reader]


def read_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("acceptance output must be a json object")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Gate-check: A5 financial testing standardization requires multiple distinct dates.")
    parser.add_argument("--gate-plan", required=True)
    parser.add_argument("--gate-id", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    gate_rows = read_tsv_rows(Path(args.gate_plan))
    gate_row = next((row for row in gate_rows if row.get("gate_id") == args.gate_id), None)
    if not gate_row:
        raise ValueError(f"gate_id not found: {args.gate_id}")

    min_dates = int(str(gate_row.get("min_distinct_sample_dates", "0")).strip() or "0")
    source_plan_path = Path(str(gate_row.get("source_plan_tsv", "")).strip())
    if not source_plan_path.is_absolute():
        source_plan_path = (Path.cwd() / source_plan_path).resolve()

    source_rows = read_tsv_rows(source_plan_path)
    distinct_dates_passed: set[str] = set()
    pending_input_pack_ids: list[str] = []
    missing_outputs: list[str] = []
    failed_outputs: list[str] = []

    for row in source_rows:
        input_pack_id = str(row.get("input_pack_id", "")).strip()
        sample_date = str(row.get("sample_date", "")).strip()
        output_rel = str(row.get("acceptance_output_json", "")).strip()
        if not input_pack_id:
            continue

        if not output_rel:
            pending_input_pack_ids.append(input_pack_id)
            continue

        output_path = Path(output_rel)
        if not output_path.is_absolute():
            output_path = (Path.cwd() / output_path).resolve()
        if not output_path.exists():
            missing_outputs.append(f"{input_pack_id}::{output_rel}")
            continue

        payload = read_json(output_path)
        if bool(payload.get("passed")) is True and sample_date:
            distinct_dates_passed.add(sample_date)
        else:
            failed_outputs.append(f"{input_pack_id}::{output_rel}")

    passed = len(distinct_dates_passed) >= min_dates and not missing_outputs and not failed_outputs

    out = {
        "acceptance_id": "A5_FIN_STD_MULTI_PACK_GATE_ACCEPTANCE_V1",
        "gate_id": args.gate_id,
        "min_distinct_sample_dates": min_dates,
        "distinct_dates_passed": sorted(distinct_dates_passed),
        "pending_input_pack_ids": pending_input_pack_ids,
        "missing_outputs": missing_outputs,
        "failed_outputs": failed_outputs,
        "passed": passed,
        "still_need_evidence": [] if passed else ["need_second_distinct_sample_date_input_pack"],
    }
    Path(args.output_json).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
