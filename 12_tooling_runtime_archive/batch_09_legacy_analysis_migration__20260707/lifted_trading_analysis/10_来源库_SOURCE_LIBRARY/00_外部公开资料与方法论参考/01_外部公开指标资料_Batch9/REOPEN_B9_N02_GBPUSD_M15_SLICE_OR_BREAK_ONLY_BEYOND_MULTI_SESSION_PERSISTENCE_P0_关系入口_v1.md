# REOPEN_B9_N02_GBPUSD_M15_SLICE_OR_BREAK_ONLY_BEYOND_MULTI_SESSION_PERSISTENCE_P0 关系入口 v1

## 作用

- 对 `GBPUSD/M15 slice -> or_break_only -> session_close_beyond_or -> next-session all-closes -> second next-session first 30m` 做关系入口级收口。
- 当前专门记录：`or_break_only` 分支已从 next-session continuation 的 `all-closes` 子集继续推进到 second next-session persistence 观察。

## 当前边界（写死）

- 当前输入只接受：
  - `n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_observation_p0_sample_gbpusd_m15_slice_v1.csv`
  - `real_input_samples\n02_real_input_gbpusd_m15_v1.csv`
  - `real_input_samples\n02_or_proof_config_v1.json`
- 当前只表达：
  - `second_next_session_first_30m_all_closes_beyond_prior_or`
  - `second_next_session_first_30m_not_all_closes_beyond_prior_or`
  - `missing_second_next_session_first_30m_data`
- 当前不表达：
  - `failed breakout`
  - `retest / reject / day type`
  - 第三/更多 session persistence

## 当前真值组成（v1）

- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_gbpusd_m15_slice_or_break_only_beyond_multi_session_persistence_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_gbpusd_m15_slice_or_break_only_beyond_multi_session_persistence_acceptance_v1.md`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_p0_build_v1.py`
- `observation_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_observation_p0_sample_gbpusd_m15_slice_v1.csv`
- `summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_p0_summary_gbpusd_m15_slice_v1.json`
- `card_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_card_gbpusd_m15_slice_v1.md`
- `card_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_card_summary_gbpusd_m15_slice_v1.json`

## 2026-07-06 fresh-run

- `next_session_first_30m_all_closes_beyond_prior_or_rows=105`
- `second_next_session_first_30m_all_closes_beyond_prior_or_rows=57`
- `second_next_session_first_30m_not_all_closes_beyond_prior_or_rows=21`
- `missing_second_next_session_first_30m_data_rows=27`

## 当前裁决

- 当前 `or_break_only` 分支已进入 multi-session persistence 观察层，但仍属于 `without_failed_breakout`。
- 若后续继续推进，优先只扩：
  - `second_next_session_first_30m_all_closes_beyond_prior_or`
  这一支，不反向污染 confirmed-cross 主链。
