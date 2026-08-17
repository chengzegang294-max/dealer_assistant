"""
clean_dragon_tiger_list_v1.py
作用：东财龙虎榜CSV → 分类机构/北向/游资营业部 净买TOP50
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path


OUT_COLS = ["rank","seat_type","seat_name","net_buy_yuan","buy_yuan","sell_yuan","stock_code_6d","stock_name","change_pct","daily_turnover_pct"]


def clean_code(v: str) -> str:
    if not v: return ""
    v = v.strip()
    digits = "".join(ch for ch in v if ch.isdigit())
    return digits[-6:] if len(digits) >= 6 else ""


def seat_type_from_name(name: str) -> str:
    if not name: return "游资营业部"
    n = name.strip()
    if "机构" in n or "机构专用" in n: return "机构"
    if "北向" in n or "香港" in n or "深股通" in n or "沪股通" in n or "沪深股通" in n: return "北向"
    return "游资营业部"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-root", required=True)
    ap.add_argument("--out-root", required=True)
    ap.add_argument("--trade-date", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)
    raw_root, out_root, td = Path(args.raw_root), Path(args.out_root), args.trade_date
    matches = list(raw_root.glob(f"dragon_tiger_raw_{td}.csv")) + list(raw_root.glob("dragon_tiger_raw_*.csv"))
    if not matches:
        print("[4_龙虎榜] 未找到 dragon_tiger_raw_*.csv，SKIP")
        return 0
    src = matches[0]
    print(f"[4_龙虎榜] 读原始CSV：{src.name}")
    rows_out = []
    with src.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for idx, r in enumerate(reader, start=1):
            pick = lambda *ks, default="": next((str(r.get(k) or "").strip() for k in ks if (r.get(k) or "").strip() != ""), default)
            seat = pick("营业部","席位","营业部名称","席位名称","买方营业部","卖方营业部","seat_name","seat","名称")
            code = clean_code(pick("代码","股票代码","code"))
            name = pick("名称","股票简称","股票名称","name","stock_name")
            if not (seat or code or name):
                continue
            row = {c:"" for c in OUT_COLS}
            row["rank"] = str(idx)
            row["seat_type"] = seat_type_from_name(seat)
            row["seat_name"] = seat
            row["net_buy_yuan"] = pick("净买入","净买入额","净额","净买","net_buy","净买入金额")
            row["buy_yuan"] = pick("买入额","买入金额","买入","buy","买")
            row["sell_yuan"] = pick("卖出额","卖出金额","卖出","sell","卖")
            row["stock_code_6d"] = code
            row["stock_name"] = name
            row["change_pct"] = pick("涨跌幅","当日涨跌幅","change_pct","pct_chg")
            row["daily_turnover_pct"] = pick("换手率","换手率%","换手","turnover","daily_turnover_pct")
            rows_out.append(row)
    rows_out.sort(key=lambda r: float(r["net_buy_yuan"] or "0").real if (r["net_buy_yuan"] or "").replace("-","").replace(".","").isdigit() else 0.0, reverse=True)
    rows_out = rows_out[:50]
    for i, r in enumerate(rows_out, 1): r["rank"] = str(i)
    out_p = out_root / f"a_share_dragon_tiger_top50_{td}.csv"
    if args.apply and rows_out:
        with out_p.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=OUT_COLS, extrasaction="ignore")
            w.writeheader()
            for r in rows_out: w.writerow(r)
        print(f"[4_龙虎榜] WROTE {out_p} → TOP{len(rows_out)} 行（机构/北向/游资 自动分类）")
    else:
        print(f"[4_龙虎榜] DRY_RUN/空：匹配 {len(rows_out)} 行；加--apply写输出")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
