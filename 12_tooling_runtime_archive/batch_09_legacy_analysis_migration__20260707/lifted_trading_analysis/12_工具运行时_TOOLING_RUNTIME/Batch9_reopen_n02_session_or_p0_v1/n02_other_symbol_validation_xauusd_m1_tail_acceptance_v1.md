# n02_other_symbol_validation_xauusd_m1_tail_acceptance v1

## 目的

- 记录 `REOPEN_B9_N02_OTHER_SYMBOL_VALIDATION_XAUUSD_M1_TAIL_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `.\data\mt_exports_drop\xauusd_m1_tail_20000.csv`
- 生成脚本：
  - `real_input_samples\n02_mt5_export_ingest_v1.py`
  - `real_input_samples\n02_proof_of_mapping_v2.py`
  - `real_input_samples\n02_ib_proof_of_mapping_v1.py`
  - `n02_other_symbol_validation_xauusd_m1_tail_build_v1.py`
- 输出：
  - `real_input_samples\n02_real_input_xauusd_m1_tail_v1.csv`
  - `real_input_samples\n02_proof_of_mapping_output_xauusd_m1_tail_v1.csv`
  - `real_input_samples\n02_ib_proof_of_mapping_output_xauusd_m1_tail_v1.csv`
  - `n02_other_symbol_validation_xauusd_m1_tail_summary_v1.md`
  - `n02_other_symbol_validation_xauusd_m1_tail_summary_v1.json`

## 2026-07-05 fresh-run 验收

- 本轮结果：
  - `bars_rows=20000`
  - `or_rows=37`
  - `or_defined_rows=30`
  - `ib_rows=30`
  - `ib_defined_rows=30`
- 当前结论：
  - `XAUUSD/M1 tail` 已能独立跑通最小 OR/IB validation。
  - 当前验证层只说明 `other symbol` 可跑性，不写回主 `EURUSD/M1` runtime。
  - 当前仍不升级成 `failed breakout / retest / reject / day type`。

## 关键统计

- `or_defined_ratio=30/37`
- `ib_defined_ratio=30/30`
- `or_first_break_direction_counts={"down": 17, "none": 7, "up": 13}`
- `or_first_break_mode_counts={"close": 19, "none": 7, "wick": 11}`

## 当前不通过项

- 当前还没有第二个外汇 symbol 的同口径输入样本。
