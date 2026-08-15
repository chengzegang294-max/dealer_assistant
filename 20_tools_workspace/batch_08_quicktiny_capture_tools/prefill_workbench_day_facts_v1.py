# -*- coding: utf-8 -*-
"""Prefill workbench day FACT fields only (three-card shell).

Never fills judgment fields (bias / confirm yes-no / judge_ok / one-liners).
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(r"d:\Stock\dealer_assistant")
DEFAULT_OUT_DIR = (
    ROOT
    / r"02_runtime\shortline_workbench\batch_01_three_card_shell__20260809\daily"
)
DEFAULT_SECTOR_DIR = ROOT / r"02_runtime\quicktiny_capture\sector_daily_snapshots"
DEFAULT_P1_DIR = (
    ROOT
    / r"02_runtime\shortline_funding_gap\batch_01_p1_manual_validation__20260809\daily"
)


def load_json(path: Path | None) -> dict[str, Any] | None:
    if not path:
        return None
    if not path.exists():
        raise FileNotFoundError(path)
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError(f"json root must be object: {path}")
    return obj


def ladder_summary(payload: dict[str, Any] | None) -> str:
    if not payload:
        return "（无 ladder 输入）"
    dates = payload.get("dates") or []
    if not dates:
        return "（ladder 无 dates）"
    day = dates[0]
    boards = day.get("boards") or []
    levels = []
    for b in boards:
        if isinstance(b, dict) and b.get("level") is not None:
            n = len(b.get("stocks") or [])
            levels.append(f"{b.get('level')}板x{n}")
    top = f"最高板={boards[0].get('level')}" if boards else "最高板=?"
    dist = "；".join(levels[:6]) if levels else "无板高分布"
    return f"{top}；总连板池={day.get('totalStocks')}；{dist}"


def sector_top_note(payload: dict[str, Any] | None) -> str:
    if not payload:
        return "（无 sector 输入）"
    if payload.get("success") is False:
        return f"snapshot失败 code={payload.get('code')}"
    data = payload.get("data") or {}
    rows = [
        r
        for r in (data.get("rows") or [])
        if isinstance(r, dict) and not r.get("__truncated__")
    ]
    rows_sorted = sorted(rows, key=lambda r: r.get("mainNetAmount") or 0, reverse=True)
    top = []
    for r in rows_sorted[:5]:
        name = r.get("sectorName") or r.get("themeName") or r.get("sectorCode")
        amt = r.get("mainNetAmount")
        top.append(f"{name}:{amt}")
    minute = data.get("snapshotMinute") or ""
    head = f"分钟={minute}；条数={data.get('returned') or len(rows)}"
    if top:
        return head + "；主力净额前5：" + "; ".join(top)
    return head


def resolve_sector_path(trade_date: str, explicit: Path | None) -> Path | None:
    if explicit:
        return explicit
    cand = DEFAULT_SECTOR_DIR / f"sector_capital_flow_snapshot__{trade_date}.json"
    return cand if cand.exists() else None


def resolve_p1_path(trade_date: str) -> Path:
    return DEFAULT_P1_DIR / f"p1_day__{trade_date}.md"


def render_md(
    trade_date: str,
    *,
    ladder_fact: str,
    sector_path: str,
    sector_note: str,
    p1_path: str,
    p1_exists: bool,
) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    p1_line = p1_path if p1_exists else f"{p1_path}（尚未生成）"
    return f"""# 工作台日文件（事实预填）__{trade_date}

- 交易日：`{trade_date}`
- 预填时间：`{now}`
- 批次：`batch_01_three_card_shell__20260809`
- 口径：只预填事实格与路径引用；判断格留空

======== 一、盘前方向卡 ========
- 今天偏强 / 偏弱 / 中性：
- 该盯板块：
- 该盯标的：
- 连板天梯昨日/结构（事实）：{ladder_fact}
- sector 快照路径（事实）：{sector_path}
- sector 事实摘要：{sector_note}
- P1 竞价段引用（事实）：{p1_line}
- 直播间方向摘要（可选）：
- 盘前一句话：

======== 二、盘中确认卡 ========
- 早上判断是否被资金确认：
- 仍值得盯：
- 直播间转折解释（可选）：
- 10:00：是 / 否 / 不清楚；一句话：
- 13:30：是 / 否 / 不清楚；一句话：
- 14:30（可选）：是 / 否 / 不清楚；一句话：
- 盘中一句话：

======== 三、盘后复盘卡 ========
- 今天判断对不对：
- 真正有用的信息来自哪里：
- 最没用的是：
- 连板天梯结构结果（事实）：{ladder_fact}
- sector 当日快照路径（事实）：{sector_path}
- P1 日记录路径（事实）：{p1_line}
- 值得沉长期库：
- 竞价期判断增量价值：有 / 无 / 不清楚
- 盘中资金确认增量价值：有 / 无 / 不清楚
- 盘后一句话：

======== 四、引用（不替代独立链）========
- p1_day：{p1_line}
- sector：{sector_path}
"""


def main() -> None:
    ap = argparse.ArgumentParser(description="Prefill workbench day fact fields only")
    ap.add_argument("--trade-date", required=True, help="YYYYMMDD")
    ap.add_argument("--ladder-json", type=Path, default=None)
    ap.add_argument("--sector-json", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = ap.parse_args()

    trade_date = args.trade_date.strip()
    sector_path = resolve_sector_path(trade_date, args.sector_json)
    sector_payload = load_json(sector_path) if sector_path else None
    ladder_payload = load_json(args.ladder_json)

    p1_path = resolve_p1_path(trade_date)
    sector_path_text = (
        str(sector_path)
        if sector_path and sector_path.exists()
        else f"{DEFAULT_SECTOR_DIR / f'sector_capital_flow_snapshot__{trade_date}.json'}（不存在）"
    )

    md = render_md(
        trade_date,
        ladder_fact=ladder_summary(ladder_payload),
        sector_path=sector_path_text,
        sector_note=sector_top_note(sector_payload),
        p1_path=str(p1_path),
        p1_exists=p1_path.exists(),
    )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_md = args.out_dir / f"workbench_day__{trade_date}.md"
    out_md.write_text(md, encoding="utf-8")
    print("wrote", out_md)
    print("sector_path", sector_path_text)
    print("p1_exists", p1_path.exists())


if __name__ == "__main__":
    main()
