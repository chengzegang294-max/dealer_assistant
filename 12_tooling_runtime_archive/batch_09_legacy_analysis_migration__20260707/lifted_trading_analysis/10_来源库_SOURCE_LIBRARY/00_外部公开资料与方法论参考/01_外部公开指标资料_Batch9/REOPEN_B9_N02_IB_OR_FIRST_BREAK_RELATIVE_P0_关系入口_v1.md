# REOPEN_B9_N02 IB OR FIRST_BREAK_RELATIVE_P0 关系入口 v1

## 作用

- 把 `IB vs OR relation` 再向下推进一层，固定 `first_break relative to IB/OR` 的最小证据链。
- 当前只负责：
  - `first_break_direction` 对应的同侧边界对齐关系
  - 当前字段是否足以确认“OR 首破也等于 IB 首破”
  - 若不能确认时，明确写出还缺 `break price`

## 当前边界（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `n02_ib_or_relation_p0_sample_v1.csv`
- 当前只做：
  - 从 `IB_OR relation sample` 派生保守版 `first_break relative`
- 当前明确不做：
  - `IB acceptance`
  - `IB failed breakout`
  - `IB retest/reject`
  - `day type`
  - 任何“只要 OR 首破就等同 IB 首破”的武断升级

## 当前口径（保守写法）

- 若 `first_break_direction` 指向的 OR 边界与 IB 同侧边界完全重合：
  - 可确认：`OR 首破 == IB 同侧首破`
- 若二者同侧边界之间仍有 gap：
  - 只能确认：`OR 首破发生在该侧`
  - 不能确认：`该次首破是否已穿过 IB 同侧边界`
  - 这类行必须显式标记：
    - `requires_break_price_for_ib_confirmation = 1`

## 当前真值组成（v1）

- `relative_entry_md`：`REOPEN_B9_N02_IB_OR_FIRST_BREAK_RELATIVE_P0_关系入口_v1.md`
- `parent_relation_entry_md`：`REOPEN_B9_N02_IB_OR_RELATION_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_first_break_relative_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_first_break_relative_acceptance_v1.md`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_first_break_relative_p0_build_v1.py`
- `source_relation_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_relation_p0_sample_v1.csv`
- `relative_sample_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_first_break_relative_p0_sample_v1.csv`
- `relative_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_first_break_relative_p0_summary_v1.json`

## 最小验收（关系开题级）

- 每一行都能给出：
  - `first_break_direction`
  - `same_side_gap_to_ib`
  - `shared_boundary_on_break_side`
  - `can_confirm_ib_break_from_current_fields`
  - `requires_break_price_for_ib_confirmation`
- `relative_summary_json` 必须显式记录：
  - `confirms_ib_break_only_when_shared_edge=true`
  - `requires_break_price_rows`
  - `first_break_relative_case_counts`

## 2026-07-03 fresh-run

- 运行入口：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_first_break_relative_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_first_break_relative_p0_sample_v1.csv`
  - `n02_ib_or_first_break_relative_p0_summary_v1.json`
- 关键统计：
  - `input_rows=138`
  - `output_rows_written=138`
  - `shared_edge_break_rows=14`
  - `gap_remaining_rows=124`
  - `can_confirm_ib_break_rows=14`
  - `requires_break_price_rows=124`
  - `requires_break_price_ratio=0.8985507246376812`
  - `london shared_edge_break_rows=2`
  - `new_york shared_edge_break_rows=12`
- 当前裁决：
  - 本轮只能对 `14/138` 行确认“OR 首破也等于 IB 同侧首破”
  - 对其余 `124/138` 行，当前字段只能保守写成：
    - `OR 首破已发生`
    - `IB 是否同侧被穿透仍需 break price`

## 2026-07-03 break_bar evidence child 已开

- 已新增子入口：
  - `REOPEN_B9_N02_IB_OR_BREAK_BAR_EVIDENCE_P0_关系入口_v1.md`
- 已新增产物：
  - `n02_ib_or_break_bar_evidence_p0_sample_v1.csv`
  - `n02_ib_or_break_bar_evidence_p0_summary_v1.json`
- 当前最小裁决：
  - `ib_same_side_cross_confirmed_rows=15`
  - `ib_same_side_not_crossed_rows=123`
  - `direction_mode_mismatch_rows=1`
- 当前含义：
  - `requires_break_price` 这一层已被真实首破当根证据替代
  - 同时暴露出 `1` 行上游 relation 的 direction/mode 漂移
  - 当前已继续向下游完成 `confirmed cross / OR break only` 两支分桶

## 下一步最顺动作

- 若继续沿同一条线推进，优先补：
  - 基于 `15` 行 confirmed cross 做最小 outcome 壳
  - 或对 `123` 行继续定义 “OR break only, not IB break”
- 继续保持不做：
  - `acceptance`
  - `failed breakout`
  - `retest / reject`
  - `day type`
