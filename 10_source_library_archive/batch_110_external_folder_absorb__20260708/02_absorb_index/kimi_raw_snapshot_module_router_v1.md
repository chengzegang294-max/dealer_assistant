# Kimi Raw Snapshot Module Router v1

更新时间：2026-07-08

## 目的

- 对 `00_raw_snapshot/` 做“模块级重分类索引”，先把资料从“堆文件”变成“可导航的模块树”。
- 不改任何原文文件；只新增索引与路由。

## 模块树（先跑通导航）

### M00 索引与总览

- `MASTER_INDEX_v1.0.md`
- `INDEX_v2.0.md`
- `DOCUMENT_CATALOG_HANDBOOK_v1.0.md`
- 动作：以 `MASTER_INDEX` 为总入口，其他作为辅助检索入口。

### M01 对象卡定义（12张）

- `OBJECT_CARD_*_v1.0.md`
- 动作：后续重做“我们自己的对象卡版本”，并补字段合同+验收样本；原文只作为来源证据。

### M02 回测与稳健性

- `BACKTEST_FRAMEWORK_DESIGN_v1.0.md`
- `BACKTEST_ROBUSTNESS_v1.0.md`
- `BACKTEST_AND_ATTRIBUTION_DESIGN_v1.0.md`
- `BACKTEST_REPORT_TEMPLATE_v1.0.md`
- `OBJECT_CARD_BACKTEST_SCHEDULE_v1.0.md`
- 动作：抽出“硬门槛/失败模式/验收模板”写入内部合同层，不直接照搬结构。

### M03 数据与ETL

- `DATA_PIPELINE_ETL_v1.0.md`
- `DATA_PROVIDER_GUIDE_v1.0.md`
- `DATA_AVAILABILITY_AUDIT_v1.0.md`
- `ALTERNATIVE_DATA_v1.0.md`
- 动作：重做“数据可用性审计表”（成本/频率/缺失策略/降级），作为跨市场扩展的地基。

### M04 治理与制度（明柜）

- `TRADING_SYSTEM_BLUEPRINT_v1.0.md`
- `MING_CABINET_HYBRID_ARCHITECTURE_v1.0.md`
- `GOVERNANCE_ARCHITECTURE_CHINA_v1.0.md`
- `GOVERNANCE_ARCHITECTURE_OPTIONS_v1.0.md`
- 动作：把“制度切换触发器/审查门槛/日志要求”抽成可执行合同与字段，不停留在比喻叙事。

### M05 风控与仓管

- `RISK_ARCHITECTURE_P0_R_v1.0.md`
- `TCA_DESIGN_v1.0.md`
- `REGULATORY_COMPLIANCE_v1.0.md`
- 动作：重做“组合层仓管”缺口清单（集中度/相关性/风险预算/回撤梯子）并写验收断言。

### M06 日报与控制台

- `DAILY_REPORT_GENERATOR_v1.0.md`
- `EMPEROR_CONSOLE_UI_v1.0.md`
- `ERROR_HANDLING_DEGRADATION_v1.0.md`
- `DEPLOYMENT_AND_OPERATIONS_v1.0.md`
- 动作：先把日报的输出字段与固定结构写成合同，再谈 UI。

### M07 用户想法整合（终局需求）

- `USER_IDEAS_INTEGRATION_v1.0.md`
- `Code X➕投研=私人投研管家_导出.md`
- `问题2.txt` / `问题3.txt`
- 动作：以“终局需求→模块缺口→字段与验收”重写内部方向，不直接复述 Kimi。

### M08 外部参考与搜索/GLM产物

- `EXTERNAL_SYSTEM_REFERENCE_*.md`
- `EXTERNAL_STRATEGY_RAW_MATERIAL_v*.md`
- `GLM_*`
- 动作：一律先降级为“研究参考”，只抽可量化子集进入候选清单。

### M09 审计与一致性检查

- `A_AUDIT_REPORT_v1.0.md`
- `B_EXPERIMENT_*`
- 动作：把“字段不一致/已知问题/修复建议”抽成内部任务板，不直接当成完成态。

## 下一步（连续推进）

1. 针对每个模块抽出“必须字段/必须验收/降级策略”三件套。
2. 把抽取结果落到 `02_absorb_index/` 的 TSV（可用于多 AI 讨论与工程排期）。
