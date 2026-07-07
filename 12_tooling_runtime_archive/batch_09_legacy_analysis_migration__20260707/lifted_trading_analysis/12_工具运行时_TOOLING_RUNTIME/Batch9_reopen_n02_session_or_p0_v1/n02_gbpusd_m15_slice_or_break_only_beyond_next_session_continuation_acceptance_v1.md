# n02_gbpusd_m15_slice_or_break_only_beyond_next_session_continuation_acceptance v1

## 目的

- 记录 `REOPEN_B9_N02_GBPUSD_M15_SLICE_OR_BREAK_ONLY_BEYOND_NEXT_SESSION_CONTINUATION_P0` 的最小验收结果。

## 本次验收对象

- 脚本：
  - `n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_p0_build_v1.py`
- 产物：
  - `n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_observation_p0_sample_gbpusd_m15_slice_v1.csv`
  - `n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_p0_summary_gbpusd_m15_slice_v1.json`
  - `n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_card_gbpusd_m15_slice_v1.md`
  - `n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_card_summary_gbpusd_m15_slice_v1.json`

## 2026-07-06 fresh-run 验收

- `session_close_beyond_or_rows=168`
- `next_session_first_30m_all_closes_beyond_prior_or_rows=105`
- `next_session_first_30m_not_all_closes_beyond_prior_or_rows=23`
- `missing_next_session_first_30m_data_rows=40`
- `london_rows=88`
- `new_york_rows=80`
- `next_session_first_30m_full_window_rows=128`
- `next_session_first_bar_expected_side_rows=106`

## 当前结论

- 已确认 `GBPUSD/M15 slice` 的 `or_break_only -> session_close_beyond_or` 分支可以独立落到下一同类 session 首 30 分钟 continuation 观察。
- 已确认这层只依赖 `historical_recovered` 的 `GBPUSD/M15` bars 与 `session config`，不污染 `EURUSD/M1` 主链。
- 已确认这层仍不把任何结果改写成 `failed breakout / retest / reject / day type`。

## 当前不通过项

- 当前仍未做：
  - `second_next_session_first_30m_all_closes_beyond_prior_or` 之后的 third/更多 session persistence
  - `session_close_not_beyond_or` 的 next-session 分层
  - 任意 `failed breakout` 定义
