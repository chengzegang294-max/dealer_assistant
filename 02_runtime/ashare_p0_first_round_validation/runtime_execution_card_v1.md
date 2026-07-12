# AShare P0 First Round Validation Execution Card v1

## 生成入口

- 仓库级正式入口：
  - `00_entry/A股_P0_功能合同__20260711.md`
- repo 级执行合同：
  - `00_entry/A股_P0_离线验证执行卡__20260712.md`
  - `00_entry/A股_P0_离线验证结论门槛__20260712.md`
- `INDEX_NOTE`:
  - `02_runtime/ashare_p0_first_round_validation/README.md`
  - `02_runtime/ashare_p0_first_round_validation/reports/README.md`

## 当前范围

- 当前任务：
  - `T01 量价阈值触发密度`
  - `T02 主力资金主触发`
  - `T03 业绩事件可得性与降级`
  - `T04 行业轮动阈值敏感度`
  - `T05 历史类比样本门槛`
- 当前输入：
  - A 股日线行情
  - 量能字段
  - 行业映射字段
  - 资金字段
  - 业绩事件字段
- 当前输出：
  - 单项结果页
  - 首轮汇总结论页
  - 归档统计表

## 当前作用

- 把 `00_entry` 的字段、样本、输出模板和门槛文档接到实际 runtime 工作线。
- 固定首轮结果页应该落在哪里，避免“脚本先跑了，结果不知道放哪”。
- 当前只提供最小执行骨架，不假装脚本已经齐全。

## 推荐运行顺序

1. `T01`
2. `T02`
3. `T04`
4. `T05`
5. `T03`
6. `first_round_summary`

## 当前结果入口

- `reports/T01_result_stub_v1.md`
- `reports/T02_result_stub_v1.md`
- `reports/T03_availability_and_downgrade_stub_v1.md`
- `reports/T04_result_stub_v1.md`
- `reports/T05_result_stub_v1.md`
- `reports/first_round_summary_stub_v1.md`

## 当前产物边界

- `reports/`：
  - 放结构化结果页和汇总结论
- `artifacts/`：
  - 放统计表、日志、导出文件和后续批次归档说明
- 当前不把真实结果直接回写到 `00_entry`

## 证据强度

- 当前 stub 文档：`INDEX_NOTE`
- 当前尚未生成的结果表：`not_generated_yet`
- 后续离线新跑结果：`hard`
- 若回收旧结果：`historical_recovered`
