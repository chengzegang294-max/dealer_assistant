import argparse
import hashlib
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class FileRec:
    path: str
    dir_rel: str
    name: str
    base: str
    ext: str
    size: int


def _normalize_basename(base: str) -> str:
    s = base.strip()
    while True:
        prev = s
        if s.endswith("）"):
            import re

            s = re.sub(r"（\d+）$", "", s).strip()
        s = s.rstrip()
        import re

        s = re.sub(r"\(\d+\)$", "", s).strip()
        s = re.sub(r"\s+", " ", s).strip()
        if s == prev:
            break
    return s


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def iter_files(root: str) -> list[FileRec]:
    root_abs = os.path.abspath(root)
    items: list[FileRec] = []
    for dirpath, _, filenames in os.walk(root_abs):
        for fn in filenames:
            path = os.path.join(dirpath, fn)
            try:
                st = os.stat(path)
            except OSError:
                continue
            base, ext = os.path.splitext(fn)
            dir_rel = os.path.relpath(dirpath, root_abs)
            items.append(
                FileRec(
                    path=os.path.abspath(path),
                    dir_rel=dir_rel,
                    name=fn,
                    base=base,
                    ext=ext.lower(),
                    size=int(st.st_size),
                )
            )
    return items


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--min-copies", type=int, default=2)
    args = ap.parse_args()

    files = iter_files(args.root)
    groups: dict[str, list[FileRec]] = {}
    for it in files:
        norm = (_normalize_basename(it.base) + it.ext).lower()
        groups.setdefault(norm, []).append(it)

    dup_groups = {k: v for k, v in groups.items() if len(v) >= args.min_copies}
    rows: list[tuple] = []
    same_hash_groups = 0
    same_hash_files = 0
    for norm, items in sorted(dup_groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        with_hash = []
        for it in sorted(items, key=lambda x: (x.dir_rel, x.name)):
            digest = _sha256(it.path)
            with_hash.append((it, digest))
        unique_hashes = {d for _, d in with_hash}
        if len(unique_hashes) == 1:
            same_hash_groups += 1
            same_hash_files += len(with_hash)
        preferred = None
        for it, d in with_hash:
            if "(1)" not in it.name and "（1）" not in it.name:
                preferred = (it, d)
                break
        if preferred is None:
            preferred = with_hash[0]
        keep_hash = preferred[1]
        for it, d in with_hash:
            action = "KEEP" if it.path == preferred[0].path else ("DROP" if d == keep_hash else "REVIEW")
            reason = (
                "preferred_non_(1)"
                if it.path == preferred[0].path and "(1)" not in it.name and "（1）" not in it.name
                else ("same_hash_as_keep" if action == "DROP" else ("hash_diff" if action == "REVIEW" else ""))
            )
            rows.append(
                (
                    norm,
                    len(with_hash),
                    it.ext,
                    it.size,
                    d,
                    action,
                    reason,
                    it.dir_rel,
                    it.name,
                    it.path,
                )
            )

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="") as f:
        f.write(
            "\t".join(
                [
                    "norm_key",
                    "copies",
                    "ext",
                    "size_bytes",
                    "sha256",
                    "action_suggestion",
                    "reason",
                    "dir_rel",
                    "name",
                    "path",
                ]
            )
            + "\n"
        )
        for r in rows:
            f.write("\t".join(str(x) for x in r) + "\n")

    print(f"files_total={len(files)}")
    print(f"dup_groups_total={len(dup_groups)}")
    print(f"dup_files_total={sum(len(v) for v in dup_groups.values())}")
    print(f"same_hash_groups={same_hash_groups}")
    print(f"same_hash_files={same_hash_files}")
    print(f"out={os.path.abspath(args.out)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

