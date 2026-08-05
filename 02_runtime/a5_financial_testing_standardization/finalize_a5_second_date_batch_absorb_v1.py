from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REQUIRED_SCREENSHOT_NAMES = [
    "市场情绪总览.png",
    "市场宽度涨停跌停.png",
    "龙虎榜异动资金.png",
]


def read_tsv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return [dict(row) for row in reader]


def write_tsv_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Finalize second-date batch absorb status and emit absorb summary.")
    parser.add_argument("--batch-root", required=True)
    parser.add_argument("--sample-date", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    batch_root = Path(args.batch_root).resolve()
    sample_date = args.sample_date.strip()
    manifest_path = batch_root / "manifest_v1.tsv"
    screenshot_dir = batch_root / "00_raw_snapshot" / "user_screenshots"

    missing_files: list[str] = []
    absorbed_relative_paths: list[str] = []
    for name in REQUIRED_SCREENSHOT_NAMES:
        rel = f"00_raw_snapshot/user_screenshots/{sample_date}__{name}"
        if not (screenshot_dir / f"{sample_date}__{name}").exists():
            missing_files.append(rel)
        else:
            absorbed_relative_paths.append(rel)

    manifest_updated = False
    if manifest_path.exists():
        rows = read_tsv_rows(manifest_path)
        fieldnames = list(rows[0].keys()) if rows else ["relative_path", "material_type", "sample_date", "status", "source_note"]
        changed = False
        for row in rows:
            rel = str(row.get("relative_path", "")).strip()
            if rel in absorbed_relative_paths:
                if row.get("status") != "absorbed":
                    row["status"] = "absorbed"
                    changed = True
                if row.get("source_note") != "from 暂时存放 吸收":
                    row["source_note"] = "from 暂时存放 吸收"
                    changed = True
        if changed:
            write_tsv_rows(manifest_path, rows, fieldnames)
            manifest_updated = True

    payload = {
        "acceptance_id": "A5_SECOND_DATE_BATCH_ABSORB_FINALIZE_V1",
        "batch_root": str(batch_root),
        "sample_date": sample_date,
        "absorbed_relative_paths": absorbed_relative_paths,
        "missing_files": missing_files,
        "manifest_updated": manifest_updated,
        "ready_for_input_pack_acceptance": len(missing_files) == 0,
    }
    Path(args.output_json).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
