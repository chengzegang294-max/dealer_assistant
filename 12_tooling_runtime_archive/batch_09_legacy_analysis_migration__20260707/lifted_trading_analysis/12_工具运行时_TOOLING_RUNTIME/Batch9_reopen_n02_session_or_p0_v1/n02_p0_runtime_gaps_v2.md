# n02_p0_runtime_gaps v2

## 目的

- 记录 `REOPEN_B9_N02_SESSION_OR_P0` 在 v2 版本的剩余审计缺口。

## v2 已补齐

- 已新增并落盘 `first_break_mode`，用于区分：
  - `close / wick / none / ambiguous`

## v2 仍未完成

- `session_timezone` 的 DST / overlap 仍需扩大核验样本（已补 3 段 DST 抽查窗口 + 2 段 overlap 抽查证据）。
- DST 切换周的 `or_start_utc/or_end_utc` 跳变一致性已补证据，但仍待扩大抽查窗口与覆盖更多年份。
- DST 切换周的“真实 bars OR anchor 对齐”已补春季样本（M1）与秋季样本（M5，london/new_york 均覆盖）。
- `by_local_date` 的本地日期归属已补最小抽查证据（跨本地 23:xx->00:00 的 UTC 窗口），但仍待扩大抽查与覆盖更多时段。
- `by_local_date` 的真实 bars 分桶已补最小抽查证据（london/new_york 跨日切换），且 OR window 命中数已符合 `M1 + 30min => 30 bars` 与 `M5 + 30min => 6 bars`（秋季回切窗口）。
- OR 边界语义已补最小抽查证据（`in_or` 为 `[start,end)`，`post_or` 为 `>=end`）。
- `width_error_day` 阈值仍需真实运行后核对。
- 当前仍只覆盖 `EURUSD M1` 的 `london/new_york` 样本。

## 当前明确不含

- `IB`
- `ib_*`
- `or_break_high / or_break_low`
- `target_trigger_source`
