# n01_p0_runtime_atr_calculation_checklist v1

## 目的

- 给 `REOPEN_B9_N01_VOL_STATE_P0` 第一份真实 runtime 数据接入前提供固定 ATR 计算口径清单。
- 防止把 ATR 输入长度、baseline、percentile window 和 squeeze 口径混写。

## 当前冻结参数骨架

- `atr_length = 14`
- `atr_baseline_length = 50`
- `atr_percentile_window = 252`
- `squeeze_mode = ttm_pro_like`

## 接入前必须逐项确认

### 1. ATR 核心定义检查

- 当前 `atr_length` 固定为 `14`。
- 计算口径应与当前来源说明保持一致：
  - `ATR = SMA(True Range, default 14)`
- 若实际实现不是这一定义：
  - 不直接沿用 `v1`
  - 先补来源说明或新开版本

### 2. baseline 定义检查

- 当前 `atr_baseline_length` 固定为 `50`。
- baseline 必须明确写清是：
  - `SMA of ATR`
  - 或 `EMA of ATR`
- 若真实实现尚不能确认 `SMA/EMA`：
  - 允许继续停留在示例行层
  - 不宣称已完成真实接入

### 3. ATR ratio 检查

- `atr_ratio = atr_value / baseline_atr`
- 必须确认：
  - 分子和分母使用同一 ATR 基础定义
  - baseline 不为 `0`
- 若 baseline 缺失或历史不足：
  - `atr_ratio = na`

### 4. percentile window 检查

- 当前 `atr_percentile_window` 固定为 `252`
- percentile 结果必须保持 `0-100`
- 不允许在 `v1` 中悄悄改成：
  - `0-1`
  - 其他 lookback 长度

### 5. regime 分箱检查

- `atr_percentile_regime` 当前只允许：
  - `extreme`
  - `elevated`
  - `normal`
  - `calm`
  - `squeeze`
  - `unknown`
- 若 percentile 历史不足：
  - `atr_percentile = na`
  - `atr_percentile_regime = unknown`

### 6. squeeze 检查

- `squeeze_mode = ttm_pro_like`
- 当前只允许输出：
  - `squeeze_is_on`
  - `squeeze_tier`
  - `squeeze_fired`
- 不允许在未升级版本时额外写入：
  - `compression_state`
  - `vol_regime_code`

### 7. 最小抽查样本

- 至少抽查：
  - 1 条 ATR / baseline 都可算的样本
  - 1 条 percentile 历史不足样本
  - 1 条 squeeze 为 `off` 或 `medium/high/low` 的样本
- 每条抽查至少记录：
  - `bar_time`
  - `atr_value`
  - `atr_ratio`
  - `atr_percentile`
  - `atr_percentile_regime`
  - `squeeze_tier`

## 不通过时怎么处理

- 若 ATR 核心定义不清：
  - 不写入真实数据
- 若 baseline 口径不清：
  - 不宣称 `atr_ratio` 已完成
- 若 percentile window 被改动：
  - 不覆盖 `v1`
  - 改走新版本
