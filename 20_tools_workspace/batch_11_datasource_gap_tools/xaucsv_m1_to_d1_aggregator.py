import csv
import os
from datetime import datetime
from collections import defaultdict, OrderedDict

CSV_PATH = r"D:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\XAUUSD CSV\XAUUSD CSV\XAUUSD_1 Min_Bid_2003.05.05_2026.04.27.csv"
OUT_DIR = r"D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_datasource_gap__20260811"

OUT_2026Q1 = os.path.join(OUT_DIR, "xauusd_d1_sample_2026Q1__20260811.tsv")
OUT_RANDOM = os.path.join(OUT_DIR, "xauusd_d1_random_sample_23years__20260811.tsv")

SAMPLES_PER_YEAR = 5
TOTAL_EXPECTED = 8322566


def parse_date_fast(s):
    return s[:4] + "-" + s[5:7] + "-" + s[8:10]


def parse_year_fast(s):
    return int(s[:4])


def parse_month_fast(s):
    return s[5:7]


def in_2026q1_fast(s):
    if s < "2026.01.01":
        return False
    if s > "2026.04.27 23:59:59":
        return False
    return True


def aggregate():
    total_lines = 0
    aggregated_lines = 0
    skipped_non_2026q1 = 0
    skipped_errors = 0

    daily_buckets_2026q1 = OrderedDict()

    yearly_sample_buckets = defaultdict(OrderedDict)
    yearly_sample_count = defaultdict(int)

    monthly_stats = defaultdict(lambda: {"days": 0, "total_range": 0.0})

    current_2026q1_key = None
    current_2026q1_agg = None

    yearly_current_key = {}
    yearly_current_bucket = {}

    with open(CSV_PATH, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        total_lines += 1

        last_progress = 0

        for row in reader:
            total_lines += 1

            if len(row) < 6:
                skipped_errors += 1
                continue

            time_str = row[0]
            if len(time_str) < 19:
                skipped_errors += 1
                continue

            try:
                o = float(row[1])
                h = float(row[2])
                l = float(row[3])
                c = float(row[4])
                v = float(row[5])
            except ValueError:
                skipped_errors += 1
                continue

            date_key = parse_date_fast(time_str)
            year = parse_year_fast(time_str)
            in_q1 = in_2026q1_fast(time_str)

            if in_q1:
                aggregated_lines += 1

                if current_2026q1_key != date_key:
                    current_2026q1_key = date_key
                    if date_key not in daily_buckets_2026q1:
                        daily_buckets_2026q1[date_key] = [o, h, l, c, v]
                        current_2026q1_agg = daily_buckets_2026q1[date_key]
                    else:
                        current_2026q1_agg = daily_buckets_2026q1[date_key]
                        current_2026q1_agg[0] = o
                        if h > current_2026q1_agg[1]:
                            current_2026q1_agg[1] = h
                        if l < current_2026q1_agg[2]:
                            current_2026q1_agg[2] = l
                        current_2026q1_agg[3] = c
                        current_2026q1_agg[4] = v
                else:
                    if h > current_2026q1_agg[1]:
                        current_2026q1_agg[1] = h
                    if l < current_2026q1_agg[2]:
                        current_2026q1_agg[2] = l
                    current_2026q1_agg[3] = c
                    current_2026q1_agg[4] += v
            else:
                skipped_non_2026q1 += 1

            if yearly_sample_count[year] < SAMPLES_PER_YEAR:
                if year not in yearly_current_key or yearly_current_key[year] != date_key:
                    yearly_current_key[year] = date_key
                    if date_key not in yearly_sample_buckets[year]:
                        if yearly_sample_count[year] < SAMPLES_PER_YEAR:
                            yearly_sample_buckets[year][date_key] = [date_key, o, h, l, c, v]
                            yearly_sample_count[year] += 1
                            yearly_current_bucket[year] = yearly_sample_buckets[year][date_key]
                        else:
                            yearly_current_bucket[year] = None
                    else:
                        yearly_current_bucket[year] = yearly_sample_buckets[year][date_key]
                        bucket = yearly_current_bucket[year]
                        bucket[1] = o
                        if h > bucket[2]:
                            bucket[2] = h
                        if l < bucket[3]:
                            bucket[3] = l
                        bucket[4] = c
                        bucket[5] = v
                else:
                    bucket = yearly_current_bucket.get(year)
                    if bucket is not None:
                        if h > bucket[2]:
                            bucket[2] = h
                        if l < bucket[3]:
                            bucket[3] = l
                        bucket[4] = c
                        bucket[5] += v

            if total_lines - last_progress >= 1000000:
                pct = total_lines * 100.0 / TOTAL_EXPECTED
                print(f"  进度: {total_lines:,} / {TOTAL_EXPECTED:,} 行 ({pct:.1f}%)")
                last_progress = total_lines

    data_rows_2026q1 = []
    for date_key in sorted(daily_buckets_2026q1.keys()):
        agg = daily_buckets_2026q1[date_key]
        rng = agg[1] - agg[2]
        month_key = "2026-" + parse_month_fast(date_key.replace("-", "."))
        monthly_stats[month_key]["days"] += 1
        monthly_stats[month_key]["total_range"] += rng
        data_rows_2026q1.append(
            (
                date_key,
                f"{agg[0]:.3f}",
                f"{agg[1]:.3f}",
                f"{agg[2]:.3f}",
                f"{agg[3]:.3f}",
                f"{agg[4]:.5f}",
            )
        )

    with open(OUT_2026Q1, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["date", "open", "high", "low", "close", "volume"])
        for row in data_rows_2026q1:
            writer.writerow(row)

    random_sample_rows = []
    for year in sorted(yearly_sample_buckets.keys()):
        for date_key in sorted(yearly_sample_buckets[year].keys()):
            bucket = yearly_sample_buckets[year][date_key]
            random_sample_rows.append(
                (
                    bucket[0],
                    f"{bucket[1]:.3f}",
                    f"{bucket[2]:.3f}",
                    f"{bucket[3]:.3f}",
                    f"{bucket[4]:.3f}",
                    f"{bucket[5]:.5f}",
                )
            )

    with open(OUT_RANDOM, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["date", "open", "high", "low", "close", "volume"])
        for row in random_sample_rows:
            writer.writerow(row)

    print()
    print("=" * 80)
    print("XAUUSD M1 → D1 聚合统计")
    print("=" * 80)
    print(f"CSV 源文件: {CSV_PATH}")
    print(f"总行数（含表头）: {total_lines:,}")
    print(f"实际聚合行数（2026-01-01 ~ 2026-04-27）: {aggregated_lines:,}")
    print(f"SKIP 行数（其他年份仅计数）: {skipped_non_2026q1:,}")
    print(f"解析错误行: {skipped_errors}")
    print(f"2026Q1 聚合交易日数: {len(data_rows_2026q1)}")
    print()
    print("--- 月份统计 ---")
    for month_key in ["2026-01", "2026-02", "2026-03", "2026-04"]:
        stats = monthly_stats[month_key]
        days = stats["days"]
        avg_range = stats["total_range"] / days if days > 0 else 0.0
        month_name = {"2026-01": "1月", "2026-02": "2月", "2026-03": "3月", "2026-04": "4月"}[month_key]
        print(f"  {month_name}: 交易日 {days} 天 | 平均波动 (high-low) ${avg_range:.3f}")
    print()
    print(f"--- 23年抽样日线总数: {len(random_sample_rows)} 条 ---")
    print()

    print("=" * 80)
    print(f"[文件1] {os.path.basename(OUT_2026Q1)}  前20行预览")
    print("=" * 80)
    with open(OUT_2026Q1, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()
    for i, line in enumerate(lines[:21]):
        print(f"  {i:02d}: {line.rstrip()}")
    if len(lines) > 21:
        print(f"  ... (共 {len(lines)-1} 行数据，已省略 {len(lines)-21} 行)")

    print()
    print("=" * 80)
    print(f"[文件2] {os.path.basename(OUT_RANDOM)}  前20行预览")
    print("=" * 80)
    with open(OUT_RANDOM, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()
    for i, line in enumerate(lines[:21]):
        print(f"  {i:02d}: {line.rstrip()}")
    if len(lines) > 21:
        print(f"  ... (共 {len(lines)-1} 行数据，已省略 {len(lines)-21} 行)")

    print()
    print("=" * 80)
    print("统计摘要")
    print("=" * 80)
    print(f"  文件1输出路径: {OUT_2026Q1}")
    print(f"  文件1大小: {os.path.getsize(OUT_2026Q1):,} 字节")
    print(f"  文件2输出路径: {OUT_RANDOM}")
    print(f"  文件2大小: {os.path.getsize(OUT_RANDOM):,} 字节")
    print()
    print("  覆盖年份范围:", sorted(yearly_sample_buckets.keys())[0], "→", sorted(yearly_sample_buckets.keys())[-1])
    print(f"  覆盖总年数: {len(yearly_sample_buckets)} 年")
    for y in sorted(yearly_sample_buckets.keys()):
        cnt = len(yearly_sample_buckets[y])
        print(f"    {y}年: 抽样 {cnt} 天")


if __name__ == "__main__":
    aggregate()
