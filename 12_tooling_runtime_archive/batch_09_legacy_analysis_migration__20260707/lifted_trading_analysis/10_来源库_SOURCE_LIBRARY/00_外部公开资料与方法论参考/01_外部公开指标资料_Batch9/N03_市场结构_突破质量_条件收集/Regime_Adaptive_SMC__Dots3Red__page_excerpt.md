# Smart Money Concepts - Regime-Adaptive SMC 页面摘录

- source_url: https://www.tradingview.com/script/OHQsRH7Z-Smart-Money-Concepts-Regime-Adaptive-SMC-Dots3Red/
- source_kind: TradingView open-source page
- author: Dots3Red
- capture_method: WebSearch indexed page body
- capture_date: 2026-06-12

## 关键原文摘录

- `the same pattern — an Order Block, a Fair Value Gap, a structure break — behaves differently depending on whether the market is trending or ranging`
- `BOS labels confirming continuation` / `CHoCH signals flagging potential reversals`
- `Volatility override: a separate check compares current ATR against its 50-bar SMA`
- `Order Blocks require an additional displacement filter`
- `⚠️ REPAINTING BEHAVIOR — IMPORTANT`
- `The following elements will change on the current bar`
- `BOS/CHoCH labels based on pivots inherit the standard pivot detection delay`
- `Confirmed pivots themselves do not repaint — once a bar is no longer within the pivot lookback window, its pivot status is final.`

## 当前判断

- 这条非常适合补 N03 的 `confirmed pivot + non-repaint disclosure` 样本。
- 它的价值不在于 SMC 全家桶本身，而在于它把三个层次说开了：
  - confirmed pivots 本身的最终性
  - 基于 pivots 的 BOS/CHoCH 自带标准确认延迟
  - live bar 上某些可视元素会变
- 这比一句简单的 `non-repainting` 更适合作审计模板。

## 审计重点

- `Confirmed pivots themselves do not repaint` 只能说明 pivot 最终确认后稳定，不等于事件“即时可交易”。
- `BOS/CHoCH labels based on pivots inherit the standard pivot detection delay` 说明结构标签仍然有滞后。
- regime filter、ATR override、order block displacement filter 属于复杂框架层，不应被误并进 N03 最小定义。

## 可保留细节清单

- source: TradingView indexed page body / 2026-06-12
  what: confirmed pivots 最终不重绘
  why: 可作为 N03 审计口径的关键披露
  repo_mapping: N03 重绘/延迟审计
- source: TradingView indexed page body / 2026-06-12
  what: BOS/CHoCH labels 基于 pivots，因此继承标准 pivot delay
  why: 明确区分“稳定”与“实时”
  repo_mapping: N03 定义层说明
- source: TradingView indexed page body / 2026-06-12
  what: 当前 bar 的 live 元素会变化
  why: 这类说明比泛泛说 non-repaint 更可信
  repo_mapping: N03 审计样本
- source: TradingView indexed page body / 2026-06-12
  what: regime classifier 会改变 trending / ranging / volatile 下展示的结构内容
  why: 说明复杂 SMC 框架已经远超最小 BOS/CHoCH 定义
  repo_mapping: N03 边界说明

## Kimi 二次整理稿补充

- `batch9_sources_kimi` 已补到一批有助于审计边界的参数与实现口径：
  - regime 由 `ADX + Choppiness + ATR Spike` 组合决定
  - `pivot_len = 7`
  - `conf_mode = "Close"`，并允许切换 `Close / Wick`
  - `smooth_len = 6`
  - `vol_thresh = 1.5`
- 这些补充最有价值的地方不是让我们吸收整套 SMC，而是帮助把 N03 边界讲得更清楚：
  - `conf_mode` 直接对应 `close` vs `wick`
  - `pivot_len` 让“标准确认延迟”有了更具体的参数锚点
  - regime / OB / FVG 这些仍应留在复杂框架层，不进入当前最小定义
- Kimi 稿还补到了：
  - OB 位移门控：`abs(close - open) > atr_raw * ob_mult`
  - FVG 检测和 mitigation 的存在
  - 当前 bar 的 regime 状态会实时变化，但结构确认依旧依赖已确认对象
- 因此它更适合作为：
  - N03 审计样本增强
  - `pivot_confirm_delay_bars` 与 `current_bar_visuals_mutable` 的说明来源
  - 而不是直接作为 N03 P0 字段扩容依据

## 当前裁决

- 保留：作为“confirmed pivot 最终稳定，但结构信号仍有标准延迟”的复杂 open-source 样本
- 不做：不把其 order block / FVG / premium-discount / regime adaptation 全部吸收到当前 N03 最小定义
- 后续若补原始源码页，应优先核：live pivot、confirmed pivot、BOS/CHoCH 标签这三类对象的更新时机
