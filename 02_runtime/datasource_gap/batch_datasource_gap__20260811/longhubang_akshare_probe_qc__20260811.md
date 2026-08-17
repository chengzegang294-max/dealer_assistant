# 龙虎榜 akshare 接口探活 QC 报告 __20260811

- **akshare 版本**: 1.18.64
- **探活日期**: 20260811
- **生成时间**: 2026-08-11

## 接口总览

| 接口名 | 是否可用 | 字段数 | 样例行数 | 样例列名前5 | 空值最高的3列+率 |
|--------|----------|--------|----------|-------------|------------------|
| stock_lhb_detail_em(trade_date/start_date,end_date) | 可用 | 21 | 70 | 序号,代码,名称,上榜日,解读 | 上榜后1日=1.0000;上榜后10日=1.0000;上榜后5日=1.0000 |
| stock_lhb_ggtj_em(start_date,end_date) | 异常 | 0 | 0 |  |  |
| stock_lhb_stock_statistic_em(symbol=近一月) | 可用 | 20 | 772 | 序号,代码,名称,最近上榜日,收盘价 | 序号=0.0000;代码=0.0000;名称=0.0000 |

## 各接口详细

### stock_lhb_detail_em

- **是否可用**: 可用
- **字段数**: 21
- **样例行数**: 70
- **样例列名前5**: 序号,代码,名称,上榜日,解读
- **空值最高的3列+率**: 上榜后1日=1.0000;上榜后10日=1.0000;上榜后5日=1.0000
- **说明**: 原参数 trade_date 不存在, 使用 start_date/end_date=20260810 成功

### stock_lhb_ggtj_em

- **是否可用**: 异常
- **字段数**: 0
- **样例行数**: 0
- **说明**: akshare 1.18.64 模块无 stock_lhb_ggtj_em 属性, 仅 stock_lhb_ggtj_sina(symbol='5') 可用
- **错误信息**: module 'akshare' has no attribute 'stock_lhb_ggtj_em'

```
Traceback (most recent call last):
  File "D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_datasource_gap__20260811\_temp_probe_final.py", line 66, in <module>
    df2 = ak.stock_lhb_ggtj_em(start_date="20260801", end_date="20260810")
```

### stock_lhb_stock_statistic_em

- **是否可用**: 可用
- **字段数**: 20
- **样例行数**: 772
- **样例列名前5**: 序号,代码,名称,最近上榜日,收盘价
- **空值最高的3列+率**: 序号=0.0000;代码=0.0000;名称=0.0000

## 结论

- 3 个接口中 **2/3** 可用
- 失败摘要:
  - stock_lhb_ggtj_em: akshare 1.18.64 模块无 stock_lhb_ggtj_em 属性, 仅 stock_lhb_ggtj_sina(symbol='5') 可用; Err=module 'akshare' has no attribute 'stock_lhb_ggtj_em'

## 脚手架脚本

- 脚本路径: `scaffold_longhubang_akshare_daily.py`
- probe 模式: dry-run 探活 + QC 摘要 TSV -> `out_longhubang_dryrun/`
- fetch 模式: `raise NotImplementedError` 禁止实跑