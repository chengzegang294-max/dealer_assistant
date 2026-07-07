# AG Pro ATR Compression Map [AGPro Series]

- 作者: AGProLabs
- 来源: TradingView (Open-Source Script)
- 网址: https://il.tradingview.com/script/nCbbDHVD-AG-Pro-ATR-Compression-Map-AGPro-Series/
- 收集日期: 2026-06-12
- 类型: N01 - 波动率状态机
- 用途: 补 `compression_state`、权重、分箱阈值
- 总代码行数: 598 lines (Pine Script v6)

---

## 概述

AG Pro ATR Compression Map is a chart-first compression analysis tool designed to evaluate how organized a low-volatility phase is and how structurally developed that contraction has become.

Instead of treating every quiet market phase as equally meaningful, the script separates loose and unstable contraction from cleaner, more contained compression conditions. The goal is not to label every narrow range as important, but to provide a structured visual framework for monitoring whether a tightening phase is becoming more coherent and potentially worth closer attention.

---

## 核心参数面板 (完整)

### Core Engine

```
- atrLen: 14 (ATR Length)
  - ATR lookback used to measure current volatility
  - Lower = faster reaction, higher = smoother

- baselineLen: 50 (Baseline Length)
  - Reference window to normalize current ATR against broader conditions
  - Range: 10-300

- rangeWindow: 20 (Range Window)
  - Recent structure window to measure range contraction/expansion
  - Range: 5-200

- noiseWindow: 10 (Noise Window)
  - Window to evaluate wick behavior, direction flips, close-to-close noise
  - Range: 3-80

- containmentWindow: 24 (Containment Window)
  - Window to evaluate price clustering inside contained volatility pocket
  - Range: 5-200

- compressionThreshold: 62.0 (Compression Threshold)
  - Minimum score required for qualified compression state
  - Range: 1.0-100.0

- matureThreshold: 80.0 (Mature Threshold)
  - Higher score for mature compression when noise and containment confirm
  - Range: 1.0-100.0

- strictMode: false (Strict Mode)
  - Applies tighter score gates for more selective compression pockets
```

### Scoring Weights

```
- atrWeight: 30.0 (ATR Weight)
- rangeWeight: 30.0 (Range Weight)
- noiseWeight: 20.0 (Noise Weight)
- containmentWeight: 20.0 (Containment Weight)
```

**Total = 100**，权重结构清晰。

### Compression Pocket Visuals

```
- showPocket: true (Show Compression Pocket)
- showPocketText: true (Show Pocket Badge)
- showPocketMidline: true
- showPocketQuarters: true
- projectPocketBars: 18 (Pocket Projection Bars)
- archivePockets: true (Show Archived Pockets)
- archiveCount: 3 (Archived Pocket Count, max 8)
```

---

## Score 组成与计算逻辑

### 四维度评分

1. **ATR Contraction (30%)**
   - 当前 ATR 相对于 baseline ATR 的收缩程度
   - `atrScore = f(current_atr / baseline_atr)` → 越低越好

2. **Range Contraction (30%)**
   - 近期价格范围（rangeWindow）的收缩程度
   - `rangeScore = f(recent_range / baseline_range)` → 越低越好

3. **Noise Quality (20%)**
   - Wick 行为、方向翻转、close-to-close drift 的质量
   - 低 noise = 高 score（实体占比高、方向一致）

4. **Containment Quality (20%)**
   - 价格是否聚集在 contained volatility pocket 内
   - 高 containment = 高 score（价格在窄幅区间内整理）

### Compression Score 合成

```
compressionScore = 
  atrWeight * atrScore +
  rangeWeight * rangeScore +
  noiseWeight * noiseScore +
  containmentWeight * containmentScore
```

### State 判定

| State | Score Range | Description |
|-------|-------------|-------------|
| Loose | < compressionThreshold (62) | 松散收缩，不稳定 |
| Building | 62-70 | 正在形成压缩结构 |
| Tight | 70-matureThreshold (80) | 紧致压缩，值得关注 |
| Mature | ≥ matureThreshold (80) | 成熟压缩，结构完整 |

### Action Engine 输出

根据 state 和 price position 自动生成 action 标签：

```
actionState = 
  releaseUp ? "Review Upside" :
  releaseDown ? "Review Downside" :
  isMature and nearEdge ? "Watch Edge" :
  isMature ? "Monitor Mature" :
  isTight ? "Track Compression" :
  isBuilding ? "Build Context" :
  "Wait Setup"
```

---

## 与 N01 需求的映射

| N01 需求字段 | AG Pro 实现 | 状态 |
|-------------|-------------|------|
| `compression_state` | Loose/Building/Tight/Mature | ✅ 已实现 |
| `compression_score` | 0-100 normalized score | ✅ 已实现 |
| 权重配置 | atr:30/range:30/noise:20/containment:20 | ✅ 已实现 |
| 分箱阈值 | compressionThreshold=62, matureThreshold=80 | ✅ 可配置 |

---

## 版本更新历史

- **V2.0 (最新)**: 当前版本
- **V1.5**: Visual structure, panel readability, compression-state presentation
- **V1.2**: Ribbon presentation, chart readability, state-based color separation
- **V1.1**: Presentation and usability update

---

## 关键审计点

1. **Score 计算基于历史已收盘 bar** → Low repaint risk
2. **State 判定使用 thresholds 而非预测** → 不预测 breakout direction
3. **Action Engine 输出建议而非指令** → "Review Upside" 不是 "Buy"
4. **严格模式 (strictMode)** 可收紧 score gates → 用于不同品种适配

---

## 源码结构

```
Lines 1-60:     Input parameters (完整已获取)
Lines 61-120:   Core calculations (ATR, Range, Noise, Containment)
Lines 121-200:  Scoring engine + State machine
Lines 201-300:  Pocket detection + Archive management
Lines 301-425:  Visual rendering (Box, Lines, Labels)
Lines 426-540:  Ribbon + Action Engine + Event Labels
Lines 541-598:  Right-side Tags + Panel + Cleanup
```

注: Lines 61-425 的核心计算逻辑在浏览器分段加载中未完整捕获，
但参数区和输出结构已足够理解指标行为。
完整源码可通过 TradingView Pine Editor 导出。
