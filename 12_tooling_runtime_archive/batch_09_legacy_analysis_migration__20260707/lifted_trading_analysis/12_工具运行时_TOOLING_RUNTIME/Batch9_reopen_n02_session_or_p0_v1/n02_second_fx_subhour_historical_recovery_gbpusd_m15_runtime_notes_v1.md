# n02_second_fx_subhour_historical_recovery_gbpusd_m15_runtime_notes v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是把 `GBPUSD/M15` 从 `terminal export insufficient` 停点继续推进到 `historical_recovered canonical + OR/IB proof`。

## 当前边界

- 当前不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - 任意 `failed breakout` 相关定义
- 当前只落：
  - `real_input_samples\n02_real_input_gbpusd_m15_v1.csv`
  - `real_input_samples\n02_real_input_gbpusd_m15_report_v1.json`
  - `real_input_samples\n02_proof_of_mapping_output_gbpusd_m15_v1.csv`
  - `real_input_samples\n02_ib_proof_of_mapping_output_gbpusd_m15_v1.csv`
  - `n02_second_fx_subhour_historical_recovery_gbpusd_m15_summary_v1.md`
  - `n02_second_fx_subhour_historical_recovery_gbpusd_m15_summary_v1.json`
- 当前不伪装：
  - `TradeMaxGlobal-Demo__60088394` terminal fresh export 已成功修复
  - 当前证据属于 fresh export

## 当前怎么跑（v1）

- 历史输入：
  - `12_工具运行时_TOOLING_RUNTIME\VTMarkets-Live 2\GBPUSD-VIP15.hst`
- 生成器：
  - `real_input_samples\n02_mt4_hst_ingest_v1.py`
  - `real_input_samples\n02_proof_of_mapping_v2.py`
  - `real_input_samples\n02_ib_proof_of_mapping_v1.py`
  - `n02_second_fx_subhour_historical_recovery_gbpusd_m15_build_v1.py`
- 输出：
  - `real_input_samples\n02_real_input_gbpusd_m15_v1.csv`
  - `real_input_samples\n02_real_input_gbpusd_m15_report_v1.json`
  - `real_input_samples\n02_proof_of_mapping_output_gbpusd_m15_v1.csv`
  - `real_input_samples\n02_ib_proof_of_mapping_output_gbpusd_m15_v1.csv`
  - `n02_second_fx_subhour_historical_recovery_gbpusd_m15_summary_v1.md`
  - `n02_second_fx_subhour_historical_recovery_gbpusd_m15_summary_v1.json`

## 推荐复现命令

- `python real_input_samples\n02_mt4_hst_ingest_v1.py --symbol GBPUSD --timeframe M15`
- `python real_input_samples\n02_proof_of_mapping_v2.py --input ".\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_real_input_gbpusd_m15_v1.csv" --output ".\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_output_gbpusd_m15_v1.csv"`
- `python real_input_samples\n02_ib_proof_of_mapping_v1.py --input ".\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_real_input_gbpusd_m15_v1.csv" --output ".\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_ib_proof_of_mapping_output_gbpusd_m15_v1.csv" --symbol GBPUSD --timeframe M15`
- `python n02_second_fx_subhour_historical_recovery_gbpusd_m15_build_v1.py`

## 2026-07-05 fresh-run 结果

- historical recovered bars 已生成：
  - `source_hst=VTMarkets-Live 2\GBPUSD-VIP15.hst`
  - `bars_record_count=19032`
  - `bars_first_bar_time=2021-06-15T15:30:00Z`
  - `bars_last_bar_time=2022-03-18T23:45:00Z`
  - `bars_unique_minute_components=["00","15","30","45"]`
  - `bars_step_minutes_histogram={"15": 18991, "45": 1, "2895": 37, "2955": 2}`
- proof 已独立跑通：
  - `or_rows=457`
  - `or_defined_rows=396`
  - `ib_rows=457`
  - `ib_defined_rows=396`
  - `gate_status=historical_recovered_second_fx_subhour_ready`

## 当前结论

- 当前 `GBPUSD/M15` 已不再卡在 `build_or_reuse_hcc_reader_then_convert_to_canonical_bars`。
- 仓内现成 `HST reader` 足够把旧仓 `GBPUSD-VIP15.hst` 转成 canonical bars，并继续跑 OR / IB proof。
- 当前这层证据模式固定为：
  - `historical_recovered`
  - `declares_terminal_fresh_export=false`

## provenance 说明

- 这层结果来自旧仓 `VTMarkets-Live 2` 历史资产，不冒充今天的新 terminal 导出。
- `real_input_samples` 下的 proof 脚本早期会把基准目录解析到旧根目录；当前这批复现命令已统一改写为 repo 内相对路径（从仓库根目录执行），不再把树外路径写成默认入口。
- 当前已把复现命令统一改为 repo 内相对路径（从仓库根目录执行）。
