# n02_ib_or_first_break_relative_runtime_notes v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `first_break relative to IB/OR` 的保守关系层口径。

## 当前边界

- 不写回：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `n02_ib_or_relation_p0_sample_v1.csv`
- 当前只落：
  - `n02_ib_or_first_break_relative_p0_sample_v1.csv`
  - `n02_ib_or_first_break_relative_p0_summary_v1.json`
- 当前不推进：
  - `IB acceptance`
  - `IB failed breakout`
  - `IB retest/reject`
  - `day type`

## 当前怎么用（v1）

- 输入：
  - `n02_ib_or_relation_p0_sample_v1.csv`
- 生成脚本：
  - `n02_ib_or_first_break_relative_p0_build_v1.py`
- 输出：
  - `n02_ib_or_first_break_relative_p0_sample_v1.csv`
  - `n02_ib_or_first_break_relative_p0_summary_v1.json`
- 当前字段只表达：
  - `同侧 OR 边界值`
  - `同侧 IB 边界值`
  - `same_side_gap_to_ib`
  - `shared_boundary_on_break_side`
  - `can_confirm_ib_break_from_current_fields`
  - `requires_break_price_for_ib_confirmation`
- 当前明确不表达：
  - “gap 存在时，这次 OR 首破已经穿透 IB”

## 推荐复现命令

- `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_first_break_relative_p0_build_v1.py`

## 2026-07-03 fresh-run 结果

- 运行入口：
  - `python n02_ib_or_first_break_relative_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_first_break_relative_p0_sample_v1.csv`
  - `n02_ib_or_first_break_relative_p0_summary_v1.json`
- 关键统计：
  - `input_rows=138`
  - `output_rows_written=138`
  - `first_break_relative_case_counts={"or_break_with_ib_same_side_gap_remaining": 124, "shared_edge_break": 14}`
  - `shared_edge_break_rows=14`
  - `gap_remaining_rows=124`
  - `can_confirm_ib_break_rows=14`
  - `requires_break_price_rows=124`
  - `requires_break_price_ratio=0.8985507246376812`
  - `london shared_edge_break_rows=2`
  - `new_york shared_edge_break_rows=12`
- 当前结论：
  - 当前字段只能严格确认 `14` 行 shared-edge 情形。
  - 其余 `124` 行仍然缺 `break price`，不能把 `OR 首破` 直接升级成 `IB 首破`。

## 2026-07-03 break_bar evidence child fresh-run

- 运行入口：
  - `python n02_ib_or_break_bar_evidence_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_break_bar_evidence_p0_sample_v1.csv`
  - `n02_ib_or_break_bar_evidence_p0_summary_v1.json`
- 关键统计：
  - `ib_same_side_cross_confirmed_rows=15`
  - `ib_same_side_not_crossed_rows=123`
  - `direction_mode_match_rows=137`
  - `direction_mode_mismatch_rows=1`
- 当前结论：
  - `requires_break_price` 已不再是当前主缺口
  - 后续应基于 confirmed cross / not crossed 两支继续分流，而不是继续停在保守口径

## 当前最顺动作

- 若继续推进，优先补：
  - `confirmed cross` 的最小 outcome 壳
  - `OR break only` 的分流定义
- 继续保持不做：
  - `acceptance`
  - `failed breakout`
  - `retest / reject`
  - `day type`
