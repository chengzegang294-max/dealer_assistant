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

T1_MULS = [0.9, 1.0, 1.1]
PURITY_THRS = [0.55, 0.60, 0.65]
SEC5_BILLIONS = [80, 100, 120]

OUT_TSV = Path(__file__).parent / "sensitivity_full_27combos__20260811.tsv"
OUT_MD = Path(__file__).parent / "sensitivity_27_signal_matrix.md"

PARAM_COLS = ["t1_mul", "purity_thr", "sec5_billion"]


def main() -> None:
    combos: list[tuple[float, float, float]] = []
    for t1 in T1_MULS:
        for pt in PURITY_THRS:
            for s5 in SEC5_BILLIONS:
                combos.append((t1, pt, s5))

    print(f"共 {len(combos)} 种参数组合 (t1_mul={T1_MULS} × purity_thr={PURITY_THRS} × sec5_billion={SEC5_BILLIONS})")
    print(f"目标文件: {OUT_TSV}\n")

    header = PARAM_COLS + TSV_HEADER
    all_rows: list[list[str]] = []

    t1_trigger_count = 0
    low_dispersion_count = 0
    purity_cluster_count = 0
    consecutive_div_ge2_count = 0
    fake_strength_warning_count = 0

    for idx, (t1_mul, purity_thr, sec5_billion) in enumerate(combos, 1):
        m = calc_day(
            DRY_RUN_LADDER, DRY_RUN_SECTOR, prev=None,
            t1_mul=t1_mul,
            purity_thr=purity_thr,
            sec5_billion=sec5_billion,
        )
        row = [
            f"{t1_mul:g}",
            f"{purity_thr:g}",
            f"{sec5_billion:g}",
        ] + m.tsv_row()
        all_rows.append(row)

        t1_triggered = m.T1_pct >= m.T1_dynamic_threshold
        low_dispersion = m.sector_top5_sum_yi < sec5_billion
        purity_cluster = m.Purity_ge2_pct >= purity_thr * 100
        consecutive_div_ge2 = m.consecutive_divergence_days >= 2
        fake_strength = m.fake_strength_warning == "YES"

        if t1_triggered:
            t1_trigger_count += 1
        if low_dispersion:
            low_dispersion_count += 1
        if purity_cluster:
            purity_cluster_count += 1
        if consecutive_div_ge2:
            consecutive_div_ge2_count += 1
        if fake_strength:
            fake_strength_warning_count += 1

        print(f"[{idx:02d}/27] t1_mul={t1_mul:g}, purity_thr={purity_thr:g}, sec5_b={sec5_billion:3g}亿 -> "
              f"T1_thr={m.T1_dynamic_threshold:4.1f}%  "
              f"T1={'PASS' if t1_triggered else 'WAIT'}  "
              f"抱团={'YES' if purity_cluster else 'NO '}  "
              f"低离散={'YES' if low_dispersion else 'NO '}  "
              f"背离≥2={'Y' if consecutive_div_ge2 else '-'}  "
              f"假强={'Y' if fake_strength else '-'}")

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

    print("\n==============================")
    print("===  CONSOLE SUMMARY 27    ===")
    print("==============================")
    print(f"参数空间: {len(T1_MULS)} t1_mul × {len(PURITY_THRS)} purity_thr × {len(SEC5_BILLIONS)} sec5_b = {len(combos)} 组合")
    print(f"1) T1 信号触发 (T1_pct ≥ T1_dynamic_threshold):     {t1_trigger_count}/27")
    print(f"2) 低离散 (sec5_sum < sec5_billion thr):            {low_dispersion_count}/27")
    print(f"3) 抱团 (Purity ≥ purity_thr × 100):                {purity_cluster_count}/27")
    print(f"4) 连续背离 ≥ 2 天:                                  {consecutive_div_ge2_count}/27")
    print(f"5) 假强警示触发:                                      {fake_strength_warning_count}/27")
    print("==============================\n")

    print("=== 生成 3×3×3 Purity×T1 触发矩阵（按 sec5 分页） -> sensitivity_27_signal_matrix.md ===")

    sec5_pages = {}
    for s5 in SEC5_BILLIONS:
        sec5_pages[s5] = {}
        for pt in PURITY_THRS:
            sec5_pages[s5][pt] = {}
            for t1 in T1_MULS:
                sec5_pages[s5][pt][t1] = None

    for r in all_rows:
        t1_mul_val = float(r[0])
        purity_thr_val = float(r[1])
        sec5_val = float(r[2])
        T1_thr = float(r[8])
        T1_pct_val = float(r[9])
        Purity_val = float(r[11])
        t1_pass = T1_pct_val >= T1_thr
        purity_pass = Purity_val >= purity_thr_val * 100
        sec5_pages[sec5_val][purity_thr_val][t1_mul_val] = (t1_pass, purity_pass, T1_pct_val, T1_thr, Purity_val)

    md_lines: list[str] = []
    md_lines.append("# Sensitivity 27 Combos: Purity × T1 触发矩阵（按 sec5_billion 分页）")
    md_lines.append("")
    md_lines.append(f"- 参数空间: t1_mul∈{T1_MULS} × purity_thr∈{PURITY_THRS} × sec5_billion∈{SEC5_BILLIONS} = 27 组合")
    md_lines.append(f"- 数据日: 20260810（8/10 真实数据 calc_day，prev=None）")
    md_lines.append(f"- 记号: `T1_PASS` / `T1_WAIT` · `PURITY_YES` / `PURITY_NO` · 单元格为 `(T1状态, Purity状态)`")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

    for s5 in SEC5_BILLIONS:
        md_lines.append(f"## Page: sec5_billion = {s5} 亿")
        md_lines.append("")
        md_lines.append(f"低离散条件: sector_top5_sum_yi < {s5} 亿  （8/10 实际值 = {all_rows[0][12]} 亿）")
        md_lines.append("")
        header_row = "| purity_thr \\\\ t1_mul | " + " | ".join(f"{t1:g}" for t1 in T1_MULS) + " |"
        sep_row = "|" + "|".join(["---"] * (len(T1_MULS) + 1)) + "|"
        md_lines.append(header_row)
        md_lines.append(sep_row)

        for pt in PURITY_THRS:
            cells = []
            for t1 in T1_MULS:
                info = sec5_pages[s5][pt][t1]
                if info is None:
                    cells.append("N/A")
                    continue
                t1_pass, purity_pass, T1_pct_val, T1_thr, Purity_val = info
                t1_str = "T1_PASS" if t1_pass else "T1_WAIT"
                pur_str = "PURITY_YES" if purity_pass else "PURITY_NO"
                cells.append(f"`({t1_str}, {pur_str})`<br>T1={T1_pct_val:.1f}%/{T1_thr:.1f}%<br>Pur={Purity_val:.1f}%/{pt*100:.0f}%")
            line = f"| {pt:g} | " + " | ".join(cells) + " |"
            md_lines.append(line)

        md_lines.append("")
        md_lines.append("### 本页单独计数")
        md_lines.append("")
        t1_pass_page = sum(1 for pt in PURITY_THRS for t1 in T1_MULS if sec5_pages[s5][pt][t1] and sec5_pages[s5][pt][t1][0])
        pur_pass_page = sum(1 for pt in PURITY_THRS for t1 in T1_MULS if sec5_pages[s5][pt][t1] and sec5_pages[s5][pt][t1][1])
        md_lines.append(f"- T1 触发: {t1_pass_page}/9")
        md_lines.append(f"- 抱团满足: {pur_pass_page}/9")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

    md_lines.append("## 全局汇总")
    md_lines.append("")
    md_lines.append("| sec5_billion | T1 触发 /9 | 抱团满足 /9 |")
    md_lines.append("|---|---|---|")
    for s5 in SEC5_BILLIONS:
        t1_pass_page = sum(1 for pt in PURITY_THRS for t1 in T1_MULS if sec5_pages[s5][pt][t1] and sec5_pages[s5][pt][t1][0])
        pur_pass_page = sum(1 for pt in PURITY_THRS for t1 in T1_MULS if sec5_pages[s5][pt][t1] and sec5_pages[s5][pt][t1][1])
        md_lines.append(f"| {s5} 亿 | {t1_pass_page}/9 | {pur_pass_page}/9 |")
    md_lines.append("")
    md_lines.append(f"**合计**: T1={t1_trigger_count}/27 · 抱团={purity_cluster_count}/27 · 低离散={low_dispersion_count}/27 · 背离≥2天={consecutive_div_ge2_count}/27 · 假强={fake_strength_warning_count}/27")
    md_lines.append("")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines) + "\n")

    print(f"写入 -> {OUT_MD}")
    print("=== DONE ===")


if __name__ == "__main__":
    main()
