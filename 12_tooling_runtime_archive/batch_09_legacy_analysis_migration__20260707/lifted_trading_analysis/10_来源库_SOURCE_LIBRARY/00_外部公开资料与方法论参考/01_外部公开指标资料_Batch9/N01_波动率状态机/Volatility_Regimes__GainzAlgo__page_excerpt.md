# Volatility Regimes | GainzAlgo 页面摘录

- source_url: https://www.tradingview.com/script/aZUlxrYQ-Volatility-Regimes-GainzAlgo/
- source_kind: TradingView open-source page
- capture_method: WebSearch snippet + direct page fetch shell
- capture_date: 2026-06-12
- supporting_evidence_url: https://www.tradingview.com/script/2z7JVYdK-Volatility-Regimes-GainzAlgo/

## 可确认摘录

- TradingView 搜索摘要显示，该脚本包含 `Volatility Regime Detection`，并将市场划分为 4 个阶段。
- 已抓到的摘要片段包括：
  - `COMPRESSION`: ATR < 70% of baseline
  - `EXPANSION`: ATR 115-140% of baseline
  - `ATR Percentile Ranking`: shows where current ATR ranks historically
  - `Volatility Breakout Signals`: markers when ATR exceeds threshold; default threshold 1.5x ATR average
- 已抓到的功能描述还提到：趋势变化配合 rising ATR、平滑过滤减少假信号。

## 新增补充证据（同标题 TradingView 索引正文）

- 已命中一个同标题的 TradingView 索引页，能拿到比原页更完整的正文说明。
- 正文显示这不是单一 regime 小工具，而是一个 `comprehensive ATR-based trading system`。
- `Volatility Regime Detection acts as the "brain" of the system`，其他组件会跟着 regime 自适应：
  - ATR bands expand/contract with regime changes
  - Stop loss distances automatically adjust
  - Take profit targets scale proportionally
  - Signal sensitivity filters itself based on market phase
- 其底层口径明确写出：
  - `ATR = SMA(True Range, default 14)`
  - `Baseline ATR = SMA or EMA of ATR over long period (default 50 bars)`
  - `ATR Ratio = Current ATR / Baseline ATR`
- 四档 regime 现在可以更明确地记录为：
  - `COMPRESSION`: ratio < 0.70
  - `EXPANSION`: ratio between 1.15 and 1.40
  - `HIGH VOLATILITY`: ratio > 1.40
  - `EXHAUSTION`: ATR declines after a prior high-volatility phase
- 还补到了两条关键工程信息：
  - `Two-stage signal confirmation`: Step 1 = volatility breakout, Step 2 = trend confirmation
  - `Integrated risk management`: dynamic stop loss, position size calculator, proportional take profit

## 可保留细节清单

- source: TradingView supporting evidence page / 2026-06-12
  what: 用 `ATR Ratio = current ATR / baseline ATR` 做 regime 分类
  why: 这是可直接映射的状态机主轴
  repo_mapping: `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\N01_波动率状态机`
- source: TradingView supporting evidence page / 2026-06-12
  what: baseline ATR 默认是 50 bars，当前 ATR 默认 14
  why: 给了最小可复刻参数骨架
  repo_mapping: 后续 N01 字段草案
- source: TradingView supporting evidence page / 2026-06-12
  what: 4 档 regime = compression / expansion / high volatility / exhaustion
  why: 比之前只抓到两档片段强得多
  repo_mapping: N01 诊断标签候选
- source: TradingView supporting evidence page / 2026-06-12
  what: two-stage confirmation = breakout first, trend confirmation second
  why: 说明它不是直接拿 ATR regime 当入场信号
  repo_mapping: 研究侧定义说明，不进当前硬 gate
- source: TradingView supporting evidence page / 2026-06-12
  what: regime 驱动 band/SL/TP/signal sensitivity 一起变化
  why: 说明它是“统一波动框架”而不只是单指标
  repo_mapping: N01 解释层和 ingest 备注
- source: TradingView supporting evidence page / 2026-06-12
  what: integrated risk management 含 position size calculator
  why: 这部分超出当前主线，只能记为背景说明
  repo_mapping: 暂不吸收进当前 FX 主线指标字段

## 当前判断

- 这页目前更像 `vol regime framework / dashboard`，不是单一 squeeze 指标。
- 对本仓库最有价值的是：
  - 4 档 regime 离散化
  - ATR 相对 baseline 的状态划分
  - ATR percentile 历史分位
  - breakout threshold 的状态标记
- 现在可以进一步补充：
  - ATR baseline 默认长窗
  - ATR ratio 是核心状态变量
  - breakout 与 trend confirmation 必须分阶段理解

## 抓取局限

- 原始脚本页直接抓取时，仍然常常只返回页面壳。
- 本文件现在既用了搜索摘要，也用了 TradingView 索引正文的扩展证据，但仍不是源码级证据。
- `supporting_evidence_url` 与原始 `source_url` 虽然同标题，但 script id 不同，因此当前只把它当作强补充证据，不直接宣称与原页完全同一。
- 若后续需要更高置信度，应由用户在浏览器中手动保存脚本页或复制源码页。
