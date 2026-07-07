# REOPEN_B9_N02_GBPUSD_M15_SLICE_OR_BREAK_ONLY_SAME_DAY_SESSION_CLOSE_P0 关系入口 v1

## 作用

- 对 `GBPUSD/M15 slice -> or_break_only -> same-day session close` 做关系入口级收口。
- 当前专门记录：`or_break_only` 分支已从 branch card 继续推进到 same-day `session_close_beyond_or / session_close_not_beyond_or`。

## 当前边界（写死）

- 当前输入只接受：
  - `n02_ib_or_or_break_only_candidates_p0_sample_gbpusd_m15_slice_v1.csv`
  - `real_input_samples\n02_real_input_gbpusd_m15_v1.csv`
- 当前只表达：
  - `return_inside_or_observed_same_day`
  - `session_close_beyond_or`
  - `session_close_not_beyond_or`
- 当前不表达：
  - `failed breakout`
  - `retest / reject / day type`
  - 更深 next-session / multi-session

## 当前真值组成（v1）

- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_gbpusd_m15_slice_or_break_only_same_day_session_close_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_gbpusd_m15_slice_or_break_only_same_day_session_close_acceptance_v1.md`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_same_day_session_close_split_p0_build_v1.py`
- `split_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_same_day_session_close_split_p0_summary_gbpusd_m15_slice_v1.json`
- `beyond_card_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_session_close_beyond_or_card_gbpusd_m15_slice_v1.md`
- `beyond_card_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_session_close_beyond_or_summary_gbpusd_m15_slice_v1.json`
- `not_beyond_card_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_session_close_not_beyond_or_card_gbpusd_m15_slice_v1.md`
- `not_beyond_card_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_session_close_not_beyond_or_summary_gbpusd_m15_slice_v1.json`
- `beyond_next_session_entry_md`：`10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\REOPEN_B9_N02_GBPUSD_M15_SLICE_OR_BREAK_ONLY_BEYOND_NEXT_SESSION_CONTINUATION_P0_关系入口_v1.md`
- `beyond_multi_session_entry_md`：`10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\REOPEN_B9_N02_GBPUSD_M15_SLICE_OR_BREAK_ONLY_BEYOND_MULTI_SESSION_PERSISTENCE_P0_关系入口_v1.md`

## 2026-07-06 fresh-run

- `or_break_only_rows=325`
- `return_inside_or_observed_same_day_rows=312`
- `session_close_beyond_or_rows=168`
- `session_close_not_beyond_or_rows=157`
- `session_close_beyond_or_direction_counts={"down":96,"up":72}`
- `session_close_not_beyond_or_direction_counts={"down":76,"up":81}`

## 当前裁决

- 当前 `or_break_only` 分支已脱离“只有说明卡”的阶段，进入 same-day `session close` 分流。
- 其中 `session_close_beyond_or` 已继续推进到下一同类 session 首 30 分钟 continuation 观察。
- 其中 `next_session_first_30m_all_closes_beyond_prior_or` 子集已继续推进到 second next-session persistence。
- 当前主线仍保持 `NO failed breakout`。
- 若后续继续推进，优先只扩：
  - `session_close_beyond_or` 的 all-closes continuation 样本
  - 或 `session_close_not_beyond_or`
  其中一支，不反向污染 confirmed-cross 主链。
