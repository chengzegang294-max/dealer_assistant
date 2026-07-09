# 批次 24 - SOURCE_LIBRARY 03_Kimi old root retirement layer - 评估 - 2026-06-24

## 目标

- land the cleanest first cut from the `03_Kimi拆书待入库 -> 01_Kimi拆书待入库` migration lane
- keep this batch limited to the old-root retirement files plus the batch docs/scripts

## 范围

- target old root:
  - `10_来源库_SOURCE_LIBRARY/03_Kimi拆书待入库`
- exact retirement slice in this cut:
  - root-level old-lane contracts, readme, panel exports, and duplicate ledgers only

## 阅读结果

- `docs/SOURCE_LIBRARY_BACKLOG__来源层真实迁移__2026-06-23.md` classifies the whole `03_Kimi拆书待入库` deletion cluster as `真实迁移 / relayout`
- the cluster size is `237` old-path deletions and is explicitly paired with the new truth root `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库`
- the cleanest first cut is the `13` root-level retirement files under the old root:
  - cut contracts
  - root readme
  - root panel exports
  - root S-bucket ledgers
  - root duplicate ledgers
- this cut avoids mixing the much larger `GROUP_08 / GROUP_09` old-tree retirements into the first deletion batch

## 四分流裁决

- absorbed now:
  - the `13` root-level retirement deletions under `03_Kimi拆书待入库`
- reopen later:
  - grouped old-tree retirements such as `GROUP_08` and `GROUP_09`
- future bucket:
  - deeper grouped deletions after the root-lane retirement is committed
- source-only for this cut:
  - unrelated modified files and non-source-library runtime items

## 裁决

- `Batch 24` should contain only the root-level old-lane retirement deletions plus the batch docs/scripts
- do not mix `GROUP_08 / GROUP_09` subtree deletions into this first cut
- do not mix `tools/s_bucketize.py`, runtime snapshot files, or the MT4 duplicate directory into this cut
