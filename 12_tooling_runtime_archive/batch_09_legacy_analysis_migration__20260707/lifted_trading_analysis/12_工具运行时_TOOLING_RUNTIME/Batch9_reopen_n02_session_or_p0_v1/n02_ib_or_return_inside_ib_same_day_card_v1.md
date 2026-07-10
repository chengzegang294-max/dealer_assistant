# N02 IB OR 回到区间内当日说明卡 v1

## 作用

- 把 `return_inside_ib_observed_same_day` 固定为独立说明卡。
- 当前只表达：confirmed cross 之后，同日本地日内观察到价格回到 `IB` 边界内侧。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-03 fresh-run

- 总行数：`15`
- 方向分布：`{"down": 6, "up": 9}`
- mode 分布：`{"close": 6, "wick": 9}`
- `session_close_beyond_ib_rows`：`9`
- `session_close_not_beyond_ib_rows`：`6`

## Session 分布

- `london`: `{"rows": 2, "session_close_beyond_ib_rows": 0, "session_close_not_beyond_ib_rows": 2}`
- `new_york`: `{"rows": 13, "session_close_beyond_ib_rows": 9, "session_close_not_beyond_ib_rows": 4}`

## 当前裁决

- 这张卡只固定 `return_inside` 观测事实。
- 后续若继续推进，应从 `session_close_beyond_ib` 的二次分桶或更细的 return-inside 说明继续展开。
