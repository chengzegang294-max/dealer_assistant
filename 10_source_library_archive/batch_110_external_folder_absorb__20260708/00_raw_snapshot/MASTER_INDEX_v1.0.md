# 全仓库文件总索引 (MASTER INDEX)

> **生成时间**: 2026-07-07
> **仓库路径**: `E:\downloads\Desktop\找系统\特征`
> **总文件数**: 110 个 (88个 .md + 22个 .py)
> **状态**: 活跃开发中 — 12张对象卡全部编码完成，系统骨架完整

---

## 一、对象卡文件 (Object Cards) — 系统核心执行层

12张可运行对象卡，统一接口 `calculate(raw_input) → ObjectCardOutput`。

| # | 文件 | 对象ID | 功能 | 状态 |
|---|------|--------|------|------|
| 1 | `OBJECT_CARD_PERIOD_QUEEN_P0_F__CycleStateSystem_v1.0.md` | PERIOD_QUEEN_P0_F | 七态周期状态识别（系统心脏） | ✅ 已编码 |
| 2 | `OBJECT_CARD_VOLFAC_P0_A__VolatilityFactor_v1.0.md` | VOLFAC_P0_A | 波动率因子（id2_std_3m→年化→分位） | ✅ 已编码 |
| 3 | `OBJECT_CARD_VOLTARGET_P0_R__VolatilityTargeting_v1.0.md` | VOLTARGET_P0_R | 波动率目标仓位（position_scalar = target/current） | ✅ 已编码 |
| 4 | `OBJECT_CARD_CHZL_BSD_P0_E__Chanlun_Buy_Sell_Signals_v1.0.md` | CHZL_BSD_P0_E | 缠论分型/笔/中枢，1Buy/2Buy/3Buy | ✅ 已编码 |
| 5 | `OBJECT_CARD_BPB_P0_E__Brooks_Breakout_Pullback_v1.0.md` | BPB_P0_E | 突破回调质量（38.2%/50%/61.8%） | ✅ 已编码 |
| 6 | `OBJECT_CARD_TKR7_P0_E__AO_Divergence_v1.0.md` | TKR7_P0_E | AO背离检测（常规+隐藏） | ✅ 已编码 |
| 7 | `OBJECT_CARD_MFLOW_P0_A__MoneyFlow_v1.0.md` | MFLOW_P0_A | 资金流向（主力流入/流出/早盘意图） | ✅ 已编码 |
| 8 | `OBJECT_CARD_INSTB_P0_A__InstitutionalBehavior_v1.0.md` | INSTB_P0_A | 机构行为（吸筹/派发，季报+OHLCV） | ✅ 已编码 |
| 9 | `OBJECT_CARD_KELLY_P0_R__KellyCriterion_v1.0.md` | KELLY_P0_R | 半凯利仓位，连续亏损降级 | ✅ 已编码 |
| 10 | `OBJECT_CARD_VP_P0_E__VolumeProfile_v1.0.md` | VP_P0_E | 成交量分布（POC/VAH/VAL/HVN/LVN） | ✅ 已编码 |
| 11 | `OBJECT_CARD_YTC_P0_E__YTC_Microstructure_v1.0.md` | YTC_P0_E | 微观结构（TST/BOF/BP/P） | ✅ 已编码 |
| 12 | `OBJECT_CARD_ATRATIO_P0_A__ActiveTradeRatio_v1.0.md` | ATRATIO_P0_A | 活跃度比率（A股纯多头空信号） | ✅ 已编码 |

---

## 二、可运行Python代码 (Prototypes)

| # | 文件 | 功能 | 依赖 | 状态 |
|---|------|------|------|------|
| 1 | `object_card_period_queen.py` | PeriodQueen 完整实现（25KB） | numpy | ✅ 验证通过 |
| 2 | `object_card_volfac.py` | VolFac 波动率因子（17KB） | numpy | ✅ 验证通过 |
| 3 | `object_card_voltarget.py` | VolTarget 仓位管理（24KB） | numpy | ✅ 验证通过 |
| 4 | `object_card_chzl_bsd.py` | 缠论分型实现 | numpy | ✅ 验证通过 |
| 5 | `object_card_bpb.py` | Brooks突破回调 | numpy | ✅ 验证通过 |
| 6 | `object_card_tkr7.py` | AO背离检测 | numpy | ✅ 验证通过 |
| 7 | `object_card_mflow.py` | 资金流向（真实/模拟双模式） | - | ✅ 验证通过 |
| 8 | `object_card_instb.py` | 机构行为 | - | ✅ 验证通过 |
| 9 | `object_card_kelly.py` | 凯利公式 | numpy | ✅ 验证通过 |
| 10 | `object_card_vp.py` | 成交量分布 | numpy | ✅ 验证通过 |
| 11 | `object_card_ytc.py` | YTC微观结构 | - | ✅ 验证通过 |
| 12 | `object_card_atratio.py` | 活跃度比率 | - | ✅ 验证通过 |
| 13 | `data_pipeline.py` | 数据管道（Simulated/AkShare/Tushare三源） | akshare, numpy | ⚠️ 远程不可用，本地正常 |
| 14 | `governance_architecture.py` | 治理架构运行时 | - | ✅ 基础实现 |
| 15 | `prototype_console.py` | 控制台v1.0 | - | ✅ 可运行 |
| 16 | `prototype_console_v2.py` | 控制台v2.0（五态面板+投票模拟+事件流） | - | ✅ 可运行 |
| 17 | `rkx_analysis.py` | 瑞芯微对象卡聚合分析演示 | numpy | ✅ 可运行 |

---

## 三、系统设计文档 (Architecture & Design)

### 3.1 核心架构
| 文件 | 说明 |
|------|------|
| `TRADING_SYSTEM_BLUEPRINT_v1.0.md` | **系统总蓝图** — 五层端到端链路串联（数据→对象卡→投票→风控→执行） |
| `SYSTEM_ARCHITECTURE_DRAFT.md` | 系统架构初稿 |
| `MING_CABINET_HYBRID_ARCHITECTURE_v1.0.md` | 明柜混合架构设计 |
| `GOVERNANCE_ARCHITECTURE_CHINA_v1.0.md` | A股治理架构 |
| `GOVERNANCE_ARCHITECTURE_OPTIONS_v1.0.md` | 期权治理架构 |
| `RISK_ARCHITECTURE_P0_R_v1.0.md` | 风控架构 |

### 3.2 回测与归因
| 文件 | 说明 |
|------|------|
| `BACKTEST_FRAMEWORK_DESIGN_v1.0.md` | 回测框架设计 |
| `BACKTEST_AND_ATTRIBUTION_DESIGN_v1.0.md` | 回测与归因设计 |
| `BACKTEST_ROBUSTNESS_v1.0.md` | 回测鲁棒性 |
| `BACKTEST_REPORT_TEMPLATE_v1.0.md` | 回测报告模板 |
| `OBJECT_CARD_BACKTEST_SCHEDULE_v1.0.md` | 对象卡回测计划 |

### 3.3 数据与ETL
| 文件 | 说明 |
|------|------|
| `DATA_PIPELINE_ETL_v1.0.md` | 数据管道ETL设计 |
| `DATA_PROVIDER_GUIDE_v1.0.md` | 数据供应商指南 |
| `DATA_AVAILABILITY_AUDIT_v1.0.md` | 数据可用性审计 |
| `ALTERNATIVE_DATA_v1.0.md` | 另类数据 |

### 3.4 策略与投票
| 文件 | 说明 |
|------|------|
| `STRATEGY_BUNDLES_v1.0.md` | 策略包设计 |
| `STRATEGY_DESIGN_REFERENCE_v1.0.md` | 策略设计参考v1 |
| `STRATEGY_DESIGN_REFERENCE_v2.0.md` | 策略设计参考v2 |
| `VOTE_DECISION_TABLE_P0_E_v1.0.md` | 投票决策表 |
| `GAS_12_INDICATOR_MAP_P0_A_v1.0.md` | 12指标映射表 |

---

## 四、外部策略原材料 (External Strategy Raw Materials)

多版本迭代的外部策略参考文档，记录系统进化轨迹。

| 文件 | 版本 | 说明 |
|------|------|------|
| `EXTERNAL_STRATEGY_RAW_MATERIAL_v1.0.md` | v1.0 | 初版外部策略原材料 |
| `EXTERNAL_STRATEGY_RAW_MATERIAL_v2.0.md` | v2.0 | 第二版 |
| `EXTERNAL_STRATEGY_RAW_MATERIAL_v3.0.md` | v3.0 | 第三版 |
| `EXTERNAL_STRATEGY_RAW_MATERIAL_v4.0.md` | v4.0 | 第四版 |
| `EXTERNAL_STRATEGY_RAW_MATERIAL_v5.0.md` | v5.0 | 第五版 |
| `EXTERNAL_STRATEGY_RAW_MATERIAL_v6.0.md` | v6.0 | 第六版 |
| `EXTERNAL_STRATEGY_RAW_MATERIAL_v7.0.md` | v7.0 | 最新版 |
| `EXTERNAL_SYSTEM_FUNCTION_MAP_v0.1.md` | v0.1 | 外部系统功能映射 |
| `EXTERNAL_SYSTEM_REFERENCE_v1.0.md` | v1.0 | 外部系统参考 |
| `EXTERNAL_SYSTEM_REFERENCE_v2.0.md` | v2.0 | 外部系统参考v2 |

---

## 五、GLM 交付物与任务记录

GLM（前期AI助手）产生的各类交付文档和任务指令。

| 文件 | 说明 |
|------|------|
| `GLM_MATERIAL_PACKAGE_INDEX.md` | GLM材料包索引 |
| `GLM_TASK_INSTRUCTION.md` | GLM任务总指令 |
| `GLM_SEARCH_TASK_INSTRUCTION.md` | GLM搜索任务指令 |
| `GLM_SEARCH_01_执行层补充_跨市场_风控_另类数据_v1.0.md` | 搜索任务01 |
| `GLM_TASK_02_CHANLUN_OBJECT_CARD.md` | 任务02：缠论对象卡 |
| `GLM_TASK_04_CHANLUN_FULL_QUANT_FORMULA.md` | 任务04：缠论全量化公式 |
| `GLM_TASK_05_TK_FOREX_OPTIMIZATION.md` | 任务05：TK外汇优化 |
| `GLM_TASK_06_BACKTEST_FRAMEWORK.md` | 任务06：回测框架 |
| `GLM_TASK_07_A股特殊因子字段化提取.md` | 任务07：A股因子提取 |
| `GLM_TASK_08_第二优先级执行层对象卡.md` | 任务08：第二优先级对象卡 |
| `GLM_TASK_09_A股跨市场适配审计.md` | 任务09：跨市场适配审计 |
| `GLM_DELIVERY_04_CHANLUN_FULL_QUANT_v1.0.md` | 交付04：缠论全量化 |
| `GLM_DELIVERY_05_TK_FOREX_OPTIMIZATION_v1.0.md` | 交付05：TK外汇优化 |
| `GLM_DELIVERY_06_TIER1_EXECUTION_FIELDS_v1.0.md` | 交付06：Tier1执行字段v1 |
| `GLM_DELIVERY_07_TIER1_EXECUTION_FIELDS_v2.0.md` | 交付07：Tier1执行字段v2 |
| `GLM_DELIVERY_09_A股跨市场适配审计与因子提取_v1.0.md` | 交付09：跨市场适配 |

---

## 六、审计与一致性检查

| 文件 | 说明 |
|------|------|
| `A_AUDIT_REPORT_v1.0.md` | **92份文档一致性审计报告** — VOLFAC/ATRATIO补充标准输出字段 |
| `B_EXPERIMENT_B_EXP_20260707_223225_REPORT.md` | B实验报告（数据管道验证） |
| `INDEX_v2.0.md` | 仓库索引v2 |
| `DOCUMENT_CATALOG_HANDBOOK_v1.0.md` | 文档目录手册 |

---

## 七、功能模块设计文档

| 文件 | 模块 | 说明 |
|------|------|------|
| `A5_FUNDAMENTAL_INTEGRATION_v1.0.md` | 基本面 | A5组基本面整合 |
| `CHZL_ZS_量化公式与互锁视图_v1.0.md` | 缠论 | 缠论中枢量化公式与互锁 |
| `CONVERTIBLE_BOND_v1.0.md` | 可转债 | 可转债模块 |
| `DAILY_REPORT_GENERATOR_v1.0.md` | 日报 | 日报生成器 |
| `DEPLOYMENT_AND_OPERATIONS_v1.0.md` | 部署运维 | 部署与运维 |
| `DY_INTEGRATION_v1.0.md` | 抖音 | 抖音整合（如有） |
| `EMPEROR_CONSOLE_UI_v1.0.md` | UI | 控制台UI设计 |
| `ERROR_HANDLING_DEGRADATION_v1.0.md` | 容错 | 错误处理与降级 |
| `GLOBAL_MACRO_v1.0.md` | 宏观 | 全球宏观 |
| `INDEX_ENHANCEMENT_v1.0.md` | 指增 | 指数增强 |
| `LIVE_TRADING_SYSTEM_DESIGN_v1.0.md` | 实盘 | 实盘交易系统设计 |
| `MACRO_ENVIRONMENT_SCORER_v1.0.md` | 宏观 | 宏观环境评分器 |
| `MTF_SEB_v0.1.md` | 多时间框架 | MTF SEB分析 |
| `PERFORMANCE_OPTIMIZATION_GUIDE_v1.0.md` | 性能 | 性能优化指南 |
| `REGULATORY_COMPLIANCE_v1.0.md` | 合规 | 监管合规 |
| `SENTIMENT_INDICATORS_v1.0.md` | 情绪 | 情绪指标 |
| `TCA_DESIGN_v1.0.md` | 交易成本 | TCA设计 |
| `TESTING_SPECIFICATION_v1.0.md` | 测试 | 测试规范 |
| `TRADING_SYSTEM_COMPARISON_DESIGN_v1.0.md` | 对比 | 交易系统对比设计 |
| `USER_IDEAS_INTEGRATION_v1.0.md` | 用户需求 | 用户想法整合 |
| `USER_OPERATION_MANUAL_v1.0.md` | 手册 | 用户操作手册 |
| `TK外汇核心概念对象卡_Kimi版_v1.0.md` | TK外汇 | TK外汇核心概念 |

---

## 八、编程与开发指令

| 文件 | 说明 |
|------|------|
| `MASTER_PROGRAMMING_INSTRUCTION_v1.0.md` | **主编程指令** — 系统开发总规范 |
| `PROGRAMMING_AI_ULTIMATE_TASK_PACKAGE_v1.0.md` | AI终极任务包 |
| `README_FOR_PROGRAMMING_AI.md` | 编程AI README |
| `SYSTEM_ENHANCEMENT_DESIGN_v1.0.md` | 系统增强设计 |
| `全仓库功能映射大表_v1.0.md` | 功能映射大表v1 |
| `全仓库功能映射大表_v2.0.md` | 功能映射大表v2 |
| `执行层字段化优先级清单.md` | 执行层字段化优先级 |
| `后续方向建议清单.md` | 后续方向建议 |

---

## 九、其他文档

| 文件 | 说明 |
|------|------|
| `Code X➕投研=私人投研管家_导出.md` | CodeX投研管家导出 |
| `SEARCH_RESERVE_LIST_HIJKLMNOPQ_v1.0.md` | 搜索储备清单（打新/因子库/事件驱动） |

---

## 十、系统状态速览

### 已完成 ✅
- [x] 12张对象卡全部编码完成并通过验证
- [x] 数据管道原型（`data_pipeline.py`）
- [x] 控制台v2.0（`prototype_console_v2.py`）
- [x] 系统蓝图（`TRADING_SYSTEM_BLUEPRINT_v1.0.md`）
- [x] 92份文档一致性审计
- [x] 瑞芯微对象卡聚合分析演示

### 待完成 ⏳
- [ ] `ObjectCardRegistry` 统一调度器 — 输入股票代码自动跑完全部对象卡
- [ ] `BACKTEST_FRAMEWORK` CSCV-PBO回测诚实性检验框架
- [ ] 对象卡互锁联调（CHZL_BSD × BPB × TKR7 共振检测）
- [ ] PERIOD_QUEEN 接入真实涨跌停数据替代模拟统计
- [ ] A股纯多头 Sell信号收口一致性检查

### 已知问题 ⚠️
- **AkShare远程不可用**: 远程环境爬虫被防火墙拦截，已内置 fallback 到 `SimulatedDataSource`
- **对象卡输出字段格式不一致**: 部分 `signal_strength` 值范围有差异，统一收口时需注意
- **PERIOD_QUEEN状态识别精度**: 简化实现基于OHLCV统计特征模拟，生产环境需接入真实涨跌停榜单

---

## 十一、文件命名规范

```
OBJECT_CARD_{OBJECT_ID}__{Description}_v{version}.md
{Subsystem}_{Description}_v{version}.md
object_card_{short_name}.py
```

### 对象ID编码规则
- `P0_F` — PeriodQueen (环境识别层)
- `P0_E` — Execution (执行层，纯技术)
- `P0_A` — A股特殊因子
- `P0_R` — Risk (风控层)

---

*本索引由系统自动生成，随仓库演进定期更新。*
