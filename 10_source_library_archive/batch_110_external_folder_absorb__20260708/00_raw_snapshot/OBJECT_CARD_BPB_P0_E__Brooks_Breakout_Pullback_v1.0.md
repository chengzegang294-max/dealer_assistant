# BPB_P0_E — Brooks Breakout Pullback（突破回调）对象卡

> 功能层：P0_E（执行层 — 入场/出场/执行质量）  
> 成熟度：proxy_quantizable_now（只需 OHLCV，趋势线和突破检测基于价格行为）  
> 生产者：Kimi  
> 来源：GLM_DELIVERY_07 蓝图 + Al Brooks Price Action 素材 + 用户仓库 A1 组 CUTPACK  
> 状态：已冻结核心字段，待代码实现

---

## 1. 基本定义

Brooks Breakout Pullback（BPB，突破回调）是 Al Brooks 价格行为体系中的核心入场模式之一。它描述的是：

1. **突破**：价格以强力 K 线突破关键水平（趋势线、前高/前低、区间边界）
2. **回调**：突破后价格回撤到突破区域附近
3. **继续**：回调结束后价格继续原方向运动

**三种变体**：
- **BPB（Breakout Pullback）**：有效回调后，价格继续原方向（可交易）
- **Failed Breakout（BOF）**：突破后价格迅速回到原区间（不可交易，甚至可反向交易）
- **First/Second Pullback**：只取前两次回调，第三次（以及之后）的回调不交易（成功率下降）

**Brooks BPB 的定位**：BPB 是一种**结构型入场信号**，它回答的是"什么时候在趋势突破后安全入场"的问题。它不预测方向，只确认突破的有效性。

---

## 2. 核心概念与字段冻结

### 2.1 基础字段（已冻结）

```text
bpb_trend_direction     ENUM    -- 当前趋势方向：'up' / 'down' / 'sideways'
bpb_trend_strength      INT(0-10)   -- 突破前的趋势强度评分
bpb_breakout_level      FLOAT   -- 突破的关键价格水平（前高/前低/趋势线）
bpb_breakout_bar_idx    INT     -- 突破 K 线的索引
bpb_breakout_high       FLOAT   -- 突破 K 线的最高价
bpb_breakout_low        FLOAT   -- 突破 K 线的最低价
bpb_breakout_close      FLOAT   -- 突破 K 线的收盘价
bpb_breakout_body_pct   FLOAT   -- 突破 K 线实体占整根 K 线范围的比例（0.0-1.0）
                                  -- 实体 > 70% 视为"强力突破"，< 30% 视为"犹豫突破"
bpb_breakout_volume_ratio   FLOAT   -- 突破 K 线成交量 / 前 20 根平均成交量
                                      -- > 2.0 视为放量突破，< 1.0 视为缩量突破
```

### 2.2 回调字段（已冻结）

```text
bpb_pullback_count      INT     -- 当前是第几次回调（1st / 2nd / 3rd+）
bpb_pullback_start_idx  INT     -- 回调开始 K 线索引（突破后的第一根回调 K 线）
bpb_pullback_end_idx    INT     -- 回调结束 K 线索引（如果已结束）
bpb_pullback_low        FLOAT   -- 回调期间的最低价（上升趋势中）
bpb_pullback_high       FLOAT   -- 回调期间的最高价（下降趋势中）
bpb_pullback_magnitude  FLOAT   -- 回调幅度 %（相对于突破 K 线实体）
                                  -- 计算公式：
                                  -- 上升趋势：(bpb_breakout_high - bpb_pullback_low) / bpb_breakout_body * 100
                                  -- 下降趋势：(bpb_pullback_high - bpb_breakout_low) / bpb_breakout_body * 100
bpb_pullback_depth_ratio    FLOAT   -- 回调深度比率（0.0-1.0+）：
                                      -- 相对于突破 K 线全范围 (high-low) 的比率
                                      -- 0.0 = 未回调，1.0 = 完全回到突破前水平，>1.0 = 突破失败
bpb_pullback_bar_count  INT     -- 回调已持续多少根 K 线
bpb_pullback_volume     FLOAT   -- 回调期间的平均成交量（与突破量对比）
```

### 2.3 突破有效性字段（已冻结）

```text
bpb_is_valid_breakout   BOOL    -- 是否有效突破：
                                  -- 强力突破（body_pct > 0.7）+ 放量（volume_ratio > 1.5）= True
                                  -- 犹豫突破（body_pct < 0.3）或 缩量 = False
bpb_is_failed_breakout  BOOL    -- 是否假突破：
                                  -- 突破后 3 根 K 线内回到原区间 = True
                                  -- 这是 BOF（Breakout Failure）的判定
bpb_is_pullback_valid   BOOL    -- 回调是否有效（可交易）：
                                  -- 回调深度 <= 50%（浅回调）+ 未破关键水平 = True
                                  -- 回调深度 > 61.8% 或 破关键水平 = False（假突破或深回调）
bpb_pullback_quality    ENUM    -- 回调质量：
                                  -- 'PERFECT' = 浅回调（< 38.2%），高概率继续
                                  -- 'GOOD' = 中等回调（38.2%-50%），可交易
                                  -- 'DEEP' = 深回调（50%-61.8%），谨慎交易
                                  -- 'FAILED' = 超过 61.8% 或破水平，不交易
                                  -- 'TOO_EARLY' = 回调尚未结束，观望
```

### 2.4 信号字段（已冻结）

```text
bpb_signal_type         ENUM    -- BPB 信号类型：
                                  -- 'NONE' = 无信号
                                  -- 'BPB_LONG' = 上升趋势回调做多
                                  -- 'BPB_SHORT' = 下降趋势回调做空
                                  -- 'BOF_LONG' = 假突破后反向做多（下降趋势假突破）
                                  -- 'BOF_SHORT' = 假突破后反向做空（上升趋势假突破）
                                  -- 'WAITING_PULLBACK' = 突破已发生，等待回调
                                  -- 'PULLBACK_TOO_DEEP' = 回调过深，放弃
                                  -- 'THIRD_PULLBACK' = 第三次回调，不交易
bpb_signal_strength     INT(0-10)   -- 信号强度：
                                      -- 1st pullback + PERFECT quality + 放量突破 = 9-10
                                      -- 2nd pullback + GOOD quality + 放量突破 = 6-8
                                      -- 1st pullback + DEEP quality = 4-5
                                      -- 其他情况 = 0-3
bpb_entry_price         FLOAT   -- 建议入场价格：
                                  -- 对于 BPB：回调结束后第一根确认 K 线的收盘价
                                  -- 对于 BOF：原区间边界 + 缓冲
bpb_stop_loss_price     FLOAT   -- 建议止损价格：
                                  -- BPB：回调低点下方（做多）或 回调高点上方（做空）+ ATR缓冲
                                  -- BOF：突破水平另一侧 + ATR缓冲
bpb_target_price        FLOAT   -- 建议目标价格：
                                  -- 基于突破 K 线高度的 1:1 或 1:2 风险报酬比
bpb_gap_down_destroyer    BOOL    -- 跳空破位检测：
                                     -- True = 突破后次日出现大幅跳空低开（>1.5×ATR），破坏 BPB 结构
                                     -- 检测到跳空破位时，自动取消 BPB 信号，转为 BOF 处理
                                     -- A股特有：游资"一日游"行情常导致次日跳空低开
bpb_liquidity_filter      FLOAT   -- 流动性过滤阈值（默认 5000万元）：
                                     -- 个股平均成交额 < 此阈值时，BPB 信号无效
                                     -- 防止小盘股突破后无量回调导致无法成交
                                     -- 单位：人民币万元
```

### 2.5 AL Brooks 20 形态子类型（已冻结，补充字段）

```text
bpb_sub_type            ENUM    -- AL Brooks 20 种入场形态子类型（与 bpb_signal_type 配合使用）：
                                  -- 当 bpb_signal_type = 'BPB_LONG' 或 'BPB_SHORT' 时，bpb_sub_type 指示具体形态
                                  -- 当 bpb_signal_type = 'NONE' 时，bpb_sub_type = 'NONE'

# 趋势跟随形态（M1-M8，对应 BPB 1st/2nd pullback）
-- 'M1_EMA_BREAKOUT' = EMA 突破入场（价格突破 EMA + 连续 2 棒收盘于 EMA 同侧）
-- 'M2_EMA_PULLBACK' = EMA 回撤入场（价格回撤至 EMA + 反转信号棒 + EMA 方向不变）
-- 'M3_EMA_DOUBLE_TEST' = EMA 二次测试（价格再次测试 EMA + 形成双底/双顶）
-- 'M4_EMA_FLAG' = EMA 旗形突破（价格沿 EMA 整理 3-10 棒 + 突破信号棒）
-- 'M5_EMA_GAP_FILL' = EMA 缺口回补（价格跳空偏离 EMA + 回补缺口 + 信号棒）
-- 'M6_TRENDLINE_BREAK' = 趋势线突破（价格突破下降趋势线 + 收盘于线上方）
-- 'M7_CHANNEL_FOLLOW' = 通道顺势入场（趋势通道内 + 价格触及通道线 + 反转信号棒）
-- 'M8_BREAKOUT_PULLBACK' = 突破回调入场（价格突破前高/前低 + 回调至突破点 + 信号棒）

# 反转形态（M9-M16，对应 BOF/反转信号）
-- 'M9_DOUBLE_BOTTOM_TOP' = 双底双顶（W/M，两个相近低点/高点 + 中间小反弹 + 突破颈线）
-- 'M10_HEAD_SHOULDER' = 头肩顶底（三峰/三谷 + 中间峰最高/谷最低 + 颈线突破）
-- 'M11_TRIPLE_PUSH' = 三重推动（三波同向推动 + 力度递减 + 反转信号棒）
-- 'M12_WEDGE_REVERSAL' = 楔形反转（三条收敛趋势线 + 假突破 + 反向突破）
-- 'M13_CLIMAX_REVERSAL' = 高潮反转（连续 3+ 根大实体同向棒 + 大幅偏离 EMA + 反转信号棒）
-- 'M14_RANGE_REVERSAL' = 区间突破反转（价格突破区间 + 迅速回到区间内 + 收盘于原区间侧）
-- 'M15_MA_CROSS_REVERSAL' = 均线穿越反转（价格穿越 EMA + 在 EMA 另一侧收盘 + 形成反向信号棒）
-- 'M16_TRENDLINE_FAKEOUT' = 趋势线假突破（价格假突破趋势线 + 回到原趋势侧 + 确认棒）

# 区间交易形态（M17-M20，对应 YTC TST/区间交易）
-- 'M17_RANGE_BOTTOM' = 区间底部买入（价格触及区间下沿 + 下尾线 + 多头信号棒）
-- 'M18_RANGE_TOP' = 区间顶部做空（价格触及区间上沿 + 上尾线 + 空头信号棒）
-- 'M19_RANGE_MID' = 区间中轨入场（价格从区间一侧运行至中轨 + 反转信号棒，轻仓）
-- 'M20_RANGE_BREAKOUT_TEST' = 区间突破回测（价格突破区间 + 回测原区间边界 + 信号棒）

# 默认/未分类
-- 'NONE' = 无具体形态（通用 BPB 信号）
-- 'MIXED' = 多个形态同时满足（罕见，信号增强）

bpb_sub_type_strength     INT(0-10)   -- 形态子类型的强度评分（独立于 bpb_signal_strength）：
                                          -- 趋势跟随形态（M1-M8）：5-7 分（基础）
                                          -- 反转形态（M9-M16）：7-8 分（高概率，但 A 股纯多头下 M10/M12/M14/M16 更适用）
                                          -- 区间交易形态（M17-M20）：4-6 分（基础，M19 仅 4 分）
                                          -- 与 bpb_signal_strength 的关系：
                                            -- final_strength = bpb_signal_strength + (bpb_sub_type_strength - 5) / 2
                                            -- 即：子类型强度高于平均（>5）时，最终强度略微增加；低于平均（<5）时，略微降低

bpb_sub_type_confidence   FLOAT(0-1)  -- 形态识别的置信度：
                                          -- 基于形态匹配的关键点数量 / 总关键点数量
                                          -- 例如 M9（双底）需要 2 个底 + 1 个颈线 + 1 个突破 = 4 个关键点
                                          -- 若只满足 3/4 → confidence = 0.75
                                          -- confidence < 0.6 时，bpb_sub_type = 'NONE'（不指定具体形态）
```

### 2.6 形态识别与策略映射（已冻结）

```text
# 形态 → 策略映射（由 PERIOD_QUEEN 的 regime_state 决定）
bpb_sub_type_strategy_map  ENUM    -- 当前形态在当前状态下的策略适用性：
                                      -- 'APPROVED' = 该形态在当前状态下被允许
                                      -- 'RESTRICTED' = 该形态在当前状态下被限制（如 2nd pullback 限制）
                                      -- 'FORBIDDEN' = 该形态在当前状态下被禁止
                                      -- 'NOT_APPLICABLE' = 该形态与当前方向不匹配（如 SHORT 形态在 LONG 策略中）

# 具体映射规则（由 STRATEGY_BUNDLES_v1.0.md 定义）：
# ATTACK_SUSTAINED: M1-M8 APPROVED, M9-M16 FORBIDDEN, M17-M20 FORBIDDEN
# ATTACK_CONFIRMED: M1-M8 APPROVED, M9-M16 RESTRICTED, M17-M20 RESTRICTED
# POWER_TRANSITION: M1-M8 RESTRICTED, M9-M16 RESTRICTED, M17-M20 APPROVED (TST)
# REMAINING_WARMTH: ALL FORBIDDEN (EXIT_ONLY)
# GESTATION: M1-M8 RESTRICTED, M9-M16 APPROVED (抄底), M17-M20 APPROVED (试错)
# ATTACK_UNSUSTAINED / CUTTING_COMPLETE: ALL FORBIDDEN
```

---

## 3. 计算逻辑（伪代码）

### 3.1 趋势检测与突破识别

```python
def detect_trend_and_breakout(ohlcv_df, lookback=20, min_trend_bars=5):
    """
    检测趋势方向和突破
    
    参数:
        ohlcv_df: DataFrame with [open, high, low, close, volume]
        lookback: 回溯窗口（用于检测趋势和关键水平）
        min_trend_bars: 最小趋势 K 线数（确认趋势需要至少 N 根同向 K 线）
    
    返回:
        dict with trend_direction, breakout_level, breakout_bar_idx, etc.
    """
    recent = ohlcv_df.tail(lookback)
    
    # 1. 检测趋势方向（简化版：基于连续同向收盘价）
    up_bars = sum(1 for i in range(1, len(recent)) if recent['close'].iloc[i] > recent['close'].iloc[i-1])
    down_bars = sum(1 for i in range(1, len(recent)) if recent['close'].iloc[i] < recent['close'].iloc[i-1])
    
    if up_bars >= min_trend_bars and up_bars > down_bars * 1.5:
        trend_direction = 'up'
    elif down_bars >= min_trend_bars and down_bars > up_bars * 1.5:
        trend_direction = 'down'
    else:
        trend_direction = 'sideways'
    
    # 2. 检测关键水平（前高/前低）
    recent_high = recent['high'].max()
    recent_low = recent['low'].min()
    recent_high_idx = recent['high'].idxmax()
    recent_low_idx = recent['low'].idxmin()
    
    # 3. 检测突破（最新一根 K 线是否突破关键水平）
    last_bar = recent.iloc[-1]
    prev_bar = recent.iloc[-2]
    
    breakout_detected = False
    breakout_level = None
    breakout_type = None
    
    if trend_direction == 'up':
        # 上升趋势：突破前高
        if last_bar['high'] > recent_high and prev_bar['high'] <= recent_high:
            breakout_detected = True
            breakout_level = recent_high
            breakout_type = 'HIGH_BREAK'
    elif trend_direction == 'down':
        # 下降趋势：突破前低
        if last_bar['low'] < recent_low and prev_bar['low'] >= recent_low:
            breakout_detected = True
            breakout_level = recent_low
            breakout_type = 'LOW_BREAK'
    
    if not breakout_detected:
        return {
            'bpb_trend_direction': trend_direction,
            'bpb_is_valid_breakout': False,
            'bpb_signal_type': 'NONE',
        }
    
    # 4. 突破 K 线质量评估
    breakout_bar = last_bar
    bar_range = breakout_bar['high'] - breakout_bar['low']
    body = abs(breakout_bar['close'] - breakout_bar['open'])
    body_pct = body / bar_range if bar_range > 0 else 0
    
    avg_volume_20 = ohlcv_df['volume'].tail(20).mean()
    volume_ratio = breakout_bar['volume'] / avg_volume_20 if avg_volume_20 > 0 else 1.0
    
    is_valid = body_pct > 0.7 and volume_ratio > 1.5
    
    return {
        'bpb_trend_direction': trend_direction,
        'bpb_trend_strength': int(max(up_bars, down_bars) / lookback * 10),
        'bpb_breakout_level': breakout_level,
        'bpb_breakout_bar_idx': len(ohlcv_df) - 1,
        'bpb_breakout_high': breakout_bar['high'],
        'bpb_breakout_low': breakout_bar['low'],
        'bpb_breakout_close': breakout_bar['close'],
        'bpb_breakout_body_pct': round(body_pct, 2),
        'bpb_breakout_volume_ratio': round(volume_ratio, 2),
        'bpb_is_valid_breakout': is_valid,
    }
```

### 3.2 回调检测与评估

```python
def detect_and_evaluate_pullback(ohlcv_df, breakout_info, max_pullback_bars=10):
    """
    检测突破后的回调并评估质量
    
    参数:
        ohlcv_df: DataFrame
        breakout_info: detect_trend_and_breakout 的输出
        max_pullback_bars: 最大回调检测 K 线数
    
    返回:
        dict with pullback info and signal
    """
    if not breakout_info['bpb_is_valid_breakout']:
        return {'bpb_signal_type': 'NONE'}
    
    trend = breakout_info['bpb_trend_direction']
    breakout_level = breakout_info['bpb_breakout_level']
    breakout_bar_idx = breakout_info['bpb_breakout_bar_idx']
    breakout_high = breakout_info['bpb_breakout_high']
    breakout_low = breakout_info['bpb_breakout_low']
    breakout_body = abs(breakout_info['bpb_breakout_close'] - ohlcv_df.iloc[breakout_bar_idx]['open'])
    
    # 取突破后的 K 线
    post_breakout = ohlcv_df.iloc[breakout_bar_idx + 1:]
    if len(post_breakout) == 0:
        return {'bpb_signal_type': 'WAITING_PULLBACK'}
    
    # 1. 检测假突破（BOF）
    # 突破后 3 根 K 线内回到原区间
    bof_check_window = post_breakout.head(3)
    if trend == 'up':
        if any(bof_check_window['close'] < breakout_level):
            return {
                'bpb_signal_type': 'BOF_SHORT',
                'bpb_is_failed_breakout': True,
                'bpb_signal_strength': 6,
                'bpb_entry_price': breakout_level - breakout_body * 0.5,
                'bpb_stop_loss_price': breakout_high + breakout_body * 0.5,
            }
    elif trend == 'down':
        if any(bof_check_window['close'] > breakout_level):
            return {
                'bpb_signal_type': 'BOF_LONG',
                'bpb_is_failed_breakout': True,
                'bpb_signal_strength': 6,
                'bpb_entry_price': breakout_level + breakout_body * 0.5,
                'bpb_stop_loss_price': breakout_low - breakout_body * 0.5,
            }
    
    # 2. 检测回调
    # 上升趋势：价格从突破高点开始下降
    # 下降趋势：价格从突破低点开始上升
    pullback_detected = False
    pullback_low = breakout_high  # 上升趋势中
    pullback_high = breakout_low    # 下降趋势中
    pullback_start_idx = None
    pullback_end_idx = None
    
    for i, (idx, bar) in enumerate(post_breakout.iterrows()):
        if i >= max_pullback_bars:
            break
        
        if trend == 'up':
            if bar['low'] < breakout_high:
                pullback_detected = True
                pullback_low = min(pullback_low, bar['low'])
                if pullback_start_idx is None:
                    pullback_start_idx = idx
                pullback_end_idx = idx
            elif pullback_detected and bar['close'] > breakout_high:
                # 回调结束，价格重新站上突破高点
                break
        
        elif trend == 'down':
            if bar['high'] > breakout_low:
                pullback_detected = True
                pullback_high = max(pullback_high, bar['high'])
                if pullback_start_idx is None:
                    pullback_start_idx = idx
                pullback_end_idx = idx
            elif pullback_detected and bar['close'] < breakout_low:
                break
    
    if not pullback_detected:
        return {'bpb_signal_type': 'WAITING_PULLBACK'}
    
    # 3. 计算回调幅度
    if trend == 'up':
        pullback_magnitude = (breakout_high - pullback_low) / breakout_body * 100 if breakout_body > 0 else 0
        depth_ratio = (breakout_high - pullback_low) / (breakout_high - breakout_low) if (breakout_high - breakout_low) > 0 else 0
    else:
        pullback_magnitude = (pullback_high - breakout_low) / breakout_body * 100 if breakout_body > 0 else 0
        depth_ratio = (pullback_high - breakout_low) / (breakout_high - breakout_low) if (breakout_high - breakout_low) > 0 else 0
    
    # 4. 评估回调质量
    if depth_ratio < 0.382:
        pullback_quality = 'PERFECT'
    elif depth_ratio < 0.50:
        pullback_quality = 'GOOD'
    elif depth_ratio < 0.618:
        pullback_quality = 'DEEP'
    else:
        pullback_quality = 'FAILED'
    
    # 5. 生成信号
    if pullback_quality == 'FAILED':
        return {
            'bpb_signal_type': 'PULLBACK_TOO_DEEP',
            'bpb_pullback_quality': pullback_quality,
            'bpb_pullback_magnitude': round(pullback_magnitude, 2),
            'bpb_pullback_depth_ratio': round(depth_ratio, 2),
        }
    
    # 判断回调是否结束（简化：出现第一根同向确认 K 线）
    if pullback_end_idx is not None:
        confirm_bar = ohlcv_df.loc[pullback_end_idx]
        if trend == 'up' and confirm_bar['close'] > confirm_bar['open']:
            signal_type = 'BPB_LONG'
            signal_strength = 9 if pullback_quality == 'PERFECT' else (7 if pullback_quality == 'GOOD' else 4)
            entry_price = confirm_bar['close']
            stop_loss = pullback_low - breakout_body * 0.2
            target = breakout_high + (breakout_high - pullback_low) * 2  # 1:2 RR
        elif trend == 'down' and confirm_bar['close'] < confirm_bar['open']:
            signal_type = 'BPB_SHORT'
            signal_strength = 9 if pullback_quality == 'PERFECT' else (7 if pullback_quality == 'GOOD' else 4)
            entry_price = confirm_bar['close']
            stop_loss = pullback_high + breakout_body * 0.2
            target = breakout_low - (pullback_high - breakout_low) * 2
        else:
            return {'bpb_signal_type': 'WAITING_PULLBACK'}
    else:
        return {'bpb_signal_type': 'WAITING_PULLBACK'}
    
    return {
        'bpb_signal_type': signal_type,
        'bpb_signal_strength': signal_strength,
        'bpb_pullback_quality': pullback_quality,
        'bpb_pullback_magnitude': round(pullback_magnitude, 2),
        'bpb_pullback_depth_ratio': round(depth_ratio, 2),
        'bpb_entry_price': round(entry_price, 4),
        'bpb_stop_loss_price': round(stop_loss, 4),
        'bpb_target_price': round(target, 4),
        'bpb_risk_reward_ratio': round(abs(target - entry_price) / abs(entry_price - stop_loss), 2) if abs(entry_price - stop_loss) > 0 else 0,
    }
```

### 3.3 回调计数管理

```python
def update_pullback_count(symbol_state, current_signal):
    """
    更新回调计数（每个交易品种独立计数）
    
    规则：
    - 同一方向的 BPB 信号，计数递增
    - 方向改变或出现 BOF，计数重置
    - 3rd+ 回调不交易
    """
    if current_signal['bpb_signal_type'] in ['BPB_LONG', 'BPB_SHORT']:
        prev_direction = symbol_state.get('last_bpb_direction')
        current_direction = 'LONG' if 'LONG' in current_signal['bpb_signal_type'] else 'SHORT'
        
        if prev_direction == current_direction:
            symbol_state['pullback_count'] = symbol_state.get('pullback_count', 0) + 1
        else:
            symbol_state['pullback_count'] = 1
            symbol_state['last_bpb_direction'] = current_direction
        
        current_signal['bpb_pullback_count'] = symbol_state['pullback_count']
        
        if symbol_state['pullback_count'] >= 3:
            current_signal['bpb_signal_type'] = 'THIRD_PULLBACK'
            current_signal['bpb_signal_strength'] = 0
    
    elif current_signal['bpb_signal_type'] in ['BOF_LONG', 'BOF_SHORT']:
        # BOF 重置计数
        symbol_state['pullback_count'] = 0
        symbol_state['last_bpb_direction'] = None
    
    return current_signal
```

---

## 4. 与现有指标的互锁逻辑（已冻结）

### 4.1 与 KD MTF 的互锁（已冻结）

```text
互锁规则 BPB × KD MTF：

1. 趋势方向确认：
   - BPB 只在 KD MTF 方向一致时激活：
     - BPB_LONG 需要 kd_day_signal = 'bullish' 且 kd_week_bias ≠ 'extreme_overbought'
     - BPB_SHORT 需要 kd_day_signal = 'bearish' 且 kd_week_bias ≠ 'extreme_oversold'
   - 若 kd_day_signal = 'neutral' → BPB 信号降级为 'WAITING'（无明确方向）

2. KD 极端区过滤：
   - kd_week_extreme_zone = 'overbought' → BPB_LONG 禁止（追高风险）
   - kd_week_extreme_zone = 'oversold' → BPB_SHORT 禁止（杀跌风险）
   - 但 BOF_SHORT 在 overbought 区域可以激活（假突破后反向做空）

3. KD 对齐层级对 BPB 的调制：
   - kd_alignment_tier = 'strong' → BPB 信号强度 +1（多周期确认，突破可靠性高）
   - kd_alignment_tier = 'weak' → BPB 信号强度 -1（方向不明，突破可能假）
   - kd_alignment_tier = 'conflict' → BPB 信号无效（不要交易）

4. KD 4H 确认：
   - bpb_signal_type 只在 kd_4h_confirm 与趋势方向一致时执行
   - 若 kd_4h_confirm = 'neutral' → 等待 4H 确认后再入场
```

### 4.2 与 Volty 的互锁（已冻结）

```text
互锁规则 BPB × VOLTY：

1. 波动率对突破质量的影响：
   - volty_trend_state = 'expansion' → 突破可能因波动率扩大而失真 → bpb_is_valid_breakout 需额外验证
   - volty_trend_state = 'contraction' → 突破更可靠（低波动后的突破通常有效）
   - volty_trend_state = 'trending' → 正常处理

2. Volty 止损与 BPB 的协同：
   - BPB 的止损位（bpb_stop_loss_price）应与 volty_up_stop / volty_dn_stop 比较：
     - 若 BPB 止损位在 volty_stop 更保守的一侧 → 使用 BPB 止损
     - 若 BPB 止损位在 volty_stop 之外 → 使用 volty_stop（更保守）

3. Volty 翻转与 BPB 的冲突：
   - volty_flip_signal = 'bearish_flip' 且 bpb_signal_type = 'BPB_LONG' → 冲突！
     - 处理方式：BPB 信号降级为 'REDUCE'（减仓），或取消（如果 flip 确认）
   - volty_flip_signal = 'bullish_flip' 且 bpb_signal_type = 'BPB_SHORT' → 同理降级
```

### 4.3 与 Volume Profile 的互锁（已冻结）

```text
互锁规则 BPB × VP：

1. VP 位置对突破/回调的过滤：
   - 突破发生在 VP 的 LVN（低成交量区）→ 突破可能快速运行（无阻力），BPB 回调浅，信号强
   - 突破发生在 VP 的 HVN（高成交量区）→ 突破遇到阻力，BPB 可能深回调，信号弱
   - 回调回到 VP 的 POC 附近 → 自然支撑/阻力，BPB 在此处有较高概率反弹

2. VP 的多周期确认：
   - 日线 VP 显示突破方向与日内 VP 一致 → BPB 信号强度 +1
   - 日线 VP 显示突破方向与日内 VP 冲突 → BPB 信号强度 -2（大周期过滤小周期）

3. VP 对假突破的识别：
   - 价格突破 VP 的 VAH 但迅速回到 VA 内部 → 假突破（BOF），VP 提供额外验证
```

### 4.4 与缠论 BSD 的互锁（已冻结）

```text
互锁规则 BPB × CHZL_BSD：

1. 缠论趋势类型与 BPB 的激活条件：
   - chzl_trend_type = 'TREND_UP' → 激活 BPB_LONG 监测
   - chzl_trend_type = 'TREND_DOWN' → 激活 BPB_SHORT 监测
   - chzl_trend_type = 'CONSOLIDATION' → BPB 不激活（震荡市中突破假信号多）
   - 这是 GLM_DELIVERY_07 中明确要求的："仅当 chzl_trend_type=TREND_UP 时激活 BPB 监测"

2. BSD 与 BPB 的共振：
   - BSD 2Buy（回调不破前低）+ BPB_LONG（突破回调）→ 共振！
     - 2Buy 提供结构确认，BPB 提供入场时机
     - 信号强度 +2，风险报酬比优化
   - BSD 3Buy（离开中枢回踩）+ BPB_LONG → 3Buy 是结构信号，BPB 是执行时机
     - 3Buy 定义了"可以买的区域"，BPB 定义了"具体什么价格买"

3. BSD 与 BOF 的反向共振：
   - BSD 1Sell（顶背驰）+ BOF_SHORT（假突破后反向做空）→ 共振
     - 1Sell 预示趋势反转，BOF 确认假突破，两者结合形成高概率做空信号
```

### 4.5 与 TK-R6/R8 的互锁（已冻结）

```text
互锁规则 BPB × TK-R6/R8：

1. TK-R6 阻挡与 BPB 回调的协同：
   - R6 = TOUCH_BOUNCE（强支撑）+ BPB 回调到 R6 区域 → 回调结束概率高，BPB 信号强
   - R6 = DEEP_RETR（深回撤）+ BPB 回调 → 回调可能过深，BPB 质量降级为 'DEEP'
   - R6 = PIERCED（结构破坏）+ BPB → BPB 无效（结构已破坏，不是回调而是反转）

2. TK-R8 资格对 BPB 的过滤：
   - R8_qualified = False → 忽略 BPB 信号（结构无效，回调不可靠）
   - R8_qualified = True → BPB 信号有效
   - 这是安全门：R8 先验证结构，BPB 再执行入场

3. BPB 对 R6 状态的预判：
   - 在 BPB 回调过程中，如果价格回调深度 < 0.382 → 预示 R6 可能 = TOUCH_BOUNCE
   - 如果回调深度 0.382-0.618 → 预示 R6 可能 = DEEP_RETR
   - 如果回调 > 0.618 → 预示 R6 可能 = PIERCED（结构破坏）
```

---

## 5. 失效模式（已冻结）

```text
BPB 失效条件：

1. 无明确趋势：
   - chzl_trend_type = 'CONSOLIDATION' 或 kd_alignment_tier = 'conflict' → BPB 不激活
   - 震荡市中突破频繁假信号，BPB 回调后反转概率高

2. 突破质量差：
   - bpb_breakout_body_pct < 0.3（犹豫突破）→ 即使回调浅，也不交易
   - bpb_breakout_volume_ratio < 1.0（缩量突破）→ 突破可能无机构参与，不可持续

3. 回调过深：
   - bpb_pullback_depth_ratio > 0.618 → 不是回调，可能是趋势反转
   - 回调 > 1.0（完全回到突破前）→ 假突破（BOF），按 BOF 逻辑处理

4. 第三次回调：
   - bpb_pullback_count >= 3 → 不交易（Brooks 规则：只取前两次）
   - 第三次回调成功率显著下降，风险增加

5. 与主要指标冲突：
   - BPB 与 KD MTF 方向冲突 → 以 KD 为准（方向过滤优先）
   - BPB 与 Volty flip 冲突 → 以 Volty 为准（实时翻转信号优先）
   - BPB 与缠论 BSD 结构冲突 → 以 BSD 为准（结构信号优先）

6. A 股特殊失效：
   - 涨停/跌停限制价格运动 → 突破/回调被扭曲，BPB 失去意义
   - T+1 限制当日出场 → BPB 的止损无法当日执行
   - 散户行为导致"假突破"（整数关口、心理关口）→ 需要 VP 过滤
```

---

## 6. A 股特殊适配（已冻结）

```text
A 股 BPB 适配规则：

1. 涨停/跌停影响：
   - limit_up = True → 突破被强制终止（价格无法继续上涨），BPB 不激活
   - limit_down = True → 突破被强制终止，BPB 不激活
   - 涨跌停次日可能跳空，突破/回调的连续性被破坏

2. T+1 影响：
   - BPB 信号一旦触发，当日无法出场
   - 因此 BPB 的止损必须在入场时就设定好（预埋止损），而非盘中动态调整
   - 建议：A 股 BPB 只用于日线/周线级别的波段（留有足够空间）

3. 散户行为与假突破：
   - A 股散户在整数关口（10, 20, 30...）大量交易，形成"心理关口"
   - 突破整数关口后，散户可能追涨/杀跌，导致回调深度异常
   - 应对：整数关口的 BPB 回调深度阈值放宽到 0.618（而非 0.5）

4. 小盘股流动性：
   - 小盘股（<50亿）的突破可能由单笔大单触发，不代表趋势
   - BPB 回调时可能因流动性不足导致价格大幅波动
   - 应对：小盘股 BPB 信号强度降低 2 分，或仅用于大盘股/ETF

5. 集合竞价跳空：
   - 开盘跳空突破前高 → 这不是"真正的突破"（没有盘中确认），BPB 需要等待盘中回调确认
   - 应对：跳空突破的 BPB 需要至少 3 根盘中 K 线确认后才激活
```

---

## 7. 成熟度与数据需求

| 维度 | 评估 |
|------|------|
| **所需数据** | OHLCV（已有） |
| **计算复杂度** | 中（需要趋势检测 + 峰值检测 + 回调追踪） |
| **实时性能** | 每根 K 线更新一次，需要维护状态（回调计数） |
| **回测可行性** | 高（历史 OHLCV 即可回测） |
| **A 股落地** | 可直接落地（需处理涨跌停/整数关口/T+1） |
| **外汇/期货/币圈落地** | 直接可用（无限制） |
| **跨周期** | 支持（日线/4H/1H 均可，小周期回调次数可能更多） |

---

> 文件：OBJECT_CARD_BPB_P0_E__Brooks_Breakout_Pullback_v1.0.md  
> 生产者：Kimi  
> 状态：字段已冻结，待代码实现
