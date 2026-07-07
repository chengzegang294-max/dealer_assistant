# REOPEN_B9_N02_SECOND_FX_SUBHOUR_INPUT_CACHE_RECOVERY_READY_P0 关系入口 v1

## 作用

- 对 `GBPUSD/M15` 的 `cache recovery ready` 做关系入口级收口。
- 当前只确认 `TradeMaxGlobal-Demo__60088394` 是否已经具备继续回收到 canonical bars 的真实缓存和日志条件。

## 当前边界（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - 任意 `failed breakout` 相关定义
- 当前只新增：
  - `GBPUSD/M15 cache recovery ready` 的 inventory/recovery summary
- 当前不把：
  - `XBreaking GBPUSD probe csv`
  - `MT5 cache *.hcc`
  直接冒充成 `GBPUSD/M15 canonical export`

## 当前真值组成（v1）

- `entry_md`：`REOPEN_B9_N02_SECOND_FX_SUBHOUR_INPUT_CACHE_RECOVERY_READY_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_cache_recovery_ready_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_cache_recovery_ready_acceptance_v1.md`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_cache_recovery_ready_build_v1.py`
- `summary_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_cache_recovery_ready_summary_v1.md`
- `summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_cache_recovery_ready_summary_v1.json`

## 最小验收（关系开题级）

- recovery summary 必须显式记录：
  - `repo_drop_gbpusd_m15_csv_count`
  - `mt5_cache_gbpusd_hcc_count`
  - `has_mt5_ticks_dat`
  - `common_files_gbpusd_probe_csv_count`
  - `repo_validation_log_matched_line_count`
  - `recovery_status`
  - `preferred_next_step`
  - `fallback_next_step`
- 所有输出都必须显式保留：
  - `writes_main_m1_runtime=false`
  - `is_acquisition_only=true`
  - `declares_canonical_export_done=false`

## 2026-07-05 fresh-run

- 运行入口：
  - `python n02_second_fx_subhour_input_cache_recovery_ready_build_v1.py`
- 关键统计：
  - `repo_drop_gbpusd_m15_csv_count=0`
  - `mt5_cache_gbpusd_hcc_count=6`
  - `has_mt5_ticks_dat=true`
  - `common_files_gbpusd_probe_csv_count=4`
  - `repo_validation_log_matched_line_count=10`
  - `recovery_status=cache_recovery_ready_without_canonical_export`
- 当前裁决：
  - `GBPUSD/M15` 还没有落到可 ingest 的 export csv。
  - 但 `TradeMaxGlobal-Demo__60088394` 已有继续回收所需的真实缓存与日志证据。
  - 因此下一步不再写成泛化的 `external recovery`，而是固定为：
    - `terminal export -> n02_mt5_export_ingest_v1`
  - `hcc reader` 仅保留为 fallback。

## provenance 说明

- 当前关系入口基于旧仓 `data`、本机 `MetaQuotes\Terminal` 缓存和仓内实跑归档日志共同收口。
- 本目录及同名产物承担新仓镜像回填与主线索引职责。
