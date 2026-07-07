import argparse
from pathlib import Path


def replace_in_file(path: Path, old: str, new: str) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = original.replace(old, new)
    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="directory to scan")
    parser.add_argument("--old", required=True, help="old prefix to replace")
    parser.add_argument("--new", required=True, help="new prefix")
    parser.add_argument("--glob", default="**/*", help="glob under root")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        raise FileNotFoundError(str(root))

    changed = 0
    scanned = 0
    for p in root.glob(args.glob):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".md", ".tsv"}:
            continue
        scanned += 1
        if replace_in_file(p, args.old, args.new):
            changed += 1

    print(f"scanned_files={scanned}")
    print(f"changed_files={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
