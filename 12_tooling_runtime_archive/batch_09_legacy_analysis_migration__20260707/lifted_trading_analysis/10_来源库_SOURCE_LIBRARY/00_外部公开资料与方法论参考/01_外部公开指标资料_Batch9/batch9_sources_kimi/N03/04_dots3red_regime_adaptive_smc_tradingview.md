# Smart Money Concepts - Regime-Adaptive SMC [Dots3Red]

- 作者: Dots3Red
- 来源: TradingView (Open-Source Script)
- 网址: https://www.tradingview.com/script/OHQsRH7Z-Smart-Money-Concepts-Regime-Adaptive-SMC-Dots3Red/
- 收集日期: 2026-06-12
- 类型: N03 - 市场结构/突破质量
- 用途: 补 `confirmed_pivot_non_repaint / current_bar_visuals_mutable / pivot_confirm_delay_bars`
- 总代码行数: 510 lines (Pine Script v6)

---

## 概述 (来自 TradingView 页面)

This indicator attempts to bridge a gap that most SMC traders encounter in practice: the same pattern — an Order Block, a Fair Value Gap, a structure break — behaves differently depending on whether the market is trending or ranging. A bullish Order Block in a trending market is a continuation entry zone. The same pattern near the top of a range is a reversal signal. This script uses a built-in regime classifier to determine the current market character on every bar, then filters and interprets each SMC concept accordingly.

---

## 核心架构

### 1. Regime Classifier (趋势状态分类器)

Three measurements are combined into a single trend score on every bar:

1. **ADX (Average Directional Index)**
   - Measures how strongly price is committed to a direction
   - Normalized from 0-60 range to 0-1 scale by dividing by 60
   - 参数: `adx_len = 14`

2. **Choppiness Index**
   - Measures directional efficiency
   - Inverted so high choppiness → low score
   - Near 38 (Fibonacci trend boundary) → normalized approaches 1.0
   - Near 100 (pure chop) → approaches 0.0
   - 参数: `chop_len = 14`

3. **ATR Spike Detection**
   - `vol_thresh = 1.5` (ATR ratio threshold for VOLATILE regime)
   - 推荐: 1.8-2.0 for stock indices, 1.4-1.6 for crypto/forex

**Regime State Output:**
- `is_trending` (ADX high + Choppiness low)
- `is_ranging` (ADX low + Choppiness high)
- `is_volatile` (ATR spike detected)
- 通过 `smooth_len = 6` mode filter 平滑 regime 切换

**Regime Thresholds:**
- `trend_thresh = 0.6`
- `range_thresh = 0.6`
- `vol_thresh = 1.5` (ATR multiplier)

---

### 2. Market Structure / BOS / CHoCH

**Swing Detection:**
- `pivot_len = 7` (Swing Pivot Length)
- 推荐: 5-7 for intraday, 7-10 for daily/weekly

**BOS/CHoCH Confirmation Mode:**
- `conf_mode = "Close"` (options: ["Close", "Wick"])
- **CRITICAL: This is the close-confirmed vs wick-confirmed setting**
- BOS/CHoCH 只在收盘确认后才标记（若 conf_mode="Close"）

**BOS (Break of Structure):**
- Bull BOS: 价格突破前高 (swing high)
- Bear BOS: 价格跌破前低 (swing low)
- `show_bos = true`

**CHoCH (Change of Character):**
- Bull CHoCH: 在下降趋势中，价格突破前一个次要高点
- Bear CHoCH: 在上升趋势中，价格跌破前一个次要低点
- `show_choch = true`

**Non-Repaint Implementation:**
- 使用 `barstate.isconfirmed` 或等效逻辑
- Swing pivot 基于已收盘 bar
- BOS/CHoCH 只在结构确认后绘制（非实时预测）

---

### 3. Regime-Adaptive Order Blocks (位移门控)

**Displacement Qualification:**
- `displacement_impulse = math.abs(close - open) > (atr_raw * ob_mult)`
- OB 只在出现"位移冲击"（大实体 K 线）后才标记
- `ob_mult` 参数控制位移灵敏度

**Trending Regime → Continuation OBs:**
- Bull BOS → Bull OB (做多延续)
- Bear BOS → Bear OB (做空延续)

**Ranging Regime → Reversal OBs:**
- Bull CHoCH → Bull OB (底部反转)
- Bear CHoCH → Bear OB (顶部反转)

**OB Mitigation (失效):**
- Bullish OB: `low <= ob.top` (价格从上方进入 OB 区域)
- Bearish OB: `high >= ob.bot` (价格从下方进入 OB 区域)
- 失效后 OB 变灰/变淡

---

### 4. Fair Value Gaps (FVG)

**Detection:**
- Bullish FVG: `high[2] < low[0]` (当前低点 > 前两根高点)
- Bearish FVG: `low[2] > high[0]` (当前高点 < 前两根低点)
- 最小 FVG 大小: `fvg_min_atr * atr_raw`

**FVG Mitigation:**
- 价格回补 FVG 区域后标记为 mitigated

---

## 关键参数面板

```
Regime Classifier:
- adx_len: 14
- atr_len: 14
- atr_base_len: 50 (historical expansion spikes)
- chop_len: 14
- trend_thresh: 0.6
- range_thresh: 0.6
- vol_thresh: 1.5 (Volatile ATR Mult)
- smooth_len: 6 (Regime Smoothing Filter)

Market Structure:
- pivot_len: 7 (Swing Pivot Length)
- conf_mode: "Close" (BOS/CHoCH Target Type: Close/Wick)
- show_bos: true
- show_choch: true

Order Blocks:
- ob_max: 4 (Max Dynamic OBs Per Side)
- ob_mult: displacement multiplier (隐含)

Fair Value Gaps:
- fvg_min_atr: minimum FVG size in ATR units
- fvg_max: max FVGs to display
```

---

## 与 N03 需求的映射

| N03 需求字段 | Dots3Red 实现 | 状态 |
|-------------|---------------|------|
| `confirmed_pivot_non_repaint` | Swing pivot based on closed bars + `conf_mode="Close"` | ✅ 已实现 |
| `current_bar_visuals_mutable` | 当前 bar 的 regime 状态实时变化，但 BOS/CHoCH 只基于已确认结构 | ✅ 部分实现 |
| `pivot_confirm_delay_bars` | `pivot_len = 7` + close confirmation = 至少 7 bar 延迟 | ✅ 可配置 |

---

## Non-Repaint 审计要点

1. **BOS/CHoCH 使用 `conf_mode="Close"`** → 只在收盘后确认，避免盘中重绘
2. **Swing pivot 基于历史已收盘 bar** → 非前瞻性
3. **Regime classifier 使用平滑 filter (smooth_len=6)** → regime 状态有 6 bar 的 mode filter，减少 flicker
4. **但：当前 bar 的 regime 状态是实时的** → 这是设计意图（实时评估市场环境），不是 bug

---

## 源码片段 (关键部分)

### Regime Classifier 核心
```pinescript
// Three measurements combined:
// 1. ADX normalized (0-1)
// 2. Choppiness Index inverted (0-1)
// 3. ATR spike detection (boolean → score)
// Output: trend_score → is_trending / is_ranging / is_volatile
```

### BOS/CHoCH 确认
```pinescript
conf_mode = input.string("Close", "BOS/CHoCH Target Type", options=["Close", "Wick"])
// Close = 收盘确认 (non-repaint)
// Wick = 影线确认 (earlier but less reliable)
```

### Order Block 位移门控
```pinescript
displacement_impulse = math.abs(close - open) > (atr_raw * ob_mult)
// OB 只在大实体 K 线 (displacement) 后标记
```

---

## 设置建议 (来自作者)

- **Regime Smoothing Filter**: 5-7 for intraday, 8-12 for daily/weekly
- **Volatile ATR Mult**: 1.8-2.0 for stock indices, 1.4-1.6 for crypto/forex
- **OB Displacement Mult**: 0.5-0.8 for daily, 1.0-1.5 for intraday
- **Swing Pivot Length**: 5-7 for intraday, 7-10 for daily/weekly
