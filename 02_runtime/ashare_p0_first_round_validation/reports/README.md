# AShare P0 First Round Validation Reports

更新时间：2026-07-12

## 用途

- 这里放 A 股 P0 首轮离线验证的单项结果页和首轮汇总结论页。
- 当前先放 stub，后续真实跑数结果按同结构原位增强。

## 当前文件

- `T01_result_stub_v1.md`
- `T02_result_stub_v1.md`
- `T03_availability_and_downgrade_stub_v1.md`
- `T04_result_stub_v1.md`
- `T05_result_stub_v1.md`
- `first_round_summary_stub_v1.md`

## 使用规则

- 每个任务至少保留一页结果。
- 结果页必须能回到：
  - 输入字段
  - 样本范围
  - 输出模板
  - 结论门槛
- 不在这里堆大体量 csv 或临时中转表。

## 当前回链

- runtime 执行卡：
  - `02_runtime/ashare_p0_first_round_validation/runtime_execution_card_v1.md`
- 离线验证输出模板：
  - `00_entry/A股_P0_离线验证输出模板__20260712.md`
- 离线验证结论门槛：
  - `00_entry/A股_P0_离线验证结论门槛__20260712.md`
