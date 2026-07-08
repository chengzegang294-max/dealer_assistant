# 交易策略设计参考 v1.0 — 基于外部资料与现有架构的融合

> **文档编号**: REF-DESIGN-v1.0
> **创建日期**: 2026-07-07
> **依赖文档**: `SYSTEM_ARCHITECTURE_DRAFT.md` + `STRATEGY_BUNDLES_v1.0.md` + `EXTERNAL_STRATEGY_RAW_MATERIAL_v1.0.md`
> **用途**: 将外部搜索到的策略启发，转化为现有三层架构内的可落地方案。
> **原则**: 不新增独立模块，所有增强必须自然生长于现有架构内。

---

## 1. 外部资料的启发摘要

本次搜索（3批次30条结果）覆盖了以下策略类型：

| 策略类型 | 代表来源 | 核心启发 | 采纳状态 |
|----------|----------|----------|----------|
| 多因子趋势共振 | 通达信多因子系统 | 动态阈值、多周期共振确认 | **v1.0采纳** |
| 多因子周期共振波动率 | 文华转通达信 | 震荡市均值回归策略 | **v1.1采纳** |
| 动态RSI+CCI | FMZ策略库 | 动态阈值、ADX趋势过滤、交易量确认 | **v1.0采纳** |
| 多因子均值回归 | FMZ策略库 | StochRSI+布林带、ADX过滤 | **v1.1采纳** |
| 深度学习多因子 | 天算量化 | 自适应权重、Barra组合风控 | **v1.1采纳** |
| 打板/短线 | 多篇游资策略 | 板块热度、竞价规则 | **部分借鉴** |
| 机构多因子分类 | 公募基金研报 | 组合优化模型、风格暴露控制 | **v1.1采纳** |

**关键共识**: 所有成熟的外部策略都遵循 "环境判断 → 多因子共振 → 风控执行 → 组合优化" 的四层结构。我们的三层架构已覆盖前三级，第四级（组合风控）是主要差距。

---

## 2. 现有架构的增强设计

### 2.1 增强一：ADX 趋势过滤器（v1.0）

**问题**: 现有 `VOLFAC` 只输出波动率高低（NORMAL/HIGH/LOW），不区分"趋势"和"震荡"。在震荡市场中，趋势跟踪策略会频繁亏损。

**外部启发**: 动态RSI+CCI策略使用ADX>25作为趋势过滤器，ADX<20作为无趋势（震荡）过滤器。

**设计方案**:

```python
# VOLFAC 对象卡增强（不新增对象卡，只增加字段）
interface_volfac_enhanced = {
    # 原有字段
    "volfac_vol_regime": str,        # NORMAL / HIGH / LOW
    "volfac_current_vol": float,      # 当前波动率
    "volfac_percentile": float,       # 历史分位数
    
    # 新增字段（v1.0）
    "volfac_adx_value": float,        # ADX值（14日）
    "volfac_adx_trend_state": str,   # STRONG_TREND / WEAK_TREND / NO_TREND
    "volfac_trend_direction": str,    # UPTREND / DOWNTREND / SIDEWAYS
}

# ADX 状态定义
adx_state_map = {
    "STRONG_TREND": "adx >= 25",     # 强趋势，优先趋势跟踪
    "WEAK_TREND": "20 <= adx < 25",  # 弱趋势，观望或轻仓
    "NO_TREND": "adx < 20",          # 无趋势，优先均值回归
}

# 与 PERIOD_QUEEN 的协同
# 当 regime_state = POWER_TRANSITION 且 adx_state = NO_TREND 时：
#   → 系统推荐切换至 MeanReversion 策略包（v1.1）
# 当 regime_state = ATTACK_SUSTAINED 且 adx_state = STRONG_TREND 时：
#   → 增强趋势跟踪信号（strength +1）
```

**对 STRATEGY_BUNDLES 的影响**: 在 `TrendFollowing` 和 `BuildPosition` 策略包的 `entry_conditions` 中增加：

```yaml
entry_conditions:
  - "volfac_adx_trend_state in [STRONG_TREND, WEAK_TREND]"
  - "若 NO_TREND → 降低 entry_min_votes 到 4（提高门槛）"
```

**数据需求**: ADX 可用日 OHLCV 计算（`DM+`, `DM-`, `TR`, `DX`, `ADX`），无需额外数据。`proxy_quantizable_now`。

---

### 2.2 增强二：动态阈值（RSI/KD 自适应）（v1.0）

**问题**: 现有 `TKR7` 和 `KD MTF` 使用固定阈值（RSI 70/30，KD 80/20）。在高波动市场中，固定阈值过于敏感；在低波动市场中，过于迟钝。

**外部启发**: 动态RSI+CCI策略使用"动态阈值"，根据市场波动率调整超买超卖阈值。

**设计方案**:

```python
# TKR7 对象卡增强
interface_tkr7_enhanced = {
    # 原有字段
    "tkr7_divergence_type": str,      # REGULAR_TOP / HIDDEN_TOP / etc.
    "tkr7_divergence_age": int,       # 背离年龄
    "tkr7_strength": int,
    
    # 新增字段（v1.0）
    "tkr7_rsi_dynamic_threshold": float,    # 动态RSI阈值（基于波动率）
    "tkr7_rsi_base_threshold": float,       # 基础阈值（70/30）
    "tkr7_threshold_adjustment": float,     # 调整量（±5-10）
}

# 动态阈值计算公式
def calculate_dynamic_threshold(base_threshold, volfac_percentile, volfac_vol_regime):
    """
    根据波动率调整RSI/KD阈值
    """
    if volfac_vol_regime == "HIGH":
        # 高波动：放宽阈值，避免过早触发
        adjustment = +5  # 超买阈值从70→75，超卖从30→25
    elif volfac_vol_regime == "LOW":
        # 低波动：收紧阈值，提高灵敏度
        adjustment = -3  # 超买阈值从70→67，超卖从30→33
    else:
        adjustment = 0
    
    return base_threshold + adjustment

# 示例
# HIGH_VOL: 超买阈值 = 75, 超卖阈值 = 25
# NORMAL_VOL: 超买阈值 = 70, 超卖阈值 = 30
# LOW_VOL: 超买阈值 = 67, 超卖阈值 = 33
```

**对 KD MTF 的影响**: 同理，KD 的 K/D 阈值（80/20）也改为动态：

```python
kd_dynamic_threshold = {
    "HIGH_VOL": {"overbought": 85, "oversold": 15},
    "NORMAL_VOL": {"overbought": 80, "oversold": 20},
    "LOW_VOL": {"overbought": 75, "oversold": 25},
}
```

**数据需求**: 仅需日 OHLCV + `VOLFAC` 输出。`proxy_quantizable_now`。

---

### 2.3 增强三：交易量确认（投票机制增强）（v1.0）

**问题**: 现有投票机制只考虑对象卡的信号强度，不考虑成交量确认。假突破常伴随成交量不足。

**外部启发**: 多因子趋势共振系统、捉妖筹码峰、动态RSI+CCI策略都强调"成交量确认"是过滤假信号的关键。

**设计方案**:

```python
# 投票机制增强（VoteEngine）
class VoteEngineEnhanced:
    """
    在原 VoteEngine 基础上增加交易量确认模块
    """
    
    def calculate_volume_confirm(self, symbol, signal_date, df_ohlcv):
        """
        计算交易量确认分数
        """
        current_volume = df_ohlcv.loc[signal_date, 'volume']
        volume_ma5 = df_ohlcv['volume'].rolling(5).mean().loc[signal_date]
        volume_ma20 = df_ohlcv['volume'].rolling(20).mean().loc[signal_date]
        
        # 确认条件
        volume_confirm_score = 0
        if current_volume > volume_ma5 * 1.2:  # 当日量 > 5日均量 20%
            volume_confirm_score += 1
        if current_volume > volume_ma20 * 1.5:  # 当日量 > 20日均量 50%
            volume_confirm_score += 1
        if volume_ma5 > volume_ma20:  # 5日均量 > 20日均量（量增趋势）
            volume_confirm_score += 1
        
        return volume_confirm_score  # 0-3
    
    def adjust_strength_by_volume(self, signal_strength, volume_confirm_score):
        """
        根据交易量确认调整信号强度
        """
        if volume_confirm_score >= 2:
            return signal_strength + 1  # 成交量确认充分，增强信号
        elif volume_confirm_score == 0:
            return max(0, signal_strength - 1)  # 成交量不足，削弱信号
        return signal_strength

# 在 Vote 决策中的应用
vote_pool = {
    "chzl_bsd": {"strength": 8, "signal_type": "3Buy"},
    "bpb": {"strength": 7, "signal_type": "1st_pullback"},
    "mflow": {"strength": 7, "signal_type": "MAIN_FORCE_IN"},
}

# 增强后
volume_confirm = calculate_volume_confirm(symbol, today, df)
for obj_id in vote_pool:
    vote_pool[obj_id]["strength"] = adjust_strength_by_volume(
        vote_pool[obj_id]["strength"], volume_confirm
    )
```

**与 MFLOW 的协同**: `MFLOW` 的 `MAIN_FORCE_IN` 信号已经包含资金流向信息。当 `volume_confirm_score >= 2` 且 `MFLOW` 确认主力流入时，信号强度额外+1（互锁增强）。

**数据需求**: 日 OHLCV 的 `volume` 字段。已有数据。`proxy_quantizable_now`。

---

### 2.4 增强四：组合风控层（v1.1）

**问题**: 现有风控（`Van Tharp + Kelly + VolTarget`）只控制单票风险，不控制组合层面的风险（行业集中、风格暴露、相关性）。

**外部启发**: 天算量化的Barra模型、公募基金的组合优化模型、多因子均值回归策略的"分散化"要求。

**设计方案**:

```python
# 新增组合风控对象卡：PORTFOLIO_RISK_P1_R
interface_portfolio_risk = {
    "object_id": "PORTFOLIO_RISK_P1_R",
    "object_name": "组合风控层",
    "function_bucket": "RISK",
    "process_layer": "PORTFOLIO",
    
    # 输入：当前持仓组合
    "portfolio_holdings": list,         # [{symbol, weight, industry, style}, ...]
    
    # 输出：组合风控指令
    "pr_industry_max_concentration": float,  # 单行业集中度上限（默认20%）
    "pr_style_exposure_limits": dict,        # 风格暴露限制（市值/价值/成长）
    "pr_correlation_check": bool,            # 持仓相关性检查
    "pr_action": str,                       # NORMAL / REDUCE_SECTOR / REBALANCE
    "pr_rebalance_instructions": list,       # 具体调仓指令
}

# 组合风控规则
portfolio_risk_rules = {
    # 行业集中度
    "industry_concentration": {
        "max_single_industry": 0.20,        # 单行业不超过20%
        "max_top3_industries": 0.60,         # 前3行业不超过60%
    },
    
    # 风格暴露（基于A5财报数据）
    "style_exposure": {
        "market_cap_bias": "-0.3 to +0.3",   # 市值偏离基准范围
        "value_growth_bias": "-0.2 to +0.2",   # 价值/成长偏离
        "profitability_bias": "-0.2 to +0.2",  # 盈利质量偏离
    },
    
    # 相关性矩阵
    "correlation_limit": {
        "max_pairwise_correlation": 0.70,   # 任意两只持仓相关性<70%
        "min_diversification_ratio": 0.50,   # 分散化比率>50%
    },
    
    # 触发调仓的条件
    "rebalance_triggers": [
        "单行业突破20%",
        "风格偏离超限",
        "相关性矩阵异常",
        "新入选股票与现有持仓相关性>0.70",
    ],
}
```

**与现有风控的层级关系**:

```
现有风控层（单票）              新增组合风控层（v1.1）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Van Tharp 2% 单票上限           行业集中度 20% 上限
Kelly 动态仓位优化              风格暴露偏离控制
VolTarget 波动率调制            持仓相关性矩阵检查
PeriodQueen 状态仓位上限        组合再平衡指令

最终仓位 = min(VanTharp, Kelly, VolTarget, PeriodQueen, PortfolioRisk)
```

**数据需求**: 需要行业分类（申万/中信）、风格因子（市值/PE/PB/ROE）。A5财报数据已有部分。`proxy_quantizable_now`（基于现有数据），但计算相关性矩阵需要历史收益率数据。

**实现版本**: v1.1（非v1.0优先）。

---

### 2.5 增强五：均值回归策略包（v1.1）

**问题**: 现有7个策略包中，没有专门应对"震荡市"的策略。在 `POWER_TRANSITION` 和 `GESTATION` 状态，系统只能"观望/试错"，效率低。

**外部启发**: 多因子周期共振波动率、多因子均值回归策略（StochRSI+布林带）、聚宽均值回归策略。

**设计方案**:

```yaml
# 新增策略包：MeanReversion（均值回归）
strategy_name: "MeanReversion"
applicable_regime: ["POWER_TRANSITION", "GESTATION"]  # 仅在无趋势/震荡状态
permission: "REDUCED"
max_position_size: 0.3
entry_min_votes: 4

# 核心逻辑：
# 1. ADX < 20（无趋势）或 VOLFAC 判定为震荡
# 2. 价格偏离均线/布林带达到极端值
# 3. 结合 KD 超买超卖（动态阈值）
# 4. 成交量确认（防止假突破）

activated_objects:
  - KD_MTF_P0_E:
      priority: 1
      allowed_types: ["OVERBOUGHT", "OVERSOLD"]
      note: "KD超买超卖是均值回归的核心信号"
      threshold_mode: "DYNAMIC"  # 使用动态阈值
      
  - TKR7_P0_E:
      priority: 2
      allowed_types: ["REGULAR_TOP_DIVERGENCE", "REGULAR_BOTTOM_DIVERGENCE"]
      note: "常规背离在震荡市中更可靠"
      
  - BPB_P0_E:
      priority: 3
      allowed_types: ["FAILED_BREAKOUT", "FAILED_BREAKDOWN"]
      note: "突破失败反转（BOF）是震荡市的特征"
      
  - YTC_P0_E:
      priority: 4
      allowed_types: ["TST", "BOF"]
      note: "S/R框架内的测试和反转"

risk_params:
  van_tharp_max_risk: 0.01  # 更严格（震荡市假信号多）
  kelly_mode: "quarter_kelly"
  voltarget_target_vol: "low"

position_strategy:
  - 单票上限: 0.05
  - 组合上限: 0.3
  - 建仓方式: "一次性试仓（不加仓）"
  - 止损: "布林带另一侧边界或 2% 固定止损"
  - 止盈: "回归均线或 3% 固定止盈"

exit_conditions:
  - "价格回归均线（偏离度<2%）"
  - "ADX 突破 25（趋势出现）→ 立即退出，切换策略包"
  - "持仓超过 5 日未回归 → 强制退出（均值回归有时间窗口）"
  - " KD 反向信号触发"

# 与现有策略包的关键区别
# 1. 不做趋势跟随，只做"回归"交易
# 2. 持仓时间更短（3-5日 vs 趋势跟踪的数周）
# 3. 止损更严格（震荡市假信号代价高）
# 4. 当ADX突破25时自动退出，不贪恋
```

**触发条件**:

```python
def should_activate_mean_reversion(regime_state, adx_state, volfac_regime):
    """
    判断是否应该激活均值回归策略包
    """
    if regime_state in ["POWER_TRANSITION", "GESTATION"]:
        if adx_state == "NO_TREND" or volfac_regime == "OSCILLATION":
            return True
    return False
```

**数据需求**: 日 OHLCV + ADX + KD + 布林带。全部可用。`proxy_quantizable_now`。

**实现版本**: v1.1（非v1.0优先，因为需要先实现ADX）。

---

## 3. 与现有对象卡的修改清单

### 3.1 v1.0 修改（立即实现）

| 对象卡 | 修改内容 | 影响面 | 数据需求 |
|--------|----------|--------|----------|
| `VOLFAC_P0_A` | 新增 `adx_value`, `adx_trend_state`, `trend_direction` 字段 | 环境识别层 | 日 OHLCV |
| `TKR7_P0_E` | 新增 `rsi_dynamic_threshold`, `threshold_adjustment` 字段；阈值逻辑改为动态 | 执行层信号生成 | 日 OHLCV + VOLFAC |
| `KD_MTF_P0_E` | KD 超买超卖阈值改为动态（基于 VOLFAC） | 执行层信号生成 | 日 OHLCV + VOLFAC |
| `VoteEngine` | 新增 `volume_confirm` 模块，在投票前调整信号强度 | 执行层投票融合 | 日 OHLCV volume |

### 3.2 v1.1 修改（后续实现）

| 对象卡/模块 | 修改内容 | 影响面 | 数据需求 |
|-------------|----------|--------|----------|
| `PORTFOLIO_RISK_P1_R` | 新增组合风控对象卡（行业/风格/相关性） | 组合层风控 | 行业分类 + 风格因子 + 历史收益率 |
| `STRATEGY_BUNDLES` | 新增 `MeanReversion` 策略包 | 策略选择层 | 全部现有数据 |
| `PERIOD_QUEEN` | 新增 ADX 辅助判断逻辑 | 环境识别层 | VOLFAC 输出 |

---

## 4. 增强后的三层决策流示例

### 示例：震荡市中的均值回归交易（v1.1）

```
Day 1：PERIOD_QUEEN 判定 POWER_TRANSITION
  VOLFAC：vol_regime = NORMAL, adx_state = NO_TREND (adx = 15)
  → regime_state = POWER_TRANSITION
  → 系统推荐：MeanReversion 策略包（而非 WaitAndSee）

Day 2：KD_MTF 发出超卖信号（K=12, D=15，动态阈值 oversold=25）
  TKR7：常规底背离，strength=7
  YTC：TST 测试 S/R 下边界，strength=6
  
  VoteEngine：
    原始投票池：KD(8) + TKR7(7) + YTC(6) = 3票（< 4，门槛未达）
    VolumeConfirm：当日量 = 5日均量 × 1.3 → volume_confirm_score = 2
    → KD strength +1 → KD(9)
    → 最终投票池：KD(9) + TKR7(7) + YTC(6) = 3票（仍 < 4）
    → 不执行，继续观察

Day 3：KD_MTF 金叉（K上穿D），超卖区金叉
  BPB：FAILED_BREAKDOWN（跌破后快速收回），strength=7
  
  VoteEngine：
    原始投票池：KD(9) + TKR7(7) + YTC(6) + BPB(7) = 4票（≥ 4）
    VolumeConfirm：score = 2 → KD +1, BPB +1
    → 最终：KD(10) + TKR7(7) + YTC(6) + BPB(8) = 4票
    → PASS

  风控调制：
    Van Tharp：单票风险 < 1%（均值回归更严格）
    Kelly：quarter_kelly → size_scalar = 0.15
    VolTarget：low → scalar = 0.8
    PeriodQueen：max_size = 0.3
    最终：min(0.15, 0.8, 0.3) = 0.15
    
  执行：买入，仓位 = 0.15 × 标准仓位
    止损：布林带下轨 - 1% 或 2% 固定止损
    止盈：均线回归或 3% 固定止盈
    时间限制：5 日内未回归 → 强制退出

Day 5：价格回归均线，偏离度从 -8% 缩窄至 -1%
  → 触发止盈，退出
  
Day 6：ADX 突破 25（趋势出现）
  → 即使仍有持仓，强制退出 MeanReversion 策略
  → 系统切换至 TrendFollowing 或 BuildPosition 策略包
```

---

## 5. 对编程 AI 的指令

### 5.1 v1.0 优先级任务

1. **实现 ADX 计算模块** (`src/backtest_engine/indicators/adx.py`):
   - 输入：日 OHLCV
   - 输出：`adx_value`, `adx_trend_state`, `trend_direction`
   - 单元测试：用已知ADX值的数据验证计算正确性

2. **增强 VOLFAC 对象卡** (`src/backtest_engine/objects/volfac.py`):
   - 新增 `adx_value` 等字段
   - 修改 `volfac_vol_regime` 逻辑：当 `adx < 20` 时，标记为 `OSCILLATION`（新增状态）
   - 保持向后兼容：原有接口不变

3. **增强 TKR7 对象卡** (`src/backtest_engine/objects/tkr7.py`):
   - 新增动态阈值计算函数
   - 修改 `tkr7_strength` 计算逻辑：根据动态阈值调整信号强度
   - 单元测试：高波动/低波动/正常波动三种场景

4. **增强 KD_MTF 对象卡** (`src/backtest_engine/objects/kd_mtf.py`):
   - 同理，阈值改为动态
   - 注意：KD_MTF 是多周期对齐，各周期的阈值应独立调整

5. **增强 VoteEngine** (`src/backtest_engine/vote/vote_engine.py`):
   - 新增 `volume_confirm` 模块
   - 在投票前调用 `adjust_strength_by_volume()`
   - 保持原有投票逻辑不变（仅增加前置调整）

### 5.2 v1.1 后续任务

6. **实现组合风控对象卡** (`src/backtest_engine/objects/portfolio_risk.py`):
   - 需要行业分类数据和历史收益率数据
   - 实现行业集中度、风格暴露、相关性矩阵检查

7. **实现 MeanReversion 策略包** (`src/backtest_engine/strategy/mean_reversion.py`):
   - 基于现有对象卡（KD_MTF, TKR7, BPB, YTC）
   - 定义新的 `entry_min_votes=4` 和 `exit_conditions`
   - 与 `StrategyBundleEngine` 集成

8. **更新 StrategyBundleEngine**:
   - 新增 `should_activate_mean_reversion()` 判断逻辑
   - 当 `adx_state=NO_TREND` 时，在 `POWER_TRANSITION`/`GESTATION` 状态推荐 MeanReversion

---

## 6. 数据需求总结

| 增强项 | 新增数据 | 来源 | 可用性 |
|--------|----------|------|--------|
| ADX | 无（从OHLCV计算） | 日OHLCV | ✅ 已有 |
| 动态阈值 | 无（从VOLFAC计算） | VOLFAC输出 | ✅ 已有 |
| 交易量确认 | 无（从OHLCV提取） | 日OHLCV volume | ✅ 已有 |
| 组合风控 | 行业分类、风格因子 | A5财报/外部数据 | ⚠️ 部分需补充 |
| 均值回归 | 无（基于现有指标） | 现有对象卡 | ✅ 已有 |

**结论**: v1.0 的3项增强全部不需要额外数据，v1.1 的2项增强需要部分补充数据。

---

## 7. 版本与排期建议

| 版本 | 内容 | 预计工作量 | 与现有排期关系 |
|------|------|-----------|---------------|
| v1.0（当前） | 实现ADX、动态阈值、交易量确认 | +2周 | 在 Week 3-4 的"对象卡实现"阶段同步完成 |
| v1.1 | 实现组合风控、均值回归策略包 | +3周 | 在 Week 5-6 的"策略包优化"阶段完成 |
| v1.2 | 机器学习权重优化（DY增强） | +4周 | 在 Week 7-9 的"AI增强"阶段完成 |

---

> 文件：STRATEGY_DESIGN_REFERENCE_v1.0.md
> 生产者：Kimi（基于外部资料+现有架构融合）
> 用途：将外部策略启发转化为可落地的增强方案
> 更新规则：每次新搜索后，评估是否有新的增强项需要补充
> 关联文件：
>   - `EXTERNAL_STRATEGY_RAW_MATERIAL_v1.0.md`（原始资料与想法）
>   - `SYSTEM_ARCHITECTURE_DRAFT.md`（三层架构）
>   - `STRATEGY_BUNDLES_v1.0.md`（策略组合）
>   - `OBJECT_CARD_VOLFAC_P0_A__VolatilityFactor_v1.0.md`（VOLFAC对象卡）
>   - `OBJECT_CARD_TKR7_P0_E__AO_Divergence_v1.0.md`（TKR7对象卡）
>   - `OBJECT_CARD_KD_MTF_P0_E__KD_MultiTimeframe_v1.0.md`（KD_MTF对象卡，如存在）
