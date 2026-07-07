# Group 06 — Market Profile · 拍卖理论 · 价格行为（可编程定义版）
> 模式4（知识库构建）：将主观术语转化为可计算定义
> 覆盖书目：Dalton《Mind over Markets》| Brooks《日本蜡烛图交易技术分析》

---

# 第一章：统一对象定义
> 每个对象给"最小可实现定义"（优先OHLCV；需更细粒度数据时注明）
> 格式：概念 → 数学/算法定义 → 计算步骤 → 数据来源 →（书名+页码）

---

## 1.1 Market Profile 核心对象
> 基于 Dalton《Mind over Markets》（页码基于原书目录结构估计，标注estimated）

### O1: TPO（Time Price Opportunity）

**概念**：将交易日按固定时间区间（通常为30分钟）分割，每个区间用一个字母标记。若某价格在该时间区间内被交易，则在该价格旁标记对应字母。

**最小可实现定义**：
```
输入：tick数据 或 分钟K线数据（OHLCV），时间区间Δt（默认30分钟）
输出：TPO矩阵 M[price_level][time_period] = letter

算法：
1. 确定当日价格精度：tick_size（最小变动价位）
2. 价格离散化：price_level = round(price / tick_size)
3. 时间区间编号：period = floor((time - open_time) / Δt)
4. 对每条成交记录/分钟K线的(H+L)/2所在的价格层级，标记对应字母
5. 结果：每个价格层级的TPO字母集合

数据需求：分钟级OHLCV（最低要求）；tick数据（更精确）
```

**来源**：Dalton, estimated p.9-13（第二章"Organizing the Day"）

---

### O2: 初始平衡（Initial Balance, IB）

**概念**：交易日最初两个TPO周期（通常为首小时）形成的价格区间，代表 locals/场内交易员建立的双边交易范围。

**最小可实现定义**：
```python
def calculate_initial_balance(ohlcv, open_time, ib_periods=2, tpo_minutes=30):
    """
    输入：分钟级OHLCV数据
    输出：IB_high, IB_low, IB_range
    """
    ib_end = open_time + timedelta(minutes=tpo_minutes * ib_periods)
    ib_data = ohlcv[ohlcv.index < ib_end]
    
    IB_high = ib_data['high'].max()      # 初始平衡高点
    IB_low = ib_data['low'].min()         # 初始平衡低点  
    IB_range = IB_high - IB_low           # 初始平衡宽度
    
    return {
        'IB_high': IB_high,
        'IB_low': IB_low,
        'IB_range': IB_range,
        'IB_mid': (IB_high + IB_low) / 2
    }
```

**可观测证据**：IB_range < 0.5 × ATR(20) → 窄幅IB，预示非趋势日可能

**来源**：Dalton, estimated p.11-13（第二章"Initial Balance"）

---

### O3: Value Area（价值区）

**概念**：当日约70%成交量（或TPO计数）所集中的价格区间，代表市场参与者认可的价值范围。

**最小可实现定义**：
```python
def calculate_value_area(tpo_matrix, volume_profile, percentile=0.7):
    """
    方法A：基于TPO计数（Dalton标准方法）
    方法B：基于成交量（更精确）
    
    TPO计数法：
    1. 找到POC（TPO计数最高的价格层级）
    2. 从POC向上下扩展，每次包含TPO计数最高的相邻层级
    3. 直到累计TPO计数 ≥ 总TPO计数 × percentile
    
    成交量法：
    1. 从成交量最大的价格层级开始
    2. 向上下扩展，每次包含成交量最大的相邻层级
    3. 直到累计成交量 ≥ 总成交量 × percentile
    """
    # TPO计数法实现
    sorted_levels = sort_price_levels_by_tpo_count(tpo_matrix)
    poc_level = sorted_levels[0]  # TPO计数最高
    
    va_levels = [poc_level]
    remaining = sorted_levels[1:]
    
    while tpo_count(va_levels) / total_tpo_count < percentile:
        # 选择上下相邻中TPO计数更高的
        upper = get_upper_adjacent(va_levels, remaining)
        lower = get_lower_adjacent(va_levels, remaining)
        
        if tpo_count(upper) > tpo_count(lower):
            va_levels.append(upper)
        else:
            va_levels.append(lower)
    
    VAH = max(va_levels)  # Value Area High
    VAL = min(va_levels)  # Value Area Low
    
    return {'VAH': VAH, 'VAL': VAL, 'POC': poc_level}
```

**关键参数**：percentile = 0.7（标准），范围0.65-0.75

**来源**：Dalton, estimated p.331-333（Appendix "Value-Area Calculation"）

---

### O4: POC（Point of Control）

**概念**：当日TPO计数最高（或成交量最大）的价格层级，代表当日市场共识最强的价格。

**最小可实现定义**：
```python
def calculate_poc(volume_profile):
    """
    输入：volume_profile[price_level] = volume_at_level
    输出：POC_price
    
    若存在多个相同最大值的层级，取中间值或取最近期的
    """
    max_volume = max(volume_profile.values())
    poc_candidates = [p for p, v in volume_profile.items() if v == max_volume]
    
    if len(poc_candidates) == 1:
        return poc_candidates[0]
    else:
        # 多个候选：取中间值（Dalton方法）
        return median(poc_candidates)
```

**来源**：Dalton, estimated p.331-333

---

### O5: 平衡 vs 失衡（Balance vs Imbalance）

**概念**：市场价格在Value Area内双向交易为"平衡"；突破Value Area向单一方向运动为"失衡"。

**最小可实现定义**：
```python
def classify_balance_imbalance(current_price, VAH, VAL, prior_VAH, prior_VAL):
    """
    平衡条件（需同时满足）：
    1. 当前价格位于前日VA内 OR 当日价格区间与前日VA重叠 > 50%
    2. 当日VA宽度 / 前日VA宽度 ∈ [0.5, 2.0]
    3. 当日POC距离前日POC < 0.3 × ATR(20)
    
    失衡条件（任一满足）：
    1. 当前价格 > 前日VAH + 0.5×IB_range（向上失衡）
    2. 当前价格 < 前日VAL - 0.5×IB_range（向下失衡）
    3. 当日VA宽度 > 2 × 前日VA宽度（波动率扩张）
    """
    in_prior_VA = (prior_VAL <= current_price <= prior_VAH)
    
    if in_prior_VA:
        return 'BALANCE'
    elif current_price > prior_VAH:
        return 'IMBALANCE_UP'
    elif current_price < prior_VAL:
        return 'IMBALANCE_DOWN'
    else:
        return 'TRANSITION'
```

**来源**：Dalton, estimated p.34-38（第三章"Trending versus Bracketed Markets"）

---

### O6: 日型分类（Day Type Classification）

**概念**：Dalton将交易日分为7种类型，每种类型反映不同的市场结构和参与者的行为模式。

**最小可实现定义**：
```python
def classify_day_type(ohlcv, open_time, close_time, IB_high, IB_low):
    """
    基于OHLCV数据的日型分类算法
    """
    day_high = ohlcv['high'].max()
    day_low = ohlcv['low'].min()
    day_range = day_high - day_low
    IB_range = IB_high - IB_low
    IB_extension = day_range / IB_range if IB_range > 0 else 0
    
    # 收盘位置（0=最低, 1=最高）
    close_pos = (ohlcv['close'].iloc[-1] - day_low) / day_range if day_range > 0 else 0.5
    
    # TPO形状分析
    tpo_counts = calculate_tpo_per_level(ohlcv)
    shape = analyze_profile_shape(tpo_counts)  # 'bell', 'b', 'p', 'd', etc.
    
    # === 分类规则 ===
    
    # 1. Normal Day（正常日）
    # IB_extension ≈ 1.0-1.3, 收盘在IB内或略扩展, 钟形分布
    if IB_extension <= 1.3 and shape == 'bell':
        return 'NORMAL_DAY'
    
    # 2. Normal Variation of Normal Day（正常变型日）
    # IB_extension ≈ 1.3-2.0, 一个方向有扩展, 收盘在扩展端
    elif 1.3 < IB_extension <= 2.0 and abs(close_pos - 0.5) > 0.3:
        return 'NORMAL_VARIATION'
    
    # 3. Trend Day（趋势日）
    # IB_extension > 2.0, 收盘在极端, 单峰偏态分布
    elif IB_extension > 2.0 and (close_pos > 0.8 or close_pos < 0.2):
        return 'TREND_DAY'
    
    # 4. Double-Distribution Trend Day（双分布趋势日）
    # 两个分离的VA, 中间有gap
    elif has_two_distributions(tpo_counts) and IB_extension > 2.0:
        return 'DOUBLE_DISTRIBUTION_TREND'
    
    # 5. Nontrend Day（非趋势日）
    # IB_extension < 1.2, 全天在IB内或略扩展, 收盘在中部
    elif IB_extension < 1.2 and 0.3 < close_pos < 0.7:
        return 'NONTREND_DAY'
    
    # 6. Neutral Day（中性日）
    # 收盘在IB中部, 上下扩展大致对称
    elif abs(close_pos - 0.5) < 0.1 and IB_extension > 1.5:
        return 'NEUTRAL_DAY'
    
    # 7. Neutral-Extreme Day（中性极端日）
    # 先向两侧扩展, 最后收盘在某一极端（表示Other Timeframe介入）
    elif IB_extension > 1.8 and (close_pos > 0.85 or close_pos < 0.15):
        # 需确认：价格曾回到IB中部区域
        if price_visited_middle(ohlcv, IB_high, IB_low):
            return 'NEUTRAL_EXTREME'
    
    return 'UNCLASSIFIED'
```

| 日型 | IB延伸倍数 | 收盘位置 | TPO形状 | 交易含义 |
|------|-----------|---------|---------|---------|
| Normal Day | 1.0-1.3 | 中部 | 钟形 | 均值回归，区间交易 |
| Normal Variation | 1.3-2.0 | 偏向一端 | 偏态钟形 | 顺势至扩展端 |
| Trend Day | >2.0 | 极端(>80%或<20%) | 单峰偏态 | 趋势跟踪，勿逆势 |
| Double-Distribution | >2.0 | 极端 | 双峰 | 趋势中有一次再平衡 |
| Nontrend Day | <1.2 | 中部 | 窄钟形 | 无方向，减少交易 |
| Neutral Day | >1.5 | 中部 | 宽平形 | 多空争夺，等方向 |
| Neutral-Extreme | >1.8 | 极端 | 宽→极端 | Other Timeframe控制方向 |

**来源**：Dalton, estimated p.19-29（第二章日型分类）

---

### O7: Other Timeframe（OTF）控制

**概念**：判断是长线参与者（Other Timeframe）还是短线参与者（Day Timeframe）在控制市场。

**最小可实现定义**：
```python
def detect_otf_control(ohlcv, IB_high, IB_low, VAH, VAL, current_price):
    """
    OTF控制检测：价格行为在Value Area极端的反应
    
    OTF买入信号（Responsive Buying）：
    - 价格跌破VAL后迅速回到VA内
    - 收盘 > VAL 且下一根K线收阳
    
    OTF卖出信号（Responsive Selling）：
    - 价格突破VAH后迅速回到VA内
    - 收盘 < VAH 且下一根K线收阴
    
    OTF方向性买入（Initiative Buying）：
    - 收盘 > VAH 且维持1小时以上
    - 成交量 > 20日均量 × 1.5
    
    OTF方向性卖出（Initiative Selling）：
    - 收盘 < VAL 且维持1小时以上
    - 成交量 > 20日均量 × 1.5
    """
    
    if current_price > VAH:
        if ohlcv['close'].iloc[-1] > VAH and time_above_VAH > 60_minutes:
            return 'OTF_INITIATIVE_BUY'
        elif quick_return_to_VA(ohlcv, VAH, VAL):
            return 'OTF_RESPONSIVE_SELL_ZONE'
    
    elif current_price < VAL:
        if ohlcv['close'].iloc[-1] < VAL and time_below_VAL > 60_minutes:
            return 'OTF_INITIATIVE_SELL'
        elif quick_return_to_VA(ohlcv, VAH, VAL):
            return 'OTF_RESPONSIVE_BUY_ZONE'
    
    return 'DAY_TIMEFRAME_CONTROL'
```

**来源**：Dalton, estimated p.40-45（第三章"Initiative versus Responsive Activity"）

---

### O8: 拍卖轮换（Auction Rotation）

**概念**：价格在VA内上下移动称为"平衡区轮换"；突破VA向新区间运动称为"方向性拍卖"。

**最小可实现定义**：
```python
def detect_auction_rotation(price_history, VAH, VAL, lookback=20):
    """
    平衡区轮换检测
    
    标准：
    - 价格在[VAL, VAH]内的停留时间占比 > 70%
    - 价格触及VAH和VAL的次数各 ≥ 2次/日
    - 无方向性突破（收盘不在VA外超过30分钟）
    
    方向性拍卖检测：
    - 价格突破VAH/VAL后，30分钟内不回撤到VA内
    - 突破后成交量 > 前20日均量 × 1.5
    """
    in_va_time = sum(1 for p in price_history if VAL <= p <= VAH) / len(price_history)
    
    touches_VAH = sum(1 for i in range(len(price_history)-1) 
                      if price_history[i] < VAH <= price_history[i+1])
    touches_VAL = sum(1 for i in range(len(price_history)-1) 
                      if price_history[i] > VAL >= price_history[i+1])
    
    if in_va_time > 0.7 and touches_VAH >= 2 and touches_VAL >= 2:
        return 'ROTATION'
    elif in_va_time < 0.5 and (touches_VAH > 0 or touches_VAL > 0):
        return 'DIRECTIONAL_AUCTION'
    else:
        return 'MIXED'
```

**来源**：Dalton, estimated p.204-210（第四章"Long-Term Auction Rotations"）

---

### O9: 3-1 Day（3-1日）

**概念**：交易日分为两个明显不同的部分——前3/4时间在一个平衡区内交易，最后1/4时间出现方向性突破。

**最小可实现定义**：
```python
def detect_31_day(ohlcv, split_ratio=0.75):
    """
    检测3-1日型
    
    条件：
    1. 前split_ratio时间的ATR < 全天ATR × 0.5
    2. 后(1-split_ratio)时间的ATR > 全天ATR × 0.8
    3. 后半段收盘方向与前段的中部偏离 > 1个前段VA宽度
    """
    split_idx = int(len(ohlcv) * split_ratio)
    first_part = ohlcv.iloc[:split_idx]
    second_part = ohlcv.iloc[split_idx:]
    
    first_atr = first_part['high'].max() - first_part['low'].min()
    second_atr = second_part['high'].max() - second_part['low'].min()
    full_atr = ohlcv['high'].max() - ohlcv['low'].min()
    
    first_mid = (first_part['high'].max() + first_part['low'].min()) / 2
    second_close = second_part['close'].iloc[-1]
    
    is_31 = (first_atr < full_atr * 0.5 and 
             second_atr > full_atr * 0.8 and 
             abs(second_close - first_mid) > first_atr)
    
    return is_31
```

**来源**：Dalton, estimated p.273（第四章"3-1 Days"）

---

### O10: Spike（尖峰）

**概念**：价格快速突破平衡区，TPO分布呈现长条形（"d"或"b"形），表示OTF力量的突然介入。

**最小可实现定义**：
```python
def detect_spike(ohlcv, VAH, VAL, spike_periods=3):
    """
    尖峰检测
    
    条件：
    1. 在spike_periods个TPO周期内，价格移动 > (VAH-VAL) × 1.5
    2. 这些周期内TPO计数 < 正常周期的50%（快速通过，无停留）
    3. 尖峰方向的成交量 > 前10个周期平均 × 2
    """
    recent_range = ohlcv['high'].tail(spike_periods).max() - ohlcv['low'].tail(spike_periods).min()
    va_width = VAH - VAL
    
    if recent_range > va_width * 1.5:
        spike_volume = ohlcv['volume'].tail(spike_periods).mean()
        normal_volume = ohlcv['volume'].tail(10).head(7).mean()
        
        if spike_volume > normal_volume * 2:
            direction = 'UP' if ohlcv['close'].iloc[-1] > ohlcv['close'].iloc[-spike_periods-1] else 'DOWN'
            return {'SPIKE': True, 'direction': direction, 'magnitude': recent_range / va_width}
    
    return {'SPIKE': False}
```

**来源**：Dalton, estimated p.280-288（第四章"Spikes"）

---

## 1.2 价格行为核心对象
> 基于 Brooks《日本蜡烛图交易技术分析》

### O11: 趋势K（Trend Bar）vs 十字星（Doji）

**概念**：K线实体明显为趋势K（代表一方控盘）；实体很小或不存在为十字星（代表平衡）。

**最小可实现定义**：
```python
def classify_bar(open_price, high, low, close, recent_bars_atr):
    """
    趋势K vs 十字星分类
    
    输入：单根K线的OHLC + 最近N根K线的平均ATR（默认10根）
    """
    body = abs(close - open_price)
    range_bar = high - low
    
    # 实体比例 = 实体 / K线波幅
    body_ratio = body / range_bar if range_bar > 0 else 0
    
    # 相对于近期平均的实体大小
    relative_body = body / recent_bars_atr if recent_bars_atr > 0 else 0
    
    if body_ratio >= 0.5 and relative_body >= 0.3:
        direction = 'BULL' if close > open_price else 'BEAR'
        return {'type': 'TREND_BAR', 'direction': direction, 
                'body_ratio': body_ratio, 'strength': relative_body}
    
    elif body_ratio < 0.3 and range_bar < recent_bars_atr * 1.2:
        return {'type': 'DOJI', 'direction': 'NEUTRAL',
                'body_ratio': body_ratio, 'context': 'balance'}
    
    else:
        return {'type': 'MIXED', 'direction': 'UNCLEAR',
                'body_ratio': body_ratio}
```

**关键阈值**：
| 参数 | 值 | 说明 |
|------|-----|------|
| body_ratio（趋势K）| ≥ 0.5 | 实体占波幅≥50% |
| body_ratio（十字星）| < 0.3 | 实体占波幅<30% |
| relative_body | ≥ 0.3×ATR | 实体≥近期平均波幅的30% |

**来源**：Brooks, p.90-102（第1章"趋势K和十字星"）

---

### O12: 反转K（Reversal Bar）

**概念**：显示趋势可能反转的K线形态——下影线长（多头反转）或上影线长（空头反转），收盘强势。

**最小可实现定义**：
```python
def classify_reversal_bar(open_p, high, low, close, prior_bar, trend_direction):
    """
    多头反转K检测
    空头反转K检测
    """
    body = abs(close - open_p)
    range_bar = high - low
    upper_shadow = high - max(open_p, close)
    lower_shadow = min(open_p, close) - low
    
    # === 多头反转K ===
    is_bull_reversal = (
        close > open_p and                    # 阳线
        lower_shadow >= range_bar * 0.3 and  # 下影线 ≥ 30%波幅
        lower_shadow >= upper_shadow * 2 and # 下影线 ≥ 2倍上影线
        close > prior_bar['close'] and       # 收盘 > 前一根收盘
        body >= range_bar * 0.3              # 实体 ≥ 30%波幅
    )
    
    # === 空头反转K ===
    is_bear_reversal = (
        close < open_p and                    # 阴线
        upper_shadow >= range_bar * 0.3 and  # 上影线 ≥ 30%波幅
        upper_shadow >= lower_shadow * 2 and # 上影线 ≥ 2倍下影线
        close < prior_bar['close'] and       # 收盘 < 前一根收盘
        body >= range_bar * 0.3
    )
    
    # === 趋势背景过滤 ===
    # 多头反转K只在下跌趋势或横盘底部有效
    # 空头反转K只在上涨趋势或横盘顶部有效
    if is_bull_reversal and trend_direction in ['DOWN', 'RANGE_BOTTOM']:
        return {'type': 'BULL_REVERSAL', 'confidence': calculate_confidence(lower_shadow, body, range_bar)}
    
    elif is_bear_reversal and trend_direction in ['UP', 'RANGE_TOP']:
        return {'type': 'BEAR_REVERSAL', 'confidence': calculate_confidence(upper_shadow, body, range_bar)}
    
    return {'type': 'NOT_REVERSAL'}
```

**来源**：Brooks, p.123-143（第1章"信号K：反转K"）

---

### O13: 孕线（Inside Bar / ii结构）

**概念**：当前K线的高低点被前一根K线的高低点完全包含。连续两根孕线为ii结构，三根为iii结构。

**最小可实现定义**：
```python
def detect_inside_bar(ohlcv, index):
    """
    孕线检测
    
    孕线：当前K线 high < 前K线 high AND 当前K线 low > 前K线 low
    """
    if index < 1:
        return False
    
    current = ohlcv.iloc[index]
    prior = ohlcv.iloc[index - 1]
    
    is_inside = (current['high'] < prior['high'] and 
                 current['low'] > prior['low'])
    
    return is_inside

def detect_ii_structure(ohlcv, index):
    """
    ii结构：连续两根孕线
    iii结构：连续三根孕线
    """
    if index < 2:
        return None
    
    is_inside_1 = detect_inside_bar(ohlcv, index)
    is_inside_2 = detect_inside_bar(ohlcv, index - 1)
    is_inside_3 = detect_inside_bar(ohlcv, index - 2) if index >= 3 else False
    
    if is_inside_1 and is_inside_2 and is_inside_3:
        return 'iii'
    elif is_inside_1 and is_inside_2:
        return 'ii'
    
    return None
```

**交易含义**：ii结构后突破方向提供高概率顺势入场点；出现在趋势末端可能是"最后的旗形"。

**来源**：Brooks, p.153-158（第1章"信号K：其他类型"）

---

### O14: 吞没K（Outside Bar / Engulfing）

**概念**：当前K线的高点超过前一根的高点，低点低于前一根的低点，形成"吞没"。

**最小可实现定义**：
```python
def detect_engulfing(ohlcv, index):
    """
    吞没检测：当前K线范围完全包含前一根K线
    """
    if index < 1:
        return None
    
    current = ohlcv.iloc[index]
    prior = ohlcv.iloc[index - 1]
    
    is_engulfing = (current['high'] > prior['high'] and 
                    current['low'] < prior['low'])
    
    if not is_engulfing:
        return None
    
    # 判断方向：收盘位置
    if close > open_p:
        direction = 'BULL_ENGULFING'
    else:
        direction = 'BEAR_ENGULFING'
    
    # ioi结构检测：吞没前是孕线 + 吞没后是孕线
    # (在调用函数时检测)
    
    return {'type': direction, 'magnitude': (current['high']-current['low']) / (prior['high']-prior['low'])}
```

**来源**：Brooks, p.164-170, p.284-290（第1章"吞没K"及多处）

---

### O15: 两段式走势（Two-Legged Move）

**概念**：趋势中的回调或反转通常以两段式展开（ABC结构）。第二段完成后，原趋势大概率延续。

**最小可实现定义**：
```python
def detect_two_legged_move(ohlcv, start_idx, trend_direction):
    """
    两段式走势检测
    
    在上升趋势中：
    - Leg A：回调第一段（跌破前低）
    - Leg B：小型反弹（不超过前高）
    - Leg C：回调第二段（新低或更高低点）
    
    在下跌趋势中反向
    
    算法：
    1. 找到趋势中的回调起点（突破迷你趋势线）
    2. 识别第一段（A）：逆势运行，至少2-3根K线
    3. 识别中间段（B）：顺势回调，不超过前极值点
    4. 识别第二段（C）：再次逆势运行
    5. 验证：C的终点是顺势入场点
    """
    
    # 简化版：使用收盘价变化率
    closes = ohlcv['close'].iloc[start_idx:].values
    
    # 找局部极值点
    from scipy.signal import find_peaks
    
    if trend_direction == 'UP':
        # 在上升趋势中找回调的两段下跌
        peaks, _ = find_peaks(closes, distance=3)
        troughs, _ = find_peaks(-closes, distance=3)
        
        # 需要：峰→谷→小峰→谷（两段下跌）
        if len(peaks) >= 2 and len(troughs) >= 2:
            # 检查是否是两段式下跌结构
            leg_a_end = troughs[0]  # 第一段结束
            mid_peak = peaks[1] if len(peaks) > 1 else None  # 中间反弹
            leg_c_end = troughs[1] if len(troughs) > 1 else None  # 第二段结束
            
            if mid_peak and leg_c_end and closes[mid_peak] < closes[peaks[0]]:
                return {
                    'TWO_LEGGED': True,
                    'leg_a_end': leg_a_end,
                    'mid_peak': mid_peak,
                    'leg_c_end': leg_c_end,
                    'entry_point': 'leg_c_breakout'
                }
    
    return {'TWO_LEGGED': False}
```

**来源**：Brooks, p.501-505（第3章"两段走势"）

---

### O16: 第二高点/第二低点（H2/L2）

**概念**：趋势中回调后第二次尝试突破前高/前低。H2突破做多、L2突破做空是Brooks体系的核心顺势入场结构。

**最小可实现定义**：
```python
def detect_h2_l2(ohlcv, trend_direction):
    """
    H2/L2检测
    
    上升趋势中的H2：
    1. 有一个波段高点H1
    2. 回调后不创新高（形成停顿/十字星/小K线）
    3. 再次上涨突破H1高点 → H2买入信号
    
    下跌趋势中的L2反向
    """
    
    highs = ohlcv['high'].values
    lows = ohlcv['low'].values
    
    if trend_direction == 'UP':
        # 找H1（波段高点）
        h1_idx = argmax_recent(highs, window=10)
        h1_price = highs[h1_idx]
        
        # 找回调低点
        post_h1_lows = lows[h1_idx:]
        pullback_idx = h1_idx + argmin(post_h1_lows)
        
        # 找H2（第二次尝试的高点）
        post_pullback = ohlcv.iloc[pullback_idx:]
        h2_candidates = post_pullback[post_pullback['high'] > h1_price * 0.995]
        
        if len(h2_candidates) > 0:
            # 真正的H2：突破H1后的回调再突破
            first_break = h2_candidates.index[0]
            # 检查突破后是否有回调
            post_break = ohlcv.loc[first_break:]
            # ...
            return {'H2': True, 'h1': h1_price, 'trigger': h2_candidates.index[0]}
    
    elif trend_direction == 'DOWN':
        # L2逻辑对称
        pass
    
    return {'H2': False, 'L2': False}
```

**来源**：Brooks, p.505-508, p.525（第3章多处，核心结构）

---

### O17: EMA缺口K线（EMA Gap Bar）

**概念**：趋势中K线整体位于EMA均线的一侧，K线极值点与EMA之间存在"缺口"。第一次出现EMA缺口K线后突破其极值点是顺势入场信号。

**最小可实现定义**：
```python
def detect_ema_gap_bar(ohlcv, ema_period=20):
    """
    EMA缺口K线检测
    
    上涨EMA缺口K线：
    - K线低点 > EMA AND K线高点 > EMA（整体在EMA上方）
    - K线低点与EMA之间有缺口（距离 > 0）
    
    下跌EMA缺口K线反向
    """
    ema = ohlcv['close'].ewm(span=ema_period).mean()
    
    results = []
    for i in range(1, len(ohlcv)):
        current = ohlcv.iloc[i]
        current_ema = ema.iloc[i]
        
        # 上涨缺口K线（整体在EMA上方，但有缺口）
        if current['low'] > current_ema:
            gap_size = current['low'] - current_ema
            # 检查是否是"第一次"缺口（前一根不是缺口）
            prior = ohlcv.iloc[i-1]
            prior_ema = ema.iloc[i-1]
            if not (prior['low'] > prior_ema):  # 前一根不是缺口K线
                results.append({
                    'index': i, 'type': 'EMA_GAP_BAR_UP',
                    'gap_size': gap_size, 'ema': current_ema
                })
        
        # 下跌缺口K线
        elif current['high'] < current_ema:
            gap_size = current_ema - current['high']
            prior = ohlcv.iloc[i-1]
            prior_ema = ema.iloc[i-1]
            if not (prior['high'] < prior_ema):
                results.append({
                    'index': i, 'type': 'EMA_GAP_BAR_DOWN',
                    'gap_size': gap_size, 'ema': current_ema
                })
    
    return results
```

**来源**：Brooks, p.693-700（第4章"EMA均线和均线回调构成的缺口K线"）

---

### O18: 2HM（2-Hour Move）

**概念**：价格连续2小时以上不触及EMA均线，表示趋势极强。第一次回踩EMA是高概率顺势入场点。

**最小可实现定义**：
```python
def detect_2hm(ohlcv, ema_period=20, min_duration=120):
    """
    2HM检测
    
    条件：
    - 连续min_duration分钟，所有K线都位于EMA同一侧
    - K线不触及EMA（low > EMA 或 high < EMA）
    """
    ema = ohlcv['close'].ewm(span=ema_period).mean()
    
    # 找连续在EMA上方的段
    above_ema = ohlcv['low'] > ema
    
    # 找连续段
    consecutive_above = find_consecutive_true(above_ema, min_duration)
    consecutive_below = find_consecutive_true(ohlcv['high'] < ema, min_duration)
    
    if len(consecutive_above) > 0:
        return {'2HM': True, 'direction': 'UP', 
                'duration_minutes': consecutive_above[0]['length'] * bar_interval}
    
    if len(consecutive_below) > 0:
        return {'2HM': True, 'direction': 'DOWN',
                'duration_minutes': consecutive_below[0]['length'] * bar_interval}
    
    return {'2HM': False}
```

**来源**：Brooks, p.700-704（第4章"2HM"）

---

### O19: 双底牛旗 / 双顶熊旗（Double Bottom Bull Flag / Double Top Bear Flag）

**概念**：趋势中回调形成的双重底（上涨趋势中）或双重顶（下跌趋势中），是趋势延续的高概率形态。

**最小可实现定义**：
```python
def detect_double_bottom_bull_flag(ohlcv, trend_high_idx):
    """
    双底牛旗检测
    
    条件：
    1. 上升趋势中有波段高点
    2. 回调后形成第一个底（低点L1）
    3. 小幅反弹后再度下跌
    4. 第二个底L2 ≈ L1（不跌破L1或仅跌破1-2跳）
    5. 从L2反弹突破中间反弹高点 → 买入信号
    """
    
    highs = ohlcv['high'].values
    lows = ohlcv['low'].values
    
    # 从趋势高点后找回调
    post_high = ohlcv.iloc[trend_high_idx:]
    
    # 找两个低点
    l1_idx = trend_high_idx + argmin(post_high['low'].head(20))
    l1_price = lows[l1_idx]
    
    # 找中间反弹高点
    post_l1 = ohlcv.iloc[l1_idx:]
    mid_high_idx = l1_idx + argmax(post_l1['high'].head(15))
    
    # 找第二个低点
    post_mid = ohlcv.iloc[mid_high_idx:]
    l2_idx = mid_high_idx + argmin(post_mid['low'].head(15))
    l2_price = lows[l2_idx]
    
    # 判断是否是双底
    price_tolerance = atr_recent * 0.1  # 允许10% ATR的偏差
    is_double_bottom = abs(l2_price - l1_price) < price_tolerance
    
    # L2不低于L1太多
    l2_not_lower = l2_price >= l1_price - price_tolerance
    
    if is_double_bottom and l2_not_lower:
        trigger_price = highs[mid_high_idx]  # 突破中间高点买入
        return {
            'DOUBLE_BOTTOM_BULL_FLAG': True,
            'l1': l1_price, 'l2': l2_price,
            'trigger': trigger_price,
            'stop': min(l1_price, l2_price) - atr_recent * 0.5
        }
    
    return {'DOUBLE_BOTTOM_BULL_FLAG': False}
```

**来源**：Brooks, p.669-677（第4章"双重顶部的熊旗和双重底部的牛旗"）

---

### O20: 最后的旗形（Final Flag）

**概念**：趋势末端出现的横盘区间（旗形），其突破失败预示趋势可能反转。

**最小可实现定义**：
```python
def detect_final_flag(ohlcv, trend_direction, trend_length_bars=50):
    """
    最后的旗形检测
    
    条件：
    1. 趋势已运行较长时间（> trend_length_bars）
    2. 出现3-10根K线的窄幅横盘（旗形）
    3. 旗形宽度 < 最近ATR × 0.5
    4. 突破旗形后缺乏跟进（2-3根K线内回到旗形内）
    5. 出现反向反转K线
    """
    
    recent = ohlcv.tail(trend_length_bars)
    
    # 检测旗形（最近10-20根K线中的横盘段）
    flag_segment = recent.tail(10)
    flag_high = flag_segment['high'].max()
    flag_low = flag_segment['low'].min()
    flag_width = flag_high - flag_low
    
    recent_atr = calculate_atr(ohlcv, 20).iloc[-1]
    
    if flag_width < recent_atr * 0.5:
        # 检查突破后是否失败
        post_flag = ohlcv.tail(5)  # 旗形后的K线
        
        if trend_direction == 'UP':
            # 向上突破后应回到旗形内
            broke_above = post_flag['high'].max() > flag_high
            failed_back = post_flag['close'].iloc[-1] < flag_high
            
            if broke_above and failed_back:
                return {'FINAL_FLAG': True, 'direction': 'UP_REVERSAL_EXPECTED'}
        
        elif trend_direction == 'DOWN':
            broke_below = post_flag['low'].min() < flag_low
            failed_back = post_flag['close'].iloc[-1] > flag_low
            
            if broke_below and failed_back:
                return {'FINAL_FLAG': True, 'direction': 'DOWN_REVERSAL_EXPECTED'}
    
    return {'FINAL_FLAG': False}
```

**来源**：Brooks, p.573-580, p.355-362（第3章和第5章多处）

---

# 第二章：判定规则库
> 将形态/日型分类写成 if/else 规则或伪代码

## 2.1 日型分类完整判定树（Dalton）

```python
def day_type_decision_tree(ohlcv):
    """
    日型分类完整判定树
    参考：Dalton, estimated p.19-29
    """
    
    IB = calculate_initial_balance(ohlcv)
    day_h = ohlcv['high'].max()
    day_l = ohlcv['low'].min()
    day_range = day_h - day_l
    IB_ext = day_range / IB['IB_range']
    close = ohlcv['close'].iloc[-1]
    close_pos = (close - day_l) / day_range
    
    # === 第一层：IB延伸 ===
    if IB_ext <= 1.3:
        # === 第二层：收盘位置 ===
        if 0.35 < close_pos < 0.65:
            return 'NONTREND_DAY'  # 非趋势日
        else:
            return 'NORMAL_DAY'     # 正常日
    
    elif 1.3 < IB_ext <= 2.0:
        if 0.35 < close_pos < 0.65:
            return 'NEUTRAL_DAY'    # 中性日
        else:
            return 'NORMAL_VARIATION'  # 正常变型日
    
    elif IB_ext > 2.0:
        # === 第二层：TPO形状 ===
        if is_double_distribution(ohlcv):
            return 'DOUBLE_DISTRIBUTION_TREND'
        
        # === 第三层：Neutral-Extreme检测 ===
        if price_visited_VA_middle(ohlcv, IB) and (close_pos > 0.85 or close_pos < 0.15):
            return 'NEUTRAL_EXTREME'
        
        # === 第四层：收盘位置 ===
        if close_pos > 0.8:
            return 'TREND_DAY_UP'
        elif close_pos < 0.2:
            return 'TREND_DAY_DOWN'
        else:
            return 'NORMAL_VARIATION'  # 回落到变型
    
    return 'UNCLASSIFIED'
```

## 2.2 开盘分类判定（Dalton）

```python
def classify_open(current_open, prior_VAH, prior_VAL, prior_range_high, prior_range_low):
    """
    开盘分类判定
    参考：Dalton, estimated p.75-84（第四章"Open Within/Outside Value/Range"）
    """
    
    if prior_VAL <= current_open <= prior_VAH:
        # Value内开盘 → 预期日内平衡/轮换
        return 'OPEN_WITHIN_VALUE', 'strategy: range_trade_until_break'
    
    elif (current_open > prior_VAH and current_open <= prior_range_high) or \
         (current_open < prior_VAL and current_open >= prior_range_low):
        # Value外但Range内 → "Return to Value"交易
        if current_open > prior_VAH:
            return 'OPEN_ABOVE_VALUE_BELOW_RANGE_HIGH', 'strategy: sell_responsive'
        else:
            return 'OPEN_BELOW_VALUE_ABOVE_RANGE_LOW', 'strategy: buy_responsive'
    
    elif current_open > prior_range_high:
        # Range外高开 → 方向性拍卖向上
        return 'OPEN_ABOVE_RANGE', 'strategy: follow_up_or_wait_for_test'
    
    elif current_open < prior_range_low:
        # Range外低开 → 方向性拍卖向下
        return 'OPEN_BELOW_RANGE', 'strategy: follow_down_or_wait_for_test'
```

## 2.3 价格行为入场结构判定树（Brooks）

```python
def price_action_entry_decision_tree(ohlcv, index, trend_direction, ema_period=20):
    """
    价格行为入场结构判定树
    参考：Brooks, 全书核心逻辑
    """
    
    current = ohlcv.iloc[index]
    ema = ohlcv['close'].ewm(span=ema_period).mean().iloc[index]
    
    # === 第一层：趋势方向 ===
    if trend_direction == 'UP':
        
        # === 第二层：位置分析 ===
        if current['low'] > ema:
            # 在EMA上方 → 强势顺势
            
            # === 第三层：结构检测 ===
            if detect_h2(ohlcv, index):
                return 'ENTRY: H2_BREAKOUT_LONG', 'stop: below_h2_setup_low'
            
            elif detect_ema_gap_bar(ohlcv, index):
                return 'ENTRY: EMA_GAP_BREAKOUT_LONG', 'stop: below_gap_bar_low'
            
            elif detect_ii_breakout(ohlcv, index, 'UP'):
                return 'ENTRY: ii_BREAKOUT_LONG', 'stop: below_ii_low'
            
            elif is_first_pullback(ohlcv, index, 'UP'):
                return 'ENTRY: FIRST_PULLBACK_LONG', 'stop: below_pullback_low'
        
        else:
            # 测试或跌破EMA → 可能转弱
            
            if detect_double_bottom_bull_flag(ohlcv, index):
                return 'ENTRY: DB_BULL_FLAG_LONG', 'stop: below_second_bottom'
            
            elif is_ema_test_with_reversal_bar(ohlcv, index):
                return 'ENTRY: EMA_TEST_REVERSAL_LONG', 'stop: below_reversal_bar_low'
    
    elif trend_direction == 'DOWN':
        # 对称的空头逻辑
        if current['high'] < ema:
            if detect_l2(ohlcv, index):
                return 'ENTRY: L2_BREAKOUT_SHORT', 'stop: above_l2_setup_high'
            elif detect_ema_gap_bar(ohlcv, index):
                return 'ENTRY: EMA_GAP_BREAKOUT_SHORT', 'stop: above_gap_bar_high'
        else:
            if detect_double_top_bear_flag(ohlcv, index):
                return 'ENTRY: DT_BEAR_FLAG_SHORT', 'stop: above_second_top'
    
    elif trend_direction == 'RANGE':
        # 区间交易
        range_high, range_low = get_range_levels(ohlcv, 30)
        
        if near_level(current, range_high, tolerance=0.01):
            if detect_reversal_bar(ohlcv, index, 'BEAR'):
                return 'ENTRY: RANGE_TOP_REVERSAL_SHORT', 'stop: above_range_high'
        
        elif near_level(current, range_low, tolerance=0.01):
            if detect_reversal_bar(ohlcv, index, 'BULL'):
                return 'ENTRY: RANGE_BOTTOM_REVERSAL_LONG', 'stop: below_range_low'
    
    return 'NO_CLEAR_ENTRY'
```

## 2.4 趋势强度评分（Brooks）

```python
def calculate_trend_strength(ohlcv, lookback=20, ema_period=20):
    """
    趋势强度综合评分
    返回0-100的分数，>70为强趋势，<30为弱/无趋势
    参考：Brooks, p.505-525（第3章"强弱的信号"）
    """
    
    ema = ohlcv['close'].ewm(span=ema_period).mean()
    score = 0
    
    # 1. 开盘跳空幅度 (>5跳加分)
    gap = abs(ohlcv['open'].iloc[0] - ohlcv['close'].iloc[-2])
    if gap > 5 * tick_size:
        score += 15
    
    # 2. 2HM检测 (连续2小时不触EMA)
    hms = detect_2hm(ohlcv)
    if hms['2HM']:
        score += 20
    
    # 3. EMA方向一致性 (连续N根在EMA同侧)
    above_ema = (ohlcv['low'] > ema).tail(lookback).sum()
    below_ema = (ohlcv['high'] < ema).tail(lookback).sum()
    if above_ema == lookback or below_ema == lookback:
        score += 15
    
    # 4. 回调深度 (<30% range加分)
    recent_range = ohlcv['high'].tail(lookback).max() - ohlcv['low'].tail(lookback).min()
    pullback = max_drawdown_from_high(ohlcv.tail(lookback))
    if pullback < recent_range * 0.3:
        score += 15
    
    # 5. 光头光脚K线比例
    trend_bar_ratio = count_trend_bars(ohlcv.tail(lookback)) / lookback
    score += trend_bar_ratio * 20
    
    # 6. 收盘位置极端性
    close_pos = (ohlcv['close'].iloc[-1] - ohlcv['low'].tail(lookback).min()) / recent_range
    if close_pos > 0.8 or close_pos < 0.2:
        score += 15
    
    return min(score, 100)
```

---

# 第三章：适用边界
> 在哪些市场/周期失效，常见误判来源

## 3.1 Market Profile 适用边界（Dalton）

| 限制因素 | 失效场景 | 检测方法 | 缓解措施 |
|---------|---------|---------|---------|
| **数据精度要求** | tick级数据不可得；仅有日K线 | 检查数据频率 < 1分钟 | 使用Volume Profile替代TPO；降低日型分类精度 |
| **市场开盘时间** | 24小时市场（加密货币/外汇）无明确"开盘" | 检查是否有固定开盘时间 | 自定义交易时段（如UTC 0:00作为人工"开盘"）；使用滚动窗口Profile |
| **流动性不足** | 小盘股/远月合约TPO分布稀疏 | TPO计数 < 10的价格层级占比 > 30% | 不应用Profile分析；改用其他方法 |
| **单一事件驱动** | 重大新闻/数据发布导致价格跳变 | 日内波幅 > 3× ATR(20) | 标记为"新闻影响市场"，暂停Profile交易（Dalton, estimated p.304） |
| **市场结构变化** | 电子交易取代场内交易，locals角色弱化 | IB_range持续缩小（< 0.3× ATR） | 调整IB定义；增加盘后时段分析 |
| **非趋势市场长期持续** | 连续5日以上Nontrend Day | 日型分类连续为Nontrend | 切换至区间交易策略；等待方向明确 |

## 3.2 价格行为适用边界（Brooks）

| 限制因素 | 失效场景 | 检测方法 | 缓解措施 |
|---------|---------|---------|---------|
| **时间周期过短** | 1分钟图噪声过大，假突破率 > 70% | 统计1分钟图的止损触发率 | 主要使用5分钟图；1分钟仅用于精确入场（Brooks, p.50-52） |
| **时间周期过长** | 日线/周线信号过于稀疏 | 月均交易信号 < 2次 | 结合多时间框架；降低仓位 |
| **极端低波动** | ATR < 历史10th百分位，K线重叠度 > 80% | ATR_percentile < 10 | 减少交易频率；降低仓位（Brooks, p.43"铁丝网形态"） |
| **极端高波动** | 黑天鹅/崩盘，连续3根K线 > 3× ATR | 日内最大K线 > 3× ATR | 扩大止损至固定金额（如Emini 2点）；减少头寸（Brooks, p.57-58） |
| **横盘区间过窄** | 全天波幅 < 5跳（Emini），无交易空间 | day_range < 5 × tick_size | 停止交易；等待突破（Brooks, p.525-530） |
| **新闻发布时** | FOMC/非农数据等，价格在5分钟内波动 > 10点 | 事件时间窗口检测 | 事件前5分钟平仓；事件后等5分钟再交易（Brooks, p.58"新闻影响"） |

## 3.3 两体系交叉边界

| 场景 | Market Profile | 价格行为 | 建议 |
|------|---------------|---------|------|
| 趋势日 | 有效：IB延伸 > 2，方向明确 | 有效：H2/L2连续触发 | **两者协同最佳** |
| 非趋势日 | 有效：VA内轮换交易 | 有效：区间顶底反转 | 两者一致，降低仓位 |
| 趋势初期 | 滞后：需等IB形成后判断 | 灵敏：趋势K序列早期识别 | 以价格行为为主，Profile验证 |
| 趋势末期 | 有效：Neutral-Extreme检测 | 有效：Final Flag识别 | 两者相互验证 |
| 低流动性市场 | 部分失效：TPO稀疏 | 部分失效：信号K不连续 | 均不适用，换其他方法 |
| 高波动黑天鹅 | 失效：日型分类崩溃 | 部分有效：固定止损保护 | 以风控优先，暂停分析 |

---

# 第四章：仓库标签映射

## 4.1 N02_session_or_time_window 映射

| 本组概念 | 映射到 N02 | 说明 |
|---------|-----------|------|
| TPO周期（30分钟分割）| N02: session_intraday_period | 日内时段划分 |
| 初始平衡（IB，首小时）| N02: opening_range | 开盘区间，与Opening Range概念一致 |
| 日型分类（7种日型）| N02: session_regime_classifier | 日内体制分类器 |
| 3-1 Day（前3/4横盘+后1/4突破）| N02: session_late_breakout | 尾盘突破时段 |
| 2HM（连续2小时不触EMA）| N02: session_trend_strength_indicator | 时段趋势强度指标 |
| 11:30陷阱（午间假突破）| N02: session_midday_trap | 午间时段陷阱模式 |
| Spike（尖峰突破）| N02: session_impulse_event | 时段冲击事件 |
| Value Area（价值区）| N02: session_value_zone | 时段价值区域 |
| 开盘分类（Value内/外/Range外）| N02: opening_classification | 开盘分类体系 |

## 4.2 structure_price_action 映射

| 本组概念 | 映射到 structure_price_action | 说明 |
|---------|------------------------------|------|
| 趋势K / 十字星 | structure_bar_classification | K线分类 |
| 反转K | structure_reversal_bar | 反转结构 |
| 孕线（ii/iii）| structure_inside_bar_consolidation | 内含线盘整 |
| 吞没K | structure_engulfing_bar | 吞没结构 |
| 两段式走势 | structure_two_legged_correction | 两段式修正 |
| H2/L2突破 | structure_second_entry | 二次入场结构 |
| EMA缺口K线 | structure_ema_gap | EMA缺口结构 |
| 双底牛旗/双顶熊旗 | structure_flag_continuation | 旗形延续结构 |
| 最后的旗形 | structure_final_flag_reversal | 末端旗形反转 |
| 趋势线/通道线 | structure_trend_channel_lines | 趋势通道线 |
| 迷你趋势线 | structure_micro_trendline | 微型趋势线 |
| 平衡/失衡 | structure_balance_imbalance | 平衡失衡状态 |
| 拍卖轮换 | structure_auction_rotation | 拍卖轮换模式 |
| Spike（尖峰）| structure_spike_breakout | 尖峰突破 |
| 铁丝网形态 | structure_barbed_wire | 铁丝网盘整 |

---

# 第五章：冲突与裁决

## 5.1 冲突一：TPO计数法 vs 成交量法计算Value Area

| 来源 | 方法 | 论据 | 页码 |
|------|------|------|------|
| **Dalton原版** | TPO计数法 | 传统Market Profile使用TPO而非成交量；TPO反映"时间=价值"的Steidlmayer理念 | estimated p.331-333 |
| **现代软件** | 成交量法 | 成交量更精确反映实际交易活动；TPO在低流动性时失真 | — |

**裁决**：**成交量法为首选，TPO法为fallback**
- 当有tick/volume数据时：使用成交量法（更精确）
- 当只有分钟K线时：使用TPO法（从分钟数据推导）
- 两者差异 > 10%时，以成交量法为准，记录差异原因

## 5.2 冲突二：20周期EMA vs 其他周期EMA

| 来源 | 立场 | 论据 | 页码 |
|------|------|------|------|
| **Brooks** | 固定20周期EMA | 20EMA在5分钟图上代表约100分钟（约1.5小时），适合日内趋势判断 | p.89多处引用 |
| **通用技术分析** | 灵活选择EMA周期 | 不同市场/时间框架需要不同周期 | — |

**裁决**：**Brooks的20周期EMA为标准默认值**
- 5分钟图：20EMA（标准）
- 15分钟图：20EMA仍适用（约5小时，适合波段）
- 1分钟图：建议使用50EMA（约50分钟，等效时间跨度）
- 日线图：20EMA仍为有效参考

## 5.3 冲突三：Dalton日型分类 vs Brooks趋势强度

| 来源 | 方法 | 特点 | 适用 |
|------|------|------|------|
| **Dalton** | 7种日型分类 | 基于TPO分布形状；偏定性 | 日级别策略选择 |
| **Brooks** | 趋势强度评分（0-100） | 基于价格行为特征；可量化 | 实时入场/出场决策 |

**裁决**：**互补使用**
- 日级别准备：使用Dalton日型分类决定当日策略框架
- 日内执行：使用Brooks趋势强度评分和入场结构执行
- Trend Day（Dalton）+ strength > 70（Brooks）= 全力顺势
- Nontrend Day（Dalton）+ strength < 30（Brooks）= 区间交易或观望

## 5.4 冲突四：Initiative vs Responsive 的定义差异

| 来源 | 定义 | 页码 |
|------|------|------|
| **Dalton** | Initiative = 突破VA向新区间运动；Responsive = VA内反向操作 | estimated p.40-45 |
| **其他MP文献** | Initiative = 主动建立新头寸；Responsive = 对价格极端做出反应 | — |

**裁决**：**以Dalton定义为标准**
- Dalton的定义更精确可操作（基于VA边界）
- 统一术语：
  - Initiative Buy = 收盘 > VAH + 维持
  - Initiative Sell = 收盘 < VAL + 维持
  - Responsive Buy = 价格跌破VAL后迅速回到VA内
  - Responsive Sell = 价格突破VAH后迅速回到VA内

## 5.5 冲突五：Brooks"只用一个时间周期" vs 多时间框架分析

| 来源 | 立场 | 论据 | 页码 |
|------|------|------|------|
| **Brooks** | 只用5分钟图 | 多周期信息矛盾导致决策瘫痪；5分钟足够捕捉所有结构 | p.50-52, p.74-76 |
| **通用做法** | 多时间框架 | 大周期定方向，小周期找入场 | — |

**裁决**：**Brooks的"单一周期"为核心原则，多周期仅作辅助确认**
- 主交易：仅使用一个时间周期（5分钟推荐）
- 辅助确认：可使用更大周期（15/60分钟）判断方向，但**不用于入场决策**
- 严禁同时使用1分钟和5分钟做交易决策（Brooks明确警告会导致亏损）

---

# 第六章：YAML索引卡

```yaml
# ============================================================
# Group 06 索引卡：Market Profile · 拍卖理论 · 价格行为
# ============================================================

group_id: "06"
group_name: "Market Profile · 拍卖理论 · 价格行为"
style: "可编程定义版（模式4）"
version: "1.0"
date_created: "2026-06-13"
date_updated: "2026-06-13"

# ------------------------------------------------------------
# 覆盖书目
# ------------------------------------------------------------
books:
  - id: "Dalton"
    title: "Mind over Markets（中文：心胜于市）"
    author: "James F. Dalton, Eric T. Jones, Robert B. Dalton"
    original: "Mind over Markets: Power Trading with Market Generated Information"
    role: "Market Profile理论体系：TPO/Value Area/日型分类"
    text_available: false
    note: "扫描版图片，页码基于目录结构estimated"
    key_chapters_estimated:
      - "Ch.2: Novice - TPO基础/日型分类 (p.7-29)"
      - "Ch.3: Advanced Beginner - 框架/OTF控制/平衡vs失衡 (p.33-57)"
      - "Ch.4: Competent - 日内交易/长期交易/特殊形态 (p.59-310)"
      - "Appendix: Value-Area Calculation (p.331-335)"

  - id: "Brooks"
    title: "日本蜡烛图交易技术分析"
    author: "Al Brooks（艾尔·布鲁克斯）"
    original: "Reading Price Charts Bar by Bar"
    role: "价格行为分析：趋势K/反转K/入场结构/趋势判断"
    text_available: true
    key_chapters:
      - "Ch.1: 价格行为 - 趋势K/十字星/信号K/反转K/吞没K (p.89-170)"
      - "Ch.2: 趋势线和通道 - 迷你趋势线/水平线/双线合璧 (p.371-410)"
      - "Ch.3: 趋势 - 两段走势/强弱信号/日型形态 (p.483-540)"
      - "Ch.4: 回调 - 初次回调/双底牛旗/EMA缺口/2HM (p.637-720)"

# ------------------------------------------------------------
# 对象清单
# ------------------------------------------------------------
objects:
  market_profile:
    - O1: "TPO（时间价格机会）"
    - O2: "Initial Balance（初始平衡）"
    - O3: "Value Area（价值区）"
    - O4: "POC（控制点）"
    - O5: "Balance vs Imbalance（平衡vs失衡）"
    - O6: "Day Type Classification（7种日型分类）"
    - O7: "OTF Control（Other Timeframe控制）"
    - O8: "Auction Rotation（拍卖轮换）"
    - O9: "3-1 Day"
    - O10: "Spike（尖峰）"
  
  price_action:
    - O11: "Trend Bar vs Doji（趋势K vs 十字星）"
    - O12: "Reversal Bar（反转K）"
    - O13: "Inside Bar / ii结构（孕线）"
    - O14: "Outside Bar / Engulfing（吞没K）"
    - O15: "Two-Legged Move（两段式走势）"
    - O16: "H2/L2（第二高点/第二低点）"
    - O17: "EMA Gap Bar（EMA缺口K线）"
    - O18: "2HM（2小时不触EMA）"
    - O19: "Double Bottom Bull Flag（双底牛旗）"
    - O20: "Final Flag（最后的旗形）"

# ------------------------------------------------------------
# 判定规则库
# ------------------------------------------------------------
rule_libraries:
  - "日型分类完整判定树（Dalton 7种日型）"
  - "开盘分类判定（Value内/外/Range外）"
  - "价格行为入场结构判定树（Brooks核心）"
  - "趋势强度评分算法（0-100量化）"

# ------------------------------------------------------------
# 适用边界
# ------------------------------------------------------------
boundaries:
  market_profile_limits:
    - "数据精度不足（无分钟级数据）"
    - "24小时市场无固定开盘"
    - "流动性不足（TPO稀疏）"
    - "单一事件驱动（新闻发布）"
    - "电子交易取代场内交易"
  
  price_action_limits:
    - "时间周期过短（1分钟噪声）"
    - "极端低波动（铁丝网形态）"
    - "极端高波动（黑天鹅）"
    - "横盘区间过窄（<5跳）"
    - "新闻发布时段"

# ------------------------------------------------------------
# 仓库标签映射
# ------------------------------------------------------------
tag_mapping:
  N02_session_or_time_window:
    - TPO周期 → session_intraday_period
    - 初始平衡 → opening_range
    - 日型分类 → session_regime_classifier
    - 3-1 Day → session_late_breakout
    - 2HM → session_trend_strength_indicator
    - 11:30陷阱 → session_midday_trap
    - Spike → session_impulse_event
    - Value Area → session_value_zone
    - 开盘分类 → opening_classification
  
  structure_price_action:
    - 趋势K/十字星 → structure_bar_classification
    - 反转K → structure_reversal_bar
    - 孕线 → structure_inside_bar_consolidation
    - 吞没K → structure_engulfing_bar
    - 两段式 → structure_two_legged_correction
    - H2/L2 → structure_second_entry
    - EMA缺口 → structure_ema_gap
    - 双底牛旗 → structure_flag_continuation
    - 最后旗形 → structure_final_flag_reversal
    - 趋势通道线 → structure_trend_channel_lines
    - 平衡/失衡 → structure_balance_imbalance

# ------------------------------------------------------------
# 跨书裁决
# ------------------------------------------------------------
cross_book_rulings:
  count: 5
  topics:
    - "TPO计数法 vs 成交量法：成交量法优先"
    - "20周期EMA为标准默认"
    - "Dalton日型 + Brooks强度：互补使用"
    - "Initiative/Responsive以Dalton定义为标准"
    - "单一交易周期为核心原则"

# ------------------------------------------------------------
# Tags
# ------------------------------------------------------------
tags:
  - "market_profile"
  - "price_action"
  - "pattern_definition"
  - "tpo"
  - "value_area"
  - "poc"
  - "initial_balance"
  - "day_type"
  - "balance_imbalance"
  - "auction_rotation"
  - "other_timeframe"
  - "responsive_initiative"
  - "trend_bar"
  - "doji"
  - "reversal_bar"
  - "inside_bar"
  - "ii_structure"
  - "engulfing"
  - "two_legged_move"
  - "h2_l2"
  - "ema_gap_bar"
  - "2hm"
  - "double_bottom_bull_flag"
  - "final_flag"
  - "trend_strength"
  - "spike"
  - "opening_range"
  - "session_analysis"
  - "programmable_definition"
  - "ohlcv_based"

# ------------------------------------------------------------
# 二次精读推荐
# ------------------------------------------------------------
second_reading_priority:
  highest:
    - book: "Brooks"
      chapters: ["Ch.1", "Ch.3"]
      reason: "第1章的K线分类和第3章的趋势判断是全书基础，需反复查阅"
    - book: "Dalton"
      chapters: ["Ch.4"]
      reason: "第四章的日内交易实战场景是MP的精华"

  high:
    - book: "Brooks"
      chapters: ["Ch.2", "Ch.4"]
      reason: "趋势线和回调结构是入场执行的关键"
    - book: "Dalton"
      chapters: ["Ch.2", "Ch.3"]
      reason: "日型分类和OTF控制是MP判断框架"

  medium:
    - book: "Dalton"
      chapters: ["Appendix"]
      reason: "Value Area计算公式的精确实现"

# ------------------------------------------------------------
# 文件清单
# ------------------------------------------------------------
files_in_group:
  - "GROUP_06_market_profile_price_action_DEFINITIONS.md"
```

---

> **Group 06 完成**
>
> 文件：`GROUP_06_market_profile_price_action_DEFINITIONS.md`
>
> 内容摘要：
> - **统一对象定义**：20个核心对象（Market Profile 10个 + 价格行为10个），每个均给出最小可实现定义（Python伪代码），优先基于OHLCV，需更细粒度数据时注明
> - **判定规则库**：4套完整判定树（日型分类/开盘分类/入场结构/趋势强度评分）
> - **适用边界**：Market Profile 6种失效场景 + 价格行为5种失效场景 + 两体系交叉边界表
> - **仓库标签映射**：N02_session_or_time_window（10项映射）+ structure_price_action（12项映射）
> - **跨书裁决**：5项冲突裁决（TPO vs 成交量/EMA周期/日型+强度/Initiative定义/单一周期原则）
> - **YAML索引卡**：完整索引
>
> **注释**：Dalton《Mind over Markets》为扫描版图片，无法提取文本。页码引用基于原书目录结构estimated。Brooks《日本蜡烛图交易技术分析》有完整文本提取，页码准确。
