# n02_second_fx_subhour_input_gate_runtime_notes v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `second FX sub-hour input gate` 的 inventory 扫描口径与边界。

## 当前边界

- 不写回：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - 主 `EURUSD/M1` 行为链下的 sample/card/summary
- 当前只落：
  - `n02_second_fx_subhour_input_gate_summary_v1.md`
  - `n02_second_fx_subhour_input_gate_summary_v1.json`
- 当前不推进：
  - `failed breakout`
  - `retest`
  - `reject`
  - `day type`
- 当前也不伪造：
  - 第二个 FX sub-hour bars
  - 第二个 FX sub-hour OR/IB proof

## 当前怎么用（v1）

- 输入根目录：
  - `TRADING_ANALYSIS_DATA_ROOT`（默认：`.\data`）
- 生成脚本：
  - `n02_second_fx_subhour_input_gate_build_v1.py`
- 输出：
  - `n02_second_fx_subhour_input_gate_summary_v1.md`
  - `n02_second_fx_subhour_input_gate_summary_v1.json`

## 推荐复现命令

- `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_gate_build_v1.py`

## 2026-07-05 fresh-run 结果

- inventory：
  - 已在 `TRADING_ANALYSIS_DATA_ROOT` 根内按 `^[A-Za-z]{6}_(m1|m5|m15|m30)\.csv$` 合同递归扫描。
  - 当前共识别 `11` 份 `FX + sub-hour` 文件。
  - 当前识别到的 `FX sub-hour` symbol 只有：`EURUSD`
  - 当前识别到的 timeframe 为：`M1 / M5 / M15`
- gate：
  - `second_fx_subhour_symbol_count=0`
  - `gate_status=blocked_by_missing_second_fx_subhour_input`
  - `blocked_reason=data_root_has_fx_subhour_files_but_only_eurusd_is_present`

## 当前结论

- 当前不是“完全没有 sub-hour 文件”，而是“只有 `EURUSD`，还没有第二个 FX symbol`。
- 因此主线下一步应收紧为：
  - `second FX sub-hour input acquisition`

## provenance 说明

- 当前 gate 只依赖旧仓 `data` 根目录的真实文件盘点，不生成伪 bars。
- 本目录下同名 summary 承担新仓镜像回填与主线索引职责。
