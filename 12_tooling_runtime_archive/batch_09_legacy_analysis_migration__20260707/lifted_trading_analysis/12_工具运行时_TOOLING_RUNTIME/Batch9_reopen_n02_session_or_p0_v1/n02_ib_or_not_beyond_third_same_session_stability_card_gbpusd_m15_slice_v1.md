# N02 IB OR 未超出第三同会话稳定性说明卡 GBPUSD M15 切片 v1

## 作用

- 把 `not_beyond third same-session stability` 观察固定成独立说明卡。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-04 fresh-run

- 总行数：`9`
- status 分布：`{"missing_third_next_session_first_30m_data": 2, "third_next_session_first_30m_all_closes_inside_prior_ib": 6, "third_next_session_first_30m_not_all_closes_inside_prior_ib": 1}`
- direction 分布：`{"down": 4, "up": 5}`
- mode 分布：`{"close": 4, "wick": 5}`
- `third_next_session_first_30m_bar_count_30_rows`：`0`
- `third_next_session_first_bar_expected_side_rows`：`6`

## Session 分布

- `london`: `{"rows": 4, "status_missing_third_next_session_first_30m_data": 1, "status_third_next_session_first_30m_not_all_closes_inside_prior_ib": 1, "status_third_next_session_first_30m_all_closes_inside_prior_ib": 2}`
- `new_york`: `{"rows": 5, "status_third_next_session_first_30m_all_closes_inside_prior_ib": 4, "status_missing_third_next_session_first_30m_data": 1}`

## 当前裁决

- `not_beyond third same-session stability` 当前只说明：第三个同类 session 首 30 分钟是否整体仍在前一日 `IB` 内侧或边界。
- 当前 `6/9` 行满足稳定内侧，`1/9` 行失稳，`2/9` 行缺第三个同类 session 数据。
- 当前已经到达 branch card 层，仍不直接改名成 `failed breakout`。
