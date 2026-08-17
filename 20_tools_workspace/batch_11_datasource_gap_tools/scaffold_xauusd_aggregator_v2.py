import csv
import os
import sys
import argparse
import glob
import io
from datetime import datetime
from collections import defaultdict, OrderedDict
from typing import Optional, List, Dict, Tuple

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

WORK_DIR = r"D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_datasource_gap__20260811"
OUT_DIR = os.path.join(WORK_DIR, "out_forex_dryrun")
DEFAULT_ARCHIVE_DIR = r"D:\Stock\trading_assistant\10_source_library_archive"
OUT_TSV = os.path.join(OUT_DIR, "xauusd_d1_2026Q1_dryrun.tsv")
OUT_QC_MD = os.path.join(WORK_DIR, "xauusd_alignment_and_probe_qc__20260811.md")

TOTAL_EXPECTED = 8322566

OK_MARK = "[OK]"
FAIL_MARK = "[FAIL]"
WARN_MARK = "[WARN]"
CHECK_PASS = "[V]"
CHECK_FAIL = "[X]"


def find_xaucsv_path(archive_dir: str) -> Optional[str]:
    pattern = os.path.join(archive_dir, "**", "XAUUSD_1 Min_Bid*.csv")
    matches = glob.glob(pattern, recursive=True)
    if matches:
        return matches[0]
    alt1 = r"D:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\XAUUSD CSV\XAUUSD CSV\XAUUSD_1 Min_Bid_2003.05.05_2026.04.27.csv"
    if os.path.exists(alt1):
        return alt1
    alt2 = r"D:\Stock\trading_assistant\00_assets\_raw_snapshot_batch09\XAUUSD CSV\XAUUSD CSV\XAUUSD_1 Min_Bid_2003.05.05_2026.04.27.csv"
    if os.path.exists(alt2):
        return alt2
    return None


def parse_date_fast(s: str) -> str:
    return s[:4] + "-" + s[5:7] + "-" + s[8:10]


def parse_month_fast(s: str) -> str:
    return s[5:7]


def in_2026q1_strict(s: str) -> bool:
    if s < "2026.01.01":
        return False
    if s >= "2026.04.01":
        return False
    return True


def build_alignment_audit(csv_header: List[str], total_rows: int, missing_counts: Dict[str, int]) -> List[Dict]:
    source_cols_clean = [c.strip() for c in csv_header]
    standard_map = [
        {"source_idx": 0, "source_col": source_cols_clean[0] if len(source_cols_clean) > 0 else "",
         "target_col": "date", "unit": "YYYY-MM-DD"},
        {"source_idx": 1, "source_col": source_cols_clean[1] if len(source_cols_clean) > 1 else "",
         "target_col": "open", "unit": "USD/oz"},
        {"source_idx": 2, "source_col": source_cols_clean[2] if len(source_cols_clean) > 2 else "",
         "target_col": "high", "unit": "USD/oz"},
        {"source_idx": 3, "source_col": source_cols_clean[3] if len(source_cols_clean) > 3 else "",
         "target_col": "low", "unit": "USD/oz"},
        {"source_idx": 4, "source_col": source_cols_clean[4] if len(source_cols_clean) > 4 else "",
         "target_col": "close", "unit": "USD/oz"},
        {"source_idx": 5, "source_col": source_cols_clean[5] if len(source_cols_clean) > 5 else "",
         "target_col": "volume", "unit": "tick count"},
        {"source_idx": -1, "source_col": "(derived)", "target_col": "amplitude", "unit": "USD/oz"},
        {"source_idx": -1, "source_col": "(derived)", "target_col": "pct_chg", "unit": "%"},
        {"source_idx": -1, "source_col": "(constant)", "target_col": "source", "unit": "text"},
    ]
    audit_rows = []
    for item in standard_map:
        src_idx = item["source_idx"]
        if src_idx >= 0 and src_idx < len(source_cols_clean):
            missing = missing_counts.get(source_cols_clean[src_idx], 0)
            rate = (missing * 100.0 / total_rows) if total_rows > 0 else 0.0
            aligned = rate < 0.01
        else:
            rate = 0.0
            aligned = True
        audit_rows.append({
            "源CSV列名": item["source_col"],
            "目标标准列": item["target_col"],
            "单位": item["unit"],
            "缺失率": f"{rate:.4f}%",
            "对齐状态": CHECK_PASS if aligned else CHECK_FAIL,
        })
    return audit_rows


def history_aggregate(csv_path: Optional[str]) -> Tuple[List, List, Dict, Optional[str]]:
    os.makedirs(OUT_DIR, exist_ok=True)

    if csv_path is None or not os.path.exists(csv_path):
        print(f"{WARN_MARK} XAUUSD CSV not found (search root: {DEFAULT_ARCHIVE_DIR}), history_aggregate skipped")
        print(f"[HINT] use --xaucsv-path to specify the correct path")
        return [], [], {}, csv_path

    print(f"[INFO] Using CSV: {csv_path}")

    total_lines = 0
    aggregated_lines = 0
    skipped_non_q1 = 0
    skipped_errors = 0
    missing_counts: Dict[str, int] = defaultdict(int)

    daily_buckets = OrderedDict()
    monthly_stats: Dict[str, Dict] = defaultdict(lambda: {"days": 0, "total_range": 0.0, "total_pct": 0.0})

    current_key = None
    current_agg = None
    csv_header = None

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        csv_header = next(reader)
        total_lines += 1

        header_clean = [c.strip() for c in csv_header]
        last_progress = 0

        for row in reader:
            total_lines += 1

            if len(row) < 6:
                skipped_errors += 1
                for i, h in enumerate(header_clean):
                    if i >= len(row) or (isinstance(row[i], str) and row[i].strip() == ""):
                        missing_counts[h] += 1
                continue

            time_str = row[0]
            if len(time_str) < 19:
                skipped_errors += 1
                missing_counts[header_clean[0]] += 1
                continue

            try:
                o = float(row[1])
                h = float(row[2])
                l = float(row[3])
                c = float(row[4])
                v = float(row[5])
            except ValueError:
                skipped_errors += 1
                for i in range(1, 6):
                    try:
                        float(row[i])
                    except (ValueError, IndexError):
                        if i < len(header_clean):
                            missing_counts[header_clean[i]] += 1
                continue

            in_q1 = in_2026q1_strict(time_str)

            if in_q1:
                aggregated_lines += 1
                date_key = parse_date_fast(time_str)

                if current_key != date_key:
                    current_key = date_key
                    if date_key not in daily_buckets:
                        daily_buckets[date_key] = [o, h, l, c, v]
                        current_agg = daily_buckets[date_key]
                    else:
                        current_agg = daily_buckets[date_key]
                        current_agg[0] = o
                        if h > current_agg[1]:
                            current_agg[1] = h
                        if l < current_agg[2]:
                            current_agg[2] = l
                        current_agg[3] = c
                        current_agg[4] = v
                else:
                    if h > current_agg[1]:
                        current_agg[1] = h
                    if l < current_agg[2]:
                        current_agg[2] = l
                    current_agg[3] = c
                    current_agg[4] += v
            else:
                skipped_non_q1 += 1

            if total_lines - last_progress >= 1000000:
                pct = total_lines * 100.0 / TOTAL_EXPECTED
                print(f"  progress: {total_lines:,} / {TOTAL_EXPECTED:,} lines ({pct:.1f}%)")
                last_progress = total_lines

    data_rows = []
    sorted_keys = sorted(daily_buckets.keys())
    prev_close = None

    for date_key in sorted_keys:
        agg = daily_buckets[date_key]
        amplitude = agg[1] - agg[2]
        month_key = "2026-" + parse_month_fast(date_key.replace("-", "."))
        monthly_stats[month_key]["days"] += 1
        monthly_stats[month_key]["total_range"] += amplitude

        if prev_close is not None and prev_close != 0:
            pct_chg = (agg[3] - prev_close) / prev_close * 100.0
        else:
            pct_chg = 0.0
        monthly_stats[month_key]["total_pct"] += abs(pct_chg)

        data_rows.append((
            date_key,
            f"{agg[0]:.3f}",
            f"{agg[1]:.3f}",
            f"{agg[2]:.3f}",
            f"{agg[3]:.3f}",
            f"{agg[4]:.5f}",
            f"{amplitude:.3f}",
            f"{pct_chg:.4f}",
            "M1_23yr_archive",
        ))
        prev_close = agg[3]

    with open(OUT_TSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["date", "open", "high", "low", "close", "volume", "amplitude", "pct_chg", "source"])
        for row in data_rows:
            writer.writerow(row)

    data_total = total_lines - 1
    audit_table = build_alignment_audit(csv_header, data_total, missing_counts)

    print()
    print("=" * 90)
    print("a) 2026Q1 99-day verification (Jan 26d / Feb / Mar)")
    print("=" * 90)
    jan_days = monthly_stats.get("2026-01", {}).get("days", 0)
    feb_days = monthly_stats.get("2026-02", {}).get("days", 0)
    mar_days = monthly_stats.get("2026-03", {}).get("days", 0)
    total_days = jan_days + feb_days + mar_days
    expected_days = 99
    check_99 = f"{CHECK_PASS} match" if total_days == expected_days else f"{CHECK_FAIL} diff(expected {expected_days}d)"
    print(f"  Jan trading days: {jan_days} d (expected ~20-22d)")
    print(f"  Feb trading days: {feb_days} d (expected ~19-21d)")
    print(f"  Mar trading days: {mar_days} d (expected ~21-23d)")
    print(f"  Q1 total:        {total_days} d -> {check_99}")

    print()
    print("  --- Monthly avg amplitude (USD) ---")
    for mk in ["2026-01", "2026-02", "2026-03"]:
        st = monthly_stats[mk]
        days = st["days"]
        avg_rng = st["total_range"] / days if days > 0 else 0.0
        name = {"2026-01": "Jan", "2026-02": "Feb", "2026-03": "Mar"}[mk]
        print(f"    {name}: avg ${avg_rng:.3f} (total ${st['total_range']:.2f} / {days}d)")

    print()
    print("=" * 90)
    print("b) Column alignment audit table")
    print("=" * 90)
    col_w = [28, 16, 14, 12, 10]
    hdr = (
        "Src CSV Column".ljust(col_w[0])
        + "Target Std Col".ljust(col_w[1])
        + "Unit".ljust(col_w[2])
        + "Missing Rate".ljust(col_w[3])
        + "Align"
    )
    print(hdr)
    print("-" * 90)
    for ar in audit_table:
        line = (
            str(ar["源CSV列名"]).ljust(col_w[0])
            + str(ar["目标标准列"]).ljust(col_w[1])
            + str(ar["单位"]).ljust(col_w[2])
            + str(ar["缺失率"]).ljust(col_w[3])
            + str(ar["对齐状态"])
        )
        print(line)

    print()
    print(f"[SUMMARY] CSV total lines (w/ header): {total_lines:,} | Aggregated M1 lines: {aggregated_lines:,} | "
          f"SKIP non-Q1: {skipped_non_q1:,} | Parse errors: {skipped_errors}")
    print(f"[OUTPUT] {OUT_TSV} ({len(data_rows)} rows)")

    return data_rows, audit_table, monthly_stats, csv_path


def _probe_fx_spot_quote_xauusd(ak) -> Tuple[Optional[object], str]:
    errors = []
    df = None
    try:
        df = ak.fx_spot_quote(symbol="XAUUSD")
        return df, ""
    except Exception as e:
        errors.append(f"fx_spot_quote(symbol=XAUUSD): {e}")
    try:
        df_all = ak.fx_spot_quote()
        if df_all is not None and not df_all.empty:
            col0 = df_all.columns[0]
            mask = df_all[col0].astype(str).str.upper().str.contains("XAUUSD|XAU/USD|XAU", na=False)
            df_filtered = df_all[mask]
            if not df_filtered.empty:
                return df_filtered, f"fallback: fx_spot_quote() no args, filtered {len(df_filtered)} XAUUSD rows"
            return df_all, f"fallback: fx_spot_quote() all {len(df_all)} rows (no XAUUSD found in col={col0})"
    except Exception as e2:
        errors.append(f"fx_spot_quote() no args: {e2}")
    return None, " ; ".join(errors)


def _probe_currency_hist_xauusd(ak) -> Tuple[Optional[object], str]:
    errors = []
    df = None
    try:
        df = ak.currency_hist(symbol="xauusd", period="daily", start_date="20260401", end_date="20260427")
        return df, ""
    except Exception as e:
        errors.append(f"currency_hist(...): {e}")
    try:
        df = ak.currency_history(base="USD", date="2026-04-15", symbols="XAU")
        return df, "fallback: currency_history(base=USD, symbols=XAU)"
    except Exception as e2:
        errors.append(f"currency_history(...): {e2}")
    try:
        df = ak.currency_time_series(base="USD", start_date="2026-04-01", end_date="2026-04-27", symbols="XAU")
        return df, "fallback: currency_time_series(base=USD, symbols=XAU)"
    except Exception as e3:
        errors.append(f"currency_time_series(...): {e3}")
    try:
        df = ak.forex_spot_em()
        if df is not None and not df.empty:
            return df, f"fallback: forex_spot_em() all {len(df)} rows"
    except Exception as e4:
        errors.append(f"forex_spot_em(): {e4}")
    return None, " ; ".join(errors)


def akshare_increment_probe() -> Dict:
    print()
    print("=" * 90)
    print("c) akshare interface probe (DRY RUN: print cols/rows only, no persist)")
    print("=" * 90)

    probe_results = {
        "fx_spot_quote": {"status": "pending", "cols": [], "nrows": 0, "err": None, "note": ""},
        "currency_hist": {"status": "pending", "cols": [], "nrows": 0, "err": None, "note": ""},
    }

    try:
        import akshare as ak
        import pandas as pd
        ak_available = True
    except ImportError:
        ak_available = False
        print(f"{WARN_MARK} akshare not installed, using MOCK data based on docs")
        print("       pip install akshare --upgrade for live probe")

    if ak_available:
        try:
            print()
            print("  [API 1] ak.fx_spot_quote(symbol='XAUUSD') -> spot snapshot")
            df1, note1 = _probe_fx_spot_quote_xauusd(ak)
            probe_results["fx_spot_quote"]["note"] = note1
            if df1 is not None and not df1.empty:
                probe_results["fx_spot_quote"]["cols"] = list(df1.columns.astype(str))
                probe_results["fx_spot_quote"]["nrows"] = len(df1)
                probe_results["fx_spot_quote"]["status"] = "OK"
                print(f"    {OK_MARK} success | rows: {len(df1)} | cols: {len(df1.columns)}")
                print(f"    colnames: {list(df1.columns.astype(str))}")
                if note1:
                    print(f"    note: {note1}")
                with pd.option_context('display.max_columns', None, 'display.width', 200):
                    print(f"    head(2):\n{df1.head(2).to_string()}")
            else:
                probe_results["fx_spot_quote"]["status"] = "EMPTY_OR_FAIL"
                probe_results["fx_spot_quote"]["err"] = note1 or "empty result"
                print(f"    {WARN_MARK} empty or all fallback failed: {note1}")
        except Exception as e:
            probe_results["fx_spot_quote"]["status"] = "FAIL"
            probe_results["fx_spot_quote"]["err"] = str(e)
            print(f"    {FAIL_MARK} call failed: {e}")

        try:
            print()
            print("  [API 2] ak.currency_hist(symbol='xauusd', period='daily', start='20260401', end='20260427') -> incremental daily")
            df2, note2 = _probe_currency_hist_xauusd(ak)
            probe_results["currency_hist"]["note"] = note2
            if df2 is not None and not df2.empty:
                probe_results["currency_hist"]["cols"] = list(df2.columns.astype(str))
                probe_results["currency_hist"]["nrows"] = len(df2)
                probe_results["currency_hist"]["status"] = "OK"
                print(f"    {OK_MARK} success | rows: {len(df2)} | cols: {len(df2.columns)}")
                print(f"    colnames: {list(df2.columns.astype(str))}")
                if note2:
                    print(f"    note: {note2}")
                with pd.option_context('display.max_columns', None, 'display.width', 200):
                    print(f"    head(3):\n{df2.head(3).to_string()}")
                    print(f"    tail(3):\n{df2.tail(3).to_string()}")
            else:
                probe_results["currency_hist"]["status"] = "EMPTY_OR_FAIL"
                probe_results["currency_hist"]["err"] = note2 or "empty result"
                print(f"    {WARN_MARK} empty or all fallback failed: {note2}")
        except Exception as e:
            probe_results["currency_hist"]["status"] = "FAIL"
            probe_results["currency_hist"]["err"] = str(e)
            print(f"    {FAIL_MARK} call failed: {e}")
    else:
        probe_results["fx_spot_quote"]["status"] = "MOCK"
        probe_results["fx_spot_quote"]["cols"] = ["pair_code", "name", "last", "bid", "ask", "pct_chg", "change", "high", "low", "open", "prev_close", "time"]
        probe_results["fx_spot_quote"]["nrows"] = 1
        probe_results["fx_spot_quote"]["err"] = "akshare not installed (mock)"

        probe_results["currency_hist"]["status"] = "MOCK"
        probe_results["currency_hist"]["cols"] = ["date", "open", "close", "high", "low", "volume"]
        probe_results["currency_hist"]["nrows"] = 19
        probe_results["currency_hist"]["err"] = "akshare not installed (mock)"

        print()
        print("  [API 1 MOCK] fx_spot_quote(XAUUSD) expected:")
        print(f"    cols: {probe_results['fx_spot_quote']['cols']}")
        print(f"    rows: {probe_results['fx_spot_quote']['nrows']} (snapshot, typically 1)")
        print()
        print("  [API 2 MOCK] currency_hist(xauusd, 20260401-20260427) expected:")
        print(f"    cols: {probe_results['currency_hist']['cols']}")
        print(f"    rows: {probe_results['currency_hist']['nrows']} (~19 trading days in April)")

    print()
    print("  --- probe summary ---")
    for name, info in probe_results.items():
        msg = f"    {name}: {info['status']} | {info['nrows']}r x {len(info['cols'])}c"
        if info.get("note"):
            msg += f" | note={str(info['note'])[:80]}"
        elif info.get("err"):
            msg += f" | ERR={str(info['err'])[:80]}"
        print(msg)

    return probe_results


def _qc_status_icon(status: str) -> str:
    if status == "OK":
        return CHECK_PASS
    if status == "MOCK":
        return "[MOCK]"
    return CHECK_FAIL


def generate_qc_md(
    data_rows: List,
    audit_table: List[Dict],
    monthly_stats: Dict,
    probe_results: Dict,
    csv_path: Optional[str],
) -> None:
    jan_days = monthly_stats.get("2026-01", {}).get("days", 0)
    feb_days = monthly_stats.get("2026-02", {}).get("days", 0)
    mar_days = monthly_stats.get("2026-03", {}).get("days", 0)
    total_days = jan_days + feb_days + mar_days

    lines = []
    lines.append("# XAUUSD Column Alignment & akshare Probe QC Report")
    lines.append("")
    lines.append(f"- **Generated**: 2026-08-11")
    lines.append(f"- **Source CSV**: {csv_path if csv_path else '(not found, aggregation skipped)'}")
    lines.append(f"- **Output Aggregate TSV**: `out_forex_dryrun/xauusd_d1_2026Q1_dryrun.tsv`")
    lines.append(f"- **Q1 Window**: 2026-01-01 ~ 2026-03-31 (strict Q1, excluding April)")
    lines.append("")
    lines.append("## 1. 2026Q1 Monthly Trading Days & Avg Amplitude")
    lines.append("")
    lines.append("| Month | Trading Days | Total Range (USD) | Avg Daily Range (USD) | Note |")
    lines.append("|-------|-------------|-------------------|----------------------|------|")
    for mk, name in [("2026-01", "Jan"), ("2026-02", "Feb"), ("2026-03", "Mar")]:
        st = monthly_stats.get(mk, {})
        days = st.get("days", 0)
        tr = st.get("total_range", 0.0)
        avg = tr / days if days > 0 else 0.0
        lines.append(f"| {name} | {days} | {tr:.2f} | {avg:.3f} |  |")
    q1_range = sum(monthly_stats.get(m, {}).get("total_range", 0.0) for m in ["2026-01", "2026-02", "2026-03"])
    q1_avg = q1_range / total_days if total_days > 0 else 0.0
    check_icon = CHECK_PASS if total_days == 99 else CHECK_FAIL
    lines.append(f"| **Q1 Total** | **{total_days}** | **{q1_range:.2f}** | **{q1_avg:.3f}** | 99d check: {check_icon} |")
    lines.append("")
    lines.append("## 2. Column Alignment Audit Table")
    lines.append("")
    lines.append("| Src CSV Column | Target Std Col | Unit | Missing Rate | Align Status |")
    lines.append("|---------------|---------------|------|-------------|-------------|")
    for ar in audit_table:
        lines.append(f"| {ar['源CSV列名']} | {ar['目标标准列']} | {ar['单位']} | {ar['缺失率']} | {ar['对齐状态']} |")
    lines.append("")
    lines.append("### Alignment Notes")
    lines.append("- Standard columns aligned to akshare `fx_spot_quote` / `currency_hist` expected contract: `date/open/high/low/close/volume`")
    lines.append("- Additional derived columns: `amplitude`(H-L), `pct_chg`((C-prev_C)/prev_C*100), `source`(M1_23yr_archive)")
    lines.append("")
    lines.append("## 3. akshare Interface Probe Results")
    lines.append("")
    lines.append("### 3.1 fx_spot_quote(symbol='XAUUSD') - Spot Snapshot")
    lines.append("")
    r1 = probe_results["fx_spot_quote"]
    icon1 = _qc_status_icon(r1["status"])
    lines.append(f"- **Status**: {icon1} {r1['status']}")
    lines.append(f"- **Rows**: {r1['nrows']}")
    lines.append(f"- **Cols**: {len(r1['cols'])}")
    lines.append(f"- **Colnames**: `{'`, `'.join(r1['cols'])}`")
    if r1.get("note"):
        lines.append(f"- **Note**: {r1['note']}")
    if r1.get("err") and r1["status"] not in ("OK",):
        lines.append(f"- **Error/Info**: {r1['err']}")
    lines.append("")
    lines.append("### 3.2 currency_hist(symbol='xauusd', period='daily', start='20260401', end='20260427') - Incremental Daily")
    lines.append("")
    r2 = probe_results["currency_hist"]
    icon2 = _qc_status_icon(r2["status"])
    lines.append(f"- **Status**: {icon2} {r2['status']}")
    lines.append(f"- **Rows**: {r2['nrows']} (increment window post CSV end-date 2026.04.27: 2026-04-01 ~ 2026-04-27)")
    lines.append(f"- **Cols**: {len(r2['cols'])}")
    lines.append(f"- **Colnames**: `{'`, `'.join(r2['cols'])}`")
    if r2.get("note"):
        lines.append(f"- **Note**: {r2['note']}")
    if r2.get("err") and r2["status"] not in ("OK",):
        lines.append(f"- **Error/Info**: {r2['err']}")
    lines.append("")
    lines.append("## 4. Aggregate TSV Sample (Head 5 + Tail 5)")
    lines.append("")
    lines.append("```tsv")
    lines.append("date\topen\thigh\tlow\tclose\tvolume\tamplitude\tpct_chg\tsource")
    if data_rows:
        for r in data_rows[:5]:
            lines.append("\t".join(r))
        if len(data_rows) > 10:
            lines.append("... (rows omitted) ...")
        for r in data_rows[-5:]:
            lines.append("\t".join(r))
    else:
        lines.append("(CSV not found, aggregation not executed)")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("*QC auto-generated by scaffold_xauusd_aggregator_v2.py*")

    with open(OUT_QC_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n[QC_REPORT] {OUT_QC_MD} generated")


def main():
    parser = argparse.ArgumentParser(description="XAUUSD aggregator scaffold v2: history_aggregate + akshare_increment_probe")
    parser.add_argument(
        "--mode",
        choices=["history_aggregate", "akshare_increment_probe"],
        default="akshare_increment_probe",
        help="runtime mode (default: akshare_increment_probe)",
    )
    parser.add_argument(
        "--xaucsv-path",
        default=None,
        help=r"XAUUSD 1min CSV path (default glob XAUUSD_1 Min_Bid*.csv under ...\10_source_library_archive)",
    )
    args = parser.parse_args()

    print("=" * 70)
    print(" scaffold_xauusd_aggregator_v2.py  |  2026-08-11")
    print(f" MODE = {args.mode}")
    print("=" * 70)

    if args.xaucsv_path:
        csv_path = args.xaucsv_path
        if not os.path.exists(csv_path):
            print(f"{WARN_MARK} --xaucsv-path file not found: {csv_path}")
            csv_path = None
    else:
        csv_path = find_xaucsv_path(DEFAULT_ARCHIVE_DIR)

    data_rows, audit_table, monthly_stats = [], [], {}
    probe_results = {}

    if args.mode == "history_aggregate":
        data_rows, audit_table, monthly_stats, _ = history_aggregate(csv_path)
        probe_results = akshare_increment_probe()
    elif args.mode == "akshare_increment_probe":
        probe_results = akshare_increment_probe()

    if args.mode == "history_aggregate":
        generate_qc_md(data_rows, audit_table, monthly_stats, probe_results, csv_path)
    else:
        if not os.path.exists(OUT_QC_MD):
            empty_monthly = {"2026-01": {"days": 0, "total_range": 0.0}, "2026-02": {"days": 0, "total_range": 0.0}, "2026-03": {"days": 0, "total_range": 0.0}}
            generate_qc_md([], [], empty_monthly, probe_results, csv_path)

    print()
    print("[DONE] scaffold_xauusd_aggregator_v2.py finished")


if __name__ == "__main__":
    main()
