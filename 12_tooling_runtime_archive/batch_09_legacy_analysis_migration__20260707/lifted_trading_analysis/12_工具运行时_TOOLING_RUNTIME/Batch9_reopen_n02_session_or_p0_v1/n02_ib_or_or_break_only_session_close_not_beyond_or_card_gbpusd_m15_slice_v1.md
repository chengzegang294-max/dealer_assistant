# n02_ib_or_or_break_only_session_close_not_beyond_or_card v1

## 作用

- 把 `OR break only + session_close_not_beyond_or` 固定成回落说明卡。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-06 fresh-run

- 总行数：`157`
- 方向分布：`{"down": 76, "up": 81}`
- mode 分布：`{"close": 88, "wick": 69}`
- extension bucket 分布：`{"0.00010_to_0.00049": 14, "ge_0.00050": 136, "lt_0.00010": 7}`

## Session 分布

- `london`: `{"rows": 79, "direction_up": 40, "mode_close": 48, "direction_down": 39, "mode_wick": 31}`
- `new_york`: `{"rows": 78, "direction_up": 41, "mode_wick": 38, "direction_down": 37, "mode_close": 40}`

## 当前裁决

- `session_close_not_beyond_or` 当前只说明：同日本地收盘已回到 `OR` 内侧或边界。
- 后续若继续推进，应从这些样本再拆 same-day pullback stability，而不是直接改名成 `failed breakout`。
