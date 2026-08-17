#!/usr/bin/env python3
import argparse
import os
import sys
import traceback
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


def get_default_trade_date():
    today = datetime.now()
    offset = max(1, (today.weekday() + 6) % 7 - 3)
    d = today - timedelta(days=offset)
    return d.strftime("%Y%m%d")


def safe_import_akshare():
    try:
        import akshare as ak
        return True, ak, getattr(ak, "__version__", "unknown")
    except Exception as e:
        return False, None, str(e)


def probe_api_detail_em(ak, date_str):
    api_name = "stock_lhb_detail_em"
    record = {
        "接口名": api_name,
        "是否可用": "异常",
        "字段数": 0,
        "样例行数": 0,
        "样例列名前5": "",
        "空值最高的3列+率": "",
        "_note": "",
        "_error": "",
        "_traceback_top3": "",
    }
    try:
        try:
            df = ak.stock_lhb_detail_em(trade_date=date_str)
        except TypeError:
            record["_note"] = "原参数 trade_date 不存在, 回退使用 start_date/end_date"
            df = ak.stock_lhb_detail_em(start_date=date_str, end_date=date_str)
        if df is None or len(df) == 0:
            record["是否可用"] = "异常"
            record["_error"] = "返回空 DataFrame 或 None"
            return record
        record["是否可用"] = "可用"
        record["字段数"] = len(df.columns)
        record["样例行数"] = len(df)
        record["样例列名前5"] = ",".join(list(df.columns)[:5])
        if len(df) > 0:
            null_rates = df.isnull().mean().sort_values(ascending=False)
            top3_items = []
            for col, rate in null_rates.head(3).items():
                top3_items.append(f"{col}={rate:.4f}")
            record["空值最高的3列+率"] = ";".join(top3_items)
        print(f"  [OK] {api_name}: cols={record['字段数']}, rows={record['样例行数']}")
        print(f"       Top5 cols: {record['样例列名前5']}")
        print(df.head(3).to_string())
    except Exception as e:
        tb_lines = traceback.format_exc().splitlines()[:3]
        record["是否可用"] = "异常"
        record["_error"] = str(e)
        record["_traceback_top3"] = "\n".join(tb_lines)
        print(f"  [FAIL] {api_name}: {e}")
        for line in tb_lines:
            print(f"       {line}")
    return record


def probe_api_ggtj_em(ak, start_date, end_date):
    api_name = "stock_lhb_ggtj_em"
    record = {
        "接口名": api_name,
        "是否可用": "异常",
        "字段数": 0,
        "样例行数": 0,
        "样例列名前5": "",
        "空值最高的3列+率": "",
        "_note": "",
        "_error": "",
        "_traceback_top3": "",
    }
    try:
        if not hasattr(ak, "stock_lhb_ggtj_em"):
            record["_note"] = "akshare 无 stock_lhb_ggtj_em 属性, 仅 stock_lhb_ggtj_sina 可用"
        df = ak.stock_lhb_ggtj_em(start_date=start_date, end_date=end_date)
        if df is None or len(df) == 0:
            record["是否可用"] = "异常"
            record["_error"] = "返回空 DataFrame 或 None"
            return record
        record["是否可用"] = "可用"
        record["字段数"] = len(df.columns)
        record["样例行数"] = len(df)
        record["样例列名前5"] = ",".join(list(df.columns)[:5])
        if len(df) > 0:
            null_rates = df.isnull().mean().sort_values(ascending=False)
            top3_items = []
            for col, rate in null_rates.head(3).items():
                top3_items.append(f"{col}={rate:.4f}")
            record["空值最高的3列+率"] = ";".join(top3_items)
        print(f"  [OK] {api_name}: cols={record['字段数']}, rows={record['样例行数']}")
        print(f"       Top5 cols: {record['样例列名前5']}")
        print(df.head(3).to_string())
    except Exception as e:
        tb_lines = traceback.format_exc().splitlines()[:3]
        record["是否可用"] = "异常"
        record["_error"] = str(e)
        record["_traceback_top3"] = "\n".join(tb_lines)
        print(f"  [FAIL] {api_name}: {e}")
        for line in tb_lines:
            print(f"       {line}")
    return record


def probe_api_stock_statistic_em(ak, symbol="近一月"):
    api_name = "stock_lhb_stock_statistic_em"
    record = {
        "接口名": api_name,
        "是否可用": "异常",
        "字段数": 0,
        "样例行数": 0,
        "样例列名前5": "",
        "空值最高的3列+率": "",
        "_note": "",
        "_error": "",
        "_traceback_top3": "",
    }
    try:
        df = ak.stock_lhb_stock_statistic_em(symbol=symbol)
        if df is None or len(df) == 0:
            record["是否可用"] = "异常"
            record["_error"] = "返回空 DataFrame 或 None"
            return record
        record["是否可用"] = "可用"
        record["字段数"] = len(df.columns)
        record["样例行数"] = len(df)
        record["样例列名前5"] = ",".join(list(df.columns)[:5])
        if len(df) > 0:
            null_rates = df.isnull().mean().sort_values(ascending=False)
            top3_items = []
            for col, rate in null_rates.head(3).items():
                top3_items.append(f"{col}={rate:.4f}")
            record["空值最高的3列+率"] = ";".join(top3_items)
        print(f"  [OK] {api_name}: cols={record['字段数']}, rows={record['样例行数']}")
        print(f"       Top5 cols: {record['样例列名前5']}")
        print(df.head(3).to_string())
    except Exception as e:
        tb_lines = traceback.format_exc().splitlines()[:3]
        record["是否可用"] = "异常"
        record["_error"] = str(e)
        record["_traceback_top3"] = "\n".join(tb_lines)
        print(f"  [FAIL] {api_name}: {e}")
        for line in tb_lines:
            print(f"       {line}")
    return record


def run_probe(date_str, outdir):
    print("=" * 72)
    print("scaffold_longhubang_akshare_daily.py  |  MODE = probe (DRY RUN)")
    print("=" * 72)

    ok_import, ak_mod, ak_ver_or_err = safe_import_akshare()
    if not ok_import:
        print(f"[FATAL] akshare 未安装或导入失败: {ak_ver_or_err}")
        return None, None
    ak = ak_mod
    print(f"akshare 版本: {ak_ver_or_err}")
    print(f"目标日期 (date): {date_str}")
    print(f"输出目录 (outdir): {outdir}")
    print()

    start_d = date_str[:6] + "01"
    end_d = date_str

    records = []
    print("[1/3] stock_lhb_detail_em")
    r1 = probe_api_detail_em(ak, date_str)
    records.append(r1)
    print()

    print("[2/3] stock_lhb_ggtj_em")
    r2 = probe_api_ggtj_em(ak, start_d, end_d)
    records.append(r2)
    print()

    print("[3/3] stock_lhb_stock_statistic_em")
    r3 = probe_api_stock_statistic_em(ak, "近一月")
    records.append(r3)
    print()

    os.makedirs(outdir, exist_ok=True)

    qc_rows = []
    for r in records:
        qc_rows.append({
            "接口名": r["接口名"],
            "字段数": r["字段数"],
            "行数": r["样例行数"],
            "空值率TOP3列": r["空值最高的3列+率"],
        })
    qc_df = pd.DataFrame(qc_rows)
    tsv_path = os.path.join(outdir, "longhubang_probe_qc_summary__20260811.tsv")
    qc_df.to_csv(tsv_path, sep="\t", index=False, encoding="utf-8-sig")
    print(f"[INFO] QC 摘要 TSV 已写入: {tsv_path}")

    return records, tsv_path


def run_fetch(date_str, outdir):
    raise NotImplementedError(
        "fetch 模式尚未实现 - 禁止实跑。当前仅 probe 模式可用(dry-run探活不存)。"
        "待确认接口签名/稳定性后再开放 fetch 落盘。"
    )


def main():
    parser = argparse.ArgumentParser(
        description="龙虎榜 akshare 日批脚手架 (scaffold_longhubang_akshare_daily.py)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    default_date = get_default_trade_date()
    script_dir = Path(__file__).resolve().parent
    default_outdir = str(script_dir / "out_longhubang_dryrun")
    parser.add_argument(
        "--date",
        type=str,
        default=default_date,
        help=f"YYYYMMDD, 默认最近交易日={default_date}",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["probe", "fetch"],
        default="probe",
        help="probe=dry-run探活不存(默认), fetch=实际抓取(当前禁止实跑)",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default=default_outdir,
        help=f"输出目录, 默认={default_outdir}",
    )
    args = parser.parse_args()

    print()
    if args.mode == "probe":
        records, tsv_path = run_probe(args.date, args.outdir)
        if records is None:
            sys.exit(1)
    elif args.mode == "fetch":
        run_fetch(args.date, args.outdir)
    else:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
