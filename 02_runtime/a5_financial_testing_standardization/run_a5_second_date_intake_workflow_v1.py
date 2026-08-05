from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_python(script: Path, *args: str, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        check=True,
        text=True,
        capture_output=capture_output,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the A5 second-date intake workflow end to end.")
    parser.add_argument("--batch-root", required=True)
    parser.add_argument("--sample-date", required=True)
    parser.add_argument("--source-family", required=True)
    parser.add_argument("--sample-plan", required=True)
    parser.add_argument("--gate-plan", required=True)
    parser.add_argument("--gate-id", required=True, default="A5_FIN_STD_GATE_MIN_TWO_DATES_V1")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--init-batch-if-missing", action="store_true")
    args = parser.parse_args()

    cwd = Path.cwd()
    runtime_root = cwd / "02_runtime" / "a5_financial_testing_standardization"
    batch_root = Path(args.batch_root).resolve()
    sample_date = args.sample_date.strip()
    source_family = args.source_family.strip()
    sample_plan = Path(args.sample_plan).resolve()
    gate_plan = Path(args.gate_plan).resolve()
    output_json = Path(args.output_json).resolve()

    init_script = runtime_root / "init_a5_second_date_batch_scaffold_v1.py"
    finalize_script = runtime_root / "finalize_a5_second_date_batch_absorb_v1.py"
    render_script = runtime_root / "render_a5_second_date_plan_row_v1.py"
    upsert_script = runtime_root / "upsert_a5_input_pack_plan_row_v1.py"
    input_pack_script = runtime_root / "run_a5_input_pack_acceptance_v1.py"
    gate_script = runtime_root / "run_a5_multi_pack_gate_acceptance_v1.py"

    workflow_steps: list[dict[str, object]] = []

    if args.init_batch_if_missing and not (batch_root / "manifest_v1.tsv").exists():
        run_python(init_script, "--batch-root", str(batch_root), "--sample-date", sample_date)
        workflow_steps.append({"step": "init_batch_scaffold", "status": "completed"})
    else:
        workflow_steps.append({"step": "init_batch_scaffold", "status": "skipped"})

    absorb_output = runtime_root / "acceptance_outputs" / f"a5_second_date_absorb_summary_{sample_date.replace('-', '')}.json"
    run_python(
        finalize_script,
        "--batch-root",
        str(batch_root),
        "--sample-date",
        sample_date,
        "--output-json",
        str(absorb_output),
    )
    workflow_steps.append({"step": "finalize_absorb", "status": "completed", "output": str(absorb_output)})
    absorb_summary = json.loads(absorb_output.read_text(encoding="utf-8"))

    render_result = run_python(
        render_script,
        "--sample-date",
        sample_date,
        "--source-family",
        source_family,
        "--source-root",
        str(batch_root),
        capture_output=True,
    )
    row_text = render_result.stdout.strip()
    workflow_steps.append({"step": "render_plan_row", "status": "completed"})

    run_python(upsert_script, "--sample-plan", str(sample_plan), "--row-text", row_text)
    workflow_steps.append({"step": "upsert_plan_row", "status": "completed", "sample_plan": str(sample_plan)})

    input_pack_id = f"A5_R2_EASTMONEY_SCREENSHOT_INPUT_PACK_{sample_date}_V1"
    input_pack_output = runtime_root / "acceptance_outputs" / f"a5_input_pack_acceptance_{source_family}_{sample_date.replace('-', '')}.json"
    run_python(
        input_pack_script,
        "--sample-plan",
        str(sample_plan),
        "--input-pack-id",
        input_pack_id,
        "--output-json",
        str(input_pack_output),
    )
    workflow_steps.append({"step": "input_pack_acceptance", "status": "completed", "output": str(input_pack_output)})
    input_pack_summary = json.loads(input_pack_output.read_text(encoding="utf-8"))

    gate_output = runtime_root / "acceptance_outputs" / f"a5_multi_pack_gate_acceptance_{sample_date.replace('-', '')}.json"
    run_python(
        gate_script,
        "--gate-plan",
        str(gate_plan),
        "--gate-id",
        args.gate_id,
        "--output-json",
        str(gate_output),
    )
    workflow_steps.append({"step": "multi_pack_gate", "status": "completed", "output": str(gate_output)})
    gate_summary = json.loads(gate_output.read_text(encoding="utf-8"))

    summary = {
        "workflow_id": "A5_SECOND_DATE_INTAKE_WORKFLOW_V1",
        "sample_date": sample_date,
        "batch_root": str(batch_root),
        "source_family": source_family,
        "steps": workflow_steps,
        "absorb_ready_for_input_pack_acceptance": absorb_summary.get("ready_for_input_pack_acceptance"),
        "input_pack_passed": input_pack_summary.get("passed"),
        "multi_pack_gate_passed": gate_summary.get("passed"),
        "multi_pack_gate_still_need_evidence": gate_summary.get("still_need_evidence", []),
    }
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
