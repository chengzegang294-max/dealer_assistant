# n01_p0_real_input_mapping_draft v1

## 目的

- 给 `REOPEN_B9_N01_VOL_STATE_P0` 第一份真实 runtime 数据接入前提供最小输入映射草案。
- 只解决 ATR / percentile / squeeze / compression_quality_score 的真实输入映射，不扩到 `compression_state / vol_regime_code / breakout`。

## 当前目标输出

- `atr_value`
- `atr_ratio`
- `atr_percentile`
- `atr_percentile_regime`
- `squeeze_is_on`
- `squeeze_tier`
- `squeeze_fired`
- `compression_quality_score`

## 最小真实输入

### 行情主输入

- `symbol`
- `timeframe`
- `bar_time`
- `open`
- `high`
- `low`
- `close`

### 配置主输入

- `atr_length = 14`
- `atr_baseline_length = 50`
- `atr_percentile_window = 252`
- `squeeze_mode = ttm_pro_like`

## 输入到输出映射

### 1. 直接透传

- `symbol <- symbol`
- `timeframe <- timeframe`
- `bar_time <- bar_time`

### 2. ATR 主值

- `atr_value`
  - 来源：
    - `high / low / close`
  - 当前 v1 口径：
    - `ATR = SMA(True Range, 14)`

### 3. baseline 与 ratio

- `baseline_atr`
  - 不直接落盘到 v1
  - 但计算 `atr_ratio` 时必须存在
  - 当前 v1 口径必须明确到 checklist 所要求的一种：
    - `baseline_atr = SMA(atr_value, 50)`
- `atr_ratio`
  - `atr_value / baseline_atr`
  - 当前 baseline lookback = `50`
- 若 baseline 历史不足：
  - `atr_ratio = na`

### 4. percentile 与 regime

- `atr_percentile`
  - 基于 `atr_value` 在 rolling window 中的分位
  - 当前 window = `252`
  - 结果保持 `0-100`
- `atr_percentile_regime`
  - 当前只允许：
    - `extreme`
    - `elevated`
    - `normal`
    - `calm`
    - `squeeze`
    - `unknown`
- 若 percentile 历史不足：
  - `atr_percentile = na`
  - `atr_percentile_regime = unknown`

### 5. squeeze 组

- `squeeze_is_on`
  - 基于当前 `squeeze_mode = ttm_pro_like`
- `squeeze_tier`
  - 当前只允许：
    - `high`
    - `medium`
    - `low`
    - `off`
- `squeeze_fired`
  - 当前只保留 `0/1`
  - 不记录方向

### 6. compression_quality_score

- 当前允许：
  - 直接计算后落数值
  - 或在真实实现未齐时先落 `na`
- 但不允许直接扩成：
  - `compression_state`
  - 子评分列

## 第一份真实数据的最小来源候选

- 候选 A：
  - MT5 / broker bar export
  - 优点：最接近未来真实链路
  - 风险：需要足够回看长度才能算 `50 / 252`
- 候选 B：
  - 手工整理的 bar-level CSV
  - 优点：适合先做 proof-of-mapping
  - 风险：可能只够短窗，不够 percentile 历史

## 第一份真实数据建议最小样本

- 至少准备三类 bar：
  - `atr_value / atr_ratio` 都可算的样本
  - `atr_percentile` 历史不足样本
  - `squeeze_tier` 非 `off` 的样本

## 历史长度最低要求

- 若只想先验证 `atr_value`：
  - 至少 `14` 根 bar
- 若想验证 `atr_ratio`：
  - 必须能同时算出 `atr_value` 与 `baseline_atr`
  - 若 baseline 定义为 `SMA(atr_value, 50)` 且 `atr_value = SMA(TR, 14)`：
    - 至少 `14 + 50 - 1 = 63` 根 bar
- 若想验证 `atr_percentile`：
  - 至少 `252` 根 bar
- 若历史长度不够：
  - 不宣称对应字段已真实接入完成

## 当前不做

- 不做 `compression_state`
- 不做 `vol_regime_code`
- 不做 `vol_breakout_signal`
- 不把订单管理逻辑直接塞进当前字段层

## 接入前必须联动

- `n01_p0_runtime_atr_calculation_checklist_v1.md`
- `n01_p0_runtime_append_protocol_v1.md`
