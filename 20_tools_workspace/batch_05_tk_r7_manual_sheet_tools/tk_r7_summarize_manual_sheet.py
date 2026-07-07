import argparse
import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheet", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--out-md", default="tkr7_manual_audit_summary_v1.md")
    parser.add_argument("--out-tsv", default="tkr7_manual_audit_summary_v1.tsv")
    args = parser.parse_args()

    sheet_path = Path(args.sheet)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not sheet_path.exists():
        raise FileNotFoundError(str(sheet_path))

    total_rows = 0
    valid_rows = 0
    counts: dict[str, int] = defaultdict(int)

    with sheet_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            total_rows += 1
            symbol = (row.get("symbol") or "").strip()
            if not symbol:
                continue
            valid_rows += 1
            key = (row.get("ao_risk_adjust_note") or "").strip() or "unknown"
            counts[key] += 1

    tsv_lines = ["ao_risk_adjust_note\tcount"]
    for key in sorted(counts.keys()):
        tsv_lines.append(f"{key}\t{counts[key]}")
    out_tsv = out_dir / args.out_tsv
    out_tsv.write_text("\n".join(tsv_lines) + "\n", encoding="utf-8")

    date_tag = datetime.now().strftime("%Y-%m-%d")
    md_lines = [
        "# TK-R7 手工标注汇总（自动生成）",
        "",
        f"- date: {date_tag}",
        f"- sheet: {sheet_path}",
        f"- total_rows: {total_rows}",
        f"- valid_rows: {valid_rows}",
        "",
        "## ao_risk_adjust_note 计数",
        "",
        "| ao_risk_adjust_note | count |",
        "|---|---:|",
    ]
    for key in sorted(counts.keys()):
        md_lines.append(f"| {key} | {counts[key]} |")
    out_md = out_dir / args.out_md
    out_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
