# REOPEN_B9_N02 IB OR RELATION_P0 关系入口 v1

## 作用

- 把 `IB_OBJECT_P0` 与 `N02 P0 OR runtime v2` 之间的第一层关系固定为可复现子项。
- 当前只负责：
  - `IB vs OR` 的最小关系样本
  - `OR inside IB` 的基础裁决
  - `IB width vs OR width` 的最小对比
- 当前仍不负责：
  - `IB acceptance`
  - `IB failed breakout`
  - `IB retest/reject`
  - `day type`

## 当前边界（写死）

- 不写入：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_p0_fields_runtime_v2.csv`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_fields_runtime_v1.csv`
- 只做：
  - `IB object sample` 与 `OR runtime v2` 的 join
  - 关系样本与摘要落盘
- 不做：
  - 任何行为门控
  - 任何 `acceptance / failed breakout / retest-reject / day type` 结论升级

## 入口依赖

- `IB object sample`：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_object_p0_sample_v1.csv`
- `OR runtime v2`：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_p0_fields_runtime_v2.csv`
- 关系生成脚本：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_relation_p0_build_v1.py`

## 当前真值组成（v1）

- `relation_entry_md`：`REOPEN_B9_N02_IB_OR_RELATION_P0_关系入口_v1.md`
- `object_entry_md`：`REOPEN_B9_N02_IB_OBJECT_P0_对象入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_relation_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_relation_acceptance_v1.md`
- `relation_build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_relation_p0_build_v1.py`
- `ib_object_sample_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_object_p0_sample_v1.csv`
- `or_runtime_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_p0_fields_runtime_v2.csv`
- `relation_sample_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_relation_p0_sample_v1.csv`
- `relation_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_relation_p0_summary_v1.json`

## 最小验收（关系开题级）

- `IB object sample` 与 `OR runtime v2` 能稳定 join
- `relation_sample_csv` 中每行都有稳定 `relation_id`
- `relation_summary_json` 显式记录：
  - `producer`
  - `scope`
  - `evidence_mode`
  - `source_path`
  - `repo_path`
  - 关系层边界布尔项
- 当前至少满足：
  - `relation_rows_written > 0`
  - `missing_or_match_rows = 0`
  - `or_inside_ib_rows / relation_rows_written` 可直接观测

## 2026-07-03 relation fresh-run

- 运行入口：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_relation_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_relation_p0_sample_v1.csv`
  - `n02_ib_or_relation_p0_summary_v1.json`
- 关键统计：
  - `ib_object_rows_input=138`
  - `or_runtime_rows_input=165`
  - `relation_rows_written=138`
  - `missing_or_match_rows=0`
  - `or_inside_ib_rows=138`
  - `or_inside_ib_ratio=1.0`
  - `ib_equals_or_rows=14`
  - `width_error_day_rows=0`
  - `first_break_direction_counts={"down": 56, "up": 82}`
  - `first_break_mode_counts={"close": 76, "wick": 62}`
- 当前裁决：
  - `IB vs OR` 的最小关系层已可复现
  - 当前更稳的表述是：
    - `OR` 在本轮已定义样本中全部落在 `IB` 内部
    - `IB` 平均宽度约为 `OR` 的 `1.6806x`
  - 仍不把这一步升级成 `IB acceptance` 或策略门控

## 2026-07-03 first_break relative child 已开

- 已新增子入口：
  - `REOPEN_B9_N02_IB_OR_FIRST_BREAK_RELATIVE_P0_关系入口_v1.md`
- 已新增产物：
  - `n02_ib_or_first_break_relative_p0_sample_v1.csv`
  - `n02_ib_or_first_break_relative_p0_summary_v1.json`
- 当前最小裁决：
  - `shared_edge_break_rows=14`
  - `gap_remaining_rows=124`
  - `requires_break_price_rows=124`
- 当前含义：
  - `first_break relative to IB/OR` 已从“下一步”升级为“保守可复现证据”
  - 但当前仍只确认 shared-edge 行，不确认所有 `OR 首破` 都等于 `IB 首破`
  - 这层已继续向下游支撑 `break_bar evidence`，当前主缺口已不再是 `break price`

## 下一步最顺动作

- 若继续沿同一条线推进，优先考虑：
  - 补 `first_break bar price` 或等价字段
  - 再缩减 `requires_break_price=1` 的行
  - 更广 session/sample 覆盖
- 继续保持不做：
  - `acceptance`
  - `failed breakout`
  - `retest / reject`
  - `day type`
