# -*- coding: utf-8 -*-
"""Archive today's sector-capital-flow snapshot into a dated json + tsv.

Scope:
- Only same-day snapshot accumulation.
- Does NOT fetch historical dates.
- Does NOT discover new endpoints.
- Input is an already-captured raw JSON file path.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from pathlib import Path
from typing import Any

ROW_FIELDS = [
    "sectorCode",
    "sectorName",
    "themeCode",
    "themeName",
    "mainNetAmount",
    "bigOrderNetAmount",
    "strength",
    "pctChg",
    "relativeInflow",
    "floatMarketCap",
    "changeFromOpen",
    "memberCount",
    "mainBuyAmount",
    "mainSellAmount",
    "universe",
]

TSV_COLS = [
    "trade_date",
    "actual_trade_date",
    "universe",
    "snapshot_minute",
    "sector_code",
    "sector_name",
    "theme_code",
    "theme_name",
    "main_net_amount",
    "big_order_net_amount",
    "strength",
    "pct_chg",
    "relative_inflow",
    "float_market_cap",
    "change_from_open",
    "member_count",
    "main_buy_amount",
    "main_sell_amount",
]


def normalize_date(label: str) -> str:
    text = str(label).strip()
    digits = re.sub(r"\D", "", text)
    if len(digits) != 8:
        raise ValueError(f"trade-date must be YYYYMMDD, got: {label}")
    return digits


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_same_day_or_warn(payload: dict[str, Any], trade_date: str) -> list[str]:
    notes: list[str] = []
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, dict):
        notes.append("payload_missing_data")
        return notes
    actual = str(data.get("actualTradeDate") or data.get("tradeDate") or "")
    if actual and actual != trade_date:
        raise ValueError(
            "refusing to archive mismatched day: "
            f"label={trade_date} actualTradeDate/tradeDate={actual}. "
            "This script only archives same-day snapshots."
        )
    if not actual:
        notes.append("actualTradeDate_missing_in_payload")
    return notes


def rows_from_payload(payload: dict[str, Any], trade_date: str) -> list[dict[str, Any]]:
    data = payload.get("data") or {}
    snapshot_minute = data.get("snapshotMinute")
    universe = data.get("universe")
    actual = data.get("actualTradeDate") or data.get("tradeDate") or trade_date
    out: list[dict[str, Any]] = []
    for row in data.get("rows") or []:
        if not isinstance(row, dict) or row.get("__truncated__"):
            continue
        out.append(
            {
                "trade_date": trade_date,
                "actual_trade_date": actual,
                "universe": universe or row.get("universe"),
                "snapshot_minute": snapshot_minute,
                "sector_code": row.get("sectorCode"),
                "sector_name": row.get("sectorName"),
                "theme_code": row.get("themeCode"),
                "theme_name": row.get("themeName"),
                "main_net_amount": row.get("mainNetAmount"),
                "big_order_net_amount": row.get("bigOrderNetAmount"),
                "strength": row.get("strength"),
                "pct_chg": row.get("pctChg"),
                "relative_inflow": row.get("relativeInflow"),
                "float_market_cap": row.get("floatMarketCap"),
                "change_from_open": row.get("changeFromOpen"),
                "member_count": row.get("memberCount"),
                "main_buy_amount": row.get("mainBuyAmount"),
                "main_sell_amount": row.get("mainSellAmount"),
            }
        )
    return out


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=TSV_COLS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in TSV_COLS})


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Archive same-day sector snapshot json into dated json+tsv (no historical fetch)."
    )
    ap.add_argument("--input-json", required=True, type=Path, help="Already captured raw JSON path")
    ap.add_argument("--output-dir", required=True, type=Path, help="Archive output directory")
    ap.add_argument("--trade-date", required=True, help="YYYYMMDD same-day label")
    ap.add_argument(
        "--copy-mode",
        choices=["copy", "rewrite"],
        default="copy",
        help="copy=keep raw bytes via copy2; rewrite=pretty dump",
    )
    args = ap.parse_args()

    trade_date = normalize_date(args.trade_date)
    if not args.input_json.exists():
        raise FileNotFoundError(args.input_json)

    payload = load_json(args.input_json)
    if not isinstance(payload, dict):
        raise ValueError("input json must be an object")
    if payload.get("success") is False:
        raise ValueError(
            f"input marks success=false code={payload.get('code')}; refuse to archive"
        )

    notes = assert_same_day_or_warn(payload, trade_date)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    out_json = args.output_dir / f"sector_capital_flow_snapshot__{trade_date}.json"
    out_tsv = args.output_dir / f"sector_capital_flow_snapshot__{trade_date}.tsv"
    out_meta = args.output_dir / f"sector_capital_flow_snapshot__{trade_date}.meta.json"

    if args.copy_mode == "copy":
        shutil.copy2(args.input_json, out_json)
    else:
        out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    rows = rows_from_payload(payload, trade_date)
    write_tsv(out_tsv, rows)

    data = payload.get("data") or {}
    meta = {
        "trade_date": trade_date,
        "input_json": str(args.input_json),
        "output_json": str(out_json),
        "output_tsv": str(out_tsv),
        "row_count": len(rows),
        "success": payload.get("success"),
        "actual_trade_date": data.get("actualTradeDate"),
        "snapshot_minute": data.get("snapshotMinute"),
        "universe": data.get("universe"),
        "returned": data.get("returned"),
        "notes": notes,
        "scope": "same_day_archive_only_no_historical_fetch",
    }
    out_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print("wrote", out_json)
    print("wrote", out_tsv)
    print("wrote", out_meta)
    print("rows", len(rows))


if __name__ == "__main__":
    main()
