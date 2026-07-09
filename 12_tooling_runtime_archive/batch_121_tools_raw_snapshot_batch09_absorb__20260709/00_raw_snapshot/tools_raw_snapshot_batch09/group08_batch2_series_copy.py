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
GROUP08_ROOT = REPO_ROOT / "10_来源库_SOURCE_LIBRARY" / "01_Kimi拆书待入库" / "GROUP_08_A股量化_数据研究"
EXTERNAL_ROOT = CUT_FILE_ROOT / "S" / "03_券商研报"
AUDIT_TSV = GROUP08_ROOT / "GROUP_08_外部精确路径勾验_v1.tsv"
LEDGER_TSV = GROUP08_ROOT / "GROUP_08_前后路径台账_v1.tsv"
STAGING_ROOT = GROUP08_ROOT / "00_external_import_staging" / "confirmed_series"

SERIES_MATCHES: dict[str, str] = {
    "S-037": r"04_多因子\海通选股因子系列研究1：弱者终有逆袭日,强势几无持续时：A股市场的动量反转效应研究.pdf",
    "S-038": r"04_多因子\海通选股因子系列研究2：因子模型的尾部相关性研究.pdf",
    "S-039": r"04_多因子\海通选股因子系列研究3：从Spearman相关系数出发研究因子有效性，Kalman+Filter模型在因子选择中的应用.pdf",
    "S-040": r"04_多因子\海通选股因子系列研究4：多因子选股模型的有效与失效.pdf",
    "S-041": r"04_多因子\海通选股因子系列研究5：寻找股价驱动新因子净换手率.pdf",
}

CONFIRMED_STATUS = "SERIES_MANUAL_CONFIRMED"
DELETE_PREREQ = "check_repo_refs_then_delete_external_subset"


def read_tsv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader), list(reader.fieldnames or [])


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    audit_rows, audit_fields = read_tsv(AUDIT_TSV)
    ledger_rows, ledger_fields = read_tsv(LEDGER_TSV)

    audit_by_id = {row["paper_id"]: row for row in audit_rows}
    ledger_by_id = {row["paper_id"]: row for row in ledger_rows}

    copied: list[str] = []
    for paper_id, rel_src in SERIES_MATCHES.items():
        src_path = EXTERNAL_ROOT / rel_src
        if not src_path.exists():
            raise FileNotFoundError(f"missing source for {paper_id}: {src_path}")

        dst_path = STAGING_ROOT / Path(rel_src)
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)

        audit_row = audit_by_id[paper_id]
        audit_row["match_count"] = "1"
        audit_row["best_match_path"] = str(src_path)
        audit_row["best_match_name"] = src_path.name
        audit_row["status"] = CONFIRMED_STATUS

        ledger_row = ledger_by_id[paper_id]
        ledger_row["source_path_before"] = str(src_path)
        ledger_row["repo_staging_path_after"] = str(dst_path)
        ledger_row["path_match_status"] = CONFIRMED_STATUS
        ledger_row["copy_status"] = "COPIED"
        ledger_row["delete_prereq"] = DELETE_PREREQ

        copied.append(f"{paper_id}\t{src_path.name}")

    write_tsv(AUDIT_TSV, audit_rows, audit_fields)
    write_tsv(LEDGER_TSV, ledger_rows, ledger_fields)

    print(f"batch2_copied={len(copied)}")
    print(f"status={CONFIRMED_STATUS}")
    for item in copied:
        print(item)


if __name__ == "__main__":
    main()
