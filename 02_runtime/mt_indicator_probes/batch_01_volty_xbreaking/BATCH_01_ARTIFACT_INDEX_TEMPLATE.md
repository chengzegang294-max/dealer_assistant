# Probe Batch 01 Artifact Index Template

## 批次信息

- `batch_id`: `batch_01_volty_xbreaking`
- `date_tag`: `20260701`
- `operator`: `agent`
- `platform_mix`: `MT4 + MT5`
- `playbook`: `MT4_MT5_FIRST_RUN_PLAYBOOK.md`

## Volty

- `platform`: `MT4`
- `probe_entry`: `12_tooling_runtime_archive\batch_02_mt_indicator_family\MT4Probe_Volty.mq4`
- `indicator_entry`: `12_tooling_runtime_archive\batch_02_mt_indicator_family\VoltyChannel_Stop_v2_1M.mq4`
- `symbol`: `EURUSD`
- `indicator_tf`: `H1`
- `csv`: `artifacts\volty\csv\MT4_probe_Volty_EURUSD_H1_20250102_000000_20260701T035759.csv`
- `log`: `artifacts\volty\log\20260701_20260701T035759.log`
- `log_excerpt`: `artifacts\volty\log\20260701_20260701T035759__excerpt.txt`
- `tester_report`: `artifacts\volty\tester_report\mt4probe_volty_dumpseries_portable_20260701T035759.htm`
- `result_status`: `fresh_run_dumpseries_verified`
- `repo_csv_dir`: `artifacts\volty\csv`
- `repo_log_dir`: `artifacts\volty\log`
- `repo_tester_report_dir`: `artifacts\volty\tester_report`
- `rerun_tester_ini`: `mt4probe_volty_dumpseries_portable.ini`
- `rerun_expert_inputs`: `MT4Probe_Volty_dumpseries_0_6.ini`
- `history_patch_script`: `fill_mt4_eurusd_h1_history_v1.py`
- `gui_rerun_script`: `run_volty_dumpseries_gui_once.ps1`
- `rerun_parameter_status`: `batch_local_dumpseries_template_ready`
- `intake_backfill`: `03_docs\mt_indicator_engineering\volty_probe_result_intake_v1.md`
- `chart_tf`: `60`
- `indicator_tf_raw`: `60`
- `indicator_name`: `Probe\VoltyChannel_Stop_v2_1M`
- `max_modes`: `8`
- `max_shifts`: `50`
- `used_common`: `0`
- `status_row`: `DONE`
- `normalize_command`: `python probe_artifact_ingest_v1.py --family volty --kind csv --normalize-volty-summary`
- `normalize_series_command`: `python probe_artifact_ingest_v1.py --family volty --kind csv --normalize-volty-series`
- `series_dump_support`: `MT4Probe_Volty.mq4 supports DumpSeries/DumpModeStart/DumpModeEnd`
- `series_row_count`: `350`
- `history_patch_summary`: `artifacts\volty\history_patch\fill_mt4_eurusd_h1_history_latest.json`

## XBreaking

- `platform`: `MT5`
- `probe_entry`: `12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreakingProbe.mq5`
- `indicator_entry`: `12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreaking.ex5`
- `symbol`: `EURUSD`
- `indicator_tf`: `PERIOD_H1`
- `csv`: `artifacts\xbreaking\csv\XBreaking_probe_EURUSD_H1_20250102_000030.csv`
- `log`: `artifacts\xbreaking\log\20260701_20260701T041405.log`
- `log_excerpt`: `artifacts\xbreaking\log\20260701_20260701T041405__excerpt.txt`
- `tester_report`: `artifacts\xbreaking\tester_report\xbreaking_probe_portable.htm`
- `result_status`: `fresh_run_probe_report_verified`
- `repo_csv_dir`: `artifacts\xbreaking\csv`
- `repo_log_dir`: `artifacts\xbreaking\log`
- `repo_tester_report_dir`: `artifacts\xbreaking\tester_report`
- `mt5_tester_ini`: `12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreakingProbe.ini`
- `mt4_tester_ini`: `12_tooling_runtime_archive\batch_02_mt_indicator_family\MT4Probe_XBreaking.ini`
- `mt5_rerun_script`: `run_xbreaking_probe_once.ps1`
- `mt5_environment_inventory`: `environment_snapshots\mt_environment_inventory_latest.json`
- `ini_status`: `repo_local_relative_report_ready_with_runtime_fallback`
- `environment_selection_status`: `origin_autodiscovery + DataRootOverride + EnvironmentInventoryJson/EnvironmentSelector ready`
- `intake_backfill`: `03_docs\mt_indicator_engineering\xbreaking_buffer_semantics_log_v1.md`
- `handle`: `10`
- `init_err`: `0`
- `bars_to_probe`: `200`
- `max_buffers`: `8`
- `buffer_activity_profile`: `buffer0_only`
- `log_assessment`: `tester_log_present_and_strongly_related`
- `report_runtime_note`: `Report=xbreaking_probe_portable may land under MT5 data root instead of tester\\files`
- `validation_matrix_example`: `artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_20260701T1305`
- `validation_matrix_run_summary`: `artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_20260701T1305\run_summary.json`
- `validation_matrix_ingest_manifest`: `artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_20260701T1305\ingest_manifest.json`
- `validation_matrix_index`: `artifacts\xbreaking\validation_matrix\validation_matrix_index_latest.json`
- `environment_label`: `ICMarketsSC-Demo__52886989`

## 回写检查

- `volty_intake_updated`: `yes`
- `xbreaking_semantics_updated`: `yes`
- `field_draft_rechecked`: `yes`
- `root_readme_sync_needed`: `no`

## 备注

- `XBreaking` 已通过 `run_xbreaking_probe_once.ps1` 自动跑出 fresh-run `csv + tester report + terminal log + tester log`。
- `XBreaking` 默认回收时现已优先更强相关的 `tester\logs`，避免先拿到弱相关 terminal log。
- `XBreakingProbe.ini` 与 `MT4Probe_XBreaking.ini` 已改为终端内相对报告路径，不再默认依赖旧仓库绝对地址。
- `XBreaking` 的 `validation_matrix/<tag>/` 当前支持两种选环境方式：`DataRootOverride` 与 `EnvironmentInventoryJson + EnvironmentSelector`。
- 通过 `probe_artifact_ingest_v1.py --archive-tag <tag>` 回收到 `validation_matrix` 时，当前会自动写出 `ingest_manifest.json`，记录 `source_path / repo_path / matched_keywords / excerpt_path`。
- `validation_matrix_index_latest.json` 当前会总览各 archive 的 `symbol / chart_period / indicator_period / environment_label / selection_mode / manifest_record_count`。
- `Volty` 已完成一轮 `EURUSD/H1/DumpSeries=1` fresh-run，当前 `series_row_count = 350`，`series -> field row` 已闭环。
