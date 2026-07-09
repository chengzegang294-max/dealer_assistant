# N02 第二 FX 次小时输入采集验收 v1

## 目的

- 记录 `REOPEN_B9_N02_SECOND_FX_SUBHOUR_INPUT_ACQUISITION_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `TRADING_ANALYSIS_DATA_ROOT`（默认：`.\data`）
  - `12_tooling_runtime_archive\batch_05_legacy_mt4_probe_assets__20260706\03_MT4便携探针实例\history\ICMarketsSC-Demo03`
  - `12_tooling_runtime_archive\batch_05_legacy_mt4_probe_assets__20260706\mt4_probe_instance\history\ICMarketsSC-Demo03`
- 生成脚本：
  - `n02_second_fx_subhour_input_acquisition_build_v1.py`
- 输出：
  - `n02_second_fx_subhour_input_acquisition_summary_v1.md`
  - `n02_second_fx_subhour_input_acquisition_summary_v1.json`

## 2026-07-05 fresh-run 验收

- 本轮结果：
  - `data_subhour_file_count=11`
  - `mt4_subhour_file_count=8`
  - `combined_second_fx_subhour_symbol_count=0`
  - `known_higher_tf_fx_symbols_without_subhour=["GBPUSD","USDCHF","USDJPY"]`
  - `recommended_target=GBPUSD/M15`
  - `acquisition_status=blocked_by_missing_second_fx_subhour_across_known_sources`
- 当前结论：
  - 当前已知 `data + MT4 history` 源整体不存在第二个 FX symbol 的 `sub-hour` 输入。
  - `GBPUSD / USDCHF / USDJPY` 当前只见到更高周期影子，不足以直接落 `sub-hour validation`。
  - 因此当前这层只能收口为 `acquisition`，下一步固定为：
    - `GBPUSD/M15 cache recovery ready`
    - `TradeMaxGlobal-Demo__60088394: terminal export -> n02_mt5_export_ingest_v1`

## 当前不通过项

- 当前缺口固定为：
  - `GBPUSD/M15 sub-hour input sample`
