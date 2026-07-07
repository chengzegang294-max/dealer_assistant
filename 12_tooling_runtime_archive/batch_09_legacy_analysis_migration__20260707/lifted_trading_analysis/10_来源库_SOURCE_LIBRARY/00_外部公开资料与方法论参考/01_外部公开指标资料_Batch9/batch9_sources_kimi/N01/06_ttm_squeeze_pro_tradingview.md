# TTM Squeeze Pro

- 作者: Beardy_Fred
- 来源: TradingView (Open-Source Script)
- 网址: https://www.tradingview.com/script/0drMdHsO-TTM-Squeeze-Pro/
- 收集日期: 2026-06-12
- 类型: N01 - 波动率状态机
- 用途: 补 `squeeze_tier` 细节和 fired 逻辑
- 总代码行数: 57 lines (Pine Script v5)
- 人气: 204,187 views, 6,500 favorites

---

## 概述

The TTM Squeeze is a visual way of seeing how Bollinger Bands (standard deviations from a simple moving average) relate to Keltner Channels (average true range bands) compared with the momentum of the price action. The concept is that as Bollinger Bands compress within Keltner Channels, price volatility decreases, giving way for a potential explosive price movement up or down.

---

## 完整源码

```pinescript
//@version=5
indicator('Beardy Squeeze Pro', shorttitle='Squeeze', overlay=false, precision=2)

length = input.int(20, "TTM Squeeze Length")

// BOLLINGER BANDS
BB_mult = input.float(2.0, "Bollinger Band STD Multiplier")
BB_basis = ta.sma(close, length)
dev = BB_mult * ta.stdev(close, length)
BB_upper = BB_basis + dev
BB_lower = BB_basis - dev

// KELTNER CHANNELS
KC_mult_high = input.float(1.0, "Keltner Channel #1")
KC_mult_mid = input.float(1.5, "Keltner Channel #2")
KC_mult_low = input.float(2.0, "Keltner Channel #3")
KC_basis = ta.sma(close, length)
devKC = ta.sma(ta.tr, length)
KC_upper_high = KC_basis + devKC * KC_mult_high
KC_lower_high = KC_basis - devKC * KC_mult_high
KC_upper_mid = KC_basis + devKC * KC_mult_mid
KC_lower_mid = KC_basis - devKC * KC_mult_mid
KC_upper_low = KC_basis + devKC * KC_mult_low
KC_lower_low = KC_basis - devKC * KC_mult_low

// SQUEEZE CONDITIONS
NoSqz = BB_lower < KC_lower_low or BB_upper > KC_upper_low    // NO SQUEEZE: GREEN
LowSqz = BB_lower >= KC_lower_low or BB_upper <= KC_upper_low  // LOW COMPRESSION: BLACK
MidSqz = BB_lower >= KC_lower_mid or BB_upper <= KC_upper_mid  // MID COMPRESSION: RED
HighSqz = BB_lower >= KC_lower_high or BB_upper <= KC_upper_high // HIGH COMPRESSION: ORANGE

// MOMENTUM OSCILLATOR
mom = ta.linreg(close - math.avg(math.avg(ta.highest(high, length), ta.lowest(low, length)), ta.sma(close, length)), length, 0)

// MOMENTUM HISTOGRAM COLOR
iff_1 = mom > nz(mom[1]) ? color.new(color.aqua, 0) : color.new(#2962ff, 0)
iff_2 = mom < nz(mom[1]) ? color.new(color.red, 0) : color.new(color.yellow, 0)
mom_color = mom > 0 ? iff_1 : iff_2

// SQUEEZE DOTS COLOR
sq_color = HighSqz ? color.new(color.orange, 0) : MidSqz ? color.new(color.red, 0) : LowSqz ? color.new(color.black, 0) : color.new(color.green, 0)

// ALERTS
Detect_Sqz_Start = input.bool(true, "Alert Price Action Squeeze")
Detect_Sqz_Fire = input.bool(true, "Alert Squeeze Firing")
if Detect_Sqz_Start and NoSqz[1] and not NoSqz
    alert("Squeeze Started")
else if Detect_Sqz_Fire and NoSqz and not NoSqz[1]
    alert("Squeeze Fired")

// PLOTS
plot(mom, title='MOM', color=mom_color, style=plot.style_columns, linewidth=2)
plot(0, title='SQZ', color=sq_color, style=plot.style_circles, linewidth=3)
```

---

## Squeeze Tier 定义

| Tier | 条件 | 颜色 | 含义 |
|------|------|------|------|
| No Squeeze | `BB_lower < KC_lower_low OR BB_upper > KC_upper_low` | **GREEN** | 无挤压，波动正常 |
| Low Squeeze | `BB_lower >= KC_lower_low OR BB_upper <= KC_upper_low` | **BLACK** | 低度压缩 |
| Mid Squeeze | `BB_lower >= KC_lower_mid OR BB_upper <= KC_upper_mid` | **RED** | 中度压缩 |
| High Squeeze | `BB_lower >= KC_lower_high OR BB_upper <= KC_upper_high` | **ORANGE** | 高度压缩 |

## Squeeze Fired 逻辑

```pinescript
// Squeeze Start: 从 No Squeeze 进入任意 Squeeze
NoSqz[1] and not NoSqz

// Squeeze Fired: 从 Squeeze 回到 No Squeeze（爆发）
NoSqz and not NoSqz[1]
```

## Momentum 计算

```pinescript
mom = ta.linreg(
    close - avg(avg(highest(high, length), lowest(low, length)), sma(close, length)),
    length, 0
)
```

使用线性回归的动量振荡器，基于：
- 当前 close
- 与 (最高价 + 最低价)/2 和 SMA 的均值的偏差

**Momentum 颜色规则：**
- mom > 0 且上升: aqua (浅青)
- mom > 0 且下降: blue (#2962ff)
- mom < 0 且下降: red
- mom < 0 且上升: yellow

---

## 关键参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| TTM Squeeze Length | 20 | BB/KC/Momentum 的共用长度 |
| BB STD Multiplier | 2.0 | 布林带标准差倍数 |
| Keltner Channel #1 | 1.0 | KC tight (High Squeeze 阈值) |
| Keltner Channel #2 | 1.5 | KC mid (Mid Squeeze 阈值) |
| Keltner Channel #3 | 2.0 | KC wide (Low Squeeze 阈值) |

---

## 与 AG Pro ATR Compression Map 的对比

| 维度 | TTM Squeeze Pro (57 lines) | AG Pro ATR Compression Map (598 lines) |
|------|---------------------------|--------------------------------------|
| 核心原理 | BB vs KC 挤压 | ATR + Range + Noise + Containment 四维评分 |
| Squeeze 层级 | 4 级 (No/Low/Mid/High) | 4 级 (Loose/Building/Tight/Mature) |
| Momentum | ✅ Linear Regression Oscillator | ❌ 无独立 momentum |
| 可视化 | Histogram + Dots | Ribbon + Box + Panel + Tags |
| 复杂度 | 极简 | 极繁 |
| 参数可调性 | 5 个参数 | 20+ 个参数 |

---

## 关键审计点

1. **使用 `or` 而非 `and` 在 Squeeze 条件中**: 
   - `BB_lower >= KC_lower_low OR BB_upper <= KC_upper_low`
   - 这意味着只要**一侧**挤压就算 squeeze，不需要两侧同时挤压
   - 与官方 TTM Squeeze 的 `and` 逻辑可能有差异

2. **Momentum 使用 `nz(mom[1])` 检测方向变化**: 无前视，无重绘

3. **Alert 逻辑基于 `NoSqz` 状态变化**: 纯状态机，无预测

4. **SMA 作为 basis (非 EMA)**: 比 EMA 更平滑，延迟更大
