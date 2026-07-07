# kd_mtf_p0_contract_notes_v1

## 目的

- 这份说明配合：
  - `kd_mtf_p0_field_sample_v1.csv`
  - `kd_mtf_p0_field_header_v1.txt`
- 用来证明 `多周期KD P0` 已经进入“第一版输出证据”阶段。

## 当前口径

- 样本数据是演示用假数据，不是真实回测结果。
- 只用于说明：
  - 表头顺序
  - 空值写法
  - 默认值写法
  - 字符串枚举写法
- 当前严格只覆盖 `KD P0` 的 `6` 个字段。

## 表头规则

- 运行时主键列固定为：
  - `symbol`
  - `timeframe`
  - `bar_time`
- 后续字段顺序固定为：
  - `kd_week_bias`
  - `kd_day_signal`
  - `kd_4h_confirm`
  - `kd_alignment_tier`
  - `kd_direction_filter`
  - `kd_week_extreme_zone`

## 样本说明

### 第 1 行

- 作用：演示 `week/day/4h` 三层同向的高一致性状态
- 演示点：
  - `kd_alignment_tier = s`
  - `kd_direction_filter = long_preferred`
  - `kd_week_extreme_zone = normal`

### 第 2 行

- 作用：演示 `week` 与 `day` 冲突时的保守等待状态
- 演示点：
  - `kd_alignment_tier = conflict`
  - `kd_direction_filter = wait`
  - `kd_week_extreme_zone = overbought`

### 第 3 行

- 作用：演示 `day` 有主信号但 `4h` 尚未确认的中间状态
- 演示点：
  - `kd_alignment_tier = b`
  - `kd_direction_filter = wait`
  - `kd_4h_confirm = none`

## 默认值和空值

- 默认值示例：
  - `kd_day_signal = none`
  - `kd_4h_confirm = none`
  - `kd_alignment_tier = unknown`
  - `kd_direction_filter = unknown`
- 第一版原则上不鼓励空值。
- 若周期无法可靠重建，优先写：
  - `unknown`

## 当前明确不含

- `kd_month_bias`
- `kd_1h_entry_refine`
- `kd_cross_age_bars`
- `kd_divergence_flag`
- `kd_perfect_state_flag`
- `kd_dispersion_state`
- `kd_position_size_multiplier`

## 当前结论

- `多周期KD P0` 已从：
  - 对象定义入口
  - 进入
  - 第一版输出证据
- 下一步若继续推进，应优先落：
  - 运行时路径
  - 真实 header 冻结
  - proof-of-mapping
