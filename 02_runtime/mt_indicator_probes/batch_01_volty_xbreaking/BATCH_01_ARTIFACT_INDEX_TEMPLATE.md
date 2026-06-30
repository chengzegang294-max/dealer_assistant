# Probe Batch 01 Artifact Index Template

## 批次信息

- `batch_id`: `batch_01_volty_xbreaking`
- `date_tag`: `20260626`
- `operator`: `agent + user_terminal`
- `platform_mix`: `MT4 + MT5`
- `playbook`: `MT4_MT5_FIRST_RUN_PLAYBOOK.md`

## Volty

- `platform`: `MT4`
- `probe_entry`: `12_tooling_runtime_archive\batch_02_mt_indicator_family\MT4Probe_Volty.mq4`
- `indicator_entry`: `12_tooling_runtime_archive\batch_02_mt_indicator_family\VoltyChannel_Stop_v2_1M.mq4`
- `symbol`: `EURUSD`
- `indicator_tf`: `H4`
- `csv`: `artifacts\volty\csv\MT4_probe_Volty_EURUSD_H4_20250102_000000.csv`
- `log`: `pending`
- `tester_report`: `artifacts\volty\tester_report\mt4probe_volty_portable.htm`
- `result_status`: `historical_csv_and_report_recovered`
- `repo_csv_dir`: `artifacts\volty\csv`
- `repo_log_dir`: `artifacts\volty\log`
- `repo_tester_report_dir`: `artifacts\volty\tester_report`
- `intake_backfill`: `03_docs\mt_indicator_engineering\volty_probe_result_intake_v1.md`
- `chart_tf`: `240`
- `indicator_tf_raw`: `240`
- `indicator_name`: `Probe\VoltyChannel_Stop_v2_1M`
- `max_modes`: `8`
- `max_shifts`: `50`
- `used_common`: `0`
- `status_row`: `DONE`
- `normalize_command`: `python probe_artifact_ingest_v1.py --family volty --kind csv --normalize-volty-summary`
- `normalize_series_command`: `python probe_artifact_ingest_v1.py --family volty --kind csv --normalize-volty-series`
- `series_dump_support`: `MT4Probe_Volty.mq4 supports DumpSeries/DumpModeStart/DumpModeEnd`

## XBreaking

- `platform`: `MT5`
- `probe_entry`: `12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreakingProbe.mq5`
- `indicator_entry`: `12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreaking.ex5`
- `symbol`: `EURUSD`
- `indicator_tf`: `PERIOD_H1`
- `csv`: `artifacts\xbreaking\csv\XBreaking_probe_EURUSD_H1_20250101_220500.csv`
- `log`: `artifacts\xbreaking\log\20260609.log`
- `log_excerpt`: `artifacts\xbreaking\log\20260609__excerpt.txt`
- `tester_report`: `pending`
- `result_status`: `csv_recovered_verified_buffers_partial`
- `repo_csv_dir`: `artifacts\xbreaking\csv`
- `repo_log_dir`: `artifacts\xbreaking\log`
- `repo_tester_report_dir`: `artifacts\xbreaking\tester_report`
- `intake_backfill`: `03_docs\mt_indicator_engineering\xbreaking_buffer_semantics_log_v1.md`
- `handle`: `10`
- `init_err`: `0`
- `bars_to_probe`: `200`
- `max_buffers`: `8`
- `log_assessment`: `only_excerpt_present_not_strong_tester_journal_evidence`

## 回写检查

- `volty_intake_updated`: `yes`
- `xbreaking_semantics_updated`: `yes`
- `field_draft_rechecked`: `yes`
- `root_readme_sync_needed`: `no`

## 备注

- `XBreaking` 已通过自动 ingest 找到并复制首份 `csv`，但 `log / tester_report` 仍未回收。
- `XBreaking` 已额外回收 `20260609.log + excerpt`，但 excerpt 内容为通用迁移日志片段，未检出 `XBreaking / XBreakingProbe / tester` 关键词，因此仍是 `weak_evidence`。
- `Volty` 自动扫描本机 `MetaQuotes` 目录仍未发现新产物，但已从旧仓库回收一份历史 `csv + tester report`，因此当前状态改为 `historical_recovered`。
