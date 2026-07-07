# REOPEN_B9_N02_GBPUSD_M15_SLICE_OR_BREAK_ONLY_BEYOND_NEXT_SESSION_CONTINUATION_P0 关系入口 v1

## 作用

- 对 `GBPUSD/M15 slice -> or_break_only -> session_close_beyond_or -> next same-session first 30m continuation` 做关系入口级收口。
- 当前专门记录：`or_break_only` 分支已从 same-day `session_close_beyond_or` 继续推进到下一同类 session 首 30 分钟 continuation 观察。

## 当前边界（写死）

- 当前输入只接受：
  - `n02_ib_or_or_break_only_session_close_beyond_or_candidates_p0_sample_gbpusd_m15_slice_v1.csv`
  - `real_input_samples\n02_real_input_gbpusd_m15_v1.csv`
  - `real_input_samples\n02_or_proof_config_v1.json`
- 当前只表达：
  - `next_session_first_30m_all_closes_beyond_prior_or`
  - `next_session_first_30m_not_all_closes_beyond_prior_or`
  - `missing_next_session_first_30m_data`
- 当前不表达：
  - `failed breakout`
  - `retest / reject / day type`
  - 更深 third/更多 session persistence

## 当前真值组成（v1）

- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_gbpusd_m15_slice_or_break_only_beyond_next_session_continuation_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_gbpusd_m15_slice_or_break_only_beyond_next_session_continuation_acceptance_v1.md`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_p0_build_v1.py`
- `observation_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_observation_p0_sample_gbpusd_m15_slice_v1.csv`
- `summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_p0_summary_gbpusd_m15_slice_v1.json`
- `card_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_card_gbpusd_m15_slice_v1.md`
- `card_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_card_summary_gbpusd_m15_slice_v1.json`

## 2026-07-06 fresh-run

- `session_close_beyond_or_rows=168`
- `next_session_first_30m_all_closes_beyond_prior_or_rows=105`
- `next_session_first_30m_not_all_closes_beyond_prior_or_rows=23`
- `missing_next_session_first_30m_data_rows=40`
- `london_status_counts={"missing_next_session_first_30m_data":19,"next_session_first_30m_all_closes_beyond_prior_or":61,"next_session_first_30m_not_all_closes_beyond_prior_or":8}`
- `new_york_status_counts={"missing_next_session_first_30m_data":21,"next_session_first_30m_all_closes_beyond_prior_or":44,"next_session_first_30m_not_all_closes_beyond_prior_or":15}`

## 当前裁决

- 当前 `or_break_only` 分支已从 same-day `session_close_beyond_or` 进入 next-session continuation 观察。
- 其中 `next_session_first_30m_all_closes_beyond_prior_or` 子集已继续推进到：`REOPEN_B9_N02_GBPUSD_M15_SLICE_OR_BREAK_ONLY_BEYOND_MULTI_SESSION_PERSISTENCE_P0`。
- 当前主线仍保持 `NO failed breakout`。
- 若后续继续推进，优先只扩：
  - `next_session_first_30m_all_closes_beyond_prior_or`
  这一支，不反向污染 confirmed-cross 主链。
