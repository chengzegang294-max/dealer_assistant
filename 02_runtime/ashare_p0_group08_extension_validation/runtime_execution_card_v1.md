# AShare P0 GROUP_08 Extension Validation Execution Card v1

## 生成入口

- repo 级执行合同：
  - `00_entry/A股_P0_GROUP_08扩展验证任务包__20260713.md`
  - `00_entry/A股_P0_GROUP_08扩展验证执行卡__20260713.md`
  - `00_entry/A股_P0_GROUP_08研究合同桥接与验证映射卡__20260713.md`
- `INDEX_NOTE`:
  - `02_runtime/ashare_p0_group08_extension_validation/README.md`
  - `02_runtime/ashare_p0_group08_extension_validation/artifact_index_v1.tsv`
  - `02_runtime/ashare_p0_group08_extension_validation/reports/README.md`

## 当前范围

- 当前任务：
  - `E01 事件驱动扩展验证`
  - `E02 市场择时 gate 候选验证`
  - `E03 相关性选股 -> 动态因子联动验证`
- 当前输入：
  - 研究合同字段家族
  - 字段映射说明
  - 扩展验证结论标签
- 当前输出：
  - 单项结果页
  - 扩展汇总结论页

## 当前作用

- 把 `00_entry` 的扩展验证任务包接到实际 runtime 工作线。
- 固定扩展结果页应该落在哪里，避免新验证线再次混进首轮 runtime。
- 当前只提供最小执行骨架，不假装脚本已经齐全。

## 推荐运行顺序

1. `E01`
2. `E02`
3. `E03`
4. `group08_extension_summary`

## 当前结果入口

- `reports/E01_event_driven_extension_stub_v1.md`
- `reports/E02_market_timing_gate_stub_v1.md`
- `reports/E03_corr_dynamic_linkage_stub_v1.md`
- `reports/group08_extension_summary_stub_v1.md`

## 当前产物边界

- `reports/`：
  - 放结构化结果页和扩展汇总结论
- `artifacts/`：
  - 放后续字段映射表、日志和样本对账表
- 当前不把真实结果直接回写到 `00_entry`
