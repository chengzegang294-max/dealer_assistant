# N02 IB OR 未超出第三同会话稳定性说明卡 v1

## 作用

- 把 `not_beyond third same-session stability` 观察固定成独立说明卡。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-04 fresh-run

- 总行数：`1`
- status 分布：`{"missing_third_next_session_first_30m_data": 1}`
- direction 分布：`{"up": 1}`
- mode 分布：`{"wick": 1}`
- `third_next_session_first_30m_bar_count_30_rows`：`0`
- `third_next_session_first_bar_expected_side_rows`：`0`

## Session 分布

- `london`: `{"rows": 1, "status_missing_third_next_session_first_30m_data": 1}`

## 当前裁决

- `not_beyond third same-session stability` 当前只说明：第三个同类 session 首 30 分钟是否整体仍在前一日 `IB` 内侧或边界。
- 当前 `0/1` 行满足稳定内侧，`0/1` 行失稳，`1/1` 行缺第三个同类 session 数据。
- 当前已经到达 branch card 层，仍不直接改名成 `failed breakout`。
