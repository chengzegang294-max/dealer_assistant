# VOLTARGET_P0_R — Volatility Targeting（波动率目标）对象卡

> 功能层：P0_R（风控层 — 仓位/止损/回撤）  
> 成熟度：proxy_quantizable_now（只需现有 ATR + Volty 参数）  
> 生产者：Kimi  
> 来源：搜索汇总 + 公开标准定义  
> 状态：已冻结核心字段，待代码实现

---

## 1. 基本定义

Volatility Targeting（波动率目标）是一种动态仓位管理方法：将**投资组合的年化波动率锁定在目标值**（如 10%），当市场波动率升高时自动降低仓位，当市场波动率降低时自动提高仓位。它不是"每笔风险固定比例"，而是"组合风险固定"。

核心洞察：同一个策略，不同仓位可以让 Sharpe 0.8 变成 Sharpe 3 的"灾难"（过满）或 Sharpe 0.2 的"平稳"（过轻）。波动率目标通过动态调整仓位，使组合风险始终处于可控范围。

与 Kelly 的区别：Kelly 根据"胜率/赔率"优化仓位，Vol Targeting 根据"当前波动率"调整仓位。两者互补：Kelly 回答"该下多少"，Vol Targeting 回答"当前环境允许下多少"。

---

## 2. 核心公式（已冻结）

### 2.1 基础公式

```
target_position = target_vol / current_vol × base_position

其中：
  target_vol    = 目标年化波动率（默认 10% = 0.10）
  current_vol   = 当前资产/策略的已实现年化波动率
  base_position = 基准仓位（如 Kelly 计算出的理论仓位，或固定 100%）
```

### 2.2 从 ATR 计算 current_vol（简化版本）

```
current_vol = ATR_14 × sqrt(252) / current_price

其中：
  ATR_14       = 14日平均真实波幅
  sqrt(252)    = 年化系数（一年约 252 个交易日）
  current_price = 当前价格（归一化用）

更精确版本（使用对数收益率）：
current_vol = std(log_return_20) × sqrt(252)

其中：
  log_return_20 = 最近 20 日对数收益率的标准差
```

### 2.3 组合层面（多资产）

```
target_position_i = target_vol / portfolio_vol × base_position_i

其中：
  portfolio_vol = sqrt(w' × Σ × w)
  w            = 各资产权重向量
  Σ            = 协方差矩阵
  base_position_i = 第 i 个资产的基准仓位
```

---

## 3. 字段冻结

### 3.1 输入字段（从现有指标获取）

```text
vt_target_vol         FLOAT   -- 目标年化波动率（默认 0.10 = 10%）
                                     -- 可配置：保守型 = 0.08，激进型 = 0.15
vt_atr14              FLOAT   -- 14日 ATR（从现有 atr_n:14 获取）
vt_current_price      FLOAT   -- 当前价格
vt_log_return_std_20  FLOAT   -- 最近 20 日对数收益率标准差（比 ATR 更精确）
vt_base_position      FLOAT   -- 基准仓位（来自 Kelly 计算或固定策略仓位）
```

### 3.2 计算字段（已冻结）

```text
vt_current_vol        FLOAT   -- 当前已实现年化波动率
                                     -- 简化版：vt_atr14 × sqrt(252) / vt_current_price
                                     -- 精确版：vt_log_return_std_20 × sqrt(252)
vt_vol_ratio          FLOAT   -- 波动率比率 = vt_current_vol / vt_target_vol
                                     -- > 1.0 表示当前波动高于目标（需降仓）
                                     -- < 1.0 表示当前波动低于目标（可加仓）
vt_position_scalar    FLOAT   -- 仓位缩放系数 = 1 / vt_vol_ratio
                                     -- 如果 current_vol = 20%, target = 10% → scalar = 0.5（仓位减半）
                                     -- 如果 current_vol = 5%, target = 10% → scalar = 2.0（仓位翻倍）
                                     -- 上限：vt_position_scalar ≤ 2.0（防止过度加仓）
                                     -- 下限：vt_position_scalar ≥ 0.2（防止过度降仓）
vt_adjusted_position  FLOAT   -- 调整后仓位 = vt_base_position × vt_position_scalar
                                     -- 这是最终执行仓位
vt_vol_regime         ENUM    -- 当前波动率状态：
                                     -- 'low_vol'      = current_vol < 0.5 × target_vol（低波动，可加仓）
                                     -- 'normal_vol'   = 0.5 × target ≤ current ≤ 1.5 × target（正常）
                                     -- 'high_vol'     = 1.5 × target < current ≤ 2.5 × target（高波动，需降仓）
                                     -- 'extreme_vol'  = current > 2.5 × target（极端波动，强制清仓或极低仓位）
```

### 3.3 衰减与平滑字段（已冻结）

```text
vt_vol_ema            FLOAT   -- 波动率的 EMA 平滑（避免突变）
                                     -- 公式：vt_vol_ema_t = α × vt_current_vol + (1-α) × vt_vol_ema_{t-1}
                                     -- α = 2 / (N+1)，N = 10（默认）
vt_scalar_ema         FLOAT   -- 仓位缩放系数的 EMA 平滑（避免频繁调仓）
                                     -- 只有 vt_scalar_ema 变化超过 10% 时才实际调整仓位
vt_last_adjust_date   DATE    -- 上次调整仓位的日期（避免日内频繁调整）
vt_limit_atr_corrector  FLOAT   -- 涨跌停 ATR 修正系数：
                                     -- 当检测到涨停/跌停时，当前 ATR 使用修正值 = 前 20 日非涨跌停日 ATR 均值
                                     -- 防止连续涨跌停压缩 ATR 导致误判低波动
vt_overnight_gap_adj    FLOAT   -- 隔夜跳空调整系数：
                                     -- 集合竞价导致的大幅跳空会扭曲波动率计算
                                     -- 默认 = 1.0（无调整），检测到跳空 > 2×ATR 时降至 0.7
                                     -- 降低目标波动率以应对异常开盘波动
vt_astock_enabled       BOOL    -- A股模式开关（默认 False）
```

---

## 4. 计算逻辑（伪代码）

### 4.1 核心计算

```python
def calculate_vol_targeting(ohlcv_df, base_position=1.0, target_vol=0.10, 
                            atr_period=14, return_window=20, 
                            scalar_max=2.0, scalar_min=0.2,
                            ema_period=10, cooldown_days=5):
    """
    计算波动率目标调整仓位
    
    参数:
        ohlcv_df: DataFrame with [open, high, low, close, volume]
        base_position: 基准仓位（来自 Kelly 或其他策略）
        target_vol: 目标年化波动率（默认 10%）
        atr_period: ATR 计算周期（默认 14，与现有参数一致）
        return_window: 收益率标准差计算窗口（默认 20）
        scalar_max: 仓位缩放上限（默认 2.0x）
        scalar_min: 仓位缩放下限（默认 0.2x = 20%）
        ema_period: EMA 平滑周期（默认 10）
        cooldown_days: 调仓冷却期（默认 5 个交易日）
    
    返回:
        dict with vt_current_vol, vt_position_scalar, vt_adjusted_position, etc.
    """
    current_price = ohlcv_df['close'].iloc[-1]
    
    # 1. 计算 ATR14（简化版波动率）
    high_low = ohlcv_df['high'] - ohlcv_df['low']
    high_close = abs(ohlcv_df['high'] - ohlcv_df['close'].shift())
    low_close = abs(ohlcv_df['low'] - ohlcv_df['close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr14 = tr.rolling(window=atr_period).mean().iloc[-1]
    
    # 2. 计算对数收益率标准差（精确版）
    log_returns = np.log(ohlcv_df['close'] / ohlcv_df['close'].shift(1)).dropna()
    log_return_std_20 = log_returns.tail(return_window).std()
    
    # 3. 计算当前年化波动率（两种方法取更保守的）
    vol_from_atr = atr14 * np.sqrt(252) / current_price
    vol_from_returns = log_return_std_20 * np.sqrt(252)
    vt_current_vol = max(vol_from_atr, vol_from_returns)  # 取保守值
    
    # 4. EMA 平滑（避免单日突变）
    alpha = 2 / (ema_period + 1)
    # 假设前一日 vt_vol_ema 已存储
    vt_vol_ema = alpha * vt_current_vol + (1 - alpha) * prev_vol_ema
    
    # 5. 波动率比率和仓位缩放系数
    vt_vol_ratio = vt_vol_ema / target_vol
    vt_position_scalar = 1.0 / vt_vol_ratio
    
    # 6. 限制缩放系数
    vt_position_scalar = max(scalar_min, min(scalar_max, vt_position_scalar))
    
    # 7. EMA 平滑缩放系数（避免频繁调仓）
    vt_scalar_ema = alpha * vt_position_scalar + (1 - alpha) * prev_scalar_ema
    
    # 8. 冷却期检查
    days_since_last_adjust = (current_date - last_adjust_date).days
    if days_since_last_adjust < cooldown_days:
        # 冷却期内，只有变化超过 10% 才调整
        if abs(vt_scalar_ema - prev_scalar_ema) / prev_scalar_ema < 0.10:
            vt_scalar_ema = prev_scalar_ema  # 保持原仓位
    
    # 9. 调整后仓位
    vt_adjusted_position = base_position * vt_scalar_ema
    
    # 10. 波动率状态判断
    if vt_vol_ema < 0.5 * target_vol:
        vt_vol_regime = 'low_vol'
    elif vt_vol_ema <= 1.5 * target_vol:
        vt_vol_regime = 'normal_vol'
    elif vt_vol_ema <= 2.5 * target_vol:
        vt_vol_regime = 'high_vol'
    else:
        vt_vol_regime = 'extreme_vol'
    
    # 11. 极端波动处理
    if vt_vol_regime == 'extreme_vol':
        vt_adjusted_position = min(vt_adjusted_position, 0.05)  # 强制降至 5% 或以下
        vt_scalar_ema = min(vt_scalar_ema, 0.05 / base_position) if base_position > 0 else 0.0
    
    return {
        'vt_current_vol': round(vt_current_vol, 4),
        'vt_vol_ema': round(vt_vol_ema, 4),
        'vt_vol_ratio': round(vt_vol_ratio, 4),
        'vt_position_scalar': round(vt_position_scalar, 4),
        'vt_scalar_ema': round(vt_scalar_ema, 4),
        'vt_adjusted_position': round(vt_adjusted_position, 4),
        'vt_vol_regime': vt_vol_regime,
    }
```

### 4.2 多资产组合版本

```python
def calculate_portfolio_vol_targeting(positions_df, cov_matrix, target_vol=0.10):
    """
    多资产组合的波动率目标调整
    
    参数:
        positions_df: DataFrame with columns [asset, base_weight, current_price]
        cov_matrix: 协方差矩阵（年化）
        target_vol: 目标年化波动率
    
    返回:
        dict with portfolio_vol, adjusted_weights
    """
    w = positions_df['base_weight'].values
    
    # 1. 组合波动率
    portfolio_vol = np.sqrt(w.T @ cov_matrix @ w)
    
    # 2. 缩放系数
    scalar = target_vol / portfolio_vol
    scalar = max(0.2, min(2.0, scalar))
    
    # 3. 调整后的权重
    adjusted_weights = w * scalar
    
    # 4. 归一化（确保总和 = 1）
    adjusted_weights = adjusted_weights / adjusted_weights.sum()
    
    return {
        'portfolio_vol': round(portfolio_vol, 4),
        'scalar': round(scalar, 4),
        'adjusted_weights': adjusted_weights,
    }
```

---

## 5. 与现有风控层的互锁（已冻结）

### 5.1 与 Kelly Criterion 的融合

```text
融合规则 VOLTARGET × KELLY：

1. 层级关系：
   - Kelly 提供 "理论最优仓位"（基于胜率/赔率）→ kelly_f_actual
   - Vol Targeting 提供 "环境调整系数"（基于当前波动率）→ vt_scalar_ema
   - 最终仓位 = kelly_f_actual × vt_scalar_ema
   - 再与 Van Tharp 上限取 min：final_position = min(kelly_f_actual × vt_scalar_ema, 0.20)

2. 执行流程：
   Step 1: Kelly 计算理论仓位 kelly_f_actual
   Step 2: Vol Targeting 计算环境缩放系数 vt_scalar_ema
   Step 3: 初步仓位 = kelly_f_actual × vt_scalar_ema
   Step 4: 与 Van Tharp 上限取 min → final_position
   Step 5: 与单票上限取 min（A股单票 ≤ 20%）→ final_position

3. 示例：
   - Kelly 算出 f* = 40%，半凯利 = 20%，Van Tharp 上限 = 20% → kelly_f_actual = 20%
   - Vol Targeting 算出 current_vol = 20%，target = 10% → scalar = 0.5
   - 最终仓位 = 20% × 0.5 = 10%
   - 解读：策略质量很好（Kelly 说该下 20%），但市场太波动（Vol Targeting 说只能下 10%）
   
   - Kelly 算出 f* = 20%，半凯利 = 10%，Van Tharp 上限 = 20% → kelly_f_actual = 10%
   - Vol Targeting 算出 current_vol = 5%，target = 10% → scalar = 2.0
   - 最终仓位 = 10% × 2.0 = 20%（但受 Van Tharp 上限限制，仍为 20%）
   - 解读：策略质量一般（Kelly 说只下 10%），但市场很平静（Vol Targeting 说可以翻倍）
```

### 5.2 与 Van Tharp 固定风险的融合

```text
融合规则 VOLTARGET × VAN_THARP：

1. Van Tharp 2% 是"单笔风险上限"（绝对值）。
   Vol Targeting 是"仓位缩放系数"（相对值）。
   
2. 两者的结合方式：
   - Van Tharp 决定"这笔最多亏多少钱"（风险金额）
   - Vol Targeting 决定"在当前波动率下，这笔钱对应多少仓位"
   
   公式：position_size = risk_amount / (stop_distance × unit_price) × vt_scalar_ema
   
   其中：
   - risk_amount = total_capital × 0.02（Van Tharp 2%）
   - stop_distance = 止损距离（如 1.5×ATR）
   - vt_scalar_ema = 波动率缩放系数

3. 示例：
   - 总资金 100万，风险 2% = 2万
   - 止损距离 = 5元（1.5×ATR）
   - 股价 = 100元
   - 基础股数 = 20000 / 5 = 4000 股（价值 40万 = 40% 仓位）
   - 但 Vol Targeting 说当前波动率 2×目标 → scalar = 0.5
   - 调整后股数 = 4000 × 0.5 = 2000 股（价值 20万 = 20% 仓位）
   - 再与 Van Tharp 上限取 min（20%）→ 最终 20% 仓位
```

### 5.3 与 Volty 的互锁

```text
互锁规则 VOLTARGET × VOLTY：

1. Volty 提供"趋势状态"，Vol Targeting 提供"波动率调整"。两者互补：
   - volty_trend_state = 'expansion' → 波动率扩张 → Vol Targeting 自动降仓（scalar < 1.0）
   - volty_trend_state = 'contraction' → 波动率收缩 → Vol Targeting 允许加仓（scalar > 1.0）
   - volty_trend_state = 'trending' → 波动率正常 → scalar ≈ 1.0

2. Volty 的止损位与 Vol Targeting 的协同：
   - 高波动时（volty_stop_distance_atr 增大），即使 scalar 降仓，单笔绝对风险（Van Tharp 2%）仍不变。
   - 这意味着高波动时仓位自动减小，但单笔亏损金额不变（因为止损距离增大）。
   - 低波动时（volty_stop_distance_atr 减小），scalar 允许加仓，单笔绝对风险仍不变。
   - 这意味着低波动时仓位自动增大，但单笔亏损金额不变（因为止损距离减小）。
   - 效果：组合风险始终锁定在目标值，但单笔风险由 Van Tharp 控制。

3. Volty 翻转信号时的处理：
   - volty_flip_signal = 'bullish_flip' → 若 vt_vol_regime = 'high_vol' 或 'extreme_vol' → 维持低仓位（不急于追涨）
   - volty_flip_signal = 'bearish_flip' → 若 vt_vol_regime = 'high_vol' → 立即减仓至 scalar_min（恐慌性降仓）
```

### 5.4 与 KD MTF 的互锁

```text
互锁规则 VOLTARGET × KD MTF：

1. KD MTF 的极端区对 Vol Targeting 的调制：
   - kd_week_extreme_zone = 'overbought' → 即使 vt_vol_regime = 'low_vol'（允许加仓），也强制 scalar 上限为 1.0（不追涨加仓）
   - kd_week_extreme_zone = 'oversold' → 即使 vt_vol_regime = 'high_vol'（需降仓），也允许 scalar 下限为 0.5（不恐慌杀跌）

2. KD MTF 的 alignment 对 Vol Targeting 目标值的调整：
   - kd_alignment_tier = 'strong' → 目标波动率可提升至 1.2×target（策略强，可承受稍高波动）
   - kd_alignment_tier = 'weak' → 目标波动率降至 0.8×target（策略弱，保守为上）
   - kd_alignment_tier = 'conflict' → 目标波动率降至 0.5×target（方向不明，极度保守）
```

---

## 6. 与执行层的互锁（已冻结）

```text
互锁规则 VOLTARGET × EXECUTION：

1. VP 信号与 Vol Targeting 的协同：
   - VP 的 VA_BREAKOUT 信号在 high_vol 环境下 → 即使信号强，vt_scalar 可能 < 0.5 → 实际仓位小
   - VP 的 POC_REVERSION 在 low_vol 环境下 → scalar 可能 > 1.0 → 可稍微加仓（均值回归在平静期更可靠）
   - VP 的 LVN_MOMENTUM 在 extreme_vol 环境下 → 即使信号强，强制 scalar ≤ 0.2 → 极小仓位（动量策略在极端波动中容易反转）

2. CHZL_BSD 与 Vol Targeting：
   - 1Buy（趋势反转）在 high_vol 环境下 → 特别危险（波动大 + 反转不确定性高）→ scalar 强制 ≤ 0.25
   - 3Buy（趋势加速）在 low_vol 环境下 → 可加仓（趋势在平静期加速更可靠）→ scalar 可 = 1.5

3. TK-R6 与 Vol Targeting：
   - R6 = PIERCED（结构破坏）在 extreme_vol 环境下 → 强制清仓（scalar = 0）
   - R6 = TOUCH_BOUNCE 在 low_vol 环境下 → 可标准仓位（scalar = 1.0）
```

---

## 7. 多周期联立（已冻结）

```text
多周期 Vol Targeting 联立：

1. 不同周期使用不同的 target_vol：
   - 日线策略：target_vol = 10%（默认）
   - 周线策略：target_vol = 15%（长线波动更大，目标可放宽）
   - 日内策略：target_vol = 5%（日内波动更小，目标更严格）

2. 多周期约束（取最保守）：
   - 日线 scalar = 0.8，周线 scalar = 1.2 → 取 0.8（日线更保守）
   - 日线 scalar = 1.5，周线 scalar = 0.6 → 取 0.6（周线更保守）
   - 最终 scalar = min(日线scalar, 周线scalar, 日内scalar)

3. 字段化：
   - vt_daily_scalar: 日线波动率缩放系数
   - vt_weekly_scalar: 周线波动率缩放系数
   - vt_intraday_scalar: 日内波动率缩放系数
   - vt_final_scalar: 最终取 min 后的缩放系数
```

---

## 8. 失效模式（已冻结）

```text
VOLTARGET 失效条件：

1. ATR 失真：
   - 连续涨跌停（A股）→ ATR 被压缩到极限（因为 high-low 几乎不变），导致 current_vol 被低估 → scalar 过大 → 危险加仓
   - 应对：加入涨停/跌停检测，limit_up/down 时 ATR 使用前 20 日非涨停日的平均值
   - 一夜情/黑天鹅 → 单根 K 线实体极大，导致 ATR 被高估 → scalar 过小 → 过度降仓
   - 应对：ATR 使用 EMA 平滑，或使用中位数而非均值

2. 对数收益率标准差的计算窗口：
   - return_window = 20 在趋势极强时会低估波动率（因为连续同向运动，标准差小）
   - 应对：使用 GARCH 模型或 Parkinson 波动率（用 high/low 计算，比 close-to-close 更敏感）

3. 调仓过频：
   - 如果 scalar 每天变化，会导致频繁调仓 → 交易成本上升
   - 应对：cooldown_days = 5，且 scalar 变化 < 10% 时不调整

4. 多资产相关性突变：
   - 正常时期资产相关性低，危机时期相关性突然升高 → 组合波动率被低估 → scalar 过大
   - 应对：使用滚动协方差矩阵（如 60 日滚动），或压力测试（模拟相关性 = 1.0 时的组合波动）

5. 目标波动率选择不当：
   - target_vol = 20% 对于 A股小盘可能太低（实际波动 40%+），导致 scalar 常年 < 0.5，仓位过小
   - target_vol = 5% 对于外汇可能太高（实际波动 8%），导致 scalar 常年 > 1.0，接近满仓
   - 应对：target_vol 应根据资产类型和历史波动率调整：
     - A股大盘：target_vol = 10%
     - A股小盘：target_vol = 15-20%
     - 外汇主要货币对：target_vol = 8-10%
     - 币圈：target_vol = 20-30%（或更高）
```

---

## 9. A 股特殊适配（已冻结）

```text
A 股 VOLTARGET 适配规则：

1. 涨停/跌停的 ATR 处理：
   - 检测 limit_up / limit_down 状态
   - 若当日涨停/跌停 → 该日 K 线不用于 ATR 计算（因为 high-low 被价格限制扭曲）
   - 使用前 20 日非涨停/跌停日的 ATR 平均值作为替代

2. T+1 对波动率的影响：
   - T+1 导致"隔夜风险"无法当日处理 → 实际波动率比计算值更高
   - 应对：A 股 target_vol 在基础值上增加 2-3%（如 10% → 12-13%）
   - 或：对数收益率使用"开盘价到次日开盘价"而非"收盘价到收盘价"（捕捉隔夜跳空）

3. 集合竞价跳空：
   - A 股集合竞价（9:15-9:25）常产生大幅跳空 → 开盘 ATR 被跳空主导
   - 应对：使用"盘中 ATR"（排除开盘第一根 5min K 线）或调整 ATR 计算方式

4. 散户行为导致的波动率特征：
   - A 股散户在整数关口（10, 20, 30...）大量交易 → 波动率在这些关口被"人为放大"
   - 应对：波动率计算时，对整数关口的 K 线进行降权（如乘以 0.8）

5. 单票 vs 组合：
   - A 股建议以"组合"为单位做 Vol Targeting（多资产），而非单票
   - 因为单票受个股事件影响大，波动率不稳定
   - 组合波动率更稳定，Vol Targeting 效果更好
```

---

## 10. 成熟度与数据需求

| 维度 | 评估 |
|------|------|
| **所需数据** | OHLCV（已有）+ 现有 ATR14 参数 |
| **计算复杂度** | 中（需要协方差矩阵/EMA 平滑） |
| **实时性能** | 每交易日更新一次，不影响实时性能 |
| **回测可行性** | 高（历史 OHLCV 即可） |
| **A 股落地** | 可直接落地（需处理涨停/跌停 ATR 失真） |
| **外汇/期货/币圈落地** | 直接可用（币圈需提高 target_vol） |
| **跨资产** | 支持（需协方差矩阵版本） |

---

## 11. 与 Kelly 的对比总结

| 维度 | Kelly Criterion | Volatility Targeting |
|------|-----------------|---------------------|
| **核心问题** | "该下多少注？" | "当前环境允许下多少？" |
| **输入** | 胜率 p、赔率 b | 当前波动率、目标波动率 |
| **输出** | 理论最优仓位比例 | 环境调整系数 |
| **哲学** | 长期复利最大化 | 组合风险恒定 |
| **风险** | 参数估计误差 | 波动率预测误差 |
| **与现有参数关系** | 需要 backtest_p0.py 历史日志 | 需要现有 atr_n:14 + volty_trend_state |
| **建议用法** | 两者融合：final = Kelly × VolTarget × VanTharp |

---

> 文件：OBJECT_CARD_VOLTARGET_P0_R__VolatilityTargeting_v1.0.md  
> 生产者：Kimi  
> 状态：字段已冻结，待代码实现
