from __future__ import annotations

from pathlib import Path
import csv


REPO_ROOT = Path(__file__).resolve().parents[1]
GROUP08_ROOT = (
    REPO_ROOT
    / "10_来源库_SOURCE_LIBRARY"
    / "01_Kimi拆书待入库"
    / "GROUP_08_A股量化_数据研究"
)
LEDGER_TSV = GROUP08_ROOT / "GROUP_08_前后路径台账_v1.tsv"
FINAL_TSV = GROUP08_ROOT / "GROUP_08_research_pdf_最终删除勾选_逐条清单_v1.tsv"


def read_tsv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)
        fields = list(reader.fieldnames or [])
    return rows, fields


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ledger_rows, _ = read_tsv(LEDGER_TSV)
    final_rows, final_fields = read_tsv(FINAL_TSV)

    final_by_id = {r["paper_id"]: r for r in final_rows}

    added: list[str] = []
    updated: list[str] = []

    for r in ledger_rows:
        copy_status = (r.get("copy_status") or "").strip()
        if not copy_status.startswith("COPIED"):
            continue

        paper_id = r["paper_id"]
        src = (r.get("source_path_before") or "").strip()
        dst = (r.get("repo_staging_path_after") or "").strip()
        delete_prereq = (r.get("delete_prereq") or "").strip()

        if paper_id not in final_by_id:
            final_rows.append(
                {
                    "paper_id": paper_id,
                    "repo_final_tick": "WAIT_PATH_CHECK",
                    "external_final_tick": "MOVE_READY_NOT_DELETE",
                    "current_total_decision": "MOVE_READY_NOT_DELETE",
                    "delete_prereq": delete_prereq,
                    "source_path_before": src,
                    "repo_staging_path_after": dst,
                }
            )
            added.append(paper_id)
            continue

        row = final_by_id[paper_id]
        changed = False
        if row.get("delete_prereq") != delete_prereq:
            row["delete_prereq"] = delete_prereq
            changed = True
        if row.get("source_path_before") != src:
            row["source_path_before"] = src
            changed = True
        if row.get("repo_staging_path_after") != dst:
            row["repo_staging_path_after"] = dst
            changed = True
        if changed:
            updated.append(paper_id)

    final_rows.sort(key=lambda x: x.get("paper_id", ""))
    write_tsv(FINAL_TSV, final_rows, final_fields)

    print(f"sync_added={len(added)}")
    for pid in added:
        print(f"ADD\t{pid}")
    print(f"sync_updated={len(updated)}")
    for pid in updated:
        print(f"UPD\t{pid}")


if __name__ == "__main__":
    main()

