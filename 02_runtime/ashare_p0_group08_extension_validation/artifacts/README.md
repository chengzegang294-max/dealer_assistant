# AShare P0 GROUP_08 Extension Validation Artifacts

更新时间：2026-07-13

## 用途

- 这里放 `GROUP_08` 扩展验证后续产生的字段映射表、样本对账表、日志和辅助统计。
- 当前先只定义边界，不预创建大体量产物。

## 推荐子目录

- `event_driven_extension/`
- `market_timing_gate/`
- `corr_dynamic_linkage/`

## 使用规则

- 大体量 `csv / tsv / log` 只放这里，不回灌到 `00_entry`。
- 每批产物都应能回指到：
  - 任务页
  - 执行卡
  - 结果页
  - 生成脚本或手工整理入口

## 当前回链

- runtime 执行卡：
  - `02_runtime/ashare_p0_group08_extension_validation/runtime_execution_card_v1.md`
- artifact 索引：
  - `02_runtime/ashare_p0_group08_extension_validation/artifact_index_v1.tsv`
