import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class Mismatch:
    rel_path: str
    field: str
    left: str
    right: str


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--left-tsv", required=True)
    p.add_argument("--right-tsv", required=True)
    p.add_argument("--out-report", required=True)
    p.add_argument("--max-mismatches", type=int, default=200)
    return p.parse_args()


def load(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows: dict[str, dict[str, str]] = {}
        for row in reader:
            rel = (row.get("rel_path") or "").strip()
            if not rel:
                continue
            rows[rel] = dict(row)
        return rows


def pick(row: dict[str, str], key: str) -> str:
    return (row.get(key) or "").strip()


def main() -> None:
    args = parse_args()
    left_path = Path(args.left_tsv).resolve()
    right_path = Path(args.right_tsv).resolve()
    out_report = Path(args.out_report).resolve()

    left = load(left_path)
    right = load(right_path)

    left_keys = set(left.keys())
    right_keys = set(right.keys())
    only_left = sorted(left_keys - right_keys)
    only_right = sorted(right_keys - left_keys)

    mismatches: list[Mismatch] = []
    for rel_path in sorted(left_keys & right_keys):
        lrow = left[rel_path]
        rrow = right[rel_path]
        for key in ("size_bytes", "sha256"):
            lv = pick(lrow, key)
            rv = pick(rrow, key)
            if lv != rv:
                mismatches.append(Mismatch(rel_path=rel_path, field=key, left=lv, right=rv))
                if len(mismatches) >= int(args.max_mismatches):
                    break
        if len(mismatches) >= int(args.max_mismatches):
            break

    payload = {
        "format": "inventory_compare_report_v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "left_tsv": str(left_path),
        "right_tsv": str(right_path),
        "left_count": len(left),
        "right_count": len(right),
        "only_left_count": len(only_left),
        "only_right_count": len(only_right),
        "mismatch_count": len(mismatches),
        "only_left_head": only_left[:50],
        "only_right_head": only_right[:50],
        "mismatches": [asdict(x) for x in mismatches],
    }

    out_report.parent.mkdir(parents=True, exist_ok=True)
    out_report.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

