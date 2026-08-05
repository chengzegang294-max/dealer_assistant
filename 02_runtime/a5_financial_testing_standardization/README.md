# A5 financial testing standardization runtime

## 入口

- `run_a5_input_pack_acceptance_v1.py`
- `run_a5_multi_pack_gate_acceptance_v1.py`
- `run_a5_field_contract_acceptance_v1.py`
- `render_a5_second_date_plan_row_v1.py`
- `init_a5_second_date_batch_scaffold_v1.py`
- `finalize_a5_second_date_batch_absorb_v1.py`
- `upsert_a5_input_pack_plan_row_v1.py`
- `run_a5_second_date_intake_workflow_v1.py`
- `render_a5_second_date_postpass_backfill_v1.py`
- `render_a5_second_date_three_card_execution_bundle_v1.py`
- `a5_input_pack_sample_plan_v1.tsv`
- `a5_multi_pack_gate_sample_plan_v1.tsv`
- `a5_field_contract_template_v1.tsv`
- `batch150_field_contract_sample_v1.json`

## 用法

```powershell
python .\02_runtime\a5_financial_testing_standardization\run_a5_input_pack_acceptance_v1.py `
  --sample-plan .\02_runtime\a5_financial_testing_standardization\a5_input_pack_sample_plan_v1.tsv `
  --input-pack-id A5_R2_EASTMONEY_SCREENSHOT_INPUT_PACK_2026-07-29_V1 `
  --output-json .\02_runtime\a5_financial_testing_standardization\acceptance_outputs\a5_input_pack_acceptance_batch150_20260730.json
```

```powershell
python .\02_runtime\a5_financial_testing_standardization\run_a5_multi_pack_gate_acceptance_v1.py `
  --gate-plan .\02_runtime\a5_financial_testing_standardization\a5_multi_pack_gate_sample_plan_v1.tsv `
  --gate-id A5_FIN_STD_GATE_MIN_TWO_DATES_V1 `
  --output-json .\02_runtime\a5_financial_testing_standardization\acceptance_outputs\a5_multi_pack_gate_acceptance_20260730.json
```

```powershell
python .\02_runtime\a5_financial_testing_standardization\run_a5_field_contract_acceptance_v1.py `
  --contract-tsv .\02_runtime\a5_financial_testing_standardization\a5_field_contract_template_v1.tsv `
  --sample-json .\02_runtime\a5_financial_testing_standardization\batch150_field_contract_sample_v1.json `
  --output-json .\02_runtime\a5_financial_testing_standardization\acceptance_outputs\a5_field_contract_acceptance_batch150_20260730.json
```

```powershell
python .\02_runtime\a5_financial_testing_standardization\render_a5_second_date_plan_row_v1.py `
  --sample-date 2026-07-29 `
  --source-family batch_150_quicktiny_second_round_manual_sample__20260730 `
  --source-root .\10_source_library_archive\batch_150_quicktiny_second_round_manual_sample__20260730
```

```powershell
python .\02_runtime\a5_financial_testing_standardization\init_a5_second_date_batch_scaffold_v1.py `
  --batch-root .\10_source_library_archive\batch_151_second_date_sample__YYYYMMDD `
  --sample-date 2026-07-31
```

```powershell
python .\02_runtime\a5_financial_testing_standardization\finalize_a5_second_date_batch_absorb_v1.py `
  --batch-root .\10_source_library_archive\batch_151_second_date_sample__YYYYMMDD `
  --sample-date 2026-07-31 `
  --output-json .\02_runtime\a5_financial_testing_standardization\acceptance_outputs\a5_second_date_absorb_summary_20260731.json
```

```powershell
$row = python .\02_runtime\a5_financial_testing_standardization\render_a5_second_date_plan_row_v1.py `
  --sample-date 2026-07-31 `
  --source-family batch_151_second_date_sample__20260731 `
  --source-root .\10_source_library_archive\batch_151_second_date_sample__20260731

python .\02_runtime\a5_financial_testing_standardization\upsert_a5_input_pack_plan_row_v1.py `
  --sample-plan .\02_runtime\a5_financial_testing_standardization\a5_input_pack_sample_plan_v1.tsv `
  --row-text "$row"
```

```powershell
python .\02_runtime\a5_financial_testing_standardization\run_a5_second_date_intake_workflow_v1.py `
  --batch-root .\10_source_library_archive\batch_151_second_date_sample__20260731 `
  --sample-date 2026-07-31 `
  --source-family batch_151_second_date_sample__20260731 `
  --sample-plan .\02_runtime\a5_financial_testing_standardization\a5_input_pack_sample_plan_v1.tsv `
  --gate-plan .\02_runtime\a5_financial_testing_standardization\a5_multi_pack_gate_sample_plan_v1.tsv `
  --gate-id A5_FIN_STD_GATE_MIN_TWO_DATES_V1 `
  --output-json .\02_runtime\a5_financial_testing_standardization\acceptance_outputs\a5_second_date_workflow_summary_20260731.json
```

```powershell
python .\02_runtime\a5_financial_testing_standardization\render_a5_second_date_postpass_backfill_v1.py `
  --workflow-summary .\02_runtime\a5_financial_testing_standardization\acceptance_outputs\a5_second_date_workflow_summary_20260731.json `
  --output-json .\02_runtime\a5_financial_testing_standardization\acceptance_outputs\a5_second_date_postpass_backfill_20260731.json
```

```powershell
python .\02_runtime\a5_financial_testing_standardization\render_a5_second_date_three_card_execution_bundle_v1.py `
  --postpass-backfill-json .\02_runtime\a5_financial_testing_standardization\acceptance_outputs\a5_second_date_postpass_backfill_20260731.json `
  --output-json .\02_runtime\a5_financial_testing_standardization\acceptance_outputs\a5_second_date_three_card_execution_bundle_20260731.json
```
