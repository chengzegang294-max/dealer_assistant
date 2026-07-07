import argparse
import csv
import os
import re
import shutil
from collections import Counter


L1_AUCTION = "01_集合竞价教程"
L1_YOUZI = "02_游资悟道交割单"
L1_REPORT = "03_券商研报"
L1_REVIEW = "04_待归类"

REPORT_BUCKETS = {
    "高频微观": "01_高频微观",
    "指数增强": "02_指数增强",
    "机器学习": "03_机器学习",
    "多因子": "04_多因子",
    "其他": "05_其他",
}


def normalize_name(name: str) -> str:
    base, ext = os.path.splitext(name.lower())
    base = re.sub(r"\(\d+\)$", "", base).strip()
    base = re.sub(r"（\d+）$", "", base).strip()
    base = re.sub(r"\s+", " ", base)
    return base + ext


def classify_report(filename: str) -> str:
    s = filename.lower()
    ml_kw = [
        "机器学习",
        "深度学习",
        "人工智能",
        "强化学习",
        "神经网络",
        "随机森林",
        "支持向量机",
        "boosting",
        "bert",
        "gan",
        "qlib",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "reinforcement learning",
        "cnn",
        "rnn",
        "graph",
        "无监督",
        "遗传规划",
        "文本挖掘",
        "attention",
        "alphanet",
    ]
    index_kw = [
        "指数增强",
        "沪深300",
        "中证500",
        "上证50",
        "etf",
        "portable_alpha",
        "增强策略",
        "基差预测",
    ]
    micro_kw = [
        "高频",
        "微观结构",
        "market microstructure",
        "microstructure",
        "order book",
        "订单",
        "订单簿",
        "逐笔",
        "快照",
        "level2",
        "level 2",
        "指令流",
        "知情交易",
        "流动性",
        "主动成交",
        "价差",
        "折溢价",
        "日内",
        "成交量时钟",
        "波动率分解",
        "情绪温度计",
        "交易成本",
    ]
    multifactor_kw = [
        "多因子",
        "因子",
        "barra",
        "alpha",
        "选股",
        "风格因子",
        "因子择时",
        "收益预测模型",
        "风险模型",
        "组合优化",
    ]
    if any(k in s for k in ml_kw):
        return REPORT_BUCKETS["机器学习"]
    if any(k in s for k in index_kw):
        return REPORT_BUCKETS["指数增强"]
    if any(k in s for k in micro_kw):
        return REPORT_BUCKETS["高频微观"]
    if any(k in s for k in multifactor_kw):
        return REPORT_BUCKETS["多因子"]
    return REPORT_BUCKETS["其他"]


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def move_dir_if_exists(root: str, old_name: str, new_name: str) -> tuple[bool, str]:
    src = os.path.join(root, old_name)
    dst = os.path.join(root, new_name)
    if not os.path.isdir(src):
        return False, dst
    if os.path.abspath(src) == os.path.abspath(dst):
        return True, dst
    if os.path.exists(dst):
        for dirpath, _, filenames in os.walk(src):
            rel = os.path.relpath(dirpath, src)
            target_dir = dst if rel == "." else os.path.join(dst, rel)
            ensure_dir(target_dir)
            for fn in filenames:
                src_file = os.path.join(dirpath, fn)
                dst_file = os.path.join(target_dir, fn)
                if os.path.exists(dst_file):
                    continue
                shutil.move(src_file, dst_file)
        for dirpath, dirnames, filenames in os.walk(src, topdown=False):
            if not dirnames and not filenames:
                os.rmdir(dirpath)
        if os.path.isdir(src) and not os.listdir(src):
            os.rmdir(src)
        return True, dst
    shutil.move(src, dst)
    return True, dst


def guess_info_density(ext: str, bucket_l1: str, bucket_l2: str, name: str) -> str:
    ext = ext.lower()
    if ext == ".md":
        return "medium"
    if ext in (".doc", ".docx"):
        return "medium"
    if ext == ".pdf":
        if bucket_l1 == L1_REPORT and bucket_l2 in (
            REPORT_BUCKETS["高频微观"],
            REPORT_BUCKETS["机器学习"],
            REPORT_BUCKETS["多因子"],
            REPORT_BUCKETS["指数增强"],
        ):
            return "high"
        return "medium"
    return "low"


def guess_next_action(bucket_l1: str, bucket_l2: str, ext: str) -> str:
    if bucket_l1 in (L1_AUCTION, L1_YOUZI):
        return "compare_first"
    if bucket_l1 == L1_REPORT:
        if bucket_l2 == REPORT_BUCKETS["其他"]:
            return "index_only"
        return "compare_first"
    return "review"


def stage_bucket_subset(
    root: str,
    inventory_rows: list[dict[str, str]],
    bucket_l1: str,
    stage_dest_root: str,
    stage_proof_out: str,
) -> dict[str, int]:
    ensure_dir(stage_dest_root)
    ensure_dir(os.path.dirname(os.path.abspath(stage_proof_out)))

    stats = {
        "staged_rows": 0,
        "stage_copied": 0,
        "stage_existing_ok": 0,
        "stage_missing_source": 0,
        "stage_size_mismatch": 0,
    }

    with open(stage_proof_out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(
            [
                "bucket_l1",
                "file_name",
                "source_path",
                "staging_path",
                "source_exists",
                "staging_exists",
                "source_size",
                "staging_size",
                "stage_status",
            ]
        )
        for row in inventory_rows:
            if row["bucket_l1"] != bucket_l1:
                continue
            stats["staged_rows"] += 1
            source_path = row["current_path"]
            rel = os.path.relpath(source_path, root)
            staging_path = os.path.join(stage_dest_root, rel)
            ensure_dir(os.path.dirname(staging_path))

            source_exists = os.path.exists(source_path)
            source_size = os.path.getsize(source_path) if source_exists else 0

            if source_exists and not os.path.exists(staging_path):
                shutil.copy2(source_path, staging_path)

            staging_exists = os.path.exists(staging_path)
            staging_size = os.path.getsize(staging_path) if staging_exists else 0

            if not source_exists:
                status = "MISSING_SOURCE"
                stats["stage_missing_source"] += 1
            elif not staging_exists:
                status = "COPY_FAILED"
                stats["stage_size_mismatch"] += 1
            elif source_size != staging_size:
                status = "SIZE_MISMATCH"
                stats["stage_size_mismatch"] += 1
            elif os.path.getmtime(staging_path) == os.path.getmtime(source_path):
                status = "COPIED_OR_SYNCED"
                stats["stage_copied"] += 1
            else:
                status = "EXISTING_OK"
                stats["stage_existing_ok"] += 1

            w.writerow(
                [
                    bucket_l1,
                    row["file_name"],
                    source_path,
                    staging_path,
                    int(source_exists),
                    int(staging_exists),
                    source_size,
                    staging_size,
                    status,
                ]
            )

    return stats


def load_selected_paths(tsv_path: str) -> set[str]:
    selected: set[str] = set()
    with open(tsv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            current_path = (row.get("current_path") or "").strip()
            if current_path:
                selected.add(os.path.abspath(current_path))
    return selected


def stage_selected_subset(
    root: str,
    inventory_rows: list[dict[str, str]],
    selected_paths: set[str],
    stage_dest_root: str,
    stage_proof_out: str,
) -> dict[str, int]:
    ensure_dir(stage_dest_root)
    ensure_dir(os.path.dirname(os.path.abspath(stage_proof_out)))

    stats = {
        "staged_rows": 0,
        "stage_copied": 0,
        "stage_existing_ok": 0,
        "stage_missing_source": 0,
        "stage_size_mismatch": 0,
        "stage_selection_total": len(selected_paths),
        "stage_selection_matched": 0,
    }

    matched_paths: set[str] = set()
    with open(stage_proof_out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(
            [
                "bucket_l1",
                "bucket_l2",
                "file_name",
                "source_path",
                "staging_path",
                "source_exists",
                "staging_exists",
                "source_size",
                "staging_size",
                "stage_status",
            ]
        )
        for row in inventory_rows:
            source_path = os.path.abspath(row["current_path"])
            if source_path not in selected_paths:
                continue
            matched_paths.add(source_path)
            stats["staged_rows"] += 1
            rel = os.path.relpath(source_path, root)
            staging_path = os.path.join(stage_dest_root, rel)
            ensure_dir(os.path.dirname(staging_path))

            source_exists = os.path.exists(source_path)
            source_size = os.path.getsize(source_path) if source_exists else 0

            if source_exists and not os.path.exists(staging_path):
                shutil.copy2(source_path, staging_path)

            staging_exists = os.path.exists(staging_path)
            staging_size = os.path.getsize(staging_path) if staging_exists else 0

            if not source_exists:
                status = "MISSING_SOURCE"
                stats["stage_missing_source"] += 1
            elif not staging_exists:
                status = "COPY_FAILED"
                stats["stage_size_mismatch"] += 1
            elif source_size != staging_size:
                status = "SIZE_MISMATCH"
                stats["stage_size_mismatch"] += 1
            elif os.path.getmtime(staging_path) == os.path.getmtime(source_path):
                status = "COPIED_OR_SYNCED"
                stats["stage_copied"] += 1
            else:
                status = "EXISTING_OK"
                stats["stage_existing_ok"] += 1

            w.writerow(
                [
                    row["bucket_l1"],
                    row["bucket_l2"],
                    row["file_name"],
                    source_path,
                    staging_path,
                    int(source_exists),
                    int(staging_exists),
                    source_size,
                    staging_size,
                    status,
                ]
            )

    stats["stage_selection_matched"] = len(matched_paths)
    stats["stage_selection_missing_from_inventory"] = len(selected_paths - matched_paths)
    return stats


def bucketize(root: str, inventory_out: str) -> dict[str, int]:
    ensure_dir(os.path.join(root, L1_REVIEW))
    _, auction_dir = move_dir_if_exists(root, "集合竞价教程", L1_AUCTION)
    _, youzi_dir = move_dir_if_exists(root, "游资交割单+悟道心法", L1_YOUZI)
    report_src = os.path.join(root, "券商研报")
    report_root = os.path.join(root, L1_REPORT)
    ensure_dir(report_root)
    for bucket in REPORT_BUCKETS.values():
        ensure_dir(os.path.join(report_root, bucket))

    moved_reports = 0
    if os.path.isdir(report_src):
        for fn in list(os.listdir(report_src)):
            src = os.path.join(report_src, fn)
            if not os.path.isfile(src):
                continue
            bucket = classify_report(fn)
            dst = os.path.join(report_root, bucket, fn)
            if not os.path.exists(dst):
                shutil.move(src, dst)
                moved_reports += 1
        if os.path.isdir(report_src) and not os.listdir(report_src):
            os.rmdir(report_src)

    moved_review = 0
    for fn in list(os.listdir(root)):
        src = os.path.join(root, fn)
        if not os.path.isfile(src):
            continue
        dst = os.path.join(root, L1_REVIEW, fn)
        if not os.path.exists(dst):
            shutil.move(src, dst)
            moved_review += 1

    all_files: list[tuple[str, str, int]] = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            path = os.path.join(dirpath, fn)
            try:
                size = os.path.getsize(path)
            except OSError:
                size = 0
            all_files.append((path, fn, size))
    norm_counts = Counter(normalize_name(fn) for _, fn, _ in all_files)

    ensure_dir(os.path.dirname(os.path.abspath(inventory_out)))
    inventory_rows: list[dict[str, str]] = []
    with open(inventory_out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(
            [
                "file_name",
                "ext",
                "size_bytes",
                "current_path",
                "bucket_l1",
                "bucket_l2",
                "duplicate_candidate",
                "info_density_guess",
                "next_action",
            ]
        )
        for path, fn, size in sorted(all_files, key=lambda x: x[0].lower()):
            rel = os.path.relpath(path, root)
            parts = rel.split(os.sep)
            bucket_l1 = parts[0] if parts else ""
            bucket_l2 = parts[1] if len(parts) > 2 and bucket_l1 == L1_REPORT else ""
            ext = os.path.splitext(fn)[1].lower()
            dup = "y" if norm_counts[normalize_name(fn)] > 1 else "n"
            info_density = guess_info_density(ext, bucket_l1, bucket_l2, fn)
            next_action = guess_next_action(bucket_l1, bucket_l2, ext)
            inventory_rows.append(
                {
                    "file_name": fn,
                    "ext": ext,
                    "size_bytes": str(size),
                    "current_path": path,
                    "bucket_l1": bucket_l1,
                    "bucket_l2": bucket_l2,
                    "duplicate_candidate": dup,
                    "info_density_guess": info_density,
                    "next_action": next_action,
                }
            )
            w.writerow(
                [
                    fn,
                    ext,
                    size,
                    path,
                    bucket_l1,
                    bucket_l2,
                    dup,
                    info_density,
                    next_action,
                ]
            )

    return {
        "files_total": len(all_files),
        "moved_reports": moved_reports,
        "moved_review": moved_review,
        "auction_exists": int(os.path.isdir(auction_dir)),
        "youzi_exists": int(os.path.isdir(youzi_dir)),
        "report_root_exists": int(os.path.isdir(report_root)),
        "_inventory_rows": inventory_rows,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--inventory-out", required=True)
    ap.add_argument("--stage-bucket-l1")
    ap.add_argument("--stage-select-tsv")
    ap.add_argument("--stage-dest-root")
    ap.add_argument("--stage-proof-out")
    args = ap.parse_args()
    stats = bucketize(os.path.abspath(args.root), os.path.abspath(args.inventory_out))
    inventory_rows = stats.pop("_inventory_rows")

    stage_mode_args = [
        args.stage_bucket_l1,
        args.stage_select_tsv,
        args.stage_dest_root,
        args.stage_proof_out,
    ]
    if any(stage_mode_args):
        if not all([args.stage_dest_root, args.stage_proof_out]):
            raise SystemExit(
                "staging requires --stage-dest-root and --stage-proof-out together"
            )
        if bool(args.stage_bucket_l1) == bool(args.stage_select_tsv):
            raise SystemExit(
                "choose exactly one staging selector: --stage-bucket-l1 or --stage-select-tsv"
            )
        if args.stage_bucket_l1:
            stage_stats = stage_bucket_subset(
                os.path.abspath(args.root),
                inventory_rows,
                args.stage_bucket_l1,
                os.path.abspath(args.stage_dest_root),
                os.path.abspath(args.stage_proof_out),
            )
        else:
            selected_paths = load_selected_paths(os.path.abspath(args.stage_select_tsv))
            stage_stats = stage_selected_subset(
                os.path.abspath(args.root),
                inventory_rows,
                selected_paths,
                os.path.abspath(args.stage_dest_root),
                os.path.abspath(args.stage_proof_out),
            )
        stats.update(stage_stats)

    for k, v in stats.items():
        print(f"{k}={v}")
    print(f"inventory_out={os.path.abspath(args.inventory_out)}")
    if args.stage_proof_out:
        print(f"stage_proof_out={os.path.abspath(args.stage_proof_out)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
