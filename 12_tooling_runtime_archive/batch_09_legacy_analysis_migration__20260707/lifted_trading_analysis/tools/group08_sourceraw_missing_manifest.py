from __future__ import annotations

from pathlib import Path
import csv


REPO_ROOT = Path(__file__).resolve().parents[1]
KIMI_ROOT = REPO_ROOT / "10_来源库_SOURCE_LIBRARY" / "01_Kimi拆书待入库"
GROUP08_ROOT = KIMI_ROOT / "GROUP_08_A股量化_数据研究"
TXT_INDEX_TSV = GROUP08_ROOT / "05_txt源码_md归档" / "txt_md_index_v1.tsv"

SOURCE_RAW_ROOT = (
    KIMI_ROOT / "GROUP_08_A股量化_数据研究__SOURCE_RAW" / "新的参考书"
)

OUT_TSV = GROUP08_ROOT / "GROUP_08_SOURCE_RAW_missing_manifest_v1.tsv"
OUT_MD = GROUP08_ROOT / "GROUP_08_SOURCE_RAW_回找执行记录_v1.md"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader)


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = read_tsv(TXT_INDEX_TSV)

    missing_rows: list[dict[str, str]] = []
    existing_count = 0
    not_under_root = 0
    book_dirs: dict[str, int] = {}

    for row in rows:
        src_path = Path(row["src_path"])
        if src_path.exists():
            existing_count += 1
            continue

        rel_under_root = ""
        try:
            rel_under_root = str(src_path.relative_to(SOURCE_RAW_ROOT))
            if rel_under_root:
                book_name = rel_under_root.split("\\", 1)[0]
                book_dirs[book_name] = book_dirs.get(book_name, 0) + 1
        except ValueError:
            not_under_root += 1

        missing_rows.append(
            {
                "batch_id": row.get("batch_id", ""),
                "src_path": row.get("src_path", ""),
                "rel_under_source_raw": rel_under_root,
                "md_path": row.get("md_path", ""),
                "encoding": row.get("encoding", ""),
                "cluster_id": row.get("cluster_id", ""),
                "cluster_name": row.get("cluster_name", ""),
            }
        )

    fieldnames = [
        "batch_id",
        "src_path",
        "rel_under_source_raw",
        "md_path",
        "encoding",
        "cluster_id",
        "cluster_name",
    ]
    write_tsv(OUT_TSV, missing_rows, fieldnames)

    total = len(rows)
    missing = len(missing_rows)
    lines: list[str] = []
    lines.append("# GROUP_08 SOURCE_RAW 回找执行记录 v1")
    lines.append("")
    lines.append("## 目的")
    lines.append("")
    lines.append(
        "- 基于 `txt_md_index_v1.tsv` 反推 `GROUP_08_A股量化_数据研究__SOURCE_RAW\\新的参考书` 的缺失情况，形成可回找清单。"
    )
    lines.append("")
    lines.append("## 本轮结论")
    lines.append("")
    lines.append(f"- txt 索引总行数：`{total}`")
    lines.append(f"- 仍在磁盘上的 src 文件数：`{existing_count}`")
    lines.append(f"- 缺失的 src 文件数：`{missing}`")
    lines.append(f"- src_path 不在 `新的参考书` 根下的缺失行数：`{not_under_root}`")
    lines.append("")
    lines.append("## 关键产物")
    lines.append("")
    lines.append(f"- 缺失清单：`{OUT_TSV.relative_to(GROUP08_ROOT)}`")
    lines.append("")
    lines.append("## 可回找的书名分布（按缺失文件数）")
    lines.append("")
    if book_dirs:
        for book_name, cnt in sorted(book_dirs.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"- `{book_name}`：`{cnt}`")
    else:
        lines.append("- 当前无法从缺失行中解析出稳定书名。")
    lines.append("")
    lines.append("## 回找建议")
    lines.append("")
    lines.append("- 优先按书名/包名回找：")
    lines.append("  - `《Python股票量化交易从入门到实践》完整版`")
    lines.append("  - `1.量化策略代码(99份)（赠品）`")
    lines.append("- 如果你找回了任意一层目录或压缩包：")
    lines.append("  - 把它放回到 `GROUP_08_A股量化_数据研究__SOURCE_RAW\\新的参考书\\...` 的同结构位置")
    lines.append("  - 然后重新运行本脚本，缺失数会下降，说明回源成功")
    lines.append("")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"rows_total={total}")
    print(f"src_existing={existing_count}")
    print(f"src_missing={missing}")
    print(f"missing_not_under_source_raw_root={not_under_root}")
    print(f"out_tsv={OUT_TSV}")
    print(f"out_md={OUT_MD}")


if __name__ == "__main__":
    main()

