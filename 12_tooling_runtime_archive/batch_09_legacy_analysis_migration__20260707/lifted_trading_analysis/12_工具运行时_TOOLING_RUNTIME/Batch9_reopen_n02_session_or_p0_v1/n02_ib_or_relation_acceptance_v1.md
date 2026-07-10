# N02 IB 与 OR 关系层验收 v1

## 目的

- 记录 `REOPEN_B9_N02_IB_OR_RELATION_P0` 的最小关系层验收结论。

## 本次验收对象

- `IB object sample`：
  - `n02_ib_object_p0_sample_v1.csv`
- `OR runtime v2`：
  - `n02_p0_fields_runtime_v2.csv`
- 关系生成脚本：
  - `n02_ib_or_relation_p0_build_v1.py`
- 关系产物：
  - `n02_ib_or_relation_p0_sample_v1.csv`
  - `n02_ib_or_relation_p0_summary_v1.json`

## 2026-07-03 fresh-run 验收

- 验收方式：
  - `python n02_ib_or_relation_p0_build_v1.py`
- 本轮结果：
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
  - `IB_OBJECT_P0` 与 `OR runtime v2` 已实现稳定 join。
  - 本轮没有丢失匹配行，`missing_or_match_rows=0`。
  - 在当前全部已定义样本中，`OR` 均位于 `IB` 内部。
  - 该层已继续向下游支撑 `first_break relative to IB/OR` 的保守版 fresh-run。

## 关键统计

- `relation_rows=138`
- `or_inside_ib=138`
- `or_inside_ib_ratio=1.0`
- `ib_equals_or=14`
- `width_error_day_1=0`
- `first_break_up=82`
- `first_break_down=56`
- `first_break_close=76`
- `first_break_wick=62`
- `london_rows=69`
- `new_york_rows=69`

## 当前不通过项

- 当前仍只覆盖 `EURUSD M1` 的 `london/new_york` 已定义样本。
- 当前尚未进入：
  - `first_break relative to IB/OR`
  - `IB acceptance`
  - `IB failed breakout`
  - `IB retest/reject`
  - `day type`
