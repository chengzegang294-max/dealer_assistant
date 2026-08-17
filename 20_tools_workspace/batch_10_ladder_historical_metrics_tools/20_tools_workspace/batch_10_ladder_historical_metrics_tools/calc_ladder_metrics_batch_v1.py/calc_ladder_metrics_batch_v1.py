from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

UTC8 = timezone(timedelta(hours=8))

DRY_RUN_LADDER = r"d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\ladder_daily_snapshots\ladder_day_min__20260810.json"
DRY_RUN_SECTOR = r"d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\sector_daily_snapshots\sector_capital_flow_snapshot__20260810.json"

EXPECTED_0810 = {
    "max_level": 5,
    "total_stocks": 99,
    "first_panel_count": 86,
    "ge2_stocks": 13,
    "T1_pct": 12.1,
    "T3_pct": 23.2,
    "Purity_ge2_pct": 61.5,
    "sector_top5_sum_yi": 72.5,
    "align_top3_top5_count": 0,
}


@dataclass
class StockRow:
    level: int
    code: str = ""
    name: str = ""
    primary_theme: str = "UNKNOWN"
    first_limit_up_time: str = ""
    limit_up_type: str = ""
    open_num: int = 0
    trading_amount: float = 0.0
    order_amount: float = 0.0
    turnover_rate: float = 0.0

    @property
    def seal_ratio(self) -> float:
        return self.order_amount / self.trading_amount if self.trading_amount else 0.0

    @property
    def divergence_index(self) -> int:
        return (self.open_num or 0) * self.level

    @property
    def risk(self) -> str:
        s = self.seal_ratio
        d = self.divergence_index
        t = self.turnover_rate
        if s < 0.3 or d > 10 or t > 25:
            return "R"
        if s < 1 or d >= 5 or t > 15:
            return "Y"
        return "G"


@dataclass
class DayMetrics:
    date: str = ""
    max_level: int = 0
    total_stocks: int = 0
    ge2_stocks: int = 0
    first_panel_count: int = 0
    T1_dynamic_threshold: float = 25.0
    T1_pct: float = 0.0
    T3_pct: float = 0.0
    Purity_ge2_pct: float = 0.0
    sector_top5_sum_yi: float = 0.0
    align_top3_top5_count: int = 0
    consecutive_divergence_days: int = 0
    top4_di_list: list[int] = field(default_factory=list)
    top4_risk_list: list[str] = field(default_factory=list)
    p1_position_advice: str = ""
    fake_strength_warning: str = "NO"

    def tsv_row(self) -> list[str]:
        return [
            self.date,
            str(self.max_level),
            str(self.total_stocks),
            str(self.ge2_stocks),
            str(self.first_panel_count),
            f"{self.T1_dynamic_threshold:.1f}",
            f"{self.T1_pct:.1f}",
            f"{self.T3_pct:.1f}",
            f"{self.Purity_ge2_pct:.1f}",
            f"{self.sector_top5_sum_yi:.1f}",
            str(self.align_top3_top5_count),
            str(self.consecutive_divergence_days),
            "|".join(str(x) for x in self.top4_di_list) if self.top4_di_list else "",
            "|".join(self.top4_risk_list) if self.top4_risk_list else "",
            self.p1_position_advice,
            self.fake_strength_warning,
        ]


TSV_HEADER = [
    "date", "max_level", "total_stocks", "ge2_stocks", "first_panel_count",
    "T1_dynamic_threshold", "T1_pct", "T3_pct", "Purity_ge2_pct",
    "sector_top5_sum_yi", "align_top3_top5_count", "consecutive_divergence_days",
    "top4_di_list", "top4_risk_list", "p1_position_advice", "fake_strength_warning",
]


def ts_to_hhmm(ts_str: str) -> str:
    try:
        ts = int(ts_str)
        return datetime.fromtimestamp(ts, UTC8).strftime("%H:%M")
    except Exception:
        return "?"


def load_ladder(path: str) -> list[StockRow]:
    with open(path, "r", encoding="utf-8") as f:
        payload: dict[str, Any] = json.load(f)
    rows: list[StockRow] = []
    for day in payload.get("dates", []):
        for b in day.get("boards", []):
            lv = int(b.get("level", 0) or 0)
            for s in b.get("stocks", []):
                rows.append(StockRow(
                    level=lv,
                    code=str(s.get("code") or ""),
                    name=str(s.get("name") or ""),
                    primary_theme=str(s.get("primary_theme") or "UNKNOWN"),
                    first_limit_up_time=ts_to_hhmm(str(s.get("first_limit_up_time") or "")),
                    limit_up_type=str(s.get("limit_up_type") or ""),
                    open_num=int(s.get("open_num") or 0),
                    trading_amount=float(s.get("trading_amount") or 0),
                    order_amount=float(s.get("order_amount") or 0),
                    turnover_rate=float(s.get("turnover_rate") or 0),
                ))
    return rows


def load_sector(path: str) -> tuple[list[str], list[float]]:
    with open(path, "r", encoding="utf-8") as f:
        payload: dict[str, Any] = json.load(f)
    rows_src = (
        payload.get("rows")
        or payload.get("data", {}).get("rows", [])
        or payload.get("records", [])
    )
    names: list[str] = []
    amounts: list[float] = []
    for s in rows_src[:5]:
        name = (
            s.get("sectorName")
            or s.get("plateNameCn")
            or s.get("themeName")
            or s.get("name")
            or "?"
        )
        amt = float(s.get("mainNetAmount") or 0)
        names.append(str(name))
        amounts.append(amt)
    return names, amounts


def extract_date_from_path(p: str) -> str:
    stem = Path(p).stem
    for token in stem.split("__"):
        if len(token) == 8 and token.isdigit():
            return token
    return stem[:8] if len(stem) >= 8 and stem[:8].isdigit() else stem


def calc_day(
    ladder_path: str,
    sector_path: str,
    prev: DayMetrics | None,
    t1_mul: float = 1.0,
    purity_thr: float = 0.6,
    sec5_billion: float = 100.0,
) -> DayMetrics:
    stocks = load_ladder(ladder_path)
    sector_names, sector_amts = load_sector(sector_path)

    level_counter: Counter[int] = Counter()
    theme_all: Counter[str] = Counter()
    theme_ge2: Counter[str] = Counter()
    high_mid: list[StockRow] = []

    for s in stocks:
        level_counter[s.level] += 1
        theme_all[s.primary_theme] += 1
        if s.level >= 2:
            theme_ge2[s.primary_theme] += 1
            high_mid.append(s)

    N = len(stocks)
    N_ge2 = len(high_mid)
    first_panel = level_counter.get(1, 0)
    max_lv = max(level_counter.keys()) if level_counter else 0

    T1_top = theme_all.most_common(1)
    T3_top = theme_all.most_common(3)
    T1_pct = (T1_top[0][1] / N * 100) if T1_top and N else 0.0
    T3_pct = (sum(x[1] for x in T3_top) / N * 100) if N else 0.0

    T1_ge2_top = theme_ge2.most_common(1)
    P_ge2 = (T1_ge2_top[0][1] / N_ge2 * 100) if T1_ge2_top and N_ge2 else 0.0

    top3_themes = [x[0] for x in T3_top]
    overlap = sum(
        1 for th in top3_themes
        if any(th and th in n or (n and n in th) for n in sector_names)
    )

    total_top5_yi = sum(sector_amts) / 1e8

    if first_panel > 80:
        T1_th_raw = 20.0
    elif first_panel < 60:
        T1_th_raw = 30.0
    else:
        T1_th_raw = 25.0
    T1_th = T1_th_raw * t1_mul

    sorted_by_lv_di = sorted(
        high_mid, key=lambda s: (-s.level, -s.divergence_index)
    )
    top4 = sorted_by_lv_di[:4]
    top4_di = [s.divergence_index for s in top4]
    top4_risk = [s.risk for s in top4]

    m = DayMetrics(
        date=extract_date_from_path(ladder_path),
        max_level=max_lv,
        total_stocks=N,
        ge2_stocks=N_ge2,
        first_panel_count=first_panel,
        T1_dynamic_threshold=T1_th,
        T1_pct=T1_pct,
        T3_pct=T3_pct,
        Purity_ge2_pct=P_ge2,
        sector_top5_sum_yi=total_top5_yi,
        align_top3_top5_count=overlap,
        top4_di_list=top4_di,
        top4_risk_list=top4_risk,
    )

    low_dispersion = total_top5_yi < sec5_billion
    diverged_today = overlap == 0 and low_dispersion
    if prev is not None:
        if diverged_today:
            m.consecutive_divergence_days = prev.consecutive_divergence_days + 1
        else:
            m.consecutive_divergence_days = 0
        if low_dispersion and max_lv > prev.max_level and prev.max_level > 0:
            m.fake_strength_warning = "YES"
    else:
        m.consecutive_divergence_days = 1 if diverged_today else 0

    advice_parts: list[str] = []
    if m.consecutive_divergence_days >= 3:
        advice_parts.append("连续3天背离→🔴强制休息")
    if m.fake_strength_warning == "YES":
        advice_parts.append("假强→P1仓位降1档")
    if m.T1_pct >= T1_th:
        advice_parts.append("T1集中→可试错")
    else:
        advice_parts.append("T1分散→多看少动")
    if m.Purity_ge2_pct >= purity_thr * 100:
        advice_parts.append("中高位抱团→盯前排")
    m.p1_position_advice = "；".join(advice_parts)

    return m


def find_files(directory: str, pattern: str, start: str | None, end: str | None) -> list[tuple[str, str]]:
    d = Path(directory)
    results: list[tuple[str, str]] = []
    for p in sorted(d.glob(pattern)):
        dt = extract_date_from_path(str(p))
        if start and dt < start:
            continue
        if end and dt > end:
            continue
        results.append((dt, str(p)))
    return results


def pair_ladder_sector(ladder_dir: str, sector_dir: str, start: str | None, end: str | None) -> list[tuple[str, str, str]]:
    ladder_files = dict(find_files(ladder_dir, "ladder_day_min__*.json", start, end))
    sector_files = dict(find_files(sector_dir, "sector_capital_flow_snapshot__*.json", start, end))
    dates = sorted(set(ladder_files.keys()) & set(sector_files.keys()))
    return [(dt, ladder_files[dt], sector_files[dt]) for dt in dates]


def write_tsv(rows: list[DayMetrics], out_path: str, append: bool) -> None:
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    write_header = (not append) or (not Path(out_path).exists()) or Path(out_path).stat().st_size == 0
    with open(out_path, "a" if append else "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        if write_header:
            w.writerow(TSV_HEADER)
        for r in rows:
            w.writerow(r.tsv_row())


def assert_dry_run(m: DayMetrics) -> None:
    errors: list[str] = []
    for k, v in EXPECTED_0810.items():
        actual = getattr(m, k)
        if isinstance(v, int):
            if abs(int(actual) - v) > 0:
                errors.append(f"{k}: expected {v}, got {actual}")
        else:
            if abs(float(actual) - v) > 0.5:
                errors.append(f"{k}: expected {v}±0.5, got {actual}")
    if errors:
        print("[DRY-RUN FAIL] 8/10 指标不匹配:")
        for e in errors:
            print(f"  × {e}")
        print("\n实际计算值:")
        for k in EXPECTED_0810:
            print(f"  {k} = {getattr(m, k)}")
        sys.exit(2)
    print("[DRY-RUN OK] 8/10 核心指标匹配（容差±0.5 / 整数严格）")


def main() -> None:
    p = argparse.ArgumentParser(description="连板天梯 12 冻结指标批量计算（历史回写 + 每日 append）")
    p.add_argument("--ladder-dir", default=r"d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\ladder_daily_snapshots")
    p.add_argument("--sector-dir", default=r"d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\sector_daily_snapshots")
    p.add_argument("--output-tsv", default=r"d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\metrics_history.tsv")
    p.add_argument("--start-date", default=None, help="YYYYMMDD 可选过滤起始")
    p.add_argument("--end-date", default=None, help="YYYYMMDD 可选过滤结束")
    p.add_argument("--dry-run", action="store_true", help="仅跑 8/10 真实文件并校验指标，不写 TSV")
    p.add_argument("--t1-mul", type=float, default=1.0, help="T1 动态阈值乘法系数（默认 1.0）")
    p.add_argument("--purity-thr", type=float, default=0.6, help="中高位抱团纯度阈值（默认 0.6，即 60%）")
    p.add_argument("--sec5-billion", type=float, default=100.0, help="sector 前5 合计亿数低离散阈值（默认 100）")
    args = p.parse_args()

    if args.dry_run:
        print("=== [DRY-RUN] 8/10 单日指标校验 ===")
        print(f"(t1_mul={args.t1_mul}, purity_thr={args.purity_thr}, sec5_billion={args.sec5_billion})")
        m = calc_day(
            DRY_RUN_LADDER, DRY_RUN_SECTOR, prev=None,
            t1_mul=args.t1_mul,
            purity_thr=args.purity_thr,
            sec5_billion=args.sec5_billion,
        )
        print(f"date={m.date} 最高板={m.max_level} 总数={m.total_stocks} 首板={m.first_panel_count}")
        print(f"T1阈值={m.T1_dynamic_threshold:.1f}% T1={m.T1_pct:.1f}% T3={m.T3_pct:.1f}% Purity≥2板={m.Purity_ge2_pct:.1f}%")
        print(f"sector前5合计={m.sector_top5_sum_yi:.1f}亿 对齐度={m.align_top3_top5_count}/3 连续背离={m.consecutive_divergence_days}天")
        print(f"top4 DI={m.top4_di_list} top4 风险={m.top4_risk_list}")
        print(f"P1建议: {m.p1_position_advice}  假强警示={m.fake_strength_warning}")
        assert_dry_run(m)
        return

    pairs = pair_ladder_sector(args.ladder_dir, args.sector_dir, args.start_date, args.end_date)
    if not pairs:
        print("未找到匹配的 ladder+sector JSON 对")
        sys.exit(1)

    rows: list[DayMetrics] = []
    prev: DayMetrics | None = None
    for dt, lp, sp in pairs:
        m = calc_day(
            lp, sp, prev,
            t1_mul=args.t1_mul,
            purity_thr=args.purity_thr,
            sec5_billion=args.sec5_billion,
        )
        rows.append(m)
        prev = m
        print(f"[{dt}] max={m.max_level} N={m.total_stocks} T1={m.T1_pct:.1f}% P_ge2={m.Purity_ge2_pct:.1f}% "
              f"sec5={m.sector_top5_sum_yi:.1f}亿 align={m.align_top3_top5_count} div_days={m.consecutive_divergence_days}")

    write_tsv(rows, args.output_tsv, append=True)
    print(f"\n写入 {len(rows)} 天 -> {args.output_tsv}")


if __name__ == "__main__":
    main()
