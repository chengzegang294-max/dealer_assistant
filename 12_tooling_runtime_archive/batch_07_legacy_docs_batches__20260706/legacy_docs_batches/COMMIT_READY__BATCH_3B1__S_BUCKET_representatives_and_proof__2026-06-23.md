# Commit Ready Batch 3B1 - S_BUCKET representatives + stage proof - 2026-06-23

## 目标

- Land the `03_券商研报` representatives selection TSV series and its stage-proof TSV series as one evidence-only commit.
- Keep this batch purely tabular evidence.
- Do not include `S_BUCKET__staging/` or any `GROUP_*` trees.

## 精确暂存文件

- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_report_representatives_v1.tsv` ... `S_BUCKET_report_representatives_v52.tsv`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_stage_proof__03_券商研报__representatives_v1.tsv` ... `S_BUCKET_stage_proof__03_券商研报__representatives_v52.tsv`

## 显式排除项

- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET__staging/`
- any `S_BUCKET_stage_proof__01_集合竞价教程__*.tsv`
- any `S_BUCKET_SUMMARY__*.md` / `S_BUCKET_INDEX__*.tsv` / `S_BUCKET_功能*`
- any `S_BUCKET_KIMI_*` contract files
- any `GROUP_*` subtrees

## 建议提交信息

- `docs: add S_BUCKET representatives v1-v52 and stage proof v1-v52 (03_券商研报)`

## 暂存命令

- Use:
  - `docs/commit_ready_stage_batch_3B1__S_BUCKET_representatives_and_proof__2026-06-23.ps1`
  - `docs/commit_ready_batch_3B1__S_BUCKET_representatives_and_proof__paths.txt`

## 验证

- Run the script once with `-DryRun`.
- Confirm that only `104` TSV evidence files plus the batch pack files are targeted.
