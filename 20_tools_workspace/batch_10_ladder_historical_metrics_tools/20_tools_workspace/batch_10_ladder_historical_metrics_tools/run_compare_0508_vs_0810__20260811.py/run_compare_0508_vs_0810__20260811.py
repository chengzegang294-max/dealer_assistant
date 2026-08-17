from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path

WORK_DIR = Path(r"D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_10_ladder_historical_tools__20260811")
sys.path.insert(0, str(WORK_DIR))

from calc_ladder_metrics_batch_v1 import DayMetrics, TSV_HEADER, calc_day

LADDER_CSV = r"D:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\ashare_watchlist\factors_ladder_20260508.csv"

OUT_TSV = str(WORK_DIR / "compare_0508_vs_0810__20260811.tsv")
OUT_MD = str(WORK_DIR / "compare_0508_vs_0810__20260811.md")
LADDER_JSON = str(WORK_DIR / "_tmp_ladder_20260508.json")
SECTOR_JSON = str(WORK_DIR / "_tmp_sector_20260508.json")

INDICATOR_LABELS = {
    "date": "日期",
    "max_level": "最高连板(max_lv)",
    "total_stocks": "连板总数",
    "ge2_stocks": "≥2板数",
    "first_panel_count": "首板数",
    "T1_dynamic_threshold": "T1动态阈值(%)",
    "T1_pct": "T1集中度(%)",
    "T3_pct": "T3集中度(%)",
    "Purity_ge2_pct": "中高位抱团纯度(Purity)(%)",
    "sector_top5_sum_yi": "行业前5主力净流入合计(sec5)(亿)",
    "align_top3_top5_count": "主题-行业对齐度(/3)",
    "consecutive_divergence_days": "连续背离天数",
    "top4_di_list": "top4发散指数(DI)",
    "top4_risk_list": "top4风险灯",
    "p1_position_advice": "P1仓位建议",
    "fake_strength_warning": "假强警示",
}

NUMERIC_KEYS = [
    "max_level", "total_stocks", "ge2_stocks", "first_panel_count",
    "T1_dynamic_threshold", "T1_pct", "T3_pct", "Purity_ge2_pct",
    "sector_top5_sum_yi", "align_top3_top5_count", "consecutive_divergence_days",
]


def csv_to_ladder_json(csv_path: str, json_path: str) -> None:
    boards: dict[int, list[dict]] = {}
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lv = int(row["ladder_height"] or 0)
            trading_amount_raw = float(row.get("order_amount") or 0) * 3.5
            stock = {
                "code": row["code"],
                "name": row["name"],
                "primary_theme": row["industry"] or "UNKNOWN",
                "first_limit_up_time": "",
                "limit_up_type": "",
                "open_num": int(row["open_num"] or 0),
                "trading_amount": trading_amount_raw,
                "order_amount": float(row["order_amount"] or 0),
                "turnover_rate": float(row["turnover_rate"] or 0),
            }
            boards.setdefault(lv, []).append(stock)

    board_list = [{"level": lv, "stocks": stocks} for lv, stocks in sorted(boards.items())]
    payload = {"dates": [{"boards": board_list}]}
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def build_sector_json(json_path: str) -> None:
    names = ["煤炭", "钢铁", "有色", "电力", "石化"]
    amounts_yi = [22.0, 18.5, 16.0, 13.5, 10.0]
    total_yi = sum(amounts_yi)
    print(f"[合成sector] top5={names} 各自(亿)={amounts_yi} 合计={total_yi:.1f}亿")
    rows = [
        {"sectorName": n, "mainNetAmount": a * 1e8}
        for n, a in zip(names, amounts_yi)
    ]
    payload = {"rows": rows}
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def metrics_to_dict(m: DayMetrics, force_date: str | None = None) -> dict:
    return {
        "date": force_date if force_date else m.date,
        "max_level": m.max_level,
        "total_stocks": m.total_stocks,
        "ge2_stocks": m.ge2_stocks,
        "first_panel_count": m.first_panel_count,
        "T1_dynamic_threshold": round(m.T1_dynamic_threshold, 1),
        "T1_pct": round(m.T1_pct, 1),
        "T3_pct": round(m.T3_pct, 1),
        "Purity_ge2_pct": round(m.Purity_ge2_pct, 1),
        "sector_top5_sum_yi": round(m.sector_top5_sum_yi, 1),
        "align_top3_top5_count": m.align_top3_top5_count,
        "consecutive_divergence_days": m.consecutive_divergence_days,
        "top4_di_list": ",".join(str(x) for x in m.top4_di_list),
        "top4_risk_list": ",".join(m.top4_risk_list),
        "p1_position_advice": m.p1_position_advice,
        "fake_strength_warning": "0" if m.fake_strength_warning == "NO" else ("1" if m.fake_strength_warning == "YES" else m.fake_strength_warning),
    }


def load_0810_from_dryrun() -> dict:
    dry = WORK_DIR / "dry_run_20260810.tsv"
    with open(dry, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter="\t")
        row = next(reader)
    result = {}
    for k in TSV_HEADER:
        v = row.get(k, "")
        if k in NUMERIC_KEYS:
            try:
                if "." in str(v):
                    result[k] = round(float(v), 1)
                else:
                    result[k] = int(v)
            except ValueError:
                result[k] = v
        elif k == "top4_di_list" or k == "top4_risk_list":
            result[k] = str(v).replace("|", ",").replace("，", ",")
        elif k == "fake_strength_warning":
            vv = str(v).strip().upper()
            if vv == "NO":
                result[k] = "0"
            elif vv == "YES":
                result[k] = "1"
            else:
                result[k] = str(v)
        else:
            result[k] = v
    result["date"] = "20260810"
    return result


def direction_str(diff_val, key: str) -> str:
    if key not in NUMERIC_KEYS:
        return "持平"
    if isinstance(diff_val, (int, float)):
        if diff_val > 0:
            return "上升"
        if diff_val < 0:
            return "下降"
    return "持平"


def compute_diff(v05, v08, key: str):
    if key in NUMERIC_KEYS:
        try:
            a = float(v05) if not isinstance(v05, (int, float)) else v05
            b = float(v08) if not isinstance(v08, (int, float)) else v08
            return round(a - b, 1)
        except (ValueError, TypeError):
            return ""
    return ""


def write_compare_tsv(d05: dict, d08: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["指标名", "20260508值", "20260810值", "差值", "变化方向"])
        for k in TSV_HEADER:
            label = INDICATOR_LABELS.get(k, k)
            v05 = d05.get(k, "")
            v08 = d08.get(k, "")
            diff = compute_diff(v05, v08, k)
            drc = direction_str(diff, k)
            w.writerow([label, v05, v08, diff, drc])


def write_compare_md(d05: dict, d08: dict, path: str) -> None:
    lines = []
    lines.append("# 20260508 vs 20260810 连板天梯16项指标对比报告")
    lines.append("")
    lines.append(f"- 生成日期：2026-08-11")
    lines.append(f"- 基准日(0810)：max_lv=5 / T1=12.1% / Purity=61.5% / sec5=72.5亿")
    lines.append(f"- 对比日(0508)：factors_ladder CSV 特征匹配数=2，sector 为合成(煤炭/钢铁/有色/电力/石化 合计≈80亿)")
    lines.append("")
    lines.append("## 一、指标对比表")
    lines.append("")
    lines.append("| 指标名 | 20260508值 | 20260810值 | 差值 | 变化方向 |")
    lines.append("|---|---:|---:|---:|---|")
    for k in TSV_HEADER:
        label = INDICATOR_LABELS.get(k, k)
        v05 = d05.get(k, "")
        v08 = d08.get(k, "")
        diff = compute_diff(v05, v08, k)
        drc = direction_str(diff, k)
        align = "" if k not in NUMERIC_KEYS else ""
        lines.append(f"| {label} | {v05} | {v08} | {diff} | {drc} |")
    lines.append("")
    lines.append("## 二、P1 建议文案对比")
    lines.append("")
    lines.append("| 日期 | P1仓位建议 | 假强警示 | 核心背景 |")
    lines.append("|---|---|---|---|")
    lines.append(f"| 20260810 | {d08.get('p1_position_advice','')} | {d08.get('fake_strength_warning','')} | 首板86只+最高5板，T1=12.1%分散，sec5=72.5亿<100低离散，对齐度=0→连续背离1天 |")
    lines.append(f"| 20260508 | {d05.get('p1_position_advice','')} | {d05.get('fake_strength_warning','')} | 首板{d05.get('first_panel_count','')}只+最高{d05.get('max_level','')}板，T1={d05.get('T1_pct','')}%，sec5={d05.get('sector_top5_sum_yi','')}亿，对齐度={d05.get('align_top3_top5_count','')} |")
    lines.append("")
    lines.append("## 三、核心差异洞察")
    lines.append("")
    t1_diff = compute_diff(d05.get("T1_pct", 0), d08.get("T1_pct", 0), "T1_pct")
    p_diff = compute_diff(d05.get("Purity_ge2_pct", 0), d08.get("Purity_ge2_pct", 0), "Purity_ge2_pct")
    s_diff = compute_diff(d05.get("sector_top5_sum_yi", 0), d08.get("sector_top5_sum_yi", 0), "sector_top5_sum_yi")
    lv_diff = compute_diff(d05.get("max_level", 0), d08.get("max_level", 0), "max_level")
    lines.append(f"- **T1集中度**：0508={d05.get('T1_pct','')}% vs 0810={d08.get('T1_pct','')}% → {'更集中' if t1_diff and t1_diff>0 else ('更分散' if t1_diff and t1_diff<0 else '持平')}（差{t1_diff}pp）")
    lines.append(f"- **中高位抱团Purity**：0508={d05.get('Purity_ge2_pct','')}% vs 0810={d08.get('Purity_ge2_pct','')}% → {'更强' if p_diff and p_diff>0 else ('更弱' if p_diff and p_diff<0 else '持平')}（差{p_diff}pp）")
    lines.append(f"- **行业资金sec5**：0508={d05.get('sector_top5_sum_yi','')}亿 vs 0810={d08.get('sector_top5_sum_yi','')}亿 → {'更高' if s_diff and s_diff>0 else ('更低' if s_diff and s_diff<0 else '持平')}（差{s_diff}亿）")
    lines.append(f"- **最高板高度**：0508={d05.get('max_level','')}板 vs 0810={d08.get('max_level','')}板 → {'更高' if lv_diff and lv_diff>0 else ('更低' if lv_diff and lv_diff<0 else '持平')}（差{lv_diff}板）")
    lines.append("")
    lines.append("## 四、结论与操作提示")
    lines.append("")
    lines.append("> 注：0508 sector 为合成数据，sec5 相关结论仅供参考，需以真实归档数据回补后方可定论。")
    lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def print_tsv_console(path: str) -> None:
    print("\n===== [CONSOLE] 对比 TSV 全表 =====")
    with open(path, "r", encoding="utf-8-sig") as f:
        for i, line in enumerate(f):
            print(line.rstrip("\n"))
    print("===== TSV END =====\n")


def print_md_head(path: str, n: int = 30) -> None:
    print(f"===== [CONSOLE] Markdown 报告前 {n} 行 =====")
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= n:
                break
            print(line.rstrip("\n"))
    print("===== MD HEAD END =====\n")


def main() -> None:
    print("[1/6] CSV→JSON 转换连板天梯数据...")
    csv_to_ladder_json(LADDER_CSV, LADDER_JSON)
    print(f"  → 写出: {LADDER_JSON}")

    print("[2/6] 合成 sector_top5 JSON（煤炭/钢铁/有色/电力/石化 ≈80亿）...")
    build_sector_json(SECTOR_JSON)
    print(f"  → 写出: {SECTOR_JSON}")

    print("[3/6] 调用 calc_day 计算 20260508 的16列指标...")
    m05 = calc_day(LADDER_JSON, SECTOR_JSON, prev=None)
    d05 = metrics_to_dict(m05, force_date="20260508")
    print(f"  → 0508 指标计算完毕: max_lv={d05['max_level']} N={d05['total_stocks']} T1={d05['T1_pct']}% Purity={d05['Purity_ge2_pct']}% sec5={d05['sector_top5_sum_yi']}亿")

    print("[4/6] 载入 20260810 基准指标...")
    d08 = load_0810_from_dryrun()
    print(f"  → 0810 基准载入: max_lv={d08['max_level']} N={d08['total_stocks']} T1={d08['T1_pct']}% Purity={d08['Purity_ge2_pct']}% sec5={d08['sector_top5_sum_yi']}亿")

    print("[5/6] 生成对比 TSV + Markdown 报告...")
    write_compare_tsv(d05, d08, OUT_TSV)
    print(f"  → TSV: {OUT_TSV}")
    write_compare_md(d05, d08, OUT_MD)
    print(f"  → MD : {OUT_MD}")

    print("[6/6] 控制台打印输出...")
    print_tsv_console(OUT_TSV)
    print_md_head(OUT_MD, 30)

    for tmp in [LADDER_JSON, SECTOR_JSON]:
        try:
            os.remove(tmp)
        except OSError:
            pass


if __name__ == "__main__":
    main()
