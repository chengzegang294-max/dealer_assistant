# Batch9 待用户手动补网页清单 v1

## 说明

- 你现在有空的话，就补这张单子里最前面的页面。
- 原则：优先补“我已摘录但还不是源码级证据”的页，尤其是 TradingView 难抓页。
- 你补回来的形式可以是：
  - 网页另存 `html`
  - 浏览器复制的正文 `md/txt`
  - open-source 页里的源码复制版
  - 页面截图加链接

## 最优先：现在就值得补

### N02

1. `Initial Balance Breakout Strategy for Day Traders`
   - 作者/来源：`MarketProfile.info`
   - 网页地址：`https://marketprofile.info/articles/initial-balance-breakout-strategy`
   - 用途：补 `ib_high / ib_low / ib_range / ib_accept_2period`
  - 当前状态：已有页面摘录 + Kimi 整理的较完整正文，仍不是源码级证据
   - 建议你补：
     - 全文另存
     - 文中关于 `2 periods outside IB` 的原文段落
     - 若能找到作者配套源码/图表示例更好

### N01

2. `Volatility Regimes | GainzAlgo`
   - 作者/来源：`GainzAlgo`
   - 网页地址：`https://www.tradingview.com/script/aZUlxrYQ-Volatility-Regimes-GainzAlgo/`
   - 用途：补 `vol_regime_code / vol_breakout_signal / trend_confirmation_after_vol_breakout`
   - 当前状态：已做扩展正文证据，但仍缺源码页
   - 建议你补：
     - open-source 脚本页源码
     - 若源码页打不开，至少补完整正文和参数区

3. `AG Pro ATR Compression Map`
   - 作者/来源：`AGPro Series`
   - 网页地址：`https://il.tradingview.com/script/nCbbDHVD-AG-Pro-ATR-Compression-Map-AGPro-Series/`
   - 用途：补 `compression_state`、权重、分箱阈值
  - 当前状态：已有正文摘录 + Kimi 整理的状态枚举/权重/阈值，仍缺源码页
   - 建议你补：
     - 状态枚举名
     - score 组成项和权重
     - 参数面板或源码片段

### N03

4. `Regime-Adaptive SMC | Dots3Red`
   - 作者/来源：`Dots3Red`
   - 网页地址：`https://www.tradingview.com/script/OHQsRH7Z-Smart-Money-Concepts-Regime-Adaptive-SMC-Dots3Red/`
   - 用途：补 `confirmed_pivot_non_repaint / current_bar_visuals_mutable / pivot_confirm_delay_bars`
  - 当前状态：已有正文摘录 + Kimi 整理的参数面板/分层结构，审计价值高，但仍缺源码级对象时机核验
   - 建议你补：
     - 关于 non-repaint / delay 的原文段
     - 若有源码，补 pivot confirm 相关部分

5. `Institutional Market Structure BOS and CHoCH | algo_aakash`
   - 作者/来源：`algo_aakash`
   - 网页地址：`https://fr.tradingview.com/script/UjDVwAtJ-Institutional-Market-Structure-BOS-and-CHoCH-algo-aakash/`
   - 用途：补 `close-confirmed`、`confirmed swing` 与过滤层边界
  - 当前状态：已有页面摘录 + Kimi 整理的 pivot/位移/confluence 细节，仍缺完整源码核验
   - 建议你补：
     - 源码或完整正文
     - displacement / EMA / volume / HTF 的作用说明

## 第二优先：有空再补

### N01

6. `TTM Squeeze Pro`
   - 作者/来源：`Beardy_Fred`
   - 网页地址：`https://www.tradingview.com/script/0drMdHsO-TTM-Squeeze-Pro/`
   - 用途：补 `squeeze_tier` 细节和 fired 逻辑
  - 当前状态：已摘录，且 Kimi 已整理出完整代码；当前缺口已明显缩小

7. `ATR Regime Study [CHE]`
   - 作者/来源：`CHE`
   - 网页地址：`https://www.tradingview.com/script/uHAIENY5/`
   - 用途：补 `atr_percentile_regime` 阈值与 panel 字段
   - 当前状态：已摘录，仍缺源码/表格字段名

### N03

8. `BOS & ChoCh Market Structure`
   - 作者/来源：`Dinkelfras`
   - 网页地址：`https://www.tradingview.com/script/UNz4BxUN-BOS-ChoCh-Market-Structure/`
   - 用途：补 `break_confirmation_mode` 的源码级口径
   - 当前状态：已摘录

9. `SMC Indicator`
   - 作者/来源：`QuantitativeEdge`
   - 网页地址：`https://www.tradingview.com/script/97OKEUwv-SMC-Indicator/`
   - 用途：核验其 `non-repainting detection engine` 是否只是话术
   - 当前状态：已摘录，但需谨慎审计

10. `Smart Money Structure | GainzAlgo`
   - 作者/来源：`GainzAlgo`
   - 网页地址：`https://www.tradingview.com/script/HKBMUhq3-Smart-Money-Structure-GainzAlgo/`
   - 用途：补复杂结构框架的过滤层/无重绘主张
   - 当前状态：仅作为审计样本，不进当前最小字段

## 你补回来后我最需要什么

- 最好文件名里带来源名
- 最好附原始链接
- 如果是源码复制，尽量不要删参数区和注释
- 如果你只来得及做一半，优先给我：
  - `GainzAlgo Volatility Regimes`
  - `Initial Balance Breakout`
  - `Dots3Red Regime-Adaptive SMC`

## 回传落点建议

- 先临时放到：
  - `d:\Stock\trading_analysis\10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9`
- 若是 `N01 strictMode / AG Pro` 这一类 Kimi 追问回帖，优先放到：
  - `d:\Stock\trading_analysis\10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\batch9_sources_kimi\N01\strictMode_kimi_followup`
- 若是书类/PDF 整理稿，优先放到：
  - `d:\Stock\trading_analysis\10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库`
- 我再按类型帮你归位并更新 manifest

## 当前裁决

- 你现在就可以补，不用等我。
- 最值钱的是：
  - N02 的 IB 页面
  - N01 的 GainzAlgo / AG Pro
  - N03 的 Dots3Red / algo_aakash
