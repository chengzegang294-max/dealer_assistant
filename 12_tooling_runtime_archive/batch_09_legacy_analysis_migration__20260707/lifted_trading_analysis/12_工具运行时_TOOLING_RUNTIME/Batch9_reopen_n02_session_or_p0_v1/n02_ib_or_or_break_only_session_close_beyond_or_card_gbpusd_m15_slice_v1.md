# N02 IB OR 仅 OR 突破且收盘超出 OR 说明卡 GBPUSD M15 切片 v1

## 作用

- 把 `OR break only + session_close_beyond_or` 固定成独立说明卡。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-06 fresh-run

- 总行数：`168`
- 方向分布：`{"down": 96, "up": 72}`
- mode 分布：`{"close": 88, "wick": 80}`
- extension bucket 分布：`{"0.00010_to_0.00049": 1, "ge_0.00050": 167}`

## Session 分布

- `london`: `{"rows": 88, "direction_down": 49, "mode_close": 46, "direction_up": 39, "mode_wick": 42}`
- `new_york`: `{"rows": 80, "direction_down": 47, "mode_wick": 38, "direction_up": 33, "mode_close": 42}`

## 当前裁决

- `session_close_beyond_or` 当前只说明：同日本地收盘仍位于 `OR` 首破同侧外侧。
- 后续若继续推进，应从这些样本再拆 same-side continuation / persistence，而不是直接改名成 `failed breakout`。
