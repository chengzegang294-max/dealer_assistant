# N02 IB OR 收盘超出区间说明卡 GBPUSD M15 切片 v1

## 作用

- 把 `session_close_beyond_ib` 固定成独立说明卡。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-03 fresh-run

- 总行数：`27`
- 方向分布：`{"down": 17, "up": 10}`
- mode 分布：`{"close": 18, "wick": 9}`
- extension bucket 分布：`{"0.001_to_0.00299": 7, "ge_0.003": 20}`

## Session 分布

- `london`: `{"rows": 13, "direction_up": 6, "mode_wick": 3, "mode_close": 10, "direction_down": 7}`
- `new_york`: `{"rows": 14, "direction_up": 4, "mode_close": 8, "direction_down": 10, "mode_wick": 6}`

## 当前裁决

- `session_close_beyond_ib` 当前只说明：同日本地收盘仍位于 `IB` 边界外侧。
- 后续若继续推进，应从这些样本再拆 continuation/persistence 观察，而不是直接改名成 `failed breakout`。
