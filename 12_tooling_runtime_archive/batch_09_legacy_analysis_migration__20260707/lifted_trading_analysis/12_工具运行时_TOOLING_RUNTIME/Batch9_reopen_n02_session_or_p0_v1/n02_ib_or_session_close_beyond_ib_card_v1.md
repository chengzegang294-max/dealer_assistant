# N02 IB OR 收盘超出区间说明卡 v1

## 作用

- 把 `session_close_beyond_ib` 固定成独立说明卡。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-03 fresh-run

- 总行数：`9`
- 方向分布：`{"down": 4, "up": 5}`
- mode 分布：`{"close": 4, "wick": 5}`
- extension bucket 分布：`{"0.001_to_0.00299": 5, "ge_0.003": 3, "lt_0.001": 1}`

## Session 分布

- `new_york`: `{"rows": 9, "direction_down": 4, "mode_close": 4, "direction_up": 5, "mode_wick": 5}`

## 当前裁决

- `session_close_beyond_ib` 当前只说明：同日本地收盘仍位于 `IB` 边界外侧。
- 后续若继续推进，应从这些样本再拆 continuation/persistence 观察，而不是直接改名成 `failed breakout`。
