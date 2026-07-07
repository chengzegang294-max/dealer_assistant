# ATR Regime Study [CHE] 页面摘录

- source_url: https://www.tradingview.com/script/uHAIENY5/
- source_kind: TradingView open-source page
- author: CHE
- capture_method: WebSearch indexed page body
- capture_date: 2026-06-12

## 关键原文摘录

- `This study classifies volatility into five regimes by converting ATR into a percentile rank over a rolling window`
- `That value is mapped to one of five regimes: above ninety (Extreme), between seventy and ninety (Elevated), between thirty and seventy (Normal), between ten and thirty (Calm), and below ten (Squeeze).`
- `The standardized scale makes symbols and timeframes easier to compare than raw ATR values.`
- `Percentile ranking of ATR within a rolling window.`
- `Five discrete regimes with fixed thresholds at ninety, seventy, thirty, and ten.`
- `No higher-timeframe requests are used, so repaint risk is limited to normal live-bar fluctuation until the bar closes.`

## 当前判断

- 这条正好补上 N01 里还缺的 `regime/percentile/extreme` 明确分档页。
- 它比普通 ATR percentile 页更有价值，因为不只是给一个阈值，而是给了：
  - 五档 regime 命名
  - 固定 percentile 阈值
  - 跨品种/跨周期可比性的解释
- 这适合给 N01 增加统一的 `atr_percentile_regime` 命名层。

## 可保留细节清单

- source: TradingView indexed page body / 2026-06-12
  what: ATR 被转成 rolling percentile rank，再映射到五档 regime
  why: 适合作为标准化波动状态机
  repo_mapping: N01 regime 字段草案
- source: TradingView indexed page body / 2026-06-12
  what: 五档阈值为 90 / 70 / 30 / 10
  why: 这是最直接可复刻的分箱口径
  repo_mapping: N01 percentile bucket 说明
- source: TradingView indexed page body / 2026-06-12
  what: 标准化尺度提升 cross-asset / cross-timeframe comparability
  why: 对我们后面统一指标家族很有帮助
  repo_mapping: N01 研究说明
- source: TradingView indexed page body / 2026-06-12
  what: repaint risk 限于 live bar fluctuation until the bar closes
  why: 给 close 后状态落盘提供了清晰边界
  repo_mapping: N01 审计备注

## 最小字段映射建议

- atr_percentile
- atr_percentile_regime
- atr_regime_is_extreme
- atr_regime_is_squeeze
- atr_percentile_window

## 抓取局限

- 当前拿到的是 TradingView 索引正文，不是源码页。
- 阈值和 regime 命名已经足够清楚，但尚未核到 table / label 的具体输出字段名。
- 若后续用户补源码页，优先核对：percentile 计算函数、窗口默认值、regime 字符串枚举。
