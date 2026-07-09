from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def run_python(script: Path, args: list[str], cwd: Path) -> None:
    cmd = [sys.executable, str(script), *args]
    subprocess.run(cmd, cwd=cwd, check=True)


def runtime_relative_to_repo(path_value: str) -> str:
    return str(Path("02_runtime/butler_r0_ohlcv_object_cards") / path_value).replace("\\", "/")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run registry_v0 minimal + acceptance across multiple sample-plan rows.")
    parser.add_argument("--sample-plan", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--summary-json", required=True)
    parser.add_argument("--status-filter", default="multi_registry_ready")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    runtime_dir = Path(__file__).resolve().parent
    sample_plan = Path(args.sample_plan)
    output_dir = Path(args.output_dir)
    summary_path = Path(args.summary_json)
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    registry_runner = runtime_dir / "run_registry_v0_minimal.py"
    acceptance_runner = runtime_dir / "run_registry_v0_acceptance_v1.py"

    rows = [row for row in read_rows(sample_plan) if row.get("status") == args.status_filter]
    batch_rows: list[dict[str, object]] = []
    for row in rows:
        registry_id = row["registry_id"]
        output_json = output_dir / f"{registry_id}_output.json"
        acceptance_json = output_dir / f"{registry_id}_acceptance.json"
        run_python(
            registry_runner,
            [
                "--registry-id",
                registry_id,
                "--input-csv",
                runtime_relative_to_repo(row["primary_daily_sample"]),
                "--market-proxy-csv",
                runtime_relative_to_repo(row["market_proxy_daily_sample"]),
                "--output-json",
                str(output_json),
            ],
            repo_root,
        )
        run_python(
            acceptance_runner,
            [
                "--sample-plan",
                str(sample_plan),
                "--input-json",
                str(output_json),
                "--output-json",
                str(acceptance_json),
            ],
            repo_root,
        )
        acceptance_payload = json.loads(acceptance_json.read_text(encoding="utf-8"))
        batch_rows.append(
            {
                "registry_id": registry_id,
                "primary_symbol": row["primary_symbol"],
                "market_proxy_symbol": row["market_proxy_symbol"],
                "output_json": str(output_json).replace("\\", "/"),
                "acceptance_json": str(acceptance_json).replace("\\", "/"),
                "acceptance_status": acceptance_payload["acceptance_status"],
                "final_signal": acceptance_payload["summary_snapshot"]["final_signal"],
                "trade_gate": acceptance_payload["summary_snapshot"]["trade_gate"],
                "blockers": acceptance_payload["summary_snapshot"]["blockers"],
            }
        )

    failed = [row["registry_id"] for row in batch_rows if row["acceptance_status"] != "pass"]
    summary = {
        "sample_plan": str(sample_plan).replace("\\", "/"),
        "status_filter": args.status_filter,
        "batch_count": len(batch_rows),
        "pass_count": sum(1 for row in batch_rows if row["acceptance_status"] == "pass"),
        "fail_count": len(failed),
        "failed_registry_ids": failed,
        "batch_rows": batch_rows,
        "batch_status": "pass" if not failed else "fail",
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
