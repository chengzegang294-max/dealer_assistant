# n02_ib_or_not_beyond_multi_session_stability_card v1

## 作用

- 把 `not_beyond multi-session stability` 观察固定成独立说明卡。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-04 fresh-run

- 总行数：`2`
- status 分布：`{"second_next_session_first_30m_all_closes_inside_prior_ib": 1, "second_next_session_first_30m_not_all_closes_inside_prior_ib": 1}`
- direction 分布：`{"up": 2}`
- mode 分布：`{"close": 1, "wick": 1}`
- `second_next_session_first_30m_bar_count_30_rows`：`2`
- `second_next_session_first_bar_expected_side_rows`：`1`

## Session 分布

- `london`: `{"rows": 2, "status_second_next_session_first_30m_all_closes_inside_prior_ib": 1, "status_second_next_session_first_30m_not_all_closes_inside_prior_ib": 1}`

## 当前裁决

- `not_beyond multi-session stability` 当前只说明：第二个同类 session 首 30 分钟是否整体仍在前一日 `IB` 内侧或边界。
- 当前 `1/2` 行满足稳定内侧，`1/2` 行不满足，`0/2` 行缺第二个同类 session 数据。
- 后续若继续推进，应从满足稳定内侧的样本再拆第三个同类 session stability，不直接改名成 `failed breakout`。
