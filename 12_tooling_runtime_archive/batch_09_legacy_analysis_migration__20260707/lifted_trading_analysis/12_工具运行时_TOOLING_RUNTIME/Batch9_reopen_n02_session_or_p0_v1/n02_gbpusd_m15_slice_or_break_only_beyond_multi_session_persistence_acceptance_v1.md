# N02 GBPUSD M15 切片仅 OR 突破超出后多会话延续验收 v1

## 目的

- 记录 `REOPEN_B9_N02_GBPUSD_M15_SLICE_OR_BREAK_ONLY_BEYOND_MULTI_SESSION_PERSISTENCE_P0` 的最小验收结果。

## 本次验收对象

- 脚本：
  - `n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_p0_build_v1.py`
- 产物：
  - `n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_observation_p0_sample_gbpusd_m15_slice_v1.csv`
  - `n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_p0_summary_gbpusd_m15_slice_v1.json`
  - `n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_card_gbpusd_m15_slice_v1.md`
  - `n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_card_summary_gbpusd_m15_slice_v1.json`

## 2026-07-06 fresh-run 验收

- `next_session_first_30m_all_closes_beyond_prior_or_rows=105`
- `second_next_session_first_30m_all_closes_beyond_prior_or_rows=57`
- `second_next_session_first_30m_not_all_closes_beyond_prior_or_rows=21`
- `missing_second_next_session_first_30m_data_rows=27`

## 当前结论

- 已确认 `GBPUSD/M15 slice` 的 `or_break_only` 分支可以在 next-session continuation 的 `all-closes` 子集上继续推进到 second next-session persistence 观察。
- 已确认这层只依赖 `historical_recovered` 的 `GBPUSD/M15` bars 与 `session config`，不污染 `EURUSD/M1` 主链。
- 已确认这层仍不把任何结果改写成 `failed breakout / retest / reject / day type`。

## 当前不通过项

- 当前仍未做：
  - third/更多 session persistence
  - `session_close_not_beyond_or` 的 next-session / multi-session 分层
  - 任意 `failed breakout` 定义
