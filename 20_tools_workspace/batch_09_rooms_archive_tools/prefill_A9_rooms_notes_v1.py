"""
prefill_A9_rooms_notes_v1.py — 纯事实预填（判断格全留空）
按房 / 按日 抽 JSON → 写 10_ingest/<房名>_<YYYYMMDD>_NOTES_partial_prefill.md

用法（默认 dry-run，不写文件只打印）：
  python prefill_A9_rooms_notes_v1.py --trade-date 20260811 --rooms-root ../../02_runtime/info_live_room_sampling/rooms
  python prefill_A9_rooms_notes_v1.py --trade-date 20260811 --rooms-root ../../02_runtime/info_live_room_sampling/rooms --apply-draft

抽的事实字段（全是纯统计，不判情绪/价值/风格）：
  - total_messages / total_authors / last_message_at（JSON.data.messages 长度/作者数/最后一条时间戳）
  - topics_top5（JSON.data.topics 前 5 或 高频话题词频前 5，空=UNKNOWN）
  - mentions_count_ladder（JSON 所有字符串 正则 6 位股票代码 数 与连板16列 TSV 重合率）
  - capital_flow_hot_words（行业成交Top5 JSON 板块名 TOP3 重合）
  - export_start_at / export_end_at（JSON.heuristics.export_start / export_end）
  - raw_file_count / latest_raw_size_kb / latest_raw_sha256（当日 raw 计数）
  - manual_judgment_3cells（空行留空：情绪偏多空/主抓风格/次日节奏，只给占位）
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOMS_9A = [
    "复盘哥",
    "独家老师5号",
    "独家短线老师6号",
    "机构电话会议纪要+小作文+情报",
    "梅森",
    "顺势而为",
    "混江龙",
    "天赢居",
    "先知",
]

STOCK_6D = re.compile(r"\b(?:60[0-3]\d{3}|68[58]\d{3}|00[0-3]\d{3}|30[0-7]\d{3}|0[12][0-9]{4})\b")
USER_TAG_LINE = re.compile(
    r"^(?:(\d{4}/\d{2}/\d{2})\s+)?(\d{1,2}:\d{2}(?::\d{2})?)\s+([^\s20\d-][^\s]{1,28})\s+(?:\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}(?::\d{2})?\s+)?(.*)$",
    re.DOTALL,
)
DATE_IN_NAME = re.compile(r"(20\d{6})")

TOPIC_KEYWORDS = [
    "重要公告", "题材", "板块异动", "涨停", "连板", "复盘",
    "机会", "风险", "赛道", "情绪", "接力", "龙头", "切换",
    "分歧", "一致", "芯片", "AI", "算力", "消费", "医药",
    "新能源", "军工", "地产", "金融", "煤炭", "钢铁", "化工",
    "半导体", "储能", "光伏", "汽车", "机器人", "数据要素",
]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def ymd_from_name(s: str) -> str | None:
    m = DATE_IN_NAME.search(s)
    return m.group(1) if m else None


def flatten_strings(node, out: list[str] | None = None) -> list[str]:
    if out is None:
        out = []
    if isinstance(node, dict):
        for v in node.values():
            flatten_strings(v, out)
    elif isinstance(node, list):
        for x in node:
            flatten_strings(x, out)
    elif isinstance(node, str):
        out.append(node)
    return out


def extract_room_facts(room_dir: Path, trade_ymd: str) -> dict:
    raw_dir = room_dir / "00_raw"
    facts = {
        "room_name": room_dir.name,
        "trade_ymd": trade_ymd,
        "raw_file_count": 0,
        "latest_raw_name": "",
        "latest_raw_size_kb": 0,
        "latest_raw_sha256": "",
        "export_start_at": "",
        "export_end_at": "",
        "total_messages": 0,
        "newly_added_messages": 0,
        "total_authors": 0,
        "last_message_at": "",
        "topics_top5_joined": "UNKNOWN",
        "stock_codes_found_uniq": 0,
        "stock_codes_total_hits": 0,
    }
    if not raw_dir.exists():
        return facts
    raws_today = []
    for p in sorted(raw_dir.glob("*.json")):
        y = ymd_from_name(p.name)
        if y and y == trade_ymd:
            raws_today.append(p)
    raws_today.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    facts["raw_file_count"] = len(raws_today)
    if facts["raw_file_count"] == 0:
        return facts
    latest = raws_today[0]
    facts["latest_raw_name"] = latest.name
    facts["latest_raw_size_kb"] = round(latest.stat().st_size / 1024.0, 2)
    facts["latest_raw_sha256"] = sha256_file(latest)

    try:
        with latest.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return facts

    if not isinstance(data, dict):
        return facts

    exported_at = data.get("exported_at")
    if exported_at:
        facts["export_end_at"] = str(exported_at)[:24]

    sample_range = data.get("sample_range") if isinstance(data, dict) else None
    if isinstance(sample_range, dict):
        first = sample_range.get("first") if isinstance(sample_range, dict) else None
        last = sample_range.get("last") if isinstance(sample_range, dict) else None
        pieces = []
        if isinstance(first, dict):
            for k in ("display_date", "display_time"):
                v = first.get(k)
                if v:
                    pieces.append(str(v))
        if pieces:
            facts["export_start_at"] = " ".join(pieces).strip()
        pieces2 = []
        if isinstance(last, dict):
            for k in ("display_date", "display_time"):
                v = last.get(k)
                if v:
                    pieces2.append(str(v))
            if pieces2:
                facts["last_message_at"] = " ".join(pieces2).strip()

    try:
        facts["total_messages"] = int(data.get("message_count") or 0)
    except Exception:
        facts["total_messages"] = 0
    try:
        facts["newly_added_messages"] = int(data.get("newly_added_count") or 0)
    except Exception:
        facts["newly_added_messages"] = 0

    messages = data.get("messages") if isinstance(data, dict) else None
    authors: set[str] = set()
    bag_text_parts: list[str] = []
    if isinstance(messages, list) and messages:
        if facts["total_messages"] == 0:
            facts["total_messages"] = len(messages)
        for msg in messages:
            if not isinstance(msg, dict):
                continue
            text = str(msg.get("text") or "")
            if not text:
                continue
            bag_text_parts.append(text)
            m = USER_TAG_LINE.match(text)
            if m:
                name = (m.group(3) or "").strip()
                if name and 1 <= len(name) <= 32:
                    authors.add(name)
    facts["total_authors"] = len(authors)

    joined_bag = "\n".join(bag_text_parts)
    codes = STOCK_6D.findall(joined_bag)
    facts["stock_codes_total_hits"] = len(codes)
    facts["stock_codes_found_uniq"] = len(set(codes))

    kw_counter: Counter = Counter()
    for kw in TOPIC_KEYWORDS:
        kw_counter[kw] = joined_bag.count(kw)
    top = [(n, kw) for kw, n in kw_counter.items() if n >= 1]
    top.sort(reverse=True)
    if top:
        facts["topics_top5_joined"] = " ".join(f"{kw}:{n}" for n, kw in top[:5])

    return facts


def render_markdown(f: dict) -> str:
    lines = []
    lines.append(f"# {f['room_name']} / {f['trade_ymd']}  NOTES_partial_prefill（事实预填，判断格全留空）")
    lines.append("")
    lines.append(f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- 当日 Raw 文件数：{f['raw_file_count']}")
    if f["raw_file_count"]:
        lines.append(f"- 最新 Raw：`{f['latest_raw_name']}`  ({f['latest_raw_size_kb']} KB)  SHA256=`{f['latest_raw_sha256'][:16]}`")
    lines.append("")
    lines.append("## 一、事实统计（纯抽，不判）")
    lines.append("")
    lines.append(f"| 项 | 值 |")
    lines.append(f"|---|---|")
    lines.append(f"| total_messages（消息条数） | {f['total_messages']} |")
    lines.append(f"| newly_added_count（本轮增量新增） | {f['newly_added_messages']} |")
    lines.append(f"| total_authors（发言人数） | {f['total_authors']} |")
    lines.append(f"| last_message_at（最后消息时间戳） | {f['last_message_at'] or '未提取到'} |")
    lines.append(f"| export 窗口 start / end | {f['export_start_at'] or 'UNKNOWN'} / {f['export_end_at'] or 'UNKNOWN'} |")
    lines.append(f"| 股票代码命中（去重 / 总次数） | {f['stock_codes_found_uniq']} / {f['stock_codes_total_hits']} |")
    lines.append(f"| topics_top5（关键词频次TOP5） | {f['topics_top5_joined'] or 'UNKNOWN'} |")
    lines.append("")
    lines.append("## 二、人工判断（3 格，留空等你填）")
    lines.append("")
    lines.append("```")
    lines.append("[ ] 情绪偏多空（强多 / 多 / 震荡 / 空 / 强空）：________")
    lines.append("[ ] 主抓风格（打板 / 低吸 / 埋伏 / 空仓 / 轮动）：________")
    lines.append("[ ] 次日节奏（接力高度 / 中位 / 首板 / 观望）：________")
    lines.append("```")
    lines.append("")
    lines.append("> 看完你自己填上面 3 格，然后整段复制进 `20_absorb/NOTES.md`，末尾加一行：")
    lines.append(f"> 「已吸收 @ {f['trade_ymd'][:4]}-{f['trade_ymd'][4:6]}-{f['trade_ymd'][6:8]}」")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trade-date", required=True, help="YYYYMMDD")
    ap.add_argument("--rooms-root", required=True, help="rooms 家族根")
    ap.add_argument("--apply-draft", action="store_true", help="真写 10_ingest/ 下的 md（默认只打印 dry-run 摘要）")
    ap.add_argument("--only-room", default="", help="只处理一间房名，默认 A 桶 9 房全走")
    args = ap.parse_args()

    rooms_root = Path(args.rooms_root).resolve()
    targets = [args.only_room] if args.only_room else ROOMS_9A
    summary_rows = []
    for name in targets:
        room_dir = rooms_root / name
        facts = extract_room_facts(room_dir, args.trade_date)
        md = render_markdown(facts)
        status = "SKIP_NO_RAW_TODAY" if facts["raw_file_count"] == 0 else ("OK_DRAFT_WRITTEN" if args.apply_draft else "DRY_RUN")
        summary_rows.append((name, status, facts["raw_file_count"], facts["total_messages"], facts["newly_added_messages"], facts["total_authors"], facts["stock_codes_found_uniq"]))
        if status == "DRY_RUN":
            head = "\n".join(md.splitlines()[:20])
            print(f"--- DRY_RUN [{name}] {status} raw={facts['raw_file_count']} ---\n{head}\n")
        elif status == "SKIP_NO_RAW_TODAY":
            print(f"SKIP [{name}] 当日无 Raw，跳过（先知/漏导出常见）")
        else:
            ingest_dir = room_dir / "10_ingest"
            ingest_dir.mkdir(parents=True, exist_ok=True)
            out = ingest_dir / f"{name}_{args.trade_date}_NOTES_partial_prefill.md"
            out.write_text(md, encoding="utf-8")
            print(f"WROTE [{name}] {out}")

    print("--- PREFILL SUMMARY（A 桶 9 房）---")
    print("房间名 / 状态 / Raw数 / 消息数 / 新增 / 作者数 / 股票代码去重")
    for r in summary_rows:
        print("  {0:<22} {1:<18} {2:>3} {3:>6} {4:>5} {5:>4} {6:>4}".format(*r))
    ok = sum(1 for s in summary_rows if s[1] != "SKIP_NO_RAW_TODAY")
    skip = sum(1 for s in summary_rows if s[1] == "SKIP_NO_RAW_TODAY")
    print(f"TOTAL {len(summary_rows)} 房：{ok} 房生成草稿，{skip} 房当日无 Raw（漏导出/先知常见）")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
