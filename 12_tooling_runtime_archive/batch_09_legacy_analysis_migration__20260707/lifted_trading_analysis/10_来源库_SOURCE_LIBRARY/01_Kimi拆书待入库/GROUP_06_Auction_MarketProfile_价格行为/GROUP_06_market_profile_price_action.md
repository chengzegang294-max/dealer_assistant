# 组06 — Auction/Market Profile + 蜡烛图/价格行为 · 可计算定义与判定规则库

> 处理模式: 模式4（知识库构建）  
> 标签: `market_profile`, `price_action`, `candlestick`, `auction_theory`, `technical_analysis`  
> 目标: 将主观术语转化为可用OHLCV数据计算的算法定义

---

## 一、统一对象定义（OHLCV可计算定义）

---

### O-01: TPO (Time Price Opportunity) — 时间价格机会

**概念来源**: 《Mind over Markets》Dalton  
**主观定义**: TPO是Market Profile的基础单元，代表价格在某一个水平上的存在被记录。  
**可计算定义**:
```python
def generate_tpo_profile(ohlcv_data, time_bucket='30min', price_tick_size=0.25):
    """
    输入: OHLCV数据 (DataFrame with columns: timestamp, open, high, low, close, volume)
    输出: TPO Profile矩阵 — price_level × time_bucket 的二值矩阵
    
    TPO存在 = 1 当且仅当: price_level ∈ [low_of_bucket, high_of_bucket]
    """
    import pandas as pd
    import numpy as np
    
    # 按时间桶重采样
    resampled = ohlcv_data.resample(time_bucket).agg({
        'high': 'max',
        'low': 'min'
    })
    
    # 确定价格范围
    min_price = int(ohlcv_data['low'].min() / price_tick_size) * price_tick_size
    max_price = int(ohlcv_data['high'].max() / price_tick_size) * price_tick_size
    price_levels = np.arange(min_price, max_price + price_tick_size, price_tick_size)
    
    # 构建TPO矩阵
    tpo_matrix = pd.DataFrame(0, index=price_levels, columns=resampled.index)
    
    for timestamp, row in resampled.iterrows():
        mask = (price_levels >= row['low']) & (price_levels <= row['high'])
        tpo_matrix.loc[mask, timestamp] = 1
    
    # TPO计数 = 每个价格水平上的时间桶数量
    tpo_count = tpo_matrix.sum(axis=1)
    
    return {
        'matrix': tpo_matrix,
        'tpo_count': tpo_count,
        'price_levels': price_levels
    }
```

**计算复杂度**: O(P × T)，其中P为价格水平数，T为时间桶数  
**所需数据**: OHLC（L和H用于确定每个时间桶的价格覆盖范围）

---

### O-02: Value Area (VA) — 价值区域

**概念来源**: 《Mind over Markets》Dalton  
**主观定义**: 市场认为"公允价值"的价格区间，约70%的TPO或成交量在此区间内。  
**可计算定义**:
```python
def calculate_value_area(tpo_count, method='tpo', percentile=0.70, volumes=None):
    """
    输入: 
        tpo_count: Series — price_level → TPO计数
        method: 'tpo' 或 'volume'
        percentile: 0.70 (标准Value Area) 或可调
        volumes: 各价格水平的成交量（method='volume'时需要）
    输出:
        VAH (Value Area High), VAL (Value Area Low), POC
    """
    if method == 'volume' and volumes is not None:
        weights = volumes
    else:
        weights = tpo_count
    
    # 按价格排序
    sorted_prices = weights.sort_index(ascending=False)  # 从高到低
    total_weight = sorted_prices.sum()
    target_weight = total_weight * percentile
    
    # 从POC向两边扩展，直到累积权重达到70%
    poc_price = weights.idxmax()
    
    cumulative = weights[poc_price]
    vah = poc_price
    val = poc_price
    
    prices_above = sorted(sorted_prices.index[sorted_prices.index > poc_price], reverse=True)
    prices_below = sorted(sorted_prices.index[sorted_prices.index < poc_price])
    
    i_above, i_below = 0, 0
    
    while cumulative < target_weight and (i_above < len(prices_above) or i_below < len(prices_below)):
        # 交替向上/向下扩展，每次选择权重较大的一侧
        weight_above = sorted_prices.get(prices_above[i_above], 0) if i_above < len(prices_above) else 0
        weight_below = sorted_prices.get(prices_below[i_below], 0) if i_below < len(prices_below) else 0
        
        if weight_above >= weight_below and i_above < len(prices_above):
            vah = prices_above[i_above]
            cumulative += weight_above
            i_above += 1
        elif i_below < len(prices_below):
            val = prices_below[i_below]
            cumulative += weight_below
            i_below += 1
        else:
            break
    
    return {
        'VAH': vah,           # Value Area High
        'VAL': val,           # Value Area Low
        'POC': poc_price,     # Point of Control
        'VWAP': (weights * weights.index).sum() / total_weight,  # 加权均价
        'coverage': cumulative / total_weight
    }
```

**简化版（用于实时计算）**:
```python
def value_area_fast(tpo_count, percentile=0.70):
    """
    快速近似: 使用累积分布直接截断
    """
    total = tpo_count.sum()
    cumsum = tpo_count.sort_index().cumsum()
    
    lower_target = total * (1 - percentile) / 2
    upper_target = total * (1 + percentile) / 2
    
    val = cumsum[cumsum >= lower_target].index[0]
    vah = cumsum[cumsum >= upper_target].index[0]
    poc = tpo_count.idxmax()
    
    return {'VAH': vah, 'VAL': val, 'POC': poc}
```

---

### O-03: POC (Point of Control) — 控制点

**概念来源**: 《Mind over Markets》Dalton  
**主观定义**: TPO最多的价格水平，即市场花费最多时间交易的价格。  
**可计算定义**:
```python
def calculate_poc(tpo_count):
    """
    POC = argmax_price(tpo_count[price])
    如果有多个价格水平TPO相同，取中间值或VWAP最近者
    """
    max_tpo = tpo_count.max()
    candidates = tpo_count[tpo_count == max_tpo].index
    
    if len(candidates) == 1:
        return candidates[0]
    else:
        # 多POC情况: 取中点
        return candidates.mean()  # 或 candidates.median()
```

**变体**: 若用成交量替代TPO，则POC = 最大成交量所在价格水平（Volume Point of Control, VPOC）

---

### O-04: 趋势K (Trend Bar) vs 十字星 (Doji) — 趋势/非趋势判定

**概念来源**: 《日本蜡烛图交易技术分析》Brooks  
**主观定义**: 趋势K有明显实体，代表多头或空头控盘；十字星实体很小，代表多空均衡。  
**可计算定义**:
```python
def classify_bar(open_p, high, low, close, atr_20, context='auto'):
    """
    输入: OHLC + ATR(20) + 市场背景
    输出: bar_type ∈ {BULL_TREND, BEAR_TREND, DOJI}
    
    判定规则:
    1. 实体 = |close - open|
    2. 波幅 = high - low
    3. body_ratio = 实体 / 波幅
    4. 趋势K: body_ratio > 0.5 且 实体 > 0.3 * ATR(20)
    5. 十字星: body_ratio < 0.3 或 实体 < 0.2 * ATR(20)
    """
    body = abs(close - open_p)
    range_bar = high - low
    
    if range_bar == 0:
        return 'DOJI'
    
    body_ratio = body / range_bar
    
    # 趋势K判定
    if body_ratio > 0.5 and body > 0.3 * atr_20:
        if close > open_p:
            return 'BULL_TREND'
        else:
            return 'BEAR_TREND'
    
    # 十字星判定
    if body_ratio < 0.3 or body < 0.2 * atr_20:
        return 'DOJI'
    
    # 过渡状态
    return 'NEUTRAL'
```

**上下文敏感性**: 同一实体大小在强趋势中可能是"小K线"，在平静市场中可能是"趋势K"——必须与ATR相对比较。

---

### O-05: 信号K (Signal Bar) — 开仓信号判定

**概念来源**: 《日本蜡烛图交易技术分析》Brooks  
**主观定义**: 让交易者相信市场已具备开仓条件、存在较高盈利可能性的单根或一组K线。  
**可计算定义**:
```python
def identify_signal_bars(ohlcv, index, direction, lookback=5):
    """
    判定第index根K线是否为direction方向的信号K
    
    输入:
        ohlcv: DataFrame
        index: K线索引
        direction: 'LONG' 或 'SHORT'
        lookback: 回溯期
    输出:
        signal_type ∈ {REVERSAL, BREAKOUT, PULLBACK, FALSE_BREAK, NONE}
        quality_score: 0-100
    """
    bar = ohlcv.iloc[index]
    prev = ohlcv.iloc[index-1] if index > 0 else None
    
    signals = []
    
    # 1. 经典反转K判定
    if direction == 'LONG':
        # 下影线占比 1/3~1/2，上影线很小
        lower_shadow = min(bar['close'], bar['open']) - bar['low']
        upper_shadow = bar['high'] - max(bar['close'], bar['open'])
        range_bar = bar['high'] - bar['low']
        
        if range_bar > 0:
            if (lower_shadow / range_bar >= 0.33 and 
                lower_shadow / range_bar <= 0.5 and
                upper_shadow / range_bar < 0.15 and
                bar['close'] > bar['open']):  # 阳线
                signals.append(('REVERSAL', 80))
    
    elif direction == 'SHORT':
        upper_shadow = bar['high'] - max(bar['close'], bar['open'])
        lower_shadow = min(bar['close'], bar['open']) - bar['low']
        range_bar = bar['high'] - bar['low']
        
        if range_bar > 0:
            if (upper_shadow / range_bar >= 0.33 and
                upper_shadow / range_bar <= 0.5 and
                lower_shadow / range_bar < 0.15 and
                bar['close'] < bar['open']):  # 阴线
                signals.append(('REVERSAL', 80))
    
    # 2. 吞没形态判定
    if prev is not None:
        if direction == 'LONG':
            if (bar['low'] < prev['low'] and 
                bar['high'] > prev['high'] and
                bar['close'] > bar['open']):  # 阳线吞没
                signals.append(('ENGULFING', 70))
        elif direction == 'SHORT':
            if (bar['low'] < prev['low'] and
                bar['high'] > prev['high'] and
                bar['close'] < bar['open']):  # 阴线吞没
                signals.append(('ENGULFING', 70))
    
    # 3. 趋势K顺势判定
    bar_type = classify_bar(bar['open'], bar['high'], bar['low'], bar['close'], 
                           ATR(ohlcv['high'], ohlcv['low'], ohlcv['close']))
    if direction == 'LONG' and bar_type == 'BULL_TREND':
        signals.append(('TREND', 60))
    elif direction == 'SHORT' and bar_type == 'BEAR_TREND':
        signals.append(('TREND', 60))
    
    return signals if signals else [('NONE', 0)]
```

---

### O-06: 主动性(Initiative) vs 响应性(Responsive)行为

**概念来源**: 《Mind over Markets》Dalton  
**主观定义**: 主动性行为推动价格进入新区域（突破VAH/VAL）；响应性行为在价格极端时反向操作（VAH附近做空，VAL附近做多）。  
**可计算定义**:
```python
def classify_behavior(close_price, vah, val, poc, prev_close, trend_direction):
    """
    输入: 当前收盘价 + Value Area边界 + POC + 前收盘 + 趋势方向
    输出: behavior ∈ {INITIATIVE, RESPONSIVE, NEUTRAL}
    
    判定规则:
    1. 主动性(Initiative): 
       - 多头: 价格 > VAH 且 价格 > prev_close（主动向上突破价值区）
       - 空头: 价格 < VAL 且 价格 < prev_close（主动向下突破价值区）
    2. 响应性(Responsive):
       - 在VAH附近做空: 价格接近/突破VAH但出现反转信号
       - 在VAL附近做多: 价格接近/突破VAL但出现反转信号
    3. 中性: 价格在VA内部
    """
    va_range = vah - val
    buffer = va_range * 0.1  # 10%缓冲带
    
    # 主动性判定
    if close_price > vah + buffer and close_price > prev_close:
        return 'INITIATIVE_BULL'
    elif close_price < val - buffer and close_price < prev_close:
        return 'INITIATIVE_BEAR'
    
    # 响应性判定（需要结合反转信号）
    if close_price >= vah - buffer and close_price <= vah + buffer:
        if trend_direction == 'UP' and close_price < prev_close:
            return 'RESPONSIVE_SELL'  # VAH附近遇阻回落
    
    if close_price >= val - buffer and close_price <= val + buffer:
        if trend_direction == 'DOWN' and close_price > prev_close:
            return 'RESPONSIVE_BUY'  # VAL附近支撑反弹
    
    return 'NEUTRAL'
```

---

### O-07: 日类型分类（Day Type Classification）

**概念来源**: 《Mind over Markets》Dalton  
**主观定义**: 根据TPO Profile的形状将交易日分类，每种类型对应不同的市场行为和交易策略。  
**可计算定义**:
```python
def classify_day_type(tpo_profile, value_area):
    """
    输入: TPO Profile + Value Area
    输出: day_type ∈ {NORMAL, NORMAL_VARIATION, TREND, DOUBLE_DISTRIBUTION, 
                      NON_TREND, NEUTRAL}
    
    判定规则（基于TPO分布特征）:
    """
    poc = value_area['POC']
    vah = value_area['VAH']
    val = value_area['VAL']
    tpo_count = tpo_profile['tpo_count']
    
    # 计算分布特征
    profile_range = tpo_count.index.max() - tpo_count.index.min()
    va_range = vah - val
    va_ratio = va_range / profile_range if profile_range > 0 else 0
    
    # POC位置
    poc_position = (poc - tpo_count.index.min()) / profile_range
    
    # TPO分布偏度
    above_poc = tpo_count[tpo_count.index > poc].sum()
    below_poc = tpo_count[tpo_count.index < poc].sum()
    skew = (above_poc - below_poc) / (above_poc + below_poc)
    
    # 单峰检测
    peaks = detect_peaks(tpo_count)
    
    # 分类逻辑
    if len(peaks) >= 2 and va_ratio > 0.5:
        return 'DOUBLE_DISTRIBUTION'  # 双峰，两个POC
    
    if abs(skew) > 0.3 and va_ratio < 0.5:
        return 'TREND'  # 强偏向一侧，POC靠近极端
    
    if abs(poc_position - 0.5) < 0.15 and va_ratio > 0.6:
        return 'NON_TREND'  # POC居中，VA占大部分
    
    if abs(poc_position - 0.5) < 0.1 and len(peaks) == 1:
        return 'NORMAL'  # 标准钟形，POC居中
    
    if abs(skew) > 0.2:
        return 'NORMAL_VARIATION'  # 轻微偏向
    
    return 'NEUTRAL'
```

**各日类型特征对照表**:

| 日类型 | TPO分布特征 | POC位置 | VA占比 | 交易策略 |
|--------|------------|---------|--------|----------|
| Normal | 单峰对称 | 居中 | ~50% | 日内区间交易 |
| Trend | 长尾偏向一侧 | 靠近极端 | <40% | 顺势持仓 |
| Double Distribution | 双峰 | 两个独立峰值 | >60% | 区间突破或回归 |
| Non-trend | 扁平 | 居中 | >70% | 避免交易 |
| Neutral | 近似矩形 | 不明显 | 极高 | 观望 |

---

## 二、判定规则库（伪代码）

---

### Rule-01: Market Profile开盘位置策略

```python
RULE Market_Profile_Open_Strategy:
    INPUT: open_price, prev_vah, prev_val, prev_poc, trend_bias
    OUTPUT: trade_direction, entry_price, stop_price, confidence
    
    IF open_price > prev_vah:
        # Value Area外上方开盘
        IF trend_bias == BULLISH:
            direction = LONG
            entry = open_price
            stop = prev_vah  # 回落到VAH止损
            confidence = 0.75
            note = "开盘高于VAH，趋势向上 → 主动性做多"
        ELSE:
            direction = SHORT
            entry = open_price
            stop = prev_vah + 1.5 * ATR
            confidence = 0.55
            note = "开盘高于VAH但趋势不明 → 响应性做空（高风险）"
    
    ELIF open_price < prev_val:
        # Value Area外下方开盘
        IF trend_bias == BEARISH:
            direction = SHORT
            entry = open_price
            stop = prev_val
            confidence = 0.75
            note = "开盘低于VAL，趋势向下 → 主动性做空"
        ELSE:
            direction = LONG
            entry = open_price
            stop = prev_val - 1.5 * ATR
            confidence = 0.55
            note = "开盘低于VAL但趋势不明 → 响应性做多（高风险）"
    
    ELIF open_price >= prev_val AND open_price <= prev_vah:
        # Value Area内部开盘 → 观望，等待突破或反弹
        direction = NONE
        note = "VA内部开盘，等待价格行为确认"
        
        # 子规则: 内部开盘后的方向选择
        IF open_price > prev_poc AND trend_bias == BULLISH:
            entry = prev_vah + tick_size
            direction = LONG
            confidence = 0.60
        ELIF open_price < prev_poc AND trend_bias == BEARISH:
            entry = prev_val - tick_size
            direction = SHORT
            confidence = 0.60
    
    RETURN direction, entry, stop, confidence
```

---

### Rule-02: 价格行为反转交易规则

```python
RULE Price_Action_Reversal:
    INPUT: ohlcv, index, market_context
    OUTPUT: signal ∈ {LONG_REVERSAL, SHORT_REVERSAL, NONE}, quality
    
    bar = ohlcv[index]
    atr = ATR(ohlcv, 20)
    
    # 前提条件1: 必须有趋势可反（ADX>25说明趋势强，适合反转）
    adx = ADX(ohlcv, 14)
    IF adx < 20:
        RETURN NONE, 0  # 无趋势，反转交易无意义
    
    # 前提条件2: 价格到达极端位置（趋势线/通道线/支撑阻力）
    at_support = test_support(bar['low'], support_levels)
    at_resistance = test_resistance(bar['high'], resistance_levels)
    
    # 多头反转判定
    IF at_support OR bar['low'] < lower_channel_line:
        reversal_score = 0
        
        # 检查反转K特征
        lower_shadow = min(bar['close'], bar['open']) - bar['low']
        upper_shadow = bar['high'] - max(bar['close'], bar['open'])
        range_bar = bar['high'] - bar['low']
        
        IF range_bar > 0:
            # 下影线占1/3~1/2
            IF lower_shadow / range_bar >= 0.33 AND lower_shadow / range_bar <= 0.5:
                reversal_score += 30
            # 上影线很小
            IF upper_shadow / range_bar < 0.15:
                reversal_score += 20
            # 阳线收盘
            IF bar['close'] > bar['open']:
                reversal_score += 20
            # 收盘价高于前收
            IF bar['close'] > ohlcv[index-1]['close']:
                reversal_score += 15
            # 与前K线重叠少
            IF bar['low'] > ohlcv[index-1]['low']:
                reversal_score += 15
        
        IF reversal_score >= 70:
            RETURN LONG_REVERSAL, reversal_score
    
    # 空头反转判定（对称）
    IF at_resistance OR bar['high'] > upper_channel_line:
        reversal_score = 0
        
        upper_shadow = bar['high'] - max(bar['close'], bar['open'])
        lower_shadow = min(bar['close'], bar['open']) - bar['low']
        range_bar = bar['high'] - bar['low']
        
        IF range_bar > 0:
            IF upper_shadow / range_bar >= 0.33 AND upper_shadow / range_bar <= 0.5:
                reversal_score += 30
            IF lower_shadow / range_bar < 0.15:
                reversal_score += 20
            IF bar['close'] < bar['open']:
                reversal_score += 20
            IF bar['close'] < ohlcv[index-1]['close']:
                reversal_score += 15
            IF bar['high'] < ohlcv[index-1]['high']:
                reversal_score += 15
        
        IF reversal_score >= 70:
            RETURN SHORT_REVERSAL, reversal_score
    
    RETURN NONE, 0
```

---

### Rule-03: 趋势延续（回调入场）规则

```python
RULE Trend_Continuation_Pullback:
    INPUT: ohlcv, trend_direction, ema_period=20
    OUTPUT: entry_signal, stop_loss, target
    
    ema = EMA(ohlcv['close'], ema_period)
    atr = ATR(ohlcv, 20)
    
    IF trend_direction == UPTREND:
        # 上涨趋势中等待回调到EMA
        FOR i IN range(len(ohlcv)-5, len(ohlcv)):
            bar = ohlcv[i]
            
            # 条件1: 价格接近或触及EMA
            near_ema = abs(bar['close'] - ema[i]) < 0.5 * atr
            
            # 条件2: 回调中出现小K线/十字星（动能衰竭）
            bar_type = classify_bar(bar['open'], bar['high'], bar['low'], 
                                   bar['close'], atr)
            pullback_pause = bar_type == 'DOJI' or bar_type == 'NEUTRAL'
            
            # 条件3: 下一根K线突破信号K高点
            IF near_ema AND pullback_pause AND i < len(ohlcv)-1:
                signal_bar_high = bar['high']
                next_bar = ohlcv[i+1]
                
                IF next_bar['high'] > signal_bar_high:
                    entry = signal_bar_high + tick_size
                    stop = bar['low'] - tick_size
                    target = entry + 2 * (entry - stop)  # 2:1盈亏比
                    RETURN LONG_ENTRY, stop, target
    
    ELIF trend_direction == DOWNTREND:
        # 对称的空头逻辑
        FOR i IN range(len(ohlcv)-5, len(ohlcv)):
            bar = ohlcv[i]
            near_ema = abs(bar['close'] - ema[i]) < 0.5 * atr
            bar_type = classify_bar(...)
            pullback_pause = bar_type == 'DOJI'
            
            IF near_ema AND pullback_pause AND i < len(ohlcv)-1:
                signal_bar_low = bar['low']
                next_bar = ohlcv[i+1]
                
                IF next_bar['low'] < signal_bar_low:
                    entry = signal_bar_low - tick_size
                    stop = bar['high'] + tick_size
                    target = entry - 2 * (stop - entry)
                    RETURN SHORT_ENTRY, stop, target
    
    RETURN NONE, NULL, NULL
```

---

### Rule-04: ii/iii结构（孕线组合）突破规则

```python
RULE ii_iii_Pattern_Breakout:
    INPUT: ohlcv, index
    OUTPUT: signal, direction, quality
    
    # ii结构: 连续2根孕线（后一根K线范围在前一根范围内）
    # iii结构: 连续3根孕线
    
    IF index < 3:
        RETURN NONE, NULL, 0
    
    k0 = ohlcv[index-3]  # 母线
    k1 = ohlcv[index-2]  # 第一根孕线
    k2 = ohlcv[index-1]  # 第二根孕线（ii结构）
    k3 = ohlcv[index]    # 当前K线（iii结构的第三根）
    
    # ii结构检测
    ii_structure = (k1['high'] <= k0['high'] AND k1['low'] >= k0['low'] AND
                   k2['high'] <= k1['high'] AND k2['low'] >= k1['low'])
    
    # iii结构检测
    iii_structure = ii_structure AND (k3['high'] <= k2['high'] AND k3['low'] >= k2['low'])
    
    pattern = 'iii' if iii_structure else ('ii' if ii_structure else 'NONE')
    
    IF pattern != 'NONE':
        # 突破方向判定
        breakout_up = k3['close'] > k0['high']  # 突破母线高点
        breakout_down = k3['close'] < k0['low']  # 突破母线低点
        
        # 质量评分
        quality = 50
        IF pattern == 'iii':
            quality += 15  # iii结构蓄力更强
        
        # 顺势方向加分
        IF k3['close'] > EMA(ohlcv['close'], 20)[index]:
            IF breakout_up: quality += 20
        ELSE:
            IF breakout_down: quality += 20
        
        # 收线方向与突破方向一致
        IF breakout_up AND k3['close'] > k3['open']:
            quality += 15
        IF breakout_down AND k3['close'] < k3['open']:
            quality += 15
        
        IF breakout_up:
            RETURN BREAKOUT, LONG, quality
        IF breakout_down:
            RETURN BREAKOUT, SHORT, quality
    
    RETURN NONE, NULL, 0
```

---

### Rule-05: 二次进场（Second Entry）规则

```python
RULE Second_Entry:
    INPUT: ohlcv, first_entry_level, direction
    OUTPUT: second_entry_signal, quality
    
    """
    二次进场: 第一次反转尝试后，市场再次测试同一水平并再次反转
    特征: 第二次进场点的价格通常与第一次差不多或更差（不是更好）
    """
    
    IF direction == LONG:
        # 寻找双底结构
        lows = find_local_lows(ohlcv, lookback=10)
        IF len(lows) >= 2:
            low1, low2 = lows[-2], lows[-1]
            
            # 双底条件
            price_diff = abs(low2['low'] - low1['low']) / low1['low']
            IF price_diff < 0.001:  # 价格接近（0.1%容差）
                
                # 第二次低点的反转K检测
                bar = ohlcv[low2['index']]
                bar_type = classify_bar(bar['open'], bar['high'], bar['low'], 
                                       bar['close'], ATR(ohlcv, 20))
                
                IF bar_type == 'BULL_TREND' OR is_reversal_bar(bar, 'LONG'):
                    # 检查是否有更高的低点形成（HL）
                    IF low2['low'] >= low1['low']:
                        quality = 75
                        note = "双底二次进场，稍高的低点"
                    ELSE:
                        quality = 60
                        note = "双底二次进场，但低点更低（谨慎）"
                    
                    RETURN LONG_SECOND_ENTRY, quality
    
    ELIF direction == SHORT:
        # 对称的双顶检测
        highs = find_local_highs(ohlcv, lookback=10)
        IF len(highs) >= 2:
            high1, high2 = highs[-2], highs[-1]
            price_diff = abs(high2['high'] - high1['high']) / high1['high']
            
            IF price_diff < 0.001:
                bar = ohlcv[high2['index']]
                IF is_reversal_bar(bar, 'SHORT'):
                    IF high2['high'] <= high1['high']:
                        quality = 75
                        note = "双顶二次进场，稍低的高点"
                    ELSE:
                        quality = 60
                        note = "双顶二次进场，但高点更高（谨慎）"
                    
                    RETURN SHORT_SECOND_ENTRY, quality
    
    RETURN NONE, 0
```

---

## 三、适用边界

### 3.1 Market Profile适用条件

| 条件 | 要求 | 不满足时的处理 |
|------|------|---------------|
| 数据精度 | 需要日内数据（至少30分钟K线）构建TPO | 使用日数据时退化为成交量分布分析（Volume Profile） |
| 流动性 | 日成交量>10万手确保TPO有意义 | 低流动性市场TPO分布稀疏，POC不稳定 |
| 市场类型 | 适合拍卖市场（期货、股票、外汇） | OTC市场报价分散，VA边界模糊 |
| 时间框架 | 日内交易最佳，也可用于日线 | 周线以上TPO时间跨度过长，POC参考意义下降 |
| 趋势状态 | ADX>20时VA突破信号可靠 | ADX<20时价格在VA内震荡，突破多为假突破 |

### 3.2 价格行为/蜡烛图适用条件

| 条件 | 要求 | 不满足时的处理 |
|------|------|---------------|
| 时间框架 | 5分钟或15分钟K线最佳（Brooks主推5分钟） | 日线信号少但可靠性更高；1分钟噪音过多 |
| 市场类型 | 高流动性连续交易品种（Emini、外汇、权重股） | 低流动性品种缺口多，K线形态失真 |
| 波动性 | ATR>最小报价单位×10（确保K线有意义） | 超低波动市场K线过窄，形态无法识别 |
| 趋势背景 | 必须首先判定趋势/震荡状态 | 震荡市中趋势K信号假阳性>60% |
| 数据完整性 | 无长时段缺失数据 | 数据缺口会破坏K线形态连续性 |

### 3.3 组合使用最佳场景

```
最佳场景 = {
    "市场": "E-mini S&P 500期货 (ES)",
    "时间框架": "5分钟K线 + 日线Market Profile",
    "波动率": "ATR(20) ∈ [$10, $30]",
    "趋势状态": "ADX(14) > 25",
    "日类型": "Trend Day 或 Normal Day",
    "流动性": "日均成交量 > 200万手"
}
```

---

## 四、标签映射建议

### 4.1 Market Profile → 量化标签

| MP术语 | 量化标签 | 计算公式 | 用途 |
|--------|---------|---------|------|
| POC | POC_LEVEL | argmax(tpo_count) | 日内支撑/阻力核心参考 |
| VAH | VA_HIGH | value_area_high | 超买/响应性卖出区 |
| VAL | VA_LOW | value_area_low | 超卖/响应性买入区 |
| Initiative | INITIATIVE_BUY/SELL | 价格>VAH或<VAL+趋势确认 | 趋势延续信号 |
| Responsive | RESPONSIVE_BUY/SELL | VA边界+反转K | 均值回归信号 |
| Trend Day | DAY_TYPE=TREND | skew>0.3, va_ratio<0.4 | 日内顺势策略 |
| Normal Day | DAY_TYPE=NORMAL | 单峰对称, poc居中 | 区间交易策略 |
| Double Dist | DAY_TYPE=DBLDIST | 双峰tpo | 突破或回归策略 |
| Non-trend | DAY_TYPE=NON_TREND | 扁平分布 | 避免交易 |

### 4.2 价格行为 → 量化标签

| 价格行为术语 | 量化标签 | 计算特征 | 信号强度 |
|-------------|---------|---------|---------|
| 趋势K | BULL_TREND / BEAR_TREND | body_ratio>0.5, body>0.3ATR | ★★★ |
| 十字星 | DOJI | body_ratio<0.3 or body<0.2ATR | ★★☆ |
| 反转K | REVERSAL_LONG/SHORT | 影线比例+收线位置 | ★★★★ |
| 吞没形态 | ENGULFING | 完全包含前K+方向一致 | ★★★ |
| 孕线 | INSIDE_BAR | high<prev_high, low>prev_low | ★★☆ |
| ii结构 | ii_PATTERN | 连续2根孕线 | ★★★ |
| iii结构 | iii_PATTERN | 连续3根孕线 | ★★★★ |
| 二次进场 | 2ND_ENTRY | 双底/双顶+反转K | ★★★★ |
| 失败再失败 | FAILED_FAILURE | 突破失败后的再次失败 | ★★★★★ |
| 5跳失败 | 5TICK_FAIL | 突破<5最小单位即反转 | ★★★ |
| EMA回调 | EMA_PULLBACK | 价格接近EMA+小K线 | ★★★ |
| 两段式行情 | TWO_LEGGED | 趋势中两个清晰的推动段 | ★★★ |

### 4.3 组合信号映射

```python
COMBINED_SIGNAL_MAPPING = {
    "STRONG_LONG": {
        "conditions": [
            "open < prev_VAL",           # Market Profile: VA下方开盘
            "BULL_REVERSAL_BAR",          # Brooks: 多头反转K
            "close > EMA_20",             # 趋势向上
            "ADX > 25"                    # 趋势强劲
        ],
        "confidence": 0.85,
        "strategy": "RESPONSIVE_BUY"
    },
    
    "STRONG_SHORT": {
        "conditions": [
            "open > prev_VAH",           # Market Profile: VA上方开盘
            "BEAR_REVERSAL_BAR",          # Brooks: 空头反转K
            "close < EMA_20",             # 趋势向下
            "ADX > 25"
        ],
        "confidence": 0.85,
        "strategy": "RESPONSIVE_SELL"
    },
    
    "TREND_CONTINUATION": {
        "conditions": [
            "DAY_TYPE == TREND",         # Market Profile: 趋势日
            "TREND_BAR",                  # Brooks: 顺势趋势K
            "price > VAH (多头) or < VAL (空头)",
            "INITIATIVE_BEHAVIOR"         # 主动行为
        ],
        "confidence": 0.80,
        "strategy": "INITIATIVE_ENTRY"
    },
    
    "RANGE_BOUND": {
        "conditions": [
            "DAY_TYPE in [NORMAL, NON_TREND]",
            "DOJI or INSIDE_BAR",         # Brooks: 非趋势K线
            "price within VA",            # Market Profile: VA内部
            "ADX < 20"
        ],
        "confidence": 0.70,
        "strategy": "AVOID_OR_RANGE_TRADE"
    }
}
```

---

## 五、冲突裁决

### 5.1 跨书术语冲突

| 冲突 | Dalton (MP) | Brooks (价格行为) | 裁决 | 理由 |
|------|------------|-------------------|------|------|
| "趋势"定义 | TPO分布偏向一侧，POC靠近极端 | 连续趋势K，高点/低点持续抬高/降低 | **两者互补** | MP从宏观分布定义趋势，Brooks从微观K线确认趋势；MP用于方向判断，Brooks用于入场时机 |
| "价值"概念 | VA内部=公允价值 | 每根K线都在传递信息，无所谓"公允" | **分场景使用** | MP的VA在日内有效；Brooks方法适用于任何时间框架 |
| "主动性"vs"顺势" | Initiative=突破VA | 顺势=与趋势同向的趋势K | **Brooks定义优先** | 因为Brooks的顺势K线是MP Initiative行为的微观表现 |
| 日类型 vs K线类型 | Normal Day = 区间交易 | 趋势K在任何日都可能出现 | **日类型过滤>K线类型** | 在Non-trend Day中出现的趋势K假阳性率高，应降低仓位 |

### 5.2 同一书内矛盾处理

| 矛盾 | 情况 | 裁决 |
|------|------|------|
| Brooks: 趋势K顺势交易 vs 趋势K太大=衰竭 | 强趋势中出现极大趋势K | 第一根大K线=顺势信号；连续第二根极大K线=可能衰竭，减半仓位 |
| Dalton: 主动性突破VA vs 假突破 | 价格突破VAH但立即回落 | 需要Brooks确认: 突破VAH后无趋势K跟随=假突破；有趋势K跟随=真突破 |
| Brooks: 二次进场 vs 三次进场 | 楔形形态允许三次进场 | 默认只交易二次进场；三次进场仅在楔形（通道收敛）中允许 |

---

## 六、YAML 汇总卡

```yaml
---
group: "06"
theme: "Auction/Market Profile + 蜡烛图/价格行为"
processing_mode: "4 (知识库构建)"
objective: "将主观术语转化为OHLCV可计算定义"

books:
  - title: "Mind over Markets"
    author: "James F. Dalton, Eric T. Jones, Robert B. Dalton"
    key_contributions:
      - "TPO Profile构建算法"
      - "Value Area (VA) 计算: 70% TPO覆盖区间"
      - "POC (Point of Control): TPO最大值价格"
      - "日类型分类: Normal/Trend/Double Dist/Non-trend/Neutral"
      - "主动性(Initiative) vs 响应性(Responsive)行为框架"
      - "趋势市场 vs 平衡市场(Bracketed)判定"
    data_requirements:
      - "日内OHLC（至少30分钟K线）"
      - "前日VAH/VAL/POC作为当日参考"
    
  - title: "日本蜡烛图交易技术分析"
    author: "艾尔·布鲁克斯 (Al Brooks)"
    key_contributions:
      - "趋势K vs 十字星可计算分类"
      - "反转K的量化特征（影线比例+收线位置）"
      - "吞没/孕线/ii/iii结构检测算法"
      - "二次进场(Second Entry)规则"
      - "失败再失败(Failed Failure)高概率结构"
      - "EMA回调+小K线=趋势延续入场"
    data_requirements:
      - "5分钟OHLCV（最佳）"
      - "EMA(20)作为趋势参考"
      - "ATR(20)作为K线大小标准化基准"

objects_defined: 7  # O-01~O-07
rules_defined: 5   # Rule-01~Rule-05
combined_signals: 4
applicability_boundaries: 3
label_mappings: 20+

key_formulas:
  TPO: "tpo_matrix[price, time] = 1 if price ∈ [low, high] of time_bucket"
  VA: "70% of cumulative TPO from POC outward"
  POC: "argmax_price(tpo_count[price])"
  Trend_Bar: "body_ratio > 0.5 AND body > 0.3 × ATR(20)"
  Doji: "body_ratio < 0.3 OR body < 0.2 × ATR(20)"
  Reversal_Score: "基于影线比例+收线位置+前K关系的综合评分(0-100)"

best_practices:
  - "先用Market Profile判定日类型和VA边界（宏观框架）"
  - "再用价格行为在VA边界或趋势中寻找精确入场点（微观执行）"
  - "ADX>25时优先考虑顺势信号（Initiative + 趋势K）"
  - "ADX<20时优先考虑VA内部的响应性交易（Responsive + 反转K）"
  - "Non-trend Day中即使出现趋势K也应降低仓位50%"
  - "二次进场成功率>首次进场，应重点监控"

pitfalls:
  - "在低流动性市场使用TPO → POC不稳定"
  - "在震荡市中追趋势K → 假阳性>60%"
  - "忽视日类型过滤 → Normal Day中趋势K多为假突破"
  - "二次进场价格优于首次 → 可能是陷阱"
  - "1分钟图中交易 → 噪音过多，止损频繁触发"

cross_group_refs:
  - "Group 01: ATR计算, ADX计算, EMA计算"
  - "Group 05: 趋势跟踪系统的入场/出场可与MP/PA信号结合"
  - "Group 07: 布鲁克斯价格行为反映了机构订单流的微观结构"
```

---

> **处理说明**: 本组采用模式4（知识库构建），核心目标是将Market Profile和Price Action的主观术语转化为可用标准OHLCV数据计算的伪代码。所有对象定义包含完整的算法描述，判定规则可直接转化为Python/C++代码。Dalton的宏观市场结构框架与Brooks的微观价格行为执行形成了互补体系。  
> **关键原则**: MP提供"在哪里交易"（VA边界/日类型），Brooks提供"何时交易"（信号K/反转结构）；两者结合优于单独使用任何一种方法。
