"""
calc_limit_up_stats_and_pass_rate_v1.py
作用：东财连板天梯导出CSV → 统计涨停/跌停/炸板/晋级率（和之前连板字段合同对齐）
"""
from __future__ import annotations
import argparse
import csv
from collections import Counter
from pathlib import Path


def to_int(s: str) -> int | None:
    if not s: return None
    s = s.strip().replace("+","").replace("%","")
    try: return int(float(s))
    except Exception: return None


def to_float(s: str) -> float | None:
    if not s: return None
    s = s.strip().replace("%","")
    try: return float(s)
    except Exception: return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-root", required=True)
    ap.add_argument("--out-root", required=True)
    ap.add_argument("--trade-date", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)
    raw_root, out_root, td = Path(args.raw_root), Path(args.out_root), args.trade_date
    matches = list(raw_root.glob(f"limit_up_ladder_raw_{td}.csv")) + list(raw_root.glob("limit_up_ladder_raw_*.csv"))
    if not matches:
        print("[3_涨跌停] 未找到 limit_up_ladder_raw_*.csv，SKIP")
        return 0
    src = matches[0]
    print(f"[3_涨跌停] 读原始CSV：{src.name}")
    # 先把首板/2板/3板/4板/N板 分组统计
    new_1board, new_2board, new_3board, new_4plus = 0, 0, 0, 0
    limit_up_total = 0
    limit_down_total = 0
    blow_open = 0  # 炸板
    sector_counter: Counter[str] = Counter()
    max_consec = 0
    # 计数用
    def pick(r, *ks):
        for k in ks:
            v = str(r.get(k) or "").strip()
            if v: return v
        return ""
    with src.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    # 先看列名：东财导出一般「连板天数 1=首板 2=二板…
    for r in rows:
        # 分类判断（字段合同跟你之前连板保持一致）
        code = pick(r, "代码","股票代码","code")
        sec = pick(r, "板块","所属板块","所属行业","概念","概念题材","sector")
        if sec:
            sector_counter[sec] += 1
        cd = to_int(pick(r,"连板","连板数","连板天数","board","连板高度","consecutive_limit_up_days"))
        name_status = pick(r, "状态","涨停状态","状态标签","status")
        # 涨停/跌停
        if "跌停" in name_status:
            limit_down_total += 1; continue
        if "炸板" in name_status or "开板" in name_status:
            blow_open += 1; cd = cd or 1
        if cd and cd>0:
            limit_up_total += 1
            max_consec = max(max_consec, cd)
            if cd == 1: new_1board += 1
            elif cd == 2: new_2board += 1
            elif cd == 3: new_3board += 1
            else: new_4plus += 1
    total_limit_like = max(limit_up_total + blow_open, 1)
    # 晋级率分母：上一板数量（这里先用历史对比近似，后面填充每日历史）
    pass_1_2 = (new_2board / max(new_1board + new_2board, 1)) * 100.0
    pass_2_3 = (new_3board / max(new_2board + new_3board, 1)) * 100.0
    pass_3_plus = (new_4plus / max(new_3board + new_4plus, 1)) * 100.0
    blow_rate = (blow_open / total_limit_like) * 100.0
    sector_top5 = sector_counter.most_common(5)
    out_row = {
        "trade_date": td,
        "limit_up_count_new": str(new_1board),
        "limit_up_count_total": str(limit_up_total),
        "limit_down_count": str(limit_down_total),
        "open_limit_up_blow_count": str(blow_open),
        "blow_rate_pct": f"{blow_rate:.2f}",
        "board_pass_rate_1to2_pct": f"{pass_1_2:.2f}",
        "board_pass_rate_2to3_pct": f"{pass_2_3:.2f}",
        "board_pass_rate_3plus_pct": f"{pass_3_plus:.2f}",
        "max_consecutive_days": str(max_consec),
        "sector_distribution_top5": " ; ".join(f"{s}:{n}" for s,n in sector_top5) if sector_top5 else "",
    }
    out_p = out_root / f"a_share_daily_limit_up_stats_{td}.csv"
    if args.apply:
        with out_p.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(out_row.keys()))
            w.writeheader(); w.writerow(out_row)
        print(f"[3_涨跌停] WROTE {out_p} → 涨停{limit_up_total}家/炸板{blow_open}家/跌停{limit_down_total}家/晋级率1进2={pass_1_2:.1f}%/板块TOP5={sector_top5}")
    else:
        print(f"[3_涨跌停] DRY_RUN → {out_row}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
