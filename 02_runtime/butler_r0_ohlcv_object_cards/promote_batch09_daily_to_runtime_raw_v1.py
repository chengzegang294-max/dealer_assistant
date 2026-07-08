from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path


CATALOG_HEADERS = [
    "symbol",
    "timeframe",
    "provider",
    "date_range",
    "repo_path",
    "source_type",
    "source_csv",
    "source_metadata",
    "generator_entry",
    "current_role",
    "evidence_mode",
    "note",
]

MAP_HEADERS = [
    "source_repo_path",
    "promoted_repo_path",
    "symbol",
    "date_range",
    "batch_family",
    "action",
    "evidence_mode",
    "note",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_catalog(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_catalog(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CATALOG_HEADERS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def upsert_catalog_row(rows: list[dict[str, str]], new_row: dict[str, str]) -> None:
    for idx, row in enumerate(rows):
        if row.get("repo_path") == new_row["repo_path"]:
            rows[idx] = new_row
            return
    rows.append(new_row)


def read_csv_meta(path: Path) -> tuple[str, str, str]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"csv has no rows: {path}")
    symbol = rows[0].get("symbol") or path.stem.replace("_1d", "").replace("_", ".")
    first_date = rows[0]["date"].replace("-", "")
    last_date = rows[-1]["date"].replace("-", "")
    return symbol, first_date, last_date


def write_map(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=MAP_HEADERS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote batch09 daily csv blocks from 00_assets into runtime formal raw input.")
    parser.add_argument(
        "--source-root",
        default="00_assets/_raw_snapshot_batch09",
        help="Repo-relative source root.",
    )
    parser.add_argument(
        "--target-root",
        default="02_runtime/butler_r0_ohlcv_object_cards/data/raw/daily_ohlcv/batch09_promoted",
        help="Repo-relative target root.",
    )
    args = parser.parse_args()

    repo = repo_root()
    source_root = repo / args.source_root
    target_root = repo / args.target_root
    catalog_path = repo / "02_runtime/butler_r0_ohlcv_object_cards/data/raw/daily_ohlcv/catalog_v1.tsv"
    map_path = target_root / "batch09_promotion_map_v1.tsv"
    generator_rel = "02_runtime/butler_r0_ohlcv_object_cards/promote_batch09_daily_to_runtime_raw_v1.py"
    map_rel = str(map_path.relative_to(repo)).replace("\\", "/")

    families = [
        ("ashare_clean", source_root / "ashare_clean", target_root / "ashare_clean"),
        ("watchlist_kline_1d", source_root / "ashare_watchlist" / "kline_1d", target_root / "watchlist_kline_1d"),
    ]

    catalog_rows = read_catalog(catalog_path)
    promotion_rows: list[dict[str, str]] = []

    for family_name, source_dir, target_dir in families:
        if not source_dir.exists() and not target_dir.exists():
            continue
        target_dir.mkdir(parents=True, exist_ok=True)
        source_files = sorted(source_dir.glob("*.csv")) if source_dir.exists() else []
        dest_files = sorted(target_dir.glob("*.csv"))
        files = source_files if source_files else dest_files

        for file_path in files:
            src_path = file_path
            dest_path = target_dir / file_path.name
            source_repo_path = str((source_dir / file_path.name).relative_to(repo)).replace("\\", "/")

            if src_path.exists() and src_path.resolve() != dest_path.resolve():
                shutil.move(str(src_path), str(dest_path))

            symbol, first_date, last_date = read_csv_meta(dest_path)
            promoted_repo_path = str(dest_path.relative_to(repo)).replace("\\", "/")
            promotion_rows.append(
                {
                    "source_repo_path": source_repo_path,
                    "promoted_repo_path": promoted_repo_path,
                    "symbol": symbol,
                    "date_range": f"{first_date}-{last_date}",
                    "batch_family": family_name,
                    "action": "move_promote",
                    "evidence_mode": "historical_recovered",
                    "note": "从合同外 00_assets/_raw_snapshot_batch09 归位到 runtime 正式原始输入层；保留 batch09 回链",
                }
            )

            upsert_catalog_row(
                catalog_rows,
                {
                    "symbol": symbol,
                    "timeframe": "1d",
                    "provider": "Batch09_Legacy",
                    "date_range": f"{first_date}-{last_date}",
                    "repo_path": promoted_repo_path,
                    "source_type": "historical_promote",
                    "source_csv": source_repo_path,
                    "source_metadata": map_rel,
                    "generator_entry": generator_rel,
                    "current_role": "formal_historical_runtime_input",
                    "evidence_mode": "historical_recovered",
                    "note": "由 batch09 原始快照归位提升；可作为 runtime 正式历史输入，但不冒充当前在线拉取",
                },
            )

        if source_dir.exists():
            try:
                source_dir.rmdir()
            except OSError:
                pass

    catalog_rows.sort(key=lambda r: (r["symbol"], r["provider"], r["repo_path"]))
    write_catalog(catalog_path, catalog_rows)
    write_map(map_path, promotion_rows)

    watchlist_parent = source_root / "ashare_watchlist"
    if watchlist_parent.exists():
        try:
            watchlist_parent.rmdir()
        except OSError:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
