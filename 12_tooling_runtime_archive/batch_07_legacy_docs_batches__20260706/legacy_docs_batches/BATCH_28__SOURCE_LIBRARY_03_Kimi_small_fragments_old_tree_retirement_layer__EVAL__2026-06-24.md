# Batch 28 - SOURCE_LIBRARY 03_Kimi small fragments old-tree retirement layer - EVAL - 2026-06-24

## 目标

- close the remaining deletion residue under `03_Kimi拆书待入库` after `Batch 24-27`
- keep this batch limited to the small fragment groups plus the batch docs/scripts

## 范围

- target old root:
  - `10_来源库_SOURCE_LIBRARY/03_Kimi拆书待入库`
- target groups in this cut:
  - `GROUP_01_微观结构_交易所_HFT`
  - `GROUP_02_期权_波动率_波动率微笑`
  - `GROUP_03_组合管理_风险模型_交易成本`
  - `GROUP_04_统计套利_研究方法_ML`
  - `GROUP_05_趋势_系统交易`
  - `GROUP_07_传记_行业史_故事`
- stage boundary:
  - deletion-only paths under the target groups
  - plus the batch docs/scripts under `docs/`

## 阅读结果

- the `03_Kimi拆书待入库` deletion cluster is classified as `真实迁移 / relayout` in:
  - `docs/SOURCE_LIBRARY_BACKLOG__来源层真实迁移__2026-06-23.md`
- after `Batch 27` retired `GROUP_06`, the remaining residue is `15` deletions across the small fragment groups above
- this batch should group those fragments into a single final cleanup cut to close the `03_Kimi` old-tree retirement lane

## 四分流裁决

- absorbed now:
  - `15` small-fragment old-tree retirement deletions across `GROUP_01/02/03/04/05/07`
- reopen later:
  - none inside `03_Kimi拆书待入库` after this cut
- future bucket:
  - any deeper regrouping/relabeling work inside the new truth root (`01_Kimi拆书待入库`)
- source-only for this cut:
  - runtime snapshot items, tooling files, and unrelated directories

## 裁决

- `Batch 28` should contain only the small-fragment retirement deletions plus the batch docs/scripts
- do not mix runtime snapshot files, `tools/s_bucketize.py`, or MT4/MT5 directories into this cut

