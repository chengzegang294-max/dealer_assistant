# n02_ib_or_session_close_not_beyond_pullback_card v1

## 作用

- 把 `session_close_not_beyond_ib` 固定成回落分支说明卡。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-03 fresh-run

- 总行数：`21`
- 方向分布：`{"down": 10, "up": 11}`
- mode 分布：`{"close": 9, "wick": 12}`
- extension bucket 分布：`{"0.001_to_0.00299": 9, "ge_0.003": 3, "lt_0.001": 9}`

## Session 分布

- `london`: `{"rows": 7, "direction_down": 3, "mode_close": 4, "direction_up": 4, "mode_wick": 3}`
- `new_york`: `{"rows": 14, "direction_down": 7, "mode_wick": 9, "direction_up": 7, "mode_close": 5}`

## 当前裁决

- `session_close_not_beyond_ib` 当前只说明：同日本地收盘已回到 `IB` 边界内侧或边界处。
- 后续若继续推进，应从这些样本再拆 pullback stability 观察，而不是直接改名成 `failed breakout`。
