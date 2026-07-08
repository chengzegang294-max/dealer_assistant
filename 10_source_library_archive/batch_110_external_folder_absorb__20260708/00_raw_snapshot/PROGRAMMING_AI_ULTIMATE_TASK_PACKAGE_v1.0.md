# 编程 AI 终极任务包 v1.0

> **这是给编码 AI 的"总任务书"。** 不要从 INDEX 开始读，从本文档开始读。本文档告诉你：先读什么、再读什么、先写什么、再写什么、怎样算完成。
> 
> 版本：v1.0 | 最后更新：2026-07-07 | 覆盖文档：33 份有效 + 2 份代码原型

---

## 一、项目总览（30 秒了解全貌）

### 1.1 项目名称与目标

- **名称**：投资管家（Investment Steward）
- **目标**：构建一个完整的 A 股量化交易系统，覆盖回测 → 模拟盘 → 实盘
- **核心特色**：
  1. 对象卡体系（Object Card）—— 可插拔的指标/策略原子
  2. 明朝内阁混合治理架构 —— 五态动态切换（常态/牛市/熊市/震荡/危机）
  3. 三层决策：PeriodQueen（环境识别）→ StrategyBundles（策略选择）→ Vote+Risk（执行管理）
  4. 纯多头 A 股策略（T+1, 涨跌停, 小盘股分层）

### 1.2 技术栈（不可更改）

| 层级 | 技术选择 | 理由 |
|------|----------|------|
| 语言 | Python 3.10+ | 用户指定 |
| 数据处理 | **polars 优先** / pandas 兼容 | 性能优先 |
| 数据存储 | Parquet（特征缓存）+ JSONL（日志） | 高效、可压缩 |
| 回测引擎 | **自研**（非 vnpy/Backtrader） | 对象卡驱动，自定义 pipeline |
| 数据源 | tushare / akshare / Wind（本地缓存） | 用户已有数据 |
| 测试 | pytest + hypothesis | 单元 + 模糊测试 |
| 部署 | Windows 单机 | 用户环境 |

### 1.3 工作目录

```
D:\Stock\trading_assistant\          # 主代码仓库（代码放这里）
E:\downloads\Desktop\找系统\特征\      # 文档资产库（设计文档在这里）
```

---

## 二、总架构图（一张图理解全系统）

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              投资管家 — 全系统架构                                    │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│   ┌─────────────────────────────────────────────────────────────────────────┐       │
│   │                         数据源层                                       │       │
│   │  日 OHLCV  │  分钟级  │  周线  │  Wind资金流向  │  季频财报  │  情绪指标  │       │
│   └─────────────────────────────────────────────────────────────────────────┘       │
│                                    │                                                │
│                                    ▼                                                │
│   ┌─────────────────────────────────────────────────────────────────────────┐       │
│   │                         数据管道 (Data Pipeline)                       │       │
│   │   ETL → 清洗 → 复权 → 对齐 → 特征缓存 (Parquet) → DataCatalog           │       │
│   └─────────────────────────────────────────────────────────────────────────┘       │
│                                    │                                                │
│                                    ▼                                                │
│   ┌─────────────────────────────────────────────────────────────────────────┐       │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │       │
│   │  │ 缠论分型  │  │ 缠论笔    │  │ 缠论中枢  │  │ 缠论趋势  │  │ 买卖信号  │  │       │
│   │  │ CHZL_FX  │  │ CHZL_BI  │  │ CHZL_ZS  │  │ CHZL_TREND│  │ CHZL_BSD │  │       │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │       │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │       │
│   │  │ 成交量分布│  │ AO背离   │  │ BPB      │  │ YTC      │  │ TK R6/R7 │  │       │
│   │  │ VP       │  │ TKR7     │  │ 突破回调  │  │ 微观结构  │  │ 外汇模式  │  │       │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │       │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │       │
│   │  │ 资金流向  │  │ 波动率因子│  │ 活跃比率  │  │ 机构行为  │  │ 周期女王  │  │       │
│   │  │ MFLOW    │  │ VOLFAC   │  │ ATRATIO  │  │ INSTB    │  │ PERIOD_Q │  │       │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │       │
│   │  ┌──────────┐  ┌──────────┐                                           │       │
│   │  │ 凯利公式  │  │ 波动率目标│                                           │       │
│   │  │ KELLY    │  │ VOLTARGET│                                           │       │
│   │  └──────────┘  └──────────┘                                           │       │
│   │                         对象卡引擎 (Object Cards)                     │       │
│   └─────────────────────────────────────────────────────────────────────────┘       │
│                                    │                                                │
│                                    ▼                                                │
│   ┌─────────────────────────────────────────────────────────────────────────┐       │
│   │                         投票机制 (Vote Engine)                           │       │
│   │   对象卡输出 → 互锁检查 → 过滤器 → 成熟度加权 → 合并信号 → 执行建议       │       │
│   └─────────────────────────────────────────────────────────────────────────┘       │
│                                    │                                                │
│                                    ▼                                                │
│   ┌─────────────────────────────────────────────────────────────────────────┐       │
│   │                         风控层 (Risk Engine)                             │       │
│   │   Van Tharp 仓位管理 → Kelly 公式 → 波动率目标 → 风控门控 → 前置风控     │       │
│   └─────────────────────────────────────────────────────────────────────────┘       │
│                                    │                                                │
│                                    ▼                                                │
│   ┌─────────────────────────────────────────────────────────────────────────┐       │
│   │                         执行层 (Execution Engine)                        │       │
│   │   ┌──────────┐    ┌──────────┐    ┌──────────┐                        │       │
│   │   │ 回测模式  │    │ 模拟模式  │    │ 实盘模式  │                        │       │
│   │   │ BACKTEST │ →  │ PAPER    │ →  │ LIVE     │                        │       │
│   │   │ 历史回放  │    │ 实时模拟  │    │ 真实交易  │                        │       │
│   │   └──────────┘    └──────────┘    └──────────┘                        │       │
│   │   SignalBuffer → RiskGate → OrderConverter → PreTradeRisk →          │       │
│   │   OrderRouter → OrderLifecycle → AccountManager → Monitoring         │       │
│   └─────────────────────────────────────────────────────────────────────────┘       │
│                                    │                                                │
│                                    ▼                                                │
│   ┌─────────────────────────────────────────────────────────────────────────┐       │
│   │                         治理层 (Governance)                            │       │
│   │   皇帝控制台 → 内阁票拟 → 六科给事中 → 台谏系统 → 模式切换               │       │
│   │   (EmperorConsole → Cabinet → SixDepartments → TaiJian → RegimeSwitch) │       │
│   └─────────────────────────────────────────────────────────────────────────┘       │
│                                    │                                                │
│                                    ▼                                                │
│   ┌─────────────────────────────────────────────────────────────────────────┐       │
│   │                         持久化与监控                                      │       │
│   │   交易日志 (WAL) → 持仓快照 → 灾难恢复 → 五层监控 → 告警通知              │       │
│   └─────────────────────────────────────────────────────────────────────────┘       │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 三、分阶段实现计划（Phase 1 → 4）

> **核心原则**：每个 Phase 完成后必须能通过 pytest 测试。没有测试 = 没有完成。

---

## Phase 1：基础设施（预计 2-3 周）

**目标**：让系统能跑起来，一个最简单的对象卡（VOLFAC）能从数据输入到回测输出。

### 3.1 Phase 1 必读文档（按顺序）

| 顺序 | 文档 | 为什么必读 | 预计阅读时间 |
|------|------|-----------|-------------|
| 1 | `README_FOR_PROGRAMMING_AI.md` | 入场手册，环境配置，目录约定 | 5 min |
| 2 | `MASTER_PROGRAMMING_INSTRUCTION_v1.0.md` | 编程规范，对象卡字段冻结，命名规则 | 15 min |
| 3 | `SYSTEM_ARCHITECTURE_DRAFT.md` | 理解三层决策架构 | 10 min |
| 4 | `DATA_AVAILABILITY_AUDIT_v1.0.md` | 数据审计，知道有什么数据、缺什么数据 | 10 min |
| 5 | `OBJECT_CARD_PERIOD_QUEEN_P0_F__CycleStateSystem_v1.0.md` | 核心过滤器，先读它理解"环境识别" | 15 min |
| 6 | `OBJECT_CARD_VOLFAC_P0_A__VolatilityFactor_v1.0.md` | 最简单的对象卡，第一批实现 | 10 min |
| 7 | `OBJECT_CARD_TKR7_P0_E__AO_Divergence_v1.0.md` | 纯 OHLCV，标准指标，第一批实现 | 10 min |
| 8 | `OBJECT_CARD_VP_P0_E__VolumeProfile_v1.0.md` | 纯 OHLCV，但需滚动窗口，第一批实现 | 15 min |
| 9 | `OBJECT_CARD_BPB_P0_E__Brooks_Breakout_Pullback_v1.0.md` | 纯 OHLCV，价格行为，第一批实现 | 15 min |
| 10 | `BACKTEST_FRAMEWORK_DESIGN_v1.0.md` | 回测引擎 Pipeline 设计 | 20 min |

### 3.2 Phase 1 实现模块（按顺序）

```
Week 1-2: 数据管道 + 基础框架
├── src/
│   ├── __init__.py
│   ├── config.py              # 配置管理（路径、参数、阈值）
│   ├── data_pipeline/
│   │   ├── __init__.py
│   │   ├── loader.py          # DataLoader: 从 Parquet/CSV 加载 OHLCV
│   │   ├── preprocessor.py    # 数据清洗：复权、停牌处理、异常值检测
│   │   ├── catalog.py         # DataCatalog: 数据资产目录
│   │   └── cache.py           # FeatureCache: Parquet 缓存管理
│   ├── backtest_engine/
│   │   ├── __init__.py
│   │   ├── engine.py          # BacktestEngine 主类
│   │   ├── pipeline.py        # Pipeline 执行器（逐日/逐分钟迭代）
│   │   └── types.py           # 共享类型定义（Signal, Order, Position, Bar）
│   └── objects/
│       ├── __init__.py
│       ├── base.py            # ObjectCardBase: 抽象基类，所有对象卡继承它
│       ├── volfac.py          # VOLFAC 对象卡
│       ├── tkr7.py            # TKR7 对象卡
│       ├── vp.py              # VP 对象卡
│       └── bpb.py             # BPB 对象卡
│
Week 2-3: 投票 + 风控 + 回测执行
├── src/backtest_engine/
│   ├── vote/
│   │   ├── __init__.py
│   │   ├── engine.py          # VoteDecisionEngine
│   │   └── rules.py           # 互锁检查、过滤器规则
│   ├── risk/
│   │   ├── __init__.py
│   │   ├── van_tharp.py       # Van Tharp 仓位管理
│   │   ├── kelly.py           # KellyCriterion（简化版，先固定参数）
│   │   ├── vol_target.py      # VolatilityTargeting
│   │   └── gate.py            # RiskGate 轻量风控检查
│   └── execution/
│       ├── __init__.py
│       ├── mock_broker.py     # MockBroker（回测用）
│       ├── executor.py        # BacktestExecutor
│       └── account.py         # 回测账户跟踪（简化版）
│
Week 3: 测试 + 报告
├── tests/
│   ├── test_data_pipeline.py
│   ├── test_volfac.py
│   ├── test_tkr7.py
│   ├── test_vp.py
│   ├── test_bpb.py
│   ├── test_vote_engine.py
│   └── test_backtest_engine.py
├── src/backtest_engine/performance/
│   ├── __init__.py
│   ├── metrics.py             # 夏普比率、最大回撤、胜率等
│   └── report.py              # 回测报告生成
```

### 3.3 Phase 1 验收标准（必须全部通过）

```python
# 验收测试 1: VOLFAC 对象卡能正确计算波动率
from src.objects.volfac import VolatilityFactor

obj = VolatilityFactor(lookback=20)
result = obj.calculate(df)  # df: polars DataFrame with OHLCV
assert "volatility_20d" in result.columns
assert result["volatility_20d"].null_count() < len(result) * 0.1  # 缺失率 < 10%

# 验收测试 2: 回测引擎能完整跑完一个周期
def test_backtest_end_to_end():
    engine = BacktestEngine(mode=TradingMode.BACKTEST)
    engine.load_data(symbols=["000001.SZ"], start="2020-01-01", end="2020-12-31")
    engine.register_objects([VOLFAC(), TKR7()])
    engine.run()
    assert engine.trades  # 至少有一条交易记录
    assert engine.equity_curve  # 有权益曲线
    assert engine.metrics.sharpe_ratio is not None  # 有绩效指标

# 验收测试 3: 风控门控能阻止违规订单
risk_gate = RiskGate(max_single_position_pct=0.2)
order = Order(symbol="000001.SZ", target_value=1_000_000)  # 假设总资金 100万
result = risk_gate.check(order, account=Account(total_value=1_000_000))
assert not result.passed  # 因为单笔 > 20%
```

---

## Phase 2：策略核心 + 选股层（预计 2-3 周）

**目标**：实现完整的对象卡体系（12 张 + PeriodQueen），加入选股层和基本面过滤。

### 3.4 Phase 2 必读文档

| 顺序 | 文档 | 重点 |
|------|------|------|
| 1 | `OBJECT_CARD_CHZL_FX_P0_S__Chanlun_Fenxing_v1.0.md` | 缠论分型（结构层基础） |
| 2 | `OBJECT_CARD_CHZL_BI_P0_S__Chanlun_Bi_v1.0.md` | 缠论笔（依赖分型） |
| 3 | `OBJECT_CARD_CHZL_ZS_P0_S__Chanlun_Zhongshu_v1.0.md` | 缠论中枢（依赖笔） |
| 4 | `OBJECT_CARD_CHZL_TREND_P0_S__Chanlun_Trend_v1.0.md` | 缠论趋势（依赖中枢） |
| 5 | `OBJECT_CARD_CHZL_BSD_P0_E__Chanlun_Buy_Sell_Signals_v1.0.md` | 缠论买卖信号（核心执行卡） |
| 6 | `OBJECT_CARD_YTC_P0_E__YTC_Microstructure_v1.0.md` | YTC 微观结构（多周期 S/R） |
| 7 | `OBJECT_CARD_MFLOW_P0_A__MoneyFlow_v1.0.md` | 资金流向（选股层） |
| 8 | `OBJECT_CARD_KELLY_P0_R__KellyCriterion_v1.0.md` | Kelly 公式（风控层） |
| 9 | `OBJECT_CARD_VOLTARGET_P0_R__VolatilityTargeting_v1.0.md` | 波动率目标（风控层） |
| 10 | `STRATEGY_BUNDLES_v1.0.md` | 7 个策略组合定义 |
| 11 | `VOTE_DECISION_TABLE_P0_E_v1.0.md` | 投票判定规则 |
| 12 | `RISK_ARCHITECTURE_P0_R_v1.0.md` | 风控架构联动规则 |
| 13 | `A5_FUNDAMENTAL_INTEGRATION_v1.0.md` | 财报选股层（第一层过滤器） |
| 14 | `DY_INTEGRATION_v1.0.md` | DY 评分层（元评分） |
| 15 | `GAS_12_INDICATOR_MAP_P0_A_v1.0.md` | 12 个 GAS 指标映射 |

### 3.5 Phase 2 实现模块

```
Week 4-5: 缠论对象卡 + 策略组合
├── src/objects/
│   ├── chzl_fx.py             # 缠论分型
│   ├── chzl_bi.py             # 缠论笔（依赖 FX）
│   ├── chzl_zs.py             # 缠论中枢（依赖 BI）
│   ├── chzl_trend.py          # 缠论趋势（依赖 ZS）
│   ├── chzl_bsd.py            # 缠论买卖信号（核心执行卡）
│   ├── ytc.py                 # YTC 微观结构
│   ├── mflow.py               # 资金流向（选股层）
│   ├── kelly.py               # Kelly 公式（风控层）
│   └── voltarget.py           # 波动率目标（风控层）
│
├── src/backtest_engine/strategy/
│   ├── __init__.py
│   ├── bundles.py             # 7 个策略组合（TrendFollowing, BreakoutPullback...）
│   └── selector.py            # 策略选择器（根据 PeriodQueen 状态）
│
Week 5-6: 选股层 + 基本面过滤
├── src/data_pipeline/fundamental/
│   ├── __init__.py
│   ├── a5_selector.py         # A5 财报选股（第一层过滤器）
│   ├── dy_scoring.py         # DY 评分层（元评分）
│   └── filters.py            # 排雷 + 评分 + 估值过滤器
│
├── src/backtest_engine/vote/
│   ├── __init__.py
│   ├── engine.py             # VoteDecisionEngine（完整版）
│   ├── maturity.py           # 成熟度评估与升级
│   └── abort_codes.py        # ABORT 原因编码（14 种）
```

### 3.6 Phase 2 验收标准

```python
# 验收测试 1: 缠论笔能正确识别
from src.objects.chzl_bi import ChanlunBi

bi = ChanlunBi()
result = bi.calculate(df)
assert "bi_start" in result.columns
assert "bi_end" in result.columns
assert "bi_direction" in result.columns
assert result.filter(pl.col("bi_direction").is_not_null()).height > 0

# 验收测试 2: 策略组合映射正确
from src.backtest_engine.strategy.bundles import StrategyBundles

bundles = StrategyBundles()
period_state = PeriodState.ATTACK_SUSTAINED
active = bundles.get_active_objects(period_state)
assert "CHZL_BSD" in active
assert "BPB" in active
assert "VOLTARGET" in active

# 验收测试 3: A5 选股过滤能正确排雷
from src.data_pipeline.fundamental.a5_selector import A5FundamentalSelector

selector = A5FundamentalSelector()
pool = selector.filter(symbols, date="2024-06-30")
assert all(s not in pool for s in suspended_symbols)  # 停牌被过滤
assert all(s not in pool for s in st_symbols)  # ST 被过滤
```

---

## Phase 3：执行层与实盘接口（预计 2-3 周）

**目标**：实现完整的订单生命周期管理、风控前置、监控告警，让系统能从模拟盘过渡到实盘。

### 3.7 Phase 3 必读文档

| 顺序 | 文档 | 重点 |
|------|------|------|
| 1 | `LIVE_TRADING_SYSTEM_DESIGN_v1.0.md` | **核心文档**：订单状态机、风控前置、券商接口、监控、灾难恢复 |
| 2 | `EXTERNAL_STRATEGY_RAW_MATERIAL_v4.0.md` | 实盘技术参考资料（Ptrade API、滑点、延迟） |
| 3 | `BACKTEST_AND_ATTRIBUTION_DESIGN_v1.0.md` | 回测诚实性参数、Brinson 归因 |
| 4 | `BACKTEST_REPORT_TEMPLATE_v1.0.md` | 三级报告模板、日报生成器 |

### 3.8 Phase 3 实现模块

```
Week 7-8: 执行层核心
├── src/trading_engine/
│   ├── __init__.py
│   ├── engine.py              # TradingEngine（总控，切换 BACKTEST/PAPER/LIVE）
│   ├── modes.py               # TradingMode 枚举
│   ├── execution/
│   │   ├── __init__.py
│   │   ├── signal_buffer.py   # 信号缓冲区（去重、延迟、排序）
│   │   ├── risk_gate.py       # 风控门控（轻量检查）
│   │   ├── converter.py       # 信号→订单转换器
│   │   ├── pre_trade_risk.py  # 风控前置（深度检查、独立执行）
│   │   ├── router.py          # 订单路由
│   │   ├── lifecycle.py       # 订单生命周期管理（状态机）
│   │   ├── backtest_exec.py   # 回测执行器（继承现有）
│   │   └── live_exec.py       # 实盘执行器
│   ├── broker/
│   │   ├── __init__.py
│   │   ├── interface.py       # BrokerInterface 抽象基类
│   │   ├── mock.py            # MockBroker（回测）/ PaperBroker（模拟盘）
│   │   ├── ptrade.py          # PtradeBroker（恒生接口）
│   │   └── qmt.py             # QMTBroker（迅投接口）
│   ├── account/
│   │   ├── __init__.py
│   │   ├── manager.py         # AccountManager（实时资金/持仓/P&L）
│   │   ├── monitoring.py      # MonitoringSystem（五层监控）
│   │   └── alerts.py          # 告警通知（日志/弹窗/邮件）
│   └── persistence/
│       ├── __init__.py
│       ├── wal.py             # 写前日志（TradeLog）
│       ├── snapshot.py        # 持仓快照
│       └── recovery.py        # 灾难恢复（从 WAL + 快照重建）
│
Week 8-9: 回测诚实性 + 归因 + 报告
├── src/backtest_engine/performance/
│   ├── attribution.py         # Brinson 归因 + 多因子归因
│   ├── calendar.py            # 日历效应分析
│   └── event.py               # 事件驱动分析
├── src/backtest_engine/report/
│   ├── __init__.py
│   ├── templates/
│   │   ├── level1.py          # Level 1：基础报告（一键生成）
│   │   ├── level2.py          # Level 2：策略体检
│   │   └── level3.py          # Level 3：深度归因
│   └── daily.py               # 日报生成器
```

### 3.9 Phase 3 验收标准

```python
# 验收测试 1: 订单状态机正确转换
from src.trading_engine.execution.lifecycle import OrderLifecycleManager, OrderState

mgr = OrderLifecycleManager(broker=MockBroker())
oid = mgr.create_order(order=Order(symbol="000001.SZ", target_value=100000))
assert mgr.get_state(oid) == OrderState.PENDING

mgr.submit(oid)
assert mgr.get_state(oid) == OrderState.SUBMITTED

mgr.on_fill(oid, FillRecord(quantity=1000, price=10.0))
assert mgr.get_state(oid) == OrderState.FILLED

# 验收测试 2: 回撤熔断能触发
from src.trading_engine.execution.pre_trade_risk import PreTradeRisk

risk = PreTradeRisk(account=AccountManager(), config=RiskConfig(max_daily_drawdown=0.05))
# 模拟日回撤 6%
account.daily_pnl = -60_000
account.daily_high_pnl = 1_000_000
result = risk.validate(Order(symbol="000001.SZ", target_value=100000))
assert not result.allowed  # 因为回撤 > 5%
assert "DRAWDOWN_CIRCUIT" in result.reason

# 验收测试 3: 回测诚实性参数生效
def test_backtest_honesty():
    engine = BacktestEngine(
        mode=TradingMode.BACKTEST,
        honesty_params=BacktestHonestyParams(slippage_pct=0.002)
    )
    engine.load_data(symbols=["000001.SZ"], start="2020-01-01", end="2020-01-31")
    engine.register_objects([VOLFAC()])
    engine.run()
    # 检查是否有滑点影响
    for trade in engine.trades:
        assert trade.fill_price != trade.signal_price  # 滑点导致价格不同

# 验收测试 4: 灾难恢复能重建状态
from src.trading_engine.persistence.recovery import RecoveryManager

recovery = RecoveryManager(log_dir=Path("logs/trades"))
state = recovery.recover()
assert state.cash >= 0
assert isinstance(state.positions, dict)
```

---

## Phase 4：治理架构 + 控制台 + 扩展（预计 1-2 周）

**目标**：实现明朝内阁混合治理架构，让控制台能运行。用户通过控制台与系统交互。

### 3.10 Phase 4 必读文档

| 顺序 | 文档 | 重点 |
|------|------|------|
| 1 | `MING_CABINET_HYBRID_ARCHITECTURE_v1.0.md` | 最终治理方案：五态动态切换 |
| 2 | `EMPEROR_CONSOLE_UI_v1.0.md` | 控制台界面设计 |
| 3 | `governance_architecture.py` | 已有 Python 接口设计（49KB，可直接编码） |
| 4 | `prototype_console.py` | 已有终端控制台原型（30KB，可运行） |
| 5 | `USER_IDEAS_INTEGRATION_v1.0.md` | 用户素材（投研管家、因子大赛等） |
| 6 | `STRATEGY_DESIGN_REFERENCE_v1.0.md` | 策略设计参考（增强方向） |
| 7 | `STRATEGY_DESIGN_REFERENCE_v2.0.md` | 策略设计参考 v2 |

### 3.11 Phase 4 实现模块

```
Week 9-10: 治理架构 + 控制台
├── src/governance/
│   ├── __init__.py
│   ├── enums.py               # RegimeMode, PeriodQueenState, Verdict
│   ├── documents.py           # MemorialDocument, ReviewDocument, ImperialEdict
│   ├── audit.py               # AuditLogger（起居注）
│   ├── strategies.py          # 5 种 RegimeModeStrategy
│   ├── controller.py          # RegimeModeController（模式切换）
│   ├── cabinet.py             # Cabinet（内阁票拟）
│   ├── departments.py         # SixDepartments（六科给事中）
│   ├── taijian.py             # TaiJianSystem（台谏系统）
│   ├── emperor.py             # EmperorConsole（用户接口）
│   └── engine.py              # GovernanceEngine（总控）
│
├── src/console/
│   ├── __init__.py
│   ├── main.py                # 控制台入口
│   ├── ui.py                  # UI 渲染（ANSI 颜色 / 可选 rich）
│   ├── commands.py            # 命令解析（m/v/r/L 等）
│   └── panels.py              # 面板渲染（首辅/次辅/六科/台谏）
│
Week 10: 扩展与优化（可选，按用户优先级）
├── src/backtest_engine/objects/
│   ├── atratio.py             # ATRATIO（LIMITED，仅大盘流动性充足时）
│   ├── instb.py               # INSTB（needs_extra_data，v1.1）
│   └── tk_r6.py               # TK R6（外汇模式，A股适配需审查）
│   ├── tk_r7.py               # TK R7
│   └── tk_r8.py               # TK R8
│
├── src/backtest_engine/performance/
│   ├── walk_forward.py        # Walk-Forward 分析
│   ├── monte_carlo.py         # 蒙特卡洛模拟
│   └── decay_analysis.py      # 策略衰减分析
```

### 3.12 Phase 4 验收标准

```python
# 验收测试 1: 治理模式切换
from src.governance.engine import GovernanceEngine
from src.governance.enums import RegimeMode

engine = GovernanceEngine()
assert engine.controller.current_mode == RegimeMode.NORMAL

engine.controller.switch_mode(RegimeMode.BULL, reason="ADX > 40, 均线多头排列")
assert engine.controller.current_mode == RegimeMode.BULL
assert engine.audit.logs[-1].action == "MODE_SWITCH"

# 验收测试 2: 控制台能渲染
from src.console.main import ConsoleApp

app = ConsoleApp(mode=RegimeMode.BEAR)
output = app.render()
assert "首辅" in output
assert "次辅" in output
assert "六科" in output
assert "台谏" in output

# 验收测试 3: 内阁票拟能生成
from src.governance.cabinet import Cabinet
from src.governance.documents import MemorialDocument

cabinet = Cabinet(audit=AuditLogger())
memorial = MemorialDocument(
    subject="策略切换申请",
    content="ADX > 40，申请从 MeanReversion 切换到 TrendFollowing",
    recommended_action=Verdict.APPROVE
)
verdict = cabinet.deliberate(memorial)
assert verdict in (Verdict.APPROVE, Verdict.REJECT, Verdict.AMEND)
```

---

## 四、关键约束（违反 = 不可接受）

### 4.1 数据约束

```python
# 必须严格遵守
- 日 OHLCV 是全部对象卡的基础输入（2018-2024）
- 使用 polars 优先，pandas 仅用于兼容（明确标记 @pandas_compat）
- 所有特征缓存用 Parquet 格式
- 历史数据不可修改（immutable），只读引用
- 复权处理：前复权用于回测，后复权用于分析，必须明确标记
```

### 4.2 交易约束

```python
# 必须严格遵守
- A 股纯多头（short 不可用）
- T+1：当日买入不可卖出
- 涨跌停：涨停不卖、跌停不买
- 停牌/退市：自动过滤，不可交易
- 股票委托取整 100 股，可转债取整 10 张
- 最小佣金 5 元，印花税千 1（卖时），过户费十万分之 2
- 单标的最大持仓 ≤ 20% 总资金
- 单一行业 ≤ 30% 总资金
```

### 4.3 编码约束

```python
# 必须严格遵守
- 所有对象卡字段已冻结，只实现不修改
- 对象卡必须继承 ObjectCardBase，实现 calculate() 方法
- 输出必须包含统一接口字段：object_id, signal_type, signal_strength, confidence...
- 回测和实盘共享信号层、投票层、风控层，仅在执行层区分
- 每个模块必须有 pytest 测试，覆盖率 ≥ 80%
- 禁止使用 print 输出，全部使用 logging
- 路径用 Path 对象，禁止硬编码字符串
```

### 4.4 对象卡不可量化内容

```python
# 这些内容是 shell_only，不要强行公式化
- 哲学、心法、审美、直觉 → NOT_QUANT_YET 或 shell_only
- 只有常规 A 股数据可直接落地的保留 proxy_quantizable_now
- 依赖 Level-2 / 龙虎榜 / NLP / 另类数据的 → 降级为 needs_extra_data
```

---

## 五、文档清单（33 份有效文档）

### 5.1 纲领层（3 份）

| 文件名 | 状态 | 用途 |
|--------|------|------|
| `SYSTEM_ARCHITECTURE_DRAFT.md` | ✅ 冻结 | 三层决策架构 |
| `STRATEGY_BUNDLES_v1.0.md` | ✅ 冻结 | 7 个策略组合 |
| `VOTE_DECISION_TABLE_P0_E_v1.0.md` | ✅ 冻结 | 投票判定规则 |

### 5.2 对象卡（15 张）

| 文件名 | 功能层 | 状态 | 优先级 |
|--------|--------|------|--------|
| `OBJECT_CARD_CHZL_FX_P0_S__Chanlun_Fenxing_v1.0.md` | 结构 | ✅ 可编码 | Phase 2 |
| `OBJECT_CARD_CHZL_BI_P0_S__Chanlun_Bi_v1.0.md` | 结构 | ✅ 可编码 | Phase 2 |
| `OBJECT_CARD_CHZL_ZS_P0_S__Chanlun_Zhongshu_v1.0.md` | 结构 | ✅ 可编码 | Phase 2 |
| `OBJECT_CARD_CHZL_TREND_P0_S__Chanlun_Trend_v1.0.md` | 结构 | ✅ 可编码 | Phase 2 |
| `OBJECT_CARD_CHZL_BSD_P0_E__Chanlun_Buy_Sell_Signals_v1.0.md` | 执行 | ✅ 可编码 | Phase 2 |
| `OBJECT_CARD_VP_P0_E__VolumeProfile_v1.0.md` | 执行 | ✅ 可编码 | Phase 1 |
| `OBJECT_CARD_TKR7_P0_E__AO_Divergence_v1.0.md` | 执行 | ✅ 可编码 | Phase 1 |
| `OBJECT_CARD_BPB_P0_E__Brooks_Breakout_Pullback_v1.0.md` | 执行 | ✅ 可编码 | Phase 1 |
| `OBJECT_CARD_YTC_P0_E__YTC_Microstructure_v1.0.md` | 执行 | ✅ 可编码 | Phase 2 |
| `OBJECT_CARD_TK_R6_P0_E__TK_Forex_Pattern_v1.0.md` | 执行 | ⚠️ 审查 | Phase 4 |
| `OBJECT_CARD_TK_R7_P0_E__TK_Forex_Pattern_v1.0.md` | 执行 | ⚠️ 审查 | Phase 4 |
| `OBJECT_CARD_TK_R8_P0_E__TK_Forex_Pattern_v1.0.md` | 执行 | ⚠️ 审查 | Phase 4 |
| `OBJECT_CARD_KELLY_P0_R__KellyCriterion_v1.0.md` | 风控 | ✅ 可编码 | Phase 2 |
| `OBJECT_CARD_VOLTARGET_P0_R__VolatilityTargeting_v1.0.md` | 风控 | ✅ 可编码 | Phase 2 |
| `OBJECT_CARD_MFLOW_P0_A__MoneyFlow_v1.0.md` | 选股 | ✅ 可编码 | Phase 2 |
| `OBJECT_CARD_VOLFAC_P0_A__VolatilityFactor_v1.0.md` | 选股 | ✅ 可编码 | Phase 1 |
| `OBJECT_CARD_ATRATIO_P0_A__ActiveTradeRatio_v1.0.md` | 选股 | ⚠️ LIMITED | Phase 4 |
| `OBJECT_CARD_INSTB_P0_A__InstitutionalBehavior_v1.0.md` | 选股 | 🔶 待实现 | Phase 4 |
| `OBJECT_CARD_PERIOD_QUEEN_P0_F__CycleStateSystem_v1.0.md` | 过滤 | ✅ 可编码 | Phase 2 |

### 5.3 架构与参考（13 份）

| 文件名 | 优先级 | 状态 | 对应 Phase |
|--------|--------|------|----------|
| `BACKTEST_FRAMEWORK_DESIGN_v1.0.md` | P0 | ✅ 冻结 | Phase 1 |
| `OBJECT_CARD_BACKTEST_SCHEDULE_v1.0.md` | P1 | ✅ 冻结 | Phase 1-2 |
| `DATA_AVAILABILITY_AUDIT_v1.0.md` | P0 | ✅ 冻结 | Phase 1 |
| `MASTER_PROGRAMMING_INSTRUCTION_v1.0.md` | P0 | ✅ 冻结 | **全部** |
| `GAS_12_INDICATOR_MAP_P0_A_v1.0.md` | P1 | ✅ 冻结 | Phase 2 |
| `RISK_ARCHITECTURE_P0_R_v1.0.md` | P0 | ✅ 冻结 | Phase 2-3 |
| `USER_IDEAS_INTEGRATION_v1.0.md` | P1 | ✅ 已整理 | Phase 2-4 |
| `DY_INTEGRATION_v1.0.md` | P1 | ✅ 已整理 | Phase 2 |
| `A5_FUNDAMENTAL_INTEGRATION_v1.0.md` | P1 | ✅ 已整理 | Phase 2 |
| `BACKTEST_REPORT_TEMPLATE_v1.0.md` | P1 | ✅ 已整理 | Phase 3 |
| `LIVE_TRADING_SYSTEM_DESIGN_v1.0.md` | P0 | ✅ 可编码 | Phase 3 |
| `BACKTEST_AND_ATTRIBUTION_DESIGN_v1.0.md` | P2 | ✅ 新增 | Phase 3 |
| `EXTERNAL_STRATEGY_RAW_MATERIAL_v4.0.md` | P2 | ✅ 新增 | Phase 3 |

### 5.4 治理架构（4 份 + 1 代码）

| 文件名 | 状态 | 对应 Phase |
|--------|------|----------|
| `MING_CABINET_HYBRID_ARCHITECTURE_v1.0.md` | ✅ 主文档 | Phase 4 |
| `EMPEROR_CONSOLE_UI_v1.0.md` | ✅ 主文档 | Phase 4 |
| `governance_architecture.py` | ✅ 可编码 | Phase 4 |
| `prototype_console.py` | ✅ 可运行 | Phase 4 |

### 5.5 映射表（2 份）

| 文件名 | 状态 | 用途 |
|--------|------|------|
| `全仓库功能映射大表_v2.2.md` | ✅ 主文档 | 58 对象，6 层映射 |

---

## 六、编码 AI 工作流程

```
Step 1: 通读本任务包（你现在在读的这份文档）
    ↓
Step 2: 按当前 Phase 的"必读文档"顺序阅读
    ↓
Step 3: 按当前 Phase 的"实现模块"顺序编码
    ↓
Step 4: 每个模块完成后写 pytest 测试
    ↓
Step 5: 运行测试，修复失败项
    ↓
Step 6: 对照"验收标准"，确认全部通过
    ↓
Step 7: 通知用户本 Phase 完成，等待进入下一阶段
    ↓
Step 8: 用户确认后，进入下一 Phase
```

---

## 七、常见问题速查

**Q: 某个对象卡字段不理解怎么办？**
> 不要猜测，回头读该对象卡的文档。字段已冻结，不可修改。

**Q: 回测和实盘代码要重复写吗？**
> 不要。信号层、投票层、风控层共享代码。执行层通过 `TradingMode` 切换 BrokerInterface 实现。

**Q: 测试数据从哪来？**
> 用 `tushare` 或 `akshare` 下载少量真实数据（如 000001.SZ 2020-2021 年日数据），存为 fixtures。

**Q: 治理架构是强制必须实现的吗？**
> Phase 1-3 不强制。但建议 Phase 1 就实现 `RegimeMode` 枚举和 `PeriodQueen` 状态机，因为它们是策略选择的核心输入。

**Q: 实盘代码需要真实账户吗？**
> Phase 1-2 不需要。Phase 3 的 `PtradeBroker` / `QMTBroker` 需要真实账户，但先用 `MockBroker` 和 `PaperBroker` 跑通。

**Q: 遇到文档和代码冲突听谁的？**
> 文档优先。文档已冻结意味着核心逻辑不可更改。如有冲突，记录问题并询问用户。

---

> 文件：PROGRAMMING_AI_ULTIMATE_TASK_PACKAGE_v1.0.md
> 生产者：Kimi（基于 33 份文档 + 2 份代码原型的综合编排）
> 用途：编程 AI 的"总任务书"，从本文档开始阅读，不再需要从 INDEX 逐份查找
> 状态：✅ 完成 | 版本：v1.0
> 更新规则：当新增 Phase 或文档变更时，同步更新本文档的文档清单和对应 Phase
