import os
import csv
from datetime import datetime, timedelta
from pathlib import Path

TOOLS_ROOT = Path(r"D:\Stock\trading_assistant\20_tools_workspace")
OUTPUT_DIR = Path(r"D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_oldrepo_cleanup__20260811")
STAT_TSV = OUTPUT_DIR / "tools_top_level_stat__20260811.tsv"
RULING_TSV = OUTPUT_DIR / "tools_batch_ruling__20260811.tsv"

TODAY = datetime(2026, 8, 11)
ONE_YEAR_AGO = TODAY - timedelta(days=365)
AUG_2026 = datetime(2026, 8, 1)
JULY_2026 = datetime(2026, 7, 1)

MAINLINE_KEYWORDS = [
    ["ingest", "capture", "snapshot", "extract", "export", "inventory", "quicktiny", "接入", "采集", "快照", "抽取", "导出"],
    ["backtest", "pipeline", "score", "review", "analyze", "selected", "group08", "live", "room", "info", "回测", "流水线", "评分", "复盘", "分析", "直播"],
    ["home", "frontend", "ui", "page", "component", "a5_p0", "前端", "页面", "组件"],
    ["document", "manual", "sheet", "md", "tk_r", "文档", "手册", "说明", "人工表"],
]

BATCH_DIR_NAMES = [
    "batch_01_selected",
    "batch_02_group08_pipeline",
    "batch_03_general_ingest_tools",
    "batch_04_tk_r6_manual_sheet_tools",
    "batch_05_tk_r7_manual_sheet_tools",
    "batch_06_tk_r8_manual_sheet_tools",
    "batch_07_info_live_room_tools",
    "batch_08_quicktiny_capture_tools",
    "_raw_snapshot_batch09",
    "a5_p0_home_batch1_frontend",
]


def scan_all_files(root: Path):
    all_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            fp = Path(dirpath) / fn
            try:
                st = fp.stat()
                all_files.append({
                    "path": fp,
                    "size_kb": st.st_size / 1024.0,
                    "mtime": datetime.fromtimestamp(st.st_mtime),
                })
            except (OSError, PermissionError):
                pass
    return all_files


def collect_batch_stats(all_files):
    batch_stats = {}
    for dname in BATCH_DIR_NAMES:
        dpath = TOOLS_ROOT / dname
        if not dpath.exists():
            continue
        files_in_batch = [f for f in all_files if str(f["path"]).startswith(str(dpath) + os.sep)]
        total_size_kb = sum(f["size_kb"] for f in files_in_batch)
        latest_mtime = max((f["mtime"] for f in files_in_batch), default=None)
        has_readme = any(
            f["path"].parent == dpath and f["path"].name.lower() in ("readme.md", "readme.txt", "readme")
            for f in files_in_batch
        )
        has_requirements = any(
            f["path"].parent == dpath and f["path"].name.lower() == "requirements.txt"
            for f in files_in_batch
        )
        has_py = any(f["path"].suffix.lower() == ".py" for f in files_in_batch)
        batch_stats[dname] = {
            "dir_name": dname,
            "file_count": len(files_in_batch),
            "total_size_kb": round(total_size_kb, 2),
            "latest_mtime": latest_mtime.strftime("%Y-%m-%d") if latest_mtime else "",
            "has_readme": "Y" if has_readme else "N",
            "has_requirements": "Y" if has_requirements else "N",
            "has_py": "Y" if has_py else "N",
        }
    return batch_stats


def match_mainline(dir_name: str) -> int:
    matched = 0
    lower = dir_name.lower()
    for kw_group in MAINLINE_KEYWORDS:
        if any(kw.lower() in lower for kw in kw_group):
            matched += 1
    return matched


def make_ruling(stat_row):
    dir_name = stat_row["dir_name"]
    latest = datetime.strptime(stat_row["latest_mtime"], "%Y-%m-%d") if stat_row["latest_mtime"] else None
    has_readme = stat_row["has_readme"] == "Y"
    file_count = stat_row["file_count"]
    mainline_hits = match_mainline(dir_name)

    is_aug_2026_plus = latest is not None and latest >= AUG_2026
    is_july_2026_plus = latest is not None and latest >= JULY_2026
    is_over_1yr = latest is not None and latest < ONE_YEAR_AGO
    empty_shell_no_readme = (not has_readme) and file_count <= 3

    reasons = []
    ruling = "待裁决"

    absorb_conditions = []
    if is_aug_2026_plus:
        absorb_conditions.append("202608后活跃")
    elif is_july_2026_plus:
        absorb_conditions.append("202607后活跃")
    if has_readme:
        absorb_conditions.append("有README")
    if mainline_hits >= 1:
        absorb_conditions.append(f"主线命中{mainline_hits}条")

    delete_conditions = []
    if is_over_1yr:
        delete_conditions.append(">1年未更新")
    if empty_shell_no_readme:
        delete_conditions.append("零README空壳")

    strong_absorb = (is_aug_2026_plus and has_readme and mainline_hits >= 1)
    medium_absorb = (is_july_2026_plus and has_readme and mainline_hits >= 2)

    if strong_absorb or medium_absorb:
        ruling = "可吸收"
        reasons = absorb_conditions
    elif delete_conditions:
        ruling = "可删除"
        reasons = delete_conditions
    else:
        ruling = "待裁决"
        pending_reasons = []
        if not is_july_2026_plus:
            pending_reasons.append("非2026年活跃")
        if not has_readme:
            pending_reasons.append("无README")
        if mainline_hits == 0:
            pending_reasons.append("与主线无关")
        elif mainline_hits < 2:
            pending_reasons.append(f"主线弱关联({mainline_hits})")
        reasons = pending_reasons if pending_reasons else absorb_conditions

    return ruling, mainline_hits, "、".join(reasons)


def main():
    print(f"[1/4] 扫描文件中: {TOOLS_ROOT}")
    all_files = scan_all_files(TOOLS_ROOT)
    print(f"      共发现 {len(all_files)} 个文件，总大小 {round(sum(f['size_kb'] for f in all_files)/1024, 2)} MB")

    print(f"[2/4] 收集 batch 目录统计...")
    batch_stats = collect_batch_stats(all_files)

    stat_rows = list(batch_stats.values())
    stat_rows.sort(key=lambda r: r["total_size_kb"], reverse=True)

    with open(STAT_TSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["目录名", "文件数", "大小KB", "最新文件日期", "含README", "含requirements.txt", "含.py脚本"])
        for r in stat_rows:
            w.writerow([
                r["dir_name"], r["file_count"], r["total_size_kb"],
                r["latest_mtime"], r["has_readme"], r["has_requirements"], r["has_py"],
            ])
    print(f"      已写入 {STAT_TSV.name} ({len(stat_rows)} 行)")

    print(f"[3/4] Top20 大文件抽样 + 裁决生成...")
    all_files_sorted = sorted(all_files, key=lambda f: f["size_kb"], reverse=True)
    top20 = all_files_sorted[:20]

    ruling_rows = []
    for r in stat_rows:
        ruling, ml_hits, reasons = make_ruling(r)
        ruling_rows.append({
            "dir_name": r["dir_name"],
            "file_count": r["file_count"],
            "total_size_kb": r["total_size_kb"],
            "latest_mtime": r["latest_mtime"],
            "has_readme": r["has_readme"],
            "has_py": r["has_py"],
            "mainline_hits": ml_hits,
            "ruling": ruling,
            "reasons": reasons,
        })

    with open(RULING_TSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow([
            "目录名", "文件数", "大小KB", "最新文件日期",
            "含README", "含.py", "主线命中数", "裁决", "理由"
        ])
        for r in ruling_rows:
            w.writerow([
                r["dir_name"], r["file_count"], r["total_size_kb"],
                r["latest_mtime"], r["has_readme"], r["has_py"],
                r["mainline_hits"], r["ruling"], r["reasons"],
            ])
        w.writerow([])
        w.writerow(["===== Top20 大文件抽样 ====="])
        w.writerow(["排名", "大小KB", "修改日期", "相对路径"])
        for i, f in enumerate(top20, 1):
            rel = f["path"].relative_to(TOOLS_ROOT)
            w.writerow([i, round(f["size_kb"], 2), f["mtime"].strftime("%Y-%m-%d"), str(rel)])
    print(f"      已写入 {RULING_TSV.name}")

    print("\n" + "=" * 100)
    print("【 tools_top_level_stat 全表 】")
    print("=" * 100)
    header = f"{'目录名':<38} {'文件数':>6} {'大小KB':>10} {'最新日期':>12} {'README':>6} {'req.txt':>7} {'py':>3}"
    print(header)
    print("-" * len(header))
    for r in stat_rows:
        print(
            f"{r['dir_name']:<38} {r['file_count']:>6} {r['total_size_kb']:>10.2f} "
            f"{r['latest_mtime']:>12} {r['has_readme']:>6} {r['has_requirements']:>7} {r['has_py']:>3}"
        )

    print("\n" + "=" * 100)
    print("【 Top20 大文件 · 前10行 】")
    print("=" * 100)
    hdr2 = f"{'#':>3} {'大小KB':>10} {'修改日期':>12}  路径"
    print(hdr2)
    print("-" * len(hdr2))
    for i, f in enumerate(top20[:10], 1):
        rel = f["path"].relative_to(TOOLS_ROOT)
        print(f"{i:>3} {f['size_kb']:>10.2f} {f['mtime'].strftime('%Y-%m-%d'):>12}  {rel}")

    print("\n" + "=" * 100)
    print("【 tools_batch_ruling 摘要 】")
    print("=" * 100)
    counts = {"可吸收": 0, "待裁决": 0, "可删除": 0}
    for r in ruling_rows:
        counts[r["ruling"]] = counts.get(r["ruling"], 0) + 1
    print(f"  可吸收: {counts['可吸收']}   待裁决: {counts['待裁决']}   可删除: {counts['可删除']}")
    print("-" * 100)
    hdr3 = f"{'裁决':<6} {'目录名':<38} {'主线':>4}  理由"
    print(hdr3)
    print("-" * len(hdr3))
    for r in ruling_rows:
        print(f"{r['ruling']:<6} {r['dir_name']:<38} {r['mainline_hits']:>4}  {r['reasons']}")

    print(f"\n[完成] 输出文件:")
    print(f"  1. {STAT_TSV}")
    print(f"  2. {RULING_TSV}")


if __name__ == "__main__":
    main()
