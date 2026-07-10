# N02 IB OR 回到区间内当日说明卡 GBPUSD M15 切片 v1

## 作用

- 把 `return_inside_ib_observed_same_day` 固定为独立说明卡。
- 当前只表达：confirmed cross 之后，同日本地日内观察到价格回到 `IB` 边界内侧。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-03 fresh-run

- 总行数：`45`
- 方向分布：`{"down": 26, "up": 19}`
- mode 分布：`{"close": 24, "wick": 21}`
- `session_close_beyond_ib_rows`：`24`
- `session_close_not_beyond_ib_rows`：`21`

## Session 分布

- `london`: `{"rows": 19, "session_close_beyond_ib_rows": 12, "session_close_not_beyond_ib_rows": 7}`
- `new_york`: `{"rows": 26, "session_close_beyond_ib_rows": 12, "session_close_not_beyond_ib_rows": 14}`

## 当前裁决

- 这张卡只固定 `return_inside` 观测事实。
- 后续若继续推进，应从 `session_close_beyond_ib` 的二次分桶或更细的 return-inside 说明继续展开。
