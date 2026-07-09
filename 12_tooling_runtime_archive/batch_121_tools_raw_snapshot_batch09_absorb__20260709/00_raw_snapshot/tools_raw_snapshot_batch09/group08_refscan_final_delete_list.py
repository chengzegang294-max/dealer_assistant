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
FINAL_TSV = GROUP08_ROOT / "GROUP_08_research_pdf_最终删除勾选_逐条清单_v1.tsv"
OUT_FULL = GROUP08_ROOT / "GROUP_08_repo_refscan_for_final_delete_list_v1.tsv"
OUT_SUMMARY = GROUP08_ROOT / "GROUP_08_repo_refscan_summary_v1.tsv"


def iter_text_files(root: Path) -> list[Path]:
    exts = {".md", ".tsv", ".txt", ".py", ".json", ".yml", ".yaml"}
    paths: list[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in exts:
            continue
        if ".git" in p.parts:
            continue
        paths.append(p)
    return paths


def read_text(path: Path) -> str:
    for enc in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=enc, errors="ignore")
        except Exception:
            continue
    return ""


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    rows = read_tsv(FINAL_TSV)
    targets: list[tuple[str, str, str]] = []
    for r in rows:
        src_full = (r.get("source_path_before") or "").strip()
        base_name = Path(src_full).name if src_full else ""
        if base_name:
            targets.append((r["paper_id"], "basename", base_name))
        if src_full:
            targets.append((r["paper_id"], "fullpath", src_full))

    repo_files = iter_text_files(REPO_ROOT)
    file_cache = [(p, read_text(p)) for p in repo_files]

    full_rows: list[dict[str, str]] = []
    for pid, token_type, token in targets:
        hits: list[str] = []
        for p, text in file_cache:
            if token and token in text:
                hits.append(str(p))
        full_rows.append(
            {
                "paper_id": pid,
                "token_type": token_type,
                "token": token,
                "match_count": str(len(hits)),
                "match_files_sample": " | ".join(hits[:30]),
            }
        )

    write_tsv(
        OUT_FULL,
        full_rows,
        ["paper_id", "token_type", "token", "match_count", "match_files_sample"],
    )

    summary_rows: list[dict[str, str]] = []
    g08_prefix = str(GROUP08_ROOT).lower()
    for r in full_rows:
        files = (r.get("match_files_sample") or "").split(" | ") if r.get("match_files_sample") else []
        files = [x.strip() for x in files if x.strip()]
        outside = [p for p in files if not p.lower().startswith(g08_prefix)]
        summary_rows.append(
            {
                "paper_id": r["paper_id"],
                "token_type": r["token_type"],
                "match_count": r.get("match_count", "0"),
                "outside_group08_count": str(len(outside)),
                "outside_group08_sample": " | ".join(outside[:10]),
            }
        )

    write_tsv(
        OUT_SUMMARY,
        summary_rows,
        [
            "paper_id",
            "token_type",
            "match_count",
            "outside_group08_count",
            "outside_group08_sample",
        ],
    )

    print(f"refscan_targets={len(targets)}")
    print(f"repo_files={len(repo_files)}")
    print(f"out_full={OUT_FULL}")
    print(f"out_summary={OUT_SUMMARY}")


if __name__ == "__main__":
    main()

