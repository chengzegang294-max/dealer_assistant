# N02 IB 与 OR 关系层运行说明 v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `IB_OBJECT_P0` 与 `N02 P0 OR runtime v2` 的最小关系层口径。

## 当前边界

- 不写回：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
- 当前只落：
  - `n02_ib_or_relation_p0_sample_v1.csv`
  - `n02_ib_or_relation_p0_summary_v1.json`
- 当前不推进：
  - `IB acceptance`
  - `IB failed breakout`
  - `IB retest/reject`
  - `day type`

## 当前怎么用（v1）

- 关系输入：
  - `n02_ib_object_p0_sample_v1.csv`
  - `n02_p0_fields_runtime_v2.csv`
- 关系生成脚本：
  - `n02_ib_or_relation_p0_build_v1.py`
- 关系输出：
  - `n02_ib_or_relation_p0_sample_v1.csv`
  - `n02_ib_or_relation_p0_summary_v1.json`
- 关系字段当前只覆盖：
  - `or_inside_ib`
  - `ib_equals_or`
  - `ib_width_minus_or_width`
  - `ib_width_to_or_width_ratio`
  - `or_high_to_ib_high_gap`
  - `or_low_to_ib_low_gap`
  - `first_break_direction`
  - `first_break_mode`
  - `width_error_day`

## 推荐复现命令

- `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_relation_p0_build_v1.py`

## 2026-07-03 fresh-run 结果

- 运行入口：
  - `python n02_ib_or_relation_p0_build_v1.py`
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
  - `london relation_rows=69`
  - `new_york relation_rows=69`
- 当前结论：
  - `IB vs OR` 的最小关系层已完成 fresh-run 闭环。
  - 当前已定义样本下，`OR inside IB` 为全量成立，不需要再靠口头假设。
  - 这一步仍只是关系层证据，不是行为门控。

## 2026-07-03 first_break relative child fresh-run

- 运行入口：
  - `python n02_ib_or_first_break_relative_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_first_break_relative_p0_sample_v1.csv`
  - `n02_ib_or_first_break_relative_p0_summary_v1.json`
- 关键统计：
  - `shared_edge_break_rows=14`
  - `gap_remaining_rows=124`
  - `can_confirm_ib_break_rows=14`
  - `requires_break_price_rows=124`
- 当前结论：
  - `first_break relative to IB/OR` 已完成一层保守落盘
  - 当前不能把 gap remaining 行误读成“已确认 IB 首破”
  - 这层已继续向下游支撑 `break_bar evidence` fresh-run，并将 `requires_break_price` 缺口转成真实当根证据

## 当前最顺动作

- 若继续推进，优先做：
  - 补 `first_break bar price` 或等价字段
  - 缩减 `requires_break_price_rows`
  - 扩大样本覆盖
- 继续保持不做：
  - `acceptance`
  - `failed breakout`
  - `retest / reject`
  - `day type`
