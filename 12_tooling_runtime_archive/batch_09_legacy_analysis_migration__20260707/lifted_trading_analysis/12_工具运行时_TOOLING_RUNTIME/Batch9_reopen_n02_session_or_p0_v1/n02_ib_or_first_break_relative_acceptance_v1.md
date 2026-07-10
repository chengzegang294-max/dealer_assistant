# N02 IB OR 首次突破相对位置验收 v1

## 目的

- 记录 `REOPEN_B9_N02_IB_OR_FIRST_BREAK_RELATIVE_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `n02_ib_or_relation_p0_sample_v1.csv`
- 生成脚本：
  - `n02_ib_or_first_break_relative_p0_build_v1.py`
- 输出：
  - `n02_ib_or_first_break_relative_p0_sample_v1.csv`
  - `n02_ib_or_first_break_relative_p0_summary_v1.json`

## 2026-07-03 fresh-run 验收

- 验收方式：
  - `python n02_ib_or_first_break_relative_p0_build_v1.py`
- 本轮结果：
  - `input_rows=138`
  - `output_rows_written=138`
  - `shared_edge_break_rows=14`
  - `gap_remaining_rows=124`
  - `can_confirm_ib_break_rows=14`
  - `requires_break_price_rows=124`
  - `requires_break_price_ratio=0.8985507246376812`
  - `london shared_edge_break_rows=2`
  - `new_york shared_edge_break_rows=12`
- 当前结论：
  - 当前字段足以对 `14/138` 行给出强确认。
  - 对 `124/138` 行，系统已显式拒绝假确认，要求额外 `break price`。

## 关键统计

- `shared_edge_break=14`
- `gap_remaining=124`
- `can_confirm_ib_break=14`
- `requires_break_price=124`
- `requires_break_price_ratio=0.8985507246376812`
- `london_shared_edge_break=2`
- `newyork_shared_edge_break=12`

## 当前不通过项

- 当前仍没有 `first_break` 发生当根的实际价位证据。
- 因此当前仍不能把大多数 `OR 首破` 自动升级为 `IB 首破`。
- 当前仍只覆盖 `EURUSD M1` 的 `london/new_york` 已定义样本。
