# Commit Ready Batch 3B2 - S_BUCKET Kimi contracts - 2026-06-23

## 目标

- Land the `S_BUCKET` Kimi contract files (prompt / direct_message) and the batch manifests/READMEs as an independent commit.
- Keep this batch purely contractual and small.
- Do not include representatives/proof series and do not include `S_BUCKET__staging/`.

## 精确暂存文件

- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_KIMI_batch1_prompt_v1.txt`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_KIMI_batch1_priority_read_prompt_v1.txt`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_KIMI_batch1_round2_direct_message_v2.txt`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_KIMI_batch1_round2_focus_prompt_v1.txt`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_KIMI_batch1_round3_function_core_direct_message_v1.txt`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_KIMI_batch1_round3_function_core_prompt_v1.txt`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_batch1_round2_focus_README_v1.md`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_batch1_round2_focus_manifest_v1.tsv`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_batch1_round3_function_core_README_v1.md`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_batch1_round3_function_core_manifest_v1.tsv`

## 显式排除项

- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET__staging/`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_report_representatives_v*.tsv`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_stage_proof__*.tsv`
- any `GROUP_*` subtrees

## 建议提交信息

- `docs: add S_BUCKET Kimi contract pack (batch1 prompts/manifests/readmes)`

## 暂存命令

- Use:
  - `docs/commit_ready_stage_batch_3B2__S_BUCKET_KIMI_contracts__2026-06-23.ps1`
  - `docs/commit_ready_batch_3B2__S_BUCKET_KIMI_contracts__paths.txt`

## 验证

- Run the script once with `-DryRun`.
- Confirm that only the `10` contract files plus the batch pack files are targeted.
