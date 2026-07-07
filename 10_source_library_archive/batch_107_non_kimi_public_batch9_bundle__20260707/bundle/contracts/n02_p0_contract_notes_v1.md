# n02_p0_contract_notes v1

## 目的

- 这份说明配合：
  - `n02_p0_field_sample_v1.csv`
  - `n02_p0_field_header_v1.txt`
- 用来证明 `REOPEN_B9_N02_SESSION_OR_P0` 已经进入“第一版输出证据”阶段。

## 当前口径

- 样本数据是演示用假数据，不是真实回测结果。
- 只用于说明：
  - 表头顺序
  - 空值写法
  - 默认值写法
  - 字符串枚举写法
- 当前严格只覆盖 `N02 P0` 的 `12` 个字段。

## 表头规则

- 运行时主键列固定为：
  - `symbol`
  - `timeframe`
  - `bar_time`
- 后续字段顺序固定为：
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

## 样本说明

### 第 1 行

- 作用：演示 `opening_range_defined = 1` 之后的完整 OR 字段状态
- 演示点：
  - `first_break_direction = up`
  - `width_error_day = 0`
  - 所有 OR 价格字段均可用

### 第 2 行

- 作用：演示 `opening_range_defined = 0` 时的空值状态
- 演示点：
  - `opening_range_high / low / mid / width / width_pct_open = na`
  - `first_break_direction = none`
  - `width_error_day = 0`
  - `session_open_price` 已有值，但 OR 尚未完成

## 默认值和空值

- 默认值示例：
  - `opening_range_defined = 0`
  - `first_break_direction = none`
  - `width_error_day = 0`
- 空值示例：
  - `opening_range_high = na`
  - `opening_range_low = na`
  - `opening_range_mid = na`
  - `opening_range_width = na`
  - `opening_range_width_pct_open = na`

## 当前明确不含

- `or_break_high`
- `or_break_low`
- `target_trigger_source`
- `ib_high`
- `ib_low`
- `ib_range`
- `ib_break_direction`
- `ib_accept_2period`
- `ib_regime_narrow_or_wide`
- `ib_failed_breakout_event`
- `session_bias`

## 当前结论

- `REOPEN_B9_N02_SESSION_OR_P0` 已从：
  - 最小实施草案
  - 进入
  - 第一版输出证据
- 下一步若继续推进，应优先落真实字段输出路径，而不是再新增概念文档。
