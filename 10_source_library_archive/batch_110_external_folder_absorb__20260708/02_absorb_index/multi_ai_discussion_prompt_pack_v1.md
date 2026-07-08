# 多 AI 讨论包 v1

更新时间：2026-07-08

## 目的

- 以“现有资产清单 + 明确缺口 + 可量化降级 + 可复现验收”为前置，把外部学习与资料扩展变成可吸收的结构化产物。

## 固定前置事实（必须带给其他 AI）

- 已有对象卡（12张）：`CHZL_BSD` `BPB` `TKR7` `VP` `YTC` `MFLOW` `INSTB` `VOLFAC` `VOLTARGET` `KELLY` `PERIOD_QUEEN` `ATRATIO`
- 主哲学：
  - 不预测涨跌，只管理风险暴露
  - 必须可复现（同输入同输出）
  - 必须可回测诚实性验证（避免过拟合与未来信息泄露）
- 关键缺口（当前优先）：
  - 宏观 5 维评分
  - 组合层仓管（集中度/相关性/回撤梯子/风险预算）
  - 自动化日报（含持仓诊断、关注池、分歧点与后续实验清单）
  - 偏差分析（AI判断 vs 实际）
  - 跨市场适配（A股/外汇/币/期货）
  - 对象卡统一调度与联动（registry + pipeline + 互锁）
- 参考材料入口：
  - `00_raw_snapshot/MASTER_INDEX_v1.0.md`
  - `00_raw_snapshot/USER_IDEAS_INTEGRATION_v1.0.md`
  - `00_raw_snapshot/TRADING_SYSTEM_BLUEPRINT_v1.0.md`
  - `00_raw_snapshot/MING_CABINET_HYBRID_ARCHITECTURE_v1.0.md`

## 讨论题 1：对象卡补完（不是泛泛找老师）

### 问题

- 对于每张对象卡，哪些交易博主/视频体系最适合补：
  - 定义
  - 字段
  - 失效模式
  - 样本案例

### 输出格式（TSV）

- `object_card`
- `creator`
- `platform`
- `learnable_module`
- `can_quantize_now`
- `required_data`
- `ashare_proxy`
- `why_fit_our_gap`
- `why_not_full_copy`

## 讨论题 2：模块缺口 → 学习来源

### 问题

- 谁最适合补“宏观评分框架”？
- 谁最适合补“组合资产配置/仓位管理”？
- 谁最适合补“风险暴露而非预测”的哲学和实现？
- 谁最适合补“多周期执行，而不是纯日线”？
- 谁最适合补“日报/复盘/偏差分析”的工作流？

### 输出格式（TSV）

- `gap_module`
- `candidate_sources`
- `what_to_extract`
- `quantizable_subset`
- `required_data`
- `acceptance_test_idea`
- `notes`

## 讨论题 3：强制三分流（否则不可吸收）

### 输出格式（TSV）

- `source`
- `content_unit`
- `bucket`（`QUANTIZABLE_NOW / RESEARCH_ONLY / NOT_QUANT_YET`）
- `why`
- `required_data`
- `fallback_proxy`
- `do_not_copy_warning`

## 讨论题 4：终局扩展（模块级借鉴，而非整套移植）

### 问题

- 终局是“私人投资管家 + 三权分立讨论 + 内阁裁决”，现有 A股纯多头框架如何扩成跨市场版本？
- 哪些模块必须保持统一？
- 哪些模块应该按市场分叉？
- 哪些交易系统适合作为“模块级借鉴”，而不是整套移植？

### 输出格式（TSV）

- `module`
- `keep_unified_or_fork`
- `why`
- `candidate_systems_to_learn`
- `what_to_extract`
- `acceptance_gate`
