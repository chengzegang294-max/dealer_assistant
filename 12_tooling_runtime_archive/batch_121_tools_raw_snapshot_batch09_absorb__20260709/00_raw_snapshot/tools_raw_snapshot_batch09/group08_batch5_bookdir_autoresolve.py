from __future__ import annotations

import csv
import os
from pathlib import Path
import shutil


if not os.environ.get("ALLOW_ARCHIVE_ONLY_RUN"):
    raise RuntimeError(
        "ARCHIVE_ONLY: legacy tool expects retired external assets. Set ALLOW_ARCHIVE_ONLY_RUN=1 and CUT_FILE_ROOT to run intentionally."
    )

_cut_file_root = (os.environ.get("CUT_FILE_ROOT") or "").strip()
if not _cut_file_root:
    raise RuntimeError("ARCHIVE_ONLY: CUT_FILE_ROOT is required (example: D:\\Stock\\cut_file__TO_DELETE__YYYYMMDD).")

CUT_FILE_ROOT = Path(_cut_file_root)

REPO_ROOT = Path(__file__).resolve().parents[1]
GROUP08_ROOT = (
    REPO_ROOT
    / "10_来源库_SOURCE_LIBRARY"
    / "01_Kimi拆书待入库"
    / "GROUP_08_A股量化_数据研究"
)
BOOK_ROOT = CUT_FILE_ROOT / "《Python股票量化交易从入门到实践》完整版" / "2.其他量化资料(62份)（赠品）"
AUDIT_TSV = GROUP08_ROOT / "GROUP_08_外部精确路径勾验_v1.tsv"
LEDGER_TSV = GROUP08_ROOT / "GROUP_08_前后路径台账_v1.tsv"
STAGING_ROOT = GROUP08_ROOT / "00_external_import_staging" / "confirmed_bookdir"
AMBIG_REPORT_TSV = GROUP08_ROOT / "GROUP_08_bookdir_ambiguous_candidates_v1.tsv"

CONFIRMED_STATUS = "BOOKDIR_EXACT_PATH_CONFIRMED"
DELETE_PREREQ = "check_repo_refs_then_move_not_delete"


def read_tsv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader), list(reader.fieldnames or [])


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def normalize_key(text: str) -> str:
    text = text.strip().strip('"').lower()
    out: list[str] = []
    for ch in text:
        if "\u4e00" <= ch <= "\u9fff" or ch.isalnum():
            out.append(ch)
    return "".join(out)


def main() -> None:
    if not BOOK_ROOT.exists():
        raise FileNotFoundError(f"missing BOOK_ROOT: {BOOK_ROOT}")

    pdfs = list(BOOK_ROOT.rglob("*.pdf"))
    by_norm_stem: dict[str, list[Path]] = {}
    for p in pdfs:
        by_norm_stem.setdefault(normalize_key(p.stem), []).append(p)

    audit_rows, audit_fields = read_tsv(AUDIT_TSV)
    ledger_rows, ledger_fields = read_tsv(LEDGER_TSV)
    audit_by_id = {row["paper_id"]: row for row in audit_rows}
    ledger_by_id = {row["paper_id"]: row for row in ledger_rows}

    resolved: list[str] = []
    ambiguous: list[dict[str, str]] = []

    for paper_id, ledger_row in ledger_by_id.items():
        if (ledger_row.get("copy_status") or "").strip() != "WAIT_MANUAL_PATH":
            continue

        title = (ledger_row.get("title_anchor") or "").strip()
        if not title:
            continue

        key = normalize_key(title)
        hits = by_norm_stem.get(key, [])

        if len(hits) == 1:
            src_path = hits[0]
            rel_under_book = src_path.relative_to(BOOK_ROOT)
            dst_path = STAGING_ROOT / rel_under_book
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dst_path)

            audit_row = audit_by_id.get(paper_id)
            if audit_row is not None:
                audit_row["match_count"] = "1"
                audit_row["best_match_path"] = str(src_path)
                audit_row["best_match_name"] = src_path.name
                audit_row["status"] = CONFIRMED_STATUS

            ledger_row["source_path_before"] = str(src_path)
            ledger_row["repo_staging_path_after"] = str(dst_path)
            ledger_row["path_match_status"] = CONFIRMED_STATUS
            ledger_row["copy_status"] = "COPIED"
            ledger_row["delete_prereq"] = DELETE_PREREQ

            resolved.append(f"{paper_id}\t{src_path.name}")
        elif len(hits) > 1:
            candidates = " | ".join(str(p.relative_to(BOOK_ROOT)) for p in hits[:20])
            ambiguous.append(
                {
                    "paper_id": paper_id,
                    "title_anchor": title,
                    "normalized_key": key,
                    "candidate_count": str(len(hits)),
                    "candidates_sample": candidates,
                }
            )

    write_tsv(AUDIT_TSV, audit_rows, audit_fields)
    write_tsv(LEDGER_TSV, ledger_rows, ledger_fields)

    report_fields = [
        "paper_id",
        "title_anchor",
        "normalized_key",
        "candidate_count",
        "candidates_sample",
    ]
    write_tsv(AMBIG_REPORT_TSV, ambiguous, report_fields)

    print(f"batch5_bookdir_auto_resolved={len(resolved)}")
    for item in resolved:
        print(item)
    print(f"batch5_bookdir_ambiguous={len(ambiguous)}")
    print(f"ambiguous_report={AMBIG_REPORT_TSV}")


if __name__ == "__main__":
    main()
