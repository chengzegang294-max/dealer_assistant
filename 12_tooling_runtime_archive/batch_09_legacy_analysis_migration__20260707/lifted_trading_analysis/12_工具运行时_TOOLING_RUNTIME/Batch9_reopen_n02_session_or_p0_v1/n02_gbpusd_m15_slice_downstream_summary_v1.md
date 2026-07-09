# N02 GBPUSD M15 切片下游总览 v1

## 作用

- 把 `GBPUSD/M15 historical recovered -> slice runtime -> downstream terminal summary` 收口成一份总览。
- 当前只覆盖 `without_failed_breakout` 范围，不把任何分支升级成 `failed breakout / retest / reject / day type`。

## 2026-07-06 fresh-run

- `slice_or_rows`：`457`
- `slice_or_defined_rows`：`396`
- `slice_ib_rows`：`457`
- `slice_ib_defined_rows`：`396`
- `relation_rows`：`396`
- `first_break_relative_case_counts`：`{"no_break": 23, "or_break_with_ib_same_side_gap_remaining": 325, "shared_edge_break": 48}`
- `break_bar_evidence_status_counts`：`{"ib_same_side_cross_confirmed": 48, "no_break_in_upstream_relation": 23, "or_break_bar_found_but_ib_same_side_not_crossed": 325}`
- `cross_outcome_split`：`{"confirmed_cross_rows": 48, "or_break_only_rows": 325, "no_break_rows": 23}`
- `post_cross`：`{"rows": 48, "return_inside_rows": 45, "session_close_beyond_ib_rows": 27}`
- `next_session`：`{"beyond_rows": 27, "beyond_status_counts": {"missing_next_session_first_30m_data": 6, "next_session_first_30m_all_closes_beyond_prior_ib": 13, "next_session_first_30m_not_all_closes_beyond_prior_ib": 8}, "not_beyond_rows": 21, "not_beyond_status_counts": {"missing_next_session_first_30m_data": 5, "next_session_first_30m_all_closes_inside_prior_ib": 14, "next_session_first_30m_not_all_closes_inside_prior_ib": 2}}`
- `multi_session`：`{"beyond_rows": 13, "beyond_status_counts": {"missing_second_next_session_first_30m_data": 5, "second_next_session_first_30m_all_closes_beyond_prior_ib": 2, "second_next_session_first_30m_not_all_closes_beyond_prior_ib": 6}, "not_beyond_rows": 14, "not_beyond_status_counts": {"missing_second_next_session_first_30m_data": 1, "second_next_session_first_30m_all_closes_inside_prior_ib": 9, "second_next_session_first_30m_not_all_closes_inside_prior_ib": 4}}`
- `terminal`：`{"total_rows": 11, "resolved_rows": 8, "missing_rows": 3, "beyond_status_counts": {"missing_third_next_session_first_30m_data": 1, "third_next_session_first_30m_all_closes_beyond_prior_ib": 1}, "not_beyond_status_counts": {"missing_third_next_session_first_30m_data": 2, "third_next_session_first_30m_all_closes_inside_prior_ib": 6, "third_next_session_first_30m_not_all_closes_inside_prior_ib": 1}}`
- `or_break_only_same_day_session_close`：`{"rows": 325, "return_inside_or_rows": 312, "session_close_beyond_or_rows": 168, "session_close_not_beyond_or_rows": 157, "by_session": {"london": {"rows": 167, "return_inside_or_rows": 165, "session_close_beyond_or_rows": 88, "session_close_not_beyond_or_rows": 79}, "new_york": {"rows": 158, "return_inside_or_rows": 147, "session_close_beyond_or_rows": 80, "session_close_not_beyond_or_rows": 78}}}`
- `or_break_only_branch_cards`：`{"session_close_beyond_or_rows": 168, "session_close_beyond_or_direction_counts": {"down": 96, "up": 72}, "session_close_not_beyond_or_rows": 157, "session_close_not_beyond_or_direction_counts": {"down": 76, "up": 81}}`
- `or_break_only_beyond_next_session_continuation`：`{"rows": 168, "status_counts": {"missing_next_session_first_30m_data": 40, "next_session_first_30m_all_closes_beyond_prior_or": 105, "next_session_first_30m_not_all_closes_beyond_prior_or": 23}, "by_session": {"london": {"rows": 88, "status_missing_next_session_first_30m_data": 19, "status_next_session_first_30m_all_closes_beyond_prior_or": 61, "status_next_session_first_30m_not_all_closes_beyond_prior_or": 8}, "new_york": {"rows": 80, "status_next_session_first_30m_all_closes_beyond_prior_or": 44, "status_missing_next_session_first_30m_data": 21, "status_next_session_first_30m_not_all_closes_beyond_prior_or": 15}}}`
- `or_break_only_beyond_next_session_continuation_card`：`{"rows": 168, "status_counts": {"missing_next_session_first_30m_data": 40, "next_session_first_30m_all_closes_beyond_prior_or": 105, "next_session_first_30m_not_all_closes_beyond_prior_or": 23}, "direction_counts": {"down": 96, "up": 72}}`
- `or_break_only_beyond_multi_session_persistence`：`{"rows": 105, "status_counts": {"missing_second_next_session_first_30m_data": 27, "second_next_session_first_30m_all_closes_beyond_prior_or": 57, "second_next_session_first_30m_not_all_closes_beyond_prior_or": 21}, "by_session": {"london": {"rows": 61, "status_second_next_session_first_30m_not_all_closes_beyond_prior_or": 14, "status_missing_second_next_session_first_30m_data": 17, "status_second_next_session_first_30m_all_closes_beyond_prior_or": 30}, "new_york": {"rows": 44, "status_second_next_session_first_30m_all_closes_beyond_prior_or": 27, "status_missing_second_next_session_first_30m_data": 10, "status_second_next_session_first_30m_not_all_closes_beyond_prior_or": 7}}}`
- `or_break_only_beyond_multi_session_persistence_card`：`{"rows": 105, "status_counts": {"missing_second_next_session_first_30m_data": 27, "second_next_session_first_30m_all_closes_beyond_prior_or": 57, "second_next_session_first_30m_not_all_closes_beyond_prior_or": 21}, "direction_counts": {"down": 55, "up": 50}}`

## 当前裁决

- `GBPUSD/M15` recovered downstream 已完成 slice 化与 terminal summary 收口。
- `or_break_only` 分支已继续推进到 same-day `session_close_beyond_or / session_close_not_beyond_or`，并对 beyond_or 分支补到 next-session continuation 与 multi-session persistence。
- 这条链当前固定停在 `gbpusd_m15_slice_downstream_plus_or_break_only_beyond_multi_session_persistence_done_without_failed_breakout`。
- `no_break_rows` 与缺失后续 session 数据都已显式保留，不再混入 `confirmed cross` 或 `or break only`。
- 当前仍不把任何结果改写成 `failed breakout`。
