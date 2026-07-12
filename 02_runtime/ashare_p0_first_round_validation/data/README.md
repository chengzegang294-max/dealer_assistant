# AShare P0 First Round Validation Data Notes

更新时间：2026-07-12

## 用途

- 这里放 A 股 P0 首轮离线验证的输入模板、字段合同副本和后续手工整理的宽表。
- 当前先承接 `T02` 的统一输入合同模板，不把临时中转文件直接扔到根目录。

## 当前文件

- `t02_fund_flow_input_contract_v1.csv`

## 使用边界

- 当前允许放：
  - 可复用输入模板
  - 手工整理后的首轮验证宽表
- 当前不建议放：
  - 一次性下载缓存
  - 临时筛选中转表
  - 没有字段说明的大表

## 当前回链

- `00_entry/A股_P0_首轮数据字段清单__20260712.md`
- `00_entry/A股_P0_离线验证执行卡__20260712.md`
- `02_runtime/ashare_p0_first_round_validation/runtime_execution_card_v1.md`
