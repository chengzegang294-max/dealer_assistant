"""
clean_northbound_and_margin_v1.py
作用：东财北向资金 + 两融余额 CSV → 合并1行当日总额
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path


OUT_COLS = ["trade_date","northbound_total_net_yuan","hgt_net_yuan","sgt_net_yuan","margin_total_balance_yuan","margin_daily_change_yuan","margin_daily_change_pct"]


def to_float_s(s):
    if not s: return 0.0
    s = s.strip().replace(",","").replace("亿","").replace("元","").replace("%","")
    try: return float(s)
    except Exception: return 0.0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-root", required=True)
    ap.add_argument("--out-root", required=True)
    ap.add_argument("--trade-date", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)
    raw_root, out_root, td = Path(args.raw_root), Path(args.out_root), args.trade_date
    matches = list(raw_root.glob(f"northbound_margin_raw_{td}.csv")) + list(raw_root.glob("northbound_margin_raw_*.csv"))
    if not matches:
        print("[5_北向+两融] 未找到 northbound_margin_raw_*.csv，SKIP")
        return 0
    src = matches[0]
    print(f"[5_北向+两融] 读原始CSV：{src.name}")
    out = {c: "" for c in OUT_COLS}
    out["trade_date"] = td
    with src.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    def pick(r, *ks):
        for k in ks:
            v = str(r.get(k) or "").strip()
            if v: return v
        return ""
    # 一般东财北向CSV前2行分别是沪股通净买/深股通净买/第3行北向合计；两融余额后面行
    hgt = sgt = total = 0.0
    margin_bal = margin_chg = margin_chg_pct = 0.0
    for r in rows:
        name_or_type = pick(r,"项目","指标","类型","名称","北向/两融项目","item","name")
        if any(k in name_or_type for k in ["沪股通","沪股通净","沪港通净买","HGT"]) and not "合计" in name_or_type:
            hgt = to_float_s(pick(r,"当日净流入","净流入","净额","金额","净买额","数值"))
        elif any(k in name_or_type for k in ["深股通","深港通","SGT"]) and not "合计" in name_or_type:
            sgt = to_float_s(pick(r,"当日净流入","净流入","净额","金额","净买额","数值"))
        elif any(k in name_or_type for k in ["北向合计","北向合计净买","沪深港通合计","北向资金合计"]):
            total = to_float_s(pick(r,"当日净流入","净流入","净额","金额","净买额","数值"))
        elif any(k in name_or_type for k in ["两融余额","融资融券余额","两融总余额"]):
            margin_bal = to_float_s(pick(r,"余额","金额","当日余额","数值"))
        elif any(k in name_or_type for k in ["两融变动","融资融券变动","两融当日变动","两融增减"]):
            if "%変動" in name_or_type or "变动%" in name_or_type or "涨跌幅" in name_or_type:
                margin_chg_pct = to_float_s(pick(r,"变动%","涨跌幅","百分比","数值"))
            else:
                margin_chg = to_float_s(pick(r,"变动额","当日变动","增减额","数值"))
    # 没有合计列：沪+深
    if total == 0.0 and (hgt or sgt): total = hgt + sgt
    out["northbound_total_net_yuan"] = str(total) if total else ""
    out["hgt_net_yuan"] = str(hgt) if hgt else ""
    out["sgt_net_yuan"] = str(sgt) if sgt else ""
    out["margin_total_balance_yuan"] = str(margin_bal) if margin_bal else ""
    out["margin_daily_change_yuan"] = str(margin_chg) if margin_chg else ""
    out["margin_daily_change_pct"] = str(margin_chg_pct) if margin_chg_pct else ""
    out_p = out_root / f"a_share_northbound_margin_{td}.csv"
    if args.apply:
        with out_p.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=OUT_COLS)
            w.writeheader(); w.writerow(out)
        print(f"[5_北向+两融] WROTE {out_p} → 北向合计={total}/沪={hgt}/深={sgt}；两融余额={margin_bal}（变动={margin_chg}）")
    else:
        print(f"[5_北向+两融] DRY_RUN → {out}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
