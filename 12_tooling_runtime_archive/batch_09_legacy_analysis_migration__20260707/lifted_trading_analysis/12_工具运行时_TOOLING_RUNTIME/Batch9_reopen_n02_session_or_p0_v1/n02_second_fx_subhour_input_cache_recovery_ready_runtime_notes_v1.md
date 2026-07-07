# n02_second_fx_subhour_input_cache_recovery_ready_runtime_notes v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是把 `GBPUSD/M15 export or external recovery` 继续收紧成可执行的 `cache recovery ready` 停点。

## 当前边界

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - 任意 `failed breakout / retest reject / day type` 定义
- 当前只落：
  - `n02_second_fx_subhour_input_cache_recovery_ready_summary_v1.md`
  - `n02_second_fx_subhour_input_cache_recovery_ready_summary_v1.json`
- 当前不伪装：
  - `GBPUSD/M15` canonical bars 已经导出
  - `GBPUSD/M15` 已经完成 ingest 或 OR/IB proof

## 当前怎么跑（v1）

- 输入根：
  - `TRADING_ANALYSIS_DATA_ROOT`（默认：`.\data`）
  - `C:\Users\91883\AppData\Roaming\MetaQuotes\Terminal\C9F9BDDC460DF35F331B73B79A3DD57C\bases\TradeMaxGlobal-Demo`
  - `C:\Users\91883\AppData\Roaming\MetaQuotes\Terminal\Common\Files`
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\gbpusd_h1_tmgm_longwin_20260702T0250\log\20260702.log`
- 生成脚本：
  - `n02_second_fx_subhour_input_cache_recovery_ready_build_v1.py`
- 输出：
  - `n02_second_fx_subhour_input_cache_recovery_ready_summary_v1.md`
  - `n02_second_fx_subhour_input_cache_recovery_ready_summary_v1.json`

## 推荐复现命令

- `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_cache_recovery_ready_build_v1.py`

## 2026-07-05 fresh-run 结果

- `data` 层：
  - `gbpusd_m15_csv_count=0`
  - `gbpusd_any_csv_count=1`
  - 当前只见旧 `GBPUSD/H1` 直购 csv，不见 `GBPUSD/M15` export
- `MT5 cache` 层：
  - `gbpusd_hcc_count=6`
  - `has_gbpusd_ticks_dat=true`
  - `history\GBPUSD\2021.hcc~2026.hcc` 已存在
- `Common\Files` 层：
  - `gbpusd_probe_csv_count=4`
  - 已见 `GBPUSD/H1/H4` probe csv
- `repo log` 层：
  - `matched_line_count=10`
  - 已明确匹配 `preliminary downloading of M1 history started/completed`
  - 已明确匹配 `history data begins from 2021.07.23 00:00`
- recovery gate：
  - `recovery_status=cache_recovery_ready_without_canonical_export`
  - `preferred_next_step=terminal_export_to_drop_then_ingest_with_n02_mt5_export_ingest_v1`
  - `fallback_next_step=build_or_reuse_hcc_reader_then_convert_to_canonical_bars`

## 当前结论

- 主线已不再是泛化的 `external recovery` 抽象描述，而是已经锁定到：
  - 环境：`TradeMaxGlobal-Demo__60088394`
  - 真实缓存：`GBPUSD/*.hcc + ticks.dat`
  - 真实日志：`GBPUSD M1 history completed`
  - 下一跳：`terminal export -> n02_mt5_export_ingest_v1`
- 只有在 `terminal export` 仍不可拿到 `GBPUSD/M15` csv 时，才回退到 `hcc reader` 路径。

## provenance 说明

- 当前 recovery-ready 层只做真实缓存、日志和落盘缺口盘点，不宣称 canonical bars 已生成。
- 本目录下同名 summary 承担新仓镜像回填与主线索引职责。
