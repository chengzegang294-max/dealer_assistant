# AShare P0 First Round Validation Data Notes

更新时间：2026-07-12

## 用途

- 这里放 A 股 P0 首轮离线验证的输入模板、字段合同副本和后续手工整理的宽表。
- 当前先承接 `T02` 的统一输入合同模板，不把临时中转文件直接扔到根目录。

## 当前文件

- `t02_fund_flow_input_contract_v1.csv`
- `t02_multi_symbol_sample_v1.csv`
- `t02_real_input_sources_manifest_v1.tsv`
- `t02_real_input_assembly_note_v1.md`
- `t02_sources/README.md`

## 使用边界

- 当前允许放：
  - 可复用输入模板
  - 真实源表 manifest
  - 字段来源与拼接说明
  - 真实源表落点目录
  - 手工整理后的首轮验证宽表
  - 真实源抓取失败 metadata
- 当前不建议放：
  - 一次性下载缓存
  - 临时筛选中转表
  - 没有字段说明的大表

## 当前回链

- `00_entry/A股_P0_首轮数据字段清单__20260712.md`
- `00_entry/A股_P0_离线验证执行卡__20260712.md`
- `02_runtime/ashare_p0_first_round_validation/runtime_execution_card_v1.md`

## 当前状态

- `t02_sources/` 已建好 `moneyflow_tushare / northbound_tushare / industry_tushare` 三类真实源落点。
- 当前已跑通：
  - 单标的 `moneyflow` 真源
  - 多标的 `moneyflow_batch` 真源
  - `northbound` 真源
  - `industry` 真源
- 当前 latest 真实宽表已切换为 `5` 标的样本：
  - `moneyflow_batch__sample5__20260501_20260531.csv`
- `artifacts/t02_input_prepare/t02_fund_flow_input_normalized_latest.csv` 继续保留为模板级底表，不再充当 latest 真实资金源。
