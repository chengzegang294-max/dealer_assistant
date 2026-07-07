# Squeeze for MetaTrader 5 页面摘录

- source_url: https://www.mql5.com/en/code/24731
- source_kind: MQL5 CodeBase
- author: Mladen Rakic
- capture_method: WebFetch
- capture_date: 2026-06-12

## 关键原文摘录

- `when standard deviation value is greater than average true range, then the market is supposed to be trending`
- `when standard deviation value is less than average true range, then the market is supposed to be consolidating (ranging)`
- `When the value of it is zero, then the market is in a "squeeze" mode (consolidating).`
- `When the value is different from 0, then it compares median price to average close ... above the average = trend up ... below the average = trend down`

## 当前判断

- 这是一个很干净的 squeeze 定义页，核心是 `stddev vs ATR`。
- 对本仓库最有价值的是两层逻辑：
  - squeeze / non-squeeze 的零值状态
  - 非零后再判断 trend up / trend down
- 这比泛泛的波动大/波动小更容易做成状态机字段。

## 适合吸收的最小字段

- squeeze_on
- squeeze_state
- trend_bias_after_release
- stddev_vs_atr_ratio

## 备注

- 当前只落页面摘录，后续可继续补 `.mq5` 源码。
