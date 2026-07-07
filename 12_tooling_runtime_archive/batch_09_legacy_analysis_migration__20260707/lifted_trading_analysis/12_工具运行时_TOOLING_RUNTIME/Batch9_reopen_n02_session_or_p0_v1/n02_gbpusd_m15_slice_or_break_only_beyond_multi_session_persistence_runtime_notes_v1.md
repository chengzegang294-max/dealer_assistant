# n02_gbpusd_m15_slice_or_break_only_beyond_multi_session_persistence_runtime_notes v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是把 `GBPUSD/M15 slice -> or_break_only -> session_close_beyond_or -> next-session all-closes -> second next-session first 30m` 固定成可追溯闭环。

## 当前边界

- 当前输入只来自：
  - `n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_observation_p0_sample_gbpusd_m15_slice_v1.csv`
  - `real_input_samples\n02_real_input_gbpusd_m15_v1.csv`
  - `real_input_samples\n02_or_proof_config_v1.json`
- 当前只观察：
  - `second_next_session_first_30m_all_closes_beyond_prior_or`
  - `second_next_session_first_30m_not_all_closes_beyond_prior_or`
  - `missing_second_next_session_first_30m_data`
- 当前不定义：
  - `failed breakout`
  - `retest / reject / day type`
  - 第三/更多 session 的 persistence

## 当前怎么跑（v1）

- 生成脚本：
  - `n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_p0_build_v1.py`
- 关键产物：
  - `n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_observation_p0_sample_gbpusd_m15_slice_v1.csv`
  - `n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_p0_summary_gbpusd_m15_slice_v1.json`
  - `n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_card_gbpusd_m15_slice_v1.md`
  - `n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_card_summary_gbpusd_m15_slice_v1.json`

## 2026-07-06 fresh-run 结果

- `next_session_first_30m_all_closes_beyond_prior_or_rows=105`
- `second_next_session_first_30m_all_closes_beyond_prior_or_rows=57`
- `second_next_session_first_30m_not_all_closes_beyond_prior_or_rows=21`
- `missing_second_next_session_first_30m_data_rows=27`

## 当前结论

- `or_break_only` 分支已从 next-session continuation 的 `all-closes` 子集进一步推进到 second next-session 首 30 分钟 persistence 观察。
- 当前主线可明确区分：
  - 第二个 next-session 首 30 分钟全体 close 仍在 prior `OR` 外侧同方向
  - 第二个 next-session 首 30 分钟未能全体保持在 prior `OR` 外侧
  - 因缺 bars 导致无法观察第二个 next-session
- 这层结果仍然只属于 `without_failed_breakout`。
