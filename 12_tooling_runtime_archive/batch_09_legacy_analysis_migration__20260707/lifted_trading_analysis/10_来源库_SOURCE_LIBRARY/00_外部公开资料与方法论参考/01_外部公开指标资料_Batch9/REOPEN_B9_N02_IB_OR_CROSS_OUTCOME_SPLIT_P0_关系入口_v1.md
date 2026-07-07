# REOPEN_B9_N02 IB OR CROSS_OUTCOME_SPLIT_P0 关系入口 v1

## 作用

- 把 `break_bar evidence` 继续推进成两支可复现分流：
  - `confirmed cross`
  - `OR break only`
- 同时给 `confirmed cross` 新开最小 `outcome_shell`，只声明“进入 post-cross 跟踪域”，不提前定义 `failed breakout / retest / reject / day type`。

## 当前边界（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `n02_ib_or_break_bar_evidence_p0_sample_v1.csv`
- 当前不推进：
  - `failed breakout`
  - `retest`
  - `reject`
  - `day type`
  - 任何结果级交易门控

## 当前真值组成（v1）

- `entry_md`：`REOPEN_B9_N02_IB_OR_CROSS_OUTCOME_SPLIT_P0_关系入口_v1.md`
- `parent_entry_md`：`REOPEN_B9_N02_IB_OR_BREAK_BAR_EVIDENCE_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_cross_outcome_split_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_cross_outcome_split_acceptance_v1.md`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_cross_outcome_split_p0_build_v1.py`
- `break_bar_evidence_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_break_bar_evidence_p0_sample_v1.csv`
- `confirmed_cross_candidates_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_confirmed_cross_candidates_p0_sample_v1.csv`
- `or_break_only_candidates_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_candidates_p0_sample_v1.csv`
- `confirmed_cross_outcome_shell_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_confirmed_cross_outcome_shell_p0_sample_v1.csv`
- `summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_cross_outcome_split_p0_summary_v1.json`

## 最小验收（关系开题级）

- `138` 行必须全部进入两支之一：
  - `confirmed cross`
  - `OR break only`
- `confirmed_cross_outcome_shell_csv` 只覆盖 `confirmed cross` 分支
- `summary_json` 必须显式记录：
  - `confirmed_cross_rows`
  - `or_break_only_rows`
  - `outcome_shell_rows`
  - `direction_mode_mismatch_rows`

## 2026-07-03 fresh-run

- 运行入口：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_cross_outcome_split_p0_build_v1.py`
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
- 当前裁决：
  - `confirmed cross` 与 `OR break only` 已完成独立分桶。
  - `confirmed_cross_outcome_shell` 已把 `15` 行推进到 post-cross 跟踪入口。
  - 这一步仍不等于已定义 `failed breakout` 或其他 outcome。

## 2026-07-03 post_cross_path child 已开

- 已新增子入口：
  - `REOPEN_B9_N02_IB_OR_POST_CROSS_PATH_P0_关系入口_v1.md`
- 已新增产物：
  - `n02_ib_or_post_cross_path_observation_p0_sample_v1.csv`
  - `n02_ib_or_post_cross_path_observation_p0_summary_v1.json`
  - `n02_ib_or_or_break_only_branch_card_v1.md`
  - `n02_ib_or_or_break_only_branch_summary_v1.json`
- 当前最小裁决：
  - `return_inside_ib_observed_same_day_rows=15`
  - `session_close_beyond_ib_rows=9`
  - `or_break_only_rows=123`
- 当前含义：
  - `confirmed cross` 已有同日 post-cross 观察
  - `OR break only` 已有独立说明卡
  - 当前已继续向下游固定 `return_inside` 说明卡与 `session_close` 二次分桶
  - 当前已继续新开 `session_close` 两张独立 branch card

## 下一步最顺动作

- 若继续沿同一条线推进，优先补：
  - `session_close_beyond_ib=9` 的 continuation / persistence 观察
  - 或 `session_close_not_beyond_ib=6` 的 pullback stability 观察
- 继续保持不做：
  - `failed breakout`
  - `retest / reject`
  - `day type`
