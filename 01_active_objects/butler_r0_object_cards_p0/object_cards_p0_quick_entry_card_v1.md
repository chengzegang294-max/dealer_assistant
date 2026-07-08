# Object Cards P0 简明执行入口卡 v1

## 用途

- 给“12 张对象卡（P0）”在新仓库里继续重做与落地提供最短入口。
- 目标是：先把对象卡的“我们自己的版本”做成可跑 + 可验收；Kimi 版本只作为来源证据。

## 当前不变量

- 不预测涨跌：对象卡输出的是风险暴露与结构确认，不输出“保证上涨”的叙事。
- 先讨论后推进：任何新增体系/买数据/接入新市场，必须先过“讨论先行门槛”。
- 先验收再升级：未补齐验收样本的对象卡不得进入硬门控。

## 当前来源位置（只读）

- 来源快照：
  - `..\..\10_source_library_archive\batch_110_external_folder_absorb__20260708\00_raw_snapshot\`
- 提升归位代码副本（.py，仅作为参考）：
  - `..\..\10_source_library_archive\batch_110_external_folder_absorb__20260708\03_quantize\promoted_code_from_raw_snapshot\`
- 内部重做要求清单：
  - `..\..\10_source_library_archive\batch_110_external_folder_absorb__20260708\02_absorb_index\internal_rebuild_requirements_from_kimi_v1.md`

## 我们要重做的对象卡清单（先从定义与验收样本开始）

- `PERIOD_QUEEN`：环境识别层（未来要接宏观 5 维）
- `VOLFAC`：波动率因子
- `VOLTARGET`：波动率目标仓位（连接 VOLFAC 与风控层）
- `MFLOW`：资金流向（需要数据可用性审计与降级路径）
- `CHZL_BSD`：结构信号（分型/笔/中枢）
- `BPB`：突破回调质量
- `VP`：成交量分布
- `TKR7`：AO 背离
- `YTC`：微观结构（A股需明确数据降级）
- `KELLY`：仓位建议（依赖交易日志与偏差分析）
- `INSTB`：机构行为（方法层）
- `ATRATIO`：A股纯多头语境下默认跳过或降级

## 下一跳（不做长文）

1. 先把 `00_raw_snapshot` 文档按模块重分类成索引（不改原文）。
2. 每张对象卡先补“字段合同 + 最小验收样本 + 可跑入口”。
3. 再做互锁、投票、风控、日报。
