from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HEADER = [
    "visible_order",
    "room_anchor",
    "auto_priority_hint",
    "auto_tags",
    "score_a_stock_relevance",
    "score_intraday_timeliness",
    "score_uniqueness",
    "score_traceability",
    "score_update_stability",
    "score_low_noise",
    "score_history_review_friendly",
    "total_score",
    "tier",
    "review_status",
    "reviewer_note",
]


DATE_RE = re.compile(r"20\d{2}/\d{2}/\d{2}")
TIME_RE = re.compile(r"\b\d{2}/\d{2}\s+\d{2}:\d{2}\b|\b\d{2}:\d{2}:\d{2}\b")


def clean_text(value: object) -> str:
    return " ".join(str(value or "").replace("\r", "\n").split())


def slug_like(value: str) -> str:
    text = clean_text(value)
    if not text:
        return "unknown"
    return (
        text.replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
        .replace("*", "_")
        .replace("?", "_")
        .replace("\"", "_")
        .replace("<", "_")
        .replace(">", "_")
        .replace("|", "_")
        .replace(" ", "_")
    )


def is_room_title_candidate(item: dict) -> bool:
    text = clean_text(item.get("room_anchor", ""))
    css_path = clean_text(item.get("css_path", ""))
    class_name = clean_text(item.get("class_name", ""))

    if not text:
        return False
    if any(
        bad in text
        for bad in [
            "直播间列表",
            "重要提示",
            "立即前往APP签到",
            "开通 取消",
            "讲师 ",
            "签到",
        ]
    ):
        return False
    if DATE_RE.search(text) or TIME_RE.search(text):
        return False
    if len(text) > 30:
        return False
    if "text-black text-bold" in class_name:
        return True
    if "#room" in css_path and "text-cut" in class_name and "text-gray" not in class_name:
        return True
    return False


def infer_tags(room_anchor: str) -> list[str]:
    text = clean_text(room_anchor)
    checks = [
        ("a_stock_core", ["竞价", "擒妖", "低吸", "主波浪", "盘面", "擒龙"]),
        ("research", ["机构", "研报", "电话会议", "投研", "小作文", "资讯"]),
        ("review", ["复盘"]),
        ("notice", ["通知群", "置顶"]),
        ("trial", ["试着更新", "试更新", "暂时没有"]),
    ]
    tags: list[str] = []
    for tag, keywords in checks:
        if any(keyword in text for keyword in keywords):
            tags.append(tag)
    if not tags:
        tags.append("general")
    return tags


def score_room(room_anchor: str, tags: list[str]) -> dict[str, int | str]:
    a_stock = 8
    timeliness = 8
    uniqueness = 6
    traceability = 6
    stability = 6
    noise = 6
    history = 4

    if "research" in tags:
        a_stock += 10
        uniqueness += 6
        traceability += 5
    if "a_stock_core" in tags:
        a_stock += 12
        timeliness += 8
        traceability += 3
    if "review" in tags:
        traceability += 4
        history += 1
    if "notice" in tags:
        a_stock -= 8
        timeliness -= 2
        uniqueness -= 3
        noise -= 4
    if "trial" in tags:
        stability -= 3
        noise -= 1

    if "小作文嗅嗅+机构研报" in room_anchor:
        uniqueness += 4
        timeliness += 2
    if "机构电话会议纪要+小作文+情报" in room_anchor:
        uniqueness += 4
        traceability += 2
    if "机构研报资讯精选" in room_anchor:
        timeliness += 2
    if "猫哥竞价" in room_anchor:
        timeliness += 4
    if "银河投递员" in room_anchor:
        timeliness += 3
    if "七福潜伏低吸" in room_anchor:
        timeliness += 2

    a_stock = max(0, min(25, a_stock))
    timeliness = max(0, min(20, timeliness))
    uniqueness = max(0, min(15, uniqueness))
    traceability = max(0, min(15, traceability))
    stability = max(0, min(10, stability))
    noise = max(0, min(10, noise))
    history = max(0, min(5, history))

    total = a_stock + timeliness + uniqueness + traceability + stability + noise + history
    if total >= 80:
        tier = "S"
        hint = "high"
    elif total >= 65:
        tier = "A"
        hint = "medium_high"
    elif total >= 50:
        tier = "B"
        hint = "medium"
    else:
        tier = "C"
        hint = "low"

    return {
        "score_a_stock_relevance": a_stock,
        "score_intraday_timeliness": timeliness,
        "score_uniqueness": uniqueness,
        "score_traceability": traceability,
        "score_update_stability": stability,
        "score_low_noise": noise,
        "score_history_review_friendly": history,
        "total_score": total,
        "tier": tier,
        "auto_priority_hint": hint,
    }


def build_rows(data: dict) -> list[dict[str, str]]:
    seen: dict[str, dict] = {}
    for item in data.get("rooms", []):
        if not is_room_title_candidate(item):
            continue
        room_anchor = clean_text(item.get("room_anchor", ""))
        order = int(item.get("visible_order", 9999))
        current = seen.get(room_anchor)
        if current is None or order < int(current["visible_order"]):
            seen[room_anchor] = {
                "visible_order": str(order),
                "room_anchor": room_anchor,
            }

    rows: list[dict[str, str]] = []
    for room_anchor, base in sorted(seen.items(), key=lambda x: int(x[1]["visible_order"])):
        tags = infer_tags(room_anchor)
        scored = score_room(room_anchor, tags)
        rows.append(
            {
                "visible_order": base["visible_order"],
                "room_anchor": room_anchor,
                "auto_priority_hint": str(scored["auto_priority_hint"]),
                "auto_tags": ",".join(tags),
                "score_a_stock_relevance": str(scored["score_a_stock_relevance"]),
                "score_intraday_timeliness": str(scored["score_intraday_timeliness"]),
                "score_uniqueness": str(scored["score_uniqueness"]),
                "score_traceability": str(scored["score_traceability"]),
                "score_update_stability": str(scored["score_update_stability"]),
                "score_low_noise": str(scored["score_low_noise"]),
                "score_history_review_friendly": str(scored["score_history_review_friendly"]),
                "total_score": str(scored["total_score"]),
                "tier": str(scored["tier"]),
                "review_status": "auto_scored_needs_human_confirmation",
                "reviewer_note": "",
            }
        )
    return rows


def build_tsv(rows: list[dict[str, str]]) -> str:
    lines = ["\t".join(HEADER)]
    for row in rows:
        lines.append("\t".join(clean_text(row.get(col, "")) for col in HEADER))
    return "\n".join(lines) + "\n"


def build_summary(data: dict, rows: list[dict[str, str]], source_path: Path) -> str:
    top_rows = sorted(rows, key=lambda row: int(row["total_score"]), reverse=True)
    s_rows = [row for row in top_rows if row["tier"] == "S"]
    a_rows = [row for row in top_rows if row["tier"] == "A"]
    b_rows = [row for row in top_rows if row["tier"] == "B"]

    lines = [
        "# 信息直播间房间首轮评分卡摘要",
        "",
        f"- source_json: `{source_path}`",
        f"- exported_at: `{clean_text(data.get('exported_at', ''))}`",
        f"- raw_room_count: `{data.get('room_count', 0)}`",
        f"- cleaned_room_count: `{len(rows)}`",
        "- scoring_mode: `auto_scored_needs_human_confirmation`",
        "",
        "## 默认置顶候选",
        "",
    ]

    if s_rows or a_rows:
        for row in s_rows + a_rows[:5]:
            lines.append(
                f"- `{row['tier']}` | `{row['room_anchor']}` | `{row['total_score']}` | `{row['auto_tags']}`"
            )
    else:
        lines.append("- 当前无 `S/A` 候选")

    lines.extend(["", "## 常规跟踪候选", ""])
    if b_rows:
        for row in b_rows[:8]:
            lines.append(
                f"- `{row['tier']}` | `{row['room_anchor']}` | `{row['total_score']}`"
            )
    else:
        lines.append("- 当前无 `B` 候选")

    lines.extend(
        [
            "",
            "## 说明",
            "",
            "- 本轮评分以房间名关键词和当前定位做自动初判，仍需要人审确认。",
            "- 原始导出里混入了右侧正文卡片和弹窗元素，本摘要已先做清洗，只保留房间标题候选。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a cleaned room scorecard from live-room room-list JSON."
    )
    parser.add_argument("--input", required=True, help="Path to room-list JSON")
    parser.add_argument("--out-dir", required=True, help="Directory to place outputs")
    args = parser.parse_args()

    input_path = Path(args.input)
    out_dir = Path(args.out_dir)
    data = json.loads(input_path.read_text(encoding="utf-8"))
    rows = build_rows(data)

    export_date = clean_text(data.get("exported_at", "")[:10]) or "unknown_date"
    export_slug = slug_like(export_date)

    out_dir.mkdir(parents=True, exist_ok=True)
    tsv_path = out_dir / f"info_live_room_scorecard__{export_slug}.tsv"
    md_path = out_dir / f"info_live_room_scorecard_summary__{export_slug}.md"

    tsv_path.write_text(build_tsv(rows), encoding="utf-8")
    md_path.write_text(build_summary(data, rows, input_path), encoding="utf-8")

    print(str(tsv_path))
    print(str(md_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
