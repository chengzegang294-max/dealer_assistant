# Volatility Regimes GainzAlgo 手动网页摘录

更新时间：2026-07-14

## 文件类型

- `ARTIFACT`

## 原路径

- `https://www.tradingview.com/script/2z7JVYdK-Volatility-Regimes-GainzAlgo/`

## 新路径

- `batch_146/00_raw_snapshot/Volatility_Regimes__GainzAlgo__manual_web_capture__20260713.md`

## 生成入口

- `manual_webpage_capture`

## 适用对象

- `Batch9 N01 GainzAlgo`

## 当前作用

- 补强 `GainzAlgo` 的网页正文、参数口径与 regime 解释。
- 让 `N01` 不再只依赖历史回收摘录。

## 证据强度

- `manual_webpage_capture`

## 状态

- `active`

## 网页正文摘录

- 页面概述：
  - `This is a comprehensive ATR-based trading system designed for professional traders who need advanced volatility analysis ...`
- 页面来源强度：
  - 当前页就是 `TradingView` 原作者公开脚本页，不再只是二手转述页
- 页面头部信号：
  - `OPEN-SOURCE SCRIPT`
  - `ChartSource code`
  - `View in Pine Editor・384 lines`
- 统一波动率基础：
  - `All calculations share a single ATR baseline calculation`
- ATR 计算：
  - `True Range = Maximum of: Current High - Current Low; |Current High - Previous Close|; |Current Low - Previous Close|`
  - `ATR = Simple Moving Average of True Range over specified period (default: 14)`
- Baseline 与 Ratio：
  - `Baseline ATR = SMA or EMA of ATR over long period (default: 50 bars)`
  - `ATR Ratio = Current ATR ÷ Baseline ATR`
- ATR Bands：
  - `Upper Band = Current Close + (ATR × Band Multiplier)`
  - `Lower Band = Current Close - (ATR × Band Multiplier)`
  - `Band 1: 1.0× ATR`
  - `Band 2: 2.0× ATR`
  - `Band 3: 3.0× ATR`
- Stop Loss：
  - `For Long Positions: Stop Loss = Entry Price - (ATR × SL Multiplier)`
  - `For Short Positions: Stop Loss = Entry Price + (ATR × SL Multiplier)`
  - `Default Multiplier: 2.0× ATR`
- Take Profit：
  - `TP1 = Entry Price ± (ATR × TP1 Multiplier) [default: 1.5×]`
  - `TP2 = Entry Price ± (ATR × TP2 Multiplier) [default: 2.5×]`
  - `TP3 = Entry Price ± (ATR × TP3 Multiplier) [default: 4.0×]`
- Position Size：
  - `Position Size = Account Risk Amount ÷ Stop Loss Distance`
- 信号逻辑：
  - `Bullish: Price > MA AND Current ATR > ATR MA`
  - `Bearish: Price < MA AND Current ATR > ATR MA`

## 源码页可见摘录

- 源码可见性：
  - `Source code`
  - `View in Pine Editor・384 lines`
- 源码首屏可见行：
  - `//@version=6`
  - `// © GainzAlgo`
  - `indicator("Volatility Regimes | GainzAlgo", overlay=true)`
  - `var G5 = "Visual Settings"`
  - `color upperBandColorInput  = input.color(BAND_COLOR_UPPER, "Upper Band Color", group=G5)`
  - `color lowerBandColorInput  = input.color(BAND_COLOR_LOWER, "Lower Band Color", group=G5)`
  - `color signalColorInput     = input.color(SIGNAL_COLOR, "Volatility Signal Color", group=G5)`
  - `color bullTrendSignalInput = input.color(BULL_COLOR, "Bullish Trend Signal Color", group=G5)`
  - `color bearTrendSignalInput = input.color(BEAR_COLOR, "Bearish Trend Signal Color", group=G5)`

## regime 分类摘录

- `COMPRESSION`
  - `Ratio < 0.70`
  - `Market consolidating, volatility contracting, energy building`
- `EXPANSION`
  - `Ratio between 1.15 and 1.40`
  - `Volatility breaking out, early phase of directional movement`
- `HIGH VOLATILITY`
  - `Ratio > 1.40`
  - `Strong sustained trend with high participation`
- `EXHAUSTION`
  - `ATR declining after high volatility period`
  - `Requires: Previous high ratio + declining ATR over X bars (default: 5)`

## 当前可确认的最小计算口径

- `tr = max(high - low, abs(high - prev_close), abs(low - prev_close))`
- `atr = sma(tr, 14)`
- `baseline_atr = sma_or_ema(atr, 50)`
- `atr_ratio = atr / baseline_atr`
- `upper_band = close + atr * band_multiplier`
- `lower_band = close - atr * band_multiplier`
- `long_stop = entry - atr * sl_multiplier`
- `short_stop = entry + atr * sl_multiplier`
- `tp1 = entry +/- atr * 1.5`
- `tp2 = entry +/- atr * 2.5`
- `tp3 = entry +/- atr * 4.0`
- `position_size = account_risk_amount / stop_loss_distance`
- `regime =`
  - `compression` if `atr_ratio < 0.70`
  - `expansion` if `1.15 <= atr_ratio <= 1.40`
  - `high_volatility` if `atr_ratio > 1.40`
  - `exhaustion` if `previous_high_ratio_present and atr_declining_for_x_bars`

## 对 N01 的当前可用价值

- 可补：
  - `definition_page`
  - `regime_interpretation`
  - 大部分 `computation_snippet`
  - 一部分 `parameter_panel`
- 当前仍缺：
  - 更完整 Pine 代码段
  - 更细输入参数面板截图

## 缺口

- 仍需后续补：
  - 更完整 Pine 源码片段或更可审计参数区块
