import argparse
import csv
import hashlib
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class Stat:
    selected: int
    copied: int
    skipped_exists_same_sha: int
    conflicts: int
    missing_source: int
    total_bytes_copied: int


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", required=True)
    p.add_argument("--ledger-tsv", required=True)
    p.add_argument("--gaps-tsv", default="")
    p.add_argument("--incoming-root-rel", required=True)
    p.add_argument("--mirror-root-rel", required=True)
    p.add_argument("--incoming-prefix", default="")
    p.add_argument("--mirror-prefix", default="")
    p.add_argument("--out-manifest", required=True)
    p.add_argument("--out-report", required=True)
    p.add_argument("--conflict-dir-rel", required=True)
    p.add_argument("--hash-limit-bytes", type=int, default=300 * 1024 * 1024)
    return p.parse_args()


def norm_posix(text: str) -> str:
    return text.replace("\\", "/").lstrip("/")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def safe_rel_under(root: Path, target: Path) -> str:
    return str(target.relative_to(root)).replace("\\", "/")


def main() -> None:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    ledger_path = (repo_root / Path(args.ledger_tsv)).resolve()
    gaps_path = (repo_root / Path(args.gaps_tsv)).resolve() if str(args.gaps_tsv).strip() else None
    incoming_root = (repo_root / Path(args.incoming_root_rel)).resolve()
    mirror_root = (repo_root / Path(args.mirror_root_rel)).resolve()
    out_manifest = (repo_root / Path(args.out_manifest)).resolve()
    out_report = (repo_root / Path(args.out_report)).resolve()
    conflict_dir = (repo_root / Path(args.conflict_dir_rel)).resolve()

    incoming_root_rel = norm_posix(args.incoming_root_rel).rstrip("/") + "/"
    incoming_prefix_raw = norm_posix(args.incoming_prefix).strip("/")
    mirror_prefix_raw = norm_posix(args.mirror_prefix).strip("/")
    incoming_prefix = incoming_prefix_raw + "/" if incoming_prefix_raw else ""
    mirror_prefix = mirror_prefix_raw + "/" if mirror_prefix_raw else ""
    hash_limit = int(args.hash_limit_bytes)
    incoming_prefix_dir = Path(incoming_prefix_raw) if incoming_prefix_raw else Path(".")

    only_lifted_set: set[str] | None = None
    if gaps_path:
        lifted: set[str] = set()
        with gaps_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for row in reader:
                rel = (row.get("lifted_rel_path") or "").strip()
                if rel:
                    lifted.add(rel)
        only_lifted_set = lifted

    mirror_root.mkdir(parents=True, exist_ok=True)
    conflict_dir.mkdir(parents=True, exist_ok=True)
    out_manifest.parent.mkdir(parents=True, exist_ok=True)

    stat = Stat(
        selected=0,
        copied=0,
        skipped_exists_same_sha=0,
        conflicts=0,
        missing_source=0,
        total_bytes_copied=0,
    )

    rows: list[dict[str, str]] = []
    with ledger_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for raw in reader:
            if (raw.get("decision") or "").strip() != "PROMOTE_INCOMING_TO_MIRROR__NEEDS_RULES":
                continue
            if only_lifted_set is not None:
                lifted_rel = (raw.get("lifted_rel_path") or "").strip()
                if not lifted_rel or lifted_rel not in only_lifted_set:
                    continue
            incoming_rel = norm_posix((raw.get("incoming_rel_path") or "").strip())
            if not incoming_rel:
                continue
            match_rel = incoming_rel
            if incoming_root_rel and match_rel.startswith(incoming_root_rel):
                match_rel = match_rel.split(incoming_root_rel, 1)[1]
            if incoming_prefix and not match_rel.startswith(incoming_prefix):
                continue

            rest = match_rel.split(incoming_prefix, 1)[1] if incoming_prefix else match_rel
            mirror_rel = mirror_prefix + rest
            src = incoming_root / incoming_prefix_dir / Path(rest)
            dst = mirror_root / Path(mirror_rel)

            stat = Stat(
                selected=stat.selected + 1,
                copied=stat.copied,
                skipped_exists_same_sha=stat.skipped_exists_same_sha,
                conflicts=stat.conflicts,
                missing_source=stat.missing_source,
                total_bytes_copied=stat.total_bytes_copied,
            )

            if not src.exists() or not src.is_file():
                rows.append(
                    {
                        "incoming_rel_path": incoming_rel,
                        "mirror_rel_path": mirror_rel,
                        "action": "MISSING_SOURCE",
                    }
                )
                stat = Stat(
                    selected=stat.selected,
                    copied=stat.copied,
                    skipped_exists_same_sha=stat.skipped_exists_same_sha,
                    conflicts=stat.conflicts,
                    missing_source=stat.missing_source + 1,
                    total_bytes_copied=stat.total_bytes_copied,
                )
                continue

            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                if int(dst.stat().st_size) <= hash_limit and int(src.stat().st_size) <= hash_limit:
                    src_sha = sha256_file(src)
                    dst_sha = sha256_file(dst)
                    if src_sha == dst_sha:
                        rows.append(
                            {
                                "incoming_rel_path": incoming_rel,
                                "mirror_rel_path": mirror_rel,
                                "action": "SKIP_EXISTS_SAME_SHA",
                            }
                        )
                        stat = Stat(
                            selected=stat.selected,
                            copied=stat.copied,
                            skipped_exists_same_sha=stat.skipped_exists_same_sha + 1,
                            conflicts=stat.conflicts,
                            missing_source=stat.missing_source,
                            total_bytes_copied=stat.total_bytes_copied,
                        )
                        continue
                conflict_path = conflict_dir / Path(mirror_rel)
                conflict_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, conflict_path)
                rows.append(
                    {
                        "incoming_rel_path": incoming_rel,
                        "mirror_rel_path": mirror_rel,
                        "action": "CONFLICT_COPIED_TO_CONFLICT_DIR",
                        "conflict_rel_path": safe_rel_under(conflict_dir, conflict_path),
                    }
                )
                stat = Stat(
                    selected=stat.selected,
                    copied=stat.copied,
                    skipped_exists_same_sha=stat.skipped_exists_same_sha,
                    conflicts=stat.conflicts + 1,
                    missing_source=stat.missing_source,
                    total_bytes_copied=stat.total_bytes_copied,
                )
                continue

            shutil.copy2(src, dst)
            rows.append(
                {
                    "incoming_rel_path": incoming_rel,
                    "mirror_rel_path": mirror_rel,
                    "action": "COPIED",
                }
            )
            stat = Stat(
                selected=stat.selected,
                copied=stat.copied + 1,
                skipped_exists_same_sha=stat.skipped_exists_same_sha,
                conflicts=stat.conflicts,
                missing_source=stat.missing_source,
                total_bytes_copied=stat.total_bytes_copied + int(src.stat().st_size),
            )

    with out_manifest.open("w", encoding="utf-8", newline="\n") as handle:
        fieldnames = ["incoming_rel_path", "mirror_rel_path", "action", "conflict_rel_path"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})

    payload = {
        "format": "promote_incoming_prefix_v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(repo_root),
        "ledger_tsv": str(ledger_path),
        "gaps_tsv": str(gaps_path) if gaps_path else "",
        "incoming_root": str(incoming_root),
        "mirror_root": str(mirror_root),
        "incoming_prefix": incoming_prefix,
        "mirror_prefix": mirror_prefix,
        "manifest_path": str(out_manifest),
        "conflict_dir": str(conflict_dir),
        "hash_limit_bytes": hash_limit,
        "stat": asdict(stat),
    }
    out_report.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
