"""
migrate_raw_from_batch05_and_batch07_to_rooms_v1.py
用途：信息直播间 batch 的 00_raw/*.json 按房间名复制到 rooms/<房名>/00_raw/
家族根：d:/Stock/dealer_assistant/02_runtime/info_live_room_sampling/rooms

用例：
  python migrate_raw_from_batch05_and_batch07_to_rooms_v1.py
  python migrate_raw_from_batch05_and_batch07_to_rooms_v1.py --apply
  python migrate_raw_from_batch05_and_batch07_to_rooms_v1.py --apply --batch-dir ../../02_runtime/info_live_room_sampling/batch_07_daily_close__20260810/00_raw

说明：默认 dry-run（无 --apply）；复制不移动；不替你出站抓站。
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOMS_24 = [
    # 每日 A8 + B14；末尾两间为 FROZEN_OUT（仍可 migrate 入库，不参与每日置顶）
    "复盘哥",
    "独家老师5号",
    "独家短线老师6号",
    "梅森",
    "顺势而为",
    "混江龙",
    "天赢居",
    "先知",
    "天机",
    "游资胖大叔",
    "潜伏王者",
    "k神",
    "周期女王",
    "格兰投研",
    "擒龙小师姐",
    "独家竞价低吸",
    "小锦鲤",
    "核心逻辑社",
    "梦幻一步",
    "新生代",
    "龙头交易猿",
    "小作文嗅嗅+机构研报",
    "机构电话会议纪要+小作文+情报",  # FROZEN_OUT F1
    "机构研报资讯精选",  # FROZEN_OUT F2
]
ROOMS_SET = set(ROOMS_24)

ROOM_ALIASES = {
    "独家5号": "独家老师5号",
    "独家6号": "独家短线老师6号",
    "短线6号": "独家短线老师6号",
    "机构电话+小作文": "机构电话会议纪要+小作文+情报",
    "K神": "k神",
    "格兰": "格兰投研",
    "小师姐": "擒龙小师姐",
    "机构研报精选": "机构研报资讯精选",
    "小作文嗅嗅": "小作文嗅嗅+机构研报",
    "天机短线试更新": "天机",
}


def resolve_room(raw: str) -> str | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    if raw in ROOMS_SET:
        return raw
    if raw in ROOM_ALIASES:
        return ROOM_ALIASES[raw]
    for formal in ROOMS_24:
        if raw == formal or raw.startswith(formal) or formal.startswith(raw):
            return formal
    if raw.startswith("天机"):
        return "天机"
    if raw.startswith("周期女王"):
        return "周期女王"
    return None


def detect_room_name(json_path: Path) -> str | None:
    """优先 JSON.room_anchor / forced_room_anchor；否则父目录（priority_rooms/<房>/）。"""
    data = None
    try:
        with json_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = None

    if isinstance(data, dict):
        for k in ("room_anchor", "forced_room_anchor", "source_room", "room_name", "room"):
            hit = resolve_room(str(data.get(k) or ""))
            if hit:
                return hit
        heur = data.get("heuristics")
        if isinstance(heur, dict):
            for k in (
                "forced_room_anchor",
                "room_anchor_candidate",
                "initial_room_anchor_candidate",
            ):
                hit = resolve_room(str(heur.get(k) or ""))
                if hit:
                    return hit

    return resolve_room(json_path.parent.name)


def iter_candidate_files(batch_dirs: list[Path]):
    for bd in batch_dirs:
        if not bd.exists():
            continue
        for p in bd.rglob("info_live_*export*.json"):
            if p.is_file():
                yield p


def main() -> int:
    ap = argparse.ArgumentParser(description="复制 batch raw JSON → rooms/<房>/00_raw/")
    ap.add_argument(
        "--rooms-root",
        default=str(
            Path(__file__).resolve().parent.parent.parent
            / "02_runtime"
            / "info_live_room_sampling"
            / "rooms"
        ),
    )
    ap.add_argument("--batch-dir", action="append", default=None)
    ap.add_argument("--apply", action="store_true", help="真复制；默认只打印计划")
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="兼容参数：与默认相同（不加 --apply 就是 dry-run）",
    )
    args = ap.parse_args()

    rooms_root = Path(args.rooms_root).resolve()
    if not rooms_root.exists():
        print(f"FATAL: rooms root 不存在: {rooms_root}")
        return 2

    batch_dirs: list[Path] = []
    if args.batch_dir:
        for d in args.batch_dir:
            batch_dirs.append(Path(d).resolve())
    else:
        info_root = rooms_root.parent
        for pattern in ("batch_05__*/00_raw", "batch_07_daily_close__*/00_raw"):
            batch_dirs.extend(sorted(info_root.glob(pattern)))

    print(f"rooms root: {rooms_root}")
    print(f"扫描 batch 00_raw 目录数: {len(batch_dirs)}")
    for d in batch_dirs:
        print(f"  - {d}")

    plan: dict[str, list[tuple[Path, Path]]] = defaultdict(list)
    unresolved: list[Path] = []
    for src in iter_candidate_files(batch_dirs):
        room = detect_room_name(src)
        if not room:
            unresolved.append(src)
            continue
        dst = rooms_root / room / "00_raw" / src.name
        if dst.exists() and dst.stat().st_size == src.stat().st_size:
            plan[room + "__SKIP_SAME_SIZE"].append((src, dst))
            continue
        plan[room].append((src, dst))

    total_plan = sum(len(v) for k, v in plan.items() if not k.endswith("__SKIP_SAME_SIZE"))
    skip_plan = sum(len(v) for k, v in plan.items() if k.endswith("__SKIP_SAME_SIZE"))
    hit_rooms = len([k for k in plan if not k.endswith("__SKIP_SAME_SIZE")])
    print("")
    print(
        f"命中 {hit_rooms} 房；拟搬 {total_plan} 文件；"
        f"{skip_plan} 个同大小已存在跳过；{len(unresolved)} 个未能识别房名"
    )
    for room, lst in sorted(plan.items()):
        if room.endswith("__SKIP_SAME_SIZE"):
            continue
        print(f"  [{room}] -> {len(lst)} 个文件")

    if unresolved:
        print("")
        print(f"未能识别房名的文件（共{len(unresolved)}，示例前10个）：")
        for p in unresolved[:10]:
            print(f"  - {p}")

    if not args.apply:
        print("")
        print("dry-run 结束。加 --apply 真实复制（原文件保留）。")
        return 0

    moved_ok = 0
    for room, lst in plan.items():
        if room.endswith("__SKIP_SAME_SIZE"):
            continue
        for src, dst in lst:
            try:
                dst.parent.mkdir(parents=True, exist_ok=True)
                if not dst.exists():
                    shutil.copy2(src, dst)
                moved_ok += 1
            except Exception as e:
                print(f"FAIL {src} -> {dst}: {e}")
    print("")
    print(f"复制完成。成功: {moved_ok}/{total_plan}（原文件保留不动）")
    print(f"时间戳: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
