# 提交就绪批次 3A - S_BUCKET core truth anchors - 2026-06-23

## 目标

- Land the minimal `S_BUCKET_*` truth anchors as an independent commit.
- Keep this batch small and stable.
- Do not include `GROUP_*` trees and do not include the large `S_BUCKET_report_representatives_*` / `S_BUCKET_stage_proof_*` series in this first step.

## 精确暂存文件

1. `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_SUMMARY__2026-06-17.md`
2. `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_INDEX__2026-06-17.tsv`
3. `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_功能映射表_v1.tsv`
4. `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_功能归类最小框架_v1.md`

## 显式排除项

- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET__staging/`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_report_representatives_v*.tsv`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_stage_proof__*.tsv`
- any `GROUP_*` subtrees

## 建议提交信息

- `docs: add S_BUCKET core truth anchors (summary/index/framework/map)`

## 暂存命令

- Use:
  - `docs/commit_ready_stage_batch_3A__S_BUCKET_core__2026-06-23.ps1`
  - `docs/commit_ready_batch_3A__S_BUCKET_core__paths.txt`

## 验证

- Run the script once with `-DryRun`.
- Confirm that only the `4` files above are targeted.
