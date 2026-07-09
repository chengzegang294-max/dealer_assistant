# Batch 26 - SOURCE_LIBRARY 03_Kimi GROUP_09 old-tree retirement layer - EVAL - 2026-06-24

## 目标

- land the next clean deletion-only cut from the `03_Kimi拆书待入库 -> 01_Kimi拆书待入库` migration lane
- keep this batch limited to the `GROUP_09_完善体系书库_切割产物` old-tree retirement slice plus the batch docs/scripts

## 范围

- target old root:
  - `10_来源库_SOURCE_LIBRARY/03_Kimi拆书待入库`
- target old subtree in this cut:
  - `10_来源库_SOURCE_LIBRARY/03_Kimi拆书待入库/GROUP_09_完善体系书库_切割产物`
- stage boundary:
  - deletion-only paths under the target subtree
  - plus the batch docs/scripts under `docs/`

## 阅读结果

- the `03_Kimi拆书待入库` deletion cluster is classified as `真实迁移 / relayout` in:
  - `docs/SOURCE_LIBRARY_BACKLOG__来源层真实迁移__2026-06-23.md`
- after `Batch 24-25`, the remaining deletion residue under `03_Kimi拆书待入库` is small and grouped
- `GROUP_09_完善体系书库_切割产物 = 21` deletions is now the cleanest next standalone cut

## 四分流裁决

- absorbed now:
  - `03_Kimi拆书待入库/GROUP_09_完善体系书库_切割产物` old-tree retirement deletions (`21`)
- reopen later:
  - other grouped old-tree retirement such as `GROUP_06`
- future bucket:
  - any deeper regrouping/relabeling work inside the new truth root (`01_Kimi拆书待入库`)
- source-only for this cut:
  - runtime snapshot items, tooling files, and unrelated directories

## 裁决

- `Batch 26` should contain only the `GROUP_09` old-tree retirement deletions plus the batch docs/scripts
- do not mix `GROUP_06` deletion slice into this cut
- do not mix runtime snapshot files, `tools/s_bucketize.py`, or MT4/MT5 directories into this cut

