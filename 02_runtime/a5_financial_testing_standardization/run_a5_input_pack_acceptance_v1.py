from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def pipe_split(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def read_plan_row(path: Path, input_pack_id: str) -> dict[str, str]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            if row.get("input_pack_id") == input_pack_id:
                return row
    raise ValueError(f"input_pack_id not found in sample plan: {input_pack_id}")


def read_tsv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return [dict(row) for row in reader]


def file_exists(root: Path, relative_path: str) -> bool:
    return (root / relative_path).exists()


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate A5 financial-testing standardization input pack.")
    parser.add_argument("--sample-plan", required=True)
    parser.add_argument("--input-pack-id", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    plan_row = read_plan_row(Path(args.sample_plan), args.input_pack_id)
    source_root = Path(plan_row["source_root"]).resolve()
    required_files = pipe_split(plan_row.get("required_files", ""))
    optional_files = pipe_split(plan_row.get("optional_files", ""))

    checks: list[dict[str, object]] = []

    checks.append(
        {
            "field": "source_root_exists",
            "expected": True,
            "actual": source_root.exists(),
        }
    )

    for rel in ["README.md", "provenance.md", "manifest_v1.tsv"]:
        checks.append(
            {
                "field": f"batch_required_file::{rel}",
                "expected": True,
                "actual": (source_root / rel).exists(),
            }
        )

    required_missing = [rel for rel in required_files if not file_exists(source_root, rel)]
    checks.append(
        {
            "field": "required_files_present",
            "expected": "present",
            "actual": "|".join(required_missing) if required_missing else "present",
        }
    )

    optional_missing = [rel for rel in optional_files if not file_exists(source_root, rel)]
    checks.append(
        {
            "field": "optional_files_present",
            "expected": "allow_missing",
            "actual": "|".join(optional_missing) if optional_missing else "present",
        }
    )

    manifest_present = (source_root / "manifest_v1.tsv").exists()
    if manifest_present:
        manifest_rows = read_tsv_rows(source_root / "manifest_v1.tsv")
        manifest_paths = {str(row.get("relative_path", "")).strip() for row in manifest_rows if row.get("relative_path")}
        manifest_missing = [rel for rel in required_files if rel not in manifest_paths]
        checks.append(
            {
                "field": "manifest_covers_required_files",
                "expected": "covered",
                "actual": "|".join(manifest_missing) if manifest_missing else "covered",
            }
        )
    else:
        checks.append(
            {
                "field": "manifest_covers_required_files",
                "expected": "covered",
                "actual": "manifest_missing",
            }
        )

    passed = all(
        (check["field"] != "source_root_exists" or bool(check["actual"]) is True)
        and (
            not str(check["field"]).startswith("batch_required_file::") or bool(check["actual"]) is True
        )
        and (check["field"] != "required_files_present" or check["actual"] == "present")
        and (check["field"] != "manifest_covers_required_files" or check["actual"] == "covered")
        for check in checks
    )

    out = {
        "acceptance_id": "A5_FIN_STD_INPUT_PACK_ACCEPTANCE_V1",
        "input_pack_id": args.input_pack_id,
        "source_root": str(source_root),
        "checks": checks,
        "passed": passed,
    }
    Path(args.output_json).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
