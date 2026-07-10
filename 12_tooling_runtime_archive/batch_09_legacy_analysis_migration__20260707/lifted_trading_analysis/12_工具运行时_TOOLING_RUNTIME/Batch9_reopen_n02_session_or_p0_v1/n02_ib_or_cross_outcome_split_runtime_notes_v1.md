# N02 IB OR 过交叉结果分桶运行说明 v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `confirmed cross` 与 `OR break only` 的分桶结果，以及 `confirmed cross outcome shell` 的运行口径。

## 当前边界

- 不写回：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `n02_ib_or_break_bar_evidence_p0_sample_v1.csv`
- 当前只落：
  - `n02_ib_or_confirmed_cross_candidates_p0_sample_v1.csv`
  - `n02_ib_or_or_break_only_candidates_p0_sample_v1.csv`
  - `n02_ib_or_confirmed_cross_outcome_shell_p0_sample_v1.csv`
  - `n02_ib_or_cross_outcome_split_p0_summary_v1.json`
- 当前不推进：
  - `failed breakout`
  - `retest`
  - `reject`
  - `day type`

## 当前怎么用（v1）

- 输入：
  - `n02_ib_or_break_bar_evidence_p0_sample_v1.csv`
- 生成脚本：
  - `n02_ib_or_cross_outcome_split_p0_build_v1.py`
- 输出：
  - `n02_ib_or_confirmed_cross_candidates_p0_sample_v1.csv`
  - `n02_ib_or_or_break_only_candidates_p0_sample_v1.csv`
  - `n02_ib_or_confirmed_cross_outcome_shell_p0_sample_v1.csv`
  - `n02_ib_or_cross_outcome_split_p0_summary_v1.json`
- 当前字段只表达：
  - 哪些行属于 `confirmed cross`
  - 哪些行属于 `OR break only`
  - `confirmed cross` 已进入 `post_cross_path_pending_definition`

## 推荐复现命令

- `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_cross_outcome_split_p0_build_v1.py`

## 2026-07-03 fresh-run 结果

- 运行入口：
  - `python n02_ib_or_cross_outcome_split_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_confirmed_cross_candidates_p0_sample_v1.csv`
  - `n02_ib_or_or_break_only_candidates_p0_sample_v1.csv`
  - `n02_ib_or_confirmed_cross_outcome_shell_p0_sample_v1.csv`
  - `n02_ib_or_cross_outcome_split_p0_summary_v1.json`
- 关键统计：
  - `input_rows=138`
  - `confirmed_cross_rows=15`
  - `or_break_only_rows=123`
  - `outcome_shell_rows=15`
  - `direction_mode_mismatch_rows=1`
  - `london confirmed_cross_rows=2`
  - `new_york confirmed_cross_rows=13`
- 当前结论：
  - `confirmed cross` 和 `OR break only` 已完成稳定分桶。
  - `confirmed_cross_outcome_shell` 已给 `15` 行建立 post-cross 跟踪入口。
  - 当前仍不把 `outcome_shell` 误写成 `failed breakout` 或其他结果定义。

## 2026-07-03 post_cross_path child fresh-run

- 运行入口：
  - `python n02_ib_or_post_cross_path_and_or_break_only_card_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_post_cross_path_observation_p0_sample_v1.csv`
  - `n02_ib_or_post_cross_path_observation_p0_summary_v1.json`
  - `n02_ib_or_or_break_only_branch_card_v1.md`
  - `n02_ib_or_or_break_only_branch_summary_v1.json`
- 关键统计：
  - `return_inside_ib_observed_same_day_rows=15`
  - `session_close_beyond_ib_rows=9`
  - `or_break_only_rows=123`
- 当前结论：
  - 主线已从“只分桶”推进到“confirmed_cross 同日观察 + OR break only 说明卡”
  - 当前仍只写 observation / card，不写结果定义

## 当前最顺动作

- 若继续推进，优先补：
  - `return_inside_ib_observed_same_day` 的说明卡
  - 或 `session_close_beyond_ib` 的二次分桶
- 继续保持不做：
  - `failed breakout`
  - `retest / reject`
  - `day type`
