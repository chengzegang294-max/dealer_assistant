import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

p = Path(r"d:/Stock/dealer_assistant/02_runtime/info_live_room_sampling/batch_08_rooms_backfill__20260812/00_raw")
# only this batch filenames
batch_names = [
"info_live_export__20260811_195325.json",
"info_live_incremental_export__20260811_194939.json",
"info_live_incremental_export__20260811_194637.json",
"info_live_incremental_export__20260811_194440.json",
"info_live_incremental_export__20260811_194004.json",
"info_live_incremental_export__20260811_193802.json",
"info_live_incremental_export__20260811_193642.json",
"info_live_incremental_export__20260811_193222.json",
"info_live_incremental_export__20260811_193118.json",
"info_live_incremental_export__20260811_192952.json",
"info_live_incremental_export__20260811_192752.json",
"info_live_export__20260811_192735.json",
"info_live_incremental_export__20260811_192517.json",
"info_live_export__20260811_192506.json",
"info_live_incremental_export__20260811_192325.json",
"info_live_export__20260811_192316.json",
"info_live_incremental_export__20260811_192146.json",
"info_live_incremental_export__20260811_192048.json",
"info_live_incremental_export__20260811_191944.json",
"info_live_incremental_export__20260811_191839.json",
"info_live_incremental_export__20260811_191730.json",
"info_live_export__20260811_191651.json",
"info_live_incremental_export__20260811_190530.json",
"info_live_incremental_export__20260811_185711.json",
"info_live_incremental_export__20260811_185537.json",
"info_live_incremental_export__20260811_185230.json",
"info_live_incremental_export__20260811_184919.json",
"info_live_export__20260811_184909.json",
]
A = {
"复盘哥","独家老师5号","独家短线老师6号","机构电话会议纪要+小作文+情报",
"梅森","顺势而为","混江龙","天赢居","先知"
}
B = {
"天机","游资胖大叔","潜伏王者","k神","周期女王","格兰投研","擒龙小师姐",
"独家竞价低吸","小锦鲤","核心逻辑社","梦幻一步","新生代","龙头交易猿",
"机构研报资讯精选","小作文嗅嗅+机构研报"
}

def bucket(ra):
    if not ra: return "?"
    if ra in A: return "A"
    if ra in B: return "B"
    for x in A:
        if ra.startswith(x) or x.startswith(ra): return "A"
    for x in B:
        if ra.startswith(x) or x.startswith(ra): return "B"
    return "?"

def count_msgs(d):
    n = d.get("message_count") or d.get("total_messages")
    if n is not None: return int(n)
    for k in ("visible_messages","messages","all_messages"):
        if isinstance(d.get(k), list): return len(d[k])
    return 0

rows = []
by_room = defaultdict(list)
for n in batch_names:
    f = p / n
    if not f.exists():
        rows.append((n, "MISSING", 0, "", "?", "file missing"))
        continue
    d = json.loads(f.read_text(encoding="utf-8"))
    ra = (d.get("room_anchor") or "").strip()
    stop = d.get("stop_reason") or ""
    nmsg = count_msgs(d)
    b = bucket(ra)
    kind = "current" if "info_live_export__" in n and "incremental" not in n else "incremental"
    rows.append((n, ra, nmsg, stop, b, kind))
    by_room[ra].append((n, nmsg, stop, kind))

out = Path(r"d:/Stock/dealer_assistant/02_runtime/info_live_room_sampling/batch_08_rooms_backfill__20260812/A5_AB本批吸收回报__20260812_night2.md")
lines = []
lines.append("# A5 A+B 本批吸收回报（night2 · 28 文件）")
lines.append("")
lines.append("更新时间：" + datetime.now().strftime("%Y-%m-%d %H:%M"))
lines.append("状态：**已复制中转篮 + migrate 入 rooms/00_raw**（仅 raw 层）")
lines.append("给 Trae：本页 + SENTINEL + 勿对未点「可吸收」的房强开 NOTES。")
lines.append("")
lines.append("## 1. 按房汇总")
lines.append("")
lines.append("| 房间 | 桶 | 本批文件数 | 最高条数 | 备注 |")
lines.append("|------|----|-----------|---------|------|")
for ra in sorted(by_room.keys(), key=lambda x: (bucket(x), x)):
    items = by_room[ra]
    mx = max(t[1] for t in items)
    notes = []
    if mx == 0: notes.append("有 0 条文件")
    if any(t[2]=="scroll_end" for t in items): notes.append("含 scroll_end")
    if any(t[2]=="manual_limit" for t in items): notes.append("含 manual_limit")
    if ra in ("机构研报资讯精选","机构电话会议纪要+小作文+情报"):
        if mx > 0:
            notes.append("本批重导有内容→解除勿吸收（见 §3）")
        else:
            notes.append("仍零内容，保持勿吸收")
    lines.append(f"| {ra} | {bucket(ra)} | {len(items)} | {mx} | {'; '.join(notes) or '—'} |")
lines.append("")
lines.append("## 2. 逐文件")
lines.append("")
lines.append("| 文件 | 房间 | 桶 | 类型 | 条数 | stop |")
lines.append("|------|------|----|------|------|------|")
for n, ra, nmsg, stop, b, kind in rows:
    lines.append(f"| `{n}` | {ra} | {b} | {kind} | {nmsg} | {stop or '—'} |")
lines.append("")
lines.append("## 3. 误跑清单更新")
lines.append("")
# decide lifts
phone = by_room.get("机构电话会议纪要+小作文+情报") or []
inst = by_room.get("机构研报资讯精选") or []
# also prefix match keys
for k,v in list(by_room.items()):
    if "机构电话" in k and k != "机构电话会议纪要+小作文+情报":
        phone = phone + v
    if "机构研报" in k and k != "机构研报资讯精选":
        inst = inst + v
pmx = max([t[1] for t in phone], default=-1)
imx = max([t[1] for t in inst], default=-1)
lines.append(f"- 机构电话会议纪要+小作文+情报：本批最高条数={pmx}")
lines.append(f"- 机构研报资讯精选：本批最高条数={imx}")
lines.append("")
lines.append("## 4. 路径")
lines.append("")
lines.append("- 中转：`batch_08_rooms_backfill__20260812/00_raw/`")
lines.append("- 正史：`rooms/<房>/00_raw/`")
lines.append("- 索引：`rooms/SENTINEL_INDEX.md`")
lines.append("")
lines.append("## 5. Trae 硬规则")
lines.append("")
lines.append("1. 本批仅 raw 入柜；NOTES 仍需用户 `/吸收确认`")
lines.append("2. 微信金十停线；C/D 不进 rooms")
lines.append("3. 空壳文件保留作废样，引用正史时以有条数文件为准")
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("rooms", len(by_room), "files", len(rows))
print("wrote", out)
for ra, items in sorted(by_room.items(), key=lambda x: -max(t[1] for t in x[1])):
    print(f"{bucket(ra)}\t{ra}\tnfiles={len(items)}\tmax={max(t[1] for t in items)}")
