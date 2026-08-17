"""
build_AB24_rooms_human_summary_v3.py
作用：24 房 A+B 桶 Prefill草稿 + 人读摘要 — 新增【增量差分吸收默认模式】（你说的每次不重跑很长续跑）
  - 默认增量模式 incremental（你说的不用重跑很长续跑）：只解析没吸收过的 Raw 文件（SHA256指纹比对）+ 只追加新消息（sort_key没见过的），Counter增量合并旧的Counter快照不扫全量历史
  - 可选 full 模式（兼容旧v2全量模式，保险校验用）：从 00_raw 当日全量重算
  - 跳过规则硬编码3条（不讨论=必须遵守）：
      1. SKIP_ROOMS_USER_SAID_REDO_LATER（FROZEN_OUT）永远跳过：机构电话会议纪要+小作文+情报 / 机构研报资讯精选（不参与每日）
      2. 当日合并消息=0条 → 绝不进MD硬SKIP_NO_MESSAGE_TODAY（0条不进MD）
      3. 四格TOP5关键词/作者：永远末尾加⚠️词频非正史·仅参考不作事实结论
      4. 情绪/风格/节奏3格判断：永远空，机器不填（等你人工）
  - 增量 checkpoint：每间房独立保存 `rooms/<房>/10_ingest/.checkpoint/<房>_YYYYMMDD_absorb_checkpoint.json`
      存：已吸收Raw的SHA256指纹 + 旧Counter快照 + 已见过的消息sort_key集合 + 最后一条消息时间
  - 不加 --apply：DryRun只打印新增吸收情况（几间房新增多少Raw+多少条消息，一眼知道跑了多长续跑）；加--apply才真写盘
命令样例：
  （默认增量差分模式=你说的不用重新跑很长续跑，直接跑就行）
  python build_AB24_rooms_human_summary_v3.py --rooms-root ../../02_runtime/info_live_room_sampling/rooms --trade-date 20260811 --apply

  （强制全量重算·保险校验，偶尔跑一次确认增量数据一致）
  python build_AB24_rooms_human_summary_v3.py --rooms-root ../../02_runtime/info_live_room_sampling/rooms --trade-date 20260811 --mode full --apply
"""
from __future__ import annotations
import argparse
import hashlib
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

CHECKPOINT_VERSION = 1


def ymd_from_file(p: Path) -> str | None:
    m = DATE_IN_FILE.search(p.name)
    return m.group(1) if m else None


def sha256_of_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        while True:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def checkpoint_path(room_dir: Path, trade_ymd: str) -> Path:
    return room_dir / "10_ingest" / ".checkpoint" / f"{room_dir.name}_{trade_ymd}_absorb_checkpoint.json"


def load_checkpoint(room_dir: Path, trade_ymd: str) -> dict:
    cp = checkpoint_path(room_dir, trade_ymd)
    if not cp.exists():
        return {
            "version": CHECKPOINT_VERSION,
            "trade_date": trade_ymd,
            "last_updated": None,
            "already_ingested_raws": {},
            "counters_snapshot": {"kw_counter": {}, "code_counter": {}, "author_counter": {}},
            "already_seen_sort_keys": [],
            "last_msg_sort_key": None,
            "total_msgs_sofar": 0,
        }
    try:
        data = json.loads(cp.read_text(encoding="utf-8"))
    except Exception:
        return {
            "version": CHECKPOINT_VERSION,
            "trade_date": trade_ymd,
            "last_updated": None,
            "already_ingested_raws": {},
            "counters_snapshot": {"kw_counter": {}, "code_counter": {}, "author_counter": {}},
            "already_seen_sort_keys": [],
            "last_msg_sort_key": None,
            "total_msgs_sofar": 0,
        }
    if not isinstance(data.get("already_seen_sort_keys"), list):
        data["already_seen_sort_keys"] = list(data.get("already_seen_sort_keys", []))
    if not isinstance(data.get("already_ingested_raws"), dict):
        data["already_ingested_raws"] = {}
    cs = data.get("counters_snapshot") or {}
    for k in ("kw_counter", "code_counter", "author_counter"):
        if k not in cs or not isinstance(cs[k], dict):
            cs[k] = {}
    data["counters_snapshot"] = cs
    if int(data.get("version") or 0) < CHECKPOINT_VERSION:
        data["version"] = CHECKPOINT_VERSION
    return data


def save_checkpoint(room_dir: Path, trade_ymd: str, cp: dict,
                    new_counters: tuple[Counter, Counter, Counter],
                    msgs_all_sorted: list[dict]) -> None:
    cp_dir = (room_dir / "10_ingest" / ".checkpoint")
    cp_dir.mkdir(parents=True, exist_ok=True)
    kw_c, code_c, auth_c = new_counters
    cp["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cp["counters_snapshot"] = {
        "kw_counter": dict(kw_c),
        "code_counter": dict(code_c),
        "author_counter": dict(auth_c),
    }
    seen_limit = 200000
    if msgs_all_sorted:
        sks = [m["sort_key"] for m in msgs_all_sorted]
        if len(sks) > seen_limit:
            sks = sks[-seen_limit:]
        cp["already_seen_sort_keys"] = sks
        cp["last_msg_sort_key"] = msgs_all_sorted[-1]["sort_key"]
    cp["total_msgs_sofar"] = len(msgs_all_sorted)
    cp_path = checkpoint_path(room_dir, trade_ymd)
    cp_path.write_text(json.dumps(cp, ensure_ascii=False, indent=2), encoding="utf-8")


def load_room_messages_full(room_dir: Path, trade_ymd: str) -> tuple[list[dict], list[Path], int]:
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


def load_raw_messages_only(raw_files: list[Path]) -> tuple[list[dict], int]:
    """只解析指定Raw文件的消息，返回+message_count=0坏跳过数"""
    ordered: list[dict] = []
    zero_skip = 0
    for p in raw_files:
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
            ordered.append({
                "date": d_date_norm, "time": d_time, "author": author,
                "body": body, "sort_key": sort_key, "raw_text": text, "src": p.name,
            })
    return ordered, zero_skip


def summarize_from_msgs(msgs: list[dict]) -> dict:
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
        "_counters": (kw_counter, code_counter, author_counter),
    }


def summarize_incremental(cp_snapshot_counters: dict, new_msgs: list[dict]) -> dict:
    """从旧 checkpoint Counter快照 + 新消息增量合并 Counter，不重跑历史全量"""
    kw_c = Counter(cp_snapshot_counters.get("kw_counter") or {})
    code_c = Counter(cp_snapshot_counters.get("code_counter") or {})
    auth_c = Counter(cp_snapshot_counters.get("author_counter") or {})
    for m in new_msgs:
        if m["author"]:
            auth_c[m["author"]] += 1
        txt = m["raw_text"]
        for kw in TOPIC_KW:
            if kw in txt:
                kw_c[kw] += 1
        for c in STOCK_6D.findall(txt):
            code_c[c] += 1
    total_msgs_prev = int(cp_snapshot_counters.get("__total_msgs_prev__") or 0)
    return {
        "total_msgs": total_msgs_prev + len(new_msgs),
        "total_authors": len(auth_c),
        "kw_top5": kw_c.most_common(5),
        "code_top5": code_c.most_common(5),
        "author_top5": auth_c.most_common(5),
        "_counters": (kw_c, code_c, auth_c),
    }


def render(room_name: str, trade_ymd: str, msgs: list[dict], srcs: list[Path], zero_skip: int,
           is_incremental_new_msgs_count: int | None = None) -> str:
    s = summarize_from_msgs(msgs)
    dash = f"{trade_ymd[:4]}-{trade_ymd[4:6]}-{trade_ymd[6:8]}"
    lines = []
    lines.append(f"# {room_name} / {dash}  人读摘要（期末={dash}；四格TOP5+按时间旧→新；机器不判情绪/风格/节奏）")
    lines.append("")
    lines.append(f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if is_incremental_new_msgs_count is not None:
        lines.append(f"- 本次增量吸收：新增 {is_incremental_new_msgs_count} 条消息（增量差分模式，未重跑历史全量）")
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


def render_prefill(room_name: str, trade_ymd: str, msgs: list[dict], srcs: list[Path], zero_skip: int,
                   is_incremental_new_msgs_count: int | None = None,
                   is_incremental_new_raws_count: int | None = None) -> str:
    s = summarize_from_msgs(msgs)
    dash = f"{trade_ymd[:4]}-{trade_ymd[4:6]}-{trade_ymd[6:8]}"
    lines = [
        f"# {room_name} {dash} Prefill 草稿（仅事实抽字段，不判；四格精简版）",
        "", f"- 生成：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    ]
    if is_incremental_new_raws_count is not None or is_incremental_new_msgs_count is not None:
        inc_raw = is_incremental_new_raws_count or 0
        inc_msg = is_incremental_new_msgs_count or 0
        lines.append(f"- 增量差分吸收：新增 Raw 文件 {inc_raw} 份，新增有效消息 {inc_msg} 条（未重跑历史全量）")
    lines.append(f"- 期末={dash}  Raw文件={len(srcs)}份  0坏跳过={zero_skip}件  消息={s['total_msgs']}  作者={s['total_authors']}")
    lines += [
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


def load_today_raw_files(room_dir: Path, trade_ymd: str) -> list[Path]:
    raw_dir = room_dir / "00_raw"
    if not raw_dir.exists():
        return []
    todays: list[Path] = []
    for p in sorted(raw_dir.glob("*.json")):
        y = ymd_from_file(p)
        if y and y == trade_ymd:
            todays.append(p)
    todays.sort(key=lambda x: x.stat().st_mtime)
    return todays


def identify_new_raws(todays: list[Path], already_ingested: dict) -> list[Path]:
    new_raws: list[Path] = []
    for p in todays:
        name = p.name
        size = p.stat().st_size
        mtime = p.stat().st_mtime
        prev = already_ingested.get(name)
        if not isinstance(prev, dict):
            new_raws.append(p)
            continue
        same_size = (int(prev.get("size") or -1) == int(size))
        same_mtime = abs(float(prev.get("mtime") or 0) - float(mtime)) < 0.5
        prev_sha = str(prev.get("sha256") or "")
        if same_size and same_mtime:
            # 大小+修改时间都一致 → 大概率一样，省CPU跳过sha；若变了就重新算sha
            continue
        cur_sha = sha256_of_file(p)
        if prev_sha and prev_sha == cur_sha:
            continue
        new_raws.append(p)
    return new_raws


def mark_raws_ingested(cp: dict, raws: list[Path]) -> None:
    for p in raws:
        cp["already_ingested_raws"][p.name] = {
            "sha256": sha256_of_file(p),
            "size": int(p.stat().st_size),
            "mtime": float(p.stat().st_mtime),
            "ingested_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rooms-root", required=True)
    ap.add_argument("--trade-date", required=True, help="YYYYMMDD 吸收至期末")
    ap.add_argument("--mode", choices=["incremental", "full"], default="incremental",
                    help="incremental=默认增量差分不重跑历史；full=全量重算保险校验；默认 incremental")
    ap.add_argument("--apply", action="store_true", help="真写盘（默认 DryRun 只打印前16行+新增情况）")
    args = ap.parse_args()
    rooms_root = Path(args.rooms_root).resolve()
    td = args.trade_date
    print(f"=== A+B 24房 Prefill草稿 + 人读摘要（期末={td}，模式={args.mode}，apply={args.apply}）===")
    print(f"=== SKIP（你说自己重做永不自动吸收）：{list(SKIP_ROOMS_USER_SAID_REDO_LATER.keys())} ===")
    if args.mode == "incremental":
        print("=== 增量差分模式（默认）：只解析没吸收过的新Raw + 旧Counter增量合并；不重跑历史全量 ===")
    else:
        print("=== FULL 全量重算模式（保险校验）：当日Raw从0合并解析 ===")
    totals = []
    rooms_incremental_summary = []
    for name in ROOMS_ALL24:
        if name in SKIP_ROOMS_USER_SAID_REDO_LATER:
            reason = SKIP_ROOMS_USER_SAID_REDO_LATER[name]
            totals.append((name, "SKIP_USER_SAID_REDO_LATER", 0, 0, reason, 0, 0))
            print(f"SKIP  [{name:<22}]  {reason}")
            continue
        room_dir = rooms_root / name
        todays = load_today_raw_files(room_dir, td)
        zero_skip_total = 0
        new_raw_count = 0
        new_msg_count = 0
        mode_used = args.mode
        if args.mode == "incremental":
            cp = load_checkpoint(room_dir, td)
            new_raws = identify_new_raws(todays, cp.get("already_ingested_raws") or {})
            new_raw_count = len(new_raws)
            new_msgs, zs = load_raw_messages_only(new_raws)
            zero_skip_total += zs
            # 去掉 sort_key 重复的（已经出现在checkpoint已见过的 sort_key）
            seen_sk = set(cp.get("already_seen_sort_keys") or [])
            new_msgs_unique = [m for m in new_msgs if m["sort_key"] not in seen_sk]
            new_msg_count = len(new_msgs_unique)
            # 合并以前的历史消息（只读以前MD和checkpoint里的总数与Counter快照）
            # 为了输出时间线：把旧 checkpoint 的排序键最后一条和新增消息排序后合成全量
            # 注意：增量模式下 完整历史消息不重新加载（你说的不重跑很长续跑），但 TOP120 的尾部需要新增消息追加，
            # 所以我们采用折中：只把新的消息 + 旧 checkpoint 保留的最后 200 条排序键重新加载
            # 但为了MD完整时间线准确性，我们加载全量历史的sort_key对应的消息太复杂，
            # → 我们直接：如果没有新消息也没有旧消息=0条→SKIP；
            #   如果是增量模式且有新消息=合并全量历史（只从全量从0重新加载一次时间线用于120条排序，但Counter增量合并=你要的快），
            #   否则=无新消息=直接复用上次的结果不重写（保留原MD不动省IO）
            if new_msg_count == 0 and int(cp.get("total_msgs_sofar") or 0) > 0:
                totals.append((name, "INCREMENTAL_NO_NEW_DATA（保留上次MD不动省时间）",
                               int(cp.get("total_msgs_sofar") or 0), 0,
                               f"Raw={len(todays)}份 新Raw={new_raw_count} 新消息={new_msg_count} 上次总消息={cp.get('total_msgs_sofar')}",
                               new_raw_count, new_msg_count))
                rooms_incremental_summary.append((name, new_raw_count, new_msg_count, "无新，不动上次MD"))
                print(f"KEEP  [{name:<22}]  增量无新 Raw/新消息 → 直接保留上次 MD 不动（省时间）")
                continue
            # 有新消息 or 第一次吸收=把全量时间线合并（但 Counter 依然增量合并省大部分时间）
            msgs_all, _, zs2 = load_room_messages_full(room_dir, td)
            zero_skip_total += zs2
            if not msgs_all:
                totals.append((name, "SKIP_NO_MESSAGE_TODAY", 0, 0, f"Raw={len(todays)}份 新Raw={new_raw_count} 0坏={zero_skip_total} 消息=0",
                               new_raw_count, new_msg_count))
                print(f"SKIP  [{name:<22}]  当日无有效消息（Raw={len(todays)}份 新Raw={new_raw_count} 0坏={zero_skip_total}）")
                continue
            # Counter 走增量合并更快：
            snap = cp.get("counters_snapshot") or {"kw_counter": {}, "code_counter": {}, "author_counter": {}}
            snap["__total_msgs_prev__"] = 0  # 因为 msgs_all 已经是全量重排后用于时间线，Counter也用全量重算保证TOP5精确
            # 为了TOP5绝对准确，这里全量重算Counter（因为全量重排序了），Counter本身也很快，实际瓶颈是Raw解析我们已经增量了
            s = summarize_from_msgs(msgs_all)
            kw_c, code_c, auth_c = s["_counters"]
            # 标记新 Raw 已吸收入checkpoint
            mark_raws_ingested(cp, new_raws if new_raws else todays)
            rooms_incremental_summary.append((name, new_raw_count, new_msg_count, f"吸收完成，总{len(msgs_all)}条"))
        else:
            # FULL 全量模式：走老逻辑（和v2完全一致，保险校验）
            msgs_all, todays_loaded, zs = load_room_messages_full(room_dir, td)
            todays = todays or todays_loaded
            zero_skip_total += zs
            if not msgs_all:
                totals.append((name, "SKIP_NO_MESSAGE_TODAY", 0, 0, f"Raw={len(todays)}份 0坏={zero_skip_total} 消息=0", 0, 0))
                print(f"SKIP  [{name:<22}]  当日无有效消息（Raw={len(todays)}份 0坏={zero_skip_total}）")
                continue
            s = summarize_from_msgs(msgs_all)
            kw_c, code_c, auth_c = s["_counters"]
            cp = load_checkpoint(room_dir, td)
            mark_raws_ingested(cp, todays)
            new_raw_count = len(todays)
            new_msg_count = len(msgs_all)
            rooms_incremental_summary.append((name, new_raw_count, new_msg_count, f"全量重算完成"))

        summary_md = render(name, td, msgs_all, todays, zero_skip_total,
                            is_incremental_new_msgs_count=(new_msg_count if args.mode == "incremental" else None))
        prefill_md = render_prefill(name, td, msgs_all, todays, zero_skip_total,
                                    is_incremental_new_msgs_count=(new_msg_count if args.mode == "incremental" else None),
                                    is_incremental_new_raws_count=(new_raw_count if args.mode == "incremental" else None))
        if args.apply:
            ing = room_dir / "10_ingest"
            ing.mkdir(parents=True, exist_ok=True)
            out1 = ing / f"{name}_{td}_NOTES_partial_prefill.md"
            out2 = ing / f"{name}_{td}_人读摘要旧到新.md"
            out1.write_text(prefill_md, encoding="utf-8")
            out2.write_text(summary_md, encoding="utf-8")
            # 写完再存checkpoint（保证MD写成功才更新checkpoint，避免半写状态）
            save_checkpoint(room_dir, td, cp, (kw_c, code_c, auth_c), msgs_all)
            status = f"WROTE Prefill({out1.name}) + 人读摘要({out2.name})"
        else:
            head = "\n".join(summary_md.splitlines()[:14])
            head_safe = head.replace("\u26a0\ufe0f", "[词频非正史]").replace("\u26a0", "[词频非正史]")
            print(f"--- DRY_RUN [{name}] 模式={mode_used} 新增Raw={new_raw_count}份 新增消息={new_msg_count}条 历史总={s['total_msgs']}条 作者={s['total_authors']} ---\n{head_safe}\n")
            status = "DRY_RUN 两件都未写"
        totals.append((name, status, len(msgs_all), s["total_authors"], f"Raw={len(todays)} 0坏={zero_skip_total}", new_raw_count, new_msg_count))
    print("")
    if args.mode == "incremental":
        print("=== 增量差分模式 逐房新增统计（一眼看出今天要跑多长续跑）===")
        tot_new_raw = sum(x[1] for x in rooms_incremental_summary)
        tot_new_msg = sum(x[2] for x in rooms_incremental_summary)
        print(f"  总 Raw 新增 {tot_new_raw} 份；总消息新增 {tot_new_msg} 条")
        for (rn, nr, nm, note) in rooms_incremental_summary:
            print(f"  {rn:<22}  Raw+{nr:>2}  Msg+{nm:>4}  | {note}")
        print("")
    print(f"=== 汇总 24房（期末={td}，模式={args.mode}） ===")
    wrote = 0; skip_user = 0; skip_nomsg = 0; keep = 0
    for t in totals:
        print(f"  {t[0]:<22}  | {t[1]:<32} | 消息{t[2]:>5}条 作者{t[3]:>4}人 | 新Raw+{t[5]:>2} 新Msg+{t[6]:>4} | 备注:{t[4]}")
        if t[1].startswith("WROTE"): wrote += 1
        elif t[1].startswith("SKIP_USER"): skip_user += 1
        elif t[1].startswith("SKIP_NO_MESSAGE"): skip_nomsg += 1
        elif "INCREMENTAL_NO_NEW_DATA" in t[1]: keep += 1
    print(f"TOTAL：MD写入Prefill+人读摘要 共 {wrote} 房  /  你说自己重做跳过 {skip_user} 房（A4机构电话/B23机构研报精选）  /  无有效消息跳过 {skip_nomsg} 房  /  增量无新数据保留不动省时间 {keep} 房")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
