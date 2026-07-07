# Batch9 字段落盘优先级清单 v1

## 说明

- 目标：给 `N01 / N02 / N03` 的标准字段排一个实际落盘顺序。
- 这张清单解决的是“先落哪些字段最稳、最有共用价值、最不容易踩定义争议”。
- 当前结论：先从 `L3-ready + planned_same_name` 的字段开始；`L2-conditional` 只做后续候选，不抢先落。

## 优先级定义

- `P0`
  - 可立即准备落盘
  - 定义相对清楚
  - 对后续研究/分桶/索引共用价值最高
- `P1`
  - 第二批落盘
  - 需要依赖 P0 完成后再补上下文或组合关系
- `P2`
  - 暂缓
  - 虽有价值，但定义争议、源码缺口或对象级时序问题还没收清

## 前置依赖

- 先遵守：
  - [Batch9_统一字段命名规范_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/Batch9_统一字段命名规范_v1.md#L1-L227)
- 再参考：
  - [Batch9_统一字段索引表_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/Batch9_统一字段索引表_v1.md#L1-L114)
  - [Batch9_标准字段名到实际落盘名映射表_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/Batch9_标准字段名到实际落盘名映射表_v1.md#L1-L117)

## P0：第一批建议落盘

### N01

- `atr_value`
- `atr_ratio`
- `atr_percentile`
- `atr_percentile_regime`
- `squeeze_is_on`
- `squeeze_tier`
- `squeeze_fired`
- `compression_quality_score`

**原因**
- 定义相对稳
- 能直接支撑波动状态分桶
- 不强依赖争议性对象级逻辑

### N02

- `session_id`
- `session_timezone`
- `opening_range_window_minutes`
- `opening_range_high`
- `opening_range_low`
- `opening_range_mid`
- `opening_range_width`
- `opening_range_width_pct_open`
- `session_open_price`
- `opening_range_defined`
- `first_break_direction`
- `width_error_day`

**原因**
- 这是 N02 最基础的时段上下文层
- 一旦没有这批字段，后面 OR/IB/acceptance 都缺锚点
- 跨市场时段对齐也依赖这批字段

### N03

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
- `structure_event_bar_close_confirmed`

**原因**
- 这是 N03 最小定义层
- 能先把结构事件和审计层分开
- 还没把复杂 confluence 混进来

## P1：第二批建议落盘

### N01

- `atr_baseline_value`
- `atr_regime_is_extreme`
- `atr_regime_is_squeeze`
- `squeeze_momentum_sign`
- `atr_contraction_score`
- `range_tightness_score`
- `noise_cleanliness_score`
- `containment_score`

**原因**
- 这些字段有价值，但更多是 P0 的增强层
- 适合在 P0 跑通后补细化解释与子评分

### N02

- `or_break_high`
- `or_break_low`
- `target_trigger_source`

**原因**
- 这些字段依赖 P0 的 OR 定义先稳定
- 容易受到 `close` vs `high_low` 触发口径影响

### N03

- 当前不建议单独开太多 P1 新字段
- 优先等待 P0 结构定义层稳定后，再决定是否补更细的结构状态字段

## P2：暂缓字段

### N01

- `compression_state`
- `vol_regime_code`
- `vol_breakout_signal`
- `trend_confirmation_after_vol_breakout`
- `squeeze_momentum_accel`
- `atr_percentile_window`

**暂缓原因**
- 仍有源码缺口
- 状态枚举/阈值/二阶段对象逻辑未完全核清

### N02

- `session_bias`
- `ib_high`
- `ib_low`
- `ib_range`
- `ib_break_direction`
- `ib_accept_2period`
- `ib_regime_narrow_or_wide`
- `ib_failed_breakout_event`
- `custom_session_used`
- `session_ma_bias`

**暂缓原因**
- IB 目前主要还是定义文章，不是源码级证据
- `ib_failed_breakout_event` 虽然定义已经更稳，但仍未到源码实现层
- bias/MA bias 也混有较重实现差异

### N03

- `pivot_confirm_delay_bars`
- `confirmed_pivot_non_repaint`
- `structure_label_inherits_pivot_delay`
- `current_bar_visuals_mutable`
- `close_vs_wick_risk_note`
- `future_leak_risk_flag`
- `extra_confluence_used`
- `source_complexity_tier`
- `failed_breakout_event`

**暂缓原因**
- 它们很重要，但大多属于审计层或对象级行为层
- 需要更细的源码级更新时间/延迟确认核验

## 本轮新增收口

- `compression_state`
  - 命名和候选枚举已明显收敛到 `Loose/Building/Tight/Mature`
  - 但因仍缺 AG Pro 原始源码页，继续留在 `P2`
- `ib_failed_breakout_event`
  - 命名和定义已收敛到 `price returns into IB`
  - 但因仍主要来自定义文章，不提前升到 `P1/P0`

## 不进入当前最小落盘层

- `position_size_calculator`
- `dynamic_stop_loss`
- `take_profit_scaling`
- `integrated_risk_management`
- `profit_days`
- `loss_days`
- `error_days`
- `options_premium_decay_logic`
- `FVG`
- `order_block`
- `premium_discount`
- `Fib`
- `regime_adaptation`
- `HTF_overlay`
- `volume_scoring`
- `EMA_momentum_confirmation`

## 当前建议执行顺序

- 第一步：
  - 先做 `P0 / N02`
  - 因为它提供统一 session 与 opening range 锚点
- 第二步：
  - 做 `P0 / N01`
  - 用于补波动环境分桶
- 第三步：
  - 做 `P0 / N03`
  - 把结构事件最小定义层补进来
- 第四步：
  - 再按解释力与稳定性补 `P1`
- 最后：
  - 等更多源码级证据补齐，再考虑 `P2`

## 当前裁决

- 现在不建议直接从最花哨的字段开做。
- 最适合先落的是：
  - N02 的时段锚点
  - N01 的波动状态锚点
  - N03 的结构事件锚点
- 所有 `P2` 字段都要继续保留“未收集完全”备注，不提前冒充成熟字段。
