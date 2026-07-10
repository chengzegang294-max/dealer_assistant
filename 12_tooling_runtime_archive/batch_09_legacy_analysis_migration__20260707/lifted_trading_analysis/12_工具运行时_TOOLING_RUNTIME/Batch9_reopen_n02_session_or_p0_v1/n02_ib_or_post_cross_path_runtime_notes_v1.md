# N02 IB OR 过交叉后路径运行说明 v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `confirmed_cross` 分支的同日 `post_cross_path observation`，以及 `OR break only` 分支的说明卡口径。

## 当前边界

- 不写回：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `n02_ib_or_break_bar_evidence_p0_sample_v1.csv`
- 当前只落：
  - `n02_ib_or_post_cross_path_observation_p0_sample_v1.csv`
  - `n02_ib_or_post_cross_path_observation_p0_summary_v1.json`
  - `n02_ib_or_or_break_only_branch_card_v1.md`
  - `n02_ib_or_or_break_only_branch_summary_v1.json`
- 当前不推进：
  - `failed breakout`
  - `retest`
  - `reject`
  - `day type`

## 当前怎么用（v1）

- 输入：
  - `n02_ib_or_confirmed_cross_candidates_p0_sample_v1.csv`
  - `n02_ib_or_confirmed_cross_outcome_shell_p0_sample_v1.csv`
  - `n02_ib_or_or_break_only_candidates_p0_sample_v1.csv`
  - `real_input_samples\n02_first_real_input_bars_v1.csv`
- 生成脚本：
  - `n02_ib_or_post_cross_path_and_or_break_only_card_p0_build_v1.py`
- 输出：
  - `n02_ib_or_post_cross_path_observation_p0_sample_v1.csv`
  - `n02_ib_or_post_cross_path_observation_p0_summary_v1.json`
  - `n02_ib_or_or_break_only_branch_card_v1.md`
  - `n02_ib_or_or_break_only_branch_summary_v1.json`
- 当前字段只表达：
  - `return_inside_ib_observed_same_day`
  - `first_return_inside_ib_bar_time_utc`
  - `session_close_beyond_ib`
  - `OR break only` 的稳定说明卡

## 推荐复现命令

- `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_post_cross_path_and_or_break_only_card_p0_build_v1.py`

## 2026-07-03 fresh-run 结果

- 运行入口：
  - `python n02_ib_or_post_cross_path_and_or_break_only_card_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_post_cross_path_observation_p0_sample_v1.csv`
  - `n02_ib_or_post_cross_path_observation_p0_summary_v1.json`
  - `n02_ib_or_or_break_only_branch_card_v1.md`
  - `n02_ib_or_or_break_only_branch_summary_v1.json`
- 关键统计：
  - `post_cross_rows=15`
  - `return_inside_ib_observed_same_day_rows=15`
  - `session_close_beyond_ib_rows=9`
  - `or_break_only_rows=123`
  - `or_break_only_gap_bucket_counts={"0.00010_to_0.00049": 64, "ge_0.00050": 30, "lt_0.00010": 29}`
- 当前结论：
  - `confirmed_cross` 分支的 `15/15` 行都在同日本地日内观察到了回到 `IB` 边界内侧。
  - `9/15` 行在当日收盘仍保持在 `IB` 外侧。
  - `OR break only` 分支已具备独立 branch card。
  - 这些都仍是 observation / card，不是 `failed breakout` 定义。

## 2026-07-03 return_inside_and_session_close_split child fresh-run

- 运行入口：
  - `python n02_ib_or_return_inside_and_session_close_split_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_return_inside_ib_same_day_candidates_p0_sample_v1.csv`
  - `n02_ib_or_return_inside_ib_same_day_card_v1.md`
  - `n02_ib_or_return_inside_ib_same_day_summary_v1.json`
  - `n02_ib_or_session_close_beyond_ib_candidates_p0_sample_v1.csv`
  - `n02_ib_or_session_close_not_beyond_ib_candidates_p0_sample_v1.csv`
  - `n02_ib_or_session_close_beyond_split_p0_summary_v1.json`
- 关键统计：
  - `return_inside_rows=15`
  - `session_close_beyond_ib_rows=9`
  - `session_close_not_beyond_ib_rows=6`
  - `session_close_beyond_ib_ratio=0.6`
- 当前结论：
  - 主线已从 `post_cross observation` 推进到 `return_inside card + session_close split`
  - 当前仍只写 observation / split，不写 `failed breakout` 定义

## 当前最顺动作

- 若继续推进，优先补：
  - `session_close_beyond_ib=9` 的独立说明卡
  - 或 `session_close_not_beyond_ib=6` 的回落分支说明
- 继续保持不做：
  - `failed breakout`
  - `retest / reject`
  - `day type`
