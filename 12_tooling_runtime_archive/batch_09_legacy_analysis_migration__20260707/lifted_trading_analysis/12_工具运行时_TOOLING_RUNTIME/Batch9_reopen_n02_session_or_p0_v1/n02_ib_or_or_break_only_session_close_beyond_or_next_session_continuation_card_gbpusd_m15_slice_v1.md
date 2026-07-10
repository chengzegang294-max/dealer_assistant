# N02 IB OR 仅 OR 突破收盘超出 OR 下一会话延续说明卡 GBPUSD M15 切片 v1

## 作用

- 把 `or_break_only + session_close_beyond_or + next same-session first 30m continuation` 固定成独立说明卡。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-06 fresh-run

- 总行数：`168`
- status 分布：`{"missing_next_session_first_30m_data": 40, "next_session_first_30m_all_closes_beyond_prior_or": 105, "next_session_first_30m_not_all_closes_beyond_prior_or": 23}`
- direction 分布：`{"down": 96, "up": 72}`
- mode 分布：`{"close": 88, "wick": 80}`
- `next_session_first_30m_full_window_rows`：`128`
- `next_session_first_bar_expected_side_rows`：`106`

## Session 分布

- `london`: `{"rows": 88, "status_missing_next_session_first_30m_data": 19, "status_next_session_first_30m_all_closes_beyond_prior_or": 61, "status_next_session_first_30m_not_all_closes_beyond_prior_or": 8}`
- `new_york`: `{"rows": 80, "status_next_session_first_30m_all_closes_beyond_prior_or": 44, "status_missing_next_session_first_30m_data": 21, "status_next_session_first_30m_not_all_closes_beyond_prior_or": 15}`

## 当前裁决

- `session_close_beyond_or` 当前只说明：下一同类 session 首 30 分钟是否整体仍在前一日 `OR` 外侧同方向。
- 当前 `105/168` 行满足持续外侧，`23/168` 行不满足，`40/168` 行缺下一同类 session 数据。
- 后续若继续推进，应只从满足持续外侧的样本再拆 continuation persistence，不直接改名成 `failed breakout`。
