# 编程 AI 总任务指令书 v1.0

> 版本：v1.0 | 状态：已确认数据就绪，可全面启动编码  
> 目标：将 12 张已冻结对象卡转化为可运行的回测框架  
> 原则：只读结构，不预测；保守升级；互锁优先；T+1 约束

---

## 1. 任务总览

### 1.1 你要做什么

实现一个**对象卡驱动的回测框架**，核心能力：
1. 加载 A 股历史数据（日 OHLCV + 分钟级 + 资金流向）
2. 按 Pipeline 顺序计算 12 张对象卡的输出字段
3. 执行互锁检查、过滤器、风控调制、投票融合
4. 生成交易信号并模拟执行
5. 输出绩效报告和成熟度升级证据

### 1.2 你不要做什么

- 不要预测价格（所有对象卡只读结构）
- 不要修改对象卡字段定义（字段已冻结，只实现）
- 不要引入新的对象卡或策略（只实现已有的 12 张）
- 不要做实盘交易（只回测）

### 1.3 工作空间

所有代码和产出放在 `D:\Stock\trading_assistant`（活跃仓库）或 `E:\downloads\Desktop\找系统\特征`（资产目录）。

---

## 2. 参考文件清单（必读）

### 2.1 对象卡文件（12 张，核心输入）

按回测优先级排列：

| 顺序 | 文件路径 | 对象卡 | 功能层 | 优先级 | 备注 |
|------|----------|--------|--------|--------|------|
| 1 | `OBJECT_CARD_VOLFAC_P0_A__VolatilityFactor_v1.0.md` | VOLFAC | 选股 | 第一批 | 纯 OHLCV，最简单 |
| 2 | `OBJECT_CARD_TKR7_P0_E__AO_Divergence_v1.0.md` | TKR7 | 执行 | 第一批 | 纯 OHLCV，标准指标 |
| 3 | `OBJECT_CARD_VP_P0_E__VolumeProfile_v1.0.md` | VP | 执行 | 第一批 | 纯 OHLCV，但需滚动窗口 |
| 4 | `OBJECT_CARD_BPB_P0_E__Brooks_Breakout_Pullback_v1.0.md` | BPB | 执行 | 第一批 | 纯 OHLCV，价格行为 |
| 5 | `OBJECT_CARD_VOLTARGET_P0_R__VolatilityTargeting_v1.0.md` | VOLTARGET | 风控 | 第二批 | 依赖 VOLFAC 输出 |
| 6 | `OBJECT_CARD_MFLOW_P0_A__MoneyFlow_v1.0.md` | MFLOW | 选股 | 第二批 | 依赖 Wind 资金流向 |
| 7 | `OBJECT_CARD_YTC_P0_E__YTC_Microstructure_v1.0.md` | YTC | 执行 | 第二批 | 需多周期 S/R |
| 8 | `OBJECT_CARD_CHZL_BSD_P0_E__Chanlun_Buy_Sell_Signals_v1.0.md` | CHZL_BSD | 执行 | 第三批 | 依赖笔/中枢推导 |
| 9 | `OBJECT_CARD_KELLY_P0_R__KellyCriterion_v1.0.md` | KELLY | 风控 | 第三批 | 依赖交易日志 |
| 10 | `OBJECT_CARD_INSTB_P0_A__InstitutionalBehavior_v1.0.md` | INSTB | 方法 | 第五批 | 季频滞后，方法层 |
| 11 | `OBJECT_CARD_ATRATIO_P0_A__ActiveTradeRatio_v1.0.md` | ATRATIO | 选股 | 有条件 | A 股纯多头无效，跳过 |
| 12 | `OBJECT_CARD_CHZL_ZS_量化公式与互锁视图_v1.0.md` | 缠论体系 | 结构 | 基础 | 分型/笔/中枢/SQL 视图 |

### 2.2 架构文档（设计规范）

| 文件 | 用途 |
|------|------|
| `BACKTEST_FRAMEWORK_DESIGN_v1.0.md` | 回测引擎架构：统一输出接口、互锁执行顺序、投票融合规则、成熟度升级验收 |
| `OBJECT_CARD_BACKTEST_SCHEDULE_v1.0.md` | 回测排期：按周分批、数据需求、每周检查点 |
| `DATA_AVAILABILITY_AUDIT_v1.0.md` | 数据审计：数据获取路径、降级策略、质量检查 |
| `EXTERNAL_SYSTEM_REFERENCE_v1.0.md` | 外部参考：KA-MATS/Quant67/B3/vnpy 的设计借鉴 |
| `全仓库功能映射大表_v2.0.md` | 全仓库 58 对象的功能映射、成熟度、互锁关系 |

### 2.3 数据来源（已确认就绪）

```text
✓ 日 OHLCV（前复权，2018-2024，全 A 股）
✓ 周线 OHLCV（从日线合成）
✓ 分钟级 OHLCV（60min/15min/5min，2019-2024）
✓ Wind 资金流向数据（mfd_sellord, mfd_volinflowrate_open_m）
✓ 缠论笔/中枢推导代码（已有现成逻辑）
✓ ATR14（从 OHLCV 计算）

✗ 季报机构持仓（可选，INSTB 方法层用）
✗ Level-2 逐笔数据（ATRATIO 用，但纯多头无效，跳过）
✗ 外汇 OHLCV（TK 策略用，可选）
```

---

## 3. 统一输出接口（硬性规范）

### 3.1 所有对象卡必须输出的字段

每个对象卡无论内部多复杂，对外返回必须是以下字典结构：

```python
# 标准输出接口（Python dict）
# 所有字段名必须与对象卡文件中的定义完全一致

standard_output = {
    # === 基础信息（必填） ===
    "object_id": str,           # 如 "CHZL_BSD_P0_E"
    "object_name": str,         # 如 "缠论三类买卖点"
    "function_bucket": str,     # "STRUCTURE" / "ENERGY" / "EXECUTION" / "RISK" / "SELECTION"
    "process_layer": str,       # "FEATURE" / "SIGNAL" / "FILTER" / "POSITION" / "EXECUTION_CONSTRAINT"
    "timestamp": str,             # "2024-01-15"（K 线日期）
    "symbol": str,              # 如 "000001.SZ"
    "timeframe": str,           # "DAILY" / "WEEKLY" / "60MIN" / "15MIN" / "5MIN" / "1MIN"

    # === 信号核心（至少填一项） ===
    "signal_type": str,         # "NONE" / "LONG" / "SHORT" / "FILTER_PASS" / "FILTER_BLOCK" / "ENHANCE" / "DOWNGRADE" / "CONTEXT"
    "signal_strength": int,      # 0-10，执行层 ≥ 5 才有投票权
    "signal_confidence": float,  # 0.0-1.0，< 0.3 视为噪音

    # === 互锁（执行层必填） ===
    "lock_status": str,         # "LOCKED" / "UNLOCKED" / "CONFLICT" / "EXPIRED"
    "lock_reason": str,         # 锁定/解锁原因简述

    # === 过滤操作（过滤器/风控层必填） ===
    "filter_action": str,       # "PASS" / "ENHANCE" / "DOWNGRADE" / "BLOCK" / "CONTEXT_ONLY" / "REVERSE"
    "target_object_id": str,    # filter_action 的作用对象，空字符串表示全局

    # === 风控（风控层必填） ===
    "risk_action": str,         # "NONE" / "REDUCE_SIZE" / "INCREASE_SIZE" / "FORCE_CLOSE" / "HALT_NEW" / "CRISIS_MODE"
    "size_scalar": float,       # 仓位缩放系数，1.0=标准，0.0=禁止
    "stop_adjustment": float,   # 止损调整（ATR 倍数偏移），0.0=不调整

    # === 元数据（必填） ===
    "maturity_status": str,     # "FROZEN_FIELDS" / "PSEUDO_TESTED" / "SINGLE_FACTOR_BT" / "COMBINED_BT" / "OUT_OF_SAMPLE" / "PROXY_QUANTIZABLE"
    "data_requirement": str,    # "OHLCV" / "OHLCV_INTRADAY" / "LEVEL2" / "QUARTERLY" / "FUND_FLOW" / "MULTI"
    "effectiveness_scope": str, # "ASHARE_LONG_ONLY" / "ASHARE_LONG_SHORT" / "GLOBAL" / "ASHARE_METHOD"
}
```

### 3.2 接口验证规则（回测引擎的硬性检查）

在消费任何对象卡输出前，回测引擎必须执行以下检查。任一失败，该对象卡输出被丢弃：

```python
VALIDATION_RULES = [
    "timestamp 必须在该 K 线收盘后（避免未来信息泄露）",
    "signal_confidence < 0.3 的 signal_type 强制设为 'NONE'",
    "filter_action == 'BLOCK' 时必须有 target_object_id 或明确标注 'GLOBAL_BLOCK'",
    "risk_action == 'FORCE_CLOSE' 时必须有 stop_adjustment 和 size_scalar",
    "ASHARE_LONG_ONLY 环境下 signal_type == 'SHORT' 的输出被丢弃",
    "timeframe 必须与 process_layer 兼容（如 SELECTION 层不支持 1MIN）",
    "data_requirement 必须与当前数据环境匹配（无 LEVEL2 时丢弃 LEVEL2 依赖对象卡）",
]
```

---

## 4. Pipeline 执行顺序（硬性约束）

### 4.1 时间框架优先级

```
WEEKLY Pipeline → DAILY Pipeline → INTRADAY Pipeline（60MIN/15MIN/5MIN）
     │
     ▼ 上下文注入（单向）
```

**规则 1**：高时间框架优先。周线必须先于日线计算。周线 `CONFLICT` 或 `UNLOCKED` 时，日线 Pipeline 暂停选股。

**规则 2**：选股层先于执行层。`SELECTION` 层（MFLOW/VOLFAC）在 `STRUCTURE` 层之前计算。被 `BLOCK` 的标的不进入后续层。

**规则 3**：风控层在投票前最后介入。`RISK` 层在 `VOTE_POOL` 前调制 `size_scalar`。

**规则 4**：投票通过后，风控层再次检查。Van Tharp 2% 硬性上限触发 → 强制 `ABORT`。

### 4.2 上下文注入规范

```python
# 高时间框架向低时间框架注入的内容（只读，不反向）
INJECTED_CONTEXT = {
    "signal_type": str,         # 信号类型
    "signal_strength": int,     # 信号强度（作为下限基准）
    "lock_status": str,         # 互锁状态
    "lock_reason": str,         # 锁定原因
}

# 不注入的内容（避免信息泄露）
NOT_INJECTED = ["stop_adjustment", "size_scalar", "内部中间字段"]

# 接收规则（低时间框架如何处理）
RECEIVE_RULES = {
    "周线 LONG + LOCKED → 日线 signal_strength 最低为 5",
    "周线 CONFLICT → 日线 signal_confidence × 0.5",
    "周线 NONE → 不影响日线（多周期共振是增强，不是前提）",
}
```

---

## 5. 投票与信号融合（entry_min_votes = 3）

### 5.1 有投票权的对象（必须满足全部条件）

```python
VOTE_ELIGIBLE = {
    "function_bucket": ["EXECUTION", "FILTER"],
    "signal_type": ["LONG", "SHORT", "FILTER_PASS"],
    "signal_strength": lambda x: x >= 5,
    "lock_status": ["LOCKED", "UNLOCKED"],
    "signal_confidence": lambda x: x >= 0.3,
    "maturity_status": ["SINGLE_FACTOR_BT", "COMBINED_BT", "OUT_OF_SAMPLE", "PROXY_QUANTIZABLE"],
}
```

### 5.2 投票规则

```python
VOTE_RULES = [
    "日线至少 3 个有投票权的对象投 LONG/FILTER_PASS → 触发执行",
    "多周期共振：周线票 × 1.5 + 日线票 × 1.0 + 分钟票 × 0.8，总分 ≥ 5 时 strength + 1",
    "过滤器否决：filter_action='BLOCK' 且 target 匹配 → 该票被扣除",
    "风控一票否决：Van Tharp 2% 触发 → 强制 ABORT",
    "同一功能 bucket 最多贡献 2 票（防止单一维度过度集中）",
]
```

### 5.3 最终信号生成

```python
def generate_final_signal(vote_pool, risk_modulation):
    """
    步骤：
    1. 收集所有有投票权对象的 signal_type
    2. 计算赞成票、反对票、弃权票
    3. 应用过滤器否决（扣除被 BLOCK 的票）
    4. 应用风控层一票否决（如触发）
    5. 检查加权总分 ≥ 3？
       YES → final_signal_type = 'LONG'（若赞成 > 反对）
            final_signal_strength = min(10, 平均赞成票 strength + 多周期共振加分)
            final_size_scalar = min(所有风控层 size_scalar)  # 取最保守的
            final_stop_adjustment = 所有风控层 stop_adjustment 的加权平均
       NO  → final_signal_type = 'ABORT'
            abort_reason = 原因字符串（票数不足/风控否决/过滤器阻断）
    """
    pass
```

---

## 6. 对象卡实现要点（按优先级）

### 6.1 VOLFAC（第一批，最简单）

```python
# 核心逻辑：60 日收益率标准差 → 年化波动率 → 历史分位 → 波动率状态
# 输入：日收盘价（60 日滚动窗口）
# 输出：volfac_id2_std_3m, volfac_annualized_vol, volfac_vol_percentile, volfac_vol_regime, volfac_vol_trend
# 关键阈值：分位 > 80% = HIGH_VOL, < 20% = LOW_VOL, > 95% = EXTREME_VOL
# 小盘股分层：按市值分层计算分位（<50亿, 50-500亿, >500亿）
```

### 6.2 TKR7（第一批，标准指标）

```python
# 核心逻辑：AO = SMA(median_price, 5) - SMA(median_price, 34)
# 背离检测：价格新高但 AO 未新高 = 常规背离；价格新低但 AO 未新低 = 常规底背离
# 隐藏背离：价格回撤但未破前低，AO 更高 = 隐藏看涨背离
# 输入：日 OHLCV
# 输出：ao_divergence_type, ao_divergence_confidence, ao_peak_diff, ao_force_exit
# 关键阈值：confidence < 0.3 过滤；age > 8 过期；age 2-3 提前预警（A 股 T+1）
```

### 6.3 VP（第一批，滚动窗口）

```python
# 核心逻辑：滚动 60 日成交量分布 → POC / VAH / VAL / HVN / LVN
# 信号：价格突破 VAH 做多，突破 VAL 做空；价格回归 POC 观察
# 输入：日 OHLCV（60 日滚动窗口）
# 输出：poc, vah, val, va_breakout_signal, volume_integrity_score
# 关键阈值：volume_integrity_score < 0.6 时信号降级；数据 < 20K 线时不可靠
```

### 6.4 BPB（第一批，价格行为）

```python
# 核心逻辑：识别趋势线 → 检测突破 → 测量回调深度
# 1st pullback：突破后首次回调，可交易
# 2nd pullback：突破后第二次回调，限制交易
# 3rd+ pullback：不交易
# 输入：日 OHLCV
# 输出：bpb_pullback_count, bpb_callback_depth, bpb_breakout_quality, bpb_signal_type
# 关键阈值：callback_depth > 0.618 视为反转；body_pct < 0.3 突破质量差
```

### 6.5 VOLTARGET（第二批，依赖 VOLFAC）

```python
# 核心逻辑：目标波动率（大盘股 10%，小盘股 20%）/ 当前波动率 = scalar
# 输入：VOLFAC 的 volfac_annualized_vol
# 输出：vt_scalar, vt_size_scalar, vt_current_vol, vt_vol_regime
# 关键阈值：EXTREME_VOL → scalar = 0.2；HIGH_VOL → scalar < 1.0；LOW_VOL → scalar > 1.0
# A 股适配：涨停/跌停日 ATR 用前 20 日非停日均值；T+1 隔夜风险 target_vol + 2-3%
```

### 6.6 MFLOW（第二批，依赖 Wind 数据）

```python
# 核心逻辑：主力流出单数占比 + 开盘净流入率 → 资金流向信号
# 输入：Wind 资金流向数据（mfd_sellord, mfd_volinflowrate_open_m）
# 输出：mflow_sellord_ratio, mflow_inflow_ratio, mflow_open_intent, mflow_divergence_score
# 关键阈值：sellord_ratio > 0.6 → BLOCK；inflow_ratio > 0.05 → ENHANCE
# A 股适配：早盘 9:30 首笔数据可用；小盘股/ST 股数据缺失标记为 'NONE'
```

### 6.7 CHZL_BSD（第三批，最复杂）

```python
# 核心逻辑：分型 → 笔 → 中枢 → 背驰 → 三类买卖点
# 输入：日 OHLCV → 推导分型/笔/中枢/背驰
# 输出：bsd_type（1Buy/2Buy/3Buy/1Sell/2Sell/3Sell）, bsd_stop_price, bsd_is_trailing, bsd_id
# 止损：1Buy = bi.low - 0.5×ATR；2Buy = prev_low - 0.2×ATR；3Buy = zs.zd - 0.1×ATR
# 关键：旧笔规则（顶底间 ≥ 2 独立 K 线）；MACD 面积背驰（a段 vs c段）
# 互锁：与 KD MTF 共振确认；与 MFLOW 资金确认；与 VP 突破确认
```

---

## 7. 回测引擎核心模块（需实现）

### 7.1 模块清单

```text
backtest_engine/
├── data/
│   ├── data_loader.py          # 统一数据加载器（DataLoader 类）
│   ├── data_validator.py       # 数据质量检查（缺失率、复权一致性、成交量一致性）
│   └── feature_store.py        # 特征缓存（Parquet 格式，按 symbol/date/version 索引）
├── objects/
│   ├── base_object.py          # 对象卡基类（定义标准输出接口）
│   ├── volfac.py              # VOLFAC 对象卡实现
│   ├── tkr7.py                # TKR7 对象卡实现
│   ├── vp.py                  # VP 对象卡实现
│   ├── bpb.py                 # BPB 对象卡实现
│   ├── voltarget.py           # VOLTARGET 对象卡实现
│   ├── mflow.py               # MFLOW 对象卡实现
│   ├── ytc.py                 # YTC 对象卡实现
│   ├── chzl_bsd.py            # CHZL_BSD 对象卡实现
│   ├── kelly.py               # KELLY 对象卡实现
│   └── instb.py               # INSTB 对象卡实现（方法层，不干预执行）
├── pipeline/
│   ├── weekly_pipeline.py      # 周线 Pipeline
│   ├── daily_pipeline.py     # 日线 Pipeline（含选股层 → 结构层 → 能量层 → 执行层 → 风控层）
│   ├── intraday_pipeline.py  # 分钟级 Pipeline
│   └── interlock_engine.py   # 互锁检查引擎
├── vote/
│   ├── vote_pool.py           # 投票池（收集有投票权对象）
│   ├── vote_fusion.py         # 信号融合（加权投票、过滤器否决、风控一票否决）
│   └── signal_generator.py   # 最终信号生成
├── risk/
│   ├── van_tharp.py          # Van Tharp 2% 硬性上限
│   ├── kelly_manager.py      # Kelly 动态优化（半凯利/四分之一凯利/自适应）
│   └── voltarget_manager.py  # VolTarget 环境系数调制
├── execution/
│   ├── trade_executor.py     # 交易执行模拟（买入/卖出/止损）
│   ├── position_tracker.py   # 持仓跟踪
│   └── trade_logger.py       # 交易日志（用于 KELLY 和绩效评估）
├── performance/
│   ├── metrics.py            # 绩效指标计算（年化收益、夏普、最大回撤、胜率、盈亏比）
│   ├── benchmark.py          # 基准对比（纯现金持有 + 买入持有）
│   └── report_generator.py  # 回测报告生成
└── config/
    ├── backtest_config.yaml   # 回测参数配置（entry_min_votes, stop_k, atr_n, 交易成本等）
    └── object_registry.json   # 对象卡注册表（列出所有激活的对象卡及其参数）
```

### 7.2 关键配置参数（已冻结，不可修改）

```yaml
# backtest_config.yaml
backtest:
  start_date: "2018-01-01"
  end_date: "2024-12-31"
  capital: 1000000
  stock_pool: "all_a_share"  # 或 "hs300_zz500_zz1000"
  exclude_st: true
  exclude_new_stock_days: 252  # 上市不足 1 年剔除
  
trading:
  entry_min_votes: 3
  allow2_risk_mult: 0.20
  stop_k: 1.5
  atr_n: 14
  transaction_cost: 0.0025  # 双边 0.25%
  t1_penalty: 0.8  # T+1 惩罚系数（Kelly 用）
  max_single_stock_weight: 0.20  # 单票上限 20%

risk:
  van_tharp_max_risk: 0.02  # 2% 硬性上限
  kelly_default_f: 0.25  # 默认半凯利
  kelly_crisis_threshold: 3  # 连续亏损 3 笔进入危机模式
  voltarget_target_vol_large: 0.10  # 大盘股目标波动率 10%
  voltarget_target_vol_small: 0.20  # 小盘股目标波动率 20%
```

---

## 8. 验收标准（编程 AI 的交付物必须满足）

### 8.1 代码质量

```text
□ 所有对象卡实现必须符合标准输出接口（3.1 节）
□ 所有对象卡字段名与对象卡文件中的定义完全一致
□ 代码中有明确的注释标注"字段冻结，不可修改"
□ 使用类型提示（Python type hints）
□ 使用 polars 替代 pandas（性能要求）
□ 单元测试覆盖每个对象卡的核心计算逻辑
```

### 8.2 功能验证

```text
□ DataLoader 能正确加载所有确认就绪的数据源
□ 每个对象卡能独立运行并输出标准字段
□ 互锁引擎能正确检测 CONFLICT/EXPIRED 并降级
□ 投票池能正确计算赞成票/反对票/加权总分
□ 风控层能在投票前和投票后正确调制 size_scalar
□ 交易执行能正确模拟 T+1（买入后次日才能卖出）
□ 绩效指标计算正确（与手动计算对比验证）
```

### 8.3 第一批回测验收（Week 1-2 目标）

```text
□ VOLFAC：高波动分位（>80%）标的年化收益 < 低波动分位（<20%）标的
□ TKR7：常规背离胜率 > 40%，隐藏背离胜率 > 45%
□ VP：VA 突破胜率 > 42%，volume_integrity_score ≥ 0.6 时胜率显著高于 < 0.6
□ BPB：1st pullback 胜率 > 45%，2nd pullback 胜率 > 40%
□ 所有对象卡：信号不劣于纯现金持有（无信号基准）
```

---

## 9. 已知限制与注意事项

```text
1. ATRATIO 纯多头无效：ASHARE_LONG_ONLY 环境下 ATRATIO 对象卡应跳过，不投入计算资源
2. INSTB 方法层：不干预实时执行，只作为选股池背景参考，无需进入 Pipeline 执行层
3. 涨停/跌停处理：所有涉及 ATR 计算的对象卡必须使用 limit_atr_corrector（剔除涨跌停日）
4. 小盘股分层：VOLFAC 和 VOLTARGET 必须按市值分层处理（<50亿, 50-500亿, >500亿）
5. 数据缺失：即使数据已确认就绪，代码中仍需实现降级路径（以防未来数据缺失）
6. 并发安全：Feature Store 缓存需线程安全，支持多进程并行（对象卡计算天然可并行）
7. 版本控制：每次回测记录参数版本、数据哈希、对象卡版本号，确保可复现
```

---

## 10. 交付物清单

编程 AI 完成第一批（Week 1-2）后，需交付以下文件：

```text
deliverables_week1_2/
├── code/
│   ├── backtest_engine/          # 完整回测框架代码（7.1 节模块清单）
│   ├── tests/                    # 单元测试
│   └── notebooks/                # 验证 notebook（每个对象卡一个）
├── data/
│   ├── feature_store/            # 预计算特征缓存（Parquet 格式）
│   └── backtest_results/         # 回测结果（每个对象卡一个 CSV）
├── reports/
│   ├── volfac_backtest_report.md # VOLFAC 单因子回测报告
│   ├── tkr7_backtest_report.md   # TKR7 单因子回测报告
│   ├── vp_backtest_report.md     # VP 单因子回测报告
│   ├── bpb_backtest_report.md    # BPB 单因子回测报告
│   └── summary.md                # 第一批总结：各对象卡表现、问题、下一步建议
└── config/
    ├── backtest_config.yaml      # 实际使用的回测参数
    └── object_registry.json    # 实际激活的对象卡列表
```

---

> 文件：MASTER_PROGRAMMING_INSTRUCTION_v1.0.md  
> 生产者：Kimi  
> 状态：数据已确认就绪，可全面启动编码  
> 建议：编程 AI 按此指令书实现，每周对照 OBJECT_CARD_BACKTEST_SCHEDULE_v1.0.md 检查进度
> 
> 关键决策记录：
> - 数据就绪：日 OHLCV ✓ / 周线 ✓ / 分钟级 ✓ / Wind 资金流 ✓ / 缠论推导 ✓
> - ATRATIO 跳过：A 股纯多头无效，不投入资源
> - INSTB 方法层：不干预执行，仅在选股池使用
> - 技术栈：Python + polars + pytest + yaml/json
