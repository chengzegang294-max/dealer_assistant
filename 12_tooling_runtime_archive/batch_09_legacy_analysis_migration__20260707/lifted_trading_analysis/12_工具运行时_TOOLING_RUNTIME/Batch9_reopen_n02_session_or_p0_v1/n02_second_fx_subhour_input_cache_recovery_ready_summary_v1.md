# n02_second_fx_subhour_input_cache_recovery_ready_summary v1

## Role

- Scan the preferred `GBPUSD/M15` recovery path beyond known `data + MT4 history` sources.
- Keep this layer acquisition-only: confirm cache and runtime evidence, but do not claim a canonical export exists yet.

## 2026-07-05 fresh-run

- repo_drop_gbpusd_m15_csv_count: `0`
- mt5_cache_gbpusd_hcc_count: `6`
- mt5_cache_has_ticks_dat: `true`
- common_files_gbpusd_probe_csv_count: `4`
- repo_validation_log_matched_line_count: `10`
- recovery_status: `cache_recovery_ready_without_canonical_export`
- preferred_next_step: `terminal_export_to_drop_then_ingest_with_n02_mt5_export_ingest_v1`
- fallback_next_step: `build_or_reuse_hcc_reader_then_convert_to_canonical_bars`

## Current Decision

- No `GBPUSD/M15` canonical export csv was found under the known `data` drop paths.
- The preferred `TradeMaxGlobal-Demo__60088394` MT5 runtime already contains recoverable source evidence: yearly `GBPUSD/*.hcc`, `ticks.dat`, repo-copied tester log matches, and `Common\Files` GBPUSD probe csv files.
- Therefore the mainline is no longer blocked at generic acquisition. It advances to `GBPUSD/M15 cache recovery ready`, with the next exact action fixed to `terminal export -> n02_mt5_export_ingest_v1`, and `hcc reader` kept only as fallback.
