# N02 IB OR 超出后第三同会话延续说明卡 GBPUSD M15 切片 v1

## 作用

- 把 `beyond third same-session persistence` 观察固定成独立说明卡。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-04 fresh-run

- 总行数：`2`
- status 分布：`{"missing_third_next_session_first_30m_data": 1, "third_next_session_first_30m_all_closes_beyond_prior_ib": 1}`
- direction 分布：`{"down": 1, "up": 1}`
- mode 分布：`{"close": 2}`
- `third_next_session_first_30m_bar_count_30_rows`：`0`
- `third_next_session_first_bar_expected_side_rows`：`1`

## Session 分布

- `london`: `{"rows": 1, "status_third_next_session_first_30m_all_closes_beyond_prior_ib": 1}`
- `new_york`: `{"rows": 1, "status_missing_third_next_session_first_30m_data": 1}`

## 当前裁决

- `beyond third same-session persistence` 当前只说明：第三个同类 session 首 30 分钟是否整体仍在前一日 `IB` 外侧。
- 当前 `1/2` 行满足持续外侧，`0/2` 行不满足，`1/2` 行缺第三个同类 session 数据。
- 当前已经到达 branch card 层，仍不直接改名成 `failed breakout`。
