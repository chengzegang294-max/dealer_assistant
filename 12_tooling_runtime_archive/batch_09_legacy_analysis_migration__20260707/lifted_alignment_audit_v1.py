import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class InventoryRow:
    rel_path: str
    size_bytes: int
    mtime_utc: str
    sha256: str


@dataclass(frozen=True)
class AuditRow:
    lifted_rel_path: str
    category: str
    proposed_target_rel_path: str
    target_exists: bool
    target_sha256_match: str
    size_bytes: int
    sha256: str


ROOT_DOCS = (
    "00_主线检索索引.md",
    "01_阶段一_项目记录_过去与落地.md",
    "02_阶段二_工作方向_想法库.md",
    "03_阶段二_当下计划_执行清单.md",
    "关于日活.md",
    "PLAYBOOK_滚动模板.md",
    "ashare_daily_ops.md",
)

KIMI_PREFIX_REWRITES: tuple[tuple[str, str], ...] = (
    (
        "GROUP_08_A股量化_数据研究__SOURCE_RAW/",
        "GROUP_08_A股量化_数据研究/01_source_raw/",
    ),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", required=True)
    p.add_argument("--lifted-root", required=True)
    p.add_argument("--inventory-tsv", required=True)
    p.add_argument("--out-tsv", required=True)
    p.add_argument("--out-summary", required=True)
    return p.parse_args()


def load_inventory(path: Path) -> list[InventoryRow]:
    rows: list[InventoryRow] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            rel = (row.get("rel_path") or "").strip().replace("\\", "/")
            if not rel:
                continue
            rows.append(
                InventoryRow(
                    rel_path=rel,
                    size_bytes=int((row.get("size_bytes") or "0").strip() or "0"),
                    mtime_utc=(row.get("mtime_utc") or "").strip(),
                    sha256=(row.get("sha256") or "").strip(),
                )
            )
    return rows


def norm_posix(path: str) -> str:
    return path.replace("\\", "/").lstrip("/")


def rewrite_kimi_inbox_rel(rest: str) -> str:
    rel = norm_posix(rest)
    for src, dst in KIMI_PREFIX_REWRITES:
        src_norm = norm_posix(src)
        dst_norm = norm_posix(dst)
        if rel.startswith(src_norm):
            return dst_norm + rel.split(src_norm, 1)[1]
    return rel


def map_target(rel_path: str) -> tuple[str, str]:
    rel = norm_posix(rel_path)
    if rel in ROOT_DOCS:
        return (
            "active_main_docs",
            f"04_active_main_docs/batch_01_selected/{Path(rel).name}",
        )

    if rel == "docs/ops/ashare_daily_ops.md":
        return ("active_main_docs", "04_active_main_docs/batch_01_selected/ashare_daily_ops.md")

    if rel == "docs/playbooks/PLAYBOOK_滚动模板.md":
        return ("active_main_docs", "04_active_main_docs/batch_01_selected/PLAYBOOK_滚动模板.md")

    if rel.startswith(".vscode/"):
        return ("repo_settings", rel)

    if rel.startswith(".trae/"):
        if rel == ".trae/README__ARCHIVE_ONLY.md":
            return ("trae_mirror_select", "21_trae_system_archive/batch_01_selected/README.md")
        if rel == ".trae/agents/README__ARCHIVE_ONLY.md":
            return ("trae_mirror_select", "21_trae_system_archive/batch_02_selected/README.md")
        if rel == ".trae/agents/p0-exec-evidence-officer/PROMPT.md":
            return ("trae_mirror_select", "21_trae_system_archive/batch_02_selected/p0-exec-evidence-officer_PROMPT.md")
        return ("trae_raw_snapshot", f"21_trae_system_archive/_raw_snapshot_batch09/{rel}")

    if rel.startswith("docs/commit_ready_stage_batch_") or rel.startswith("docs/commit_ready_batch_"):
        return (
            "commit_helpers",
            f"12_tooling_runtime_archive/batch_06_legacy_commit_helpers__20260706/legacy_docs_commit_helpers/{rel.split('/', 1)[1]}",
        )

    if rel.startswith("docs/") and ("__EVAL__" in rel or rel.startswith("docs/COMMIT_READY__BATCH_")):
        return (
            "docs_batches",
            f"12_tooling_runtime_archive/batch_07_legacy_docs_batches__20260706/legacy_docs_batches/{rel.split('/', 1)[1]}",
        )

    if rel.startswith("docs/"):
        return (
            "docs_backlog_or_other",
            f"12_tooling_runtime_archive/batch_08_legacy_docs_backlog__20260706/legacy_docs_backlog/{rel.split('/', 1)[1]}",
        )

    if rel.startswith("backtest_out/"):
        return ("backtest_out_archive", f"12_tooling_runtime_archive/batch_04_legacy_backtest_out__20260706/{rel}")

    if rel.startswith("10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/"):
        rest = rel.split("10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/", 1)[1]
        rewritten = rewrite_kimi_inbox_rel(rest)
        return ("source_library_mirror", f"10_source_library_archive/mirror_kimi_inbox/{rewritten}")

    if rel.startswith("11_冻结总结层_FROZEN_SUMMARIES/"):
        rest = rel.split("11_冻结总结层_FROZEN_SUMMARIES/", 1)[1]
        return ("frozen_summaries_raw_snapshot", f"11_frozen_summaries_archive/_raw_snapshot_batch09/{rest}")

    if rel.startswith("12_工具运行时_TOOLING_RUNTIME/"):
        rest = rel.split("12_工具运行时_TOOLING_RUNTIME/", 1)[1]
        return (
            "tooling_runtime_raw_snapshot",
            f"12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_trading_analysis/12_工具运行时_TOOLING_RUNTIME/{rest}",
        )

    if rel.startswith("DY_R1_KD_MTF_P0/"):
        return ("dy_family_raw_snapshot", f"12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_trading_analysis/{rel}")

    if rel.startswith("tools/"):
        return ("tools_unclassified", f"20_tools_workspace/_raw_snapshot_batch09/{rel.split('/',1)[1]}")

    if rel.startswith("data/"):
        return ("data_unclassified", f"00_assets/_raw_snapshot_batch09/{rel.split('/',1)[1]}")

    if rel.startswith("10_来源库_SOURCE_LIBRARY/"):
        rest = rel.split("10_来源库_SOURCE_LIBRARY/", 1)[1]
        return (
            "source_library_raw_snapshot",
            f"10_source_library_archive/_raw_snapshot_batch09/10_来源库_SOURCE_LIBRARY/{rest}",
        )

    return ("unclassified", f"12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_trading_analysis/{rel}")


def sha256_if_small(path: Path, size_bytes: int, limit_bytes: int = 10 * 1024 * 1024) -> Optional[str]:
    if size_bytes > limit_bytes:
        return None
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def write_tsv(rows: list[AuditRow], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(
            "lifted_rel_path\tcategory\tproposed_target_rel_path\ttarget_exists\ttarget_sha256_match\tsize_bytes\tsha256\n"
        )
        for r in rows:
            handle.write(
                f"{r.lifted_rel_path}\t{r.category}\t{r.proposed_target_rel_path}\t{int(r.target_exists)}\t{r.target_sha256_match}\t{r.size_bytes}\t{r.sha256}\n"
            )


def write_summary(rows: list[AuditRow], out_path: Path, args: argparse.Namespace) -> None:
    by_cat: dict[str, int] = {}
    by_cat_exists: dict[str, int] = {}
    for r in rows:
        by_cat[r.category] = by_cat.get(r.category, 0) + 1
        if r.target_exists:
            by_cat_exists[r.category] = by_cat_exists.get(r.category, 0) + 1
    summary = {
        "format": "lifted_alignment_audit_v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(Path(args.repo_root).resolve()),
        "lifted_root": str(Path(args.lifted_root).resolve()),
        "inventory_tsv": str(Path(args.inventory_tsv).resolve()),
        "row_count": len(rows),
        "category_counts": dict(sorted(by_cat.items(), key=lambda x: (-x[1], x[0]))),
        "category_target_exists_counts": dict(sorted(by_cat_exists.items(), key=lambda x: (-x[1], x[0]))),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    lifted_root = Path(args.lifted_root).resolve()
    inventory_tsv = Path(args.inventory_tsv).resolve()
    out_tsv = Path(args.out_tsv).resolve()
    out_summary = Path(args.out_summary).resolve()

    items = load_inventory(inventory_tsv)
    rows: list[AuditRow] = []
    for item in items:
        category, target_rel = map_target(item.rel_path)
        target_abs = repo_root / Path(target_rel)
        target_exists = target_abs.exists()
        sha_match = ""
        if target_exists and item.sha256 and item.size_bytes > 0:
            other = sha256_if_small(target_abs, size_bytes=int(target_abs.stat().st_size))
            if other is not None:
                sha_match = "1" if other == item.sha256 else "0"
            else:
                sha_match = "SKIP_LARGE"
        rows.append(
            AuditRow(
                lifted_rel_path=item.rel_path,
                category=category,
                proposed_target_rel_path=norm_posix(target_rel),
                target_exists=target_exists,
                target_sha256_match=sha_match,
                size_bytes=item.size_bytes,
                sha256=item.sha256,
            )
        )

    rows.sort(key=lambda r: (r.category, r.lifted_rel_path))
    write_tsv(rows, out_tsv)
    write_summary(rows, out_summary, args)


if __name__ == "__main__":
    main()
