from __future__ import annotations

from pathlib import Path
import csv


REPO_ROOT = Path(__file__).resolve().parents[2]


def find_group08_root() -> Path:
    candidates = [
        REPO_ROOT / "10_来源库_SOURCE_LIBRARY" / "01_Kimi拆书待入库" / "GROUP_08_A股量化_数据研究",
        REPO_ROOT / "10_source_library_archive" / "mirror_kimi_inbox" / "GROUP_08_A股量化_数据研究",
        REPO_ROOT / "10_source_library_archive" / "GROUP_08_A股量化_数据研究",
    ]
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


GROUP08_ROOT = find_group08_root()
FINAL_TSV = GROUP08_ROOT / "GROUP_08_research_pdf_最终删除勾选_逐条清单_v1.tsv"
REFSCAN_SUMMARY_TSV = GROUP08_ROOT / "GROUP_08_repo_refscan_summary_v1.tsv"
OUT_PLAN_TSV = GROUP08_ROOT / "GROUP_08_external_ops_plan_v1.tsv"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    final_rows = read_tsv(FINAL_TSV)
    ref_rows = read_tsv(REFSCAN_SUMMARY_TSV)

    ref_by: dict[tuple[str, str], dict[str, str]] = {}
    for r in ref_rows:
        ref_by[(r["paper_id"], r["token_type"])] = r

    out: list[dict[str, str]] = []
    for r in final_rows:
        paper_id = r["paper_id"]
        b = ref_by.get((paper_id, "basename"), {})
        f = ref_by.get((paper_id, "fullpath"), {})

        delete_prereq = (r.get("delete_prereq") or "").strip()
        if delete_prereq == "check_repo_refs_then_delete_external_subset":
            action = "DELETE_EXTERNAL_SUBSET_CANDIDATE"
        elif delete_prereq == "check_repo_refs_then_move_not_delete":
            action = "MOVE_READY_NOT_DELETE"
        else:
            action = "MOVE_READY_NOT_DELETE"

        out.append(
            {
                "paper_id": paper_id,
                "delete_prereq": delete_prereq,
                "action_recommendation": action,
                "source_path_before": (r.get("source_path_before") or "").strip(),
                "repo_staging_path_after": (r.get("repo_staging_path_after") or "").strip(),
                "outside_refs_basename": (b.get("outside_group08_count") or "0").strip(),
                "outside_refs_fullpath": (f.get("outside_group08_count") or "0").strip(),
                "outside_files_sample_basename": (b.get("outside_group08_sample") or "").strip(),
                "outside_files_sample_fullpath": (f.get("outside_group08_sample") or "").strip(),
            }
        )

    out.sort(key=lambda x: x.get("paper_id", ""))
    write_tsv(
        OUT_PLAN_TSV,
        out,
        [
            "paper_id",
            "delete_prereq",
            "action_recommendation",
            "source_path_before",
            "repo_staging_path_after",
            "outside_refs_basename",
            "outside_refs_fullpath",
            "outside_files_sample_basename",
            "outside_files_sample_fullpath",
        ],
    )
    print(f"wrote={OUT_PLAN_TSV}")
    print(f"rows={len(out)}")


if __name__ == "__main__":
    main()

