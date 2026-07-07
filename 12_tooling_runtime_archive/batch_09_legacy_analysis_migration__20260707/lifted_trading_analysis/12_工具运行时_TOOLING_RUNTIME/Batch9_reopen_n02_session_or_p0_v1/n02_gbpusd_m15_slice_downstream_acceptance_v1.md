# n02_gbpusd_m15_slice_downstream_acceptance v1

## 目的

- 记录 `REOPEN_B9_N02_GBPUSD_M15_SLICE_DOWNSTREAM_WITHOUT_FAILED_BREAKOUT_P0` 的最小验收结论。

## 本次验收对象

- slice 入口：
  - `n02_gbpusd_m15_candidate_slice_build_v1.py`
  - `n02_gbpusd_m15_candidate_slice_summary_v1.json`
- 下游收口：
  - `n02_gbpusd_m15_slice_downstream_summary_build_v1.py`
  - `n02_gbpusd_m15_slice_downstream_summary_v1.md`
  - `n02_gbpusd_m15_slice_downstream_summary_v1.json`
- terminal 关键产物：
  - `n02_ib_or_third_same_session_terminal_summary_gbpusd_m15_slice_v1.md`
  - `n02_ib_or_third_same_session_terminal_summary_gbpusd_m15_slice_v1.json`

## 2026-07-06 fresh-run 验收

- slice 已独立成立：
  - `or_slice_rows=457`
  - `or_defined_rows=396`
  - `ib_slice_rows=457`
  - `ib_defined_rows=396`
- relation / relative 已独立成立：
  - `relation_rows=396`
  - `first_break_relative_case_counts={"no_break": 23, "or_break_with_ib_same_side_gap_remaining": 325, "shared_edge_break": 48}`
- break / cross 已独立成立：
  - `ib_same_side_cross_confirmed_rows=48`
  - `or_break_only_rows=325`
  - `no_break_rows=23`
- post-cross 与后续 session 观察已独立成立：
  - `post_cross_return_inside_ib_observed_same_day_rows=45`
  - `post_cross_session_close_beyond_ib_rows=27`
  - `multi_beyond_rows=13`
  - `multi_not_beyond_rows=14`
  - `third_beyond_rows=2`
  - `third_not_beyond_rows=9`
- terminal 已独立成立：
  - `terminal_total_rows=11`
  - `terminal_resolved_rows=8`
  - `terminal_missing_rows=3`
- or_break_only same-day session close 已独立成立：
  - `return_inside_or_observed_same_day_rows=312`
  - `session_close_beyond_or_rows=168`
  - `session_close_not_beyond_or_rows=157`
- or_break_only beyond_or next-session continuation 已独立成立：
  - `next_session_continuation_rows=168`
  - `next_session_first_30m_all_closes_beyond_prior_or_rows=105`
  - `next_session_first_30m_not_all_closes_beyond_prior_or_rows=23`
  - `missing_next_session_first_30m_data_rows=40`
- or_break_only beyond_or multi-session persistence 已独立成立：
  - `multi_session_persistence_rows=105`
  - `second_next_session_first_30m_all_closes_beyond_prior_or_rows=57`
  - `second_next_session_first_30m_not_all_closes_beyond_prior_or_rows=21`
  - `missing_second_next_session_first_30m_data_rows=27`
  - `gate_status=gbpusd_m15_slice_downstream_plus_or_break_only_beyond_multi_session_persistence_done_without_failed_breakout`

## 当前结论

- 已确认 `GBPUSD/M15 historical recovered` 可以经由 slice runtime 独立跑完整条 downstream 到 terminal summary，并继续把 `or_break_only` 分支推进到 same-day session close、next-session continuation 与 multi-session persistence。
- 已确认 `no_break` 与缺失后续 session 的样本都被显式落盘，不再错误并入 `confirmed cross` 或 `or_break_only`。
- 已确认当前范围仍然保持：
  - `without_failed_breakout`
  - `writes_main_runtime=false`

## 当前不通过项

- 当前仍未做：
  - `failed breakout / retest / reject / day type`
  - 主 `EURUSD/M1` runtime 污染式持久化
  - 把 `or_break_only beyond_or` 再继续向 third/更多 session persistence 扩展
  - `session_close_not_beyond_or` 的 next-session 分层
