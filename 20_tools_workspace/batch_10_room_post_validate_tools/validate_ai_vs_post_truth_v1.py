"""
validate_ai_vs_post_truth_v1.py
作用（Step 2 你填完真值CSV+AI出完3格之后直接跑）：
  1. 读 post_truth_YYYYMMDD.csv（你填完的客观真值：每间房TOP5代码T+1/T+2实际涨跌幅/连板天数）
  2. 读每家AI的3格判断输出（JSON格式，在旧仓90区 02_ai_outputs_per_vendor/<vendor_name>/ 下的 ai_judgements.json）
  3. 按 README 里的 3.1/3.2/3.3 客观公式，算每家AI 每间房 每格的对/错/半对，再算 情绪/风格/节奏 准确率，最后算加权总分（情绪40%+风格30%+节奏30%）
  4. 输出：每家AI总分排名表 + 每格准确率排名 + 哪类判断最准的经验表（后面Step3凑100条经验用）
用法：
  python validate_ai_vs_post_truth_v1.py --trade-date 20260811 \
    --truth-csv ./post_truth_20260811_filled.csv \
    --ai-outputs-root D:/Stock/trading_assistant/90_SCRATCH_AND_TEST_ZONE/batch_10_multi_ai_room_classifier__20260813/02_ai_outputs_per_vendor \
    --rooms 复盘哥,独家老师5号,格兰投研 \
    --apply
注意：
  - 只算客观分，不讨论；AI判断是啥就是啥，真值是啥就是啥
  - 3格的判断区间规则写在 README.md §3.1~3.3，和代码完全一致
  - 不会反向覆盖新仓正式MD；结果只打印 stdout + 输出 CSV 在当前目录 result_ai_accuracy_YYYYMMDD.csv
"""
from __future__ import annotations
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


STYLE_EXPECT = ["打板", "低吸", "埋伏", "轮动"]
RHYTHM_EXPECT = ["高位接力", "中位", "首板", "观望"]
MOOD_EXPECT = ["强多", "多", "稍多", "震荡中性", "稍空", "空", "强空"]


def load_truth_csv(p: Path) -> dict[str, list[dict]]:
    """返回 room_name -> [5行 Top5 代码的真值字典]"""
    rows_by_room: dict[str, list[dict]] = defaultdict(list)
    with p.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rn = (r.get("room_name") or "").strip()
            if not rn:
                continue
            def _f(key: str) -> float | None:
                s = (r.get(key) or "").strip()
                if not s:
                    return None
                try:
                    return float(s.replace("%", ""))
                except Exception:
                    return None
            def _i(key: str) -> int | None:
                s = (r.get(key) or "").strip()
                if not s:
                    return None
                try:
                    return int(float(s))
                except Exception:
                    return None
            rows_by_room[rn].append({
                "rank": int(r.get("rank_in_room_top5") or 0),
                "code": (r.get("stock_code_6d") or "").strip(),
                "t1_close_pct": _f("T_plus_1_close_pct"),
                "t2_close_pct": _f("T_plus_2_close_pct"),
                "t1_high_pct": _f("T_plus_1_intraday_high_pct"),
                "consecutive_up_days": _i("consecutive_limit_up_days"),
            })
    for k in rows_by_room:
        rows_by_room[k].sort(key=lambda x: x["rank"])
    return dict(rows_by_room)


def avg(lst: list[float]) -> float | None:
    lst = [x for x in lst if x is not None]
    if not lst:
        return None
    return sum(lst) / float(len(lst))


def expect_mood(avg_t1_close_pct: float | None) -> str:
    if avg_t1_close_pct is None:
        return "震荡中性"
    if avg_t1_close_pct >= +2.5: return "强多"
    if avg_t1_close_pct >= +0.8: return "多"
    if avg_t1_close_pct >= +0.3: return "稍多"
    if avg_t1_close_pct <= -2.5: return "强空"
    if avg_t1_close_pct <= -0.8: return "空"
    if avg_t1_close_pct <= -0.3: return "稍空"
    return "震荡中性"


def expect_style(rows: list[dict]) -> str:
    t1_high = [r["t1_high_pct"] for r in rows]
    t1_close = [r["t1_close_pct"] for r in rows]
    consec = [r["consecutive_up_days"] or 0 for r in rows]
    avg_t1h = avg(t1_high)
    avg_t1c = avg(t1_close)
    max_consec = max(consec) if consec else 0
    if avg_t1h is not None and (avg_t1h >= +8.0 or max_consec >= 2):
        return "打板"
    if avg_t1h is not None and avg_t1c is not None and (+3.0 <= avg_t1h <= +7.0) and (avg_t1c <= +2.0):
        return "低吸"
    t2_close = [r["t2_close_pct"] for r in rows]
    avg_t2c = avg(t2_close)
    if (avg_t1h is None or avg_t1h < +3.0) and avg_t2c is not None and avg_t2c >= +3.0:
        return "埋伏"
    # 分散→轮动：t1_high差距大或命中3个不同档
    nums = [x for x in t1_high if x is not None]
    if len(nums) >= 3:
        buckets = 0
        if any(n >= +5.0 for n in nums): buckets += 1
        if any(+1.0 <= n < +5.0 for n in nums): buckets += 1
        if any(n < +1.0 for n in nums): buckets += 1
        if buckets >= 3: return "轮动"
    return "轮动"


def expect_rhythm(rows: list[dict]) -> str:
    consec = [r["consecutive_up_days"] or 0 for r in rows]
    max_consec = max(consec) if consec else 0
    t1_high = [r["t1_high_pct"] for r in rows]
    avg_t1h = avg(t1_high)
    if max_consec >= 3:
        return "高位接力"
    if max_consec == 2:
        return "中位"
    if max_consec == 1 and avg_t1h is not None and avg_t1h >= +4.0:
        return "首板"
    if (avg_t1h is None or avg_t1h < +2.0) and max_consec == 0:
        return "观望"
    # 模糊兜底
    if max_consec >= 2:
        return "中位"
    return "首板"


# 简化版半对/对/错映射成数值分：1/0.5/0
def score_class(ai_label: str, expect_label: str, labels: list[str]) -> tuple[float, str]:
    ai = (ai_label or "").strip()
    gt = (expect_label or "").strip()
    if not ai or not gt:
        return 0.0, "EMPTY_AI_OR_GT"
    if ai == gt:
        return 1.0, "CORRECT"
    # 找索引距离
    try:
        i_ai = labels.index(ai)
    except ValueError:
        # 情绪格可能命中子串：多稍多=同方向算半对
        i_ai = -1
    try:
        i_gt = labels.index(gt)
    except ValueError:
        i_gt = -1
    if i_ai >= 0 and i_gt >= 0 and abs(i_ai - i_gt) == 1:
        return 0.5, "HALF_CORRECT_NEAR"
    # 情绪同方向：多/稍多/强多 就算半对，空/稍空/强空 就算半对
    mood_pos = {"强多", "多", "稍多"}
    mood_neg = {"强空", "空", "稍空"}
    if {ai, gt} <= mood_pos or {ai, gt} <= mood_neg:
        return 0.5, "HALF_CORRECT_SAME_DIRECTION"
    return 0.0, "WRONG"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trade-date", required=True)
    ap.add_argument("--truth-csv", required=True)
    ap.add_argument("--ai-outputs-root", required=True)
    ap.add_argument("--rooms", required=True, help="逗号分隔房间列表，先3间样板房")
    ap.add_argument("--apply", action="store_true", help="写 result_ai_accuracy_YYYYMMDD.csv")
    args = ap.parse_args()
    truth_path = Path(args.truth_csv).resolve()
    ai_root = Path(args.ai_outputs_root).resolve()
    rooms = [x.strip() for x in args.rooms.split(",") if x.strip()]
    td = args.trade_date
    print(f"=== Step2 多AI vs 后验真值 打分（{td}，房间={rooms}）===")
    print(f"真值CSV：{truth_path}")
    print(f"AI输出根目录：{ai_root}")
    truth = load_truth_csv(truth_path)
    # 每间房算一次 期望情绪/风格/节奏（从真值算，不是AI）
    room_expect: dict[str, dict[str, str]] = {}
    for r in rooms:
        rows = truth.get(r) or []
        t1_close_pcts = [x["t1_close_pct"] for x in rows]
        avg_t1c = avg(t1_close_pcts)
        exp_m = expect_mood(avg_t1c)
        exp_s = expect_style(rows)
        exp_r = expect_rhythm(rows)
        room_expect[r] = {"情绪": exp_m, "风格": exp_s, "节奏": exp_r}
        print(f"  [{r:<12}] 真值期望→情绪:{exp_m:<6} 风格:{exp_s:<4} 节奏:{exp_r:<4}  (Top5平均T+1收盘涨跌={avg_t1c if avg_t1c is not None else '空'}%)")
    # 读每家AI输出：要求每家目录下放 ai_judgements.json，格式={房间名:{"情绪":"...","风格":"...","节奏":"...","理由":"..."}}
    vendor_dirs = [d for d in ai_root.iterdir() if d.is_dir()] if ai_root.exists() else []
    vendor_dirs.sort()
    if not vendor_dirs:
        print(f"WARN：在 {ai_root} 下面没找到厂商AI输出目录（应该每个厂商一个子目录，里面放 ai_judgements.json）")
        print("参考：02_ai_outputs_per_vendor/GPT4o/ai_judgements.json  内容格式样例：{")
        print('  "复盘哥":{"情绪":"多","风格":"打板","节奏":"中位","理由":"TOP5=分歧龙头算力医药 → 情绪偏暖连板多"}')
        print("}")
        return 0
    all_rows: list[dict] = []
    for vd in vendor_dirs:
        vendor = vd.name
        jf = vd / "ai_judgements.json"
        if not jf.exists():
            print(f"SKIP 厂商[{vendor}]：缺少 ai_judgements.json → 跳过")
            continue
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"SKIP 厂商[{vendor}]：解析失败 {e} → 跳过")
            continue
        mood_scores: list[float] = []
        style_scores: list[float] = []
        rhythm_scores: list[float] = []
        per_room: list[str] = []
        for r in rooms:
            judg = data.get(r) or {}
            ai_m = str(judg.get("情绪") or judg.get("mood") or "")
            ai_s = str(judg.get("风格") or judg.get("style") or "")
            ai_r = str(judg.get("节奏") or judg.get("rhythm") or "")
            exp = room_expect[r]
            ms, mtag = score_class(ai_m, exp["情绪"], MOOD_EXPECT)
            ss, stag = score_class(ai_s, exp["风格"], STYLE_EXPECT)
            rs, rtag = score_class(ai_r, exp["节奏"], RHYTHM_EXPECT)
            mood_scores.append(ms); style_scores.append(ss); rhythm_scores.append(rs)
            per_room.append(f"{r}:情绪{ms}({mtag})/风格{ss}({stag})/节奏{rs}({rtag})")
        avg_m = avg(mood_scores) or 0.0
        avg_s = avg(style_scores) or 0.0
        avg_r = avg(rhythm_scores) or 0.0
        total = round(0.4 * avg_m + 0.3 * avg_s + 0.3 * avg_r, 4)
        print(f"厂商[{vendor:<18}] → 情绪准确率={round(avg_m,3):<5} 风格={round(avg_s,3):<5} 节奏={round(avg_r,3):<5} 加权总分={total:<6}")
        for pr in per_room:
            print(f"   · {pr}")
        all_rows.append({
            "vendor": vendor,
            "mood_acc": round(avg_m, 4),
            "style_acc": round(avg_s, 4),
            "rhythm_acc": round(avg_r, 4),
            "weighted_total": total,
            "room_details": " | ".join(per_room),
        })
    all_rows.sort(key=lambda x: x["weighted_total"], reverse=True)
    print("")
    print("=== 排名（加权总分高→低）===")
    for i, r in enumerate(all_rows, 1):
        print(f"  第{i}名  {r['vendor']:<18} 总分={r['weighted_total']:<6} 情绪={r['mood_acc']:<5} 风格={r['style_acc']:<5} 节奏={r['rhythm_acc']:<5}")
    if args.apply and all_rows:
        out_csv = truth_path.parent / f"result_ai_accuracy_{td}.csv"
        fieldnames = ["vendor", "mood_acc", "style_acc", "rhythm_acc", "weighted_total", "room_details"]
        with out_csv.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for r in all_rows:
                w.writerow(r)
        print(f"WROTE 结果表：{out_csv}")
    elif not args.apply:
        print("(DRY_RUN：加 --apply 才写 result CSV，现在只打印)")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
