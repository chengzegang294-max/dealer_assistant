# -*- coding: utf-8 -*-
"""Extract minimal single-day sample from ladder/day + sector snapshot
using batch_04 min field contract. Does not discover new endpoints.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(r"d:\Stock\dealer_assistant")
DEFAULT_CONTRACT = ROOT / r"02_runtime\quicktiny_capture\batch_04_min_contract__20260808\min_field_contract__20260808.json"
DEFAULT_LADDER_SLIM = ROOT / r"02_runtime\quicktiny_capture\batch_03_field_dict__20260808\ladder_day__raw_slim__20260807.json"
DEFAULT_SECTOR_SLIM = ROOT / r"02_runtime\quicktiny_capture\batch_03_field_dict__20260808\sector_capital_flow_snapshot__raw_slim__20260807.json"
LS_DIR = Path(
    r"C:\Users\91883\AppData\Local\cn.quicktiny.sectorcapital\EBWebView\Default\Local Storage\leveldb"
)

LADDER_STOCK_KEEP_LEVELS = {"required", "recommended"}
SECTOR_ROW_KEEP_LEVELS = {"required", "recommended"}
HEADER_KEEP_LEVELS = {"required", "recommended", "optional"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_token() -> str:
    jwt_re = re.compile(rb"eyJ[A-Za-z0-9_\-]+=*(?:\.[A-Za-z0-9_\-]+=*){2}")
    candidates: list[bytes] = []
    for p in LS_DIR.iterdir():
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".ldb", ".log"} and not p.name.endswith(".log"):
            continue
        try:
            data = p.read_bytes()
        except Exception:
            continue
        candidates.extend(jwt_re.findall(data))
    if not candidates:
        raise RuntimeError("No JWT found in WebView Local Storage")
    return max(candidates, key=len).decode("ascii", "ignore").strip().rstrip("\x00")


def fetch_json(url: str, token: str, allow_error: bool = False) -> tuple[int, Any]:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 trading_assistant_min_sample/1.0",
            "Cookie": f"token={token}",
            "Authorization": f"Bearer {token}",
            "Referer": "https://stock.quicktiny.cn/",
            "Origin": "https://stock.quicktiny.cn",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            raw = resp.read()
            status = resp.status
    except urllib.error.HTTPError as e:
        raw = e.read()
        status = e.code
    try:
        body = json.loads(raw.decode("utf-8", "replace"))
    except Exception:
        body = {"_parse_error": True, "_raw_preview": raw[:2000].decode("utf-8", "replace")}
    if status != 200 and not allow_error:
        raise RuntimeError(f"HTTP {status} for {url}")
    return status, body


def is_truncated(obj: Any) -> bool:
    if isinstance(obj, dict) and obj.get("__truncated__"):
        return True
    if isinstance(obj, list):
        return any(isinstance(x, dict) and x.get("__truncated__") for x in obj)
    if isinstance(obj, dict):
        return any(is_truncated(v) for v in obj.values())
    return False


def pick_fields(src: dict[str, Any], field_specs: list[dict[str, str]], levels: set[str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for spec in field_specs:
        if spec["level"] not in levels:
            continue
        key = spec["path"]
        if key in src:
            out[key] = src[key]
    return out


def trim_ladder(raw: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    day_specs = contract["ladder_day"]["day_fields"]
    stock_specs = contract["ladder_day"]["stock_fields"]
    stock_keep = [s for s in stock_specs if s["level"] in LADDER_STOCK_KEEP_LEVELS]

    out: dict[str, Any] = {}
    if "dateRange" in raw:
        # keep if recommended/optional allowed
        for s in day_specs:
            if s["path"] == "dateRange" and s["level"] in HEADER_KEEP_LEVELS:
                out["dateRange"] = raw.get("dateRange")
                break

    meta_src = raw.get("meta") or {}
    meta_out: dict[str, Any] = {}
    for s in day_specs:
        path = s["path"]
        if not path.startswith("meta.") or s["level"] not in HEADER_KEEP_LEVELS:
            continue
        key = path.split(".", 1)[1]
        if key in meta_src:
            meta_out[key] = meta_src[key]
    if meta_out:
        out["meta"] = meta_out

    dates_out = []
    for day in raw.get("dates") or []:
        if isinstance(day, dict) and day.get("__truncated__"):
            continue
        day_out: dict[str, Any] = {}
        for key in ("date", "dayOfWeek", "totalStocks", "pauseRatio"):
            if key in day:
                day_out[key] = day[key]
        boards_out = []
        for board in day.get("boards") or []:
            if isinstance(board, dict) and board.get("__truncated__"):
                continue
            board_out: dict[str, Any] = {"level": board.get("level"), "stocks": []}
            for stock in board.get("stocks") or []:
                if isinstance(stock, dict) and stock.get("__truncated__"):
                    continue
                board_out["stocks"].append(pick_fields(stock, stock_keep, LADDER_STOCK_KEEP_LEVELS))
            boards_out.append(board_out)
        day_out["boards"] = boards_out
        dates_out.append(day_out)
    out["dates"] = dates_out
    return out


def trim_sector(raw: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    header_specs = contract["sector_capital_flow_snapshot"]["header_fields"]
    row_specs = contract["sector_capital_flow_snapshot"]["row_fields"]

    out: dict[str, Any] = {}
    if "success" in raw:
        out["success"] = raw["success"]

    data_src = raw.get("data") or {}
    data_out: dict[str, Any] = {}
    for s in header_specs:
        path = s["path"]
        if not path.startswith("data.") or s["level"] not in {"required", "recommended"}:
            continue
        key = path.split(".", 1)[1]
        if key in {"rows", "quality", "fieldDefinitions"}:
            continue
        if key in data_src:
            data_out[key] = data_src[key]

    rows_out = []
    for row in data_src.get("rows") or []:
        if isinstance(row, dict) and row.get("__truncated__"):
            continue
        rows_out.append(pick_fields(row, row_specs, SECTOR_ROW_KEEP_LEVELS))
    data_out["rows"] = rows_out
    out["data"] = data_out
    return out


def list_join(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, list):
        return "|".join(str(x) for x in v)
    return str(v)


def ladder_rows(min_obj: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for day in min_obj.get("dates") or []:
        trade_date = day.get("date")
        for board in day.get("boards") or []:
            board_level = board.get("level")
            for stock in board.get("stocks") or []:
                rows.append(
                    {
                        "trade_date": trade_date,
                        "board_level": board_level,
                        "code": stock.get("code"),
                        "name": stock.get("name"),
                        "level": stock.get("level", board_level),
                        "continue_num": stock.get("continue_num"),
                        "change_rate": stock.get("change_rate"),
                        "latest": stock.get("latest"),
                        "first_limit_up_time": stock.get("first_limit_up_time"),
                        "last_limit_up_time": stock.get("last_limit_up_time"),
                        "primary_theme": stock.get("primary_theme"),
                        "limit_up_type": stock.get("limit_up_type"),
                        "high_days": stock.get("high_days"),
                        "open_num": stock.get("open_num"),
                        "trading_amount": stock.get("trading_amount"),
                        "order_amount": stock.get("order_amount"),
                        "amount": stock.get("amount"),
                        "turnover_rate": stock.get("turnover_rate"),
                        "industry": stock.get("industry"),
                        "kpl_primary_theme": stock.get("kpl_primary_theme"),
                        "kpl_theme_tags": list_join(stock.get("kpl_theme_tags")),
                        "kpl_plate_code": stock.get("kpl_plate_code"),
                        "reason_type": stock.get("reason_type"),
                        "tags": list_join(stock.get("tags")),
                        "auto_position": stock.get("auto_position"),
                        "change_tag": stock.get("change_tag"),
                        "market_type": stock.get("market_type"),
                        "currency_value": stock.get("currency_value"),
                        "actual_currency_value": stock.get("actual_currency_value"),
                    }
                )
    return rows


def sector_rows(min_obj: dict[str, Any]) -> list[dict[str, Any]]:
    data = min_obj.get("data") or {}
    rows = []
    for row in data.get("rows") or []:
        rows.append(
            {
                "trade_date": data.get("tradeDate"),
                "actual_trade_date": data.get("actualTradeDate"),
                "universe": data.get("universe") or row.get("universe"),
                "snapshot_minute": data.get("snapshotMinute"),
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
    return rows


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in fields})


def missing_required_stock(stock: dict[str, Any], required_keys: list[str]) -> list[str]:
    miss = []
    for k in required_keys:
        if k not in stock or stock[k] is None or stock[k] == "":
            miss.append(k)
    return miss


def accept(
    date: str,
    ladder_min: dict[str, Any],
    sector_min: dict[str, Any],
    ladder_src: str,
    sector_src: str,
    contract: dict[str, Any],
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    dates = ladder_min.get("dates") or []
    day0 = dates[0] if dates else {}
    boards = day0.get("boards") or []
    stock_rows = ladder_rows(ladder_min)
    sector_data = sector_min.get("data") or {}
    s_rows = sector_rows(sector_min)

    req_stock = [
        s["path"]
        for s in contract["ladder_day"]["stock_fields"]
        if s["level"] == "required"
    ]
    stocks_missing = 0
    for st in stock_rows:
        # map tsv keys back roughly
        mapped = {
            "code": st.get("code"),
            "name": st.get("name"),
            "level": st.get("level"),
            "continue_num": st.get("continue_num"),
            "change_rate": st.get("change_rate"),
            "latest": st.get("latest"),
            "first_limit_up_time": st.get("first_limit_up_time"),
            "last_limit_up_time": st.get("last_limit_up_time"),
            "primary_theme": st.get("primary_theme"),
            "limit_up_type": st.get("limit_up_type"),
        }
        if missing_required_stock(mapped, req_stock):
            stocks_missing += 1

    # plate join hint
    ladder_plates = {str(r.get("kpl_plate_code") or "") for r in stock_rows if r.get("kpl_plate_code")}
    sector_plates = {str(r.get("sector_code") or "").rstrip("k") for r in s_rows if r.get("sector_code")}
    ladder_norm = {p.rstrip("k") for p in ladder_plates if p}
    overlap = ladder_norm & sector_plates
    join_ratio = (len(overlap) / len(ladder_norm)) if ladder_norm else 0.0

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("ladder_dates_non_empty", bool(dates), f"dates_len={len(dates)}")
    add("ladder_date_match", day0.get("date") == date, f"got={day0.get('date')}")
    add("ladder_boards_non_empty", bool(boards), f"boards_len={len(boards)}")
    add("ladder_stocks_non_empty", bool(stock_rows), f"stock_rows={len(stock_rows)}")
    add(
        "ladder_totalStocks_vs_rows",
        day0.get("totalStocks") == len(stock_rows),
        f"totalStocks={day0.get('totalStocks')} rows={len(stock_rows)}",
    )
    add(
        "ladder_required_fields",
        stocks_missing == 0,
        f"stocks_with_required_missing={stocks_missing}",
    )
    add("sector_success", sector_min.get("success") is True, f"success={sector_min.get('success')}")
    add(
        "sector_actualTradeDate_match",
        sector_data.get("actualTradeDate") == date,
        f"got={sector_data.get('actualTradeDate')}",
    )
    add("sector_rows_non_empty", bool(s_rows), f"rows={len(s_rows)}")
    add(
        "sector_returned_vs_rows",
        sector_data.get("returned") == len(s_rows),
        f"returned={sector_data.get('returned')} rows={len(s_rows)}",
    )
    add(
        "no_third_endpoint",
        True,
        "only ladder/day + sector-capital-flow/snapshot",
    )

    passed = all(c["ok"] for c in checks)
    return {
        "date": date,
        "passed": passed,
        "ladder_source": ladder_src,
        "sector_source": sector_src,
        "ladder_totalStocks": day0.get("totalStocks"),
        "ladder_stock_rows": len(stock_rows),
        "sector_returned": sector_data.get("returned"),
        "sector_row_rows": len(s_rows),
        "plate_join_overlap_count": len(overlap),
        "plate_join_ratio_vs_ladder_plates": round(join_ratio, 4),
        "checks": checks,
    }


def render_acceptance_md(acc: dict[str, Any], out_files: dict[str, str]) -> str:
    lines = [
        f"# sample_acceptance__{acc['date']}",
        "",
        f"- date: `{acc['date']}`",
        f"- passed: `{acc['passed']}`",
        f"- ladder_source: `{acc['ladder_source']}`",
        f"- sector_source: `{acc['sector_source']}`",
        f"- ladder_totalStocks / rows: `{acc['ladder_totalStocks']}` / `{acc['ladder_stock_rows']}`",
        f"- sector_returned / rows: `{acc['sector_returned']}` / `{acc['sector_row_rows']}`",
        f"- plate_join_overlap: `{acc['plate_join_overlap_count']}` (ratio=`{acc['plate_join_ratio_vs_ladder_plates']}`)",
    ]
    if acc.get("special_case"):
        lines.append(f"- special_case: `{acc['special_case']}`")
    if acc.get("special_notes"):
        lines.append(f"- special_notes: `{acc['special_notes']}`")
    lines.extend(["", "## checks", ""])
    for c in acc["checks"]:
        mark = "PASS" if c["ok"] else "FAIL"
        lines.append(f"- [{mark}] `{c['name']}` — {c['detail']}")
    lines.extend(["", "## outputs", ""])
    for k, v in out_files.items():
        p = Path(v)
        lines.append(f"- {k}: [{p.name}](file:///{p.as_posix()})")
    lines.extend(
        [
            "",
            "## 一句话",
            "",
            "- 本样本只裁 `ladder/day` 与 `sector-capital-flow/snapshot`，按最小字段合同输出 min json/tsv 并验收。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract min day sample by field contract")
    ap.add_argument("--date", default="20260807")
    ap.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    ap.add_argument("--ladder-json", type=Path, default=DEFAULT_LADDER_SLIM)
    ap.add_argument("--sector-json", type=Path, default=DEFAULT_SECTOR_SLIM)
    ap.add_argument(
        "--out-root",
        type=Path,
        default=None,
        help="Default: 02_runtime/quicktiny_capture/batch_05_min_day_sample__{date}",
    )
    ap.add_argument(
        "--prefer-full-refetch-if-truncated",
        action="store_true",
        default=True,
        help="If input slim is truncated, refetch same endpoints once (default on)",
    )
    ap.add_argument("--no-refetch", action="store_true", help="Never refetch; use local json only")
    ap.add_argument(
        "--force-refetch",
        action="store_true",
        help="Always refetch both endpoints for --date (ignore local completeness)",
    )
    ap.add_argument(
        "--allow-partial-module-errors",
        action="store_true",
        help="If one module HTTP fails, still write outputs and failing acceptance",
    )
    args = ap.parse_args()

    date = args.date
    out_root = args.out_root or (
        ROOT / f"02_runtime/quicktiny_capture/batch_05_min_day_sample__{date}"
    )
    raw_dir = out_root / "00_raw"
    derived = out_root / "derived"
    raw_dir.mkdir(parents=True, exist_ok=True)
    derived.mkdir(parents=True, exist_ok=True)

    contract = load_json(args.contract)
    ladder_raw = load_json(args.ladder_json)
    sector_raw = load_json(args.sector_json)
    ladder_src = str(args.ladder_json)
    sector_src = str(args.sector_json)
    fetch_notes: list[str] = []

    need_refetch = args.force_refetch or (
        (is_truncated(ladder_raw) or is_truncated(sector_raw)) and not args.no_refetch
    )
    if need_refetch and (args.force_refetch or args.prefer_full_refetch_if_truncated):
        token = extract_token()
        ladder_url = f"https://stock.quicktiny.cn/api/ladder/day/{date}"
        sector_url = (
            "https://stock.quicktiny.cn/api/sector-capital-flow/snapshot"
            f"?tradeDate={date}&universe=featured&order=desc&limit=500"
        )
        ladder_status, ladder_raw = fetch_json(
            ladder_url, token, allow_error=args.allow_partial_module_errors
        )
        sector_status, sector_raw = fetch_json(
            sector_url, token, allow_error=args.allow_partial_module_errors
        )
        ladder_src = f"refetch:{ladder_url}"
        sector_src = f"refetch:{sector_url}"
        if ladder_status != 200:
            fetch_notes.append(f"ladder_http={ladder_status}")
        if sector_status != 200:
            code = sector_raw.get("code") if isinstance(sector_raw, dict) else None
            fetch_notes.append(f"sector_http={sector_status} code={code}")

    # always persist raw used for this sample
    ladder_raw_path = raw_dir / f"ladder_day__{date}.json"
    sector_raw_path = raw_dir / f"sector_capital_flow_snapshot__{date}.json"
    ladder_raw_path.write_text(json.dumps(ladder_raw, ensure_ascii=False, indent=2), encoding="utf-8")
    sector_raw_path.write_text(json.dumps(sector_raw, ensure_ascii=False, indent=2), encoding="utf-8")

    ladder_min = trim_ladder(ladder_raw, contract)
    sector_min = trim_sector(sector_raw, contract)

    ladder_min_json = derived / f"ladder_day_min__{date}.json"
    sector_min_json = derived / f"sector_capital_flow_min__{date}.json"
    ladder_min_tsv = derived / f"ladder_day_min__{date}.tsv"
    sector_min_tsv = derived / f"sector_capital_flow_min__{date}.tsv"
    acceptance_md = derived / f"sample_acceptance__{date}.md"
    acceptance_json = derived / f"sample_acceptance__{date}.json"

    ladder_min_json.write_text(json.dumps(ladder_min, ensure_ascii=False, indent=2), encoding="utf-8")
    sector_min_json.write_text(json.dumps(sector_min, ensure_ascii=False, indent=2), encoding="utf-8")
    write_tsv(ladder_min_tsv, ladder_rows(ladder_min))
    write_tsv(sector_min_tsv, sector_rows(sector_min))

    out_files = {
        "ladder_raw": str(ladder_raw_path),
        "sector_raw": str(sector_raw_path),
        "ladder_min_json": str(ladder_min_json),
        "ladder_min_tsv": str(ladder_min_tsv),
        "sector_min_json": str(sector_min_json),
        "sector_min_tsv": str(sector_min_tsv),
        "sample_acceptance_md": str(acceptance_md),
        "sample_acceptance_json": str(acceptance_json),
    }
    acc = accept(date, ladder_min, sector_min, ladder_src, sector_src, contract)
    if fetch_notes:
        acc["special_notes"] = fetch_notes
        # free-tier historical sector deny is an expected smoke special-case
        if any("SECTOR_CAPITAL_DATE_ACCESS_DENIED" in n for n in fetch_notes):
            acc["special_case"] = (
                "sector free tier maxTradingDays=1; historical tradeDate denied"
            )
    acceptance_json.write_text(json.dumps(acc, ensure_ascii=False, indent=2), encoding="utf-8")
    acceptance_md.write_text(render_acceptance_md(acc, out_files), encoding="utf-8")

    print("out_root", out_root)
    print("passed", acc["passed"])
    print("ladder_rows", acc["ladder_stock_rows"], "sector_rows", acc["sector_row_rows"])
    print("acceptance", acceptance_md)


if __name__ == "__main__":
    main()
