# REOPEN_B9_N02 IB OR BREAK_BAR_EVIDENCE_P0 关系入口 v1

## 作用

- 把 `first_break relative to IB/OR` 从“还缺 break price”推进到“已有首破当根价位证据”。
- 当前只负责：
  - 首破当根 `bar_time/open/high/low/close`
  - `break_trigger_price`
  - 是否已穿过 `IB` 同侧边界
  - 与上游 `first_break_direction/mode` 是否一致

## 当前边界（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `n02_ib_or_relation_p0_sample_v1.csv`
  - `n02_ib_or_first_break_relative_p0_sample_v1.csv`
- 当前不推进：
  - `IB acceptance`
  - `IB failed breakout`
  - `IB retest/reject`
  - `day type`

## 当前真值组成（v1）

- `entry_md`：`REOPEN_B9_N02_IB_OR_BREAK_BAR_EVIDENCE_P0_关系入口_v1.md`
- `parent_entry_md`：`REOPEN_B9_N02_IB_OR_FIRST_BREAK_RELATIVE_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_break_bar_evidence_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_break_bar_evidence_acceptance_v1.md`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_break_bar_evidence_p0_build_v1.py`
- `relative_sample_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_first_break_relative_p0_sample_v1.csv`
- `relation_sample_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_relation_p0_sample_v1.csv`
- `bars_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_first_real_input_bars_v1.csv`
- `break_bar_evidence_sample_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_break_bar_evidence_p0_sample_v1.csv`
- `break_bar_evidence_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_break_bar_evidence_p0_summary_v1.json`

## 最小验收（关系开题级）

- 每一行都能给出：
  - `break_bar_time_utc`
  - `break_bar_open/high/low/close`
  - `break_trigger_price`
  - `ib_same_side_cross_confirmed`
  - `direction_mode_match_to_relation`
- `summary_json` 必须显式记录：
  - `ib_same_side_cross_confirmed_rows`
  - `ib_same_side_not_crossed_rows`
  - `direction_mode_mismatch_rows`

## 2026-07-03 fresh-run

- 运行入口：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_break_bar_evidence_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_break_bar_evidence_p0_sample_v1.csv`
  - `n02_ib_or_break_bar_evidence_p0_summary_v1.json`
- 关键统计：
  - `input_rows=138`
  - `output_rows_written=138`
  - `ib_same_side_cross_confirmed_rows=15`
  - `ib_same_side_not_crossed_rows=123`
  - `ib_same_side_cross_confirmed_ratio=0.10869565217391304`
  - `direction_mode_match_rows=137`
  - `direction_mode_mismatch_rows=1`
  - `london cross_confirmed_rows=2`
  - `new_york cross_confirmed_rows=13`
- 当前裁决：
  - 这层已经不再需要 `break price` 补证。
  - 当前样本里，只有 `15/138` 行的首破当根已经穿过 `IB` 同侧边界。
  - 其余 `123/138` 行已拿到当根价位，但确认结果是“首破发生了，仍未穿过 `IB` 同侧边界”。
  - 另有 `1` 行出现 `direction/mode` 与上游 relation 不一致，已作为上游漂移证据保留。
  - 当前漂移样本定位为：`new_york / 2026-05-07 / upstream=down+close / recheck=down+wick`

## 2026-07-03 cross outcome split child 已开

- 已新增子入口：
  - `REOPEN_B9_N02_IB_OR_CROSS_OUTCOME_SPLIT_P0_关系入口_v1.md`
- 已新增产物：
  - `n02_ib_or_confirmed_cross_candidates_p0_sample_v1.csv`
  - `n02_ib_or_or_break_only_candidates_p0_sample_v1.csv`
  - `n02_ib_or_confirmed_cross_outcome_shell_p0_sample_v1.csv`
  - `n02_ib_or_cross_outcome_split_p0_summary_v1.json`
- 当前最小裁决：
  - `confirmed_cross_rows=15`
  - `or_break_only_rows=123`
  - `outcome_shell_rows=15`
- 当前含义：
  - 当前主线已不再停在 `break_bar evidence`
  - 后续应从 `confirmed_cross` 与 `OR break only` 两支分别继续推进
  - 当前已继续进入 `post_cross_path observation` 与 `OR break only branch card`

## 下一步最顺动作

- 若继续沿同一条线推进，优先补：
  - `confirmed cross` 分支的最小 post-cross path 定义
  - 或 `OR break only` 分支的稳定说明卡
- 继续保持不做：
  - `acceptance`
  - `retest / reject`
  - `day type`
