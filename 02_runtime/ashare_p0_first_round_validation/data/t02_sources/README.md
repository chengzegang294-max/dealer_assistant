# T02 Real Source Landing Notes

更新时间：2026-07-12

## 用途

- 这里放 `T02` 首份真实源表的落点，不再把真实资金表混进模板目录。
- 当前优先承接：
  - `moneyflow_tushare/`
  - `northbound_tushare/`
  - `industry_tushare/`

## 当前边界

- 允许放：
  - 可复用真实源 CSV
  - 对应 metadata JSON
- 不建议放：
  - 一次性终端导出
  - 未经命名约束的下载缓存
  - 临时 Excel 转存中间件

## 当前回链

- `02_runtime/ashare_p0_first_round_validation/data/t02_real_input_sources_manifest_v1.tsv`
- `02_runtime/ashare_p0_first_round_validation/data/t02_real_input_assembly_note_v1.md`
- `02_runtime/ashare_p0_first_round_validation/build_t02_real_input_v1.py`

## 当前状态

- 当前已完成三条 fetcher 的首轮实跑：
  - `moneyflow_tushare/t02_moneyflow_tushare__000001_SZ__20260501_20260531__metadata.json`
  - `northbound_tushare/t02_northbound_tushare__20260501_20260531__metadata.json`
  - `industry_tushare/t02_industry_map_tushare__list_status_L__metadata.json`
- 当前三条 metadata 的统一结论：
  - `status = failed`
  - `token_source = missing`
  - `failure_reason = tushare_token_missing`
- 当前这里已经有硬证据说明“抓取入口存在且已尝试”，但还没有真实 CSV。
