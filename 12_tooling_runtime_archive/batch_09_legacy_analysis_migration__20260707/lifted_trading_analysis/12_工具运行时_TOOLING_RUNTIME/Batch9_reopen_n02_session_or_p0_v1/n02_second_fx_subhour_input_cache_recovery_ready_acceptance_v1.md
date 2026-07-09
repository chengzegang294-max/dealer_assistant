# N02 第二 FX 次小时输入缓存恢复就绪验收 v1

## 目的

- 记录 `REOPEN_B9_N02_SECOND_FX_SUBHOUR_INPUT_CACHE_RECOVERY_READY_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `TRADING_ANALYSIS_DATA_ROOT`（默认：`.\data`）
  - `C:\Users\91883\AppData\Roaming\MetaQuotes\Terminal\C9F9BDDC460DF35F331B73B79A3DD57C\bases\TradeMaxGlobal-Demo`
  - `C:\Users\91883\AppData\Roaming\MetaQuotes\Terminal\Common\Files`
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\gbpusd_h1_tmgm_longwin_20260702T0250\log\20260702.log`
- 生成脚本：
  - `n02_second_fx_subhour_input_cache_recovery_ready_build_v1.py`
- 输出：
  - `n02_second_fx_subhour_input_cache_recovery_ready_summary_v1.md`
  - `n02_second_fx_subhour_input_cache_recovery_ready_summary_v1.json`

## 2026-07-05 fresh-run 验收

- 本轮结果：
  - `repo_drop_gbpusd_m15_csv_count=0`
  - `mt5_cache_gbpusd_hcc_count=6`
  - `has_mt5_ticks_dat=true`
  - `common_files_gbpusd_probe_csv_count=4`
  - `repo_validation_log_matched_line_count=10`
  - `recovery_status=cache_recovery_ready_without_canonical_export`
- 当前结论：
  - 已确认已知 `drop` 路径下没有 `GBPUSD/M15` export csv。
  - 已确认 `TradeMaxGlobal-Demo__60088394` 下存在真实 `GBPUSD` 年度 `.hcc` 缓存与 `ticks.dat`。
  - 已确认仓内实跑归档日志明确记录 `GBPUSD` 的 `M1 history` 下载完成与起始时间。
  - 因此主线可以从 `GBPUSD/M15 export or external recovery` 推进到更精确的：
    - `GBPUSD/M15 cache recovery ready`
  - 当前下一步固定为：
    - `terminal export -> n02_mt5_export_ingest_v1`
  - 当前 fallback 固定为：
    - `build_or_reuse_hcc_reader_then_convert_to_canonical_bars`

## 当前不通过项

- 当前缺口固定为：
  - `GBPUSD/M15 canonical export csv`
  - `GBPUSD/M15 ingest output`
  - `GBPUSD/M15 proof output`
