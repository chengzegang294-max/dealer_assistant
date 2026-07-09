# 提交就绪批次 27 - SOURCE_LIBRARY 03_Kimi GROUP_06 old-tree retirement layer - 2026-06-24

## 目标

- stage the deletion-only retirement cut for `03_Kimi拆书待入库/GROUP_06_Auction_MarketProfile_价格行为`
- preserve this grouped subtree retirement as an auditable migration batch

## 精确暂存路径

- path list file:
  - `docs/commit_ready_batch_27__source_library_03_kimi_group_06_old_tree_retirement_layer__paths.txt`
- stage script:
  - `docs/commit_ready_stage_batch_27__source_library_03_kimi_group_06_old_tree_retirement_layer__2026-06-24.ps1`

## 本包纳入项

- deletion-only retirement paths under:
  - `10_来源库_SOURCE_LIBRARY/03_Kimi拆书待入库/GROUP_06_Auction_MarketProfile_价格行为`
- batch docs/scripts:
  - `docs/BATCH_27__SOURCE_LIBRARY_03_Kimi_GROUP_06_old_tree_retirement_layer__EVAL__2026-06-24.md`
  - `docs/COMMIT_READY__BATCH_27__SOURCE_LIBRARY_03_Kimi_GROUP_06_old_tree_retirement_layer__2026-06-24.md`
  - `docs/commit_ready_batch_27__source_library_03_kimi_group_06_old_tree_retirement_layer__paths.txt`
  - `docs/commit_ready_stage_batch_27__source_library_03_kimi_group_06_old_tree_retirement_layer__2026-06-24.ps1`

## 本包排除项

- any runtime snapshot or tooling items outside the batch docs/scripts
- any remaining `03_Kimi` small fragments under:
  - `GROUP_01/02/03/04/05/07`

## 建议提交信息

- `docs: add Batch 27 SOURCE_LIBRARY 03_Kimi GROUP_06 old-tree retirement layer`

