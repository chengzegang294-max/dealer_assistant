# Batch9 指标字段总表 v1

## 目的

- 把 `N01 / N02 / N03` 当前已能映射的字段、条件字段、未补完缺口放在一张表里。
- 这是一张“当前仓库可映射程度”总表，不代表已经全部收集完成。
- 当前结论：三类都已经能做 v1，但**都仍未收集完全**。

## 总览

| type_id | 类型 | 当前状态 | 可先落盘字段 | 条件字段 | 主要未补完缺口 |
|---|---|---|---|---|---|
| `N01` | 波动率状态机 | v1 可映射 | ATR / percentile / squeeze / compression quality | regime code / breakout step2 / compression state | GainzAlgo 仍缺源码页，AG Pro 仍缺核心计算段源码，shock persistence 仍未系统补齐 |
| `N02` | 时段/开盘区间结构 | v1 可映射 | OR 高低宽、时区、首破方向、width error | IB acceptance、failed breakout、session bias | 缺多市场 session 样本、IB 源码页、failed ORB 对象字段 |
| `N03` | 市场结构/突破质量 | v1 可映射 | confirmed swing、break mode、BOS/CHOCH、结构方向 | pivot delay、non-repaint 对象级披露、extra confluence | 缺源码级时序核验、过滤层归属核验、failed breakout 对象字段 |

## N01 摘要

- 可先落盘字段：
  - `atr_value`
  - `atr_baseline_value`
  - `atr_ratio`
  - `atr_percentile`
  - `atr_percentile_regime`
  - `squeeze_is_on`
  - `squeeze_tier`
  - `squeeze_fired`
  - `compression_quality_score`
- 条件字段：
  - `compression_state`
  - `vol_regime_code`
  - `vol_breakout_signal`
  - `trend_confirmation_after_vol_breakout`
- 当前缺口：
  - GainzAlgo 仍缺源码级证据
  - AG Pro 已补到枚举/权重/阈值骨架，但仍缺核心计算段源码
  - TTM 当前补到的是 Beardy_Fred 版本，`or` 口径不能自动外推全部 TTM 变体
  - realized vol persistence / vol-of-vol 还没系统补齐

见 [N01_字段草案_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N01_波动率状态机/N01_字段草案_v1.md#L1-L94)

## N02 摘要

- 可先落盘字段：
  - `session_id`
  - `session_timezone`
  - `opening_range_window_minutes`
  - `opening_range_high`
  - `opening_range_low`
  - `opening_range_mid`
  - `opening_range_width`
  - `opening_range_width_pct_open`
  - `first_break_direction`
  - `width_error_day`
- 条件字段：
  - `session_bias`
  - `ib_high / ib_low / ib_range`
  - `ib_break_direction`
  - `ib_accept_2period`
  - `ib_regime_narrow_or_wide`
  - `ib_failed_breakout_event`
- 当前缺口：
  - 多市场 open/session 样本不足
  - IB 目前只有定义文章，没有源码级证据
  - failed ORB / reclaim / acceptance 对象字段还没系统补齐

见 [N02_字段草案_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N02_时段_开盘区间结构/N02_字段草案_v1.md#L1-L97)

## N03 摘要

- 可先落盘字段：
  - `swing_mode`
  - `swing_left_bars`
  - `swing_right_bars`
  - `swing_high_confirmed`
  - `swing_low_confirmed`
  - `break_confirmation_mode`
  - `break_level_price`
  - `bos_event`
  - `choch_event`
  - `structure_direction`
- 条件字段：
  - `pivot_confirm_delay_bars`
  - `confirmed_pivot_non_repaint`
  - `structure_label_inherits_pivot_delay`
  - `current_bar_visuals_mutable`
  - `future_leak_risk_flag`
  - `extra_confluence_used`
- 当前缺口：
  - Dots3Red 已补到 `pivot_len=7` 与 `conf_mode=Close/Wick`，但仍缺源码级更新时机核验
  - algo_aakash 已补到 `ta.pivothigh/low`、`swingLen=10` 与 4 因子 confluence，但过滤层归属仍未核清
  - failed breakout 还没成一套对象级字段

见 [N03_字段草案_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N03_市场结构_突破质量_条件收集/N03_字段草案_v1.md#L1-L90)

## 当前裁决

- `N01 / N02 / N03` 都已经从“纯资料收集”进入“可映射字段草案”阶段。
- 现阶段最适合先做研究侧字段索引，不宜直接升成策略 gate。
- 后续补资料时，优先补“影响字段定义”的缺口，而不是继续堆低价值网页。
