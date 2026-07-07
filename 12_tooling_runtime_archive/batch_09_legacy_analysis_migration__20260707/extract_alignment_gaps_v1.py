import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class GapRow:
    lifted_rel_path: str
    category: str
    proposed_target_rel_path: str
    size_bytes: int
    sha256: str


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--audit-tsv", required=True)
    p.add_argument("--out-tsv", required=True)
    p.add_argument("--out-summary", required=True)
    p.add_argument("--only-category", action="append", default=[])
    return p.parse_args()


def main() -> None:
    args = parse_args()
    audit_path = Path(args.audit_tsv).resolve()
    out_tsv = Path(args.out_tsv).resolve()
    out_summary = Path(args.out_summary).resolve()
    only_categories = [str(x).strip() for x in (args.only_category or []) if str(x).strip()]
    only_set = set(only_categories)

    gaps: list[GapRow] = []
    with audit_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            if (row.get("target_exists") or "").strip() != "0":
                continue
            category = (row.get("category") or "").strip()
            if only_set and category not in only_set:
                continue
            gaps.append(
                GapRow(
                    lifted_rel_path=(row.get("lifted_rel_path") or "").strip(),
                    category=category,
                    proposed_target_rel_path=(row.get("proposed_target_rel_path") or "").strip(),
                    size_bytes=int((row.get("size_bytes") or "0").strip() or "0"),
                    sha256=(row.get("sha256") or "").strip(),
                )
            )

    gaps.sort(key=lambda x: (x.category, x.lifted_rel_path))
    out_tsv.parent.mkdir(parents=True, exist_ok=True)
    with out_tsv.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("lifted_rel_path\tcategory\tproposed_target_rel_path\tsize_bytes\tsha256\n")
        for item in gaps:
            handle.write(
                f"{item.lifted_rel_path}\t{item.category}\t{item.proposed_target_rel_path}\t{item.size_bytes}\t{item.sha256}\n"
            )

    payload = {
        "format": "lifted_alignment_gaps_v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "audit_tsv": str(audit_path),
        "out_tsv": str(out_tsv),
        "row_count": len(gaps),
        "only_categories": only_categories,
        "category_counts": {},
    }
    by_cat: dict[str, int] = {}
    for item in gaps:
        by_cat[item.category] = by_cat.get(item.category, 0) + 1
    payload["category_counts"] = dict(sorted(by_cat.items(), key=lambda x: (-x[1], x[0])))
    out_summary.parent.mkdir(parents=True, exist_ok=True)
    out_summary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

