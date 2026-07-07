# Smart Money Structure GainzAlgo 页面摘录

- source_url: https://www.tradingview.com/script/HKBMUhq3-Smart-Money-Structure-GainzAlgo/
- source_kind: TradingView open-source page
- author: GainzAlgo
- capture_method: WebSearch indexed page body
- capture_date: 2026-06-12

## 关键原文摘录

- `Smart Money Structure Analysis is a professional-grade market structure and order-flow system`
- `identify Change of Character (CHoCH), Break of Structure (BOS), cumulative volume dynamics, and trend convergence across seven timeframes`
- `Volatility adjusts signal sensitivity in real time`
- `Multi-timeframe trends define directional bias`
- `Market structure determines timing`
- `Volume confirms institutional participation`
- `Every signal must pass through up to six independent confirmation layers`
- `Pivot-based swing logic`
- `Candle confirmation`
- `Non-repainting visualization`

## 当前判断

- 这条不是 N03 当前边界内的“纯定义页”，而是一个复杂框架样本。
- 它的价值主要在于展示：
  - 结构检测如何和波动、量能、多周期偏置绑在一起
  - 一个现代 TradingView 结构脚本如何自称 `non-repainting visualization`
  - 复杂框架通常会把 `BOS/CHoCH` 外挂到更多过滤器之上
- 正因为它太复杂，所以当前只能作为 `审计样本`，不能直接拿来当 N03 定义标准。

## 审计重点

- 它明确承认有 `pivot-based swing logic`，因此仍需核查确认延迟。
- `candle confirmation` 是正面信号，但必须区分：
  - 结构点确认是否滞后
  - 结构突破是否 close-confirmed
- `seven timeframes`、`volume confirmation`、`liquidity zone detection` 等内容已经超出当前 N03 只收定义/确认逻辑的边界。

## 可保留细节清单

- source: TradingView indexed page body / 2026-06-12
  what: CHoCH/BOS 被置于波动自适应、多周期和量能过滤之下
  why: 可作为复杂结构框架样本
  repo_mapping: N03 审计样本区
- source: TradingView indexed page body / 2026-06-12
  what: 显式声明 pivot-based swing logic + candle confirmation + non-repainting visualization
  why: 便于逐项拆“无重绘”主张
  repo_mapping: N03 重绘审计清单
- source: TradingView indexed page body / 2026-06-12
  what: 六层过滤与七周期融合
  why: 说明其已超出当前主线的最小定义边界
  repo_mapping: 仅来源库保留，不直接进当前实现

## 当前裁决

- 保留：作为高复杂度 open-source 结构框架样本
- 不做：不把其 MTF / CVD / liquidity / profile 组合逻辑直接吸收到 N03 当前定义层
- 后续若用户手动补源码页，再单独做“声明 vs 实现”的逐项核验
