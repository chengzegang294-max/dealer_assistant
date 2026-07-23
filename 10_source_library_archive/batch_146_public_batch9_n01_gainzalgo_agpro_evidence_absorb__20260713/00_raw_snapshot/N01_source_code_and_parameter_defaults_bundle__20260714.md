# N01 Source Code And Parameter Defaults Bundle

更新时间：2026-07-14

## 文件类型

- `ARTIFACT`

## 原路径

- `https://www.tradingview.com/script/2z7JVYdK-Volatility-Regimes-GainzAlgo/`
- `https://www.tradingview.com/script/nCbbDHVD-AG-Pro-ATR-Compression-Map-AGPro-Series/`

## 新路径

- `batch_146/00_raw_snapshot/N01_source_code_and_parameter_defaults_bundle__20260714.md`

## 生成入口

- `manual_source_capture`

## 适用对象

- `Batch9 N01 GainzAlgo / AG Pro`

## 当前作用

- 把 `GainzAlgo` 与 `AG Pro` 当前已见的源码首屏、默认值、参数分组、tooltip 证据收成一页正式证据包。
- 让 `N01` 从“原作者页详细正文”再推进到“源码首屏 + 默认值已正式归档”。

## GainzAlgo 源码首屏证据

- 页面状态：
  - `Open-source script`
  - `Source code`
  - `View in Pine Editor・384 lines`
- 直接可见代码：

```pine
//@version=6
// © GainzAlgo
indicator("Volatility Regimes | GainzAlgo", overlay=true)
var G5 = "Visual Settings"
color upperBandColorInput  = input.color(BAND_COLOR_UPPER, "Upper Band Color", group=G5)
color lowerBandColorInput  = input.color(BAND_COLOR_LOWER, "Lower Band Color", group=G5)
color signalColorInput     = input.color(SIGNAL_COLOR, "Volatility Signal Color", group=G5)
color bullTrendSignalInput = input.color(BULL_COLOR, "Bullish Trend Signal Color", group=G5)
color bearTrendSignalInput = input.color(BEAR_COLOR, "Bearish Trend Signal Color", group=G5)
```

## GainzAlgo 默认值与参数证据

- `ATR Settings`
  - `ATR Length = 14`
- `ATR Bands Settings`
  - `Show ATR Bands = true`
  - `Band 1 Multiplier = 1.0`
  - `Band 2 Multiplier = 2.0`
  - `Band 3 Multiplier = 3.0`
- `Volatility Signals`
  - `Show Volatility Signals = true`
  - `Volatility Threshold = 1.5`
- `Trend Detection`
  - `Show Trend Signals = true`
  - `Trend Smoothing = 21`
- `Regime Calculation`
  - `ATR Baseline Length = 50`
  - `Baseline Type = "SMA"`
- `Regime Thresholds`
  - `Compression Threshold = 0.70`
  - `Expansion Threshold = 1.15`
  - `High Volatility Threshold = 1.40`
  - `Exhaustion Lookback = 5`
- `Regime Visuals`
  - `Show Regime Background = true`
  - `Show Regime Label = true`
  - `Label Position = "Top Right"`
- `Dynamic Stop Loss`
  - `Enable Dynamic Stop Loss = true`
  - `Stop Loss ATR Multiplier = 2.0`
  - `Show SL Lines = true`
- `Take Profit Levels`
  - `Enable Multiple TP Levels = true`
  - `TP1 Multiplier = 1.5`
  - `TP2 Multiplier = 2.5`
  - `TP3 Multiplier = 4.0`
  - `Show TP Labels = true`
- `Support & Resistance`
  - `Enable S/R Levels = true`
  - `S/R Lookback Period = 20`
  - `S/R Strength (ATR) = 1.5`
- `Risk Management`
  - `Enable Risk Calculator = true`
  - `Account Size = 10000`
  - `Risk Per Trade (%) = 1.0`
  - `Show Position Size = true`
- `ATR Percentile`
  - `Enable ATR Percentile = true`
  - `Percentile Lookback = 100`
  - `Show Percentile Label = true`
- `Volatility Contraction`
  - `Enable Contraction Pattern = true`
  - `Contraction Bars = 7`
  - `Contraction Threshold = 0.5`
  - `Show Contraction Alerts = true`

## GainzAlgo 最强参数行

```pine
string regimeLabelPositionInput = input.string("Top Right", "Label Position", options=["Top Left", "Top Right", "Bottom Left", "Bottom Right"], group=G9)
float slMultiplierInput    = input.float(2.0, "Stop Loss ATR Multiplier", minval=0.5, maxval=5.0, step=0.1, group=G10)
float tp1MultiplierInput   = input.float(1.5, "TP1 Multiplier", minval=0.5, maxval=5.0, step=0.1, group=G11)
float tp2MultiplierInput   = input.float(2.5, "TP2 Multiplier", minval=1.0, maxval=10.0, step=0.5, group=G11)
float tp3MultiplierInput   = input.float(4.0, "TP3 Multiplier", minval=2.0, maxval=15.0, step=0.5, group=G11)
float accountSizeInput     = input.float(10000, "Account Size", minval=100, group=G13)
float riskPercentInput     = input.float(1.0, "Risk Per Trade (%)", minval=0.1, maxval=10.0, step=0.1, group=G13)
float contractionThreshold = input.float(0.5, "Contraction Threshold", minval=0.3, maxval=0.8, step=0.05, group=G15)
```

## AG Pro 源码首屏证据

- 页面状态：
  - `OPEN-SOURCE SCRIPT`
  - `Source code`
  - `View in Pine Editor・709 lines`
- 直接可见代码：

```pine
// ATR Compression Map [AGPro Series]
// Author  : AGProLabs | AGPro Series
// Version : 2.1
//@version=6
indicator("ATR Compression Map [AGPro Series]",
     shorttitle = "AG Pro ATR",
     overlay = true,
     max_labels_count = 220,
     max_lines_count = 220,
     max_boxes_count = 120)
```

## AG Pro 默认值与参数证据

- `Core Engine`
  - `ATR Length = 14`
  - `Baseline Length = 50`
  - `Range Window = 20`
  - `Noise Window = 10`
  - `Containment Window = 24`
  - `Compression Threshold = 62.0`
  - `Mature Threshold = 80.0`
  - `Strict Mode = false`
- `Scoring`
  - `ATR Weight = 30.0`
  - `Range Weight = 30.0`
  - `Noise Weight = 20.0`
  - `Containment Weight = 20.0`
- `Compression Pocket`
  - `Show Compression Pocket = true`
  - `Show Pocket Badge = true`
  - `Show Pocket Midline = true`
  - `Show Quarter Guides = true`
  - `Pocket Projection Bars = 18`
  - `Show Archived Pockets = true`
  - `Archived Pocket Count = 3`
  - `Archived Pocket Projection = 45`
  - `Minimum Pocket Bars = 5`
- `Visuals`
  - `Show Compression Ribbon = true`
  - `Show Right-Side Tags = true`
  - `Show Event Labels = true`
  - `Event Label Density = "Normal"`
  - `Label Text Size = "Normal"`
  - `Right Tag Offset = 4`
  - `Color Bars By State = false`
- `Panel`
  - `Show Panel = true`
  - `Panel Location = "Top Right"`
  - `Panel Theme = "Dark"`
  - `Panel Text Size = "Normal"`
- `Alerts`
  - `Alert: Compression Ready = true`
  - `Alert: Mature Compression = true`
  - `Alert: Pocket Release = true`
- `Proof`
  - `Show Proof Layer = true`
  - `Proof Risk Unit (ATR) = 1.20`
  - `Proof Horizon Bars = 30`
  - `Reaction Window Bars = 3`
  - `Reaction Progress % = 40.0`

## AG Pro 最强参数行

```pine
atrLen = input.int(14, "ATR Length", minval = 1, group = G_CORE)
baselineLen = input.int(50, "Baseline Length", minval = 10, maxval = 300, group = G_CORE)
rangeWindow = input.int(20, "Range Window", minval = 5, maxval = 200, group = G_CORE)
noiseWindow = input.int(10, "Noise Window", minval = 3, maxval = 80, group = G_CORE)
containmentWindow = input.int(24, "Containment Window", minval = 5, maxval = 200, group = G_CORE)
compressionThreshold = input.float(62.0, "Compression Threshold", minval = 1.0, maxval = 100.0, step = 1.0, group = G_CORE)
matureThreshold = input.float(80.0, "Mature Threshold", minval = 1.0, maxval = 100.0, step = 1.0, group = G_CORE)
atrWeight = input.float(30.0, "ATR Weight", minval = 0.0, maxval = 100.0, step = 1.0, group = G_SCORE)
rangeWeight = input.float(30.0, "Range Weight", minval = 0.0, maxval = 100.0, step = 1.0, group = G_SCORE)
noiseWeight = input.float(20.0, "Noise Weight", minval = 0.0, maxval = 100.0, step = 1.0, group = G_SCORE)
containmentWeight = input.float(20.0, "Containment Weight", minval = 0.0, maxval = 100.0, step = 1.0, group = G_SCORE)
showPanel = input.bool(true, "Show Panel", group = G_PANEL)
panelPositionInput = input.string("Top Right", "Panel Location", options = ["Top Left", "Top Center", "Top Right", "Middle Left", "Middle Center", "Middle Right", "Bottom Left", "Bottom Center", "Bottom Right"], group = G_PANEL)
panelTheme = input.string("Dark", "Panel Theme", options = ["Dark", "Light"], group = G_PANEL)
panelSizeInput = input.string("Normal", "Panel Text Size", options = ["Tiny", "Small", "Normal", "Large"], group = G_PANEL)
proofStopAtr = input.float(1.20, "Proof Risk Unit (ATR)", minval = 0.30, maxval = 5.00, step = 0.10, group = G_PROOF)
```

## AG Pro 最强 tooltip 证据

```text
Disabled by default to keep price action visually dominant.
Enabled by default for public-release readability.
Normal is the recommended publication default.
These are historical outcome rates, not predictions.
Alerts are attention markers, not trade instructions.
```

## 当前结论

- `N01` 当前已经不是“只有原作者页 detailed methodology”。
- 当前还多了一层：
  - `源码首屏`
  - `正式参数默认值`
  - `tooltip 级默认意图证据`
- 当前剩余缺口已经进一步收缩为：
  - 更完整 Pine 代码段
  - 参数截图
  - 更硬的输入输出联动证据
