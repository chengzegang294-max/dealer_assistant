"""
build_AB24_rooms_human_summary_v2.py
作用：24 房 A+B 桶重做 Prefill草稿 + 人读摘要（四格TOP5 + 按时间旧→新消息 TOP120条，每条前200字）
  - 目标：期末 = 2026-08-11 （你定的日期），取每间房 00_raw 里所有 20260811 前缀的 Raw JSON 合并（>=2份也合并，按消息时间排序）
  - 跳过2间硬编码（你明确自己重做以后吸收）：
      SKIP_ROOMS = ["机构电话会议纪要+小作文+情报", "机构研报资讯精选"]
  - 其余 19/24 全部重做 Prefill草稿 + 人读摘要旧→新
  - 每间房 message_count=0 的 Raw JSON 自动跳过 （比如 机构研报精选那 1 件空的）
  - 不加 --apply 只 DryRun 打印首行摘要；--apply 才真写盘
命令：
  python build_AB24_rooms_human_summary_v2.py --rooms-root ../../02_runtime/info_live_room_sampling/rooms --trade-date 20260811 --apply
"""
from __future__ import annotations
import argparse
import re
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOMS_ALL24 = [
    "复盘哥", "独家老师5号", "独家短线老师6号", "机构电话会议纪要+小作文+情报",
    "梅森", "顺势而为", "混江龙", "天赢居", "先知",
    "天机", "游资胖大叔", "潜伏王者", "k神", "周期女王", "格兰投研", "擒龙小师姐",
    "独家竞价低吸", "小锦鲤", "核心逻辑社", "梦幻一步", "新生代", "龙头交易猿",
    "机构研报资讯精选", "小作文嗅嗅+机构研报",
]
SKIP_ROOMS_USER_SAID_REDO_LATER = {
    # FROZEN_OUT：永久踢出 A/B 每日置顶；只存 00_raw，永不自动出 MD
    "机构电话会议纪要+小作文+情报": "FROZEN_OUT F1（原A4）2026-08-13裁决：另行开研报/电话家族，不参与每日",
    "机构研报资讯精选": "FROZEN_OUT F2（原B23）2026-08-13裁决：与F1并为一对，不参与每日",
}
STOCK_6D = re.compile(r"\b(?:60[0-3]\d{3}|68[58]\d{3}|00[0-3]\d{3}|30[0-7]\d{3}|0[12][0-9]{4})\b")
USER_TAG = re.compile(
    r"^(?:(\d{4}/\d{2}/\d{2})\s+)?(\d{1,2}:\d{2}(?::\d{2})?)\s+([^\s20\d-][^\s]{1,28})\s+(?:\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}(?::\d{2})?\s+)?(.*)$",
    re.DOTALL,
)
TOPIC_KW = [
    "重要公告","题材","板块异动","涨停","连板","复盘","机会","风险","赛道","情绪",
    "接力","龙头","切换","分歧","一致","芯片","AI","算力","消费","医药","新能源",
    "军工","地产","金融","煤炭","钢铁","化工","半导体","储能","光伏","汽车","机器人",
    "数据要素","稀土","有色","华为","苹果","特斯拉","宁德时代","比亚迪","低吸","打板",
    "竞价","首板","二板","三板","接力","中军","补涨","题材","回流","分歧","一致",
    "T+0","超跌","高位","低位","补跌","龙头","炸板","回封","缩量","放量","缺口",
    "支撑位","压力位","止损","止盈","仓位","加仓","减仓","满仓","空仓","半仓","轮动",
]
DATE_IN_FILE = re.compile(r"(20\d{6})")


def ymd_from_file(p: Path) -> str | None:
    m = DATE_IN_FILE.search(p.name)
    return m.group(1) if m else None


def load_room_messages(room_dir: Path, trade_ymd: str) -> tuple[list[dict], list[Path], int]:
    raw_dir = room_dir / "00_raw"
    if not raw_dir.exists():
        return [], [], 0
    todays: list[Path] = []
    for p in sorted(raw_dir.glob("*.json")):
        y = ymd_from_file(p)
        if y and y == trade_ymd:
            todays.append(p)
    todays.sort(key=lambda x: x.stat().st_mtime)
    ordered_msgs: list[dict] = []
    zero_skip = 0
    for p in todays:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            zero_skip += 1
            continue
        if not isinstance(data, dict):
            zero_skip += 1
            continue
        try:
            mc = int(data.get("message_count") or 0)
        except Exception:
            mc = -1
        if mc == 0:
            zero_skip += 1
            continue
        msgs = data.get("messages")
        if not isinstance(msgs, list) or len(msgs) == 0:
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
            d_date_norm = d_date.replace("/", "-")
            sort_key = f"{d_date_norm:10s} {d_time:>8s}"
            ordered_msgs.append({
                "date": d_date_norm, "time": d_time, "author": author,
                "body": body, "sort_key": sort_key, "raw_text": text, "src": p.name,
            })
    ordered_msgs.sort(key=lambda x: x["sort_key"])
    return ordered_msgs, todays, zero_skip


def summarize(msgs: list[dict]) -> dict:
    kw_counter: Counter = Counter()
    code_counter: Counter = Counter()
    author_counter: Counter = Counter()
    for m in msgs:
        if m["author"]:
            author_counter[m["author"]] += 1
        txt = m["raw_text"]
        for kw in TOPIC_KW:
            if kw in txt:
                kw_counter[kw] += 1
        for c in STOCK_6D.findall(txt):
            code_counter[c] += 1
    return {
        "total_msgs": len(msgs),
        "total_authors": len(author_counter),
        "kw_top5": kw_counter.most_common(5),
        "code_top5": code_counter.most_common(5),
        "author_top5": author_counter.most_common(5),
    }


def render(room_name: str, trade_ymd: str, msgs: list[dict], srcs: list[Path], zero_skip: int) -> str:
    s = summarize(msgs)
    dash = f"{trade_ymd[:4]}-{trade_ymd[4:6]}-{trade_ymd[6:8]}"
    lines = []
    lines.append(f"# {room_name} / {dash}  人读摘要（期末={dash}；四格TOP5+按时间旧→新；机器不判情绪/风格/节奏）")
    lines.append("")
    lines.append(f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- 期末交易日期（吸收至）：{dash}")
    lines.append(f"- 当日 Raw 文件数：{len(srcs)} 份 （ message_count=0 坏文件跳过 {zero_skip} 件）")
    lines.append(f"- 总消息条数：{s['total_msgs']}   去重活跃作者数：{s['total_authors']}")
    if srcs:
        sizes = ", ".join(f"{x.name}({round(x.stat().st_size/1024.0,1)}KB)" for x in srcs[:3])
        if len(srcs) > 3:
            sizes += f"  ……共{len(srcs)}份"
        lines.append(f"- 源文件（按修改时间旧→新）：{sizes}")
    lines.append("")
    lines.append("## 一、四格吸收（TOP5关键词 / TOP5股票代码 / TOP5活跃作者 / 基本统计）")
    lines.append("")
    lines.append("| 格 | 项 | TOP5 值（频次高→低） |")
    lines.append("|---|---|---|")
    v1 = "  ".join(f"{k}:{n}" for k, n in s["kw_top5"]) if s["kw_top5"] else "未命中关键词"
    v1 += "  ⚠️词频非正史·仅参考不作事实结论"
    v2 = "  ".join(f"{k}:{n}" for k, n in s["code_top5"]) if s["code_top5"] else "未命中股票代码"
    v3 = "  ".join(f"{k}:{n}" for k, n in s["author_top5"]) if s["author_top5"] else "0作者"
    v3 += "  ⚠️词频非正史·仅参考"
    lines.append(f"| 1 | TOP5 关键词（板块/情绪/题材/操作） | {v1} |")
    lines.append(f"| 2 | TOP5 股票代码（6位A股，命中次数） | {v2} |")
    lines.append(f"| 3 | TOP5 活跃作者（发言条数多→少） | {v3} |")
    lines.append(f"| 4 | 基本统计（期末={dash}） | 总消息 {s['total_msgs']}条 / 活跃作者 {s['total_authors']}人 / Raw {len(srcs)}份 / message_count=0跳过 {zero_skip}件 |")
    lines.append("")
    lines.append("## 二、按时间旧→新（最早→最晚）消息摘录 TOP120 条（每条截断前200字，长截断）")
    lines.append("")
    lines.append("| # | 日期 | 时间 | 作者 | 正文前200字（>200字截断） | 来源文件 |")
    lines.append("|---|---|---|---|---|---|")
    cap = min(120, len(msgs))
    for i, m in enumerate(msgs[:cap], 1):
        body = m["body"].replace("\r", " ").replace("\n", "  ").replace("|", "/").replace("`", "'")
        if len(body) > 200:
            body = body[:200] + "…"
        src = (m.get("src") or "").replace("|", "/")
        lines.append(f"| {i} | {m['date'] or '—'} | {m['time'] or '—'} | {(m['author'] or '匿名').replace('|','/')[:22]} | {body} | {src} |")
    if len(msgs) > 120:
        lines.append(f"\n> 消息总数 {len(msgs)}>120，仅摘录前120条。要看完整 Raw 到 rooms/<房>/00_raw/*.json 打开。")
    lines.append("")
    lines.append("> 人类判断3格（机器不填，等你人工）：")
    lines.append("> ```")
    lines.append("> [ ] 情绪偏多空（强多/多/震荡/空/强空）：________")
    lines.append("> [ ] 主抓风格（打板/低吸/埋伏/空仓/轮动）：________")
    lines.append("> [ ] 次日节奏（接力高度/中位/首板/观望）：________")
    lines.append("> [ ] 复制上述4行贴入 20_absorb/NOTES.md，末尾补：已吸收 @ YYYY-MM-DD")
    lines.append("> ```")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_prefill(room_name: str, trade_ymd: str, msgs: list[dict], srcs: list[Path], zero_skip: int) -> str:
    s = summarize(msgs)
    dash = f"{trade_ymd[:4]}-{trade_ymd[4:6]}-{trade_ymd[6:8]}"
    lines = [
        f"# {room_name} {dash} Prefill 草稿（仅事实抽字段，不判；四格精简版）",
        "", f"- 生成：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 期末={dash}  Raw文件={len(srcs)}份  0坏跳过={zero_skip}件  消息={s['total_msgs']}  作者={s['total_authors']}",
        "",
        "## 事实表（只抽，不判情绪/风格/节奏）",
        "",
        "| 字段 | 值 |",
        "|---|---|",
        f"| 总消息条数 | {s['total_msgs']} |",
        f"| 当日新增消息数 | {len(msgs)}（与Raw内message_count一致，增量差见各Raw JSON newly_added_count字段） |",
        f"| 去重活跃作者数 | {s['total_authors']} |",
        f"| TOP5 关键词（频次高→低；⚠️词频非正史·仅参考不作事实结论） | { '  '.join(f'{k}:{n}' for k,n in s['kw_top5']) if s['kw_top5'] else '未命中' } |",
        f"| TOP5 股票代码（6位 命中次数） | { '  '.join(f'{k}:{n}' for k,n in s['code_top5']) if s['code_top5'] else '未命中' } |",
        f"| TOP5 活跃作者（发言条数；⚠️词频非正史·仅参考） | { '  '.join(f'{k}:{n}' for k,n in s['author_top5']) if s['author_top5'] else '0' } |",
        f"| 最后一条消息时间（按消息时间排） | { (msgs[-1]['date']+' '+msgs[-1]['time']) if msgs else '无' } |",
        f"| 最前一条消息时间（按消息时间排） | { (msgs[0]['date']+' '+msgs[0]['time']) if msgs else '无' } |",
        f"| 当日 Raw 文件名（按旧→新前3份） | {', '.join(x.name for x in srcs[:3]) }{ '…共' + str(len(srcs)) + '份' if len(srcs)>3 else '' } |",
        "",
        "## 判断3格（等你人工填，机器永不自动填）",
        "- 情绪偏多空：________",
        "- 主抓风格：________",
        "- 次日节奏：________",
        "",
        "> 吸收动作：填完3格 → 复制本段 + 3格 → 贴到 20_absorb/NOTES.md → 末尾写「已吸收 @ YYYY-MM-DD」",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rooms-root", required=True)
    ap.add_argument("--trade-date", required=True, help="YYYYMMDD 吸收至期末")
    ap.add_argument("--apply", action="store_true", help="真写盘（默认 DryRun 只打印前16行）")
    args = ap.parse_args()
    rooms_root = Path(args.rooms_root).resolve()
    td = args.trade_date
    print(f"=== A+B 24房 重做 Prefill草稿 + 人读摘要（期末={td}，apply={args.apply}）===")
    print(f"=== SKIP（你说自己重做）：{list(SKIP_ROOMS_USER_SAID_REDO_LATER.keys())} ===")
    totals = []
    for name in ROOMS_ALL24:
        if name in SKIP_ROOMS_USER_SAID_REDO_LATER:
            reason = SKIP_ROOMS_USER_SAID_REDO_LATER[name]
            totals.append((name, "SKIP_USER_SAID_REDO_LATER", 0, 0, reason))
            print(f"SKIP  [{name:<22}]  {reason}")
            continue
        room_dir = rooms_root / name
        msgs, srcs, zero_skip = load_room_messages(room_dir, td)
        if not msgs:
            totals.append((name, "SKIP_NO_MESSAGE_TODAY", 0, 0, f"Raw={len(srcs)}份 0坏={zero_skip} 消息=0（可能是还没补）"))
            print(f"SKIP  [{name:<22}]  当日无有效消息（Raw={len(srcs)}份 0坏={zero_skip}）")
            continue
        summary_md = render(name, td, msgs, srcs, zero_skip)
        prefill_md = render_prefill(name, td, msgs, srcs, zero_skip)
        s = summarize(msgs)
        if args.apply:
            ing = room_dir / "10_ingest"
            ing.mkdir(parents=True, exist_ok=True)
            out1 = ing / f"{name}_{td}_NOTES_partial_prefill.md"
            out2 = ing / f"{name}_{td}_人读摘要旧到新.md"
            out1.write_text(prefill_md, encoding="utf-8")
            out2.write_text(summary_md, encoding="utf-8")
            status = f"WROTE Prefill({out1.name}) + 人读摘要({out2.name})"
        else:
            head = "\n".join(summary_md.splitlines()[:14])
            print(f"--- DRY_RUN [{name}] 消息={s['total_msgs']} 作者={s['total_authors']} Raw={len(srcs)} ---\n{head}\n")
            status = "DRY_RUN 两件都未写"
        totals.append((name, status, len(msgs), s["total_authors"], f"Raw={len(srcs)} 0坏={zero_skip}"))
    print("")
    print("=== 汇总 24房（期末=2026-08-11） ===")
    wrote = 0; skip_user = 0; skip_nomsg = 0
    for t in totals:
        print(f"  {t[0]:<22}  | {t[1]:<20} | 消息{t[2]:>5}条 作者{t[3]:>4}人 | 备注:{t[4]}")
        if t[1].startswith("WROTE"): wrote += 1
        elif t[1].startswith("SKIP_USER"): skip_user += 1
        elif t[1].startswith("SKIP_NO_MESSAGE"): skip_nomsg += 1
    print(f"TOTAL：写入 Prefill+人读摘要 共 {wrote} 房  /  你说自己重做跳过 {skip_user} 房（A4机构电话/B23机构研报精选）  /  当日无有效消息跳过 {skip_nomsg} 房（{skip_nomsg}）")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
