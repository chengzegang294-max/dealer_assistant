# N02 P0 运行追加验收 v2

- ARCHIVE_ONLY_RUNTIME_MIRROR: 本文件记录旧 `REOPEN_B9_N02_SESSION_OR_P0` v2 append 的历史验收结果，不作为当前默认验收入口。
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 目的

- 记录 `REOPEN_B9_N02_SESSION_OR_P0` v2 的 runtime append 验收结论。
- v2 的目标是补齐 v1 无法落盘的字段级差异：`first_break_mode`。

## 本次验收对象

- proof 输入：
  - `real_input_samples\n02_proof_of_mapping_output_v2.csv`
- append 脚本：
  - `n02_p0_runtime_append_from_proof_v2.py`
- runtime csv：
  - `n02_p0_fields_runtime_v2.csv`

## 验收结果

- v2 append 已在旧链路中成功落地。
- `first_break_mode` 已进入当时的 v2 runtime csv。

## 2026-07-03 single_verify dry-run 复验

- 输入：
  - `real_input_samples\n02_real_input_eurusd_m1_20260610_utc_v1.csv`
  - `real_input_samples\n02_proof_of_mapping_output__single_verify_20260610_utc_v1.csv`
- 验收方式：
  - `python n02_p0_runtime_append_from_proof_v2.py --proof real_input_samples\n02_proof_of_mapping_output__single_verify_20260610_utc_v1.csv --dest n02_p0_fields_runtime_v2.csv`
- 本轮结果：
  - `mode=dry_run`
  - `runtime_rows_before=165`
  - `proof_rows=4`
  - `runtime_rows_after_append=165`
  - `or_defined_rows=136`
  - `or_defined_ratio=0.8242424242424242`
  - `london_ratio=68/81`
  - `new_york_ratio=68/84`
  - `first_break_direction_counts={"down": 56, "none": 29, "up": 80}`
  - `first_break_mode_counts={"close": 75, "none": 29, "wick": 61}`
- 历史结论：
  - 本轮 single-verify 输入不会扩大 v2 runtime 行数，说明该 proof 已被当前 runtime 覆盖。
  - 该结果只用于确认工具链与单日样本可复验。

## 2026-07-03 latest persist 复验

- 时区判定：
  - `eurusd_m1_export.csv` 按 `UTC` 解释与 `2026-06-10/11` 的 london/new_york OR 30 分钟窗口高低完全对齐。
- 验收方式：
  - `python real_input_samples\n02_mt5_export_ingest_v1.py --latest --symbol EURUSD --timeframe M1 --source-timezone UTC --dest real_input_samples\n02_first_real_input_bars_v1.csv`
  - `python real_input_samples\n02_proof_of_mapping_v2.py`
  - `python n02_p0_runtime_append_from_proof_v2.py --persist`
- 本轮结果：
  - `mode=persist`
  - `ingest_rows=99500`
  - `proof_rows=165`
  - `runtime_rows_before=165`
  - `runtime_rows_after_append=165`
  - `or_defined_rows=138`
  - `or_undefined_rows=27`
  - `or_defined_ratio=0.8363636363636363`
  - `london_ratio=69/81`
  - `new_york_ratio=69/84`
  - `first_break_direction_counts={"down": 56, "none": 27, "up": 82}`
  - `first_break_mode_counts={"close": 76, "none": 27, "wick": 62}`
- 历史结论：
  - `latest + persist` 已成功落地。
  - 本轮 proof 不再扩大 runtime 行数，说明 `n02_p0_fields_runtime_v2.csv` 已与当前 `latest` 导出保持同一覆盖面。
  - 这份 runtime v2 已继续向下游支撑 `n02_ib_or_relation_p0_build_v1.py` 的关系层 fresh-run。

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
- `first_break_mode_close = 11`
- `first_break_mode_wick = 7`
- `first_break_mode_none = 4`
- `first_break_mode_ambiguous = 0`

## 当前不通过项

- `session_timezone` 的 DST / overlap 仍待扩大核验样本（已补 3 段 DST 抽查窗口 + 2 段 overlap 抽查证据）。
- 已补“交易日本地日期归属”抽查证据（跨日本地 23:xx->00:00 的 UTC 窗口），但仍待扩大抽查与覆盖更多时段。
- 已补“真实 bars 分桶 + OR window 命中数”抽查证据（跨日切换 + OR window 命中：M1=30 根、秋季回切 M5=6 根）。
- 已补 OR 边界语义抽查证据（`in_or` 采用 `[start,end)`，`post_or` 采用 `>=end`）。
- v2 runtime 中 `bar_time` 已与 `or_end_utc` 对齐（样本抽查：`london=07:30Z`，`new_york=14:00Z`）。
- 已补 DST 切换周的 `or_start_utc/or_end_utc` 跳变一致性证据（london/new_york 的春秋切换均覆盖）。
- 已补 DST 切换周的“真实 bars OR anchor 对齐”证据（春季：M1；秋季：M5，london/new_york 均覆盖）。
- v2 仍只覆盖 `EURUSD M1` 的 `london/new_york` 首批样本。
