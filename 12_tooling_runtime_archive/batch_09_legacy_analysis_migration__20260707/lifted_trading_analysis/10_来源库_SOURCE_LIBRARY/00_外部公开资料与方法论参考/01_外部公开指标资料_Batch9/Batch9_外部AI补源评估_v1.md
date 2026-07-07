# Batch9 外部AI补源评估 v1

## 目的

- 评估 `batch9_sources_kimi` 与临时粘贴区多 AI 回复是否能直接吸收进 Batch9。
- 明确区分：
  - 可直接补强现有证据
  - 只能当二次整理稿
  - 仍不能算“补全”
  - 与现有证据存在冲突

## 本轮评估口径

- `A_强可用`
  - 含完整源码、原文全文、或可直接核对的关键原始片段。
- `B_可补强`
  - 信息量明显增加，但仍是二次整理稿，不是原始源码/原始网页落盘。
- `C_仅线索`
  - 只能提供搜索方向、访问状态或后续核验提示。
- `X_结论冲突`
  - 与现有 Batch9 证据冲突，不能直接纳入裁决。

## 按文件评估

| 文件 | 类型 | 本轮等级 | 是否可算补全 | 结论 |
|---|---|---|---|---|
| `N01\02_gainzalgo_volatility_regimes_STATUS.md` | N01 | `X_结论冲突 + C_仅线索` | 否 | 可保留“访问失败/疑似闭源”线索，但不能据此把 GainzAlgo 从现有清单移除 |
| `N01\03_ag_pro_atr_compression_map_tradingview.md` | N01 | `B_可补强` | 否 | 明显补到权重、阈值、状态枚举，但仍不是完整源码原件 |
| `N01\06_ttm_squeeze_pro_tradingview.md` | N01 | `A_强可用` | `部分补全` | 已含完整 Pine 代码，可显著补齐 `squeeze_tier / squeeze_fired` 证据 |
| `N02\01_initial_balance_breakout_strategy_marketprofile.info.md` | N02 | `A_强可用` | `部分补全` | 已接近全文整理，可补强 `IB` 定义与 `2 periods outside IB` 语义 |
| `N03\04_dots3red_regime_adaptive_smc_tradingview.md` | N03 | `B_可补强` | 否 | 参数与边界信息更完整，但关键 non-repaint 仍多为转述，不是源码原件 |
| `N03\05_algo_aakash_bos_choch_tradingview.md` | N03 | `B_可补强` | `部分补全` | 已补到 pivot / displacement / confluence 细节，但仍需原始源码全量核验 |

## 逐项判断

### 1. GainzAlgo

- 当前 Kimi 文件可用之处：
  - 提供了 `404 / 付费页 / 无公开源码` 这条收集线索。
- 不能直接采用之处：
  - 现有 [Volatility_Regimes__GainzAlgo__page_excerpt.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N01_波动率状态机/Volatility_Regimes__GainzAlgo__page_excerpt.md) 已有同标题索引正文与补充证据。
  - 因此不能直接下结论说“当前来源不存在”或“从清单删除”。
- 当前裁决：
  - 继续保留在 N01 缺口清单中。
  - 可新增备注：`Kimi 访问失败，疑似闭源/改链，待人工浏览器复核。`

### 2. AG Pro ATR Compression Map

- 相比现有 [AG_Pro_ATR_Compression_Map__page_excerpt.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N01_波动率状态机/AG_Pro_ATR_Compression_Map__page_excerpt.md)，Kimi 新增了：
  - 四项权重：`30 / 30 / 20 / 20`
  - 阈值：`compressionThreshold=62`、`matureThreshold=80`
  - 状态枚举：`Loose / Building / Tight / Mature`
  - 参数面板骨架
- 仍然缺：
  - 核心计算段原始源码
  - 原页面或 Pine Editor 全量导出
- 当前裁决：
  - 可作为 `compression_state`、权重、阈值的强补充证据。
  - 仍不能宣称“AG Pro 已源码级补全”。

### 3. TTM Squeeze Pro

- 这份文件最有价值：
  - 直接给出完整 57 行 Pine Script。
  - 已可核对：
    - `1.0 / 1.5 / 2.0` 三档 KC
    - `No / Low / Mid / High` 四态
    - `Squeeze Fired = NoSqz and not NoSqz[1]`
- 需要保留的审计提醒：
  - 当前实现用的是 `or`，不是很多 TTM 版本常见的 `and`。
  - 所以它适合作为“Beardy_Fred 版本口径”，不能自动代表全部 TTM 变体。
- 当前裁决：
  - 可把 N01 的 `squeeze_tier / squeeze_fired` 证据强度上调。
  - 可视为 N01 的一项实质性补全。

### 4. Initial Balance Breakout

- 相比现有 [Initial_Balance_Breakout__page_excerpt.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N02_时段_开盘区间结构/Initial_Balance_Breakout__page_excerpt.md)，Kimi 新增了：
  - 更完整的文章结构
  - breakout 类型划分
  - `failed breakout = price returns into IB`
  - 风险管理与 target 说明
- 仍然缺：
  - IB 相关源码实现
  - 会话对象级字段与 bar 级计算例子
- 当前裁决：
  - 这能补强 N02 的定义层，但不能让 `ib_*` 直接晋升为源码级字段。

### 5. Dots3Red Regime-Adaptive SMC

- 相比现有 [Regime_Adaptive_SMC__Dots3Red__page_excerpt.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N03_市场结构_突破质量_条件收集/Regime_Adaptive_SMC__Dots3Red__page_excerpt.md)，Kimi 新增了：
  - `ADX + Choppiness + ATR Spike` 的 regime 组合口径
  - `pivot_len=7`、`conf_mode="Close"` 等参数面板
  - OB / FVG / regime adaptation 的分层结构
- 仍然缺：
  - 关键 non-repaint 代码原文
  - live pivot、confirmed pivot、label refresh 的对象级更新时机
- 当前裁决：
  - 可补强 N03 审计说明。
  - 不能据此把 `confirmed_pivot_non_repaint` 判成“已完全核实”。

### 6. algo_aakash BOS/CHoCH

- 相比现有 [Institutional_Market_Structure_BOS_CHoCH__algo_aakash__page_excerpt.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N03_市场结构_突破质量_条件收集/Institutional_Market_Structure_BOS_CHoCH__algo_aakash__page_excerpt.md)，Kimi 新增了：
  - `ta.pivothigh/ta.pivotlow` 原始函数级片段
  - `i_swingLen=10`、`i_internalLen=5`
  - `displacement > 1.2 * ATR`
  - confluence score 四因子
- 仍然缺：
  - 完整源码全文
  - HTF overlay 的 lookahead 风险核验
- 当前裁决：
  - 已能更稳地支撑“confirmed swing + close-confirmed + confluence 是分层关系”。
  - 仍不能把过滤层逻辑直接混进 N03 P0。

## 对现有 Batch9 的实际影响

- `N01`
  - `TTM Squeeze Pro` 可视为明显补强，且接近可关闭该子缺口。
  - `AG Pro` 由“只有页面摘录”升级为“已有阈值/权重/状态二次证据”，但未彻底补全。
  - `GainzAlgo` 仍保留未完成标记，不能删除。
- `N02`
  - `Initial Balance` 的定义层已经更完整，但 `IB` 仍未达到源码级证据标准。
- `N03`
  - `algo_aakash` 与 `Dots3Red` 都能强化边界说明。
  - N03 仍旧只适合作定义层与审计层拆分，不适合把复杂 SMC 全家桶推入 P0。

## 对其他 AI 回复的裁决

- `Kimi`
  - 当前最有用。
  - 优势是收集推进快、整理成稿能力强。
  - 风险是会把“访问结果”直接上升为“最终裁决”，因此必须和现有证据交叉核验。
- `GLM`
  - 适合吸收它的收集流程、命名规范、fallback 方案。
  - 不适合把其推测性结论直接写进来源裁决。
- `豆包 / 千问`
  - 更适合做补充清单和一致性复述。
  - 对当前“是否补全”的新增信息价值有限。
- `DeepSeek`
  - 这轮基本没有形成可审计新增证据。

## 当前总裁决

- 可以直接吸收进 Batch9 的：
  - `TTM Squeeze Pro` 的完整代码信息
  - `Initial Balance` 的更完整文章内容
  - `AG Pro / Dots3Red / algo_aakash` 的结构化补充说明
- 仍不能视作“已经补全”的：
  - `GainzAlgo`
  - `AG Pro` 全量源码
  - `Dots3Red` non-repaint 对象级核验
  - `algo_aakash` 全量源码与 HTF 风险
  - `IB` 源码级实现

## 推荐下一步

- 先做最小吸收：
  - 把 Kimi 的可用内容并入现有缺口备注与目录说明。
- 再做证据分层：
  - 给 Kimi 这批加一个统一标签：`secondary_structured_note`。
- 暂不做错误动作：
  - 不根据 Kimi 的 GainzAlgo 状态文件把原来源从 manifest 删掉。
- 若继续推进最顺：
  - 下一步可把 `batch9_sources_kimi` 里的 5 份可用稿正式归档，并更新 `manifest notes + 00_本批说明`。
