# N02 第二 FX 次小时输入闸口验收 v1

## 目的

- 记录 `REOPEN_B9_N02_SECOND_FX_SUBHOUR_INPUT_GATE_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `TRADING_ANALYSIS_DATA_ROOT`（默认：`.\data`）
- 生成脚本：
  - `n02_second_fx_subhour_input_gate_build_v1.py`
- 输出：
  - `n02_second_fx_subhour_input_gate_summary_v1.md`
  - `n02_second_fx_subhour_input_gate_summary_v1.json`

## 2026-07-05 fresh-run 验收

- 本轮结果：
  - `fx_subhour_file_count=11`
  - `fx_subhour_symbol_count=1`
  - `fx_subhour_symbols=["EURUSD"]`
  - `fx_subhour_timeframes=["M1","M5","M15"]`
  - `second_fx_subhour_symbol_count=0`
  - `gate_status=blocked_by_missing_second_fx_subhour_input`
- 当前结论：
  - 当前 `data` 根目录确实存在 `FX + sub-hour` 实际文件。
  - 但现有命名合同下只有 `EURUSD`，没有第二个 FX symbol 的 sub-hour 输入。
  - 因此当前这层只能收口为 `input gate`，不能伪装成 `second FX sub-hour validation` 成功。

## 当前不通过项

- 当前缺口固定为：
  - `second FX sub-hour input sample`
