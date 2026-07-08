# TKR7_P0_E — TK-R7 AO 背离（Awesome Oscillator Divergence）对象卡

> 功能层：P0_E（执行层 — 入场/出场/执行质量）  
> 成熟度：proxy_quantizable_now（只需 OHLCV，AO 为标准指标）  
> 生产者：Kimi  
> 来源：GLM_DELIVERY_07 蓝图 + TK 外汇对象卡 + Bill Williams AO 标准定义  
> 状态：已冻结核心字段，待代码实现

---

## 1. 基本定义

Awesome Oscillator（AO，卓越振荡器）由 Bill Williams 设计，计算公式为：
```
AO = SMA(中位数价格, 5) - SMA(中位数价格, 34)
中位数价格 = (High + Low) / 2
```

AO 背离是指：AO 柱体的高度/方向与价格走势出现**不一致**，预示趋势可能反转（常规背离）或延续（隐藏背离）。

**TK-R7 的定位**：AO 背离不是独立入场信号，而是**过滤器/确认器**。它用于：
- 在 KD MTF 极端区确认反转可能性（常规背离）
- 在趋势中确认回调后的延续（隐藏背离）
- 在缠论 BSD 1Buy/1Sell 时提供额外验证

---

## 2. 核心概念与字段冻结

### 2.1 基础字段（已冻结）

```text
ao_value            FLOAT   -- 当前 AO 值（5期 SMA - 34期 SMA 的中位数价格）
ao_prev_value       FLOAT   -- 前一根 K 线的 AO 值（用于判断柱体方向变化）
ao_histogram[]      ARRAY<FLOAT>   -- 最近 N 根 K 线的 AO 值序列（用于峰值检测）
price_high          FLOAT   -- 当前 K 线最高价
price_low           FLOAT   -- 当前 K 线最低价
price_close         FLOAT   -- 当前 K 线收盘价
price_peak_high     FLOAT   -- 最近 N 根 K 线的价格最高峰值
price_peak_low      FLOAT   -- 最近 N 根 K 线的价格最低峰值
price_peak_high_idx INT     -- 价格最高峰值对应的 K 线索引
price_peak_low_idx  INT     -- 价格最低峰值对应的 K 线索引
```

### 2.2 派生字段（已冻结）

```text
ao_peak_high        FLOAT   -- AO 序列中的最高峰值（仅取正柱体）
ao_peak_low         FLOAT   -- AO 序列中的最低峰值（仅取负柱体）
ao_peak_high_idx    INT     -- AO 最高峰值对应的 K 线索引
ao_peak_low_idx     INT     -- AO 最低峰值对应的 K 线索引
ao_direction        ENUM    -- 当前 AO 柱体方向：'positive'（零轴上）/ 'negative'（零轴下）/ 'crossing_up' / 'crossing_down'
ao_trend            ENUM    -- AO 整体趋势：'rising'（柱体上升）/ 'falling'（柱体下降）/ 'oscillating'（震荡）
```

### 2.3 背离识别字段（已冻结）

```text
ao_divergence_type  ENUM    -- 背离类型：
                              -- 'NONE'              = 无背离
                              -- 'REGULAR_BULL'      = 常规底背离（价格创新低，AO 未创新低）
                              -- 'REGULAR_BEAR'      = 常规顶背离（价格创新高，AO 未创新高）
                              -- 'HIDDEN_BULL'       = 隐藏底背离（价格回调但未破前低，AO 上升）
                              -- 'HIDDEN_BEAR'       = 隐藏顶背离（价格回调但未破前高，AO 下降）
                              -- 'EXTENDED_BULL'     = 扩展底背离（连续多底，AO 逐级抬升）
                              -- 'EXTENDED_BEAR'     = 扩展顶背离（连续多顶，AO 逐级下降）
ao_divergence_strength  FLOAT   -- 背离强度（0.0-1.0）：
                                  -- 价格峰值差 / AO 峰值差的比率，标准化到 0-1
                                  -- 越接近 1.0 表示背离越显著
ao_peak_diff        FLOAT   -- 价格峰值与 AO 峰值的差值比例：
                              -- = (price_peak - price_prev_peak) / (ao_peak - ao_prev_peak)
                              -- 负值表示背离（价格上升但 AO 下降）
ao_divergence_confidence  FLOAT   -- 背离置信度（0.0-1.0）：
                                      -- 基于：峰值清晰度 + 柱体方向一致性 + 时间跨度合理性
                                      -- confidence < 0.60 的背离标记为 "weak"，不生成信号
ao_divergence_age   INT     -- 背离已持续多少根 K 线（用于判断时效性）
                              -- age > 8 的背离视为 "过期"，需要重新确认
```

### 2.4 信号字段（已冻结）

```text
ao_signal_type      ENUM    -- AO 信号类型：
                              -- 'NONE'                    = 无信号
                              -- 'REGULAR_BULL_CONFIRM'    = 常规底背离确认（看多过滤器）
                              -- 'REGULAR_BEAR_CONFIRM'    = 常规顶背离确认（看空过滤器）
                              -- 'HIDDEN_BULL_CONFIRM'     = 隐藏底背离确认（趋势延续看多）
                              -- 'HIDDEN_BEAR_CONFIRM'     = 隐藏顶背离确认（趋势延续看空）
                              -- 'FORCE_EXIT_LONG'         = 强制平多（极端区 + 顶背离）
                              -- 'FORCE_EXIT_SHORT'        = 强制平空（极端区 + 底背离）
ao_signal_strength  INT(0-10)   -- 信号强度：
                                  -- 常规背离 + KD 极端区 + Volty 趋势 = 10
                                  -- 隐藏背离 + 趋势确认 = 6-7
                                  -- 单独背离无其他确认 = 3-4
ao_recommendation   ENUM    -- 操作建议：
                              -- 'HOLD'        = 持仓不变
                              -- 'REDUCE_LONG' = 减仓做多（顶背离警告）
                              -- 'REDUCE_SHORT'= 减仓做空（底背离警告）
                              -- 'CLOSE_LONG'  = 平多（强制退出）
                              -- 'CLOSE_SHORT' = 平空（强制退出）
                              -- 'STANDBY'     = 观望（背离刚出现，等待确认）
```

---

## 3. 计算逻辑（伪代码）

### 3.1 AO 计算

```python
def calculate_ao(ohlcv_df):
    """
    计算 Awesome Oscillator
    
    参数:
        ohlcv_df: DataFrame with [high, low, close]
    
    返回:
        Series with AO values
    """
    # 1. 中位数价格
    median_price = (ohlcv_df['high'] + ohlcv_df['low']) / 2.0
    
    # 2. 5期 SMA 和 34期 SMA
    sma_5 = median_price.rolling(window=5).mean()
    sma_34 = median_price.rolling(window=34).mean()
    
    # 3. AO = 5期 SMA - 34期 SMA
    ao = sma_5 - sma_34
    
    return ao
```

### 3.2 峰值检测

```python
def detect_peaks(series, min_distance=3, prominence_threshold=0.1):
    """
    检测序列中的局部峰值
    
    参数:
        series: 输入序列（AO 或价格）
        min_distance: 峰值之间的最小距离（K 线数）
        prominence_threshold: 最小突出度（相对值）
    
    返回:
        list of {index, value, type}，type = 'peak'/'valley'
    """
    peaks = []
    
    for i in range(min_distance, len(series) - min_distance):
        # 检测峰值（局部最大值）
        if series.iloc[i] > series.iloc[i-1] and series.iloc[i] > series.iloc[i+1]:
            # 检查突出度
            left_min = min(series.iloc[max(0, i-min_distance):i])
            right_min = min(series.iloc[i+1:min(len(series), i+min_distance+1)])
            prominence = series.iloc[i] - min(left_min, right_min)
            
            if prominence > prominence_threshold:
                peaks.append({'index': i, 'value': series.iloc[i], 'type': 'peak'})
        
        # 检测谷值（局部最小值）
        elif series.iloc[i] < series.iloc[i-1] and series.iloc[i] < series.iloc[i+1]:
            left_max = max(series.iloc[max(0, i-min_distance):i])
            right_max = max(series.iloc[i+1:min(len(series), i+min_distance+1)])
            prominence = max(left_max, right_max) - series.iloc[i]
            
            if prominence > prominence_threshold:
                peaks.append({'index': i, 'value': series.iloc[i], 'type': 'valley'})
    
    return peaks
```

### 3.3 背离识别（核心）

```python
def identify_ao_divergence(ohlcv_df, ao_series, lookback=20):
    """
    识别 AO 背离
    
    参数:
        ohlcv_df: DataFrame with [high, low, close]
        ao_series: AO 值序列
        lookback: 回溯窗口（默认 20 根 K 线）
    
    返回:
        dict with divergence_type, strength, confidence, etc.
    """
    # 1. 检测价格峰值和 AO 峰值
    price_highs = detect_peaks(ohlcv_df['high'], min_distance=3)
    price_lows = detect_peaks(ohlcv_df['low'], min_distance=3)
    ao_peaks = detect_peaks(ao_series, min_distance=3)
    ao_valleys = detect_peaks(-ao_series, min_distance=3)  # 检测负值中的峰值
    
    # 2. 取最近两个峰值进行比较
    if len(price_highs) < 2 or len(ao_peaks) < 2:
        return {'ao_divergence_type': 'NONE', 'ao_divergence_confidence': 0.0}
    
    recent_price_highs = price_highs[-2:]
    recent_ao_peaks = ao_peaks[-2:]
    recent_price_lows = price_lows[-2:]
    recent_ao_valleys = ao_valleys[-2:]
    
    # 3. 常规顶背离（价格创新高，AO 未创新高）
    regular_bear = False
    if recent_price_highs[1]['value'] > recent_price_highs[0]['value']:
        if recent_ao_peaks[1]['value'] < recent_ao_peaks[0]['value']:
            regular_bear = True
    
    # 4. 常规底背离（价格创新低，AO 未创新低）
    regular_bull = False
    if recent_price_lows[1]['value'] < recent_price_lows[0]['value']:
        if recent_ao_valleys[1]['value'] < recent_ao_valleys[0]['value']:
            # 注意：AO 谷值是负值，"未创新低"意味着绝对值更小（即更接近零）
            if recent_ao_valleys[1]['value'] > recent_ao_valleys[0]['value']:
                regular_bull = True
    
    # 5. 隐藏顶背离（价格回调未破前高，AO 下降）
    hidden_bear = False
    # 需要趋势上下文：价格处于上升趋势中，回调后未创新高
    
    # 6. 隐藏底背离（价格回调未破前低，AO 上升）
    hidden_bull = False
    # 需要趋势上下文：价格处于下降趋势中，反弹后未创新低
    
    # 7. 计算背离强度
    if regular_bear:
        price_diff = recent_price_highs[1]['value'] - recent_price_highs[0]['value']
        ao_diff = recent_ao_peaks[0]['value'] - recent_ao_peaks[1]['value']  # AO 下降差
        ao_divergence_strength = min(1.0, (ao_diff / abs(price_diff)) * 10)
        
        return {
            'ao_divergence_type': 'REGULAR_BEAR',
            'ao_divergence_strength': round(ao_divergence_strength, 2),
            'ao_peak_diff': round((price_diff - ao_diff) / price_diff, 4) if price_diff != 0 else 0,
            'ao_divergence_confidence': calculate_confidence(recent_ao_peaks, recent_price_highs),
            'ao_divergence_age': 0,
        }
    
    elif regular_bull:
        price_diff = recent_price_lows[0]['value'] - recent_price_lows[1]['value']
        ao_diff = recent_ao_valleys[1]['value'] - recent_ao_valleys[0]['value']  # AO 上升差
        ao_divergence_strength = min(1.0, (ao_diff / abs(price_diff)) * 10)
        
        return {
            'ao_divergence_type': 'REGULAR_BULL',
            'ao_divergence_strength': round(ao_divergence_strength, 2),
            'ao_peak_diff': round((price_diff - ao_diff) / price_diff, 4) if price_diff != 0 else 0,
            'ao_divergence_confidence': calculate_confidence(recent_ao_valleys, recent_price_lows),
            'ao_divergence_age': 0,
        }
    
    else:
        return {
            'ao_divergence_type': 'NONE',
            'ao_divergence_strength': 0.0,
            'ao_peak_diff': 0.0,
            'ao_divergence_confidence': 0.0,
            'ao_divergence_age': 0,
        }


def calculate_confidence(ao_peaks, price_peaks):
    """
    计算背离置信度
    
    因素：
    1. 峰值清晰度（prominence）
    2. 柱体方向一致性（AO 在峰值前后的方向）
    3. 时间跨度合理性（两个峰值之间至少 5-15 根 K 线）
    """
    confidence = 0.5  # 基础值
    
    # 1. 峰值清晰度加分
    if len(ao_peaks) >= 2:
        prominence_ratio = abs(ao_peaks[1]['value'] - ao_peaks[0]['value']) / max(abs(ao_peaks[0]['value']), 0.001)
        confidence += min(0.2, prominence_ratio * 0.5)
    
    # 2. 时间跨度
    if len(price_peaks) >= 2:
        time_span = price_peaks[1]['index'] - price_peaks[0]['index']
        if 5 <= time_span <= 20:
            confidence += 0.2
        elif 3 <= time_span < 5:
            confidence += 0.1
        elif time_span > 20:
            confidence -= 0.1  # 时间太长，背离可能失效
    
    # 3. 柱体方向一致性
    # 如果 AO 在两个峰值之间始终朝背离方向运动，加 0.1
    
    return min(1.0, max(0.0, confidence))
```

### 3.4 信号生成

```python
def generate_ao_signal(divergence_result, kd_state, volty_state, chzl_bsd_state):
    """
    基于 AO 背离生成信号
    
    参数:
        divergence_result: identify_ao_divergence 的输出
        kd_state: KD MTF 状态
        volty_state: Volty 状态
        chzl_bsd_state: 缠论 BSD 状态
    
    返回:
        dict with ao_signal_type, ao_signal_strength, ao_recommendation
    """
    div_type = divergence_result['ao_divergence_type']
    div_conf = divergence_result['ao_divergence_confidence']
    div_strength = divergence_result['ao_divergence_strength']
    
    # 置信度低于 0.60 不生成信号
    if div_conf < 0.60:
        return {
            'ao_signal_type': 'NONE',
            'ao_signal_strength': 0,
            'ao_recommendation': 'HOLD',
        }
    
    # 默认
    signal_type = 'NONE'
    signal_strength = 0
    recommendation = 'HOLD'
    
    # --- 常规顶背离 ---
    if div_type == 'REGULAR_BEAR':
        signal_type = 'REGULAR_BEAR_CONFIRM'
        signal_strength = int(div_strength * 5 + 2)  # 基础 2-7
        recommendation = 'REDUCE_LONG'
        
        # KD 极端区 + 顶背离 = 强制退出
        if kd_state.get('kd_week_extreme_zone') == 'OVERBOUGHT':
            signal_type = 'FORCE_EXIT_LONG'
            signal_strength = 10
            recommendation = 'CLOSE_LONG'
        
        # 缠论 1Sell 出现 + 顶背离 = 共振
        if chzl_bsd_state.get('bsd_type') == '1S':
            signal_strength = min(10, signal_strength + 2)
    
    # --- 常规底背离 ---
    elif div_type == 'REGULAR_BULL':
        signal_type = 'REGULAR_BULL_CONFIRM'
        signal_strength = int(div_strength * 5 + 2)
        recommendation = 'REDUCE_SHORT'
        
        if kd_state.get('kd_week_extreme_zone') == 'OVERSOLD':
            signal_type = 'FORCE_EXIT_SHORT'
            signal_strength = 10
            recommendation = 'CLOSE_SHORT'
        
        if chzl_bsd_state.get('bsd_type') == '1B':
            signal_strength = min(10, signal_strength + 2)
    
    # --- 隐藏顶背离（趋势延续）---
    elif div_type == 'HIDDEN_BEAR':
        signal_type = 'HIDDEN_BEAR_CONFIRM'
        signal_strength = int(div_strength * 4 + 1)
        recommendation = 'HOLD'  # 不反向操作，只是确认趋势继续
    
    # --- 隐藏底背离（趋势延续）---
    elif div_type == 'HIDDEN_BULL':
        signal_type = 'HIDDEN_BULL_CONFIRM'
        signal_strength = int(div_strength * 4 + 1)
        recommendation = 'HOLD'
    
    # Volty 状态调制
    if volty_state.get('volty_trend_state') == 'expansion':
        signal_strength = max(0, signal_strength - 2)  # 高波动时降低信号强度
    
    return {
        'ao_signal_type': signal_type,
        'ao_signal_strength': min(10, signal_strength),
        'ao_recommendation': recommendation,
    }
```

---

## 4. 与现有指标的互锁逻辑（已冻结）

### 4.1 与 KD MTF 的互锁（已冻结）

```text
互锁规则 TKR7 × KD MTF：

1. 常规背离在 KD 极端区才有效：
   - REGULAR_BEAR 需要 kd_week_extreme_zone = 'OVERBOUGHT' 或 kd_day_signal = 'bearish'
   - REGULAR_BULL 需要 kd_week_extreme_zone = 'OVERSOLD' 或 kd_day_signal = 'bullish'
   - 若 kd_week_extreme_zone = 'neutral'，常规背离信号降级为观察（signal_strength × 0.5）

2. KD 锁仓状态对 AO 信号的影响：
   - lock_signal = 'locked' → AO 信号可正常执行
   - lock_signal = 'unlocked' → AO 信号仅作为参考，不触发实际操作（recommendation = 'STANDBY'）
   - lock_signal = 'conflicting' → AO 信号无效（因为方向不明）

3. 强制退出触发条件（已冻结）：
   - kd_week_extreme_zone = 'OVERBOUGHT' 且 ao_divergence_type = 'REGULAR_BEAR' → FORCE_EXIT_LONG
   - kd_week_extreme_zone = 'OVERSOLD' 且 ao_divergence_type = 'REGULAR_BULL' → FORCE_EXIT_SHORT
   - 这是 TKR7 的核心价值：在极端区用背离确认反转，防止追高/杀跌

4. KD 多周期对齐与 AO 背离的共振：
   - kd_alignment_tier = 'strong' 时，AO 背离信号强度 +2（因为多周期方向一致）
   - kd_alignment_tier = 'conflict' 时，AO 背离信号无效（即使背离出现，方向冲突）
```

### 4.2 与 Volty 的互锁（已冻结）

```text
互锁规则 TKR7 × VOLTY：

1. 波动率对 AO 背离的调制：
   - volty_trend_state = 'expansion' → 高波动导致 AO 柱体剧烈震荡，假背离增加 → 信号强度 -2
   - volty_trend_state = 'contraction' → 低波动期背离更可靠 → 信号强度不变
   - volty_trend_state = 'trending' → 趋势中隐藏背离更可靠，常规背离需谨慎 → 常规背离强度 -1

2. Volty 翻转信号与 AO 背离的共振：
   - volty_flip_signal = 'bullish_flip' 且 ao_divergence_type = 'REGULAR_BULL' → 共振，信号强度 +2
   - volty_flip_signal = 'bearish_flip' 且 ao_divergence_type = 'REGULAR_BEAR' → 共振，信号强度 +2
   - 方向冲突 → 以 Volty 为准（Volty 翻转是实时信号，AO 背离是滞后确认）

3. Volty 止损位与 AO 背离的协同：
   - 若 AO 发出 REDUCE_LONG 信号，但价格尚未触及 volty_up_stop → 减仓而非清仓
   - 若 AO 发出 CLOSE_LONG 信号，且价格已触及 volty_up_stop → 清仓（双重确认）
```

### 4.3 与 Volume Profile 的互锁（已冻结）

```text
互锁规则 TKR7 × VP：

1. VP 位置对 AO 背离的过滤：
   - 价格处于 VP 的 VA 内部（平衡区）时，AO 背离信号无效（震荡市中背离频繁，噪音大）
   - 价格处于 VP 的 VA 外部（趋势区）时，AO 背离信号有效
   - 价格处于 VP 的 HVN 上沿 + AO 顶背离 → 高概率反转（阻力位 + 动能衰竭）
   - 价格处于 VP 的 HVN 下沿 + AO 底背离 → 高概率反弹（支撑位 + 动能衰竭）

2. VP 的 POC 与 AO 背离的协同：
   - 价格远离 POC（>1.5×ATR）+ AO 背离 → 价格偏离"公平价值"，回归概率高，背离可靠
   - 价格接近 POC（±0.5×ATR）+ AO 背离 → 价格已回归均值，背离可能是假信号
```

### 4.4 与缠论 BSD 的互锁（已冻结）

```text
互锁规则 TKR7 × CHZL_BSD：

1. BSD 一买/一卖与 AO 背离的共振：
   - BSD 1Buy（趋势反转）+ AO REGULAR_BULL → 共振，确认一买有效性，signal_strength +2
   - BSD 1Sell（趋势反转）+ AO REGULAR_BEAR → 共振，确认一卖有效性，signal_strength +2
   - 这是 TKR7 与 BSD 最强的组合："结构 + 动能"双重确认

2. BSD 二买/二卖与 AO 隐藏背离的协同：
   - BSD 2Buy（回调不破前低）+ AO HIDDEN_BULL → 确认回调结束，趋势继续
   - BSD 2Sell（反弹不过前高）+ AO HIDDEN_BEAR → 确认反弹结束，趋势继续
   - 隐藏背离在此场景下的价值：不是反转信号，而是"回调是否结束"的确认器

3. BSD 三买/三卖与 AO 背离的冲突：
   - BSD 3Buy（离开中枢回踩）+ AO REGULAR_BEAR → 冲突！3Buy 是做多信号，但 AO 顶背离是看空信号
   - 处理方式：以 BSD 为准（3Buy 是结构信号，优先级更高），但 AO 信号触发 "REDUCE_LONG"（减仓而非清仓）
   - BSD 3Sell + AO REGULAR_BULL → 同理，以 BSD 为准，但减仓
```

### 4.5 与 TK-R6/R8 的互锁（已冻结）

```text
互锁规则 TKR7 × TK-R6/R8：

1. TK-R6 阻挡状态与 AO 背离的协同：
   - R6 = TOUCH_BOUNCE（强支撑）+ AO REGULAR_BULL → 共振，确认底背离在强支撑处有效
   - R6 = PIERCED（结构破坏）+ AO REGULAR_BULL → 背离失效（结构已被破坏，即使有背离也不可靠）
   - R6 = DEEP_RETR（深回撤）+ AO HIDDEN_BULL → 确认深回撤后趋势继续

2. TK-R8 资格与 AO 背离的过滤：
   - R8_qualified = False（结构无效）→ 忽略所有 AO 背离信号（结构不对，背离无意义）
   - R8_qualified = True + AO 背离 → 背离有效
   - 这是 TKR7 的安全门：R8 先过滤结构，AO 再确认动能

3. AO 背离对 R6 回撤的预判：
   - 在 R6 回撤过程中（价格从 IB High 向回撤），如果 AO 提前出现 HIDDEN_BULL → 预示回撤可能浅（TOUCH_BOUNCE）
   - 在 R6 回撤过程中，如果 AO 持续下降 → 预示回撤可能深（DEEP_RETR 或 PIERCED）
```

---

## 5. 失效模式（已冻结）

```text
TKR7 失效条件：

1. 数据不足：
   - AO 计算需要至少 34 根 K 线（34 期 SMA），样本不足时 AO 不可靠
   - 背离识别需要至少 2 个清晰的峰值（至少 10-15 根 K 线），样本不足时标记为 'insufficient_data'

2. 震荡市失效：
   - 价格频繁上下穿越，AO 柱体方向频繁变化，产生大量假背离
   - 应对：当 vp_current_rel_position = 'inside'（VP 平衡区）或 kd_alignment_tier = 'conflict' 时，AO 背离无效

3. 极端行情失效：
   - 连续涨停/跌停（A股）→ 价格被锁定，AO 失去意义（中位数价格不变，但 AO 值仍计算）
   - 应对：limit_up / limit_down 时，AO 信号标记为 'market_halt'，不执行

4. 多峰/多谷失效：
   - 价格出现多个相近峰值，AO 也出现多个峰值 → 背离判断困难
   - 应对：只取最近两个清晰峰值，中间如果有其他峰值干扰，标记为 'ambiguous'，降低 confidence

5. 时间过期：
   - ao_divergence_age > 8 根 K 线 → 背离视为过期，需要重新确认
   - 应对：每根 K 线更新 age，age > 8 时强制 ao_divergence_type = 'NONE'

6. 与主要指标冲突：
   - AO 背离与 KD MTF 方向冲突 → 以 KD 为准（KD 是更高层级的方向过滤）
   - AO 背离与缠论 BSD 结构冲突 → 以 BSD 为准（结构信号优先级更高）
```

---

## 6. A 股特殊适配（已冻结）

```text
A 股 TKR7 适配规则：

1. 涨停/跌停影响：
   - limit_up = True → 价格无法继续上涨，AO 的正柱体可能持续扩大但无实际意义
   - limit_down = True → 价格无法继续下跌，AO 的负柱体可能持续扩大但无实际意义
   - 应对：涨跌停期间，AO 背离信号标记为 'market_halt'，不执行
   - 但涨跌停次日开盘的跳空，可能导致 AO 柱体剧烈变化，首日信号需谨慎

2. T+1 影响：
   - AO 背离是"过滤器"而非"触发器"，T+1 对其影响较小
   - 但 AO 发出 FORCE_EXIT 信号时，当日无法执行 → 需要提前预警机制
   - 建议：AO 背离 age = 2-3 根 K 线时就发出预警，而非等到 age = 5-8

3. 散户行为影响：
   - A 股散户在整数关口大量交易，可能导致价格"假突破"整数关口
   - 这种假突破可能产生 AO 假背离
   - 应对：与 VP 的整数关口降权结合，整数关口附近的背离降低 confidence 0.2

4. 早盘跳空影响：
   - A 股集合竞价导致开盘跳空，中位数价格（high+low）/2 被跳空主导
   - AO 值可能被首日 K 线扭曲
   - 应对：开盘后第一根 5min K 线不用于 AO 计算（排除集合竞价影响），或用"盘中 AO"（从 9:35 开始计算）

5. 小盘股流动性问题：
   - 小盘股（<50亿）AO 柱体可能因单笔大单交易而剧烈波动，产生假背离
   - 应对：小盘股 AO 背离 confidence 降低 0.1，或仅用于大盘股/ETF
```

---

## 7. 成熟度与数据需求

| 维度 | 评估 |
|------|------|
| **所需数据** | OHLCV（已有） |
| **计算复杂度** | 中（需要 34 期 SMA + 峰值检测） |
| **实时性能** | 每根 K 线更新一次，不影响性能 |
| **回测可行性** | 高（历史 OHLCV 即可回测） |
| **A 股落地** | 可直接落地（需处理涨跌停/跳空） |
| **外汇/期货/币圈落地** | 直接可用（无限制） |
| **跨周期** | 支持（日线/4H/1H 均可，但 34 期 SMA 需要足够 K 线） |

---

> 文件：OBJECT_CARD_TKR7_P0_E__AO_Divergence_v1.0.md  
> 生产者：Kimi  
> 状态：字段已冻结，待代码实现
