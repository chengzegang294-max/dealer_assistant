# N02 IB OR 超出后多会话延续说明卡 GBPUSD M15 切片 v1

## 作用

- 把 `beyond multi-session persistence` 观察固定成独立说明卡。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-04 fresh-run

- 总行数：`13`
- status 分布：`{"missing_second_next_session_first_30m_data": 5, "second_next_session_first_30m_all_closes_beyond_prior_ib": 2, "second_next_session_first_30m_not_all_closes_beyond_prior_ib": 6}`
- direction 分布：`{"down": 6, "up": 7}`
- mode 分布：`{"close": 10, "wick": 3}`
- `second_next_session_first_30m_bar_count_30_rows`：`0`
- `second_next_session_first_bar_expected_side_rows`：`3`

## Session 分布

- `london`: `{"rows": 5, "status_missing_second_next_session_first_30m_data": 1, "status_second_next_session_first_30m_not_all_closes_beyond_prior_ib": 3, "status_second_next_session_first_30m_all_closes_beyond_prior_ib": 1}`
- `new_york`: `{"rows": 8, "status_second_next_session_first_30m_all_closes_beyond_prior_ib": 1, "status_second_next_session_first_30m_not_all_closes_beyond_prior_ib": 3, "status_missing_second_next_session_first_30m_data": 4}`

## 当前裁决

- `beyond multi-session persistence` 当前只说明：第二个同类 session 首 30 分钟是否整体仍在前一日 `IB` 外侧。
- 当前 `2/13` 行满足持续外侧，`6/13` 行不满足，`5/13` 行缺第二个同类 session 数据。
- 后续若继续推进，应从满足持续外侧的样本再拆第三个同类 session persistence，不直接改名成 `failed breakout`。
