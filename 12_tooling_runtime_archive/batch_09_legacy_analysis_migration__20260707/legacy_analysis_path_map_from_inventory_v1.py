import argparse
import csv
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class MapRow:
    legacy_repo_path: str
    lifted_repo_path: str
    size_bytes: int
    mtime_utc: str
    sha256: str


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--inventory-tsv", required=True)
    p.add_argument("--out-map-tsv", required=True)
    p.add_argument("--out-summary", required=True)
    p.add_argument("--legacy-prefix", default="legacy_analysis")
    p.add_argument(
        "--lifted-prefix",
        default="12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_trading_analysis",
    )
    return p.parse_args()


def clean_prefix(raw: str) -> str:
    cleaned = raw.strip().strip("/").strip("\\")
    return cleaned.replace("\\", "/")


def join_posix(prefix: str, rel_path: str) -> str:
    prefix_clean = clean_prefix(prefix)
    rel_clean = rel_path.strip().lstrip("/").replace("\\", "/")
    if not prefix_clean:
        return rel_clean
    return f"{prefix_clean}/{rel_clean}"


def load_inventory_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return [dict(row) for row in reader]


def to_map_row(row: dict[str, str], legacy_prefix: str, lifted_prefix: str) -> Optional[MapRow]:
    rel_path = (row.get("rel_path") or "").strip()
    if not rel_path:
        return None
    return MapRow(
        legacy_repo_path=join_posix(legacy_prefix, rel_path),
        lifted_repo_path=join_posix(lifted_prefix, rel_path),
        size_bytes=int((row.get("size_bytes") or "0").strip() or "0"),
        mtime_utc=(row.get("mtime_utc") or "").strip(),
        sha256=(row.get("sha256") or "").strip(),
    )


def write_map_tsv(rows: list[MapRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("legacy_repo_path\tlifted_repo_path\tsize_bytes\tmtime_utc\tsha256\n")
        for r in rows:
            handle.write(
                f"{r.legacy_repo_path}\t{r.lifted_repo_path}\t{r.size_bytes}\t{r.mtime_utc}\t{r.sha256}\n"
            )


def write_summary(rows: list[MapRow], path: Path, legacy_prefix: str, lifted_prefix: str) -> None:
    payload = {
        "format": "legacy_analysis_path_map_v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "legacy_prefix": clean_prefix(legacy_prefix),
        "lifted_prefix": clean_prefix(lifted_prefix),
        "row_count": len(rows),
        "total_bytes": sum(r.size_bytes for r in rows),
        "sha256_coverage": sum(1 for r in rows if r.sha256) / len(rows) if rows else 0.0,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    args = parse_args()
    inventory_tsv = Path(args.inventory_tsv).resolve()
    out_map = Path(args.out_map_tsv).resolve()
    out_summary = Path(args.out_summary).resolve()
    legacy_prefix = str(args.legacy_prefix)
    lifted_prefix = str(args.lifted_prefix)

    rows = [
        item
        for item in (
            to_map_row(row, legacy_prefix=legacy_prefix, lifted_prefix=lifted_prefix)
            for row in load_inventory_rows(inventory_tsv)
        )
        if item is not None
    ]
    rows.sort(key=lambda r: r.legacy_repo_path)
    write_map_tsv(rows, out_map)
    write_summary(rows, out_summary, legacy_prefix=legacy_prefix, lifted_prefix=lifted_prefix)


if __name__ == "__main__":
    main()

