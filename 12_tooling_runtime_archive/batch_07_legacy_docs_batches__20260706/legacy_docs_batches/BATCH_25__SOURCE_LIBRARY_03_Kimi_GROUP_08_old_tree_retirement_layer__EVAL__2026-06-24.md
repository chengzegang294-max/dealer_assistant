# Batch 25 - SOURCE_LIBRARY 03_Kimi GROUP_08 old-tree retirement layer - EVAL - 2026-06-24

## Goal

- land the next clean deletion-only cut from the `03_Kimi拆书待入库 -> 01_Kimi拆书待入库` migration lane
- keep this batch limited to the `GROUP_08_A股量化_数据研究` old-tree retirement slice plus the batch docs/scripts

## Scope

- target old root:
  - `10_来源库_SOURCE_LIBRARY/03_Kimi拆书待入库`
- target old subtree in this cut:
  - `10_来源库_SOURCE_LIBRARY/03_Kimi拆书待入库/GROUP_08_A股量化_数据研究`
- stage boundary:
  - deletion-only paths under the target subtree
  - plus the batch docs/scripts under `docs/`

## Read Result

- the `03_Kimi拆书待入库` deletion cluster is classified as `真实迁移 / relayout` in:
  - `docs/SOURCE_LIBRARY_BACKLOG__来源层真实迁移__2026-06-23.md`
- after `Batch 24` removed the old-root retirement layer, the remaining deletion residue under `03_Kimi拆书待入库` is `224`
- the dominant remaining slice is the grouped old subtree:
  - `GROUP_08_A股量化_数据研究 = 178` deletions
- therefore this batch should isolate `GROUP_08` as its own standalone retirement cut

## Four-Way Verdict

- absorbed now:
  - `03_Kimi拆书待入库/GROUP_08_A股量化_数据研究` old-tree retirement deletions (`178`)
- reopen later:
  - other grouped old-tree retirements such as `GROUP_09` and `GROUP_06`
- future bucket:
  - any deeper regrouping/relabeling work inside the new truth root (`01_Kimi拆书待入库`)
- source-only for this cut:
  - runtime snapshot items, tooling files, and unrelated directories

## Decision

- `Batch 25` should contain only the `GROUP_08` old-tree retirement deletions plus the batch docs/scripts
- do not mix `GROUP_09` or `GROUP_06` deletion slices into this cut
- do not mix runtime snapshot files, `tools/s_bucketize.py`, or MT4/MT5 directories into this cut

