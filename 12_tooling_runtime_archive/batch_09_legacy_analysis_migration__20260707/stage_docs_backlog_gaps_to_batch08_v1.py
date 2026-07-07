import argparse
import csv
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class Stat:
    copied: int
    skipped_exists: int
    missing_source: int


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", required=True)
    p.add_argument("--lifted-root-rel", required=True)
    p.add_argument("--gaps-tsv", required=True)
    p.add_argument("--batch08-root-rel", required=True)
    p.add_argument("--out-report", required=True)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    lifted_root = (repo_root / Path(args.lifted_root_rel)).resolve()
    gaps_path = (repo_root / Path(args.gaps_tsv)).resolve()
    batch08_root = (repo_root / Path(args.batch08_root_rel)).resolve()
    out_report = (repo_root / Path(args.out_report)).resolve()

    stat = Stat(copied=0, skipped_exists=0, missing_source=0)
    target_root = batch08_root / "legacy_docs_backlog"
    target_root.mkdir(parents=True, exist_ok=True)

    with gaps_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            if (row.get("category") or "").strip() != "docs_backlog_or_other":
                continue
            lifted_rel = (row.get("lifted_rel_path") or "").strip().replace("\\", "/")
            if not lifted_rel.startswith("docs/"):
                continue
            rest = lifted_rel.split("docs/", 1)[1]
            src = lifted_root / Path(lifted_rel)
            dst = target_root / Path(rest)
            if dst.exists():
                stat = Stat(
                    copied=stat.copied,
                    skipped_exists=stat.skipped_exists + 1,
                    missing_source=stat.missing_source,
                )
                continue
            if not src.exists() or not src.is_file():
                stat = Stat(
                    copied=stat.copied,
                    skipped_exists=stat.skipped_exists,
                    missing_source=stat.missing_source + 1,
                )
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            stat = Stat(
                copied=stat.copied + 1,
                skipped_exists=stat.skipped_exists,
                missing_source=stat.missing_source,
            )

    payload = {
        "format": "stage_docs_backlog_gaps_to_batch08_v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(repo_root),
        "lifted_root": str(lifted_root),
        "gaps_tsv": str(gaps_path),
        "batch08_root": str(batch08_root),
        "stat": asdict(stat),
    }
    out_report.parent.mkdir(parents=True, exist_ok=True)
    out_report.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

