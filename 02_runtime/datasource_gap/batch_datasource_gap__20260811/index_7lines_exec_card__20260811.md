# 7条指数 akshare 探针执行卡 __20260811

> 生成时间: 2026-08-11 10:02:25
> 输出目录: `D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_datasource_gap__20260811\out_index_dryrun`

## 一、总览状态条

🟢上指(IDX01) 🟢沪深300(IDX02) 🟢标普500(IDX03) 🟢纳指(IDX04) 🔴德指(IDX05) 🔴英指(IDX06) 🔴美元指数(IDX07)

## 二、明细卡片

### IDX01 🟢 上指
- 状态: **SUCCESS**
- 最终调用: `ak.stock_zh_index_daily(symbol='sh000001')`
- 行数: 8700
- 覆盖日期: 1990-12-19 ~ 2026-08-10
- 前4列: ['date', 'open', 'high', 'low']
- 最后2日 OHLC 样例:
  | 日期 | Open | High | Low | Close |
  |------|------|------|-----|-------|
  | 2026-08-07 | 3896.485 | 3940.935 | 3885.625 | 3940.037 |
  | 2026-08-10 | 3943.816 | 3967.592 | 3938.625 | 3966.594 |

### IDX02 🟢 沪深300
- 状态: **SUCCESS**
- 最终调用: `ak.stock_zh_index_daily(symbol='sh000300')`
- 行数: 5967
- 覆盖日期: 2002-01-04 ~ 2026-08-10
- 前4列: ['date', 'open', 'high', 'low']
- 最后2日 OHLC 样例:
  | 日期 | Open | High | Low | Close |
  |------|------|------|-----|-------|
  | 2026-08-07 | 4656.098 | 4706.729 | 4649.576 | 4694.437 |
  | 2026-08-10 | 4698.816 | 4714.465 | 4659.47 | 4702.025 |

### IDX03 🟢 标普500
- 状态: **SUCCESS**
- 最终调用: `ak.index_us_stock_sina(symbol='.INX')`
- 行数: 5689
- 覆盖日期: 2004-01-02 ~ 2026-08-10
- 前4列: ['date', 'open', 'high', 'low']
- 最后2日 OHLC 样例:
  | 日期 | Open | High | Low | Close |
  |------|------|------|-----|-------|
  | 2026-08-07 | 7735.1802 | 7763.0801 | 7719.1899 | 7757.6401 |
  | 2026-08-10 | 7751.7402 | 7773.7598 | 7743.1099 | 7753.1099 |

### IDX04 🟢 纳指
- 状态: **SUCCESS**
- 最终调用: `ak.index_us_stock_sina(symbol='.IXIC')`
- 行数: 5686
- 覆盖日期: 2004-01-02 ~ 2026-08-10
- 前4列: ['date', 'open', 'high', 'low']
- 最后2日 OHLC 样例:
  | 日期 | Open | High | Low | Close |
  |------|------|------|-----|-------|
  | 2026-08-07 | 26534.6602 | 26712.6172 | 26478.0059 | 26690.6152 |
  | 2026-08-10 | 26680.4434 | 26724.6309 | 26548.2578 | 26605.3574 |

### IDX05 🔴 德指
- 状态: **FAIL**
- 最终调用: `ak.index_global_dax()`
- 异常: `AttributeError: module 'akshare' has no attribute 'index_global_dax'`
- 尝试过的调用:
  - `ak.index_global_sina(symbol='gdaxi')`
  - `ak.stock_global_index_em(symbol='DAX')`
  - `ak.index_global_dax()`

### IDX06 🔴 英指
- 状态: **FAIL**
- 最终调用: `ak.index_global_ftse()`
- 异常: `AttributeError: module 'akshare' has no attribute 'index_global_ftse'`
- 尝试过的调用:
  - `ak.index_global_sina(symbol='ftse')`
  - `ak.stock_global_index_em(symbol='富时100')`
  - `ak.index_global_ftse()`

### IDX07 🔴 美元指数
- 状态: **FAIL**
- 最终调用: `ak.fx_spot_quote(symbol='DXY')`
- 异常: `TypeError: fx_spot_quote() got an unexpected keyword argument 'symbol'`
- 尝试过的调用:
  - `ak.currency_hist(symbol='dxy', period='daily')`
  - `ak.currency_hist_sina(symbol='美元指数')`
  - `ak.fx_spot_quote(symbol='DXY')`

## 三、QC TSV 摘要

文件: `D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_datasource_gap__20260811\out_index_dryrun\index_7lines_probe_qc.tsv`

| 内部编号 | 显示名 | 状态 | 行数 | 最早 | 最新 |
|----------|--------|------|------|------|------|
| IDX01 | 上指 | SUCCESS | 8700 | 1990-12-19 | 2026-08-10 |
| IDX02 | 沪深300 | SUCCESS | 5967 | 2002-01-04 | 2026-08-10 |
| IDX03 | 标普500 | SUCCESS | 5689 | 2004-01-02 | 2026-08-10 |
| IDX04 | 纳指 | SUCCESS | 5686 | 2004-01-02 | 2026-08-10 |
| IDX05 | 德指 | FAIL | 0 | - | - |
| IDX06 | 英指 | FAIL | 0 | - | - |
| IDX07 | 美元指数 | FAIL | 0 | - | - |
