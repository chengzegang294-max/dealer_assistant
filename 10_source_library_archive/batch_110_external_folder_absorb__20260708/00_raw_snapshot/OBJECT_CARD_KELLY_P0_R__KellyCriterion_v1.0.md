# KELLY_P0_R — Kelly Criterion（凯利公式）对象卡

> 功能层：P0_R（风控层 — 仓位/止损/回撤）  
> 成熟度：proxy_quantizable_now（需要历史交易日志，但 backtest_p0.py 可产出）  
> 生产者：Kimi  
> 来源：搜索汇总 + 公开标准定义  
> 状态：已冻结核心字段，待代码实现

---

## 1. 基本定义

Kelly Criterion（凯利公式）由 John Kelly 1956 年为香农通信理论推导，后被 Ed Thorp 用于 21 点和权证套利。它是"在已知胜率 p 和赔率 b 的情况下，计算每次下注的最优资金比例，使得长期资本几何增长率最大化"的数学公式。

核心洞察：选对方向只给你期望值，选对仓位才给你复利。专业投资者把 70% 精力放在风险预算，30% 在方向。

---

## 2. 核心公式与变体（已冻结）

### 2.1 经典二元下注版本（离散）

```
f* = (bp - q) / b = p - q/b

其中：
  f* = 每次应投入的资金比例（0 ≤ f* ≤ 1）
  p  = 胜率（盈利概率）
  q  = 1 - p（败率）
  b  = 赔率（净盈利 / 净亏损，即盈亏比）
```

**示例**：p=60%, b=1（盈亏比 1:1）→ f* = 0.6 - 0.4/1 = **20%**

### 2.2 金融资产版本（连续）

```
f* = (μ - r) / σ²

其中：
  μ  = 资产预期超额收益率
  r  = 无风险利率
  σ² = 资产方差（波动率平方）
```

这是 Merton 1969 推导的版本。对持续分布的资产，最优仓位 = 超额夏普的直接反映。  
深层联系：**Sharpe² = 2 × Kelly 的几何增长率**。

### 2.3 多资产版本（Generalized Kelly）

```
f* = Σ⁻¹ × (μ - r·1)

其中：
  Σ  = 协方差矩阵
  μ  = 收益向量
  r  = 无风险利率
  1  = 全1向量
```

本质就是 Markowitz 切线组合 × 风险偏好参数。多资产时必须考虑协方差，不能对每个资产独立用 Kelly。

---

## 3. 字段冻结

### 3.1 输入字段（从回测/历史交易提取）

```text
kelly_p                 FLOAT   -- 胜率：历史同类型交易中盈利笔数 / 总笔数
                                     -- 要求样本量 ≥ 50 笔（统计学显著性）
                                     -- 若样本不足，标记为 'estimation_low_confidence'
kelly_b                 FLOAT   -- 赔率（盈亏比）：平均盈利幅度 / 平均亏损幅度
                                     -- 修正后：扣除交易成本（佣金 + 印花税）
kelly_q                 FLOAT   -- 败率：1 - kelly_p
kelly_w                 FLOAT   -- 平均盈利金额（绝对值）
kelly_l                 FLOAT   -- 平均亏损金额（绝对值）
kelly_cost_rate         FLOAT   -- 交易成本率（佣金 + 印花税 + 滑点），默认 A股 = 0.0015（千1.5）
kelly_sample_size       INT     -- 历史样本量（用于 confidence 评估）
kelly_t1_penalty_factor    FLOAT   -- A股 T+1 惩罚系数（默认 0.8）：
                                     -- 当日买入无法卖出，实际风险 > 计算风险，仓位额外 × 0.8
kelly_limit_freeze_flag    BOOL    -- 涨跌停冻结标记：
                                     -- True = 当前价格处于涨跌停状态，禁止新仓位计算
                                     -- 由 AStock_LimitFilter 自动设置
kelly_astock_enabled       BOOL    -- A股模式开关（默认 False）：
                                     -- True 时启用所有 A 股适配规则（T+1/涨跌停/成本修正）
                                     -- False 时保持外汇/期货原始逻辑
```

### 3.2 计算字段（已冻结）

```text
kelly_f_star            FLOAT   -- 理论最优仓位比例（Kelly 原始输出）
                                     -- 公式：f* = (kelly_p × kelly_b - kelly_q) / kelly_b
                                     -- 若 f* ≤ 0 → 期望值为负，禁止交易
kelly_f_half            FLOAT   -- 半凯利（Half-Kelly）：0.5 × kelly_f_star
                                     -- 推荐默认值。平滑资产曲线，降低回撤
kelly_f_quarter         FLOAT   -- 四分之一凯利（Quarter-Kelly）：0.25 × kelly_f_star
                                     -- 用于高波动资产（A股小盘、币圈）或参数不确定性高时
kelly_f_actual          FLOAT   -- 实际执行仓位比例
                                     -- 规则：min(kelly_f_half, 0.20, 0.10) 取最保守
                                     -- 0.20 是 Van Tharp 硬性上限（allow2_risk_mult）
                                     -- 0.10 是极端保守上限（A股小盘或币圈）
kelly_risk_budget       FLOAT   -- 最终风险预算（= 总资金 × kelly_f_actual）
                                     -- 这是实际用于单笔交易的资金量
```

### 3.3 动态调整字段（已冻结）

```text
kelly_regime            ENUM    -- 当前 Kelly 计算所处的市场状态：
                                     -- 'normal'      = 正常波动，使用半凯利
                                     -- 'high_vol'    = 高波动（ATR > 2×均值），使用四分之一凯利
                                     -- 'low_vol'     = 低波动（ATR < 0.5×均值），可考虑全凯利（但需人工审核）
                                     -- 'crisis'      = 危机模式（连续3笔亏损），强制使用四分之一凯利
                                     -- 'recovery'    = 恢复期（连续3笔盈利），维持半凯利（不激进加仓）
kelly_adaptive_factor   FLOAT   -- 自适应调整系数（0.25 - 1.0）
                                     -- 默认 = 0.5（半凯利）
                                     -- 高波动时 = 0.25（四分之一凯利）
                                     -- 低波动且高 confidence 时 = 0.75（三分之二凯利）
kelly_confidence_score  INT(0-10) -- 参数估计 confidence：
                                     -- 样本量 ≥ 100，近期数据，p 和 b 稳定 → 10
                                     -- 样本量 50-99，数据较旧，p 或 b 波动 → 5-7
                                     -- 样本量 < 50，或参数近期大幅变化 → 0-3
                                     -- confidence < 5 时，强制使用四分之一凯利
```

---

## 4. 计算逻辑（伪代码）

### 4.1 核心计算

```python
def calculate_kelly(trade_history_df, cost_rate=0.0015, confidence_threshold=5):
    """
    计算 Kelly 最优仓位
    
    参数:
        trade_history_df: DataFrame with columns [pnl, entry_price, exit_price, direction]
                          至少 50 笔同类型交易
        cost_rate: 交易成本率（默认 A股千1.5）
        confidence_threshold: confidence 阈值，低于此强制使用四分之一凯利
    
    返回:
        dict with kelly_f_star, kelly_f_half, kelly_f_quarter, kelly_f_actual, etc.
    """
    # 1. 样本量检查
    n = len(trade_history_df)
    if n < 30:
        return {'error': 'sample_size_insufficient', 'kelly_f_actual': 0.0}
    
    # 2. 计算原始盈亏
    profits = trade_history_df[trade_history_df['pnl'] > 0]['pnl']
    losses = trade_history_df[trade_history_df['pnl'] < 0]['pnl'].abs()
    
    # 3. 修正交易成本
    # 假设每笔交易成本 = (entry_price + exit_price) × volume × cost_rate
    # 简化：从每笔盈亏中扣除平均成本
    avg_trade_value = (trade_history_df['entry_price'] * trade_history_df.get('volume', 1)).mean()
    cost_per_trade = avg_trade_value * cost_rate
    
    adjusted_profits = profits - cost_per_trade
    adjusted_losses = losses + cost_per_trade  # 亏损时成本增加亏损
    
    # 4. 计算胜率 p 和赔率 b
    kelly_p = len(profits) / n
    kelly_q = 1 - kelly_p
    kelly_w = adjusted_profits.mean() if len(adjusted_profits) > 0 else 0
    kelly_l = adjusted_losses.mean() if len(adjusted_losses) > 0 else 0.001  # 避免除零
    kelly_b = kelly_w / kelly_l
    
    # 5. 计算 Kelly f*
    if kelly_b <= 0 or kelly_p * kelly_b <= kelly_q:
        kelly_f_star = 0.0  # 期望值为负，不交易
    else:
        kelly_f_star = (kelly_p * kelly_b - kelly_q) / kelly_b
    
    # 6. 半凯利和四分之一凯利
    kelly_f_half = 0.5 * kelly_f_star
    kelly_f_quarter = 0.25 * kelly_f_star
    
    # 7. Confidence 评估
    if n >= 100:
        base_confidence = 10
    elif n >= 50:
        base_confidence = 7
    else:
        base_confidence = 3
    
    # 参数稳定性：近期 p 和 b 的标准差
    recent_20 = trade_history_df.tail(20)
    recent_p = len(recent_20[recent_20['pnl'] > 0]) / len(recent_20)
    recent_b = (recent_20[recent_20['pnl'] > 0]['pnl'].mean() / 
                recent_20[recent_20['pnl'] < 0]['pnl'].abs().mean()) if len(recent_20) > 0 else kelly_b
    
    p_stability = 1 - abs(kelly_p - recent_p) / max(kelly_p, 0.01)
    b_stability = 1 - abs(kelly_b - recent_b) / max(kelly_b, 0.01)
    kelly_confidence_score = int(base_confidence * min(p_stability, b_stability, 1.0))
    
    # 8. 自适应因子
    if kelly_confidence_score < confidence_threshold:
        kelly_adaptive_factor = 0.25  # 低 confidence → 四分之一凯利
    else:
        kelly_adaptive_factor = 0.5   # 正常 → 半凯利
    
    # 9. 实际执行仓位（最保守原则）
    # 与现有 Van Tharp 2% 上限的融合
    van_tharp_max = 0.20  # allow2_risk_mult
    
    kelly_f_actual = min(
        kelly_f_star * kelly_adaptive_factor,  # 自适应凯利
        van_tharp_max,                          # Van Tharp 硬性上限
        0.10 if kelly_confidence_score < 5 else 1.0  # 极端保守上限
    )
    
    # 10. 风险预算（假设总资金 = 1.0）
    kelly_risk_budget = kelly_f_actual
    
    return {
        'kelly_p': round(kelly_p, 4),
        'kelly_b': round(kelly_b, 4),
        'kelly_q': round(kelly_q, 4),
        'kelly_w': round(kelly_w, 4),
        'kelly_l': round(kelly_l, 4),
        'kelly_f_star': round(kelly_f_star, 4),
        'kelly_f_half': round(kelly_f_half, 4),
        'kelly_f_quarter': round(kelly_f_quarter, 4),
        'kelly_f_actual': round(kelly_f_actual, 4),
        'kelly_risk_budget': round(kelly_risk_budget, 4),
        'kelly_confidence_score': kelly_confidence_score,
        'kelly_adaptive_factor': kelly_adaptive_factor,
        'kelly_sample_size': n,
    }
```

### 4.2 动态更新逻辑（每 N 笔交易后重算）

```python
def update_kelly_after_trade(trade_result, kelly_state, update_interval=20):
    """
    每笔交易后更新 Kelly 状态
    
    参数:
        trade_result: dict with {pnl, entry_price, exit_price, direction, timestamp}
        kelly_state: 当前 Kelly 计算结果（字典）
        update_interval: 每 N 笔交易后重算 Kelly（默认 20）
    
    返回:
        更新后的 kelly_state
    """
    # 1. 追加到交易历史
    trade_history.append(trade_result)
    
    # 2. 检查是否需要重算
    if len(trade_history) % update_interval == 0 or len(trade_history) < 30:
        new_kelly = calculate_kelly(trade_history)
        kelly_state.update(new_kelly)
    
    # 3. 连续亏损/盈利检测（用于 regime 判断）
    recent_5 = trade_history[-5:]
    consecutive_losses = sum(1 for t in recent_5 if t['pnl'] < 0)
    consecutive_wins = sum(1 for t in recent_5 if t['pnl'] > 0)
    
    if consecutive_losses >= 3:
        kelly_state['kelly_regime'] = 'crisis'
        kelly_state['kelly_adaptive_factor'] = 0.25
    elif consecutive_wins >= 3 and kelly_state['kelly_regime'] == 'crisis':
        kelly_state['kelly_regime'] = 'recovery'
        kelly_state['kelly_adaptive_factor'] = 0.5  # 恢复但不激进
    elif kelly_state['kelly_regime'] == 'recovery' and consecutive_losses == 0:
        kelly_state['kelly_regime'] = 'normal'
    
    # 4. 高波动检测（从 Volty 获取）
    if volty_trend_state == 'expansion':
        kelly_state['kelly_regime'] = 'high_vol'
        kelly_state['kelly_adaptive_factor'] = min(kelly_state['kelly_adaptive_factor'], 0.25)
    
    # 5. 重新计算 kelly_f_actual（因为 regime 可能改变）
    kelly_state['kelly_f_actual'] = min(
        kelly_state['kelly_f_star'] * kelly_state['kelly_adaptive_factor'],
        0.20,  # Van Tharp 上限
        0.10 if kelly_state['kelly_confidence_score'] < 5 else 1.0
    )
    kelly_state['kelly_risk_budget'] = kelly_state['kelly_f_actual']
    
    return kelly_state
```

---

## 5. 与现有风控层的互锁（已冻结）

### 5.1 与 Van Tharp 固定风险（allow2_risk_mult: 0.20）的融合

```text
融合规则 KELLY × VAN_THARP：

1. 层级关系：
   - Van Tharp 2% 是"硬性上限"（ceiling）。无论 Kelly 算出多少，单笔风险不超过 2%。
   - Kelly 是"动态优化层"（optimizer）。在 Van Tharp 上限内，根据胜率和赔率优化仓位。

2. 执行公式：
   kelly_f_actual = min(kelly_f_star × kelly_adaptive_factor, van_tharp_max, extreme_conservative_max)
   
   其中：
   - van_tharp_max = 0.20
   - extreme_conservative_max = 0.10（当 confidence < 5 或 crisis 模式时）

3. 决策流程：
   Step 1: 计算 Kelly f*（理论最优）
   Step 2: 根据 regime 和 confidence 选择 adaptive_factor（0.25, 0.5, 0.75）
   Step 3: 与 Van Tharp 上限取 min → kelly_f_actual
   Step 4: 计算 kelly_risk_budget = total_capital × kelly_f_actual
   Step 5: 与单笔止损位结合，计算实际股数/手数：
           position_size = kelly_risk_budget / (stop_distance × unit_price)
```

### 5.2 与 Volty 的互锁

```text
互锁规则 KELLY × VOLTY：

1. 波动率对 Kelly 的调节：
   - volty_trend_state = 'expansion' → kelly_regime = 'high_vol', adaptive_factor = 0.25
   - volty_trend_state = 'contraction' → kelly_regime = 'normal', adaptive_factor = 0.5（或 0.75）
   - volty_trend_state = 'trending' → kelly_regime = 'normal', adaptive_factor = 0.5

2. ATR 对止损距离的影响：
   - volty_stop_distance_atr 影响单笔止损距离
   - 止损距离越大 → 同样 risk_budget 下的 position_size 越小（自动降仓）
   - 这与 Kelly 的波动率调节形成"双重保护"

3. Volty 翻转信号时的 Kelly 处理：
   - volty_flip_signal = 'bullish_flip' → 若 kelly_f_actual > 0 → 维持仓位
   - volty_flip_signal = 'bearish_flip' → 若 kelly_f_actual > 0 → 考虑减仓至 kelly_f_quarter 或清仓
```

### 5.3 与 KD MTF 的互锁

```text
互锁规则 KELLY × KD MTF：

1. KD MTF 对齐层级对 Kelly confidence 的影响：
   - kd_alignment_tier = 'strong' → kelly_confidence_score +1（方向一致性增加信心）
   - kd_alignment_tier = 'conflict' → kelly_confidence_score -2（方向冲突，降低信心）
   - kd_week_extreme_zone = 'overbought' → 做多时 kelly_f_actual × 0.5（极端区降仓）
   - kd_week_extreme_zone = 'oversold' → 做空时 kelly_f_actual × 0.5

2. KD MTF 的 lock_signal 与 Kelly 的协同：
   - lock_signal = 'locked'（强锁）→ Kelly 可正常计算仓位（方向确定）
   - lock_signal = 'unlocked'（未锁）→ kelly_f_actual 强制降至 0.05（方向不明，极小仓位试探）
   - lock_signal = 'conflicting'（冲突）→ kelly_f_actual = 0（禁止交易）
```

### 5.4 与执行层的互锁（VP / BSD / TK）

```text
互锁规则 KELLY × EXECUTION：

1. VP 信号强度对 Kelly 的调制：
   - vp_signal_strength ≥ 8 → kelly_f_actual 可提升至 min(kelly_f_half, 0.20)
   - vp_signal_strength 5-7 → kelly_f_actual 维持默认（kelly_f_quarter 或半凯利）
   - vp_signal_strength < 5 → kelly_f_actual 降至 0.05（弱信号，极小仓位）

2. CHZL_BSD 类型对 Kelly 的调制：
   - 1Buy（一买）→ 最保守，kelly_f_actual = kelly_f_quarter（趋势反转早期，不确定性高）
   - 2Buy（二买）→ 正常，kelly_f_actual = kelly_f_half（趋势确认，标准仓位）
   - 3Buy（三买）→ 可激进，kelly_f_actual = min(kelly_f_half × 1.2, 0.20)（趋势加速，但不超过上限）

3. TK-R6 状态对 Kelly 的调制：
   - R6 = TOUCH_BOUNCE → 回撤浅，kelly_f_actual = kelly_f_half
   - R6 = SHALLOW_RETR → 回撤 0.236-0.382，kelly_f_actual = kelly_f_half
   - R6 = DEEP_RETR → 回撤 0.382-0.618，kelly_f_actual = kelly_f_quarter（深度回撤，不确定性高）
   - R6 = PIERCED → 回撤突破 0.618，kelly_f_actual = 0.05（结构被破坏，极小仓位）
   - R6 = REJECTED → 回撤被强烈拒绝，kelly_f_actual = 0（禁止入场）
```

---

## 6. 失效模式（已冻结）

```text
KELLY 失效条件：

1. 样本不足：
   - kelly_sample_size < 30 → 参数估计不可靠，kelly_f_actual 强制为 0
   - 30 ≤ kelly_sample_size < 50 → kelly_f_actual = kelly_f_quarter（最保守）
   - 建议：新策略上线前，先用模拟盘/小仓位积累至少 50 笔样本

2. 参数估计误差：
   - 若实际胜率比估计低 10%（如估计 60% 实际 50%），Kelly 会从 20% 升至 40% → 严重过度交易
   - 应对：定期（每 20 笔）重算 Kelly，并做压力测试（模拟 p-10%, b-20% 后的仓位）

3. 连续亏损后的"赌徒谬误"：
   - 连续亏损 5 笔后，人性倾向是"下把一定赢"，从而 Kelly 计算出的仓位反而增大
   - 应对：连续亏损 3 笔 → kelly_regime = 'crisis' → 强制使用四分之一凯利，无论公式算出什么

4. 黑天鹅事件：
   - Kelly 假设"概率分布稳定"，但黑天鹅会改变分布
   - 应对：总仓位上限（如 50% 资金在市场中），即使 Kelly 算出 80% 也不超过 50%

5. 多资产相关性的忽略：
   - 独立对每个资产用 Kelly → 忽略相关性 → 组合风险被低估
   - 应对：多资产时必须使用 Generalized Kelly（协方差矩阵版本），或简单规则：
     - 若持仓中已有 3 只以上相关性 > 0.7 的资产 → 每只仓位额外 × 0.7
```

---

## 7. A 股特殊适配（已冻结）

```text
A 股 KELLY 适配规则：

1. 交易成本修正：
   - A 股成本 = 佣金（万分之2.5-3）+ 印花税（卖出千1）+ 过户费 + 滑点
   - 单边成本约 0.15%，双边成本约 0.25%
   - kelly_cost_rate = 0.0025（默认）
   - 若使用融券 → 额外加融券利息（约 8-10% 年化）

2. T+1 对仓位的影响：
   - 当日买入后无法卖出，因此 Kelly 的"单笔交易"在 A 股实际上是"T+1 持有"。
   - 这意味着 A 股的 kelly_f_actual 应该比外汇更保守（因为无法及时止损）。
   - 建议：A 股 kelly_f_actual 在基础值上再 × 0.8（T+1 惩罚系数）

3. 涨跌停限制：
   - limit_up / limit_down 时，kelly_f_actual = 0（禁止新入场）
   - 因为无法止损，任何仓位在涨跌停日都是"不可控风险"

4. 单票仓位上限：
   - A 股建议单票不超过总资金的 20%（即使 Kelly 算出更高）
   - 若 Kelly 算出 > 20% → 取 min(kelly_f_actual, 0.20)
   - 分散持仓：至少 3-5 只，降低单票黑天鹅风险

5. 半凯利推荐：
   - A 股散户强烈建议始终使用半凯利或四分之一凯利
   - 因为 A 股散户的参数估计误差更大（情绪化交易导致历史胜率不具代表性）
```

---

## 8. 成熟度与数据需求

| 维度 | 评估 |
|------|------|
| **所需数据** | 历史交易日志（backtest_p0.py 可产出） |
| **计算复杂度** | 低（简单统计） |
| **实时性能** | 每 N 笔交易更新一次，不影响实时性能 |
| **回测可行性** | 高（但需要至少 50 笔历史交易） |
| **A 股落地** | 可直接落地（需修正交易成本 + T+1 惩罚） |
| **外汇/期货/币圈落地** | 直接可用（交易成本不同，需调整 cost_rate） |
| **跨资产** | 支持（需协方差矩阵版本） |

---

> 文件：OBJECT_CARD_KELLY_P0_R__KellyCriterion_v1.0.md  
> 生产者：Kimi  
> 状态：字段已冻结，待代码实现
