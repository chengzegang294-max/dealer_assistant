from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence


BATCH_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BATCH_DIR.parents[2]
ARCHIVE_ROOT = BATCH_DIR / "artifacts" / "purchased_csv_contract_preview"
INDEX_PATH = ARCHIVE_ROOT / "purchased_csv_contract_preview_index_latest.json"
ACCEPTANCE_DIR = BATCH_DIR / "acceptance_snapshots"
ACCEPTANCE_PATH = ACCEPTANCE_DIR / "purchased_csv_contract_preview_acceptance_latest.json"


@dataclass(frozen=True)
class ArchiveCheck:
    archive_tag: str
    archive_dir: str
    ok: bool
    issues: List[str]


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def check_archive(archive_dir: Path) -> ArchiveCheck:
    issues: List[str] = []
    run_summary_path = archive_dir / "run_summary.json"
    ingest_manifest_path = archive_dir / "ingest_manifest.json"
    normalized_dir = archive_dir / "normalized"

    if not run_summary_path.exists():
        issues.append("missing run_summary.json")
    if not ingest_manifest_path.exists():
        issues.append("missing ingest_manifest.json")
    if not normalized_dir.exists():
        issues.append("missing normalized/ directory")

    archive_tag = archive_dir.name
    expected = None
    if run_summary_path.exists():
        run_summary = read_json(run_summary_path)
        archive_tag = str(run_summary.get("archive_tag", archive_tag))
        expected = run_summary.get("sample_count")

    if expected is not None and normalized_dir.exists():
        csv_count = len(list(normalized_dir.glob("*__normalized.csv")))
        if isinstance(expected, int) and csv_count != expected:
            issues.append(f"normalized csv count mismatch: expected={expected} got={csv_count}")

    return ArchiveCheck(
        archive_tag=archive_tag,
        archive_dir=str(archive_dir),
        ok=len(issues) == 0,
        issues=issues,
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", default=str(INDEX_PATH))
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json-only", action="store_true")
    args = parser.parse_args(argv)

    index_path = Path(args.index)
    if not index_path.is_absolute():
        index_path = PROJECT_ROOT / index_path

    if not index_path.exists():
        raise FileNotFoundError(f"index not found: {index_path}")

    index_payload = read_json(index_path)
    archives = index_payload.get("archives") or []

    checks: List[ArchiveCheck] = []
    for item in archives:
        archive_dir = Path(str(item.get("archive_dir", "")))
        if not archive_dir.exists():
            checks.append(
                ArchiveCheck(
                    archive_tag=str(item.get("archive_tag", "")),
                    archive_dir=str(archive_dir),
                    ok=False,
                    issues=["archive directory missing"],
                )
            )
            continue
        checks.append(check_archive(archive_dir))

    next_actions: List[str] = []
    for c in checks:
        if not c.ok:
            next_actions.append(f"fix purchased contract preview archive {c.archive_tag}: {', '.join(c.issues)}")

    payload = {
        "format": "purchased_csv_contract_preview_acceptance_v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "index_path": str(index_path),
        "archive_count": index_payload.get("archive_count"),
        "latest_archive_tag": index_payload.get("latest_archive_tag"),
        "latest_archive_generated_at": index_payload.get("latest_archive_generated_at"),
        "checks": [c.__dict__ for c in checks],
        "next_actions": next_actions,
    }

    if args.write_json:
        write_json(ACCEPTANCE_PATH, payload)

    if args.json_only or not args.write_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"acceptance={ACCEPTANCE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

