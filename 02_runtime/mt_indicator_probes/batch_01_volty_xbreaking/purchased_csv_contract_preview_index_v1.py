from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence


BATCH_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BATCH_DIR.parents[2]
DEFAULT_ARCHIVE_ROOT = BATCH_DIR / "artifacts" / "purchased_csv_contract_preview"
DEFAULT_INDEX_PATH = DEFAULT_ARCHIVE_ROOT / "purchased_csv_contract_preview_index_latest.json"


@dataclass(frozen=True)
class ArchiveSummary:
    archive_tag: str
    archive_dir: str
    generated_at: Optional[str]
    sample_count: Optional[int]
    error_count: Optional[int]
    normalized_dir: Optional[str]


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_ts(value: Optional[str]) -> str:
    if not value:
        return "0000-00-00T00:00:00"
    return value


def build_index(archive_root: Path) -> Dict[str, Any]:
    archive_summaries: List[ArchiveSummary] = []

    for child in sorted(archive_root.glob("*")):
        if not child.is_dir():
            continue
        run_summary_path = child / "run_summary.json"
        if not run_summary_path.exists():
            continue
        run_summary = read_json(run_summary_path)
        archive_summaries.append(
            ArchiveSummary(
                archive_tag=str(run_summary.get("archive_tag", child.name)),
                archive_dir=str(child),
                generated_at=run_summary.get("generated_at"),
                sample_count=run_summary.get("sample_count"),
                error_count=run_summary.get("error_count"),
                normalized_dir=run_summary.get("normalized_output_dir"),
            )
        )

    latest = None
    if archive_summaries:
        latest = max(archive_summaries, key=lambda x: normalize_ts(x.generated_at))

    return {
        "format": "purchased_csv_contract_preview_index_v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "archive_root": str(archive_root),
        "archive_count": len(archive_summaries),
        "latest_archive_tag": latest.archive_tag if latest else None,
        "latest_archive_generated_at": latest.generated_at if latest else None,
        "archives": [a.__dict__ for a in archive_summaries],
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-root", default=str(DEFAULT_ARCHIVE_ROOT))
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json-only", action="store_true")
    args = parser.parse_args(argv)

    archive_root = Path(args.archive_root)
    if not archive_root.is_absolute():
        archive_root = PROJECT_ROOT / archive_root

    payload = build_index(archive_root)
    if args.write_json:
        write_json(DEFAULT_INDEX_PATH, payload)

    if args.json_only or not args.write_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"index={DEFAULT_INDEX_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

