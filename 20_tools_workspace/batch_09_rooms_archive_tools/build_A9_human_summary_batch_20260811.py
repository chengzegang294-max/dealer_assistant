"""
build_A9_human_summary_batch_20260811.py
用途：ONLY A桶9房。每间房按时间旧→新整理一份人读摘要（4格+时间线原文TOPN），不判情绪/价值，只给重点。
  四格标准（你要的吸收标准）：
  1. TOP5关键词频次   2. TOP5股票代码频次   3. TOP5活跃作者（发言条数）
  4. 按时间旧→新 完整消息N条（默认抽每条前200字，最多抽TOP80条，避免太长）
产物：rooms/<房名>/10_ingest/<房名>_20260811_人读摘要旧到新.md（8间今日有Raw，先知A#9漏0件）
调用：
  python build_A9_human_summary_batch_20260811.py --rooms-root ../../02_runtime/info_live_room_sampling/rooms --trade-date 20260811 --apply
  # 不加 --apply 只打印 DryRun 摘要不写文件
"""
from __future__ import annotations
import argparse
import re
import json
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
USER_TAG = re.compile(
    r"^(?:(\d{4}/\d{2}/\d{2})\s+)?(\d{1,2}:\d{2}(?::\d{2})?)\s+([^\s20\d-][^\s]{1,28})\s+(?:\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}(?::\d{2})?\s+)?(.*)$",
    re.DOTALL,
)
TOPIC_KW = [
    "重要公告", "题材", "板块异动", "涨停", "连板", "复盘", "机会", "风险",
    "赛道", "情绪", "接力", "龙头", "切换", "分歧", "一致", "芯片", "AI", "算力",
    "消费", "医药", "新能源", "军工", "地产", "金融", "煤炭", "钢铁", "化工",
    "半导体", "储能", "光伏", "汽车", "机器人", "数据要素", "稀土", "有色",
    "华为", "苹果", "特斯拉", "宁德时代", "比亚迪",
]
DATE_IN_FILE = re.compile(r"(20\d{6})")


def ymd_from_file(p: Path) -> str | None:
    m = DATE_IN_FILE.search(p.name)
    return m.group(1) if m else None


def load_messages_today(room_dir: Path, trade_ymd: str) -> tuple[list[dict], list[Path]]:
    raw_dir = room_dir / "00_raw"
    if not raw_dir.exists():
        return [], []
    todays: list[Path] = []
    for p in sorted(raw_dir.glob("*.json")):
        y = ymd_from_file(p)
        if y and y == trade_ymd:
            todays.append(p)
    todays.sort(key=lambda x: x.stat().st_mtime)
    ordered_msgs: list[dict] = []
    for p in todays:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        msgs = data.get("messages")
        if not isinstance(msgs, list):
            continue
        for msg in msgs:
            if not isinstance(msg, dict):
                continue
            text = str(msg.get("text") or "")
            if not text:
                continue
            d_date = str(msg.get("display_date") or "")
            d_time = str(msg.get("display_time") or "")
            author = ""
            body = text
            m = USER_TAG.match(text)
            if m:
                if m.group(1):
                    d_date = m.group(1)
                d_time = m.group(2) or d_time
                author = (m.group(3) or "").strip()
                body = (m.group(4) or "").strip()
            sort_key = f"{d_date.replace('/','-'):10s} {d_time:>8s}"
            ordered_msgs.append({
                "date": d_date, "time": d_time, "author": author,
                "body": body, "sort_key": sort_key, "raw_text": text, "src": p.name,
            })
    ordered_msgs.sort(key=lambda x: x["sort_key"])
    return ordered_msgs, todays


def summarize(msgs: list[dict]) -> dict:
    kw_counter: Counter = Counter()
    code_counter: Counter = Counter()
    author_counter: Counter = Counter()
    body_all_parts = []
    for m in msgs:
        body_all_parts.append(m["body"])
        if m["author"]:
            author_counter[m["author"]] += 1
        txt = m["raw_text"]
        for kw in TOPIC_KW:
            if kw in txt:
                kw_counter[kw] += 1
        for c in STOCK_6D.findall(txt):
            code_counter[c] += 1
    joined = "\n".join(body_all_parts)
    return {
        "total_msgs": len(msgs),
        "total_authors": len(author_counter),
        "kw_top5": kw_counter.most_common(5),
        "code_top5": code_counter.most_common(5),
        "author_top5": author_counter.most_common(5),
        "joined_len": len(joined),
    }


def render_room(room_name: str, trade_ymd: str, msgs: list[dict], srcs: list[Path]) -> str:
    s = summarize(msgs)
    lines = []
    dash = f"{trade_ymd[:4]}-{trade_ymd[4:6]}-{trade_ymd[6:8]}"
    lines.append(f"# {room_name} / {dash}  人读摘要（按时间旧→新，不判情绪/价值，只给重点）")
    lines.append("")
    lines.append(f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- 当日 Raw 文件数：{len(srcs)}  总消息条数：{s['total_msgs']}  活跃作者数：{s['total_authors']}")
    if srcs:
        sizes = ", ".join(f"{x.name}({round(x.stat().st_size/1024.0,1)}KB)" for x in srcs)
        lines.append(f"- 源文件（按修改时间旧→新）：{sizes}")
    lines.append("")
    lines.append("## 一、四格重点（TOP5关键词 / TOP5股票代码 / TOP5作者 / 基本统计）")
    lines.append("")
    lines.append("| 格 | 项 | TOP5 值（频次高→低） |")
    lines.append("|---|---|---|")
    v1 = "  ".join(f"{k}:{n}" for k, n in s["kw_top5"]) if s["kw_top5"] else "未命中关键词"
    v2 = "  ".join(f"{k}:{n}" for k, n in s["code_top5"]) if s["code_top5"] else "未命中股票代码"
    v3 = "  ".join(f"{k}:{n}" for k, n in s["author_top5"]) if s["author_top5"] else "0作者"
    lines.append(f"| 1 | TOP5 关键词（板块/情绪/题材） | {v1} |")
    lines.append(f"| 2 | TOP5 股票代码（6位A股代码，命中次数） | {v2} |")
    lines.append(f"| 3 | TOP5 活跃作者（发言条数多→少） | {v3} |")
    lines.append(f"| 4 | 基本统计（总消息/作者/当日Raw） | 总消息 {s['total_msgs']} / 活跃作者 {s['total_authors']} / Raw {len(srcs)}份 / 正文字符约 {s['joined_len']} |")
    lines.append("")
    lines.append("## 二、按时间旧→新（从最早到最晚）消息摘录（每条截断前200字，默认最多抽80条）")
    lines.append("")
    lines.append("| # | 日期 | 时间 | 作者 | 正文前200字（超过截断） | 来源文件 |")
    lines.append("|---|---|---|---|---|---|")
    cap = min(80, len(msgs))
    for i, m in enumerate(msgs[:cap], 1):
        body = m["body"].replace("\r", " ").replace("\n", "  ").replace("|", "/").replace("`", "'")
        if len(body) > 200:
            body = body[:200] + "…（截断）"
        src = m["src"].replace("|", "/") if m.get("src") else ""
        lines.append(f"| {i} | {m['date'] or '—'} | {m['time'] or '—'} | {(m['author'] or '匿名').replace('|','/')[:20]} | {body} | {src} |")
    lines.append("")
    lines.append("> 人类判断格（3行留空等你填，看完你补）：")
    lines.append("> ```")
    lines.append("> [ ] 情绪偏多空（强多/多/震荡/空/强空）：________")
    lines.append("> [ ] 主抓风格（打板/低吸/埋伏/空仓/轮动）：________")
    lines.append("> [ ] 次日节奏（接力高度/中位/首板/观望）：________")
    lines.append("> ```")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rooms-root", required=True)
    ap.add_argument("--trade-date", required=True, help="YYYYMMDD")
    ap.add_argument("--apply", action="store_true", help="真写 10_ingest/*_人读摘要旧到新.md（默认DryRun只打印）")
    args = ap.parse_args()
    rooms_root = Path(args.rooms_root).resolve()
    print(f"=== A桶9房 人读摘要 按时间旧→新 （trade_date={args.trade_date}, apply={args.apply}) ===")
    totals = []
    for name in ROOMS_9A:
        room_dir = rooms_root / name
        msgs, srcs = load_messages_today(room_dir, args.trade_date)
        if not msgs:
            totals.append((name, 0, 0, "SKIP_NO_RAW_TODAY"))
            print(f"SKIP  [{name:<22}]  当日无Raw 或无消息 （先知/A9漏导出常见）")
            continue
        md = render_room(name, args.trade_date, msgs, srcs)
        s = summarize(msgs)
        if args.apply:
            out = room_dir / "10_ingest" / f"{name}_{args.trade_date}_人读摘要旧到新.md"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(md, encoding="utf-8")
            status = f"WROTE {out.name}"
        else:
            head = "\n".join(md.splitlines()[:22])
            print(f"--- DRY_RUN [{name}] total_msgs={len(msgs)} authors={s['total_authors']} ---\n{head}\n")
            status = "DRY_RUN"
        totals.append((name, len(msgs), s["total_authors"], status))
    print("")
    print("=== 汇总 A桶9房 ===")
    print("房间名 / 消息数 / 作者数 / 状态")
    ok = 0; skip = 0
    for t in totals:
        print(f"  {t[0]:<22}  {t[1]:>5}条  {t[2]:>4}作者  {t[3]}")
        if t[3].startswith("SKIP"): skip += 1
        else: ok += 1
    print(f"TOTAL 9房：写入/DryRun {ok} 房（{args.trade_date}有Raw），{skip} 房当日无Raw（漏导出先知A9）")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
