import argparse
import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


QUALITIES = [
    "no_retest",
    "retest_touch_only",
    "retest_reject_weak",
    "retest_reject_clear",
]


def to_int_flag(value: str) -> int:
    v = (value or "").strip()
    return 1 if v in {"1", "true", "True", "YES", "yes"} else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheet", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--out-md", default="tkr6_manual_audit_summary_v1.md")
    parser.add_argument("--out-tsv", default="tkr6_manual_audit_summary_v1.tsv")
    args = parser.parse_args()

    sheet_path = Path(args.sheet)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not sheet_path.exists():
        raise FileNotFoundError(str(sheet_path))

    total_rows = 0
    valid_rows = 0
    counts_by_quality: dict[str, int] = defaultdict(int)
    tp3_by_quality: dict[str, int] = defaultdict(int)

    with sheet_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            total_rows += 1
            symbol = (row.get("symbol") or "").strip()
            if not symbol:
                continue
            valid_rows += 1
            q = (row.get("ib_retest_quality") or "").strip()
            if not q:
                q = "unknown"
            counts_by_quality[q] += 1
            tp3_by_quality[q] += to_int_flag(row.get("tp3_reached") or "")

    summary_tsv_lines = ["ib_retest_quality\tcount\ttp3_reached_count\ttp3_reached_rate"]
    for q in QUALITIES + [k for k in sorted(counts_by_quality.keys()) if k not in QUALITIES]:
        c = counts_by_quality.get(q, 0)
        t = tp3_by_quality.get(q, 0)
        r = (t / c) if c else 0.0
        summary_tsv_lines.append(f"{q}\t{c}\t{t}\t{r:.4f}")

    out_tsv = out_dir / args.out_tsv
    out_tsv.write_text("\n".join(summary_tsv_lines) + "\n", encoding="utf-8")

    date_tag = datetime.now().strftime("%Y-%m-%d")
    md_lines = [
        "# TK-R6 手工标注汇总（自动生成）",
        "",
        f"- date: {date_tag}",
        f"- sheet: {sheet_path}",
        f"- total_rows: {total_rows}",
        f"- valid_rows: {valid_rows}",
        "",
        "## 分桶汇总",
        "",
        "| ib_retest_quality | count | tp3_reached_count | tp3_reached_rate |",
        "|---|---:|---:|---:|",
    ]

    for line in summary_tsv_lines[1:]:
        q, c, t, r = line.split("\t")
        md_lines.append(f"| {q} | {c} | {t} | {float(r):.4f} |")

    out_md = out_dir / args.out_md
    out_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
