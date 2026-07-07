# n02_p0_runtime_gaps v1

## 目的

- 记录 `REOPEN_B9_N02_SESSION_OR_P0` 当前运行时层面还没做的内容。
- 防止把“目录已建好、表头已冻结”误读为“运行逻辑已完成”。

## 当前未完成

- 还没有真实运行脚本接入。
- 还没有真实运行参数记录。
- 还没有跨市场 `session_id / session_timezone` 样本。
- 当前 runtime csv 虽已存在真实数据行，但仍只是首批 `EURUSD M1` 的 `london/new_york` 样本。

## 当前明确不含

- `IB`
- `ib_high / ib_low / ib_range`
- `ib_break_direction`
- `ib_accept_2period`
- `ib_regime_narrow_or_wide`
- `ib_failed_breakout_event`
- `or_break_high`
- `or_break_low`
- `target_trigger_source`

## 审计缺口

- `width_error_day` 阈值还需真实运行后核对。
- `first_break_direction` 已实现 `close-first + wick-fallback` 的细分口径，但仍未将 `close` vs `wick` 作为独立字段落盘（当前仅输出统计证据，不改 v1 表头）。
- `session_timezone` 的 DST / overlap 仍待补更多核验样本（已补首批 DST 抽查证据）。
- 当前 `first_break_direction` 已覆盖真正 break 样本，并已收紧为“唯一突破才记方向；双穿歧义 bar 记 none”的最小审计安全口径。
- 当前 `session_id` 只覆盖：
  - `london`
  - `new_york`

## 当前可宣称

- 已进入工具运行时阶段。
- 已固定运行时目录。
- 已冻结第一版表头。
- 已不再只是空壳。
- 已把第一批真实 `EURUSD M1` OR proof 行 append 进 `n02_p0_fields_runtime_v1.csv`。
- 已具备参数模板、追加脚本 stub、append_from_proof 脚本。
- 当前 runtime 行数：
  - `22`
- 当前已验证：
  - `or_defined = 18`
  - `or_undefined = 4`
  - `width_error_day_1 = 4`
  - `first_break_up = 13`
  - `first_break_down = 5`
  - `first_break_none = 4`
  - `first_break_close_up = 8`
  - `first_break_close_down = 3`
  - `first_break_wick_up = 5`
  - `first_break_wick_down = 2`
  - `london_rows = 11`
  - `new_york_rows = 11`

## 当前不可宣称

- `N02 P0 runtime implemented`
- `IB implemented`
- `ORB strategy implemented`
- `runtime validation fully passed`
- `DST / overlap verification complete`

## 下一步

- 真正接代码时，先补：
  - 真实参数来源
  - `first_break_direction` 的 `close` vs `wick` 细分口径
  - DST / overlap 的核验样本
  - 第三 session 或第二品种样本
  - 运行日志或运行说明更新
