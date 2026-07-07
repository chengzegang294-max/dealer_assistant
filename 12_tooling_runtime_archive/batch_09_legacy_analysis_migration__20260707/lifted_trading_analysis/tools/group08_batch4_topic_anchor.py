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
EXTERNAL_ROOT = CUT_FILE_ROOT / "S" / "03_券商研报"
ANCHOR_TSV = GROUP08_ROOT / "GROUP_08_主题锚点勾验_v1.tsv"


ANCHOR_ROWS: list[dict[str, str]] = [
    {
        "paper_id": "S-005",
        "title_anchor": "从极值角度进行选股因子有效性的确认——在换手率上的实证",
        "anchor_type": "METHOD_THEME_ANCHOR",
        "external_anchor_rel_path": r"04_多因子\海通选股因子系列研究6：极值视角下的多因子选股策略.pdf",
        "repo_existing_staging_rel_path": r"00_external_import_staging\confirmed_exact\04_多因子\海通选股因子系列研究6：极值视角下的多因子选股策略.pdf",
        "anchor_status": "TOPIC_ANCHOR_ONLY",
        "delete_readiness": "NOT_DELETE_BASIS",
        "anchor_rationale": "S-005 is the extreme-value methodology groundwork explicitly summarized as the lead-in to S-009's broader extreme-value multi-factor framework.",
    },
    {
        "paper_id": "S-012",
        "title_anchor": "如何捕捉短线反弹机会？",
        "anchor_type": "UPSTREAM_CITATION_ANCHOR",
        "external_anchor_rel_path": r"04_多因子\海通选股因子系列研究1：弱者终有逆袭日,强势几无持续时：A股市场的动量反转效应研究.pdf",
        "repo_existing_staging_rel_path": r"00_external_import_staging\confirmed_series\04_多因子\海通选股因子系列研究1：弱者终有逆袭日,强势几无持续时：A股市场的动量反转效应研究.pdf",
        "anchor_status": "TOPIC_ANCHOR_ONLY",
        "delete_readiness": "NOT_DELETE_BASIS",
        "anchor_rationale": "S-012 explicitly cites the confirmed momentum-reversal report as its upstream research basis, but the anchor is retained only as a thematic truth pointer.",
    },
]


FIELDNAMES = [
    "paper_id",
    "title_anchor",
    "anchor_type",
    "external_anchor_path",
    "external_anchor_name",
    "repo_existing_staging_path",
    "anchor_status",
    "delete_readiness",
    "anchor_rationale",
]


def main() -> None:
    output_rows: list[dict[str, str]] = []

    for row in ANCHOR_ROWS:
        src_path = EXTERNAL_ROOT / row["external_anchor_rel_path"]
        staging_path = GROUP08_ROOT / row["repo_existing_staging_rel_path"]

        if not src_path.exists():
            raise FileNotFoundError(f"missing external anchor: {src_path}")
        if not staging_path.exists():
            raise FileNotFoundError(f"missing existing staging anchor: {staging_path}")

        output_rows.append(
            {
                "paper_id": row["paper_id"],
                "title_anchor": row["title_anchor"],
                "anchor_type": row["anchor_type"],
                "external_anchor_path": str(src_path),
                "external_anchor_name": src_path.name,
                "repo_existing_staging_path": str(staging_path),
                "anchor_status": row["anchor_status"],
                "delete_readiness": row["delete_readiness"],
                "anchor_rationale": row["anchor_rationale"],
            }
        )

    with ANCHOR_TSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, delimiter="\t")
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"batch4_topic_anchor_rows={len(output_rows)}")
    for row in output_rows:
        print(
            "\t".join(
                [
                    row["paper_id"],
                    row["anchor_type"],
                    row["anchor_status"],
                    row["external_anchor_name"],
                ]
            )
        )


if __name__ == "__main__":
    main()
