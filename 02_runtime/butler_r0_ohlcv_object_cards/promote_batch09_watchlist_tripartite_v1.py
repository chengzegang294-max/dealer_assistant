from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path


RUNTIME_CATALOG_HEADERS = [
    "group_name",
    "file_name",
    "repo_path",
    "source_repo_path",
    "generator_entry",
    "current_role",
    "evidence_mode",
    "note",
]

SOURCE_MAP_HEADERS = [
    "source_repo_path",
    "promoted_repo_path",
    "group_name",
    "action",
    "evidence_mode",
    "note",
]

ARTIFACT_INDEX_HEADERS = [
    "artifact_file",
    "repo_path",
    "producer",
    "scope",
    "evidence_mode",
    "status",
    "note",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def write_tsv(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def move_files(
    repo: Path,
    source_dir: Path,
    patterns: list[str],
    target_dir: Path,
    action_label: str,
    note: str,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    target_dir.mkdir(parents=True, exist_ok=True)
    for pattern in patterns:
        for src in sorted(source_dir.glob(pattern)):
            dst = target_dir / src.name
            source_repo_path = str(src.relative_to(repo)).replace("\\", "/")
            promoted_repo_path = str(dst.relative_to(repo)).replace("\\", "/")
            if src.resolve() != dst.resolve():
                shutil.move(str(src), str(dst))
            rows.append(
                {
                    "source_repo_path": source_repo_path,
                    "promoted_repo_path": promoted_repo_path,
                    "group_name": action_label,
                    "action": "move_promote",
                    "evidence_mode": "historical_recovered",
                    "note": note,
                }
            )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote remaining batch09 ashare_watchlist files into runtime/source/tooling tripartite targets.")
    parser.add_argument(
        "--source-dir",
        default="00_assets/_raw_snapshot_batch09/ashare_watchlist",
        help="Repo-relative watchlist source directory.",
    )
    args = parser.parse_args()

    repo = repo_root()
    source_dir = repo / args.source_dir
    runtime_root = repo / "02_runtime/butler_r0_ohlcv_object_cards/data/raw/watchlist_inputs/batch09_promoted/structured_inputs"
    runtime_catalog = repo / "02_runtime/butler_r0_ohlcv_object_cards/data/raw/watchlist_inputs/catalog_v1.tsv"
    source_root = repo / "10_source_library_archive/batch_09_legacy_source_library_alignment__20260707/00_raw_snapshot/ashare_watchlist_text_snapshot"
    source_map = source_root / "promotion_map_v1.tsv"
    tooling_root = repo / "12_tooling_runtime_archive/batch_09_watchlist_ocr_artifacts__20260708/artifacts/ashare_watchlist_blogroom"
    tooling_index = repo / "12_tooling_runtime_archive/batch_09_watchlist_ocr_artifacts__20260708/BATCH_09_WATCHLIST_OCR_ARTIFACT_INDEX__20260708.tsv"
    generator_rel = "02_runtime/butler_r0_ohlcv_object_cards/promote_batch09_watchlist_tripartite_v1.py"

    runtime_rows = move_files(
        repo,
        source_dir,
        [
            "core_pool_*.csv",
            "focus_pool_*.csv",
            "top*_*.csv",
            "factors_ladder_*.csv",
            "watchlist_screen_*.csv",
        ],
        runtime_root,
        "runtime_structured_inputs",
        "从 batch09 ashare_watchlist 归位到 runtime watchlist 结构化输入层",
    )
    source_rows = move_files(
        repo,
        source_dir,
        ["core_pool_*.txt", "focus_pool_*.txt", "top*_*.txt"],
        source_root,
        "source_text_snapshot",
        "从 batch09 ashare_watchlist 归位到来源库文本快照层，保留原始文本形态",
    )
    artifact_rows = move_files(
        repo,
        source_dir,
        ["blogroom_*.csv", "blogroom_*.jsonl", "mx2025_summary_*.jsonl"],
        tooling_root,
        "tooling_ocr_artifacts",
        "从 batch09 ashare_watchlist 归位到 OCR/提取运行产物层，不冒充正式 runtime 输入",
    )

    runtime_catalog_rows = read_tsv(runtime_catalog)
    for row in runtime_rows:
        runtime_catalog_rows.append(
            {
                "group_name": row["group_name"],
                "file_name": Path(row["promoted_repo_path"]).name,
                "repo_path": row["promoted_repo_path"],
                "source_repo_path": row["source_repo_path"],
                "generator_entry": generator_rel,
                "current_role": "formal_historical_watchlist_input",
                "evidence_mode": "historical_recovered",
                "note": row["note"],
            }
        )
    runtime_catalog_rows.sort(key=lambda r: (r["group_name"], r["file_name"], r["repo_path"]))
    write_tsv(runtime_catalog, RUNTIME_CATALOG_HEADERS, runtime_catalog_rows)
    write_tsv(source_map, SOURCE_MAP_HEADERS, source_rows)

    artifact_index_rows: list[dict[str, str]] = []
    for row in artifact_rows:
        artifact_index_rows.append(
            {
                "artifact_file": Path(row["promoted_repo_path"]).name,
                "repo_path": row["promoted_repo_path"],
                "producer": generator_rel,
                "scope": "batch09 ashare_watchlist blogroom/mx2025 OCR extraction",
                "evidence_mode": "historical_recovered",
                "status": "promoted",
                "note": row["note"],
            }
        )
    write_tsv(tooling_index, ARTIFACT_INDEX_HEADERS, artifact_index_rows)

    if source_dir.exists():
        try:
            source_dir.rmdir()
        except OSError:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
