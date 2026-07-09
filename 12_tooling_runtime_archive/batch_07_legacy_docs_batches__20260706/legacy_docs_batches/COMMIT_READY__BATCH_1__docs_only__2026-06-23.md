# Commit Ready Batch 1 - docs only - 2026-06-23

## 目标

- Stage only the long-term documentation layer first.
- Keep config assets and process assets out of this batch.
- Make source-library and `NFTRADEZ` interpretation auditable before any wider staging.

## 精确暂存文件

1. `01_阶段一_项目记录_过去与落地.md`
2. `02_阶段二_工作方向_想法库.md`
3. `03_阶段二_当下计划_执行清单.md`
4. `关于日活.md`
5. `docs/SOURCE_CONTROL_BACKLOG_TRIAGE__2026-06-23.md`
6. `docs/SOURCE_LIBRARY_BACKLOG__来源层真实迁移__2026-06-23.md`
7. `docs/SOURCE_LIBRARY_BACKLOG__误删候选__2026-06-23.md`
8. `docs/SOURCE_LIBRARY_BACKLOG__新增真值文件__2026-06-23.md`
9. `docs/SOURCE_LIBRARY_BACKLOG__staged_commit_ready_plan__2026-06-23.md`
10. `docs/COMMIT_READY__BATCH_1__docs_only__2026-06-23.md`
11. `docs/COMMIT_READY__BATCH_2__NFTRADEZ_truth_layer__2026-06-23.md`
12. `docs/commit_ready_stage_batch_1__docs_only__2026-06-23.ps1`
13. `docs/commit_ready_stage_batch_2__NFTRADEZ_truth_layer__2026-06-23.ps1`
14. `docs/commit_ready_batch_1__docs_only__paths.txt`
15. `docs/commit_ready_batch_2__NFTRADEZ_truth_layer__paths.txt`

## 显式排除项

- `.gitignore`
- `docs/playbooks/`
- `11_冻结总结层_FROZEN_SUMMARIES`
- any files under `10_来源库_SOURCE_LIBRARY`

## 为何存在该批次

- It lands the interpretation layer first.
- It gives the source-library backlog a stable audit contract.
- It lets the later `NFTRADEZ` truth-layer batch stay small and isolated.

## 建议提交信息

- `docs: lock source-library triage and NFTRADEZ intake state`

## 暂存命令

- Use:
  - `docs/commit_ready_stage_batch_1__docs_only__2026-06-23.ps1`
  - `docs/commit_ready_batch_1__docs_only__paths.txt`

## 验证

- Run the script once with `-DryRun`.
- Confirm that only the `15` files above are targeted.
- Confirm that `.gitignore` and `docs/playbooks/` stay outside this batch.
