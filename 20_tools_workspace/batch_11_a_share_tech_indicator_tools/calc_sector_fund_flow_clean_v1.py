"""
calc_sector_fund_flow_clean_v1.py
作用：东财行业+概念板块资金流CSV → 清洗出行业/概念TOP20主力净流入+领涨股匹配
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path


OUT_COLS = ["sector_type","sector_name","change_pct","main_net_inflow_yuan","main_net_inflow_pct","lead_stock_code_6d","lead_stock_name","lead_stock_change_pct"]


def clean_code(v: str) -> str:
    if not v: return ""
    v = v.strip()
    digits = "".join(ch for ch in v if ch.isdigit())
    return digits[-6:] if len(digits) >= 6 else ""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-root", required=True)
    ap.add_argument("--out-root", required=True)
    ap.add_argument("--trade-date", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)
    raw_root, out_root, td = Path(args.raw_root), Path(args.out_root), args.trade_date
    matches = list(raw_root.glob(f"sector_fund_flow_raw_{td}.csv")) + list(raw_root.glob("sector_fund_flow_raw_*.csv"))
    if not matches:
        print("[2_板块] 未找到 sector_fund_flow_raw_*.csv，SKIP")
        return 0
    src = matches[0]
    print(f"[2_板块] 读原始CSV：{src.name}")
    rows_out = []
    with src.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            pick = lambda *ks, default="": next((str(r.get(k) or "").strip() for k in ks if (r.get(k) or "").strip() != ""), default)
            # 行业/概念判断：东财原始CSV一般有分类列，或者从名字推断（后面可以细调）
            stype_raw = pick("分类","板块类型","板块","sector_type","类型", default="概念")
            if "行业" in stype_raw or "一级" in stype_raw: stype = "行业"
            elif "概念" in stype_raw or "题材" in stype_raw: stype = "概念"
            else: stype = stype_raw or "概念"
            name = pick("名称","板块名称","板块","行业","sector","sector_name","板块名")
            if not name: continue
            row = {c:"" for c in OUT_COLS}
            row["sector_type"] = stype
            row["sector_name"] = name
            row["change_pct"] = pick("涨跌幅","涨跌幅%","change_pct","领涨股涨跌幅")
            row["main_net_inflow_yuan"] = pick("主力净流入","主力净流入金额","净流入","净流入(元)","主力净额","main_net_inflow","main_net_inflow_yuan","net_inflow")
            row["main_net_inflow_pct"] = pick("主力净占比","主力净流入占比","净流入占比","net_inflow_pct")
            row["lead_stock_code_6d"] = clean_code(pick("领涨股代码","领涨股","龙头代码","龙头股代码","股票代码"))
            row["lead_stock_name"] = pick("领涨股名称","龙头股","领涨股简称","龙头名称","股票简称","股票名称")
            row["lead_stock_change_pct"] = pick("领涨股涨跌幅","龙头涨幅","领涨涨幅")
            rows_out.append(row)
    out_p = out_root / f"a_share_sector_fund_flow_{td}.csv"
    if args.apply and rows_out:
        with out_p.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=OUT_COLS, extrasaction="ignore")
            w.writeheader()
            for r in rows_out: w.writerow(r)
        print(f"[2_板块] WROTE {out_p} → {len(rows_out)} 行（行业/概念清洗合并）")
    else:
        print(f"[2_板块] DRY_RUN/空：匹配 {len(rows_out)} 行；加--apply写输出")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
