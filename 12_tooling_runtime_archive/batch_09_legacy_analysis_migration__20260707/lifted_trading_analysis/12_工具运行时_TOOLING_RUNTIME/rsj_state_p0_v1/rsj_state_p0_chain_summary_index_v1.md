# rsj_state_p0_chain_summary_index_v1

- ARCHIVE_ONLY: 该目录为旧库运行时快照；任何执行必须人工确认并设置 `ALLOW_ARCHIVE_ONLY_RUN=1`
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 目的

- 作为 `RSJ State P0` 历史只读链路的总索引壳。
- 把已落的合同、acceptance、preview 与总链路校验收成一份可复核历史入口，避免旧链路证据散落。

## ARCHIVE_ONLY 历史命令样例

```bash
$env:ALLOW_ARCHIVE_ONLY_RUN = "1"
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_export_chain_summary_index_v1.py
```

## 导出结果

- `summary_mode = archive_chain_summary_index_export`
- `candidate_id = RSJ_STATE_P0`
- `runtime_dir_exists = True`
- `runtime_csv_exists = True`
- `preview_csv_exists = True`
- `runtime_row_count = 5`
- `preview_row_count = 3`
- `stage_count = 10`
- `all_stage_files_exist = True`
- `write_attempted = false`
- `archive_chain_summary_export_passed = true`

## 历史链路索引

- `01`
  - `rsj_state_p0_min_contract_v1.md`
- `02`
  - `rsj_state_p0_proof_of_mapping_v1.md`
- `03`
  - `rsj_state_p0_runtime_append_acceptance_v1.md`
- `04`
  - `rsj_state_p0_raw_window_sample_acceptance_v1.md`
- `05`
  - `rsj_state_p0_raw_window_mapping_acceptance_v1.md`
- `06`
  - `rsj_state_p0_append_compatibility_acceptance_v1.md`
- `07`
  - `rsj_state_p0_simulate_append_diff_acceptance_v1.md`
- `08`
  - `rsj_state_p0_replay_preview_acceptance_v1.md`
- `09`
  - `rsj_state_p0_replay_preview_acceptance_validation_v1.md`
- `10`
  - `rsj_state_p0_replay_chain_acceptance_v1.md`

## 历史可接受结论

- `RSJ State P0` 已具备从最小合同到 `replay chain validation` 的只读证据链总索引。
- 历史上仍不能宣称：
  - 已接 repo-first 历史 raw window 数据
  - 已把 replay 结果回写仓内运行产物
  - 已升级为 repo-first 历史绑定说明或旧链路信号链


