# SMC Indicator 页面摘录

- source_url: https://www.tradingview.com/script/97OKEUwv-SMC-Indicator/
- source_kind: TradingView open-source page
- author: tonngnh3
- capture_method: WebFetch
- capture_date: 2026-06-12

## 关键原文摘录

- `non-repainting detection engine`
- `Pivot Detection (The ZigZag Engine)`
- `High (H): A peak is confirmed when price retraces by the deviation percentage`
- `Low (L): A trough is confirmed when price rallies by the deviation percentage`
- `Ghost Line: A dotted line connects the last confirmed pivot to the current live price`
- `BoS`: trend continuation; `CHoCH`: trend reversal

## 当前判断

- 这页表面上强调 `non-repainting`，但正文同时承认其核心是 `ZigZag Engine + confirmed pivots + ghost line`。
- 因此它更适合作为要重点审计的反例型资料，而不是直接当成已验真无重绘来源。
- 对本仓库的价值在于：
  - 明确写出实时结构和确认结构是两回事
  - ghost line 暗示存在 developing structure 与 locked structure 的区分

## 风险备注

- 只要 swing 点确认依赖回撤百分比或后续价格动作，就不是纯粹的即时结构。
- `ghost line` 很可能是实时预估，不应和最终确认结构混用。
- 该页应保留在 N03 条件收集区，作为重绘/延迟确认审计样本。
