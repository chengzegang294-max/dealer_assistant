import os
import sys
import argparse
import traceback
from datetime import datetime
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import pandas as pd
import akshare as ak

BASE_DIR = r"D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_datasource_gap__20260811"

INDEX_MAP = [
    {
        "id": "IDX01",
        "name": "上指",
        "candidates": [
            ('stock_zh_index_daily', {'symbol': 'sh000001'}),
            ('stock_zh_index_daily_em', {'symbol': 'sh000001'}),
            ('index_zh_a_hist', {'symbol': '000001', 'period': 'daily'}),
        ],
    },
    {
        "id": "IDX02",
        "name": "沪深300",
        "candidates": [
            ('stock_zh_index_daily', {'symbol': 'sh000300'}),
            ('stock_zh_index_daily_em', {'symbol': 'sh000300'}),
            ('index_zh_a_hist', {'symbol': '000300', 'period': 'daily'}),
        ],
    },
    {
        "id": "IDX03",
        "name": "标普500",
        "candidates": [
            ('index_us_stock_sina', {'symbol': '.INX'}),
            ('stock_us_index_spot_em', {'symbol': '标普500'}),
            ('index_us_spx', {}),
        ],
    },
    {
        "id": "IDX04",
        "name": "纳指",
        "candidates": [
            ('index_us_stock_sina', {'symbol': '.IXIC'}),
            ('stock_us_index_spot_em', {'symbol': '纳斯达克'}),
            ('index_us_ixic', {}),
        ],
    },
    {
        "id": "IDX05",
        "name": "德指",
        "candidates": [
            ('index_global_sina', {'symbol': 'gdaxi'}),
            ('stock_global_index_em', {'symbol': 'DAX'}),
            ('index_global_dax', {}),
        ],
    },
    {
        "id": "IDX06",
        "name": "英指",
        "candidates": [
            ('index_global_sina', {'symbol': 'ftse'}),
            ('stock_global_index_em', {'symbol': '富时100'}),
            ('index_global_ftse', {}),
        ],
    },
    {
        "id": "IDX07",
        "name": "美元指数",
        "candidates": [
            ('currency_hist', {'symbol': 'dxy', 'period': 'daily'}),
            ('currency_hist_sina', {'symbol': '美元指数'}),
            ('fx_spot_quote', {'symbol': 'DXY'}),
        ],
    },
]

STATUS_EMOJI = {
    'SUCCESS': '🟢',
    'PARTIAL': '🟡',
    'FAIL': '🔴',
}


def try_call_one(idx_info, candidate_idx):
    func_name, kwargs = idx_info['candidates'][candidate_idx]
    call_str = f"ak.{func_name}({', '.join(f'{k}={repr(v)}' for k, v in kwargs.items())})"
    try:
        func = getattr(ak, func_name)
        df = func(**kwargs)
        if df is None or len(df) == 0:
            return None, call_str, f"Empty DataFrame from {call_str}"
        return df, call_str, None
    except Exception as e:
        return None, call_str, f"{type(e).__name__}: {str(e)[:120]}"


def probe_one(idx_info):
    last_err = None
    last_call_str = None
    df_ok = None
    tried_calls = []
    for ci in range(min(3, len(idx_info['candidates']))):
        df, call_str, err = try_call_one(idx_info, ci)
        tried_calls.append(call_str)
        last_call_str = call_str
        if df is not None:
            df_ok = df
            break
        last_err = err
    return df_ok, last_call_str, last_err, tried_calls


def extract_date_col(df):
    for c in df.columns:
        cl = str(c).lower()
        if 'date' in cl or '日期' in c or '时间' in c:
            return c
    return df.columns[0]


def extract_ohlc(df):
    cols_lower = {str(c).lower(): c for c in df.columns}
    o = cols_lower.get('open') or cols_lower.get('开盘')
    h = cols_lower.get('high') or cols_lower.get('最高')
    l = cols_lower.get('low') or cols_lower.get('最低')
    c = cols_lower.get('close') or cols_lower.get('收盘')
    return o, h, l, c


def run_probe(outdir):
    os.makedirs(outdir, exist_ok=True)
    qc_rows = []
    detail_results = []
    status_banners = []

    for idx in INDEX_MAP:
        print("\n" + "=" * 70)
        print(f"[{idx['id']}] {idx['name']} — probe start")
        df, call_str, err, tried_calls = probe_one(idx)
        status = 'FAIL'
        row_count = 0
        earliest = '-'
        latest = '-'
        last2_ohlc = None
        col_names4 = []

        if df is not None:
            try:
                status = 'SUCCESS'
                row_count = len(df)
                col_count = df.shape[1]
                col_names4 = list(df.columns[:4])
                date_col = extract_date_col(df)
                date_series = pd.to_datetime(df[date_col], errors='coerce').dt.strftime('%Y-%m-%d')
                valid_dates = date_series.dropna()
                if len(valid_dates) > 0:
                    earliest = valid_dates.iloc[0]
                    latest = valid_dates.iloc[-1]
                o, h, l, c = extract_ohlc(df)
                if all([o, h, l, c]):
                    tail2 = df.tail(2).copy()
                    tail2_dates = pd.to_datetime(tail2[date_col], errors='coerce').dt.strftime('%Y-%m-%d').tolist()
                    tail_o = tail2[o].tolist()
                    tail_h = tail2[h].tolist()
                    tail_l = tail2[l].tolist()
                    tail_c = tail2[c].tolist()
                    last2_ohlc = []
                    for i in range(len(tail2_dates)):
                        last2_ohlc.append({
                            'date': tail2_dates[i],
                            'open': tail_o[i],
                            'high': tail_h[i],
                            'low': tail_l[i],
                            'close': tail_c[i],
                        })
                print(f"  cols={col_count}  rows={row_count}  columns[:4]={col_names4}")
                print(f"  date range: {earliest} ~ {latest}")
                if last2_ohlc:
                    for r in last2_ohlc:
                        print(f"  tail date {r['date']}: O={r['open']} H={r['high']} L={r['low']} C={r['close']}")
                else:
                    print(f"  tail(2) rows:\n{df.tail(2).to_string()}")
            except Exception as inner:
                status = 'PARTIAL'
                err = (err or '') + f" | PARSE_ERR: {type(inner).__name__}: {str(inner)[:100]}"
                print(f"  [!] parse partial: {err}")
        else:
            print(f"  FAIL: {err}")
            print(f"  tried calls: {tried_calls}")

        qc_rows.append({
            '内部编号': idx['id'],
            '显示名': idx['name'],
            'akshare调用串': call_str,
            '可用状态': status,
            '行数': row_count,
            '最早日期': earliest,
            '最新日期': latest,
        })
        detail_results.append({
            'id': idx['id'],
            'name': idx['name'],
            'status': status,
            'err': err,
            'last2_ohlc': last2_ohlc,
            'tried_calls': tried_calls,
            'col_names4': col_names4,
            'row_count': row_count,
            'earliest': earliest,
            'latest': latest,
            'call_str': call_str,
        })
        banner = f"{STATUS_EMOJI[status]}{idx['name']}({idx['id']})"
        status_banners.append(banner)

    qc_tsv_path = os.path.join(outdir, 'index_7lines_probe_qc.tsv')
    fieldnames = ['内部编号', '显示名', 'akshare调用串', '可用状态', '行数', '最早日期', '最新日期']
    with open(qc_tsv_path, 'w', encoding='utf-8-sig', newline='') as f:
        import csv
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(qc_rows)

    md_path = os.path.join(BASE_DIR, 'index_7lines_exec_card__20260811.md')
    md_lines = []
    md_lines.append('# 7条指数 akshare 探针执行卡 __20260811')
    md_lines.append('')
    md_lines.append(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md_lines.append(f"> 输出目录: `{outdir}`")
    md_lines.append('')
    md_lines.append('## 一、总览状态条')
    md_lines.append('')
    md_lines.append(' '.join(status_banners))
    md_lines.append('')
    md_lines.append('## 二、明细卡片')
    md_lines.append('')
    for d in detail_results:
        emo = STATUS_EMOJI[d['status']]
        md_lines.append(f"### {d['id']} {emo} {d['name']}")
        md_lines.append(f"- 状态: **{d['status']}**")
        md_lines.append(f"- 最终调用: `{d['call_str']}`")
        if d['status'] == 'FAIL':
            md_lines.append(f"- 异常: `{d['err']}`")
            md_lines.append(f"- 尝试过的调用:")
            for tc in d['tried_calls']:
                md_lines.append(f"  - `{tc}`")
        else:
            md_lines.append(f"- 行数: {d['row_count']}")
            md_lines.append(f"- 覆盖日期: {d['earliest']} ~ {d['latest']}")
            md_lines.append(f"- 前4列: {d['col_names4']}")
            if d['last2_ohlc']:
                md_lines.append(f"- 最后2日 OHLC 样例:")
                md_lines.append(f"  | 日期 | Open | High | Low | Close |")
                md_lines.append(f"  |------|------|------|-----|-------|")
                for r in d['last2_ohlc']:
                    md_lines.append(f"  | {r['date']} | {r['open']} | {r['high']} | {r['low']} | {r['close']} |")
        md_lines.append('')
    md_lines.append('## 三、QC TSV 摘要')
    md_lines.append('')
    md_lines.append(f"文件: `{qc_tsv_path}`")
    md_lines.append('')
    md_lines.append('| 内部编号 | 显示名 | 状态 | 行数 | 最早 | 最新 |')
    md_lines.append('|----------|--------|------|------|------|------|')
    for q in qc_rows:
        md_lines.append(f"| {q['内部编号']} | {q['显示名']} | {q['可用状态']} | {q['行数']} | {q['最早日期']} | {q['最新日期']} |")
    md_lines.append('')

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print("\n" + "=" * 70)
    print("[CONSOLE OUTPUT A] 7条状态并排:")
    print(' '.join(status_banners))

    print("\n" + "=" * 70)
    print("[CONSOLE OUTPUT B] QC TSV 全部7行:")
    with open(qc_tsv_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()
        print(content.rstrip())

    print("\n" + "=" * 70)
    print("[CONSOLE OUTPUT C] MD 前20行:")
    with open(md_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 20:
                break
            print(line.rstrip('\n'))

    print("\n[DONE] QC TSV:", qc_tsv_path)
    print("[DONE] Exec MD:", md_path)


def run_fetch(outdir):
    raise NotImplementedError("fetch mode is intentionally locked. Only probe is available now.")


def main():
    parser = argparse.ArgumentParser(description='7 条指数 akshare 探针脚手架')
    parser.add_argument('--mode', choices=['probe', 'fetch'], default='probe', help='probe: 试接口并出QC; fetch: 锁死(NotImplementedError)')
    parser.add_argument('--outdir', default=os.path.join(BASE_DIR, 'out_index_dryrun'), help='QC输出目录, 默认 out_index_dryrun/')
    args = parser.parse_args()

    if args.mode == 'probe':
        run_probe(args.outdir)
    elif args.mode == 'fetch':
        run_fetch(args.outdir)


if __name__ == '__main__':
    main()
