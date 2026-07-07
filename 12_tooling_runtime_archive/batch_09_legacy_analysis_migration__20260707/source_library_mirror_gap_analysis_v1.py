import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class Gap:
    lifted_rel_path: str
    proposed_target_rel_path: str
    size_bytes: int
    sha256: str


@dataclass(frozen=True)
class MatchRow:
    lifted_rel_path: str
    proposed_target_rel_path: str
    basename: str
    candidate_count: int
    candidate_paths: str
    size_bytes: int
    sha256: str


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", required=True)
    p.add_argument("--gaps-tsv", required=True)
    p.add_argument("--out-tsv", required=True)
    p.add_argument("--out-summary", required=True)
    p.add_argument(
        "--mirror-root-rel",
        default="10_source_library_archive/mirror_kimi_inbox",
    )
    p.add_argument("--limit-per-basename", type=int, default=5)
    return p.parse_args()


def load_gaps(path: Path) -> list[Gap]:
    items: list[Gap] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            if (row.get("category") or "").strip() != "source_library_mirror":
                continue
            items.append(
                Gap(
                    lifted_rel_path=(row.get("lifted_rel_path") or "").strip().replace("\\", "/"),
                    proposed_target_rel_path=(row.get("proposed_target_rel_path") or "").strip().replace("\\", "/"),
                    size_bytes=int((row.get("size_bytes") or "0").strip() or "0"),
                    sha256=(row.get("sha256") or "").strip(),
                )
            )
    return items


def build_basename_index(root: Path, limit_per_basename: int) -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        name = path.name
        rel = str(path.relative_to(root)).replace("\\", "/")
        bucket = index.setdefault(name, [])
        if len(bucket) < limit_per_basename:
            bucket.append(rel)
    return index


def main() -> None:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    gaps_path = Path(args.gaps_tsv).resolve()
    out_tsv = Path(args.out_tsv).resolve()
    out_summary = Path(args.out_summary).resolve()
    mirror_root = (repo_root / Path(args.mirror_root_rel)).resolve()
    limit_per_basename = int(args.limit_per_basename)

    gaps = load_gaps(gaps_path)
    basename_index = build_basename_index(mirror_root, limit_per_basename=limit_per_basename)

    rows: list[MatchRow] = []
    for item in gaps:
        name = Path(item.lifted_rel_path).name
        candidates = basename_index.get(name, [])
        rows.append(
            MatchRow(
                lifted_rel_path=item.lifted_rel_path,
                proposed_target_rel_path=item.proposed_target_rel_path,
                basename=name,
                candidate_count=len(candidates),
                candidate_paths="|".join(candidates),
                size_bytes=item.size_bytes,
                sha256=item.sha256,
            )
        )

    rows.sort(key=lambda r: (-r.candidate_count, r.basename, r.lifted_rel_path))
    out_tsv.parent.mkdir(parents=True, exist_ok=True)
    with out_tsv.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(
            "lifted_rel_path\tproposed_target_rel_path\tbasename\tcandidate_count\tcandidate_paths\tsize_bytes\tsha256\n"
        )
        for r in rows:
            handle.write(
                f"{r.lifted_rel_path}\t{r.proposed_target_rel_path}\t{r.basename}\t{r.candidate_count}\t{r.candidate_paths}\t{r.size_bytes}\t{r.sha256}\n"
            )

    hit_any = sum(1 for r in rows if r.candidate_count > 0)
    payload = {
        "format": "source_library_mirror_gap_analysis_v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(repo_root),
        "mirror_root": str(mirror_root),
        "gaps_tsv": str(gaps_path),
        "row_count": len(rows),
        "hit_any_count": hit_any,
        "hit_any_ratio": (hit_any / len(rows)) if rows else 0.0,
        "limit_per_basename": limit_per_basename,
    }
    out_summary.parent.mkdir(parents=True, exist_ok=True)
    out_summary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

