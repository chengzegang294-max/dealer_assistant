# Batch9 标准字段名到实际落盘名映射表 v1

## 说明

- 目标：把“标准字段名”和“实际落盘名 v1”之间的关系写清楚。
- 这张表解决的是命名收口，不是假装这些字段都已经进了代码或 CSV。
- 当前结论：大多数 `L3-ready` 字段建议未来直接按标准名落盘；`L2-conditional` 多数仍是保留标准名；`L1-context-only` 不进入当前最小落盘层。

## 映射状态

- `planned_same_name`
  - 标准字段名 = 建议实际落盘名
  - 当前还未必已经进代码/CSV，但后续落盘建议直接同名
- `reserved_standard_only`
  - 先保留标准名，当前不强制进入实际落盘
  - 常见于 `L2-conditional`
- `not_applicable_context_only`
  - 只作背景说明，不属于当前最小落盘字段

## 字段映射

| standard_field_name | actual_landing_name_v1 | mapping_status | type_id | layer | source_alias_or_legacy_name | note |
|---|---|---|---|---|---|---|
| `atr_value` | `atr_value` | planned_same_name | N01 | A | `ATR` | 建议未来直接同名落盘 |
| `atr_baseline_value` | `atr_baseline_value` | planned_same_name | N01 | A | `Baseline ATR` | 与原始说明保持可读映射 |
| `atr_ratio` | `atr_ratio` | planned_same_name | N01 | A | `ATR Ratio` | regime 主轴变量 |
| `atr_percentile` | `atr_percentile` | planned_same_name | N01 | A | `ATR Percentile` | 分位值 |
| `atr_percentile_regime` | `atr_percentile_regime` | planned_same_name | N01 | A | `Extreme/Elevated/Normal/Calm/Squeeze` | 分位分档 |
| `atr_regime_is_extreme` | `atr_regime_is_extreme` | planned_same_name | N01 | A | n/a | 布尔命名已定 |
| `atr_regime_is_squeeze` | `atr_regime_is_squeeze` | planned_same_name | N01 | A | n/a | 布尔命名已定 |
| `squeeze_is_on` | `squeeze_is_on` | planned_same_name | N01 | A | `squeeze on` | 不用 `is_squeeze` |
| `squeeze_tier` | `squeeze_tier` | planned_same_name | N01 | A | `Orange/Red/Black/Green dots` | 统一抽象为 tier |
| `squeeze_fired` | `squeeze_fired` | planned_same_name | N01 | A | `green dot = fired` | 不保留 UI 色彩名 |
| `squeeze_momentum_sign` | `squeeze_momentum_sign` | planned_same_name | N01 | A | histogram direction | 动量方向层 |
| `compression_quality_score` | `compression_quality_score` | planned_same_name | N01 | A | `normalized compression score` | 连续变量 |
| `atr_contraction_score` | `atr_contraction_score` | planned_same_name | N01 | A | `ATR contraction` | 子项评分 |
| `range_tightness_score` | `range_tightness_score` | planned_same_name | N01 | A | `Range tightness` | 子项评分 |
| `noise_cleanliness_score` | `noise_cleanliness_score` | planned_same_name | N01 | A | `Noise evaluation` | 子项评分 |
| `containment_score` | `containment_score` | planned_same_name | N01 | A | `Containment structure` | 子项评分 |
| `compression_state` | `compression_state` | reserved_standard_only | N01 | B | `Loose/Building/Tight/Mature` | 已有稳定枚举候选，但仍缺原始源码页复核 |
| `vol_regime_code` | `vol_regime_code` | reserved_standard_only | N01 | B | `compression/expansion/high_vol/exhaustion` | 仍缺源码级证据 |
| `vol_breakout_signal` | `vol_breakout_signal` | reserved_standard_only | N01 | B | `volatility breakout` | 阈值未稳 |
| `trend_confirmation_after_vol_breakout` | `trend_confirmation_after_vol_breakout` | reserved_standard_only | N01 | B | `two-stage confirmation` | 对象级逻辑未核 |
| `squeeze_momentum_accel` | `squeeze_momentum_accel` | reserved_standard_only | N01 | B | histogram acceleration | 各实现差异较大 |
| `atr_percentile_window` | `atr_percentile_window` | reserved_standard_only | N01 | B | percentile lookback | 默认值未统一 |
| `position_size_calculator` | `n/a` | not_applicable_context_only | N01 | C | source feature | 不进当前最小字段 |
| `dynamic_stop_loss` | `n/a` | not_applicable_context_only | N01 | C | source feature | 不进当前最小字段 |
| `take_profit_scaling` | `n/a` | not_applicable_context_only | N01 | C | source feature | 不进当前最小字段 |
| `integrated_risk_management` | `n/a` | not_applicable_context_only | N01 | C | source feature | 不进当前最小字段 |
| `session_id` | `session_id` | planned_same_name | N02 | A | session label | 伦敦/纽约/自定义 |
| `session_timezone` | `session_timezone` | planned_same_name | N02 | A | `Timezone` | 防 DST 漂移 |
| `opening_range_window_minutes` | `opening_range_window_minutes` | planned_same_name | N02 | A | `Opening Range Duration` | 用全称不保留 `orTF` |
| `opening_range_high` | `opening_range_high` | planned_same_name | N02 | A | `ORH` / `orh` | 标准名替代来源缩写 |
| `opening_range_low` | `opening_range_low` | planned_same_name | N02 | A | `ORL` / `orl` | 标准名替代来源缩写 |
| `opening_range_mid` | `opening_range_mid` | planned_same_name | N02 | A | `ORM` / `orm` | 中值字段 |
| `opening_range_width` | `opening_range_width` | planned_same_name | N02 | A | `OR width` / `orw` | 区间宽度 |
| `opening_range_width_pct_open` | `opening_range_width_pct_open` | planned_same_name | N02 | A | `or_range / open` | 比例字段 |
| `session_open_price` | `session_open_price` | planned_same_name | N02 | A | `session_open_price` | 已接近标准名 |
| `opening_range_defined` | `opening_range_defined` | planned_same_name | N02 | A | `or_token` semantic | 不保留实现变量名 |
| `or_break_high` | `or_break_high` | planned_same_name | N02 | A | `daily_broke_high` | 事件名向 OR 对齐 |
| `or_break_low` | `or_break_low` | planned_same_name | N02 | A | `daily_broke_low` | 事件名向 OR 对齐 |
| `first_break_direction` | `first_break_direction` | planned_same_name | N02 | A | `first_breakout_high/low` | 用单方向字段收口 |
| `target_trigger_source` | `target_trigger_source` | planned_same_name | N02 | A | `tSrc` | 触发源 |
| `width_error_day` | `width_error_day` | planned_same_name | N02 | A | `width error` / `W` | 结果标签 |
| `session_bias` | `session_bias` | reserved_standard_only | N02 | B | `day_dir` / bias | 定义未统一 |
| `ib_high` | `ib_high` | reserved_standard_only | N02 | B | `IB High` | 主要来自文章定义 |
| `ib_low` | `ib_low` | reserved_standard_only | N02 | B | `IB Low` | 主要来自文章定义 |
| `ib_range` | `ib_range` | reserved_standard_only | N02 | B | `IB Range` | 主要来自文章定义 |
| `ib_break_direction` | `ib_break_direction` | reserved_standard_only | N02 | B | `IB breakout direction` | 需与 OR 事件分离 |
| `ib_accept_2period` | `ib_accept_2period` | reserved_standard_only | N02 | B | `2+ periods outside IB` | 已有较强定义文章证据，仍缺源码级证据 |
| `ib_regime_narrow_or_wide` | `ib_regime_narrow_or_wide` | reserved_standard_only | N02 | B | `narrow/wide IB` | 语义已较清楚，仍缺统一阈值 |
| `ib_failed_breakout_event` | `ib_failed_breakout_event` | reserved_standard_only | N02 | B | `price returns into IB` | 已有定义文章支持，仍非源码实现 |
| `custom_session_used` | `custom_session_used` | reserved_standard_only | N02 | B | `crTog` semantic | 偏配置元数据 |
| `session_ma_bias` | `session_ma_bias` | reserved_standard_only | N02 | B | SMA/EMA/RMA/WMA/VWAP bias | 可视层偏多 |
| `profit_days` | `n/a` | not_applicable_context_only | N02 | C | stats table metric | 统计面板结果 |
| `loss_days` | `n/a` | not_applicable_context_only | N02 | C | stats table metric | 统计面板结果 |
| `error_days` | `n/a` | not_applicable_context_only | N02 | C | stats table metric | 统计面板结果 |
| `options_premium_decay_logic` | `n/a` | not_applicable_context_only | N02 | C | README strategy text | 不进当前最小字段 |
| `swing_mode` | `swing_mode` | planned_same_name | N03 | A | `mode` | `pivot/fractal/custom` |
| `swing_left_bars` | `swing_left_bars` | planned_same_name | N03 | A | `bars` left side | 标准化左右确认根数 |
| `swing_right_bars` | `swing_right_bars` | planned_same_name | N03 | A | `bars` right side | 标准化左右确认根数 |
| `swing_high_confirmed` | `swing_high_confirmed` | planned_same_name | N03 | A | `FRH/PPH confirmed` | 只认确认后摆点 |
| `swing_low_confirmed` | `swing_low_confirmed` | planned_same_name | N03 | A | `FRL/PPL confirmed` | 只认确认后摆点 |
| `break_confirmation_mode` | `break_confirmation_mode` | planned_same_name | N03 | A | `Close/Wick` | 统一 mode 后缀 |
| `break_level_price` | `break_level_price` | planned_same_name | N03 | A | tracked structure level | 价格对象 |
| `bos_event` | `bos_event` | planned_same_name | N03 | A | `BOS` | 事件命名统一 |
| `choch_event` | `choch_event` | planned_same_name | N03 | A | `CHOCH/ChoCh` | 事件命名统一 |
| `structure_direction` | `structure_direction` | planned_same_name | N03 | A | prevailing direction | 结构方向 |
| `structure_event_bar_close_confirmed` | `structure_event_bar_close_confirmed` | planned_same_name | N03 | A | `close beyond level` | 确认要求 |
| `pivot_confirm_delay_bars` | `pivot_confirm_delay_bars` | reserved_standard_only | N03 | B | pivot delay | 还需更细分表 |
| `confirmed_pivot_non_repaint` | `confirmed_pivot_non_repaint` | reserved_standard_only | N03 | B | `confirmed pivots do not repaint` | 缺源码级时序核验 |
| `structure_label_inherits_pivot_delay` | `structure_label_inherits_pivot_delay` | reserved_standard_only | N03 | B | pivot-based labels delay | 条件披露字段 |
| `current_bar_visuals_mutable` | `current_bar_visuals_mutable` | reserved_standard_only | N03 | B | `current bar elements change` | live bar 行为未核清 |
| `close_vs_wick_risk_note` | `close_vs_wick_risk_note` | reserved_standard_only | N03 | B | close vs wick note | 审计说明字段 |
| `future_leak_risk_flag` | `future_leak_risk_flag` | reserved_standard_only | N03 | B | zigzag/future leak risk | 风险标记 |
| `extra_confluence_used` | `extra_confluence_used` | reserved_standard_only | N03 | B | displacement/EMA/volume/HTF | algo_aakash 已补到 4 因子样本；不混入定义层 |
| `source_complexity_tier` | `source_complexity_tier` | reserved_standard_only | N03 | B | minimal/medium/complex | 来源复杂度 |
| `failed_breakout_event` | `failed_breakout_event` | reserved_standard_only | N03 | B | failed breakout | 对象级字段待补齐 |
| `FVG` | `n/a` | not_applicable_context_only | N03 | C | source feature | 本轮越界内容 |
| `order_block` | `n/a` | not_applicable_context_only | N03 | C | source feature | 本轮越界内容 |
| `premium_discount` | `n/a` | not_applicable_context_only | N03 | C | source feature | 本轮越界内容 |
| `Fib` | `n/a` | not_applicable_context_only | N03 | C | source feature | 本轮越界内容 |
| `regime_adaptation` | `n/a` | not_applicable_context_only | N03 | C | source feature | 本轮越界内容 |
| `HTF_overlay` | `n/a` | not_applicable_context_only | N03 | C | source feature | 本轮越界内容 |
| `volume_scoring` | `n/a` | not_applicable_context_only | N03 | C | source feature | 本轮越界内容 |
| `EMA_momentum_confirmation` | `n/a` | not_applicable_context_only | N03 | C | source feature | 本轮越界内容 |

## 当前裁决

- 若后续开始真正写 CSV / md 字段索引，优先让 `planned_same_name` 直接成为实际落盘名。
- `reserved_standard_only` 暂时只在标准层保留，不宣称已经进代码或结果文件。
- `not_applicable_context_only` 不做当前最小落盘字段。
- `compression_state`、`ib_failed_breakout_event` 这类字段虽然命名已稳定，但当前仍保留在标准层，不提前抬进 P0。

## 对应文件

- [Batch9_统一字段命名规范_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/Batch9_统一字段命名规范_v1.md#L1-L227)
- [Batch9_统一字段索引表_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/Batch9_统一字段索引表_v1.md#L1-L114)
- [Batch9_指标字段总表_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/Batch9_指标字段总表_v1.md#L1-L98)
