# Batch9 统一字段命名规范 v1

## 目标

- 给 `N01 / N02 / N03` 的字段起统一名字，避免同一含义出现多套写法。
- 这份规范优先约束研究侧/诊断侧字段，不直接决定策略 gate。
- 当前结论：命名规范可先按 v1 执行，但字段本体仍有“未收集完全”的部分，命名先统一，证据继续补。

## 总原则

- 全部使用 `snake_case`
- 默认使用英文小写 ASCII
- 字段名先表达“对象”，再表达“属性/状态/动作”
- 同类含义尽量复用同一后缀，不重复发明词
- 没有明确对象时，不得只写模糊名词

## 命名顺序

- 推荐顺序：
  - `object + attribute`
  - `object + state`
  - `object + event`
  - `object + risk_note`
- 例子：
  - `opening_range_high`
  - `atr_percentile_regime`
  - `bos_event`
  - `close_vs_wick_risk_note`

## 类型约束

- `float`
  - 用于价格、比例、分值、宽度、窗口比率
  - 例子：`atr_ratio`、`opening_range_width`
- `int`
  - 用于 0/1 标志、计数、bar 数
  - 例子：`squeeze_is_on`、`pivot_confirm_delay_bars`
- `string`
  - 用于枚举、方向、模式、来源复杂度
  - 例子：`swing_mode`、`first_break_direction`
- `context`
  - 只作背景说明，不进当前最小字段层

## 布尔/标志字段规则

- 布尔优先使用这些后缀：
  - `_is_`
  - `_has_`
  - `_defined`
  - `_used`
- 推荐：
  - `squeeze_is_on`
  - `atr_regime_is_extreme`
  - `opening_range_defined`
  - `custom_session_used`
- 不推荐：
  - `is_squeeze`
  - `extreme_flag`
  - `or_done`
  - `use_custom_session_flag`

## 事件字段规则

- 事件统一优先使用 `_event`
- 突破/切换类事件，优先把对象放前面
- 推荐：
  - `bos_event`
  - `choch_event`
  - `ib_failed_breakout_event`
  - `failed_breakout_event`
- 事件若分方向，可单独配方向字段，不要把多个信息塞一个名字
- 不推荐：
  - `bos_signal_event_flag`
  - `did_choch_happen`
  - `breakout_up_or_down_signal`

## 方向/模式/等级字段规则

- 方向优先用：
  - `_direction`
  - `_bias`
- 模式优先用：
  - `_mode`
  - `_source`
- 等级/分档优先用：
  - `_tier`
  - `_regime`
  - `_state`
- 推荐：
  - `first_break_direction`
  - `session_bias`
  - `break_confirmation_mode`
  - `target_trigger_source`
  - `squeeze_tier`
  - `atr_percentile_regime`
  - `compression_state`

## 价格/区间/窗口字段规则

- 价格级字段：
  - `_high`
  - `_low`
  - `_mid`
  - `_price`
- 区间级字段：
  - `_range`
  - `_width`
- 窗口级字段：
  - `_window`
  - `_window_minutes`
  - `_bars`
- 推荐：
  - `ib_high`
  - `ib_low`
  - `break_level_price`
  - `opening_range_width`
  - `opening_range_window_minutes`
  - `swing_left_bars`
  - `swing_right_bars`

## 分值/比例/分位字段规则

- 分值统一优先：
  - `_score`
- 比率统一优先：
  - `_ratio`
  - `_pct_`
- 分位统一优先：
  - `_percentile`
- 推荐：
  - `compression_quality_score`
  - `atr_contraction_score`
  - `atr_ratio`
  - `opening_range_width_pct_open`
  - `atr_percentile`

## 审计/风险披露字段规则

- 审计说明统一优先：
  - `_risk_note`
  - `_non_repaint`
  - `_delay_bars`
  - `_mutable`
  - `_risk_flag`
- 推荐：
  - `close_vs_wick_risk_note`
  - `confirmed_pivot_non_repaint`
  - `pivot_confirm_delay_bars`
  - `current_bar_visuals_mutable`
  - `future_leak_risk_flag`

## 禁止事项

- 不要把多个维度塞进一个字段名
  - 错：`bullish_breakout_close_confirmed_signal`
- 不要把 UI 概念混成基础字段
  - 错：`green_dot_status`
  - 对：`squeeze_fired`
- 不要把来源作者习惯直接照抄进仓库标准字段
  - 错：`orh`
  - 对：`opening_range_high`
- 不要混用缩写和全称造成双轨
  - 错：同一层同时存在 `or_high` 和 `opening_range_high`
- 不要用含义不明的通用词
  - 错：`status`
  - 错：`signal`
  - 错：`value`

## 缩写规则

- 允许保留且已稳定的缩写：
  - `atr`
  - `ib`
  - `bos`
  - `choch`
- 不再新引入低可读性缩写，除非行业里极稳定
- 对外解释文档里，第一次出现缩写应配全称

## 标准命名模板

- 状态类：
  - `<object>_state`
  - `<object>_regime`
  - `<object>_tier`
- 事件类：
  - `<object>_event`
  - `<object>_break_<direction>` 仅在方向确定且不会再拆字段时使用
- 标志类：
  - `<object>_is_<adj>`
  - `<object>_has_<noun>`
- 风险类：
  - `<object>_risk_flag`
  - `<object>_risk_note`
- 时间/确认类：
  - `<object>_delay_bars`
  - `<object>_window_minutes`
  - `<object>_bar_close_confirmed`

## 当前字段映射示例

- N01
  - `atr_percentile_regime`
  - `squeeze_tier`
  - `compression_quality_score`
- N02
  - `opening_range_high`
  - `opening_range_width_pct_open`
  - `ib_accept_2period`
  - `ib_failed_breakout_event`
- N03
  - `break_confirmation_mode`
  - `bos_event`
  - `confirmed_pivot_non_repaint`

## 当前未完全定死的部分

- 只是命名定了，不代表对应字段证据已全部收齐。
- 尤其这些字段目前仍应保持条件态：
  - `compression_state`
  - `vol_regime_code`
  - `ib_accept_2period`
  - `ib_failed_breakout_event`
  - `confirmed_pivot_non_repaint`
  - `failed_breakout_event`
- 后续若字段定义变化，优先改字段说明，不轻易改字段名。

## 当前裁决

- 从现在开始，新增字段优先遵守这份 v1 命名规范。
- 若旧字段与规范冲突，先在索引表里记“推荐标准名”，不要立即批量重命名代码。
- 真正进入代码或 CSV 合约前，再做一次“标准名 -> 实际落盘名”的收口。
