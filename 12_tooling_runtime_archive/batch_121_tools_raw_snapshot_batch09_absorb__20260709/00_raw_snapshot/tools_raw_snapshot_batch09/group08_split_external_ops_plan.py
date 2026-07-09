from __future__ import annotations

import csv
import os
from pathlib import Path


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
OPS_PLAN_TSV = GROUP08_ROOT / "GROUP_08_external_ops_plan_v1.tsv"

OUT_MOVE_TSV = GROUP08_ROOT / "GROUP_08_external_move_plan_v1.tsv"
OUT_DELETE_TSV = GROUP08_ROOT / "GROUP_08_external_delete_candidate_plan_v1.tsv"

BOOK_ROOT = CUT_FILE_ROOT / "《Python股票量化交易从入门到实践》完整版" / "2.其他量化资料(62份)（赠品）"
S03_ROOT = CUT_FILE_ROOT / "S" / "03_券商研报"
DEFAULT_MOVE_DEST_ROOT = CUT_FILE_ROOT / "__GROUP_08_sorted"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def classify_root(src_path: Path) -> tuple[str, str]:
    try:
        rel = src_path.relative_to(BOOK_ROOT)
        return "BOOKDIR", str(rel)
    except Exception:
        pass
    try:
        rel = src_path.relative_to(S03_ROOT)
        return "S03", str(rel)
    except Exception:
        pass
    return "OTHER", src_path.name


def main() -> None:
    rows = read_tsv(OPS_PLAN_TSV)
    move_rows: list[dict[str, str]] = []
    delete_rows: list[dict[str, str]] = []

    for r in rows:
        src_str = (r.get("source_path_before") or "").strip()
        if not src_str:
            continue

        src = Path(src_str)
        root_type, rel_under_root = classify_root(src)
        suggested_dst = DEFAULT_MOVE_DEST_ROOT / root_type / rel_under_root

        base = {
            "paper_id": r.get("paper_id", ""),
            "root_type": root_type,
            "src_rel_under_root": rel_under_root,
            "source_path_before": src_str,
            "suggested_dest_path": str(suggested_dst),
            "repo_staging_path_after": (r.get("repo_staging_path_after") or "").strip(),
            "outside_refs_basename": (r.get("outside_refs_basename") or "0").strip(),
            "outside_refs_fullpath": (r.get("outside_refs_fullpath") or "0").strip(),
            "outside_files_sample_basename": (r.get("outside_files_sample_basename") or "").strip(),
            "outside_files_sample_fullpath": (r.get("outside_files_sample_fullpath") or "").strip(),
        }

        action = (r.get("action_recommendation") or "").strip()
        if action == "DELETE_EXTERNAL_SUBSET_CANDIDATE":
            delete_rows.append(
                {
                    **base,
                    "delete_candidate_path": src_str,
                    "delete_gate": "MANUAL_CONFIRM_ONLY",
                }
            )
        else:
            move_rows.append(
                {
                    **base,
                    "move_gate": "MANUAL_CONFIRM_ONLY",
                }
            )

    move_rows.sort(key=lambda x: x.get("paper_id", ""))
    delete_rows.sort(key=lambda x: x.get("paper_id", ""))

    write_tsv(
        OUT_MOVE_TSV,
        move_rows,
        [
            "paper_id",
            "root_type",
            "src_rel_under_root",
            "source_path_before",
            "suggested_dest_path",
            "repo_staging_path_after",
            "outside_refs_basename",
            "outside_refs_fullpath",
            "outside_files_sample_basename",
            "outside_files_sample_fullpath",
            "move_gate",
        ],
    )
    write_tsv(
        OUT_DELETE_TSV,
        delete_rows,
        [
            "paper_id",
            "root_type",
            "src_rel_under_root",
            "delete_candidate_path",
            "source_path_before",
            "suggested_dest_path",
            "repo_staging_path_after",
            "outside_refs_basename",
            "outside_refs_fullpath",
            "outside_files_sample_basename",
            "outside_files_sample_fullpath",
            "delete_gate",
        ],
    )

    print(f"move_rows={len(move_rows)}")
    print(f"delete_candidate_rows={len(delete_rows)}")
    print(f"out_move={OUT_MOVE_TSV}")
    print(f"out_delete={OUT_DELETE_TSV}")


if __name__ == "__main__":
    main()

