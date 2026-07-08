# VP_P0_E — Volume Profile（成交量分布）对象卡

> 功能层：P0_E（执行层 — 入场/出场/执行质量）  
> 成熟度：proxy_quantizable_now（只需 OHLCV，无额外数据需求）  
> 生产者：Kimi  
> 来源：搜索汇总 + 公开标准定义  
> 状态：已冻结核心字段，待代码实现

---

## 1. 基本定义

Volume Profile（成交量分布，简称 VP）将特定时间范围内的**成交量按价格水平进行统计**，形成价格维度上的成交量分布柱状图。它揭示的是"市场在不同价格上累积了多少成交量"——高成交量代表价格得到广泛认可，低成交量代表价格被市场忽略或快速穿越。

与 VWAP 的区别：VWAP 是"平均成本"（价格 × 成交量加权平均），VP 是"分布"（每个价格有多少成交量）。VWAP 是动态线，VP 是静态区域（固定周期内）。

---

## 2. 核心概念与字段冻结

### 2.1 基础字段（已冻结）

```text
vp_poc              FLOAT   -- 控制点（Point of Control）：该周期内成交量最高的价格
vp_vah              FLOAT   -- 价值区域上沿（Value Area High）：涵盖70%成交量的价格区间上界
vp_val              FLOAT   -- 价值区域下沿（Value Area Low）：涵盖70%成交量的价格区间下界
vp_profile_high     FLOAT   -- 该周期内的最高成交价（Profile High）
vp_profile_low      FLOAT   -- 该周期内的最低成交价（Profile Low）
vp_total_volume     BIGINT  -- 该周期内总成交量
```

### 2.2 派生字段（已冻结）

```text
vp_hvn_levels[]     ARRAY<FLOAT>   -- 高成交量节点（High Volume Node）：成交量显著高于均值的价位列表
vp_lvn_levels[]     ARRAY<FLOAT>   -- 低成交量节点（Low Volume Node）：成交量显著低于均值的价位列表
vp_hvn_count        INT            -- HVN 数量
vp_lvn_count        INT            -- LVN 数量
vp_current_rel_position  ENUM      -- 当前价格相对 VA 的位置：
                                      -- 'inside'  = 价格在 VA 内部（平衡区）
                                      -- 'above'   = 价格在 VAH 之上（可能突破）
                                      -- 'below'   = 价格在 VAL 之下（可能下破）
                                      -- 'at_poc'  = 价格恰好在 POC 附近（±0.5% ATR）
vp_trend_shape      ENUM           -- 成交量分布形态：
                                      -- 'ascending_triangle'  = 正三角（下方 HVN 大 > 上方 HVN 小）→ 多头趋势
                                      -- 'descending_triangle' = 倒三角（上方 HVN 大 > 下方 HVN 小）→ 空头/盘整
                                      -- 'balanced'            = 上下 HVN 均匀 → 平衡
                                      -- 'single_peak'        = 单峰（POC 突出，两侧递减）→ 典型盘整
vp_volume_integrity_score   FLOAT   -- 成交量完整性评分（0.0-1.0）：
                                     -- 基于换手率 / 自由流通盘比率，评估 VP 形态是否被人为扭曲
                                     -- 小盘股（<50亿）或庄家对倒时，该评分降低
                                     -- score < 0.6 时，VP 信号降级为观察
                                     -- score < 0.4 时，VP 信号失效（防止人为成交量造假）
```

### 2.3 入场/出场信号字段（已冻结）

```text
vp_signal_type      ENUM           -- 当前 VP 产生的信号类型：
                                      -- 'NONE'                = 无信号
                                      -- 'VA_BREAKOUT_LONG'    = 突破 VAH 做多（需 VROC 确认）
                                      -- 'VA_BREAKOUT_SHORT'   = 下破 VAL 做空（需 VROC 确认）
                                      -- 'POC_REVERSION_LONG'  = 价格从下方回归 POC，确认支撑后做多
                                      -- 'POC_REVERSION_SHORT' = 价格从上方回归 POC，确认阻力后做空
                                      -- 'LVN_MOMENTUM_LONG'   = 快速穿越 LVN 向上，动量延续做多
                                      -- 'LVN_MOMENTUM_SHORT'  = 快速穿越 LVN 向下，动量延续做空
                                      -- 'HVN_CONSOLIDATION'   = 价格停留在 HVN 区域，观望/减仓
vp_signal_strength  INT(0-10)      -- 信号强度评分（多因素加权）
vp_suggested_stop   FLOAT          -- VP 建议止损位：
                                      -- VA_BREAKOUT_LONG → 反向 VA 边缘（VAL）
                                      -- POC_REVERSION → 反向 LVN 或 Profile Low/High
                                      -- LVN_MOMENTUM → 反向 HVN 或 1.5×ATR
vp_suggested_target FLOAT          -- VP 建议目标位：下一个 HVN 或 POC（同方向）
```

---

## 3. 计算逻辑（伪代码）

### 3.1 核心计算：VP 分布

```python
def calculate_volume_profile(ohlcv_df, period=20, n_bins=50, va_pct=0.70):
    """
    计算 Volume Profile
    
    参数:
        ohlcv_df: DataFrame with [open, high, low, close, volume]
        period: 计算周期（日线级别建议 20-60，周线级别建议 10-20）
        n_bins: 价格区间划分数量
        va_pct: 价值区域百分比（默认 70%）
    
    返回:
        dict with vp_poc, vp_vah, vp_val, vp_hvn_levels, vp_lvn_levels, etc.
    """
    # 1. 取最近 period 根 K 线
    window = ohlcv_df.tail(period)
    
    # 2. 确定价格范围
    price_min = window['low'].min()
    price_max = window['high'].max()
    bin_size = (price_max - price_min) / n_bins
    
    # 3. 按价格区间分配成交量（使用典型价格：典型价格 = (high + low + close) / 3）
    bins = {}
    for idx, row in window.iterrows():
        typical_price = (row['high'] + row['low'] + row['close']) / 3.0
        volume = row['volume']
        # 将典型价格分配到对应 bin
        bin_idx = int((typical_price - price_min) / bin_size)
        bin_idx = min(bin_idx, n_bins - 1)  # 边界保护
        bin_price = price_min + (bin_idx + 0.5) * bin_size  # bin 中心价格
        bins[bin_price] = bins.get(bin_price, 0) + volume
    
    # 4. 排序得到成交量分布
    sorted_bins = sorted(bins.items(), key=lambda x: x[1], reverse=True)
    
    # 5. POC = 成交量最高的 bin 价格
    vp_poc = sorted_bins[0][0]
    vp_poc_volume = sorted_bins[0][1]
    
    # 6. VA（价值区域）= 从 POC 向两侧扩展，直到累积成交量达到 va_pct
    total_volume = sum(v for _, v in sorted_bins)
    target_va_volume = total_volume * va_pct
    
    # 按价格排序（而非成交量排序）
    price_sorted_bins = sorted(bins.items(), key=lambda x: x[0])
    
    # 找到 POC 在价格排序中的索引
    poc_idx = next(i for i, (p, _) in enumerate(price_sorted_bins) if abs(p - vp_poc) < bin_size/2)
    
    va_low_idx = poc_idx
    va_high_idx = poc_idx
    va_cum_volume = price_sorted_bins[poc_idx][1]
    
    # 向两侧扩展
    while va_cum_volume < target_va_volume:
        low_dist = poc_idx - va_low_idx if va_low_idx > 0 else float('inf')
        high_dist = va_high_idx - poc_idx if va_high_idx < len(price_sorted_bins) - 1 else float('inf')
        
        if low_dist <= high_dist and va_low_idx > 0:
            va_low_idx -= 1
            va_cum_volume += price_sorted_bins[va_low_idx][1]
        elif va_high_idx < len(price_sorted_bins) - 1:
            va_high_idx += 1
            va_cum_volume += price_sorted_bins[va_high_idx][1]
        else:
            break  # 无法继续扩展
    
    vp_val = price_sorted_bins[va_low_idx][0]
    vp_vah = price_sorted_bins[va_high_idx][0]
    
    # 7. HVN / LVN 识别
    avg_volume = total_volume / len(bins)
    vp_hvn_levels = [p for p, v in bins.items() if v > avg_volume * 1.5]  # 1.5x 均值作为 HVN 阈值
    vp_lvn_levels = [p for p, v in bins.items() if v < avg_volume * 0.3]  # 0.3x 均值作为 LVN 阈值
    
    # 8. 趋势形态判断
    lower_hvn_volume = sum(v for p, v in bins.items() if p < vp_poc and v > avg_volume * 1.5)
    upper_hvn_volume = sum(v for p, v in bins.items() if p > vp_poc and v > avg_volume * 1.5)
    
    if lower_hvn_volume > upper_hvn_volume * 1.5:
        vp_trend_shape = 'ascending_triangle'   # 正三角 → 多头
    elif upper_hvn_volume > lower_hvn_volume * 1.5:
        vp_trend_shape = 'descending_triangle'  # 倒三角 → 空头/盘整
    elif len(vp_hvn_levels) == 1:
        vp_trend_shape = 'single_peak'          # 单峰
    else:
        vp_trend_shape = 'balanced'
    
    return {
        'vp_poc': vp_poc,
        'vp_vah': vp_vah,
        'vp_val': vp_val,
        'vp_profile_high': price_max,
        'vp_profile_low': price_min,
        'vp_total_volume': total_volume,
        'vp_hvn_levels': sorted(vp_hvn_levels),
        'vp_lvn_levels': sorted(vp_lvn_levels),
        'vp_hvn_count': len(vp_hvn_levels),
        'vp_lvn_count': len(vp_lvn_levels),
        'vp_trend_shape': vp_trend_shape,
    }
```

### 3.2 信号生成逻辑

```python
def generate_vp_signal(current_price, vp_data, ohlcv_df, atr14, vroc_threshold=1.5):
    """
    基于 VP 生成交易信号
    
    参数:
        current_price: 当前价格
        vp_data: calculate_volume_profile 的输出
        ohlcv_df: 最新 OHLCV（用于计算 VROC）
        atr14: 14日 ATR（用于止损计算）
        vroc_threshold: 成交量变动率阈值（默认 1.5x）
    """
    vp = vp_data
    
    # 1. 当前位置判断
    if abs(current_price - vp['vp_poc']) / atr14 < 0.5:
        vp_current_rel_position = 'at_poc'
    elif current_price > vp['vp_vah']:
        vp_current_rel_position = 'above'
    elif current_price < vp['vp_val']:
        vp_current_rel_position = 'below'
    else:
        vp_current_rel_position = 'inside'
    
    # 2. VROC 计算（当前成交量 / 前 N 日平均成交量）
    current_volume = ohlcv_df['volume'].iloc[-1]
    avg_volume_20 = ohlcv_df['volume'].tail(20).mean()
    vp_vroc = current_volume / avg_volume_20 if avg_volume_20 > 0 else 1.0
    
    # 3. 信号生成
    vp_signal_type = 'NONE'
    vp_signal_strength = 0
    vp_suggested_stop = None
    vp_suggested_target = None
    
    # 3.1 VA 突破做多
    if vp_current_rel_position == 'above' and vp_vroc > vroc_threshold:
        vp_signal_type = 'VA_BREAKOUT_LONG'
        vp_signal_strength = min(10, int(vp_vroc * 4))  # VROC 越高，强度越大
        vp_suggested_stop = vp['vp_val'] - 0.5 * atr14   # 跌破 VA 下沿 + 缓冲
        # 目标：下一个 HVN 或 2×ATR
        next_hvn = next((h for h in vp['vp_hvn_levels'] if h > current_price), current_price + 2 * atr14)
        vp_suggested_target = next_hvn
    
    # 3.2 VA 突破做空（仅在非 A 股或期货/外汇/币圈使用）
    elif vp_current_rel_position == 'below' and vp_vroc > vroc_threshold:
        vp_signal_type = 'VA_BREAKOUT_SHORT'
        vp_signal_strength = min(10, int(vp_vroc * 4))
        vp_suggested_stop = vp['vp_vah'] + 0.5 * atr14
        next_hvn = next((h for h in reversed(vp['vp_hvn_levels']) if h < current_price), current_price - 2 * atr14)
        vp_suggested_target = next_hvn
    
    # 3.3 POC 回归做多（价格从下方回归 POC，且 POC 是 HVN）
    elif vp_current_rel_position == 'at_poc' and vp['vp_poc'] in vp['vp_hvn_levels']:
        # 需要确认价格是从下方上来的（前一根 K 线收盘价 < POC）
        prev_close = ohlcv_df['close'].iloc[-2]
        if prev_close < vp['vp_poc']:
            vp_signal_type = 'POC_REVERSION_LONG'
            vp_signal_strength = 5  # 中等强度，需其他指标确认
            vp_suggested_stop = prev_close - 0.5 * atr14
            vp_suggested_target = vp['vp_vah']  # 目标到 VAH
    
    # 3.4 POC 回归做空
    elif vp_current_rel_position == 'at_poc' and vp['vp_poc'] in vp['vp_hvn_levels']:
        prev_close = ohlcv_df['close'].iloc[-2]
        if prev_close > vp['vp_poc']:
            vp_signal_type = 'POC_REVERSION_SHORT'
            vp_signal_strength = 5
            vp_suggested_stop = prev_close + 0.5 * atr14
            vp_suggested_target = vp['vp_val']
    
    # 3.5 LVN 穿越动量（价格快速通过 LVN 区域，向下一 HVN 运行）
    # 判断：当前价格在 LVN 区域，且当前 K 线实体大（>(open-close)/ATR > 1.0）
    elif any(abs(current_price - lvn) / atr14 < 0.5 for lvn in vp['vp_lvn_levels']):
        current_bar_range = abs(ohlcv_df['close'].iloc[-1] - ohlcv_df['open'].iloc[-1])
        if current_bar_range > atr14:
            direction = 'LONG' if ohlcv_df['close'].iloc[-1] > ohlcv_df['open'].iloc[-1] else 'SHORT'
            vp_signal_type = f'LVN_MOMENTUM_{direction}'
            vp_signal_strength = 7
            # 止损：反向 HVN 或 1.5×ATR
            if direction == 'LONG':
                vp_suggested_stop = current_price - 1.5 * atr14
                vp_suggested_target = next((h for h in vp['vp_hvn_levels'] if h > current_price), current_price + 2 * atr14)
            else:
                vp_suggested_stop = current_price + 1.5 * atr14
                vp_suggested_target = next((h for h in reversed(vp['vp_hvn_levels']) if h < current_price), current_price - 2 * atr14)
    
    return {
        'vp_signal_type': vp_signal_type,
        'vp_signal_strength': vp_signal_strength,
        'vp_suggested_stop': vp_suggested_stop,
        'vp_suggested_target': vp_suggested_target,
        'vp_current_rel_position': vp_current_rel_position,
        'vp_vroc': round(vp_vroc, 2),
    }
```

---

## 4. 与现有指标的互锁逻辑

### 4.1 与 KD MTF 的互锁（已冻结）

```text
互锁规则 VP × KD MTF：

1. VP 信号只在 KD MTF "方向一致" 时生效：
   - VA_BREAKOUT_LONG 需要 kd_day_signal = 'bullish' 且 kd_week_bias ≠ 'extreme_overbought'
   - VA_BREAKOUT_SHORT 需要 kd_day_signal = 'bearish' 且 kd_week_bias ≠ 'extreme_oversold'

2. VP 信号强度受 KD MTF 对齐层级调制：
   - kd_alignment_tier = 'strong'  → vp_signal_strength 不变
   - kd_alignment_tier = 'medium' → vp_signal_strength × 0.8
   - kd_alignment_tier = 'weak'   → vp_signal_strength × 0.5，建议降级为观察
   - kd_alignment_tier = 'conflict' → vp_signal_type = 'NONE'（强制取消）

3. POC 回归信号需要 kd_4h_confirm 确认：
   - POC_REVERSION_LONG 需要 kd_4h_confirm = 'bullish'
   - POC_REVERSION_SHORT 需要 kd_4h_confirm = 'bearish'
   - 若 kd_4h_confirm = 'neutral'，vp_signal_strength 减 2 分

4. 极端区过滤：
   - kd_week_extreme_zone = 'overbought' 时，禁止 VA_BREAKOUT_LONG（追高风险）
   - kd_week_extreme_zone = 'oversold' 时，禁止 VA_BREAKOUT_SHORT（杀跌风险）
   - 但允许 POC_REVERSION（逆势回归）在极端区执行，因为 VP 的 POC 回归本质就是均值回归
```

### 4.2 与 Volty 的互锁（已冻结）

```text
互锁规则 VP × Volty：

1. VP 止损位与 Volty 止损的优先级：
   - 若 vp_suggested_stop 与 volty_up_stop / volty_dn_stop 方向一致（都在同一侧），
     取两者中更保守（更远离当前价）的作为最终止损。
   - 若方向不一致（如 VP 建议止损在 volty_stop 之外），触发告警，建议人工审核。

2. VP 信号在 Volty 极端状态下降级：
   - volty_trend_state = 'expansion'（波动扩张）→ vp_signal_strength 减 2，因为突破可能是假突破
   - volty_trend_state = 'contraction'（波动收缩）→ vp_signal_strength 加 1，因为突破可靠性更高
   - volty_trend_state = 'trending'（趋势中）→ vp_signal_strength 不变

3. VP 的 LVN_MOMENTUM 信号与 volty_flip_signal：
   - 若 volty_flip_signal = 'bullish_flip' 且 vp_signal_type = 'LVN_MOMENTUM_LONG' → 共振，强度 +2
   - 若 volty_flip_signal = 'bearish_flip' 且 vp_signal_type = 'LVN_MOMENTUM_SHORT' → 共振，强度 +2
   - 若方向冲突 → 取消 VP 信号，以 volty_flip 为准（Volty 的翻转信号优先级更高）
```

### 4.3 与缠论 BSD 的互锁（已冻结）

```text
互锁规则 VP × CHZL_BSD：

1. 缠论 1Buy/2Buy/3Buy 出现时，VP 提供"执行价位精细化"：
   - 1Buy 的理想入场点 = max(1Buy 理论位, 最近的 HVN 下沿)
     （HVN 是历史成交密集区，机构成本区，在此买入更"安全"）
   - 2Buy 的理想入场点 = max(2Buy 理论位, POC 附近)
     （POC 是"公平价格"，在此买入成本接近市场平均）
   - 3Buy 的理想入场点 = max(3Buy 理论位, VAH 下沿)
     （3Buy 是突破后回踩，VAH 由阻力变支撑）

2. VP 信号与 BSD 的优先级：
   - BSD 提供"结构信号"（什么位置可以买卖），VP 提供"执行价位"（具体什么价格入场/出场）。
   - BSD 是"战略层"，VP 是"战术层"。
   - 若 BSD 信号出现但 VP 显示当前价格处于 LVN（无成交量支撑）→ 等待价格到达 HVN 再执行。

3. 背驰确认：
   - CHZL_BC（背驰）出现时，若 VP 显示价格远离 POC（在 VA 外部）→ 背驰可靠性更高（价格偏离"公平价值"）
   - CHZL_BC 出现时，若价格恰好在 POC 附近（at_poc）→ 背驰可能是假信号（价格已经回归均值）
```

### 4.4 与 TK 外汇体系的互锁（已冻结）

```text
互锁规则 VP × TK：

1. TK-IB（回撤阻挡）与 VP 的 HVN：
   - TK-R6 的回撤深度（0.236/0.382/0.618）可用 VP 的 HVN 位置作为"历史验证"。
   - 若 0.618 回撤位恰好落在某个 HVN 上 → 该回撤位可靠性极高（历史成交密集区 + 黄金分割共振）
   - 若 0.618 回撤位落在 LVN 上 → 回撤可能继续深入（无历史支撑），TK-R6 状态可能从 BOUNCE → REJECTED

2. TK-DB/CB（需求区/供给区）与 VP 的 VAL/VAH：
   - TK-DB 的有效区域与 VP 的 VAL 功能相似（都是"支撑区"）。
   - 若 TK-DB 区域与 VP 的 VAL 或某个 HVN 重合 → 该区域成为"强支撑带"，可执行加仓。
   - 若 TK-CB 区域与 VP 的 VAH 或某个 HVN 重合 → 该区域成为"强阻力带"，可执行减仓/做空。

3. TK-XBreaking（突破/陷阱）与 VP 的 VA 突破：
   - TK XBreaking 的 buffer0（CB/DB 类型）可作为 VP 信号的事前过滤：
     - 若 XBreaking 类型 = CB（供给突破）且 VP 信号 = VA_BREAKOUT_LONG → 冲突，取消 VP 信号（供给区突破可能是假突破）
     - 若 XBreaking 类型 = DB（需求突破）且 VP 信号 = VA_BREAKOUT_LONG → 共振，强度 +2
```

---

## 5. 多周期联立（已冻结）

```text
多周期 VP 联立规则：

1. 周期层级：
   - 周线 VP（大周期）：确定主要长期价值区和 POC（长期支撑/阻力）
   - 日线 VP（中周期）：确定波段价值区和 HVN/LVN 分布
   - 60min/15min VP（小周期）：确定战术进出点

2. 联立过滤：
   - 日线 VP_signal = VA_BREAKOUT_LONG
   - 但周线 VP 显示当前价格处于周线 HVN 强阻力区 → 信号降级（可能是假突破）
   - 日线 VP_signal = POC_REVERSION_LONG
   - 且周线 VP 显示 POC 也是周线 HVN → 信号升级（长短周期共振）

3. 字段化：
   - vp_weekly_poc: 周线 POC（作为长期参考）
   - vp_weekly_position: 当前价格相对周线 VA 的位置
   - vp_daily_poc: 日线 POC
   - vp_intraday_poc: 日内 POC（如 15min）
   - vp_multi_timeframe_resonance: 多周期共振评分（0-10）
```

---

## 6. 失效模式（已冻结）

```text
VP 失效条件：

1. 数据不足：
   - 周期内 K 线数量 < 10 → VP 分布不可靠，禁止生成信号
   - 总成交量 < 历史平均成交量的 50% → 分布可能失真，信号降级

2. 极端行情：
   - 连续涨跌停（A股）→ 价格停在极限位，VP 的 VA 可能被压缩到极限，失去意义
   - 一夜情/黑天鹅 → 单根 K 线实体极大，VP 分布被单根 K 线主导，失效

3. 形态失效：
   - vp_trend_shape = 'single_peak'（单峰）但价格长期在 POC 附近震荡 → 市场处于极度平衡，任何方向突破都可能是假突破
   - HVN 数量 = 0（所有价位成交量均匀）→ 无明显的支撑/阻力，VP 信号失效

4. 与其他指标冲突：
   - VP 信号与 KD MTF 冲突（如 VP 做多但 KD 处于极端超买）→ 以 KD 为准，VP 仅作为价位参考
   - VP 信号与缠论 BSD 结构冲突（如 VP 突破但缠论显示没有背驰）→ 以缠论为准，VP 仅作为价位参考
```

---

## 7. A 股特殊适配（已冻结）

```text
A 股 VP 适配规则：

1. 涨停/跌停状态：
   - limit_up = True → 禁止 VP 生成任何 SHORT 信号（无法做空）
   - limit_down = True → 禁止 VP 生成任何 LONG 信号（跌停时抄底风险极高）
   - 涨停/跌停时 VP 的 VROC 计算失效（成交量被价格限制扭曲），信号降级为观察

2. T+1 限制：
   - VP 信号一旦触发入场，当日无法出场。
   - 因此 VP 的日内信号（如 15min LVN_MOMENTUM）在 A 股只适用于：
     - 早盘信号（9:30-10:00），留有足够时间观察当日收盘前状态
     - 或转换为日线/周线级别的波段信号

3. 集合竞价：
   - 集合竞价成交量（9:15-9:25）不计入 VP 的常规成交量（因为价格形成机制不同）。
   - 但可单独提取 `auction_volume` 和 `auction_price_diff` 作为独立因子，不混入 VP 计算。

4. 散户行为影响：
   - A 股散户在整数关口（如 10.00, 20.00）大量挂单，导致 VP 在这些价位出现"假性 HVN"。
   - 建议：在 A 股 VP 中，对整数关口的成交量进行降权处理（如乘以 0.7），减少散户噪音。
```

---

## 8. 成熟度与数据需求

| 维度 | 评估 |
|------|------|
| **所需数据** | OHLCV（已有） |
| **计算复杂度** | 中（需要排序和累积计算） |
| **实时性能** | 每根 K 线更新一次，不影响性能 |
| **回测可行性** | 高（历史 OHLCV 即可回测） |
| **A 股落地** | 可直接落地（需加入涨停/跌停/T+1 过滤） |
| **外汇/期货/币圈落地** | 直接可用（无限制） |
| **跨周期** | 支持（日线/周线/日内） |

---

> 文件：OBJECT_CARD_VP_P0_E__VolumeProfile_v1.0.md  
> 生产者：Kimi  
> 状态：字段已冻结，待代码实现
