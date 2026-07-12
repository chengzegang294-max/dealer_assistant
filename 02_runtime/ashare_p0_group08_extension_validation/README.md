# AShare P0 GROUP_08 Extension Validation Runtime

更新时间：2026-07-13

## 用途

- 这里放 `GROUP_08` 扩展验证的 runtime 骨架、执行卡、结果页 stub 和后续脚本入口。
- 这一层负责把 `00_entry` 的扩展验证任务包接到可执行工作线。

## 当前范围

- 当前只覆盖：
  - `E01 事件驱动扩展验证`
  - `E02 市场择时 gate 候选验证`
  - `E03 相关性选股 -> 动态因子联动验证`
- 当前先落：
  - `runtime_execution_card_v1.md`
  - `artifact_index_v1.tsv`
  - `reports/`
  - `artifacts/`
- 当前不含：
  - 真实运行脚本
  - 自动化 pipeline
  - 大体量统计产物

## 当前状态

- 当前是扩展验证骨架，尚未开始真实跑数。
- 当前作用是让 `GROUP_08` 合同从桥接层继续推进到可执行验证线。

## 当前默认读法

1. 先看 `00_entry/A股_P0_GROUP_08研究合同桥接与验证映射卡__20260713.md`
2. 再看 `00_entry/A股_P0_GROUP_08扩展验证任务包__20260713.md`
3. 再看 `00_entry/A股_P0_GROUP_08扩展验证执行卡__20260713.md`
4. 再看 `runtime_execution_card_v1.md`
5. 最后把结果落到 `reports/` 和 `artifacts/`

## 当前回链

- GROUP_08 研究合同桥接与验证映射卡：
  - `00_entry/A股_P0_GROUP_08研究合同桥接与验证映射卡__20260713.md`
- GROUP_08 扩展验证任务包：
  - `00_entry/A股_P0_GROUP_08扩展验证任务包__20260713.md`
- GROUP_08 扩展验证执行卡：
  - `00_entry/A股_P0_GROUP_08扩展验证执行卡__20260713.md`
