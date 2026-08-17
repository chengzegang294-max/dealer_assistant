from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from calc_ladder_metrics_batch_v1 import (
    DRY_RUN_LADDER,
    DRY_RUN_SECTOR,
    TSV_HEADER,
    calc_day,
)

T1_MULS = [0.85, 0.925, 1.0, 1.075, 1.15]
PURITY_THRS = [0.50, 0.55, 0.60, 0.65]
SEC5_BILLION = 100.0

OUT_TSV = Path(__file__).parent / "sensitivity_20combos__20260811.tsv"

PARAM_COLS = ["t1_mul", "purity_thr", "sec5_billion"]


def main() -> None:
    combos: list[tuple[float, float]] = []
    for t1 in T1_MULS:
        for pt in PURITY_THRS:
            combos.append((t1, pt))

    print(f"共 {len(combos)} 种参数组合 (t1_mul={T1_MULS} × purity_thr={PURITY_THRS})")
    print(f"sec5_billion 固定 = {SEC5_BILLION}")
    print(f"目标文件: {OUT_TSV}\n")

    header = PARAM_COLS + TSV_HEADER
    all_rows: list[list[str]] = []

    for idx, (t1_mul, purity_thr) in enumerate(combos, 1):
        m = calc_day(
            DRY_RUN_LADDER, DRY_RUN_SECTOR, prev=None,
            t1_mul=t1_mul,
            purity_thr=purity_thr,
            sec5_billion=SEC5_BILLION,
        )
        row = [
            f"{t1_mul}",
            f"{purity_thr}",
            f"{SEC5_BILLION}",
        ] + m.tsv_row()
        all_rows.append(row)
        print(f"[{idx:02d}/20] t1_mul={t1_mul:g}, purity_thr={purity_thr:g} → "
              f"T1_thr={m.T1_dynamic_threshold:.1f}%  "
              f"T1={'PASS' if m.T1_pct >= m.T1_dynamic_threshold else 'WAIT'}  "
              f"抱团={'YES' if m.Purity_ge2_pct >= purity_thr * 100 else 'NO'}  "
              f"低离散={'YES' if m.sector_top5_sum_yi < SEC5_BILLION else 'NO'}")

    OUT_TSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_TSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(header)
        w.writerows(all_rows)

    print(f"\n写入 {len(all_rows)} 行 -> {OUT_TSV}")
    print("\n=== TSV 前 10 行（含表头） ===")
    with open(OUT_TSV, "r", encoding="utf-8-sig") as f:
        for i, line in enumerate(f):
            if i >= 10:
                break
            print(line.rstrip("\n"))

    print("\n=== SUMMARY ===")
    print(f"参数空间: {len(T1_MULS)} t1_mul × {len(PURITY_THRS)} purity_thr = {len(combos)} 组合")
    print(f"固定参数: sec5_billion = {SEC5_BILLION}")
    print(f"输出列数: {len(header)} 列 ({len(PARAM_COLS)} 参数 + {len(TSV_HEADER)} 指标)")
    print(f"输出行数: {len(all_rows)} 数据行 + 1 表头")

    pass_count = sum(
        1 for r in all_rows
        if float(r[9]) >= float(r[8])
    )
    purity_count = sum(
        1 for r in all_rows
        if float(r[11]) >= float(r[1]) * 100
    )
    low_disp = sum(
        1 for r in all_rows
        if float(r[12]) < SEC5_BILLION
    )
    print(f"T1集中次数: {pass_count}/20")
    print(f"抱团满足次数: {purity_count}/20")
    print(f"低离散(sector5<{SEC5_BILLION}亿)次数: {low_disp}/20")


if __name__ == "__main__":
    main()
