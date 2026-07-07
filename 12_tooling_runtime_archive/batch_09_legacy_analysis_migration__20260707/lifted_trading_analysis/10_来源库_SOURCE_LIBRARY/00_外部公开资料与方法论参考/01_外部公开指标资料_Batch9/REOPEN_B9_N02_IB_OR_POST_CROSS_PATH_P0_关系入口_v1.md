# REOPEN_B9_N02 IB OR POST_CROSS_PATH_P0 关系入口 v1

## 作用

- 把 `confirmed_cross` 分支继续推进到同日本地日内的 `post_cross_path observation`。
- 同时把 `OR break only` 分支固定为独立说明卡与摘要。
- 当前只表达观测，不把任何观测直接升级成 `failed breakout / retest / reject / day type`。

## 当前边界（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `n02_ib_or_break_bar_evidence_p0_sample_v1.csv`
  - `n02_ib_or_confirmed_cross_outcome_shell_p0_sample_v1.csv`
- 当前不推进：
  - `failed breakout`
  - `retest`
  - `reject`
  - `day type`

## 当前真值组成（v1）

- `entry_md`：`REOPEN_B9_N02_IB_OR_POST_CROSS_PATH_P0_关系入口_v1.md`
- `parent_entry_md`：`REOPEN_B9_N02_IB_OR_CROSS_OUTCOME_SPLIT_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_post_cross_path_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_post_cross_path_acceptance_v1.md`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_post_cross_path_and_or_break_only_card_p0_build_v1.py`
- `confirmed_cross_candidates_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_confirmed_cross_candidates_p0_sample_v1.csv`
- `confirmed_cross_outcome_shell_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_confirmed_cross_outcome_shell_p0_sample_v1.csv`
- `post_cross_observation_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_post_cross_path_observation_p0_sample_v1.csv`
- `post_cross_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_post_cross_path_observation_p0_summary_v1.json`
- `or_break_only_card_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_branch_card_v1.md`
- `or_break_only_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_branch_summary_v1.json`

## 最小验收（关系开题级）

- `confirmed_cross` 每一行都能给出：
  - `return_inside_ib_observed_same_day`
  - `first_return_inside_ib_bar_time_utc`
  - `session_close_beyond_ib`
- `OR break only` 分支必须有：
  - 独立说明卡
  - gap bucket / direction / mode 摘要
- 当前所有输出都必须显式保留：
  - `defines_failed_breakout=false`

## 2026-07-03 fresh-run

- 运行入口：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_post_cross_path_and_or_break_only_card_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_post_cross_path_observation_p0_sample_v1.csv`
  - `n02_ib_or_post_cross_path_observation_p0_summary_v1.json`
  - `n02_ib_or_or_break_only_branch_card_v1.md`
  - `n02_ib_or_or_break_only_branch_summary_v1.json`
- 关键统计：
  - `post_cross_rows=15`
  - `post_cross_return_inside_ib_observed_same_day_rows=15`
  - `post_cross_session_close_beyond_ib_rows=9`
  - `or_break_only_rows=123`
  - `or_break_only_gap_bucket_counts={"0.00010_to_0.00049": 64, "ge_0.00050": 30, "lt_0.00010": 29}`
- 当前裁决：
  - `confirmed_cross` 分支的 `15/15` 行都观察到了同日本地日内回到 `IB` 边界内侧。
  - 其中 `9/15` 行在当日收盘仍保持在 `IB` 外侧。
  - `OR break only` 分支已具备独立说明卡，不再需要和 `confirmed_cross` 混写。
  - 当前仍只把这些作为 observation / branch card，不升级成 `failed breakout`。

## 2026-07-03 return_inside_and_session_close_split child 已开

- 已新增子入口：
  - `REOPEN_B9_N02_IB_OR_RETURN_INSIDE_AND_SESSION_CLOSE_SPLIT_P0_关系入口_v1.md`
- 已新增产物：
  - `n02_ib_or_return_inside_ib_same_day_candidates_p0_sample_v1.csv`
  - `n02_ib_or_return_inside_ib_same_day_card_v1.md`
  - `n02_ib_or_session_close_beyond_ib_candidates_p0_sample_v1.csv`
  - `n02_ib_or_session_close_not_beyond_ib_candidates_p0_sample_v1.csv`
  - `n02_ib_or_session_close_beyond_split_p0_summary_v1.json`
- 当前最小裁决：
  - `return_inside_rows=15`
  - `session_close_beyond_ib_rows=9`
  - `session_close_not_beyond_ib_rows=6`
- 当前含义：
  - `return_inside` 已固定成独立说明卡
  - `session_close` 已完成 beyond / not_beyond 二次分桶
  - 当前已继续向下游固定 `session_close_beyond` 与 `not_beyond_pullback` 两张分支说明卡

## 下一步最顺动作

- 若继续沿同一条线推进，优先补：
  - `session_close_beyond_ib=9` 的独立说明卡
  - 或 `session_close_not_beyond_ib=6` 的回落分支说明
- 继续保持不做：
  - `failed breakout`
  - `retest / reject`
  - `day type`
