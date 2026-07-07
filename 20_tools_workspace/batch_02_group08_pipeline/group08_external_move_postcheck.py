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

MOVE_PLAN_TSV = GROUP08_ROOT / "GROUP_08_external_move_plan_v1.tsv"
OUT_TSV = GROUP08_ROOT / "GROUP_08_external_move_postcheck_v1.tsv"
OUT_MD = GROUP08_ROOT / "GROUP_08_external_move_postcheck_v1.md"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    rows = read_tsv(MOVE_PLAN_TSV)
    out_rows: list[dict[str, str]] = []

    ok = 0
    moved = 0
    still_at_src = 0
    missing_both = 0

    for r in rows:
        pid = (r.get("paper_id") or "").strip()
        src = Path((r.get("source_path_before") or "").strip())
        dst = Path((r.get("suggested_dest_path") or "").strip())

        src_exists = "1" if src.exists() else "0"
        dst_exists = "1" if dst.exists() else "0"

        if src_exists == "0" and dst_exists == "1":
            status = "MOVED_OK"
            moved += 1
            ok += 1
        elif src_exists == "1" and dst_exists == "1":
            status = "DUPLICATE_BOTH_EXIST"
        elif src_exists == "1" and dst_exists == "0":
            status = "STILL_AT_SOURCE"
            still_at_src += 1
        else:
            status = "MISSING_BOTH"
            missing_both += 1

        out_rows.append(
            {
                "paper_id": pid,
                "source_path_before": str(src),
                "suggested_dest_path": str(dst),
                "source_exists": src_exists,
                "dest_exists": dst_exists,
                "postcheck_status": status,
            }
        )

    out_rows.sort(key=lambda x: x.get("paper_id", ""))
    write_tsv(
        OUT_TSV,
        out_rows,
        [
            "paper_id",
            "source_path_before",
            "suggested_dest_path",
            "source_exists",
            "dest_exists",
            "postcheck_status",
        ],
    )

    lines: list[str] = []
    lines.append("# GROUP_08 External Move Postcheck v1")
    lines.append("")
    lines.append(f"- move_rows: {len(rows)}")
    lines.append(f"- moved_ok: {moved}")
    lines.append(f"- still_at_source: {still_at_src}")
    lines.append(f"- missing_both: {missing_both}")
    lines.append("")
    lines.append(f"- out_tsv: {OUT_TSV.name}")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"moved_ok={moved}")
    print(f"still_at_source={still_at_src}")
    print(f"missing_both={missing_both}")
    print(f"out={OUT_TSV}")


if __name__ == "__main__":
    main()

