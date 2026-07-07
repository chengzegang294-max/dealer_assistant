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
PREFLIGHT_TSV = GROUP08_ROOT / "GROUP_08_external_ops_preflight_v1.tsv"
OUT_TSV = GROUP08_ROOT / "GROUP_08_materials_catalog_v1.tsv"
OUT_MD = GROUP08_ROOT / "GROUP_08_materials_catalog_v1.md"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def write_md(path: Path, rows: list[dict[str, str]]) -> None:
    lines: list[str] = []
    lines.append("# GROUP_08 Materials Catalog v1")
    lines.append("")
    lines.append("这是 `GROUP_08` 当前可直接使用的材料目录（以 staging 副本为准）。")
    lines.append("")
    lines.append("- staging 根目录：`00_external_import_staging/`")
    lines.append("- 真值台账：`GROUP_08_前后路径台账_v1.tsv`")
    lines.append("")
    lines.append("| paper_id | title_anchor | path_match_status | repo_staging_path_after | source_path_before | sha256 | |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    r.get("paper_id", ""),
                    r.get("title_anchor", "").replace("|", " "),
                    r.get("path_match_status", ""),
                    r.get("repo_staging_path_after", "").replace("|", " "),
                    r.get("source_path_before", "").replace("|", " "),
                    r.get("sha256", ""),
                ]
            )
            + " |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ledger_rows = read_tsv(LEDGER_TSV)
    preflight_rows = read_tsv(PREFLIGHT_TSV)

    sha_by_pid: dict[str, str] = {}
    for r in preflight_rows:
        if (r.get("action") or "").strip() not in {"MOVE", "DELETE_CANDIDATE"}:
            continue
        pid = (r.get("paper_id") or "").strip()
        sha = (r.get("staging_sha256") or "").strip()
        if pid and sha:
            sha_by_pid[pid] = sha

    out_rows: list[dict[str, str]] = []
    for r in ledger_rows:
        if not (r.get("copy_status") or "").strip().startswith("COPIED"):
            continue
        pid = r.get("paper_id", "")
        out_rows.append(
            {
                "paper_id": pid,
                "title_anchor": (r.get("title_anchor") or "").strip(),
                "path_match_status": (r.get("path_match_status") or "").strip(),
                "copy_status": (r.get("copy_status") or "").strip(),
                "repo_staging_path_after": (r.get("repo_staging_path_after") or "").strip(),
                "source_path_before": (r.get("source_path_before") or "").strip(),
                "sha256": sha_by_pid.get(pid, ""),
            }
        )

    out_rows.sort(key=lambda x: x.get("paper_id", ""))
    write_tsv(
        OUT_TSV,
        out_rows,
        [
            "paper_id",
            "title_anchor",
            "path_match_status",
            "copy_status",
            "repo_staging_path_after",
            "source_path_before",
            "sha256",
        ],
    )
    write_md(OUT_MD, out_rows)

    print(f"rows={len(out_rows)}")
    print(f"out_tsv={OUT_TSV}")
    print(f"out_md={OUT_MD}")


if __name__ == "__main__":
    main()

