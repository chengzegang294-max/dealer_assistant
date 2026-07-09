import argparse
import csv
import os
import re
from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass(frozen=True)
class CutpackInfo:
    path: str
    filename: str
    bucket: str
    title_short: str
    version: str
    retain_mode: str
    current_repo_role: str
    quant_rows: int


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _extract_first(pattern: str, text: str, flags: int = 0) -> str:
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else ""


def _extract_quant_table_rows(text: str) -> int:
    idx = text.find("QUANTIZATION_TABLE")
    if idx < 0:
        return 0
    tail = text[idx:]
    lines = tail.splitlines()
    table_started = False
    header_seen = False
    rows = 0
    for line in lines:
        s = line.strip()
        if not table_started:
            if (
                s.startswith("|")
                and "concept" in s
                and ("raw_rule_from_text" in s or "observable_proxy" in s or "quant_status" in s)
            ):
                table_started = True
                header_seen = True
            continue
        if header_seen:
            header_seen = False
            continue
        if not s.startswith("|"):
            break
        if s.startswith("|---"):
            continue
        rows += 1
    return rows


def _parse_filename(filename: str) -> tuple[str, str, str]:
    name = re.sub(r"\.md$", "", filename, flags=re.I)
    parts = name.split("__")
    if len(parts) < 4 or parts[0] != "CUTPACK":
        return "", "", ""
    version = parts[-1].lower()
    middle = parts[2:-1]
    if len(middle) == 1:
        return "", middle[0].strip(), version
    bucket = middle[0].strip()
    title_short = "__".join(p.strip() for p in middle[1:]).strip()
    return bucket, title_short, version


def _detect_retain_mode(text: str) -> str:
    v = _extract_first(r"^\s*-?\s*\*\*retain_mode\*\*\s*:\s*([A-Z_]+)\s*$", text, re.M)
    if v:
        return v
    v = _extract_first(r"^\s*-?\s*retain_mode:\s*([A-Z_]+)\s*$", text, re.M)
    if v:
        return v
    v = _extract_first(r"^\s*\|\s*retain_mode\s*\|\s*([A-Z_]+)\s*\|\s*$", text, re.M)
    return v


def _detect_current_repo_role(text: str) -> str:
    v = _extract_first(r"^\s*-?\s*\*\*current_repo_role\*\*\s*:\s*([A-Z0-9_]+)\s*$", text, re.M)
    if v:
        return v
    v = _extract_first(r"^\s*-?\s*current_repo_role:\s*([A-Z0-9_]+)\s*$", text, re.M)
    if v:
        return v
    v = _extract_first(r"^\s*\|\s*current_repo_role\s*\|\s*([A-Z0-9_]+)\s*\|\s*$", text, re.M)
    return v


def iter_cutpacks(root: str) -> Iterable[CutpackInfo]:
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if not fn.lower().endswith(".md"):
                continue
            if not fn.startswith("CUTPACK__"):
                continue
            path = os.path.join(dirpath, fn)
            text = _read_text(path)
            bucket, title_short, version = _parse_filename(fn)
            info = CutpackInfo(
                path=os.path.abspath(path),
                filename=fn,
                bucket=bucket,
                title_short=title_short,
                version=version,
                retain_mode=_detect_retain_mode(text),
                current_repo_role=_detect_current_repo_role(text),
                quant_rows=_extract_quant_table_rows(text),
            )
            yield info


def write_manifest(items: list[CutpackInfo], out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(
            [
                "bucket",
                "title_short",
                "version",
                "retain_mode",
                "current_repo_role",
                "quant_rows",
                "path",
            ]
        )
        for it in sorted(items, key=lambda x: (x.bucket, x.title_short, x.filename)):
            w.writerow(
                [
                    it.bucket,
                    it.title_short,
                    it.version,
                    it.retain_mode,
                    it.current_repo_role,
                    str(it.quant_rows),
                    it.path,
                ]
            )


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    items = list(iter_cutpacks(args.root))
    write_manifest(items, args.out)
    print(f"cutpacks={len(items)}")
    print(f"out={os.path.abspath(args.out)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
