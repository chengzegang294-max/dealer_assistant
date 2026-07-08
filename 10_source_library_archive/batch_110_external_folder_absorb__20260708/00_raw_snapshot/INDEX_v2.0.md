# 📚 投资管家系统文档总索引 v2.1

> **本文档是全部资产的总入口。编程 AI 必须从本文档开始阅读，按顺序查阅。**
> 版本：v2.4 | 最后更新：2026-07-07 | 文档总数：有效 **38** 份 + 历史存档 15 份

---

## 一、阅读顺序（必读 → 选读）

> **⚠️ 重要：编程 AI 不要从本文档开始。从 `PROGRAMMING_AI_ULTIMATE_TASK_PACKAGE_v1.0.md` 开始阅读。**
> 那份文档是"总任务书"，告诉你要先读什么、再读什么、先写什么、再写什么。

```text
编程 AI 阅读顺序（推荐路径）：

第 1 步：终极任务包（PROGRAMMING_AI_ULTIMATE_TASK_PACKAGE_v1.0.md）
         ↓ 按 Phase 读取对应文档
第 2 步：快速启动指南（README_FOR_PROGRAMMING_AI.md）
         ↓
第 3 步：编程总指令书（MASTER_PROGRAMMING_INSTRUCTION_v1.0.md）
         ↓
第 4 步：按当前 Phase 选择文档（见终极任务包 Phase 说明）
```

---

## 二、文档分类索引

### 2.1 🏛️ 纲领层（3 份）— 最高层设计

| 文件名 | 版本 | 状态 | 内容摘要 | 字数 |
|--------|------|------|----------|------|
| `SYSTEM_ARCHITECTURE_DRAFT.md` | v1.0 | ✅ 冻结 | 三层决策架构总览：环境识别→策略选择→执行管理 | ~5K |
| `STRATEGY_BUNDLES_v1.0.md` | v1.0 | ✅ 冻结 | 7 个策略组合定义，绑定 PeriodQueen 七态 | ~4K |
| `VOTE_DECISION_TABLE_P0_E_v1.0.md` | v1.0 | ✅ 冻结 | 8+3 节点 if-then 判定表，ABORT 原因编码 | ~6K |

**冻结意味着**：核心逻辑已确定，编程实现时必须严格遵循，修改需经用户审批。

---

### 2.2 🃏 对象卡（15 张）— 系统核心原子

#### 结构层（5 张）
| 文件名 | 成熟度 | 数据需求 | 状态 |
|--------|--------|----------|------|
| `OBJECT_CARD_CHZL_FX_P0_S__Chanlun_Fenxing_v1.0.md` | `proxy_quantizable_now` | 日 OHLCV | ✅ 可编码 |
| `OBJECT_CARD_CHZL_BI_P0_S__Chanlun_Bi_v1.0.md` | `proxy_quantizable_now` | 日 OHLCV | ✅ 可编码 |
| `OBJECT_CARD_CHZL_ZS_P0_S__Chanlun_Zhongshu_v1.0.md` | `proxy_quantizable_now` | 日 OHLCV | ✅ 可编码 |
| `OBJECT_CARD_CHZL_TREND_P0_S__Chanlun_Trend_v1.0.md` | `proxy_quantizable_now` | 日 OHLCV | ✅ 可编码 |
| `OBJECT_CARD_CHZL_BSD_P0_E__Chanlun_Buy_Sell_Signals_v1.0.md` | `proxy_quantizable_now` | 日 OHLCV + ZS/BI | ✅ 可编码 |

#### 执行层（6 张）
| 文件名 | 成熟度 | 数据需求 | 状态 |
|--------|--------|----------|------|
| `OBJECT_CARD_VP_P0_E__VolumeProfile_v1.0.md` | `proxy_quantizable_now` | 日 OHLCV | ✅ 可编码 |
| `OBJECT_CARD_TKR7_P0_E__AO_Divergence_v1.0.md` | `proxy_quantizable_now` | 日 OHLCV | ✅ 可编码 |
| `OBJECT_CARD_BPB_P0_E__Brooks_Breakout_Pullback_v1.0.md` | `proxy_quantizable_now` | 日 OHLCV + AL Brooks 20 形态 | ✅ 可编码 |
| `OBJECT_CARD_YTC_P0_E__YTC_Microstructure_v1.0.md` | `proxy_quantizable_now` | 日 OHLCV + 60min | ✅ 可编码 |
| `OBJECT_CARD_TK_R6_P0_E__TK_Forex_Pattern_v1.0.md` | `proxy_quantizable_now` | 日 OHLCV | ⚠️ A股适配需审查 |
| `OBJECT_CARD_TK_R7_P0_E__TK_Forex_Pattern_v1.0.md` | `proxy_quantizable_now` | 日 OHLCV | ⚠️ A股适配需审查 |
| `OBJECT_CARD_TK_R8_P0_E__TK_Forex_Pattern_v1.0.md` | `proxy_quantizable_now` | 日 OHLCV | ⚠️ A股适配需审查 |

> 注：TK R6/R7/R8 是外汇书籍概念，A股适配性待验证。编程时先实现 CHZL/VP/TKR7/BPB/YTC。

#### 风控层（2 张）
| 文件名 | 成熟度 | 数据需求 | 状态 |
|--------|--------|----------|------|
| `OBJECT_CARD_KELLY_P0_R__KellyCriterion_v1.0.md` | `proxy_quantizable_now` | 交易日志（历史） | ✅ 可编码 |
| `OBJECT_CARD_VOLTARGET_P0_R__VolatilityTargeting_v1.0.md` | `proxy_quantizable_now` | 日 OHLCV | ✅ 可编码 |

#### 选股层（3 张）
| 文件名 | 成熟度 | 数据需求 | 状态 |
|--------|--------|----------|------|
| `OBJECT_CARD_MFLOW_P0_A__MoneyFlow_v1.0.md` | `proxy_quantizable_now` | Wind 资金流向 | ✅ 可编码 |
| `OBJECT_CARD_VOLFAC_P0_A__VolatilityFactor_v1.0.md` | `proxy_quantizable_now` | 日 OHLCV | ✅ 可编码 |
| `OBJECT_CARD_ATRATIO_P0_A__ActiveTradeRatio_v1.0.md` | `LIMITED` | 日 OHLCV | ⚠️ 仅大盘流动性充足时使用 |
| `OBJECT_CARD_INSTB_P0_A__InstitutionalBehavior_v1.0.md` | `needs_extra_data` | 龙虎榜/Level-2 | 🔶 需额外数据，v1.1 实现 |

#### 过滤器（1 张）
| 文件名 | 成熟度 | 数据需求 | 状态 |
|--------|--------|----------|------|
| `OBJECT_CARD_PERIOD_QUEEN_P0_F__CycleStateSystem_v1.0.md` | `proxy_quantizable_now` | 日 OHLCV + 情绪指标 | ✅ 可编码，系统核心 |

---

### 2.3 🏗️ 架构与参考（18 份）

| 文件名 | 用途 | 优先级 | 状态 |
|--------|------|--------|------|
| `BACKTEST_FRAMEWORK_DESIGN_v1.0.md` | 回测引擎设计：Pipeline、Vote、Risk、Execution | P0 | ✅ 冻结 |
| `OBJECT_CARD_BACKTEST_SCHEDULE_v1.0.md` | Week 1-9 排期表 | P1 | ✅ 冻结 |
| `DATA_AVAILABILITY_AUDIT_v1.0.md` | 11 项数据审计清单 | P0 | ✅ 冻结 |
| `EXTERNAL_SYSTEM_REFERENCE_v1.0.md` | KA-MATS/Quant67/B3/vnpy 外部参考 | P2 | ✅ 参考 |
| `EXTERNAL_SYSTEM_REFERENCE_v2.0.md` | 国内框架全景（vnpy/WT/Hikyuu/Qlib/Backtrader/VectorBT） | P2 | ✅ 新增补充 |
| `EXTERNAL_STRATEGY_RAW_MATERIAL_v1.0.md` | 外部交易策略原始资料库（15个策略，保留Kimi取舍） | P2 | ✅ 新增 |
| `EXTERNAL_STRATEGY_RAW_MATERIAL_v2.0.md` | 外部交易策略原始资料库v2（微观结构/情绪/板块轮动） | P2 | ✅ 新增 |
| `EXTERNAL_STRATEGY_RAW_MATERIAL_v3.0.md` | 外部交易策略原始资料库v3（日历效应/事件驱动/回测/归因） | P2 | ✅ 新增 |
| `EXTERNAL_STRATEGY_RAW_MATERIAL_v4.0.md` | 外部交易策略原始资料库v4（实盘技术：订单路由/风控/监控/灾难恢复） | P2 | ✅ 新增 |
| `EXTERNAL_STRATEGY_RAW_MATERIAL_v5.0.md` | 外部交易策略原始资料库v5（国内外交易系统全景对比） | P2 | ✅ 新增 |
| `EXTERNAL_STRATEGY_RAW_MATERIAL_v6.0.md` | 外部交易策略原始资料库v6（A股制度/算法执行/组合优化/Barra因子/可视化） | P2 | ✅ 新增 |
| `STRATEGY_DESIGN_REFERENCE_v1.0.md` | 策略设计参考（ADX/动态阈值/交易量确认/组合风控/均值回归） | P2 | ✅ 新增 |
| `STRATEGY_DESIGN_REFERENCE_v1.0.md` | 策略设计参考（ADX/动态阈值/交易量确认/组合风控/均值回归） | P2 | ✅ 新增 |
| `STRATEGY_DESIGN_REFERENCE_v2.0.md` | 策略设计参考v2（缺口/竞价/尾盘/情绪/行业轮动/行为审查） | P2 | ✅ 新增 |
| `BACKTEST_AND_ATTRIBUTION_DESIGN_v1.0.md` | 回测稳健性与绩效归因设计参考（日历/事件/WF/Brinson） | P2 | ✅ 新增 |
| `PROGRAMMING_AI_ULTIMATE_TASK_PACKAGE_v1.0.md` | **编程 AI 终极任务包**：按 Phase 编排的编码指南（本文档的替代入口） | P0 | ✅ **必读入口** |
| `MASTER_PROGRAMMING_INSTRUCTION_v1.0.md` | 编程 AI 总指令书（21KB） | P0 | ✅ 冻结 |
| `GAS_12_INDICATOR_MAP_P0_A_v1.0.md` | 12 个 GAS 指标映射到对象卡 | P1 | ✅ 冻结 |
| `RISK_ARCHITECTURE_P0_R_v1.0.md` | Van Tharp + Kelly + VolTarget 三层联动 | P0 | ✅ 冻结 |
| `USER_IDEAS_INTEGRATION_v1.0.md` | 用户 4 份素材整合（投研管家/因子大赛/问题2/问题3） | P1 | ✅ 已整理 |
| `DY_INTEGRATION_v1.0.md` | 大隐体系整合（DY_R1/R2/R3 映射到现有对象卡） | P1 | ✅ 已整理 |
| `A5_FUNDAMENTAL_INTEGRATION_v1.0.md` | A5 财报估值与选股层整合 | P1 | ✅ 已整理 |
| `BACKTEST_REPORT_TEMPLATE_v1.0.md` | 三级回测报告模板 + 日报生成器 | P1 | ✅ 已整理 |
| `LIVE_TRADING_SYSTEM_DESIGN_v1.0.md` | **实盘交易系统设计**：订单状态机/风控前置/券商接口/监控/灾难恢复 | P0 | ✅ 可编码 |
| `TRADING_SYSTEM_COMPARISON_DESIGN_v1.0.md` | **交易系统对比设计参考**：国内外平台借鉴与不借鉴的决策 | P2 | ✅ 新增 |
| `SYSTEM_ENHANCEMENT_DESIGN_v1.0.md` | **系统增强设计参考**：A股制度/算法执行/组合优化/Barra因子/可视化 | P1 | ✅ 新增 |
| `TRADING_SYSTEM_COMPARISON_DESIGN_v1.0.md` | **交易系统对比设计参考**：国内外平台借鉴与不借鉴的决策 | P2 | ✅ 新增 |

---

### 2.4 🎨 治理架构（4 份 + 1 代码）

| 文件名 | 用途 | 状态 |
|--------|------|------|
| `GOVERNANCE_ARCHITECTURE_OPTIONS_v1.0.md` | 国外方案（美式/英式/瑞士/罗马） | ✅ 存档参考 |
| `GOVERNANCE_ARCHITECTURE_CHINA_v1.0.md` | 中国方案（三省六部/三会一层/内阁六科/台谏） | ✅ 存档参考 |
| `MING_CABINET_HYBRID_ARCHITECTURE_v1.0.md` | **最终方案**：明朝内阁混合架构，五态动态切换 | ✅ **主文档** |
| `EMPEROR_CONSOLE_UI_v1.0.md` | 御前会议控制台界面设计 | ✅ 主文档 |
| `governance_architecture.py` | Python 接口与类设计（49KB） | ✅ **可直接编码** |
| `prototype_console.py` | 终端控制台原型（30KB，ANSI颜色） | ✅ **可运行** |
| `dashboard_preview.html` | HTML 预览（五模式） | ✅ 演示用 |

---

### 2.5 🗺️ 映射表（2 份）

| 文件名 | 用途 | 状态 |
|--------|------|------|
| `全仓库功能映射大表_v1.0.md` | 早期版本 | ❌ 已废弃 |
| `全仓库功能映射大表_v2.0.md` | 当前版本：58 对象，6 层 | ✅ 当前有效 |
| `全仓库功能映射大表_v2.2.md` | 最新版本 | ✅ **主文档** |

---

### 2.6 📦 历史存档（GLM 交付物，仅供参考）

以下文件为 GLM 早期交付物，内容已整合到 Kimi 整理的文档中，**编程时以 Kimi 版为准**：

```
GLM_DELIVERY_04_CHANLUN_FULL_QUANT_v1.0.md
GLM_DELIVERY_05_TK_FOREX_OPTIMIZATION_v1.0.md
GLM_DELIVERY_06_TIER1_EXECUTION_FIELDS_v1.0.md
GLM_DELIVERY_07_TIER1_EXECUTION_FIELDS_v2.0.md
GLM_DELIVERY_09_A股跨市场适配审计与因子提取_v1.0.md
GLM_MATERIAL_PACKAGE_INDEX.md
GLM_SEARCH_01_执行层补充_跨市场_风控_另类数据_v1.0.md
GLM_SEARCH_TASK_INSTRUCTION.md
GLM_TASK_02_CHANLUN_OBJECT_CARD.md
GLM_TASK_04_CHANLUN_FULL_QUANT_FORMULA.md
GLM_TASK_05_TK_FOREX_OPTIMIZATION.md
GLM_TASK_06_BACKTEST_FRAMEWORK.md
GLM_TASK_07_A股特殊因子字段化提取.md
GLM_TASK_08_第二优先级执行层对象卡.md
GLM_TASK_09_A股跨市场适配审计.md
MTF_SEB_v0.1.md          ← 用户已明确拒绝此框架
TK外汇核心概念对象卡_Kimi版_v1.0.md
后续方向建议清单.md
执行层字段化优先级清单.md
```

---

## 三、交叉引用速查表

### 3.1 对象卡 → 策略组合映射

```text
哪些对象卡在哪个策略组合中被激活：

TrendFollowing (FULL)      → CHZL_BSD, BPB, VP, TKR7, MFLOW, VOLFAC
BreakoutPullback (FULL)    → BPB, YTC, VP, CHZL_BSD, MFLOW
ChannelBreakout (REDUCED)  → VP, YTC, VOLFAC
MACDDivergence (REDUCED)   → TKR7, KD MTF
MeanReversion (REDUCED)    → KD MTF, VP
TrendFollowing_Residual (EXIT_ONLY) → CHZL_BSD, VOLTARGET
TrialEntry (REDUCED)       → 任意 2-3 个 mature 对象卡
```

### 3.2 对象卡 → 数据需求映射

```text
日 OHLCV（全 A 股，2018-2024）→ 所有对象卡的基础输入
Wind 资金流向              → MFLOW（选股层）
60min/15min/5min OHLCV    → YTC（多周期 S/R）、CHZL（精细止损）
季频财报数据               → A5_FUNDAMENTAL_SELECTOR（选股层）
周线 OHLCV                → KD MTF（跨周期对齐）、CHZL_TREND（多周期）
```

### 3.3 文档 → 实现模块映射

```text
SYSTEM_ARCHITECTURE_DRAFT.md        → src/backtest_engine/pipeline/
STRATEGY_BUNDLES_v1.0.md            → src/backtest_engine/strategy/
VOTE_DECISION_TABLE_P0_E_v1.0.md    → src/backtest_engine/vote/
RISK_ARCHITECTURE_P0_R_v1.0.md      → src/backtest_engine/risk/
OBJECT_CARD_*.md                    → src/backtest_engine/objects/
BACKTEST_FRAMEWORK_DESIGN_v1.0.md   → src/backtest_engine/（整体）
LIVE_TRADING_SYSTEM_DESIGN_v1.0.md    → src/trading_engine/execution/ + broker/ + account/ + persistence/
MING_CABINET_HYBRID_ARCHITECTURE    → src/governance/（治理层）
EMPEROR_CONSOLE_UI_v1.0.md          → src/console/（控制台）
A5_FUNDAMENTAL_INTEGRATION          → src/data_pipeline/fundamental/
DY_INTEGRATION_v1.0.md              → src/backtest_engine/dy_scoring/
BACKTEST_REPORT_TEMPLATE            → src/backtest_engine/performance/
```

---

## 四、版本管理规范

```text
文档命名规范：
  {CATEGORY}_{NAME}_{VERSION}.{ext}
  
  CATEGORY 前缀：
    OBJECT_CARD_    → 对象卡定义
    SYSTEM_         → 系统架构
    STRATEGY_       → 策略组合
    VOTE_           → 投票机制
    RISK_           → 风控架构
    BACKTEST_       → 回测相关
    DATA_           → 数据相关
    USER_           → 用户想法整合
    DY_             → 大隐体系
    A5_             → A5 财报
    GOVERNANCE_     → 治理架构
    EMPEROR_        → 控制台

版本号规范：
  v{major}.{minor}
  major：架构级变更（需用户审批）
  minor：内容补充/修正（可自行更新）

状态标记：
  ✅ 冻结    = 核心逻辑已确定，编程必须遵循
  ✅ 可编码  = 内容完整，可开始实现
  ⚠️ 审查   = 内容需进一步验证
  🔶 待实现  = 已设计但等待数据/条件成熟
  ❌ 废弃    = 不再使用，仅存档
```

---

## 五、缺失文档清单（待补充）

以下方向尚未形成完整文档，是"其他方向"的工作内容：

```text
□ 性能优化指南（polars vs pandas/特征缓存/并行计算）
□ 用户操作手册（控制台命令速查/常见问题）
```

---

> 文件：INDEX_v2.0.md
> 版本：v2.4（2026-07-07 更新：新增系统增强设计 + 外部资料v6）
> 生产者：Kimi（文档索引与导航）
> 用途：编程 AI 的总入口，必须从此文档开始阅读
> 更新规则：每新增/更新一份文档，必须同步更新本索引
