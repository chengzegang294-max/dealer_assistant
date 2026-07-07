# BOS and ChoCh Market Structure 页面摘录

- source_url: https://www.tradingview.com/script/UNz4BxUN-BOS-ChoCh-Market-Structure/
- source_kind: TradingView open-source page
- author: Dinkelfras
- capture_method: WebFetch
- capture_date: 2026-06-12

## 关键原文摘录

- `Break of Structure (BOS) occurs when price breaks through a significant pivot level in the direction of the current trend`
- `Change of Character (ChoCh) signals a potential trend reversal`
- `Pivot Strength` = number of candles on each side required to confirm a swing high/low
- `Breakout Confirmation` 可以选 `Close` 或 `Wick`

## 当前判断

- 这页是 N03 非常合格的定义页。
- 最大价值不在信号本身，而在它明确写出了：
  - pivot-based structure
  - close-confirmed vs wick touch
  - BOS continuation vs ChoCh reversal
- 这类页面适合做审计口径，而不是直接拿来当无重绘实现证明。

## 审计提示

- 只要用了 pivot strength，就天然有延迟确认问题。
- 若选择 `Wick` 作为 breakout confirmation，假突破和噪音会显著增加。
- 后续若映射到仓库，只能先作为条件标签，不直接变成 gate。
