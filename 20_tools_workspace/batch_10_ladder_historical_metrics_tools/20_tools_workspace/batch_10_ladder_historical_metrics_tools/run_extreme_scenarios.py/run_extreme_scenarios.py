from __future__ import annotations

import copy
import csv
import json
import os
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from calc_ladder_metrics_batch_v1 import calc_day, DRY_RUN_LADDER, DRY_RUN_SECTOR


TSV_OUTPUT = SCRIPT_DIR / "extreme_scenarios__20260811.tsv"
TSV_HEADER = [
    "scenario_name", "max_lv", "N", "T1_pct", "Purity_ge2_pct",
    "sec5_sum_yi", "alignment", "div_days", "fake_strength_warning",
    "p1_advice_1", "p1_advice_2",
]


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def split_advice(advice: str) -> tuple[str, str]:
    parts = [p.strip() for p in advice.split("；") if p.strip()]
    a = parts[0] if len(parts) >= 1 else ""
    b = parts[1] if len(parts) >= 2 else ""
    return a, b


def build_scenario_a(base_ladder: dict, base_sector: dict) -> tuple[dict, dict]:
    ladder = copy.deepcopy(base_ladder)
    sector = copy.deepcopy(base_sector)
    rows = sector.get("data", {}).get("rows", [])
    fake_names = ["教育", "体育产业", "酒店餐饮", "种植业", "渔业"]
    for i, row in enumerate(rows[:5]):
        fake = fake_names[i]
        row["sectorName"] = fake
        row["themeName"] = fake
    return ladder, sector


def build_scenario_b(base_ladder: dict, base_sector: dict) -> tuple[dict, dict]:
    ladder = copy.deepcopy(base_ladder)
    sector = copy.deepcopy(base_sector)
    rows = sector.get("data", {}).get("rows", [])
    target_each_yi = 240.0
    target_each = int(target_each_yi * 1e8)
    for row in rows[:5]:
        row["mainNetAmount"] = target_each
    return ladder, sector


def build_scenario_c(base_ladder: dict, base_sector: dict) -> tuple[dict, dict]:
    ladder = copy.deepcopy(base_ladder)
    sector = copy.deepcopy(base_sector)
    dates = ladder.get("dates", [])
    if not dates:
        return ladder, sector
    boards = dates[0].get("boards", [])
    max_board = None
    for b in boards:
        if max_board is None or b.get("level", 0) > max_board.get("level", 0):
            max_board = b
    if max_board is not None:
        max_board["level"] = 8
        for s in max_board.get("stocks", []):
            s["level"] = 8
            s["continue_num"] = 8
            if s.get("trading_amount", 0) > 0:
                s["order_amount"] = int(s["trading_amount"] * 30)
            s["open_num"] = 0
            s["turnover_rate"] = 0.5
    for b in boards:
        for s in b.get("stocks", []):
            if s.get("trading_amount", 0) > 0:
                s["order_amount"] = int(s["trading_amount"] * 15)
            s["open_num"] = 0
            if s.get("turnover_rate", 0) > 10:
                s["turnover_rate"] = 3.0
    return ladder, sector


SCENARIO_BUILDERS = [
    ("场景A_零对齐", build_scenario_a),
    ("场景B_超大蓝筹1200亿", build_scenario_b),
    ("场景C_8连板极高封单", build_scenario_c),
]


def run_scenario(name: str, ladder: dict, sector: dict, tmpdir: str) -> tuple[str, dict]:
    lad_path = os.path.join(tmpdir, f"ladder_{name}.json")
    sec_path = os.path.join(tmpdir, f"sector_{name}.json")
    save_json(ladder, lad_path)
    save_json(sector, sec_path)
    result = calc_day(lad_path, sec_path, prev=None)
    return name, result


def extract_row(name: str, m) -> list[str]:
    p1a, p1b = split_advice(m.p1_position_advice)
    return [
        name,
        str(m.max_level),
        str(m.total_stocks),
        f"{m.T1_pct:.1f}",
        f"{m.Purity_ge2_pct:.1f}",
        f"{m.sector_top5_sum_yi:.1f}",
        str(m.align_top3_top5_count),
        str(m.consecutive_divergence_days),
        m.fake_strength_warning,
        p1a,
        p1b,
    ]


def write_tsv(rows: list[list[str]]) -> None:
    with open(TSV_OUTPUT, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(TSV_HEADER)
        for r in rows:
            w.writerow(r)


def regression_check() -> None:
    print("\n=== [回归校验] 默认场景 p1_advice 字符串一致性 ===")
    m = calc_day(DRY_RUN_LADDER, DRY_RUN_SECTOR, prev=None)
    expected_advice = "T1分散→多看少动；中高位抱团→盯前排"
    actual = m.p1_position_advice
    if actual == expected_advice:
        print(f"[OK] p1_position_advice 完全匹配:")
        print(f"     期望: {expected_advice}")
        print(f"     实际: {actual}")
    else:
        print(f"[FAIL] p1_position_advice 不匹配!")
        print(f"     期望: {expected_advice}")
        print(f"     实际: {actual}")
        sys.exit(3)


def main() -> None:
    print("=== 极端场景合成测试 ===")
    base_ladder = load_json(DRY_RUN_LADDER)
    base_sector = load_json(DRY_RUN_SECTOR)

    all_rows: list[list[str]] = []
    results: list[tuple[str, Any]] = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for name, builder in SCENARIO_BUILDERS:
            lad, sec = builder(base_ladder, base_sector)
            _, m = run_scenario(name, lad, sec, tmpdir)
            results.append((name, m))
            row = extract_row(name, m)
            all_rows.append(row)
            print(f"\n[{name}] 构建完成 -> max={m.max_level} N={m.total_stocks} "
                  f"T1={m.T1_pct:.1f}% P_ge2={m.Purity_ge2_pct:.1f}% "
                  f"sec5={m.sector_top5_sum_yi:.1f}亿 align={m.align_top3_top5_count}")

    print("\n=== 控制台打印 3 行完整结果 ===")
    print("\t".join(TSV_HEADER))
    for r in all_rows:
        print("\t".join(r))

    write_tsv(all_rows)
    print(f"\n写入 TSV -> {TSV_OUTPUT}")

    regression_check()

    print("\n全部完成 [OK]")


if __name__ == "__main__":
    main()
