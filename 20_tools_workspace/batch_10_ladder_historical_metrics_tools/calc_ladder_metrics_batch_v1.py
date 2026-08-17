# -*- coding: utf-8 -*-
"""batch 历史日批量算连板天梯结构指标（P1/P3 用）。

公式 100% 照搬冻结合同，不另开算法：
- A5_连板天梯盘后3分钟怎么看 7.1-7.6
- A5_最小字段合同 7.2 冻结公式 + 7.3 缺字段兜底
- 旧仓 calc_810_metrics.py 单日 DI/Purity/T1/T3/对齐度/风险档 逻辑
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_QUICKTINY = REPO_ROOT / "02_runtime" / "quicktiny_capture"
DEFAULT_OUTPUT_TSV = DEFAULT_QUICKTINY / "metrics_history.tsv"

UTC8 = timezone(timedelta(hours=8))

LADDER_NAME_RE = re.compile(r"ladder_day_min(?:__|_)(\d{8})\.json$", re.IGNORECASE)
SECTOR_NAME_RE = re.compile(
    r"sector_capital_flow_(?:snapshot|min)(?:__|_)(\d{8})\.json$",
    re.IGNORECASE,
)

# dry-run 与 calc_810_metrics.py 对 20260810 的对照金标（一位小数口径）
GOLDEN_20260810: dict[str, Any] = {
    "date": "20260810",
    "max_level": 5,
    "total_stocks": 99,
    "ge2_stocks": 13,
    "first_panel_count": 86,
    "T1_dynamic_threshold": 20.0,
    "T1_pct": 12.1,
    "T3_pct": 23.2,
    "Purity_ge2_pct": 61.5,
    "sector_top5_sum_yi": 72.5,
    "align_top3_top5_count": 0,
    "top4_di_list": "0,15,0,12",
    "top4_risk_list": "G,R,Y,R",
}

TSV_COLUMNS: list[str] = [
    "date",
    "max_level",
    "total_stocks",
    "ge2_stocks",
    "first_panel_count",
    "T1_dynamic_threshold",
    "T1_pct",
    "T3_pct",
    "Purity_ge2_pct",
    "sector_top5_sum_yi",
    "align_top3_top5_count",
    "consecutive_divergence_days",
    "top4_di_list",
    "top4_risk_list",
    "p1_position_advice",
    "fake_strength_warning",
]


@dataclass
class StockRow:
    """单只连板标的的展平行，便于跨 board 汇总。"""

    code: str
    name: str
    level: int
    continue_num: int
    primary_theme: str
    limit_up_type: str
    open_num: int
    trading_amount: float | None
    order_amount: float | None
    turnover_rate: float | None
    first_limit_up_time: str | None


@dataclass
class DayMetrics:
    """单日全部冻结指标 + 跨日字段（后填）。"""

    date: str
    max_level: int
    total_stocks: int
    ge2_stocks: int
    first_panel_count: int
    T1_dynamic_threshold: float
    T1_pct: float
    T3_pct: float
    Purity_ge2_pct: float
    sector_top5_sum_yi: float
    align_top3_top5_count: int
    top3_themes: list[str] = field(default_factory=list)
    sector_top5_names: list[str] = field(default_factory=list)
    top4_di_list: str = ""
    top4_risk_list: str = ""
    consecutive_divergence_days: int = 0
    p1_position_advice: str = ""
    fake_strength_warning: str = "0"
    purity_ge2_avg3: float | None = None
    is_divergence_day: bool = False
    ladder_mood: str = "中"
    sector_mood: str = "中"


def load_json(path: Path) -> Any:
    """读 JSON 文件；path 存在是为了调用方不在本函数内决定默认仓路径。"""
    return json.loads(path.read_text(encoding="utf-8"))


def safe_float(value: Any) -> float | None:
    """允许合同 recommend 字段缺失时返回 None，而不是崩或误写成 0。"""
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def safe_int(value: Any, default: int = 0) -> int:
    """open_num 等：null/缺省按 default（合同 7.3 没开板=0）。"""
    if value is None or value == "":
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def theme_of(stock: Mapping[str, Any]) -> str:
    """primary_theme 缺失时用 UNKNOWN，避免 Counter 把 None 当成合法题材键。"""
    raw = stock.get("primary_theme")
    if raw is None or str(raw).strip() == "":
        return "UNKNOWN"
    return str(raw).strip()


def di_level_of(stock: Mapping[str, Any], board_level: int) -> int:
    """DI 用板高：continue_num 优先，否则 level（合同 7.3）。"""
    cont = stock.get("continue_num")
    if cont is not None and cont != "":
        try:
            return int(cont)
        except (TypeError, ValueError):
            pass
    lv = stock.get("level")
    if lv is not None and lv != "":
        try:
            return int(lv)
        except (TypeError, ValueError):
            pass
    return int(board_level)


def flatten_ladder(ladder: Mapping[str, Any]) -> tuple[str, list[StockRow]]:
    """把 ladder min JSON 压成 (date, stocks[])，统一 board.level 与缺字段兜底。"""
    dates = ladder.get("dates") or []
    if not dates:
        raise ValueError("ladder JSON 缺少 dates[]")
    day = dates[0]
    date_key = str(day.get("date") or "").strip()
    if not re.fullmatch(r"\d{8}", date_key):
        raise ValueError(f"无法解析 ladder 日期: {date_key!r}")

    stocks: list[StockRow] = []
    for board in day.get("boards") or []:
        board_level = safe_int(board.get("level"), default=0)
        for s in board.get("stocks") or []:
            if not isinstance(s, Mapping):
                continue
            open_raw = s.get("open_num")
            # 合同 7.3：null/缺失 = 0，不当成崩
            open_num = 0 if open_raw is None or open_raw == "" else safe_int(open_raw, 0)
            stocks.append(
                StockRow(
                    code=str(s.get("code") or ""),
                    name=str(s.get("name") or ""),
                    level=board_level if board_level else safe_int(s.get("level"), 0),
                    continue_num=di_level_of(s, board_level),
                    primary_theme=theme_of(s),
                    limit_up_type=str(s.get("limit_up_type") or ""),
                    open_num=open_num,
                    trading_amount=safe_float(s.get("trading_amount")),
                    order_amount=safe_float(s.get("order_amount", s.get("amount"))),
                    turnover_rate=safe_float(s.get("turnover_rate")),
                    first_limit_up_time=(
                        None
                        if s.get("first_limit_up_time") in (None, "")
                        else str(s.get("first_limit_up_time"))
                    ),
                )
            )
    return date_key, stocks


def extract_sector_rows(sector: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    """兼容 snapshot 顶层 rows / data.rows / records 三种壳。"""
    if isinstance(sector.get("rows"), list):
        return list(sector["rows"])
    data = sector.get("data")
    if isinstance(data, Mapping) and isinstance(data.get("rows"), list):
        return list(data["rows"])
    if isinstance(sector.get("records"), list):
        return list(sector["records"])
    return []


def sector_name_of(row: Mapping[str, Any]) -> str:
    """板块名多键兼容；无名字段时占位，避免对齐度比较漏掉整行。"""
    for key in ("sectorName", "plateNameCn", "themeName", "name"):
        v = row.get(key)
        if v is not None and str(v).strip():
            return str(v).strip()
    return "?"


def sector_top5(sector: Mapping[str, Any]) -> tuple[list[str], list[float], float]:
    """按 mainNetAmount 降序取前 5（与 snapshot/calc_810 首 5 行一致，不用绝对值）。"""
    rows = extract_sector_rows(sector)
    scored: list[tuple[str, float]] = []
    for r in rows:
        if not isinstance(r, Mapping):
            continue
        amt = safe_float(r.get("mainNetAmount"))
        if amt is None:
            amt = 0.0
        scored.append((sector_name_of(r), float(amt)))
    scored.sort(key=lambda x: x[1], reverse=True)
    top = scored[:5]
    names = [n for n, _ in top]
    amounts = [a for _, a in top]
    total = float(sum(amounts))
    return names, amounts, total


def t1_dynamic_threshold(first_panel_count: int) -> float:
    """Kimi 冻结动态阈值：首板>80→20；<60→30；中间→25。"""
    if first_panel_count > 80:
        return 20.0
    if first_panel_count < 60:
        return 30.0
    return 25.0


def concentration_pct(counter: Counter[str], n_total: int, top_n: int) -> float:
    """TopN 题材数 / 总数 ×100；n_total=0 时返回 0 不除零。"""
    if n_total <= 0 or not counter:
        return 0.0
    top = counter.most_common(top_n)
    return sum(c for _, c in top) / n_total * 100.0


def purity_ge2_pct(stocks: Sequence[StockRow]) -> tuple[float, int]:
    """GLM 强制 ≥2 板纯度：Top1(≥2) / ≥2 总数 ×100。"""
    ge2 = [s for s in stocks if s.level >= 2]
    n = len(ge2)
    if n == 0:
        return 0.0, 0
    c = Counter(s.primary_theme for s in ge2)
    return concentration_pct(c, n, 1), n


def align_count(top3_themes: Sequence[str], sector_top5_names: Sequence[str]) -> int:
    """DeepSeek 方向对齐度：天梯 Top3 与 sector 前5 字面互相包含；初版无同义词字典。"""
    names = list(sector_top5_names)
    hit = 0
    for th in top3_themes:
        if any(th in n or n in th for n in names):
            hit += 1
    return hit


def seal_ratio_of(stock: StockRow) -> float | None:
    """封单比；任一金额缺失 → None（风险合成跳过封单条件，合同 7.3）。"""
    if stock.order_amount is None or stock.trading_amount is None:
        return None
    if stock.trading_amount == 0:
        return None
    return abs(stock.order_amount) / abs(stock.trading_amount)


def divergence_index(stock: StockRow) -> int:
    """Kimi DI = (open_num or 0) × level(continue_num 优先)。"""
    return int(stock.open_num) * int(stock.continue_num)


def risk_grade(stock: StockRow) -> str:
    """R/Y/G：复用 calc_810 阈值；缺封单/换率时按合同 7.3 跳过该条件。"""
    di = divergence_index(stock)
    seal = seal_ratio_of(stock)
    tr = stock.turnover_rate

    is_r = False
    if seal is not None and seal < 0.3:
        is_r = True
    if di > 10:
        is_r = True
    if tr is not None and tr > 25:
        is_r = True
    if is_r:
        return "R"

    is_y = False
    if seal is not None and seal < 1:
        is_y = True
    if di >= 5:
        is_y = True
    if tr is not None and tr > 15:
        is_y = True
    if is_y:
        return "Y"
    return "G"


def top4_high_metrics(stocks: Sequence[StockRow]) -> tuple[str, str]:
    """≥3 板高标按源序取前 4，输出 DI/风险串（对齐 calc_810 打印顺序）。"""
    high = [s for s in stocks if s.level >= 3][:4]
    di_list = ",".join(str(divergence_index(s)) for s in high)
    risk_list = ",".join(risk_grade(s) for s in high)
    return di_list, risk_list


def ladder_mood_of(total_stocks: int, max_level: int) -> str:
    """天梯情绪档：高(>100 或最高≥5) / 低(<60 且最高≤3) / 其他中。"""
    if total_stocks > 100 or max_level >= 5:
        return "高"
    if total_stocks < 60 and max_level <= 3:
        return "低"
    return "中"


def sector_mood_of(top5_sum_yi: float) -> str:
    """sector 资金档：高(>300亿) / 低(<100亿) / 其他中。"""
    if top5_sum_yi > 300:
        return "高"
    if top5_sum_yi < 100:
        return "低"
    return "中"


def round1(x: float) -> float:
    """统一保留 1 位小数，与 calc_810 打印口径一致。"""
    return round(float(x) + 1e-12, 1)


def compute_day_metrics(ladder: Mapping[str, Any], sector: Mapping[str, Any]) -> DayMetrics:
    """单日全量指标；跨日字段由 enrich_cross_day 后填。"""
    date_key, stocks = flatten_ladder(ladder)
    n = len(stocks)
    level_counter = Counter(s.level for s in stocks)
    max_level = max(level_counter.keys()) if level_counter else 0
    first_panel = level_counter.get(1, 0)

    theme_all: Counter[str] = Counter(s.primary_theme for s in stocks)
    t1 = concentration_pct(theme_all, n, 1)
    t3 = concentration_pct(theme_all, n, 3)
    top3_themes = [t for t, _ in theme_all.most_common(3)]
    purity, n_ge2 = purity_ge2_pct(stocks)
    thr = t1_dynamic_threshold(first_panel)

    s_names, _s_amts, s_total = sector_top5(sector)
    s_yi = s_total / 1e8
    align = align_count(top3_themes, s_names)
    di_s, risk_s = top4_high_metrics(stocks)

    l_mood = ladder_mood_of(n, max_level)
    s_mood = sector_mood_of(s_yi)
    # Kimi：天梯热 × sector 低分散 × 对齐度 0 → 背离日
    is_div = l_mood == "高" and s_mood == "低" and align == 0

    return DayMetrics(
        date=date_key,
        max_level=max_level,
        total_stocks=n,
        ge2_stocks=n_ge2,
        first_panel_count=first_panel,
        T1_dynamic_threshold=thr,
        T1_pct=round1(t1),
        T3_pct=round1(t3),
        Purity_ge2_pct=round1(purity),
        sector_top5_sum_yi=round1(s_yi),
        align_top3_top5_count=align,
        top3_themes=top3_themes,
        sector_top5_names=s_names,
        top4_di_list=di_s,
        top4_risk_list=risk_s,
        is_divergence_day=is_div,
        ladder_mood=l_mood,
        sector_mood=s_mood,
    )


def enrich_cross_day(days: list[DayMetrics]) -> None:
    """跨日：背离连续天数、假强警示、Purity≥2 的 3 日滚动平均、仓位建议。"""
    days_sorted = sorted(days, key=lambda d: d.date)
    for i, d in enumerate(days_sorted):
        # 3 日滚动 Purity 平均（仅满 3 日写数值；不足 None）
        window = days_sorted[max(0, i - 2) : i + 1]
        if len(window) == 3:
            d.purity_ge2_avg3 = round1(sum(x.Purity_ge2_pct for x in window) / 3.0)
        else:
            d.purity_ge2_avg3 = None

        # 连续背离：从当日往前回溯 is_divergence_day
        consec = 0
        j = i
        while j >= 0 and days_sorted[j].is_divergence_day:
            consec += 1
            j -= 1
        d.consecutive_divergence_days = consec

        # 假强：前5合计 <100亿 且 今最高板 > 昨最高板
        prev_max = days_sorted[i - 1].max_level if i > 0 else None
        if prev_max is not None and d.sector_top5_sum_yi < 100 and d.max_level > prev_max:
            d.fake_strength_warning = "1"
        else:
            d.fake_strength_warning = "0"

        d.p1_position_advice = position_advice(d)


def position_advice(d: DayMetrics) -> str:
    """矩阵格翻译为仓位态度；连续≥3 天背离强制休息（Kimi）。"""
    if d.consecutive_divergence_days >= 3:
        return "休息"
    # 结构-资金粗矩阵
    if d.ladder_mood == "高" and d.sector_mood == "高" and d.align_top3_top5_count >= 2:
        base = "积极"
    elif d.is_divergence_day or d.align_top3_top5_count == 0 and d.sector_mood == "低":
        base = "谨慎"
    elif d.ladder_mood == "低" and d.sector_mood == "低":
        base = "休息"
    else:
        base = "中性"

    if d.fake_strength_warning == "1":
        # 假强触发仓位降 1 档
        down = {"积极": "中性", "中性": "谨慎", "谨慎": "休息", "休息": "休息"}
        base = down[base]
    return base


def discover_by_date(
    root: Path,
    name_re: re.Pattern[str],
) -> dict[str, Path]:
    """在 root 下递归找 YYYYMMDD 命名文件；同日多份时优先 daily_snapshots 路径。"""
    found: dict[str, list[Path]] = {}
    if not root.exists():
        return {}
    for p in root.rglob("*.json"):
        m = name_re.search(p.name)
        if not m:
            continue
        # 跳过 meta
        if p.name.endswith(".meta.json"):
            continue
        found.setdefault(m.group(1), []).append(p)

    preferred_sub = ("daily_snapshots", "derived", "00_raw")
    out: dict[str, Path] = {}
    for date_key, paths in found.items():
        def rank(path: Path) -> tuple[int, int, str]:
            s = str(path).replace("\\", "/").lower()
            for i, token in enumerate(preferred_sub):
                if token in s:
                    return (i, len(s), s)
            return (len(preferred_sub), len(s), s)

        paths_sorted = sorted(paths, key=rank)
        out[date_key] = paths_sorted[0]
    return out


def resolve_file_map(
    ladder_dir: Path | None,
    sector_dir: Path | None,
    auto_root: Path,
) -> tuple[dict[str, Path], dict[str, Path]]:
    """ladder/sector 目录可显式传入；None 时在 auto_root 下自动搜各 batch。"""
    if ladder_dir is not None:
        ladder_map = discover_by_date(ladder_dir, LADDER_NAME_RE)
        # 非递归时也扫一层直接文件
        if not ladder_map and ladder_dir.is_dir():
            for p in ladder_dir.glob("*.json"):
                m = LADDER_NAME_RE.search(p.name)
                if m:
                    ladder_map[m.group(1)] = p
    else:
        ladder_map = discover_by_date(auto_root, LADDER_NAME_RE)

    if sector_dir is not None:
        sector_map = discover_by_date(sector_dir, SECTOR_NAME_RE)
        if not sector_map and sector_dir.is_dir():
            for p in sector_dir.glob("*.json"):
                m = SECTOR_NAME_RE.search(p.name)
                if m:
                    sector_map[m.group(1)] = p
    else:
        sector_map = discover_by_date(auto_root, SECTOR_NAME_RE)

    return ladder_map, sector_map


def filter_dates(
    dates: Iterable[str],
    start_date: str | None,
    end_date: str | None,
) -> list[str]:
    """可选 YYYYMMDD 闭区间过滤。"""
    out: list[str] = []
    for d in sorted(set(dates)):
        if start_date and d < start_date:
            continue
        if end_date and d > end_date:
            continue
        out.append(d)
    return out


def metrics_to_row(d: DayMetrics) -> dict[str, str]:
    """DayMetrics → TSV 行（全字符串，保证 header 稳定）。"""
    return {
        "date": d.date,
        "max_level": str(d.max_level),
        "total_stocks": str(d.total_stocks),
        "ge2_stocks": str(d.ge2_stocks),
        "first_panel_count": str(d.first_panel_count),
        "T1_dynamic_threshold": f"{d.T1_dynamic_threshold:.1f}",
        "T1_pct": f"{d.T1_pct:.1f}",
        "T3_pct": f"{d.T3_pct:.1f}",
        "Purity_ge2_pct": f"{d.Purity_ge2_pct:.1f}",
        "sector_top5_sum_yi": f"{d.sector_top5_sum_yi:.1f}",
        "align_top3_top5_count": str(d.align_top3_top5_count),
        "consecutive_divergence_days": str(d.consecutive_divergence_days),
        "top4_di_list": d.top4_di_list,
        "top4_risk_list": d.top4_risk_list,
        "p1_position_advice": d.p1_position_advice,
        "fake_strength_warning": d.fake_strength_warning,
    }


def write_tsv(path: Path, rows: Sequence[Mapping[str, str]]) -> None:
    """存在则 append（不写 header）；不存在则写 header。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists() or path.stat().st_size == 0
    with path.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=TSV_COLUMNS, delimiter="\t", lineterminator="\n")
        if write_header:
            w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in TSV_COLUMNS})


def pct_close(a: float, b: float, tol_pct: float = 0.1) -> bool:
    """相对误差 ≤ tol_pct% 或绝对误差在 0.1 一位小数口径内。"""
    if abs(a - b) <= 0.05 + 1e-9:
        return True
    base = max(abs(b), 1e-9)
    return abs(a - b) / base * 100.0 <= tol_pct


def run_dry_run(
    ladder_path: Path,
    sector_path: Path,
) -> int:
    """用 8/10 真实 JSON 与 calc_810 / 冻结样例对齐；差 >0.1% 则非 0 退出。"""
    if not ladder_path.is_file():
        print(f"[dry-run] missing ladder: {ladder_path}", file=sys.stderr)
        return 2
    if not sector_path.is_file():
        print(f"[dry-run] missing sector: {sector_path}", file=sys.stderr)
        return 2

    m = compute_day_metrics(load_json(ladder_path), load_json(sector_path))
    enrich_cross_day([m])

    errors: list[str] = []
    checks: list[tuple[str, float | int | str, float | int | str]] = [
        ("date", m.date, GOLDEN_20260810["date"]),
        ("max_level", m.max_level, GOLDEN_20260810["max_level"]),
        ("total_stocks", m.total_stocks, GOLDEN_20260810["total_stocks"]),
        ("ge2_stocks", m.ge2_stocks, GOLDEN_20260810["ge2_stocks"]),
        ("first_panel_count", m.first_panel_count, GOLDEN_20260810["first_panel_count"]),
        ("T1_dynamic_threshold", m.T1_dynamic_threshold, GOLDEN_20260810["T1_dynamic_threshold"]),
        ("T1_pct", m.T1_pct, GOLDEN_20260810["T1_pct"]),
        ("T3_pct", m.T3_pct, GOLDEN_20260810["T3_pct"]),
        ("Purity_ge2_pct", m.Purity_ge2_pct, GOLDEN_20260810["Purity_ge2_pct"]),
        ("sector_top5_sum_yi", m.sector_top5_sum_yi, GOLDEN_20260810["sector_top5_sum_yi"]),
        ("align_top3_top5_count", m.align_top3_top5_count, GOLDEN_20260810["align_top3_top5_count"]),
        ("top4_di_list", m.top4_di_list, GOLDEN_20260810["top4_di_list"]),
        ("top4_risk_list", m.top4_risk_list, GOLDEN_20260810["top4_risk_list"]),
    ]

    for name, got, exp in checks:
        if isinstance(exp, (int, float)) and not isinstance(exp, bool) and isinstance(got, (int, float)):
            if not pct_close(float(got), float(exp), 0.1):
                errors.append(f"{name}: got={got} expected={exp} (tol 0.1%)")
        else:
            if str(got) != str(exp):
                errors.append(f"{name}: got={got!r} expected={exp!r}")

    print("=== dry-run 20260810 ===")
    row = metrics_to_row(m)
    for k in TSV_COLUMNS:
        print(f"  {k}: {row[k]}")
    if m.purity_ge2_avg3 is not None:
        print(f"  purity_ge2_avg3(internal): {m.purity_ge2_avg3}")
    else:
        print("  purity_ge2_avg3(internal): <3 days window, None")

    if errors:
        print("[dry-run] FAIL", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("[dry-run] PASS — matches calc_810_metrics / frozen 8/10 sample")
    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    """CLI：路径全由参数进入，不在业务函数里写死绝对盘符。"""
    p = argparse.ArgumentParser(
        description="批量计算连板天梯结构指标（T1/T3/Purity/DI/对齐度/背离天数）并 append 到 TSV",
    )
    p.add_argument(
        "--ladder-dir",
        type=Path,
        default=None,
        help="ladder_day_min_*.json 所在目录；默认在 02_runtime/quicktiny_capture 下自动搜",
    )
    p.add_argument(
        "--sector-dir",
        type=Path,
        default=None,
        help="sector_snapshot_*.json 所在目录；默认同上自动搜",
    )
    p.add_argument(
        "--output-tsv",
        type=Path,
        default=DEFAULT_OUTPUT_TSV,
        help=f"输出 TSV（默认 {DEFAULT_OUTPUT_TSV}）；存在则 append",
    )
    p.add_argument("--start-date", type=str, default=None, help="起始日 YYYYMMDD（含）")
    p.add_argument("--end-date", type=str, default=None, help="结束日 YYYYMMDD（含）")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="只对 8/10 真实 JSON 做金标校验，不写 TSV",
    )
    p.add_argument(
        "--ladder-file",
        type=Path,
        default=None,
        help="dry-run 时指定 ladder 单文件；默认 ladder_daily_snapshots/8/10",
    )
    p.add_argument(
        "--sector-file",
        type=Path,
        default=None,
        help="dry-run 时指定 sector 单文件；默认 sector_daily_snapshots/8/10",
    )
    p.add_argument(
        "--auto-root",
        type=Path,
        default=DEFAULT_QUICKTINY,
        help="未传 ladder-dir/sector-dir 时的递归搜索根",
    )
    return p


def main(argv: Sequence[str] | None = None) -> int:
    """入口：dry-run 走金标；否则扫日、算指标、append TSV。"""
    args = build_arg_parser().parse_args(list(argv) if argv is not None else None)

    if args.dry_run:
        ladder_file = args.ladder_file or (
            DEFAULT_QUICKTINY / "ladder_daily_snapshots" / "ladder_day_min__20260810.json"
        )
        sector_file = args.sector_file or (
            DEFAULT_QUICKTINY
            / "sector_daily_snapshots"
            / "sector_capital_flow_snapshot__20260810.json"
        )
        return run_dry_run(ladder_file, sector_file)

    ladder_map, sector_map = resolve_file_map(args.ladder_dir, args.sector_dir, args.auto_root)
    common = sorted(set(ladder_map) & set(sector_map))
    common = filter_dates(common, args.start_date, args.end_date)
    if not common:
        print(
            f"no paired dates under ladder={args.ladder_dir or args.auto_root} "
            f"sector={args.sector_dir or args.auto_root}",
            file=sys.stderr,
        )
        return 2

    day_metrics: list[DayMetrics] = []
    for d in common:
        try:
            m = compute_day_metrics(load_json(ladder_map[d]), load_json(sector_map[d]))
        except Exception as exc:  # noqa: BLE001 — 单日失败不拖垮整批
            print(f"[skip] {d}: {exc}", file=sys.stderr)
            continue
        if m.date != d:
            # 以文件名日期为准，避免 JSON 内 date 不一致
            m.date = d
        day_metrics.append(m)

    if not day_metrics:
        print("no day metrics produced", file=sys.stderr)
        return 2

    enrich_cross_day(day_metrics)
    rows = [metrics_to_row(m) for m in sorted(day_metrics, key=lambda x: x.date)]
    write_tsv(args.output_tsv, rows)
    print(f"wrote {len(rows)} row(s) → {args.output_tsv}")
    for r in rows:
        print(
            f"  {r['date']}: T1={r['T1_pct']} T3={r['T3_pct']} "
            f"P={r['Purity_ge2_pct']} align={r['align_top3_top5_count']} "
            f"div={r['consecutive_divergence_days']} "
            f"DI=[{r['top4_di_list']}] risk=[{r['top4_risk_list']}]"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
