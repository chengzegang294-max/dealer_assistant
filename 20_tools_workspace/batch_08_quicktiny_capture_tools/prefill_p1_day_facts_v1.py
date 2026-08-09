# -*- coding: utf-8 -*-
"""Prefill P1 daily record FACT fields from same-day ladder/sector snapshots.

Does NOT fill judgment fields (bias / money still in / enough_or_not).
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(r"d:\Stock\dealer_assistant")
DEFAULT_OUT_DIR = ROOT / r"02_runtime\shortline_funding_gap\batch_01_p1_manual_validation__20260809\daily"
DEFAULT_LOG = ROOT / r"02_runtime\shortline_funding_gap\batch_01_p1_manual_validation__20260809\derived\p1_manual_validation_log__202608.tsv"


def load_json(path: Path | None) -> dict[str, Any] | None:
    if not path:
        return None
    if not path.exists():
        raise FileNotFoundError(path)
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError(f"json root must be object: {path}")
    return obj


def ladder_facts(payload: dict[str, Any] | None) -> dict[str, str]:
    out = {
        "ladder_height_note": "",
        "ladder_structure_note": "",
        "ladder_total_stocks": "",
        "ladder_top_boards": "",
    }
    if not payload:
        return out
    dates = payload.get("dates") or []
    if not dates:
        # maybe min form already trimmed
        return out
    day = dates[0]
    boards = day.get("boards") or []
    levels = []
    for b in boards:
        if isinstance(b, dict) and b.get("level") is not None:
            n = len(b.get("stocks") or [])
            levels.append(f"{b.get('level')}板x{n}")
    out["ladder_total_stocks"] = str(day.get("totalStocks") or "")
    out["ladder_top_boards"] = ";".join(levels[:6])
    out["ladder_height_note"] = (
        f"最高板={boards[0].get('level') if boards else '?'}；总连板池={day.get('totalStocks')}"
        if boards
        else f"总连板池={day.get('totalStocks')}"
    )
    out["ladder_structure_note"] = f"板高分布：{out['ladder_top_boards']}" if levels else ""
    return out


def sector_facts(payload: dict[str, Any] | None) -> dict[str, str]:
    out = {
        "sector_snapshot_archived": "否",
        "sector_top_note": "",
        "sector_snapshot_minute": "",
        "sector_returned": "",
    }
    if not payload:
        return out
    if payload.get("success") is False:
        out["sector_top_note"] = f"snapshot失败 code={payload.get('code')}"
        return out
    data = payload.get("data") or {}
    rows = [r for r in (data.get("rows") or []) if isinstance(r, dict) and not r.get("__truncated__")]
    rows_sorted = sorted(rows, key=lambda r: r.get("mainNetAmount") or 0, reverse=True)
    top = []
    for r in rows_sorted[:5]:
        name = r.get("sectorName") or r.get("themeName") or r.get("sectorCode")
        amt = r.get("mainNetAmount")
        top.append(f"{name}:{amt}")
    out["sector_snapshot_archived"] = "是"
    out["sector_snapshot_minute"] = str(data.get("snapshotMinute") or "")
    out["sector_returned"] = str(data.get("returned") or len(rows))
    out["sector_top_note"] = "主力净额前5：" + "; ".join(top) if top else ""
    return out


def render_md(trade_date: str, lf: dict[str, str], sf: dict[str, str]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""# P1 日记录（事实预填）__{trade_date}

- 交易日：`{trade_date}`
- 预填时间：`{now}`
- 口径：只预填事实格；判断格留空，由人工补

## 一、竞价期判断（9:15 - 9:25）

- 整体判断：偏强 / 偏弱 / 中性
- 竞价异动标的：
- 高标竞价表现：
- 一句话判断：

## 二、盘中资金跟随确认

- 观察时点1（建议 10:00）
  - 看什么：
  - 资金是否仍在：是 / 否 / 不清楚
  - 一句话：
- 观察时点2（建议 13:30）
  - 看什么：
  - 资金是否仍在：是 / 否 / 不清楚
  - 一句话：
- 观察时点3（可选，建议 14:30）
  - 看什么：
  - 资金是否仍在：是 / 否 / 不清楚
  - 一句话：

## 三、直播间补了什么（可选）

- 哪个房 / 哪条口径：
- 有没有非标准情报：

## 四、连板天梯 / 板块资金事实（自动预填）

- 连板结构：{lf.get('ladder_structure_note') or '（无 ladder 输入）'}
- 市场高度：{lf.get('ladder_height_note') or '（无 ladder 输入）'}
- 板块资金当日快照是否已存档：{sf.get('sector_snapshot_archived')}
- 板块快照分钟：{sf.get('sector_snapshot_minute') or '（无）'}
- 板块返回条数：{sf.get('sector_returned') or '（无）'}
- 板块当日观察摘要：{sf.get('sector_top_note') or '（无 sector 输入）'}

## 五、收盘回看

- 今天最有用的是：
- 今天最没用的是：
- 竞价期判断是否有增量价值：有 / 无 / 不清楚
- 盘中资金确认是否有增量价值：有 / 无 / 不清楚

## 六、是否够用

- 结论：够用 / 不够用
- 如果不够用，缺的是什么：
"""


def upsert_log(log_path: Path, trade_date: str, lf: dict[str, str], sf: dict[str, str]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "trade_date",
        "is_trading_day",
        "auction_bias",
        "auction_abnormal_symbols",
        "high_board_auction_note",
        "auction_one_liner",
        "intraday_t1_time",
        "intraday_t1_watch",
        "intraday_t1_money_still_in",
        "intraday_t1_note",
        "intraday_t2_time",
        "intraday_t2_watch",
        "intraday_t2_money_still_in",
        "intraday_t2_note",
        "intraday_t3_time",
        "intraday_t3_watch",
        "intraday_t3_money_still_in",
        "intraday_t3_note",
        "live_room_supplement",
        "ladder_structure_note",
        "ladder_height_note",
        "sector_snapshot_archived",
        "close_most_useful",
        "close_least_useful",
        "auction_has_incremental_value",
        "intraday_has_incremental_value",
        "enough_or_not",
        "what_is_missing",
        "recorder",
        "recorded_at",
    ]
    rows: list[dict[str, str]] = []
    if log_path.exists():
        with log_path.open(encoding="utf-8", newline="") as f:
            rows = [dict(r) for r in csv.DictReader(f, delimiter="\t")]
    rows = [r for r in rows if r.get("trade_date") != trade_date]
    rows.append(
        {
            "trade_date": trade_date,
            "is_trading_day": "是",
            "auction_bias": "",
            "auction_abnormal_symbols": "",
            "high_board_auction_note": "",
            "auction_one_liner": "",
            "intraday_t1_time": "10:00",
            "intraday_t1_watch": "",
            "intraday_t1_money_still_in": "",
            "intraday_t1_note": "",
            "intraday_t2_time": "13:30",
            "intraday_t2_watch": "",
            "intraday_t2_money_still_in": "",
            "intraday_t2_note": "",
            "intraday_t3_time": "14:30",
            "intraday_t3_watch": "",
            "intraday_t3_money_still_in": "",
            "intraday_t3_note": "",
            "live_room_supplement": "",
            "ladder_structure_note": lf.get("ladder_structure_note", ""),
            "ladder_height_note": lf.get("ladder_height_note", ""),
            "sector_snapshot_archived": sf.get("sector_snapshot_archived", ""),
            "close_most_useful": "",
            "close_least_useful": "",
            "auction_has_incremental_value": "",
            "intraday_has_incremental_value": "",
            "enough_or_not": "",
            "what_is_missing": "",
            "recorder": "cursor_prefill",
            "recorded_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    )
    with log_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description="Prefill P1 fact fields for one trade date")
    ap.add_argument("--trade-date", required=True, help="YYYYMMDD")
    ap.add_argument("--ladder-json", type=Path, default=None)
    ap.add_argument("--sector-json", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--log-tsv", type=Path, default=DEFAULT_LOG)
    args = ap.parse_args()

    trade_date = args.trade_date.strip()
    ladder = load_json(args.ladder_json)
    sector = load_json(args.sector_json)
    lf = ladder_facts(ladder)
    sf = sector_facts(sector)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_md = args.out_dir / f"p1_day__{trade_date}.md"
    out_md.write_text(render_md(trade_date, lf, sf), encoding="utf-8")
    upsert_log(args.log_tsv, trade_date, lf, sf)

    print("wrote", out_md)
    print("updated", args.log_tsv)
    print("sector_archived", sf["sector_snapshot_archived"])
    print("ladder_total", lf["ladder_total_stocks"])


if __name__ == "__main__":
    main()
