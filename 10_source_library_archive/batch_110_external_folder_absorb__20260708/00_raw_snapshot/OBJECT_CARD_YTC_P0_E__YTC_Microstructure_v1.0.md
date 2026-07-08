# YTC_P0_E — YTC TST/BOF/BPB（微观结构陷阱）对象卡

> 功能层：P0_E（执行层 — 入场/出场/执行质量）  
> 成熟度：proxy_quantizable_now（只需 OHLCV，S/R 框架预定义后可用）  
> 生产者：Kimi  
> 来源：GLM_DELIVERY_07 蓝图 + YTC Price Action 素材 + 用户仓库 A1 组 CUTPACK  
> 状态：已冻结核心字段，待代码实现

---

## 1. 基本定义

YTC（Your Trading Coach，Lance Beggs）的 TST/BOF/BPB 是三种基于**支撑/阻力（S/R）框架**的微观结构信号。它们描述的是价格在关键水平（S/R）处的三种不同行为：

1. **TST（Test of Extremes）**：价格测试 S/R 极值后迅速收回，形成"假突破/假跌破"
2. **BOF（Breakout Failure）**：价格突破 S/R 后 1-3 根 K 线内回到原区间，突破失败
3. **BPB（Breakout Pullback）**：价格突破 S/R 后回调到突破区域，然后继续原方向，突破有效

**YTC 的核心前提**：这三个信号都依赖于**预定义的 S/R 框架**。YTC 要求交易者在观察信号前，先在图表上标记出：
- 大周期（HTF）的 S/R 区
- 中周期（TF）的 S/R 区
- 小周期（LF）的 S/R 区

**没有 S/R 框架，YTC 信号无效**。

---

## 2. 核心概念与字段冻结

### 2.1 S/R 框架字段（前置条件，已冻结）

```text
ytc_srf_htf_level       FLOAT   -- 大周期（Higher Time Frame）S/R 水平
ytc_srf_tf_level        FLOAT   -- 中周期（Time Frame）S/R 水平
ytc_srf_lf_level        FLOAT   -- 小周期（Lower Time Frame）S/R 水平
ytc_srf_zone_width      FLOAT   -- S/R 区的宽度（上下缓冲），通常 = 0.5 × ATR
ytc_srf_is_valid        BOOL    -- S/R 框架是否有效（至少标记了 2 个周期的水平）
                                  -- 若只有 1 个周期或没有 → 所有 YTC 信号无效
ytc_srf_type            ENUM    -- 当前测试的 S/R 类型：
                                  -- 'RESISTANCE' = 阻力位（前高/供给区）
                                  -- 'SUPPORT' = 支撑位（前低/需求区）
                                  -- 'CONGESTION_HIGH' = 震荡区间上沿
                                  -- 'CONGESTION_LOW' = 震荡区间下沿
```

### 2.2 测试行为字段（已冻结）

```text
ytc_test_price          FLOAT   -- 测试价格（突破/测试时的极值价格）
ytc_test_bar_idx        INT     -- 测试发生的 K 线索引
ytc_test_bar_body_pct   FLOAT   -- 测试 K 线的实体比例（0.0-1.0）
ytc_test_volume_ratio   FLOAT   -- 测试 K 线成交量 / 前 20 根平均成交量
ytc_retrace_price       FLOAT   -- 测试后回撤价格（回到 S/R 区域内的价格）
ytc_retrace_bar_idx     INT     -- 回撤发生的 K 线索引
ytc_retrace_speed       FLOAT   -- 回撤速度 = 测试极值到回撤价格的距离 / 回撤 K 线数
                                  -- 快速回撤（< 2 根 K 线）= 强信号
                                  -- 慢速回撤（> 5 根 K 线）= 弱信号，可能不是 TST/BOF
```

### 2.3 三种信号判定字段（已冻结）

```text
ytc_signal_type         ENUM    -- YTC 信号类型：
                                  -- 'NONE' = 无信号
                                  -- 'TST_LONG' = 测试极值后做多（假跌破支撑）
                                  -- 'TST_SHORT' = 测试极值后做空（假突破阻力）
                                  -- 'BOF_LONG' = 突破失败做多（下破后收回）
                                  -- 'BOF_SHORT' = 突破失败做空（上破后收回）
                                  -- 'BPB_LONG' = 突破回测做多（有效突破后回调）
                                  -- 'BPB_SHORT' = 突破回测做空（有效下破后反弹）
                                  -- 'WAITING_CONFIRM' = 等待后续 K 线确认
                                  -- 'ABORTED' = 信号被取消（如过长时间未确认）
ytc_signal_subtype      ENUM    -- 信号子类型（更精确的分类）：
                                  -- 'TST_SWING_HIGH' = 测试前高（阻力）
                                  -- 'TST_SWING_LOW' = 测试前低（支撑）
                                  -- 'TST_CONGESTION' = 测试震荡区间边界
                                  -- 'BOF_WEAK' = 弱突破失败（1-2 根 K 线内收回）
                                  -- 'BOF_STRONG' = 强突破失败（3+ 根 K 线后收回）
                                  -- 'BPB_SHALLOW' = 浅回测（< 38.2% 突破范围）
                                  -- 'BPB_DEEP' = 深回测（38.2%-61.8% 突破范围）
ytc_confirmation_count  INT     -- 确认信号需要的后续 K 线数量：
                                  -- TST = 1 根确认（测试后迅速收回）
                                  -- BOF = 2-3 根确认（突破后回到原区间）
                                  -- BPB = 2-3 根确认（回调后重新突破）
ytc_confirmation_status ENUM    -- 确认状态：
                                  -- 'PENDING' = 等待确认
                                  -- 'CONFIRMED' = 已确认，信号有效
                                  -- 'FAILED' = 确认失败，信号取消
                                  -- 'EXPIRED' = 超时未确认（超过 5 根 K 线）
```

### 2.4 信号质量与执行字段（已冻结）

```text
ytc_signal_quality      ENUM    -- 信号质量：
                                  -- 'A_PLUS' = 多周期 S/R 共振 + 放量 + 快速回撤
                                  -- 'A' = 多周期 S/R 共振 + 正常量
                                  -- 'B' = 单周期 S/R + 放量
                                  -- 'C' = 单周期 S/R + 缩量（可交易但谨慎）
                                  -- 'D' = 多周期 S/R 冲突或缩量严重（不推荐）
ytc_signal_strength     INT(0-10)   -- 信号强度（基于 quality + 确认速度 + 成交量）
ytc_trigger_bar_idx     INT     -- 触发信号的 K 线索引（用于回溯验证）
ytc_entry_zone_high     FLOAT   -- 建议入场区上沿（S/R 水平 + 缓冲）
ytc_entry_zone_low      FLOAT   -- 建议入场区下沿（S/R 水平 - 缓冲）
ytc_stop_loss_price     FLOAT   -- 建议止损：
                                  -- TST/BOF：测试极值另一侧 + ATR 缓冲
                                  -- BPB：回调极值另一侧 + ATR 缓冲
ytc_target_price_1      FLOAT   -- 第一目标（1:1 风险报酬）
ytc_target_price_2      FLOAT   -- 第二目标（1:2 风险报酬）
ytc_target_price_3      FLOAT   -- 第三目标（基于前高/前低的扩展）
ytc_integer_level_s_r   BOOL    -- 整数关口 S/R 敏感度（A股特有）：
                                     -- True = 自动检测价格整数位（10, 20, 30...）作为额外 S/R 水平
                                     -- A股散户心理价位产生强 S/R，比外盘更明显
                                     -- 整数位测试视为额外一层 S/R 验证
                                     -- 仅当 price >= 10 时生效（低价股整数位意义不大）
ytc_astock_period_limit   ENUM    -- A股周期限制：
                                     -- 'daily_weekly' = 只用于日线/周线级别（默认，T+1 安全）
                                     -- 'all' = 允许所有周期（不推荐，日内 TST 因 T+1 风险极高）
```

---

## 3. 计算逻辑（伪代码）

### 3.1 S/R 框架检测（前置）

```python
def detect_sr_framework(ohlcv_df, higher_tf_ohlcv=None, lookback=30):
    """
    检测 S/R 框架（基于最近的价格极值和震荡区间）
    
    参数:
        ohlcv_df: 当前周期 DataFrame
        higher_tf_ohlcv: 大周期 DataFrame（可选，用于 HTF S/R）
        lookback: 回溯窗口
    
    返回:
        dict with S/R levels and validity
    """
    recent = ohlcv_df.tail(lookback)
    
    # 1. 检测最近的价格极值（摆动高点/低点）
    swing_highs = []
    swing_lows = []
    
    for i in range(2, len(recent) - 2):
        # 摆动高点：中间 K 线高于两侧各 2 根
        if (recent['high'].iloc[i] > recent['high'].iloc[i-1] and 
            recent['high'].iloc[i] > recent['high'].iloc[i-2] and
            recent['high'].iloc[i] > recent['high'].iloc[i+1] and
            recent['high'].iloc[i] > recent['high'].iloc[i+2]):
            swing_highs.append({'idx': i, 'price': recent['high'].iloc[i]})
        
        # 摆动低点
        if (recent['low'].iloc[i] < recent['low'].iloc[i-1] and 
            recent['low'].iloc[i] < recent['low'].iloc[i-2] and
            recent['low'].iloc[i] < recent['low'].iloc[i+1] and
            recent['low'].iloc[i] < recent['low'].iloc[i+2]):
            swing_lows.append({'idx': i, 'price': recent['low'].iloc[i]})
    
    # 2. 检测震荡区间（Congestion）
    # 简化：如果价格在最近 lookback/2 根 K 线内，高低点范围 < 2×ATR，视为震荡
    atr_14 = calculate_atr(ohlcv_df, 14)
    recent_half = recent.tail(lookback // 2)
    congestion_range = recent_half['high'].max() - recent_half['low'].min()
    
    is_congestion = congestion_range < 2 * atr_14.iloc[-1]
    
    # 3. 构建 S/R 水平
    sr_levels = []
    
    if len(swing_highs) >= 2:
        sr_levels.append({'type': 'RESISTANCE', 'price': max(sh['price'] for sh in swing_highs[-2:])})
    
    if len(swing_lows) >= 2:
        sr_levels.append({'type': 'SUPPORT', 'price': min(sl['price'] for sl in swing_lows[-2:])})
    
    if is_congestion:
        sr_levels.append({'type': 'CONGESTION_HIGH', 'price': recent_half['high'].max()})
        sr_levels.append({'type': 'CONGESTION_LOW', 'price': recent_half['low'].min()})
    
    # 4. HTF S/R（如果提供了大周期数据）
    htf_sr = None
    if higher_tf_ohlcv is not None:
        htf_recent = higher_tf_ohlcv.tail(10)
        htf_sr = {
            'high': htf_recent['high'].max(),
            'low': htf_recent['low'].min(),
        }
    
    # 5. 验证 S/R 框架有效性
    is_valid = len(sr_levels) >= 2 or htf_sr is not None
    
    return {
        'ytc_srf_htf_level': htf_sr['high'] if htf_sr else None,
        'ytc_srf_tf_level': sr_levels[0]['price'] if sr_levels else None,
        'ytc_srf_lf_level': sr_levels[1]['price'] if len(sr_levels) > 1 else None,
        'ytc_srf_zone_width': atr_14.iloc[-1] * 0.5,
        'ytc_srf_is_valid': is_valid,
        'ytc_srf_type': sr_levels[0]['type'] if sr_levels else 'NONE',
    }
```

### 3.2 TST（Test of Extremes）检测

```python
def detect_tst(ohlcv_df, sr_framework, current_bar_idx):
    """
    检测 TST（测试极值）信号
    
    TST 定义：
    - 价格测试 S/R 极值（前高/前低/震荡边界）
    - 测试后 1-2 根 K 线内迅速回到 S/R 区域内部
    - 测试 K 线通常有长影线（上影线或下影线），实体小
    
    返回：
        dict with signal or None
    """
    if not sr_framework['ytc_srf_is_valid']:
        return None
    
    current_bar = ohlcv_df.iloc[current_bar_idx]
    prev_bar = ohlcv_df.iloc[current_bar_idx - 1]
    
    # 获取当前测试的 S/R 水平
    sr_level = sr_framework['ytc_srf_tf_level']
    sr_type = sr_framework['ytc_srf_type']
    zone_width = sr_framework['ytc_srf_zone_width']
    
    # 1. 测试阻力位（TST_SHORT）
    if sr_type in ['RESISTANCE', 'CONGESTION_HIGH']:
        # 测试条件：当前 K 线高点突破 S/R 水平，但收盘价回到 S/R 区域内
        if current_bar['high'] > sr_level + zone_width and current_bar['close'] < sr_level + zone_width:
            # 检查上影线长度
            upper_shadow = current_bar['high'] - max(current_bar['open'], current_bar['close'])
            body = abs(current_bar['close'] - current_bar['open'])
            
            if upper_shadow > body * 2:  # 上影线至少是实体的 2 倍
                return {
                    'ytc_signal_type': 'TST_SHORT',
                    'ytc_signal_subtype': 'TST_SWING_HIGH' if sr_type == 'RESISTANCE' else 'TST_CONGESTION',
                    'ytc_test_price': current_bar['high'],
                    'ytc_test_bar_idx': current_bar_idx,
                    'ytc_test_bar_body_pct': round(body / (current_bar['high'] - current_bar['low']), 2) if (current_bar['high'] - current_bar['low']) > 0 else 0,
                    'ytc_retrace_price': current_bar['close'],
                    'ytc_retrace_bar_idx': current_bar_idx,  # TST 是同一根 K 线内收回
                    'ytc_retrace_speed': upper_shadow,  # 上影线长度 = 回撤幅度
                    'ytc_signal_quality': 'A' if current_bar['volume'] > ohlcv_df['volume'].tail(20).mean() * 1.5 else 'B',
                    'ytc_signal_strength': 8 if current_bar['volume'] > ohlcv_df['volume'].tail(20).mean() * 1.5 else 6,
                    'ytc_entry_zone_high': sr_level + zone_width,
                    'ytc_entry_zone_low': sr_level - zone_width,
                    'ytc_stop_loss_price': current_bar['high'] + zone_width,
                    'ytc_target_price_1': sr_level - (current_bar['high'] - sr_level) * 1,
                    'ytc_target_price_2': sr_level - (current_bar['high'] - sr_level) * 2,
                }
    
    # 2. 测试支撑位（TST_LONG）
    elif sr_type in ['SUPPORT', 'CONGESTION_LOW']:
        if current_bar['low'] < sr_level - zone_width and current_bar['close'] > sr_level - zone_width:
            lower_shadow = min(current_bar['open'], current_bar['close']) - current_bar['low']
            body = abs(current_bar['close'] - current_bar['open'])
            
            if lower_shadow > body * 2:
                return {
                    'ytc_signal_type': 'TST_LONG',
                    'ytc_signal_subtype': 'TST_SWING_LOW' if sr_type == 'SUPPORT' else 'TST_CONGESTION',
                    'ytc_test_price': current_bar['low'],
                    'ytc_test_bar_idx': current_bar_idx,
                    'ytc_test_bar_body_pct': round(body / (current_bar['high'] - current_bar['low']), 2) if (current_bar['high'] - current_bar['low']) > 0 else 0,
                    'ytc_retrace_price': current_bar['close'],
                    'ytc_retrace_bar_idx': current_bar_idx,
                    'ytc_retrace_speed': lower_shadow,
                    'ytc_signal_quality': 'A' if current_bar['volume'] > ohlcv_df['volume'].tail(20).mean() * 1.5 else 'B',
                    'ytc_signal_strength': 8 if current_bar['volume'] > ohlcv_df['volume'].tail(20).mean() * 1.5 else 6,
                    'ytc_entry_zone_high': sr_level + zone_width,
                    'ytc_entry_zone_low': sr_level - zone_width,
                    'ytc_stop_loss_price': current_bar['low'] - zone_width,
                    'ytc_target_price_1': sr_level + (sr_level - current_bar['low']) * 1,
                    'ytc_target_price_2': sr_level + (sr_level - current_bar['low']) * 2,
                }
    
    return None
```

### 3.3 BOF（Breakout Failure）检测

```python
def detect_bof(ohlcv_df, sr_framework, breakout_bar_idx, current_bar_idx):
    """
    检测 BOF（突破失败）信号
    
    BOF 定义：
    - 价格突破 S/R 水平（收盘价在 S/R 区域外）
    - 突破后 2-3 根 K 线内，收盘价回到 S/R 区域内
    
    参数:
        breakout_bar_idx: 突破发生的 K 线索引
        current_bar_idx: 当前 K 线索引（用于判断突破后是否回到原区间）
    
    返回:
        dict with signal or None
    """
    if not sr_framework['ytc_srf_is_valid']:
        return None
    
    sr_level = sr_framework['ytc_srf_tf_level']
    sr_type = sr_framework['ytc_srf_type']
    zone_width = sr_framework['ytc_srf_zone_width']
    
    breakout_bar = ohlcv_df.iloc[breakout_bar_idx]
    post_breakout = ohlcv_df.iloc[breakout_bar_idx + 1:current_bar_idx + 1]
    
    if len(post_breakout) < 2 or len(post_breakout) > 5:  # BOF 需要在 2-5 根 K 线内确认
        return None
    
    # 1. 向上突破后的 BOF（做空）
    if sr_type in ['RESISTANCE', 'CONGESTION_HIGH']:
        # 突破条件：收盘价在阻力上方
        if breakout_bar['close'] > sr_level + zone_width:
            # 检查后续 K 线是否回到阻力下方
            for idx, bar in post_breakout.iterrows():
                if bar['close'] < sr_level - zone_width:  # 回到 S/R 区域内部（甚至下方）
                    bof_speed = idx - breakout_bar_idx
                    return {
                        'ytc_signal_type': 'BOF_SHORT',
                        'ytc_signal_subtype': 'BOF_STRONG' if bof_speed >= 3 else 'BOF_WEAK',
                        'ytc_test_price': breakout_bar['high'],
                        'ytc_test_bar_idx': breakout_bar_idx,
                        'ytc_retrace_price': bar['close'],
                        'ytc_retrace_bar_idx': idx,
                        'ytc_retrace_speed': bof_speed,
                        'ytc_confirmation_count': bof_speed,
                        'ytc_confirmation_status': 'CONFIRMED',
                        'ytc_signal_quality': 'A' if bof_speed <= 2 else 'B',
                        'ytc_signal_strength': 9 if bof_speed <= 2 else 7,
                        'ytc_entry_zone_high': sr_level + zone_width,
                        'ytc_entry_zone_low': sr_level - zone_width,
                        'ytc_stop_loss_price': breakout_bar['high'] + zone_width,
                        'ytc_target_price_1': sr_level - (breakout_bar['high'] - sr_level) * 1.5,
                        'ytc_target_price_2': sr_level - (breakout_bar['high'] - sr_level) * 2.5,
                    }
    
    # 2. 向下突破后的 BOF（做多）
    elif sr_type in ['SUPPORT', 'CONGESTION_LOW']:
        if breakout_bar['close'] < sr_level - zone_width:
            for idx, bar in post_breakout.iterrows():
                if bar['close'] > sr_level + zone_width:
                    bof_speed = idx - breakout_bar_idx
                    return {
                        'ytc_signal_type': 'BOF_LONG',
                        'ytc_signal_subtype': 'BOF_STRONG' if bof_speed >= 3 else 'BOF_WEAK',
                        'ytc_test_price': breakout_bar['low'],
                        'ytc_test_bar_idx': breakout_bar_idx,
                        'ytc_retrace_price': bar['close'],
                        'ytc_retrace_bar_idx': idx,
                        'ytc_retrace_speed': bof_speed,
                        'ytc_confirmation_count': bof_speed,
                        'ytc_confirmation_status': 'CONFIRMED',
                        'ytc_signal_quality': 'A' if bof_speed <= 2 else 'B',
                        'ytc_signal_strength': 9 if bof_speed <= 2 else 7,
                        'ytc_entry_zone_high': sr_level + zone_width,
                        'ytc_entry_zone_low': sr_level - zone_width,
                        'ytc_stop_loss_price': breakout_bar['low'] - zone_width,
                        'ytc_target_price_1': sr_level + (sr_level - breakout_bar['low']) * 1.5,
                        'ytc_target_price_2': sr_level + (sr_level - breakout_bar['low']) * 2.5,
                    }
    
    # 3. 超时检测
    if len(post_breakout) >= 5:
        return {'ytc_confirmation_status': 'EXPIRED'}
    
    return {'ytc_confirmation_status': 'PENDING'}
```

### 3.4 BPB（Breakout Pullback）检测

```python
def detect_bpb(ohlcv_df, sr_framework, breakout_bar_idx, current_bar_idx):
    """
    检测 BPB（突破回测）信号
    
    BPB 定义：
    - 价格突破 S/R 水平（收盘价在 S/R 区域外）
    - 突破后回调到 S/R 区域附近（但不回到区域内）
    - 回调结束后价格继续原方向（重新突破）
    
    参数:
        breakout_bar_idx: 突破发生的 K 线索引
        current_bar_idx: 当前 K 线索引
    
    返回:
        dict with signal or None
    """
    if not sr_framework['ytc_srf_is_valid']:
        return None
    
    sr_level = sr_framework['ytc_srf_tf_level']
    sr_type = sr_framework['ytc_srf_type']
    zone_width = sr_framework['ytc_srf_zone_width']
    
    breakout_bar = ohlcv_df.iloc[breakout_bar_idx]
    post_breakout = ohlcv_df.iloc[breakout_bar_idx + 1:current_bar_idx + 1]
    
    if len(post_breakout) < 2:
        return {'ytc_confirmation_status': 'PENDING'}
    
    # 1. 向上突破后的 BPB（做多）
    if sr_type in ['RESISTANCE', 'CONGESTION_HIGH']:
        if breakout_bar['close'] > sr_level + zone_width:
            # 检测回调：价格在突破后下降，但保持在 S/R 水平上方
            pullback_low = breakout_bar['close']
            pullback_low_idx = breakout_bar_idx
            
            for idx, bar in post_breakout.iterrows():
                if bar['low'] < pullback_low:
                    pullback_low = bar['low']
                    pullback_low_idx = idx
                
                # 检查是否回到 S/R 区域内（即回调过深）
                if bar['close'] < sr_level - zone_width:
                    return {'ytc_signal_type': 'BOF_SHORT', 'ytc_confirmation_status': 'CONFIRMED'}  # 变成 BOF
                
                # 检查回调后是否重新突破
                if idx > pullback_low_idx and bar['close'] > breakout_bar['close']:
                    # 回调深度计算
                    breakout_range = breakout_bar['high'] - breakout_bar['low']
                    pullback_depth = breakout_bar['close'] - pullback_low
                    depth_ratio = pullback_depth / breakout_range if breakout_range > 0 else 0
                    
                    if depth_ratio < 0.382:
                        subtype = 'BPB_SHALLOW'
                        quality = 'A_PLUS'
                        strength = 10
                    elif depth_ratio < 0.618:
                        subtype = 'BPB_DEEP'
                        quality = 'B'
                        strength = 6
                    else:
                        return None  # 太深，不交易
                    
                    return {
                        'ytc_signal_type': 'BPB_LONG',
                        'ytc_signal_subtype': subtype,
                        'ytc_test_price': breakout_bar['high'],
                        'ytc_test_bar_idx': breakout_bar_idx,
                        'ytc_retrace_price': pullback_low,
                        'ytc_retrace_bar_idx': pullback_low_idx,
                        'ytc_retrace_speed': idx - pullback_low_idx,
                        'ytc_confirmation_count': idx - breakout_bar_idx,
                        'ytc_confirmation_status': 'CONFIRMED',
                        'ytc_signal_quality': quality,
                        'ytc_signal_strength': strength,
                        'ytc_entry_zone_high': breakout_bar['close'] + zone_width,
                        'ytc_entry_zone_low': pullback_low - zone_width,
                        'ytc_stop_loss_price': pullback_low - zone_width,
                        'ytc_target_price_1': breakout_bar['close'] + (breakout_bar['close'] - pullback_low) * 1,
                        'ytc_target_price_2': breakout_bar['close'] + (breakout_bar['close'] - pullback_low) * 2,
                        'ytc_target_price_3': breakout_bar['close'] + (breakout_bar['close'] - pullback_low) * 3,
                    }
    
    # 2. 向下突破后的 BPB（做空）
    elif sr_type in ['SUPPORT', 'CONGESTION_LOW']:
        if breakout_bar['close'] < sr_level - zone_width:
            pullback_high = breakout_bar['close']
            pullback_high_idx = breakout_bar_idx
            
            for idx, bar in post_breakout.iterrows():
                if bar['high'] > pullback_high:
                    pullback_high = bar['high']
                    pullback_high_idx = idx
                
                if bar['close'] > sr_level + zone_width:
                    return {'ytc_signal_type': 'BOF_LONG', 'ytc_confirmation_status': 'CONFIRMED'}
                
                if idx > pullback_high_idx and bar['close'] < breakout_bar['close']:
                    breakout_range = breakout_bar['high'] - breakout_bar['low']
                    pullback_depth = pullback_high - breakout_bar['close']
                    depth_ratio = pullback_depth / breakout_range if breakout_range > 0 else 0
                    
                    if depth_ratio < 0.382:
                        subtype = 'BPB_SHALLOW'
                        quality = 'A_PLUS'
                        strength = 10
                    elif depth_ratio < 0.618:
                        subtype = 'BPB_DEEP'
                        quality = 'B'
                        strength = 6
                    else:
                        return None
                    
                    return {
                        'ytc_signal_type': 'BPB_SHORT',
                        'ytc_signal_subtype': subtype,
                        'ytc_test_price': breakout_bar['low'],
                        'ytc_test_bar_idx': breakout_bar_idx,
                        'ytc_retrace_price': pullback_high,
                        'ytc_retrace_bar_idx': pullback_high_idx,
                        'ytc_retrace_speed': idx - pullback_high_idx,
                        'ytc_confirmation_count': idx - breakout_bar_idx,
                        'ytc_confirmation_status': 'CONFIRMED',
                        'ytc_signal_quality': quality,
                        'ytc_signal_strength': strength,
                        'ytc_entry_zone_high': pullback_high + zone_width,
                        'ytc_entry_zone_low': breakout_bar['close'] - zone_width,
                        'ytc_stop_loss_price': pullback_high + zone_width,
                        'ytc_target_price_1': breakout_bar['close'] - (pullback_high - breakout_bar['close']) * 1,
                        'ytc_target_price_2': breakout_bar['close'] - (pullback_high - breakout_bar['close']) * 2,
                        'ytc_target_price_3': breakout_bar['close'] - (pullback_high - breakout_bar['close']) * 3,
                    }
    
    # 3. 超时检测
    if len(post_breakout) >= 10:
        return {'ytc_confirmation_status': 'EXPIRED'}
    
    return {'ytc_confirmation_status': 'PENDING'}
```

---

## 4. 与现有指标的互锁逻辑（已冻结）

### 4.1 与 KD MTF 的互锁（已冻结）

```text
互锁规则 YTC × KD MTF：

1. YTC 信号方向与 KD MTF 的对齐：
   - YTC_LONG（TST_LONG/BOF_LONG/BPB_LONG）需要 kd_day_signal = 'bullish'
   - YTC_SHORT（TST_SHORT/BOF_SHORT/BPB_SHORT）需要 kd_day_signal = 'bearish'
   - 若 kd_day_signal = 'neutral' → YTC 信号降级为 'WAITING_CONFIRM'（方向不明）

2. KD 极端区对 YTC 的过滤：
   - kd_week_extreme_zone = 'overbought' → TST_SHORT/BOF_SHORT 信号强度 +2（极端区假突破/测试更可靠）
   - kd_week_extreme_zone = 'oversold' → TST_LONG/BOF_LONG 信号强度 +2
   - kd_week_extreme_zone = 'overbought' → BPB_LONG 禁止（追高风险）
   - kd_week_extreme_zone = 'oversold' → BPB_SHORT 禁止（杀跌风险）

3. KD 锁仓状态对 YTC 的影响：
   - lock_signal = 'locked' → YTC 信号正常执行
   - lock_signal = 'unlocked' → YTC 信号只作为参考，不触发实际入场（confirmation_status = 'PENDING'）
   - lock_signal = 'conflicting' → YTC 信号无效

4. KD 多周期对齐对 YTC 质量的影响：
   - kd_alignment_tier = 'strong' → ytc_signal_quality 提升一级（如 B→A）
   - kd_alignment_tier = 'weak' → ytc_signal_quality 降级一级（如 A→B）
   - kd_alignment_tier = 'conflict' → YTC 信号无效（方向不一致，S/R 测试可能失败）
```

### 4.2 与 Volty 的互锁（已冻结）

```text
互锁规则 YTC × VOLTY：

1. 波动率对 YTC 信号的影响：
   - volty_trend_state = 'expansion' → TST/BOF 更可靠（高波动期假突破/测试频繁），但 BPB 需谨慎（回调可能过深）
   - volty_trend_state = 'contraction' → BPB 更可靠（低波动后的突破更真实），但 TST/BOF 减少（波动小，测试少）
   - volty_trend_state = 'trending' → 正常处理

2. Volty 止损与 YTC 的协同：
   - YTC 的止损位（ytc_stop_loss_price）与 volty_up_stop/volty_dn_stop 比较：
     - 若 YTC 止损在 Volty 止损更保守的一侧 → 使用 YTC 止损
     - 若 YTC 止损在 Volty 止损之外 → 使用 Volty 止损（更保守）

3. Volty 翻转与 YTC 的冲突：
   - volty_flip_signal = 'bullish_flip' 且 ytc_signal_type = 'TST_SHORT/BOF_SHORT' → 共振！翻转确认 + 假突破做空
   - volty_flip_signal = 'bearish_flip' 且 ytc_signal_type = 'TST_LONG/BOF_LONG' → 共振！翻转确认 + 假跌破做多
   - volty_flip_signal 与 ytc_signal_type 方向冲突 → 以 Volty 为准（实时信号优先）
```

### 4.3 与 Volume Profile 的互锁（已冻结）

```text
互锁规则 YTC × VP：

1. VP 对 S/R 框架的增强：
   - VP 的 HVN（高成交量节点）可作为 YTC S/R 框架的"天然水平"：
     - 若 S/R 水平与 VP HVN 重合 → 该水平可靠性极高，YTC 信号质量提升一级
     - 若 S/R 水平与 VP LVN（低成交量节点）重合 → 该水平可能不可靠，YTC 信号质量降级

2. VP 对突破/回调的过滤：
   - 突破发生在 VP 的 LVN 区域 → 突破可能快速运行（无阻力），TST/BOF 可能减少，BPB 回调浅
   - 突破发生在 VP 的 HVN 区域 → 突破遇到阻力，TST/BOF 增加，BPB 回调深
   - 价格回到 VP POC（控制点）+ YTC TST/BOF → 高概率反转（"公平价格" + 假突破）

3. VP 多周期对 YTC 的确认：
   - 日线 VP 显示 S/R 水平是长期 HVN → YTC 信号质量 = 'A_PLUS'
   - 日线 VP 显示 S/R 水平是长期 LVN → YTC 信号质量降级（可能不是真正的 S/R）
```

### 4.4 与缠论 BSD 的互锁（已冻结）

```text
互锁规则 YTC × CHZL_BSD：

1. 缠论趋势类型与 YTC 的激活：
   - chzl_trend_type = 'TREND_UP' → 激活 YTC_LONG 信号（BPB_LONG, TST_LONG, BOF_LONG）
   - chzl_trend_type = 'TREND_DOWN' → 激活 YTC_SHORT 信号
   - chzl_trend_type = 'CONSOLIDATION' → YTC 信号活跃（震荡市中 TST/BOF 最频繁）

2. BSD 与 YTC 的共振：
   - BSD 1Buy（趋势反转）+ YTC BOF_LONG（假突破后做多）→ 共振！
     - 1Buy 提供结构反转，BOF_LONG 提供入场时机（假突破后的低点买入）
   - BSD 1Sell + YTC BOF_SHORT → 同理共振
   - BSD 2Buy/3Buy + YTC BPB_LONG → 结构确认 + 入场时机

3. BSD 与 YTC 的冲突：
   - BSD 3Buy（离开中枢）+ YTC BOF_LONG（假突破）→ 冲突！3Buy 是做多信号，BOF_LONG 也是做多，不冲突
   - 实际上 BSD 与 YTC 很少冲突，因为 BSD 是"结构信号"，YTC 是"执行时机"
   - 真正的冲突：BSD 1Buy + YTC TST_SHORT（假突破阻力做空）→ 方向完全相反
     - 处理方式：以 BSD 为准（结构反转信号优先级高于 S/R 测试）
```

### 4.5 与 Brooks BPB 的互锁（已冻结）

```text
互锁规则 YTC × BROOKS_BPB：

1. YTC 与 Brooks BPB 的功能重叠：
   - YTC BPB 和 Brooks BPB 都是"突破回调"模式，但定义不同：
     - YTC BPB：基于 S/R 框架，回调回到 S/R 区域附近（但不回到区域内）
     - Brooks BPB：基于趋势线突破，回调基于 K 线形态和百分比深度
   - 两者同时出现时 → 信号共振，质量提升

2. 优先级规则：
   - 若 YTC BPB 和 Brooks BPB 同时出现 → 取更保守的止损（两者中更远离当前价的那个）
   - 若 YTC 信号为 TST/BOF，而 Brooks 信号为 BPB → 以 YTC 为准（TST/BOF 是更即时的信号）

3. 回调深度的比较：
   - YTC BPB 的深度基于 S/R 区域（ytc_srf_zone_width）
   - Brooks BPB 的深度基于突破 K 线实体（bpb_pullback_depth_ratio）
   - 两者深度不一致时 → 标记为 'MIXED_SIGNAL'，降低仓位
```

---

## 5. 失效模式（已冻结）

```text
YTC 失效条件：

1. S/R 框架无效：
   - ytc_srf_is_valid = False → 所有 YTC 信号无效
   - 这是 YTC 的"根基"：没有 S/R 框架，就没有信号

2. 无确认：
   - ytc_confirmation_status = 'EXPIRED' → 信号超时（TST 需 1-2 根，BOF 需 2-5 根，BPB 需 2-10 根）
   - 超过确认窗口后，信号自动取消

3. 多周期 S/R 冲突：
   - HTF S/R 与 TF S/R 方向冲突（如 HTF 是阻力，TF 是支撑）→ 信号质量降级为 'D'，不推荐交易
   - 处理方式：以大周期（HTF）为准，小周期信号仅作为观察

4. 震荡市中信号过多：
   - chzl_trend_type = 'CONSOLIDATION' 或 kd_alignment_tier = 'conflict' → YTC TST/BOF 频繁出现，但成功率下降
   - 应对：震荡市中只交易 A+ 质量的信号，或完全禁用 YTC

5. 与主要指标冲突：
   - YTC 信号与 KD MTF 方向冲突 → 以 KD 为准
   - YTC 信号与 Volty flip 冲突 → 以 Volty 为准
   - YTC 信号与缠论 BSD 结构冲突 → 以 BSD 为准

6. A 股特殊失效：
   - 涨停/跌停导致 S/R 水平被价格限制扭曲 → S/R 框架可能失效
   - 集合竞价跳空导致 S/R 测试不是"真实"测试（而是跳空）→ 跳过集合竞价后的第一根 K 线
   - 散户在整数关口的假突破 → 需要 VP 过滤确认
```

---

## 6. A 股特殊适配（已冻结）

```text
A 股 YTC 适配规则：

1. 涨停/跌停影响：
   - limit_up = True → 价格无法继续上涨，YTC_SHORT 信号（TST/BOF）可能失效（不是真实测试，是价格限制）
   - limit_down = True → YTC_LONG 信号可能失效
   - 应对：涨跌停日不生成 YTC 信号（标记为 'market_halt'）

2. 集合竞价跳空：
   - 开盘跳空突破前高 → 这不是 YTC 定义的"测试"（没有盘中价格运动）
   - 应对：跳空突破的 YTC 信号需要等待至少 3 根盘中 K 线确认
   - 跳空跌破前低 → 同理，等待盘中确认

3. T+1 影响：
   - YTC 信号一旦触发，当日无法出场
   - TST/BOF 是"快速反转"信号，T+1 限制其有效性（因为无法当日止损）
   - 建议：A 股 YTC 只用于日线/周线级别（留有足够时间窗口）
   - 或：YTC 用于 ETF/指数（波动相对较小，T+1 影响可接受）

4. 整数关口影响：
   - A 股散户在整数关口（10, 20, 30...）大量交易，形成"心理 S/R"
   - 但这种 S/R 不是基于历史价格行为，而是基于心理
   - 应对：整数关口的 YTC 信号需要额外验证（如 VP 显示该关口也是 HVN）

5. 小盘股流动性问题：
   - 小盘股单笔大单可能导致"假突破"（价格瞬间突破 S/R 然后回落）
   - 应对：小盘股 YTC 信号要求成交量确认（测试 K 线成交量 > 均值 1.5 倍）

6. 多周期 S/R 的特殊处理：
   - A 股日内波动大，小周期（5min/15min）S/R 频繁变化
   - 建议：A 股 YTC 以日线 S/R 为主，日内 S/R 仅作为辅助确认
```

---

## 7. 成熟度与数据需求

| 维度 | 评估 |
|------|------|
| **所需数据** | OHLCV（已有）+ 多周期 OHLCV（用于 HTF S/R） |
| **计算复杂度** | 中（需要 S/R 框架检测 + 突破/回调追踪） |
| **实时性能** | 每根 K 线更新，需要维护状态（确认计数） |
| **回测可行性** | 高（需预定义 S/R 框架，可自动检测） |
| **A 股落地** | 可直接落地（需处理跳空/整数关口/小盘股） |
| **外汇/期货/币圈落地** | 直接可用（无限制） |
| **跨周期** | 必须多周期（HTF/TF/LF 是核心前提） |

---

> 文件：OBJECT_CARD_YTC_P0_E__YTC_Microstructure_v1.0.md  
> 生产者：Kimi  
> 状态：字段已冻结，待代码实现
