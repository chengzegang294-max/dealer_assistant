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

PURITY_THR = 0.6
SEC5_BILLIONS = [80, 90, 100, 110, 120]
T1_MULS = [0.90, 1.00, 1.10]

OUT_TSV = Path(__file__).parent / "sensitivity_sec5_t1_15combos__20260811.tsv"

PARAM_COLS = ["sec5_b", "t1_mul"]


def main() -> None:
    combos: list[tuple[float, float]] = []
    for s5 in SEC5_BILLIONS:
        for t1 in T1_MULS:
            combos.append((s5, t1))

    print(f"共 {len(combos)} 种参数组合 (sec5_billion={SEC5_BILLIONS} × t1_mul={T1_MULS})")
    print(f"purity_thr 固定 = {PURITY_THR}")
    print(f"目标文件: {OUT_TSV}\n")

    header = PARAM_COLS + TSV_HEADER
    all_rows: list[list[str]] = []

    t1_trigger_count = 0
    low_dispersion_count = 0
    warning_count = 0

    for idx, (sec5_b, t1_mul) in enumerate(combos, 1):
        m = calc_day(
            DRY_RUN_LADDER, DRY_RUN_SECTOR, prev=None,
            t1_mul=t1_mul,
            purity_thr=PURITY_THR,
            sec5_billion=sec5_b,
        )
        row = [
            f"{sec5_b:g}",
            f"{t1_mul:.2f}",
        ] + m.tsv_row()
        all_rows.append(row)

        t1_triggered = m.T1_pct >= m.T1_dynamic_threshold
        low_dispersion = m.sector_top5_sum_yi < sec5_b
        warning_triggered = m.consecutive_divergence_days >= 3 or m.fake_strength_warning == "YES"

        if t1_triggered:
            t1_trigger_count += 1
        if low_dispersion:
            low_dispersion_count += 1
        if warning_triggered:
            warning_count += 1

        print(f"[{idx:02d}/15] sec5_b={sec5_b:3g}亿, t1_mul={t1_mul:.2f} -> "
              f"T1_thr={m.T1_dynamic_threshold:4.1f}%  "
              f"T1={'PASS' if t1_triggered else 'WAIT'}  "
              f"低离散={'YES' if low_dispersion else 'NO'}  "
              f"警示={'ON' if warning_triggered else '--'}  "
              f"(sec5实际={m.sector_top5_sum_yi:.1f}亿)")

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

    print("\n=== SUMMARY 15 COMBOS ===")
    print(f"参数空间: {len(SEC5_BILLIONS)} sec5_billion × {len(T1_MULS)} t1_mul = {len(combos)} 组合")
    print(f"固定参数: purity_thr = {PURITY_THR}")
    print(f"输出列数: {len(header)} 列 ({len(PARAM_COLS)} 参数 + {len(TSV_HEADER)} 指标)")
    print(f"输出行数: {len(all_rows)} 数据行 + 1 表头")
    print(f"T1 信号触发 (T1_pct ≥ T1_dynamic_threshold): {t1_trigger_count}/15")
    print(f"低离散 (sector_top5_sum_yi < sec5_billion):      {low_dispersion_count}/15")
    print(f"连续背离≥3天 或 假强警示触发:                   {warning_count}/15")


if __name__ == "__main__":
    main()
