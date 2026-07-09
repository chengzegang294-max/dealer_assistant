# Commit Ready Batch 29 - SOURCE_LIBRARY Batch9 root contracts/lists retirement layer - 2026-06-24

## 目标

- stage the root-level deletion-only retirement cut under `01_外部公开指标资料_Batch9`
- preserve this first Batch9 slice as an auditable standalone batch

## 精确暂存路径

- path list file:
  - `docs/commit_ready_batch_29__source_library_batch9_root_contracts_lists_retirement_layer__paths.txt`
- stage script:
  - `docs/commit_ready_stage_batch_29__source_library_batch9_root_contracts_lists_retirement_layer__2026-06-24.ps1`

## 本包纳入项

- `27` root-level deletions under:
  - `10_来源库_SOURCE_LIBRARY/01_外部公开指标资料_Batch9`
- batch docs/scripts:
  - `docs/BATCH_29__SOURCE_LIBRARY_Batch9_root_contracts_lists_retirement_layer__EVAL__2026-06-24.md`
  - `docs/COMMIT_READY__BATCH_29__SOURCE_LIBRARY_Batch9_root_contracts_lists_retirement_layer__2026-06-24.md`
  - `docs/commit_ready_batch_29__source_library_batch9_root_contracts_lists_retirement_layer__paths.txt`
  - `docs/commit_ready_stage_batch_29__source_library_batch9_root_contracts_lists_retirement_layer__2026-06-24.ps1`

## 本包排除项

- any deletion paths under:
  - `10_来源库_SOURCE_LIBRARY/01_外部公开指标资料_Batch9/N01_波动率状态机`
  - `10_来源库_SOURCE_LIBRARY/01_外部公开指标资料_Batch9/N02_时段_开盘区间结构`
  - `10_来源库_SOURCE_LIBRARY/01_外部公开指标资料_Batch9/N03_市场结构_突破质量_条件收集`
  - `10_来源库_SOURCE_LIBRARY/01_外部公开指标资料_Batch9/batch9_sources_kimi`
- any runtime snapshot or tooling items outside the batch docs/scripts

## 建议提交信息

- `docs: add Batch 29 SOURCE_LIBRARY Batch9 root contracts/lists retirement layer`

