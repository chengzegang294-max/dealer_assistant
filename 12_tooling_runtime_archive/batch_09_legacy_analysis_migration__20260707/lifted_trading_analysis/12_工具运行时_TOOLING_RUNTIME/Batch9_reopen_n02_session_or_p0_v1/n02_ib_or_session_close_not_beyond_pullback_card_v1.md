# n02_ib_or_session_close_not_beyond_pullback_card v1

## 作用

- 把 `session_close_not_beyond_ib` 固定成回落分支说明卡。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-03 fresh-run

- 总行数：`6`
- 方向分布：`{"down": 2, "up": 4}`
- mode 分布：`{"close": 2, "wick": 4}`
- extension bucket 分布：`{"0.001_to_0.00299": 3, "ge_0.003": 1, "lt_0.001": 2}`

## Session 分布

- `london`: `{"rows": 2, "direction_up": 2, "mode_wick": 1, "mode_close": 1}`
- `new_york`: `{"rows": 4, "direction_up": 2, "mode_wick": 3, "direction_down": 2, "mode_close": 1}`

## 当前裁决

- `session_close_not_beyond_ib` 当前只说明：同日本地收盘已回到 `IB` 边界内侧或边界处。
- 后续若继续推进，应从这些样本再拆 pullback stability 观察，而不是直接改名成 `failed breakout`。
