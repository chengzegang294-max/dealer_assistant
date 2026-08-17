"""
run_a_tech_daily_v1.py
作用（汇总脚本= /a-tech-daily 命令的执行体）：
  按顺序跑 1~6 件脚本，对应6件标准化输出；缺原始CSV的件跳过，不报错，不杀其它件。
用法：
  python run_a_tech_daily_v1.py --raw-root 02_runtime/a_share_daily_tech_indicators/00_raw_eastmoney_pc \
    --out-root 02_runtime/a_share_daily_tech_indicators \
    --trade-date 20260813 \
    --apply
"""
from __future__ import annotations
import argparse
import csv
import datetime as dt
from pathlib import Path

from calc_daily_bar_pool_with_indicators_v1 import main as run_1
from calc_sector_fund_flow_clean_v1 import main as run_2
from calc_limit_up_stats_and_pass_rate_v1 import main as run_3
from clean_dragon_tiger_list_v1 import main as run_4
from clean_northbound_and_margin_v1 import main as run_5
from calc_index_daily_indicators_v1 import main as run_6


TASKS = [
    ("1_代码池日线+技术指标", "bar_pool_raw_*.csv", run_1),
    ("2_板块资金流清洗", "sector_fund_flow_raw_*.csv", run_2),
    ("3_涨跌停连板晋级率统计", "limit_up_ladder_raw_*.csv", run_3),
    ("4_龙虎榜TOP50", "dragon_tiger_raw_*.csv", run_4),
    ("5_北向+两融", "northbound_margin_raw_*.csv", run_5),
    ("6_指数日线+技术指标", "index_bar_raw_*.csv", run_6),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-root", required=True)
    ap.add_argument("--out-root", required=True)
    ap.add_argument("--trade-date", required=True, help="YYYYMMDD")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    raw_root = Path(args.raw_root).resolve()
    out_root = Path(args.out_root).resolve()
    td = args.trade_date
    print(f"=== /a-tech-daily 汇总执行 交易日={td} apply={args.apply} ===")
    print(f"原始CSV根：{raw_root}")
    print(f"输出根：{out_root}")
    raw_root.mkdir(parents=True, exist_ok=True)
    out_root.mkdir(parents=True, exist_ok=True)
    runs_done = 0
    for name, glob_pat, fn in TASKS:
        matches = list(raw_root.glob(glob_pat))
        if not matches:
            print(f"SKIP  [{name:<22}] → 00_raw 下没有找到 {glob_pat}，跳过（缺原始CSV，不影响其它件）")
            continue
        print(f"RUN   [{name:<22}] → 命中 {len(matches)} 份原始CSV → 执行脚本")
        try:
            rc = fn(raw_root=raw_root, out_root=out_root, trade_date=td, apply=args.apply)
        except TypeError:
            rc = fn([
                "--raw-root", str(raw_root),
                "--out-root", str(out_root),
                "--trade-date", td,
            ] + (["--apply"] if args.apply else []))
        runs_done += 1
        print(f"OK    [{name:<22}] → 返回码 rc={rc}")
    print(f"--- 汇总执行完成：{runs_done}/{len(TASKS)} 件跑完；{len(TASKS)-runs_done} 件缺原始CSV跳过 ---")
    if not args.apply:
        print("(DRY_RUN：加 --apply 才写输出 CSV，现在只打印执行)")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
