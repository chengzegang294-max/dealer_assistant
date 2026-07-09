# 批次 29 - SOURCE_LIBRARY Batch9 root contracts/lists retirement layer - 评估 - 2026-06-24

## 目标

- land the cleanest first cut from the `01_外部公开指标资料_Batch9` deletion cluster
- keep this batch limited to the Batch9 root-level contracts/lists only plus the batch docs/scripts

## 范围

- target old root:
  - `10_来源库_SOURCE_LIBRARY/01_外部公开指标资料_Batch9`
- retirement slice in this cut:
  - root-level `Batch9_*` summaries, mapping tables, and checklists
  - root-level `REOPEN_B9_*` progress notes
  - root-level P0 contract notes / headers / samples
  - root-level manifest and watch lists
- explicitly excluded in this cut:
  - `N01_波动率状态机`
  - `N02_时段_开盘区间结构`
  - `N03_市场结构_突破质量_条件收集`
  - `batch9_sources_kimi/**`

## 阅读结果

- current deletion status under Batch9 is `66` paths total, with `27` root-level files and the rest inside grouped subfolders
- the cleanest first cut is the `27` root-level contracts/lists because:
  - it is small enough to be reviewed as a single batch
  - it does not require mixing the deeper N01/N02/N03 research materials
  - it keeps the later folder-level retirements clean and auditable

## 四分流裁决

- absorbed now:
  - `27` root-level retirement deletions under `01_外部公开指标资料_Batch9`
- reopen later:
  - grouped retirements inside `N01/N02/N03` and `batch9_sources_kimi`
- future bucket:
  - any regrouping work after the deletion lane is fully closed
- source-only for this cut:
  - runtime snapshot items, tooling files, and unrelated directories

## 裁决

- `Batch 29` should contain only the Batch9 root-level retirement deletions plus the batch docs/scripts
- do not mix any subfolder retirements in this cut

