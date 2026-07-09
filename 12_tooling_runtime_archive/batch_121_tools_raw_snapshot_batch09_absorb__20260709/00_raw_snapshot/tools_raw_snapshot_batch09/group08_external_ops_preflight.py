from __future__ import annotations

from pathlib import Path
import csv
import hashlib


REPO_ROOT = Path(__file__).resolve().parents[1]
GROUP08_ROOT = (
    REPO_ROOT
    / "10_来源库_SOURCE_LIBRARY"
    / "01_Kimi拆书待入库"
    / "GROUP_08_A股量化_数据研究"
)

MOVE_PLAN_TSV = GROUP08_ROOT / "GROUP_08_external_move_plan_v1.tsv"
DELETE_PLAN_TSV = GROUP08_ROOT / "GROUP_08_external_delete_candidate_plan_v1.tsv"
OUT_TSV = GROUP08_ROOT / "GROUP_08_external_ops_preflight_v1.tsv"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def file_size(path: Path) -> int:
    try:
        return path.stat().st_size
    except Exception:
        return -1


def main() -> None:
    move_rows = read_tsv(MOVE_PLAN_TSV)
    delete_rows = read_tsv(DELETE_PLAN_TSV)

    rows_out: list[dict[str, str]] = []

    def add_row(action: str, paper_id: str, src: str, dst_or_staging: str, outside_b: str, outside_f: str) -> None:
        src_path = Path(src) if src else None
        staging_path = Path(dst_or_staging) if dst_or_staging else None

        src_exists = "0"
        staging_exists = "0"
        src_size = ""
        staging_size = ""
        src_sha256 = ""
        staging_sha256 = ""
        sha_match = ""

        if src_path and src_path.exists() and src_path.is_file():
            src_exists = "1"
            src_size = str(file_size(src_path))
            src_sha256 = sha256_file(src_path)

        if staging_path and staging_path.exists() and staging_path.is_file():
            staging_exists = "1"
            staging_size = str(file_size(staging_path))
            staging_sha256 = sha256_file(staging_path)

        if src_sha256 and staging_sha256:
            sha_match = "1" if src_sha256 == staging_sha256 else "0"

        rows_out.append(
            {
                "paper_id": paper_id,
                "action": action,
                "source_path": src,
                "staging_path": dst_or_staging,
                "source_exists": src_exists,
                "staging_exists": staging_exists,
                "source_size": src_size,
                "staging_size": staging_size,
                "source_sha256": src_sha256,
                "staging_sha256": staging_sha256,
                "sha256_match": sha_match,
                "outside_refs_basename": outside_b,
                "outside_refs_fullpath": outside_f,
            }
        )

    for r in move_rows:
        add_row(
            action="MOVE",
            paper_id=(r.get("paper_id") or "").strip(),
            src=(r.get("source_path_before") or "").strip(),
            dst_or_staging=(r.get("repo_staging_path_after") or "").strip(),
            outside_b=(r.get("outside_refs_basename") or "0").strip(),
            outside_f=(r.get("outside_refs_fullpath") or "0").strip(),
        )

    for r in delete_rows:
        add_row(
            action="DELETE_CANDIDATE",
            paper_id=(r.get("paper_id") or "").strip(),
            src=(r.get("delete_candidate_path") or "").strip(),
            dst_or_staging=(r.get("repo_staging_path_after") or "").strip(),
            outside_b=(r.get("outside_refs_basename") or "0").strip(),
            outside_f=(r.get("outside_refs_fullpath") or "0").strip(),
        )

    rows_out.sort(key=lambda x: (x.get("action", ""), x.get("paper_id", "")))
    write_tsv(
        OUT_TSV,
        rows_out,
        [
            "paper_id",
            "action",
            "source_path",
            "staging_path",
            "source_exists",
            "staging_exists",
            "source_size",
            "staging_size",
            "sha256_match",
            "source_sha256",
            "staging_sha256",
            "outside_refs_basename",
            "outside_refs_fullpath",
        ],
    )

    total = len(rows_out)
    missing_src = sum(1 for r in rows_out if r["source_exists"] != "1")
    missing_staging = sum(1 for r in rows_out if r["staging_exists"] != "1")
    mismatch = sum(1 for r in rows_out if r["sha256_match"] == "0")
    ready = sum(
        1
        for r in rows_out
        if r["source_exists"] == "1" and r["staging_exists"] == "1" and r["sha256_match"] == "1"
    )

    print(f"rows_total={total}")
    print(f"ready_sha_match={ready}")
    print(f"missing_source={missing_src}")
    print(f"missing_staging={missing_staging}")
    print(f"sha_mismatch={mismatch}")
    print(f"out={OUT_TSV}")


if __name__ == "__main__":
    main()

