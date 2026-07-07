from __future__ import annotations

from pathlib import Path
import csv
import math
from collections import defaultdict


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

PREFLIGHT_TSV = GROUP08_ROOT / "GROUP_08_external_ops_preflight_v1.tsv"
MOVE_PLAN_TSV = GROUP08_ROOT / "GROUP_08_external_move_plan_v1.tsv"
DELETE_PLAN_TSV = GROUP08_ROOT / "GROUP_08_external_delete_candidate_plan_v1.tsv"
OUT_MD = GROUP08_ROOT / "GROUP_08_external_ops_stats_v1.md"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def to_int(text: str) -> int:
    try:
        return int((text or "0").strip())
    except Exception:
        return 0


def fmt_mb(n: int) -> str:
    return f"{n / (1024 * 1024):.1f}MB"


def main() -> None:
    pre = read_tsv(PREFLIGHT_TSV)
    move = read_tsv(MOVE_PLAN_TSV)
    delete = read_tsv(DELETE_PLAN_TSV)

    size_by_pid: dict[str, int] = {}
    for r in pre:
        pid = (r.get("paper_id") or "").strip()
        sz = to_int(r.get("source_size") or "0")
        if pid and sz > 0:
            size_by_pid[pid] = sz

    agg: dict[str, dict[str, int]] = defaultdict(lambda: {"count": 0, "bytes": 0})

    for r in move:
        pid = (r.get("paper_id") or "").strip()
        root = (r.get("root_type") or "").strip() or "UNKNOWN"
        key = f"MOVE::{root}"
        agg[key]["count"] += 1
        agg[key]["bytes"] += size_by_pid.get(pid, 0)

    for r in delete:
        pid = (r.get("paper_id") or "").strip()
        root = (r.get("root_type") or "").strip() or "UNKNOWN"
        key = f"DELETE_CANDIDATE::{root}"
        agg[key]["count"] += 1
        agg[key]["bytes"] += size_by_pid.get(pid, 0)

    lines: list[str] = []
    lines.append("# GROUP_08 External Ops Stats v1")
    lines.append("")
    lines.append(f"- move_rows: {len(move)}")
    lines.append(f"- delete_candidate_rows: {len(delete)}")
    lines.append("")
    lines.append("| action | root_type | count | size |")
    lines.append("|---|---:|---:|---:|")

    def sort_key(k: str) -> tuple[str, str]:
        a, b = k.split("::", 1)
        return (a, b)

    total_bytes = 0
    total_count = 0
    for k in sorted(agg.keys(), key=sort_key):
        action, root = k.split("::", 1)
        cnt = agg[k]["count"]
        bts = agg[k]["bytes"]
        total_bytes += bts
        total_count += cnt
        lines.append(f"| {action} | {root} | {cnt} | {fmt_mb(bts)} |")

    lines.append("")
    lines.append(f"- total_rows: {total_count}")
    lines.append(f"- total_size: {fmt_mb(total_bytes)}")
    lines.append("")
    lines.append("说明：这里的 size 以 `GROUP_08_external_ops_preflight_v1.tsv` 的 source_size 为准。")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"out={OUT_MD}")


if __name__ == "__main__":
    main()

