# N02 第二 FX 次小时输入采集运行说明 v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `second FX sub-hour input acquisition` 的已知源盘点口径与边界。

## 当前边界

- 不写回：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - 主 `EURUSD/M1` 行为链下的 sample/card/summary
- 当前只落：
  - `n02_second_fx_subhour_input_acquisition_summary_v1.md`
  - `n02_second_fx_subhour_input_acquisition_summary_v1.json`
- 当前不伪造：
  - 第二个 FX 的 `sub-hour` bars
  - 第二个 FX 的 `sub-hour` OR/IB proof

## 当前怎么用（v1）

- 输入根目录：
  - `TRADING_ANALYSIS_DATA_ROOT`（默认：`.\data`）
  - `12_tooling_runtime_archive\batch_05_legacy_mt4_probe_assets__20260706\03_MT4便携探针实例\history\ICMarketsSC-Demo03`
  - `12_tooling_runtime_archive\batch_05_legacy_mt4_probe_assets__20260706\mt4_probe_instance\history\ICMarketsSC-Demo03`
- 生成脚本：
  - `n02_second_fx_subhour_input_acquisition_build_v1.py`
- 输出：
  - `n02_second_fx_subhour_input_acquisition_summary_v1.md`
  - `n02_second_fx_subhour_input_acquisition_summary_v1.json`

## 推荐复现命令

- `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_acquisition_build_v1.py`

## 2026-07-05 fresh-run 结果

- `data` 层：
  - `subhour_file_count=11`
  - `subhour_symbols=["EURUSD"]`
  - `subhour_timeframes=["M1","M5","M15"]`
- `MT4 history` 层：
  - `subhour_file_count=8`
  - `subhour_symbols=["EURUSD"]`
  - `higher_tf_symbols=["EURUSD","GBPUSD","USDCHF","USDJPY"]`
- acquisition gate：
  - `combined_second_fx_subhour_symbol_count=0`
  - `known_higher_tf_fx_symbols_without_subhour=["GBPUSD","USDCHF","USDJPY"]`
  - `recommended_target=GBPUSD/M15`
  - `acquisition_status=blocked_by_missing_second_fx_subhour_across_known_sources`

## 当前结论

- 当前缺口已不只是 `data` 根目录命名问题，而是已知 `data + MT4 history` 源整体都没有第二个 FX 的 `sub-hour` 原始源。
- 当前最顺补样本对象固定为：
  - `GBPUSD/M15`
- 当前下一跳已从泛化 `external recovery` 收紧为：
  - `GBPUSD/M15 cache recovery ready`
  - `TradeMaxGlobal-Demo__60088394: terminal export -> n02_mt5_export_ingest_v1`

## provenance 说明

- 当前 acquisition 层只做真实源盘点，不生成伪 bars。
- 本目录下同名 summary 承担新仓镜像回填与主线索引职责。
