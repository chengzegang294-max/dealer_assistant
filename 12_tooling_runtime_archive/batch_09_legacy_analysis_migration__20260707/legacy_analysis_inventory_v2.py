import argparse
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import quote


@dataclass(frozen=True)
class Row:
    rel_path: str
    kind: str
    size_bytes: int
    mtime_utc: str
    sha256: str


def iso_utc(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def iter_paths(root: Path, excluded_dirnames: set[str]) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in excluded_dirnames]
        for name in filenames:
            yield Path(dirpath) / name


def relposix(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def to_row(root: Path, path: Path, do_hash: bool) -> Row:
    st = path.stat()
    return Row(
        rel_path=relposix(root, path),
        kind="file",
        size_bytes=int(st.st_size),
        mtime_utc=iso_utc(st.st_mtime),
        sha256=sha256_file(path) if do_hash else "",
    )


def write_tsv(rows: list[Row], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        f.write("rel_path\tkind\tsize_bytes\tmtime_utc\tsha256\n")
        for r in rows:
            f.write(f"{r.rel_path}\t{r.kind}\t{r.size_bytes}\t{r.mtime_utc}\t{r.sha256}\n")


def write_summary(rows: list[Row], root: Path, out_path: Path, do_hash: bool, excluded_dirnames: list[str]) -> None:
    total_bytes = sum(r.size_bytes for r in rows)
    summary = {
        "format": "legacy_analysis_inventory_v2",
        "root": str(root),
        "root_url": f"file:///{quote(str(root).replace('\\\\', '/'))}",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "do_hash": do_hash,
        "excluded_dirnames": excluded_dirnames,
        "file_count": len(rows),
        "total_bytes": total_bytes,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--out-tsv", required=True)
    p.add_argument("--out-summary", required=True)
    p.add_argument("--hash", action="store_true")
    p.add_argument("--exclude-dirname", action="append", default=[])
    return p.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root).resolve()
    out_tsv = Path(args.out_tsv).resolve()
    out_summary = Path(args.out_summary).resolve()
    do_hash = bool(args.hash)
    excluded = [str(x).strip() for x in (args.exclude_dirname or []) if str(x).strip()]
    excluded_dirnames = set(excluded)

    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"root not found: {root}")

    rows: list[Row] = []
    for p in iter_paths(root, excluded_dirnames=excluded_dirnames):
        if p.is_file():
            rows.append(to_row(root, p, do_hash))
    rows.sort(key=lambda r: r.rel_path)
    write_tsv(rows, out_tsv)
    write_summary(rows, root, out_summary, do_hash, excluded_dirnames=excluded)


if __name__ == "__main__":
    main()

