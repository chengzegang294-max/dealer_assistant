# pv_corr_state_p0_manifest_freeze_v1

- ARCHIVE_ONLY: 该目录为旧库运行时快照；任何执行必须人工确认并设置 `ALLOW_ARCHIVE_ONLY_RUN=1`
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 目的

- 记录 `PV Corr State P0` 第一版 `manifest freeze` 的历史通过结果。
- 历史目标不是扩新层，而是把总索引相关文件冻结成历史可复核清单层。

## 本次验收对象

- manifest export：
  - `pv_corr_state_p0_export_manifest_freeze_v1.py`
- frozen compare：
  - `pv_corr_state_p0_chain_summary_acceptance_compare_v1.md`
- frozen index：
  - `pv_corr_state_p0_chain_summary_index_v1.md`

## ARCHIVE_ONLY 历史命令样例

```bash
$env:ALLOW_ARCHIVE_ONLY_RUN = "1"
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_export_manifest_freeze_v1.py
```

## 冻结结果

- export 输出确认：
  - `freeze_mode = archive_manifest_freeze_export`
  - `candidate_id = PV_CORR_STATE_P0`
  - `runtime_dir_exists = True`
  - `manifest_count = 12`
  - `all_manifest_files_exist = True`
  - `write_attempted = false`
  - `manifest_frozen = true`
  - `archive_manifest_freeze_passed = true`

## 历史可接受结论

- `PV Corr State P0` 在旧链路中已具备覆盖 `12` 个关键文件槽位的冻结清单层。
- 历史上仍不能宣称：
  - 已接 repo-first 历史 bar window 数据
  - 已进入 repo-first 历史 runtime append


