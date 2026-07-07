# REOPEN_B9_N02_GBPUSD_M15_SLICE_DOWNSTREAM_WITHOUT_FAILED_BREAKOUT_P0 关系入口 v1

## 作用

- 对 `GBPUSD/M15 historical recovered -> slice runtime -> downstream terminal summary` 做关系入口级收口。
- 当前专门记录：先前 mixed candidate runtime 已被收紧成纯 `GBPUSD/M15 slice`，并在 `NO failed breakout` 边界下跑到 `terminal summary + or_break_only same-day session close + beyond_or next-session continuation + beyond_or multi-session persistence`。

## 当前边界（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - 任意 `failed breakout / retest / reject / day type`
- 当前不把：
  - `no_break`
  - 缺第二/第三同类 `session` 数据
  冒充成 break / cross / persistence 成功

## 当前真值组成（v1）

- `entry_md`：`REOPEN_B9_N02_GBPUSD_M15_SLICE_DOWNSTREAM_WITHOUT_FAILED_BREAKOUT_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_gbpusd_m15_slice_downstream_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_gbpusd_m15_slice_downstream_acceptance_v1.md`
- `slice_build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_gbpusd_m15_candidate_slice_build_v1.py`
- `downstream_summary_build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_gbpusd_m15_slice_downstream_summary_build_v1.py`
- `summary_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_gbpusd_m15_slice_downstream_summary_v1.md`
- `summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_gbpusd_m15_slice_downstream_summary_v1.json`
- `terminal_summary_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_third_same_session_terminal_summary_gbpusd_m15_slice_v1.md`
- `terminal_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_third_same_session_terminal_summary_gbpusd_m15_slice_v1.json`
- `or_break_only_same_day_session_close_entry_md`：`10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\REOPEN_B9_N02_GBPUSD_M15_SLICE_OR_BREAK_ONLY_SAME_DAY_SESSION_CLOSE_P0_关系入口_v1.md`
- `or_break_only_beyond_next_session_entry_md`：`10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\REOPEN_B9_N02_GBPUSD_M15_SLICE_OR_BREAK_ONLY_BEYOND_NEXT_SESSION_CONTINUATION_P0_关系入口_v1.md`
- `or_break_only_beyond_multi_session_entry_md`：`10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\REOPEN_B9_N02_GBPUSD_M15_SLICE_OR_BREAK_ONLY_BEYOND_MULTI_SESSION_PERSISTENCE_P0_关系入口_v1.md`

## 最小验收（关系开题级）

- slice summary 必须显式记录：
  - `or_slice_rows`
  - `or_defined_rows`
  - `ib_slice_rows`
  - `ib_defined_rows`
- downstream summary 必须显式记录：
  - `first_break_relative_case_counts`
  - `confirmed_cross_rows`
  - `or_break_only_rows`
  - `no_break_rows`
  - `terminal_total_rows`
  - `terminal_resolved_rows`
  - `terminal_missing_rows`
  - `gate_status`
- 所有输出都必须显式保持：
  - `writes_main_runtime=false`
  - `includes_failed_breakout=false`

## 2026-07-06 fresh-run

- 运行入口：
  - `python n02_gbpusd_m15_candidate_slice_build_v1.py`
  - `python n02_gbpusd_m15_slice_downstream_summary_build_v1.py`
- 关键统计：
  - `or_slice_rows=457`
  - `or_defined_rows=396`
  - `ib_slice_rows=457`
  - `ib_defined_rows=396`
  - `confirmed_cross_rows=48`
  - `or_break_only_rows=325`
  - `no_break_rows=23`
  - `terminal_total_rows=11`
  - `terminal_resolved_rows=8`
  - `terminal_missing_rows=3`
  - `or_break_only_return_inside_or_observed_same_day_rows=312`
  - `or_break_only_session_close_beyond_or_rows=168`
  - `or_break_only_session_close_not_beyond_or_rows=157`
  - `or_break_only_beyond_next_session_all_closes_beyond_prior_or_rows=105`
  - `or_break_only_beyond_next_session_not_all_closes_beyond_prior_or_rows=23`
  - `or_break_only_beyond_next_session_missing_rows=40`
  - `or_break_only_beyond_multi_session_all_closes_beyond_prior_or_rows=57`
  - `or_break_only_beyond_multi_session_not_all_closes_beyond_prior_or_rows=21`
  - `or_break_only_beyond_multi_session_missing_rows=27`
  - `gate_status=gbpusd_m15_slice_downstream_plus_or_break_only_beyond_multi_session_persistence_done_without_failed_breakout`
- 当前裁决：
  - 当前 `GBPUSD/M15` recovered 下游链已完成 slice 化并收口到 `terminal summary + or_break_only same-day session close + beyond_or next-session continuation + beyond_or multi-session persistence`。
  - 当前继续保持 `NO failed breakout`。
  - 若后续再扩，优先只在显式需要时处理 `or_break_only beyond multi-session all-closes` 分支，不反向污染主 runtime。

## provenance 说明

- 当前关系入口以 `historical_recovered bars / slice runtime / downstream summary / terminal summary` 共同收口。
- 这层结果不是 `TMGM terminal fresh export`，也不是主 runtime 的直接持久化版本。
