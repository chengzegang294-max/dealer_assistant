# Institutional Market Structure BOS and CHoCH [algo_aakash]

- 作者: algo_aakash (AlgoTim)
- 来源: TradingView (Open-Source Script)
- 网址: https://fr.tradingview.com/script/UjDVwAtJ-Institutional-Market-Structure-BOS-and-CHoCH-algo-aakash/
- 收集日期: 2026-06-12
- 类型: N03 - 市场结构/突破质量
- 用途: 补 `close-confirmed`、`confirmed swing` 与过滤层边界
- 总代码行数: 758 lines (Pine Script v6)

---

## 概述

This indicator identifies Break of Structure (BOS) and Change of Character (CHoCH) events using confirmed swing highs and lows. The goal is to help traders visualize structural continuation and potential trend transition points while reducing noise through displacement-based confirmation.

---

## 核心特色 (来自 TradingView 页面)

- **Confirmed BOS detection** — 收盘确认的 BOS
- **Confirmed CHoCH detection** — 收盘确认的 CHoCH
- **Internal structure monitoring** — 内部结构监控
- **ATR-based displacement filtering** — ATR 位移过滤
- **EMA momentum confirmation** — EMA 动量确认
- **Volume-based confluence scoring** — 成交量汇合评分
- **Higher timeframe structure overlay** — 高时间框架结构叠加
- **Structural bias ribbon** — 结构偏向 ribbon
- **Non-repainting (confirmed bar-close logic only)** — 明确声明无重绘

---

## 核心参数面板

### Structure Engine

```
i_swingLen: 10 (Swing Length)
  - Lookback period for pivot highs and lows
  - Higher = major structure; lower = minor structure
  - Range: 3-50

i_internalLen: 5 (Internal Swing Length)
  - Secondary swing length for internal CHoCH detection
  - Range: 2-20

i_showBOS: true (Show BOS)
i_showCHoCH: true (Show CHoCH)
i_showInternal: false (Show Internal Structure)
  - Overlay lighter internal BOS/CHoCH signals
```

### Displacement Filter

```
i_displacement: true (Enable Displacement Filter)
i_displacementLen: 14 (ATR Length for displacement)
i_displacementMul: 1.2 (Displacement Multiplier)
  - Break bar body must be > 1.2× ATR to qualify
  - "Volume-weighted body size filter reduces false signals"
```

### Confluence Score (1-4 stars)

```
i_scoreEnable: true (Show Confluence Score)

Scoring factors (each adds 1 point, max 4):
1. Volume Factor (i_volFilter): break bar volume > 1.5× its 20-bar average
2. Momentum Factor (i_maFilter): price on correct side of EMA
3. Displacement strength: body > 1.2× ATR
4. HTF alignment: higher timeframe structure confirms direction

i_emaLen: 50 (EMA Length for momentum check)
```

### Visual Style

```
i_lineStyle: "Solid" (options: Solid, Dashed, Dotted)
i_lineWidth: 1
i_extendLines: false
i_showSwingDots: true (Show Swing Pivot Dots)
i_showZone: true (Show Break Zone Box)
```

### Alerts

```
i_alertBOS: true
i_alertCHoCH: true
i_alertHigh: false (Alert: High Score Only ★★★★)
  - Only trigger when Confluence Score = 4 (all factors confirmed)
```

---

## 核心实现逻辑 (来自源码)

### Swing Detection (Non-Repainting)

```pinescript
swingH = ta.pivothigh(high, i_swingLen, i_swingLen)
swingL = ta.pivotlow(low, i_swingLen, i_swingLen)
```

**关键注释 (来自源码):**
> "Uses ta.pivothigh / ta.pivotlow — values confirmed i_swingLen bars ago, so no repainting occurs."

这意味着：
- Pivot 确认延迟 = `i_swingLen` bars (默认 10 bars)
- 基于已收盘 bar，无前瞻性
- 与 Dots3Red 的 `pivot_len = 7` 类似，但 algo_aakash 用更长的 10

### Displacement Filtering

```pinescript
displacement_impulse = math.abs(close - open) > (atr * i_displacementMul)
// 默认: body > 1.2× ATR
```

与 Dots3Red 对比：
- Dots3Red: `math.abs(close - open) > (atr_raw * ob_mult)` (OB 位移)
- algo_aakash: 专门的 displacement filter 用于 BOS/CHoCH 确认

### Confluence Score 计算

| 条件 | 加分 | 说明 |
|------|------|------|
| Volume > 1.5× 20-bar avg | +1 | 成交量突增确认 |
| Price 在 EMA 正确侧 | +1 | 动量方向一致 |
| Body > 1.2× ATR | +1 | 位移强度足够 |
| HTF alignment | +1 | 高时间框架结构一致 |
| **Total** | **1-4** | **★ to ★★★★** |

---

## 与 N03 需求的映射

| N03 需求字段 | algo_aakash 实现 | 状态 |
|-------------|------------------|------|
| `close-confirmed` | 明确声明 "confirmed bar-close logic only" | ✅ 已实现 |
| `confirmed swing` | `ta.pivothigh/low` with `i_swingLen` bars delay | ✅ 已实现 |
| `displacement / EMA / volume / HTF` | Confluence Score 四因子独立开关 | ✅ 已实现 |
| 过滤层边界 | `i_displacementMul = 1.2` + volume > 1.5× avg | ✅ 可配置 |

---

## Non-Repaint 审计要点

1. **Swing detection**: `ta.pivothigh/low` with `i_swingLen` bars lookback → values confirmed N bars ago
2. **BOS/CHoCH**: Only drawn after bar close confirmation
3. **Displacement**: Uses closed bar's body (close-open) vs ATR
4. **Volume**: Uses closed bar's volume vs 20-bar SMA
5. **EMA**: Uses closed bar's EMA position
6. **明确声明**: "Non-repainting (confirmed bar-close logic only)"

---

## 与 Dots3Red 的对比

| 维度 | Dots3Red (510 lines) | algo_aakash (758 lines) |
|------|---------------------|------------------------|
| Regime Classifier | ✅ ADX + Choppiness + ATR Spike | ❌ 无 regime 分类 |
| Order Blocks | ✅ Regime-adaptive OBs | ❌ 无 OB |
| Fair Value Gaps | ✅ FVG engine | ❌ 无 FVG |
| Confluence Score | ❌ 无 | ✅ 4-factor 1-4 stars |
| HTF Overlay | ❌ 无 | ✅ Higher timeframe structure |
| Internal Structure | ❌ 无 | ✅ Internal swing length |
| Swing Length | 7 | 10 (default) |
| Displacement Filter | OB only | BOS/CHoCH + Volume-weighted |

**结论**: Dots3Red 更完整（regime + OB + FVG），algo_aakash 更专注（BOS/CHoCH + confluence scoring）。两者互补，不重复。

---

## 设置建议 (来自作者 Notes)

- **Swing Length**: 5-7 for intraday, 7-10 for daily/weekly
- **Internal Swing Length**: 3-5 for intraday micro-structure
- **Displacement Multiplier**: 1.0-1.5 for forex, 1.2-2.0 for indices
- **EMA Length**: 20-50 for momentum alignment

---

## 关键审计结论

1. **Non-repainting 实现可信**: 所有信号基于 confirmed bar-close，延迟 = swingLen (默认 10 bars)
2. **Confluence Score 是增量价值**: 4-factor 评分可作为 ADD 候选（★★★★ = 高信心 entry context）
3. **HTF overlay 需谨慎**: 多时间框架叠加在 1H 上可能导致 lookahead，需审计 HTF 数据获取方式
4. **Volume filter 在 CFD 上受限**: FX CFD volume 是 tick volume，1.5× threshold 可能不可靠
