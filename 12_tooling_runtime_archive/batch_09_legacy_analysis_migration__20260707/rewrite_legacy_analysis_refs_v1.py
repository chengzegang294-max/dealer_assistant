import argparse
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Change:
    path: str
    hit_count: int


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[2]))
    p.add_argument(
        "--lifted-prefix-posix",
        default="12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_trading_analysis",
    )
    p.add_argument("--write", action="store_true")
    p.add_argument("--out-report", required=True)
    return p.parse_args()


def read_text_any(path: Path) -> str:
    for enc in ("utf-8", "utf-8-sig", "gb18030", "utf-16", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except Exception:
            continue
    return path.read_bytes().decode("utf-8", errors="ignore")


def should_skip(path: Path) -> bool:
    lower = str(path).replace("\\", "/").lower()
    if "/.git/" in lower:
        return True
    if "/.venv" in lower:
        return True
    if "/lifted_trading_analysis/" in lower:
        return True
    if "/12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/" in lower:
        return True
    return False


def iter_text_files(root: Path) -> Iterable[Path]:
    exts = {".md", ".py", ".json", ".jsonc", ".tsv", ".txt"}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in exts:
            continue
        if should_skip(path):
            continue
        yield path


def apply_rewrites(text: str, lifted_prefix_posix: str) -> tuple[str, int]:
    lifted_posix = lifted_prefix_posix.strip().strip("/").replace("\\", "/")
    lifted_win = lifted_posix.replace("/", "\\")
    replacements = [
        ("legacy_analysis\\", lifted_win + "\\"),
        ("legacy_analysis/", lifted_posix + "/"),
        ("D:\\Stock\\trading_analysis\\", lifted_win + "\\"),
        ("D:\\Stock\\trading_analysis/", lifted_posix + "/"),
        ("D:\\Stock\\trading_analysis", lifted_win),
    ]

    out = text
    hits = 0
    for old, new in replacements:
        if old not in out:
            continue
        count = out.count(old)
        out = out.replace(old, new)
        hits += count
    return out, hits


def write_report(path: Path, changes: list[Change], args: argparse.Namespace) -> None:
    payload = {
        "format": "legacy_analysis_ref_rewrite_report_v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(Path(args.repo_root).resolve()),
        "lifted_prefix_posix": str(args.lifted_prefix_posix),
        "write": bool(args.write),
        "changed_file_count": len(changes),
        "total_hit_count": sum(item.hit_count for item in changes),
        "changes": [asdict(item) for item in changes],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    out_report = Path(args.out_report).resolve()
    lifted_prefix_posix = str(args.lifted_prefix_posix)

    if repo_root.name != "trading_assistant":
        raise ValueError(f"ref rewrite is restricted to trading_assistant repo_root, got: {repo_root}")

    changes: list[Change] = []
    for path in iter_text_files(repo_root):
        raw = read_text_any(path)
        rewritten, hits = apply_rewrites(raw, lifted_prefix_posix=lifted_prefix_posix)
        if hits <= 0:
            continue
        if args.write:
            path.write_text(rewritten, encoding="utf-8", newline="\n")
        changes.append(Change(path=str(path.relative_to(repo_root)).replace("\\", "/"), hit_count=hits))

    changes.sort(key=lambda x: (-x.hit_count, x.path))
    write_report(out_report, changes, args)


if __name__ == "__main__":
    os.environ.setdefault("PYTHONUTF8", "1")
    main()
