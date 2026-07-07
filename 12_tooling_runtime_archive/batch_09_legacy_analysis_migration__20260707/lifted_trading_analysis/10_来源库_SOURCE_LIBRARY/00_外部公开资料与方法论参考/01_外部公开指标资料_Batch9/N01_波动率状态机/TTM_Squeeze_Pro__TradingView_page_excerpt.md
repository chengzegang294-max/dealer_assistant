# TTM Squeeze Pro TradingView 页面摘录

- source_url: https://www.tradingview.com/script/0drMdHsO-TTM-Squeeze-Pro/
- source_kind: TradingView open-source page
- author: Beardy_Fred
- capture_method: WebSearch indexed page body
- capture_date: 2026-06-12

## 关键原文摘录

- `For those unfamiliar with the TTM Squeeze, it is simply a visual way of seeing how Bollinger Bands ... relate to Keltner Channels ... compared with the momentum of the price action.`
- `The concept is that as Bollinger Bands compress within Keltner Channels, price volatility decreases, giving way for a potential explosive price movement up or down.`
- `Both use a 2 standard deviation Bollinger Band`
- `The original squeeze only used a 1.5 ATR Keltner Channel`
- `The pro version uses 1.0, 1.5 and 2.0 ATR Keltner Channels`
- `The Histogram shows price momentum whereas the colored dots ... show where the Bollinger Bands are in relation to the Keltner Channels`
- `Green Dots = No Squeeze / Squeeze Fired`

## 压缩分级口径

- `Orange Dots` = High Compression / large squeeze
- `Red Dots` = Medium Squeeze
- `Black Dots` = Low compression / wide squeeze
- `Green Dots` = No Squeeze / Squeeze Fired

## 当前判断

- 这条页面证据很适合补 N01 的 `compression grading`，因为它把原版和 Pro 版的区别写得很清楚。
- 对本仓库最有价值的不是其彩色显示，而是：
  - `BB vs KC` 的压缩判定框架
  - `1.0 / 1.5 / 2.0 ATR` 三档 Keltner 分层
  - `green dot = squeeze fired`
  - histogram 只负责方向/动量，不等于压缩本身
- 这比只拿一个普通 squeeze 脚本更适合做状态机离散化。

## 可保留细节清单

- source: TradingView indexed page body / 2026-06-12
  what: Pro 版在原始 TTM Squeeze 之上加入 1.0 / 1.5 / 2.0 ATR 三档 KC
  why: 可直接转成 compression tier
  repo_mapping: N01 压缩等级字段草案
- source: TradingView indexed page body / 2026-06-12
  what: green dot 被定义为 no squeeze / squeeze fired
  why: 明确 release 状态
  repo_mapping: N01 squeeze_release 标签
- source: TradingView indexed page body / 2026-06-12
  what: histogram 用于 momentum，而彩点用于 squeeze phase
  why: 避免把动量和压缩状态混成一个信号
  repo_mapping: N01 解释层备注

## Kimi 二次整理稿补充

- `batch9_sources_kimi` 中已补到完整 57 行 Pine 代码，可把这页从“只有正文摘录”提升到“已有代码级补充说明”。
- 可明确补到的实现点：
  - `length = 20`
  - `BB_mult = 2.0`
  - `KC_mult_high / mid / low = 1.0 / 1.5 / 2.0`
  - `sq_color = orange / red / black / green`
  - `Squeeze Fired = NoSqz and not NoSqz[1]`
- 还可补到一个重要审计点：
  - 该版本的 squeeze 条件使用 `or`，不是很多 TTM 变体常见的 `and`
  - 因此它适合代表 `Beardy_Fred` 这个实现口径，不宜自动外推成全部 TTM 版本标准
- 这意味着当前 N01 中：
  - `squeeze_tier`
  - `squeeze_is_on`
  - `squeeze_fired`
  已经有比普通页面摘录更强的实现级支撑

## 最小字段映射建议

- squeeze_tier
- squeeze_is_on
- squeeze_fired
- squeeze_momentum_sign
- squeeze_momentum_accel

## 抓取局限

- 当前正文文件本身仍不是原始源码导出，而是“索引正文 + Kimi 二次整理代码稿”的组合证据。
- 点位颜色和 squeeze 条件在不同脚本实现之间仍可能存在差异，后续若拿到原始源码页，优先再核：
  - 四态命名是否完全一致
  - `or` 是否为作者最终实现
