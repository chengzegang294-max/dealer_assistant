# 批次 27 - SOURCE_LIBRARY 03_Kimi GROUP_06 old-tree retirement layer - 评估 - 2026-06-24

## 目标

- land the next clean deletion-only cut from the `03_Kimi拆书待入库 -> 01_Kimi拆书待入库` migration lane
- keep this batch limited to the `GROUP_06_Auction_MarketProfile_价格行为` old-tree retirement slice plus the batch docs/scripts

## 范围

- target old root:
  - `10_来源库_SOURCE_LIBRARY/03_Kimi拆书待入库`
- target old subtree in this cut:
  - `10_来源库_SOURCE_LIBRARY/03_Kimi拆书待入库/GROUP_06_Auction_MarketProfile_价格行为`
- stage boundary:
  - deletion-only paths under the target subtree
  - plus the batch docs/scripts under `docs/`

## 阅读结果

- the `03_Kimi拆书待入库` deletion cluster is classified as `真实迁移 / relayout` in:
  - `docs/SOURCE_LIBRARY_BACKLOG__来源层真实迁移__2026-06-23.md`
- after `Batch 24-26`, the remaining deletion residue under `03_Kimi拆书待入库` is `25`
- `GROUP_06_Auction_MarketProfile_价格行为 = 10` deletions is now the dominant grouped slice
- therefore this batch should isolate `GROUP_06` as a standalone retirement cut

## 四分流裁决

- absorbed now:
  - `03_Kimi拆书待入库/GROUP_06_Auction_MarketProfile_价格行为` old-tree retirement deletions (`10`)
- reopen later:
  - small fragments under `GROUP_01/02/03/04/05/07` (handled as a final cleanup cut)
- future bucket:
  - any deeper regrouping/relabeling work inside the new truth root (`01_Kimi拆书待入库`)
- source-only for this cut:
  - runtime snapshot items, tooling files, and unrelated directories

## 裁决

- `Batch 27` should contain only the `GROUP_06` old-tree retirement deletions plus the batch docs/scripts
- do not mix runtime snapshot files, `tools/s_bucketize.py`, or MT4/MT5 directories into this cut

