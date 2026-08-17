"""
sentinel_update_rooms_index_v1.py
用途：扫描 rooms 家族，刷新 SENTINEL_INDEX.md
结构：A 桶 8 房每日置顶 / B 桶 14 房活跃选导 / §FROZEN_OUT 另行处理（不参与每日）
调用：
  python sentinel_update_rooms_index_v1.py --rooms-root ../../02_runtime/info_live_room_sampling/rooms
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

# 每日置顶 A 桶（8）+ 活跃选导 B 桶（14）— 不含 FROZEN_OUT
ROOMS_DAILY = [
    ("A1", "复盘哥", "A"),
    ("A2", "独家老师5号", "A"),
    ("A3", "独家短线老师6号", "A"),
    ("A4", "梅森", "A"),
    ("A5", "顺势而为", "A"),
    ("A6", "混江龙", "A"),
    ("A7", "天赢居", "A"),
    ("A8", "先知", "A"),
    ("B10", "天机", "B"),
    ("B11", "游资胖大叔", "B"),
    ("B12", "潜伏王者", "B"),
    ("B13", "k神", "B"),
    ("B14", "周期女王", "B"),
    ("B15", "格兰投研", "B"),
    ("B16", "擒龙小师姐", "B"),
    ("B17", "独家竞价低吸", "B"),
    ("B18", "小锦鲤", "B"),
    ("B19", "核心逻辑社", "B"),
    ("B20", "梦幻一步", "B"),
    ("B21", "新生代", "B"),
    ("B22", "龙头交易猿", "B"),
    ("B24", "小作文嗅嗅+机构研报", "B"),
]

# 永久踢出每日：另行开研报/电话家族；只保留 00_raw，不参与置顶
FROZEN_OUT = [
    ("F1", "机构电话会议纪要+小作文+情报", "原 A#4 Tier1",
     "每天更新太多会淹没 A 桶 8 房重点；研报/电话类另行开家族"),
    ("F2", "机构研报资讯精选", "原 B#23 Tier2",
     "与 F1 并为一对 FROZEN_OUT；不吸收进每日直播间流程"),
]

ALIAS = {
    "独家老师5号": "独家5号",
    "独家短线老师6号": "独家6号/短线6号",
    "k神": "K神",
    "格兰投研": "格兰",
    "擒龙小师姐": "小师姐",
    "小作文嗅嗅+机构研报": "小作文嗅嗅（保留每日，和B23不同类）",
    "梅森": "原 A5 顺推",
    "顺势而为": "原 A6 顺推",
    "混江龙": "原 A7 顺推",
    "天赢居": "原 A8 顺推",
    "先知": "原 A9 顺推",
}

DATE_IN_NAME = re.compile(r"(20\d{6})")


def ymd_from_file(p: Path) -> str | None:
    m = DATE_IN_NAME.search(p.name)
    return m.group(1) if m else None


def last_absorbed_date(notes_md: Path) -> str:
    if not notes_md.exists():
        return "—"
    dates = []
    for line in notes_md.read_text(encoding="utf-8").splitlines():
        m2 = re.search(r"已吸收\s*@\s*(20\d{2}-\d{2}-\d{2})", line)
        if m2 and ("未吸收" not in line) and ("已吸收" in line):
            dates.append(m2.group(1))
    return sorted(dates)[-1] if dates else "—"


def draft_status(room_dir: Path, last_raw_ymd: str | None) -> str:
    ingest = room_dir / "10_ingest"
    if not ingest.exists() or last_raw_ymd is None:
        return "待生成"
    d = last_raw_ymd
    expect = [f"{d[:4]}-{d[4:6]}-{d[6:8]}", d]
    for f in ingest.glob("*_machine_draft.md"):
        for e in expect:
            if e in f.name:
                return "草稿"
    return "待生成"


def scan_room(rooms_root: Path, name: str) -> tuple[int, str, str, str]:
    room_dir = rooms_root / name
    raw_dir = room_dir / "00_raw"
    raw_files = sorted(raw_dir.glob("*.json")) if raw_dir.exists() else []
    raw_count = len(raw_files)
    last_raw = "—"
    last_ymd = None
    if raw_files:
        ymds = [ymd_from_file(p) for p in raw_files]
        ymds = [x for x in ymds if x]
        if ymds:
            last_ymd = sorted(ymds)[-1]
            last_raw = f"{last_ymd[:4]}-{last_ymd[4:6]}-{last_ymd[6:8]}"
    draft = draft_status(room_dir, last_ymd)
    absorbed = last_absorbed_date(room_dir / "20_absorb" / "NOTES.md")
    return raw_count, last_raw, draft, absorbed


def main() -> int:
    ap = argparse.ArgumentParser(description="刷新 SENTINEL_INDEX.md（含 FROZEN_OUT）")
    ap.add_argument("--rooms-root", required=True, help="rooms 家族根")
    args = ap.parse_args()
    rooms_root = Path(args.rooms_root).resolve()
    index_path = rooms_root / "SENTINEL_INDEX.md"
    if not rooms_root.exists():
        print(f"FATAL: 找不到 rooms 根: {rooms_root}")
        return 2

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines: list[str] = [
        "# 信息直播间 24 房哨兵索引 SENTINEL_INDEX",
        "",
        f"最后更新：{now}（sentinel_update_rooms_index_v1.py；A4/B23→FROZEN_OUT 不参与每日）",
        "",
        "## 一、A 桶（Tier1·每日置顶必导，★★★★★ 优先度 8 房）",
        "",
        "| A桶编号 | 房间名 | 分桶 | 层级 | Raw 文件数 | 最后 Raw 日期 | 草稿状态 | 已吸收至 | 备注/别名 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]

    for code, name, bucket in ROOMS_DAILY:
        if bucket != "A":
            continue
        raw_count, last_raw, draft, absorbed = scan_room(rooms_root, name)
        alias = ALIAS.get(name, "")
        lines.append(
            f"| {code} | {name} | A | Tier1 | {raw_count} | {last_raw} | {draft} | {absorbed} | {alias} |"
        )

    lines += [
        "",
        "**A 桶裁决（2026-08-13）：** 永久踢出「机构电话会议纪要+小作文+情报」，不再置顶不再每日必导；原 A5–A9 顺推为 A4–A8。",
        "",
        "## 二、B 桶（Tier2·每日活跃选导，★★★~★★★★，14 房）",
        "",
        "| B桶编号 | 房间名 | 分桶 | 层级 | Raw 文件数 | 最后 Raw 日期 | 草稿状态 | 已吸收至 | 备注/别名 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]

    for code, name, bucket in ROOMS_DAILY:
        if bucket != "B":
            continue
        raw_count, last_raw, draft, absorbed = scan_room(rooms_root, name)
        alias = ALIAS.get(name, "")
        lines.append(
            f"| {code} | {name} | B | Tier2 | {raw_count} | {last_raw} | {draft} | {absorbed} | {alias} |"
        )

    lines += [
        "",
        "**B 桶裁决（2026-08-13）：** 踢出 B23「机构研报资讯精选」→ FROZEN_OUT，不再每日。",
        "",
        "## §FROZEN_OUT：另行处理家族（A4机构电话 / B23机构研报·以后要做开新家族·不参与每日）",
        "",
        "用户 2026-08-13 裁决：研报+机构电话从 A/B 桶日常置顶踢出，状态=**FROZEN_OUT**；"
        "以后要做另行开新通道，不混在直播间每日流程。",
        "",
        "| FROZEN编号 | 房间名 | 原来的桶 | 状态 | Raw 保留说明 | 永久跳过原因 |",
        "|---|---|---|---|---|---|",
    ]

    for code, name, origin, reason in FROZEN_OUT:
        raw_count, last_raw, _draft, _abs = scan_room(rooms_root, name)
        lines.append(
            f"| {code} | {name} | {origin} | **FROZEN_OUT** | "
            f"00_raw **{raw_count}** 件已入库·保留不删（最后 Raw {last_raw}） | {reason} |"
        )

    lines += [
        "",
        "**FROZEN_OUT 硬规则：**",
        "1. 00_raw 永久保留不删；以后开研报/电话家族可直接拷贝。",
        "2. 每日续导 / migrate 转 MD / 分类器训练 **永远硬跳过** F1/F2，"
        "与 `SKIP_ROOMS_USER_SAID_REDO_LATER` 对齐，永不误出 MD。",
        "3. 永不置顶、不进 A/B 每日必导、不给★；要导只能单独导。",
        "",
        "---",
        "",
        "## 四、22 房每日范围 Raw 状态",
        "",
        "A 桶 8 房 + B 桶 14 房 = **22 房**参与每日；F1/F2 不计入每日置顶范围。",
        "",
    ]

    index_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"OK {index_path} 已刷新（每日22房 + FROZEN_OUT 2房）")
    print(f"  时间戳: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
