# n01_p0_contract_notes v1

## 角色

- 这份文件属于 `Batch9 / REOPEN_B9_N01_VOL_STATE_P0` 的第一版字段样本证据。
- 作用是冻结 `N01 P0` 当前最小字段合同，不代表真实运行时已接入。

## 当前固定范围

- 当前只覆盖 `8` 个 `N01 P0` 字段：
  - `atr_value`
  - `atr_ratio`
  - `atr_percentile`
  - `atr_percentile_regime`
  - `squeeze_is_on`
  - `squeeze_tier`
  - `squeeze_fired`
  - `compression_quality_score`
- 主键列保持：
  - `symbol`
  - `timeframe`
  - `bar_time`

## 样本说明

- `n01_p0_field_sample_v1.csv` 中的两行都属于演示样本，不是真实回测或实盘输出。
- 第一行只演示：
  - 浮点值写法
  - `atr_percentile_regime` 的字符串枚举
  - `squeeze_tier` 的字符串枚举
- 第二行只演示：
  - `na` 空值写法
  - `unknown / off / 0` 这类默认值写法

## 当前固定口径

- `atr_percentile` 保持 `0-100`。
- `atr_percentile_regime` 当前只允许：
  - `extreme`
  - `elevated`
  - `normal`
  - `calm`
  - `squeeze`
  - `unknown`
- `squeeze_tier` 当前只允许：
  - `high`
  - `medium`
  - `low`
  - `off`
- `squeeze_fired` 当前只保留事件位 `0/1`，不记录方向。
- `compression_quality_score` 当前允许 `na`。

## 当前不包含

- `atr_baseline_value`
- `atr_regime_is_extreme`
- `atr_regime_is_squeeze`
- `squeeze_momentum_sign`
- 四项 compression 子评分
- `compression_state`
- `vol_regime_code`
- `vol_breakout_signal`
- `trend_confirmation_after_vol_breakout`

## 使用边界

- 当前可以宣称：
  - `N01 P0 sample evidence landed`
- 当前不能宣称：
  - `N01 runtime implemented`
  - `full volatility regime engine implemented`
  - `compression_state implemented`

## 回滚方式

- 若 `squeeze_tier` 或 `compression_quality_score` 口径后续漂移，冻结 `v1`，另起 `v2`。
- 不覆盖当前 `v1` 样本证据文件。
