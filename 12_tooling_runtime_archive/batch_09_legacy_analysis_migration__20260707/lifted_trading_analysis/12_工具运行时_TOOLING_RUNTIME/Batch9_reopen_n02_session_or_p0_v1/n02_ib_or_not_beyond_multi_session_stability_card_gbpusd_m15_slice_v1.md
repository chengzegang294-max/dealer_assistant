# N02 IB OR 未超出多会话稳定性说明卡 GBPUSD M15 切片 v1

## 作用

- 把 `not_beyond multi-session stability` 观察固定成独立说明卡。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-04 fresh-run

- 总行数：`14`
- status 分布：`{"missing_second_next_session_first_30m_data": 1, "second_next_session_first_30m_all_closes_inside_prior_ib": 9, "second_next_session_first_30m_not_all_closes_inside_prior_ib": 4}`
- direction 分布：`{"down": 8, "up": 6}`
- mode 分布：`{"close": 5, "wick": 9}`
- `second_next_session_first_30m_bar_count_30_rows`：`0`
- `second_next_session_first_bar_expected_side_rows`：`9`

## Session 分布

- `london`: `{"rows": 5, "status_second_next_session_first_30m_all_closes_inside_prior_ib": 4, "status_second_next_session_first_30m_not_all_closes_inside_prior_ib": 1}`
- `new_york`: `{"rows": 9, "status_second_next_session_first_30m_not_all_closes_inside_prior_ib": 3, "status_second_next_session_first_30m_all_closes_inside_prior_ib": 5, "status_missing_second_next_session_first_30m_data": 1}`

## 当前裁决

- `not_beyond multi-session stability` 当前只说明：第二个同类 session 首 30 分钟是否整体仍在前一日 `IB` 内侧或边界。
- 当前 `9/14` 行满足稳定内侧，`4/14` 行不满足，`1/14` 行缺第二个同类 session 数据。
- 后续若继续推进，应从满足稳定内侧的样本再拆第三个同类 session stability，不直接改名成 `failed breakout`。
