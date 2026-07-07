# Institutional Market Structure BOS and CHoCH 页面摘录

- source_url: https://fr.tradingview.com/script/UjDVwAtJ-Institutional-Market-Structure-BOS-and-CHoCH-algo-aakash/
- source_kind: TradingView open-source page
- author: algo_aakash
- capture_method: WebSearch indexed page body
- capture_date: 2026-06-12

## 关键原文摘录

- `This indicator identifies Break of Structure (BOS) and Change of Character (CHoCH) events using confirmed swing highs and lows.`
- `The goal is to help traders visualize structural continuation and potential trend transition points while reducing noise through displacement-based confirmation.`
- `Features: Confirmed BOS detection / Confirmed CHoCH detection / Internal structure monitoring / ATR-based displacement filtering / EMA momentum confirmation / Volume-based confluence scoring / Higher timeframe structure overlay / Structural bias ribbon`
- `The script identifies confirmed swing highs and lows using pivot-based structure analysis.`
- `Once price closes beyond a tracked structure level, the event is classified as either: BOS when aligned with the prevailing structure direction; CHoCH when opposing the prevailing structure direction`
- `Limitations: Pivot confirmation introduces delay by design.`

## 当前判断

- 这条很适合作为 N03 的“中高复杂度定义页”。
- 它的价值不在于全部过滤器，而在于它把三层东西分开写清了：
  - confirmed swings
  - close beyond tracked level
  - displacement / EMA / volume 这些是额外 confluence，不是 BOS/CHoCH 定义本身
- 这正好有利于我们把 N03 边界守住：先收定义，再把过滤器记为审计层。

## 审计重点

- `pivot-based structure analysis` 说明它天然存在确认延迟，不能误称“即时结构”。
- `price closes beyond a tracked structure level` 是比较干净的 close-confirmed 口径，应单独保留。
- `ATR-based displacement filtering / EMA confirmation / volume scoring / HTF overlay` 明显已经进入扩展过滤层，不能混入最小定义。

## 可保留细节清单

- source: TradingView indexed page body / 2026-06-12
  what: BOS/CHoCH 的基础事件依赖 confirmed swing highs/lows
  why: 可作为 N03 最小定义锚点之一
  repo_mapping: N03 定义层
- source: TradingView indexed page body / 2026-06-12
  what: 结构突破要求 price closes beyond tracked level
  why: 适合与 wick-only break 明确区分
  repo_mapping: N03 close-confirmed 口径
- source: TradingView indexed page body / 2026-06-12
  what: displacement / EMA / volume / HTF overlay 是附加 confluence
  why: 方便把定义层与过滤层拆开
  repo_mapping: N03 审计层
- source: TradingView indexed page body / 2026-06-12
  what: pivot confirmation introduces delay by design
  why: 是反重绘表述里必须保留的披露
  repo_mapping: N03 重绘/延迟审计

## Kimi 二次整理稿补充

- `batch9_sources_kimi` 已补到更接近实现层的关键片段：
  - `swingH = ta.pivothigh(high, i_swingLen, i_swingLen)`
  - `swingL = ta.pivotlow(low, i_swingLen, i_swingLen)`
  - `i_swingLen = 10`
  - `i_internalLen = 5`
  - `displacement_impulse = abs(close - open) > atr * 1.2`
- 这让当前页面摘录可以更明确地区分三层：
  - 定义层：confirmed swing + close beyond tracked level
  - 过滤层：displacement / EMA / volume / HTF alignment
  - 评分层：1-4 星 confluence score
- Kimi 稿还补到了较清楚的 confluence 组成：
  - volume > `1.5x` 20-bar average
  - price 在 EMA 正确侧
  - body > `1.2x ATR`
  - HTF alignment
- 这些信息的作用是帮助我们守边界：
  - 可以更稳地把 `close-confirmed` 与 `confirmed swing` 留在 N03 定义层
  - 把 EMA / volume / HTF 继续留在过滤层或审计层
  - 不把 4 因子评分提前混进当前 P0
- 还要保留一个风险提醒：
  - HTF overlay 仍存在 lookahead 风险，需要等原始源码进一步核
  - volume 因子在 FX CFD 上也可能只是 tick volume 代理量

## 当前裁决

- 保留：作为 N03 `confirmed-swing + close-confirmed + extra confluence` 的清晰样本
- 不做：不把 EMA / volume / HTF overlay 直接吸收到当前 N03 最小定义
- 后续若拿到原始源码页，再核查 displacement filter 是否作用于事件触发还是只作用于显示/评分
