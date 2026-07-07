# n02_p0_runtime_append_acceptance v1

## 目的

- 记录 `REOPEN_B9_N02_SESSION_OR_P0` 首批 runtime append 证据的验收结论。
- 把“OR proof 已存在”推进到“runtime csv 已有真实 session/OR 行且边界已写清”。

## 本次验收对象

- proof 输入：
  - `real_input_samples\n02_proof_of_mapping_output_v1.csv`
- append 脚本：
  - `n02_p0_runtime_append_from_proof_v1.py`
- runtime csv：
  - `n02_p0_fields_runtime_v1.csv`

## 验收结果

- append 已成功落地。
- 示例行已被真实 proof 行替换。
- 当前 runtime csv 为：
  - `EURUSD`
  - `M1`
  - `london + new_york` session OR 首批样本
- 本轮已从“首批 append 验收”推进到：
  - `first_break_direction` 首批真实 break 样本验收

## 关键统计

- `runtime_rows = 22`
- `or_defined = 18`
- `or_undefined = 4`
- `width_error_day_1 = 4`
- `london_rows = 11`
- `new_york_rows = 11`
- `first_break_up = 13`
- `first_break_down = 5`
- `first_break_none = 4`
- `first_break_close_up = 8`
- `first_break_close_down = 3`
- `first_break_wick_up = 5`
- `first_break_wick_down = 2`
- `first_break_ambiguous_skipped = 0`
- `first_non_none_break_bar_time = 2026-06-01T07:30:00Z`
- `first_bar_time = 2026-05-31T14:00:00Z`
- `last_bar_time = 2026-06-12T07:30:00Z`

## 当前可接受结论

- `session_id / session_timezone` 已具备首批真实 runtime append 证据。
- `opening_range_high / low / mid / width` 已具备首批真实 runtime append 证据。
- `opening_range_defined` 与 `width_error_day` 已形成真实世界边界样本。
- `first_break_direction` 已具备首批真实 break 样本。
- 这一步足以支撑：
  - “N02 已有真实 append 证据”
  - “N02 已完成首批真实 break 样本验收”
  - 但不足以支撑“ORB/IB 逻辑已完成”

## 当前不通过项

- `first_break_direction` 已实现 `close-first + wick-fallback` 的细分口径，但仍未将 `close` vs `wick` 作为独立字段落盘（当前仅输出统计证据，不改 v1 表头）。
- `IB` 相关字段仍不在当前 P0 范围。
- `session_timezone` 的 DST / overlap 核验尚未完成（已补首批 DST 抽查证据）。

## 本次验收结论

- 通过：
  - `runtime append skeleton -> first real append evidence`
  - `first_break_direction first real break acceptance`
- 未通过：
  - `full N02 runtime validation`
  - `ORB / IB completion`
