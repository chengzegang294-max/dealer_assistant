# Batch 9C - GROUP_06 entry layer - EVAL - 2026-06-24

## 目标

- absorb the root entry layer of `GROUP_06`
- keep the clean entry definitions separate from the heavier `cutpack` subtrees
- leave the next `GROUP_06` cuts reviewable as body-layer or archive-layer commits

## 范围

- target root:
  - `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_06_Auction_MarketProfile_价格行为`
- current clean entry residue:
  - `3` root-level markdown files

## 目标文件

- `GROUP_06_market_profile_price_action.md`
- `GROUP_06_market_profile_price_action_DEFINITIONS.md`
- `GROUP_06_最小吸收包_v1.md`

## 阅读结果

- `GROUP_06_market_profile_price_action.md` is the root object-definition overview for the whole group
- `GROUP_06_market_profile_price_action_DEFINITIONS.md` is the programmable definitions layer, but still belongs to the root entry rather than the cutpack body
- `GROUP_06_最小吸收包_v1.md` already fixes the current absorption order and the `N02`-upstream role for this group
- both `01_A2_cutpack_v2` and `01_A2_cutpack_v2_final` are real follow-up trees and should not be mixed into the first `GROUP_06` commit

## 四分流裁决

- absorbed now:
  - `GROUP_06` root entry definitions and minimum absorption order
  - the group-level statement that this lane is an `N02` upstream object-definition layer
- reopen later:
  - `01_A2_cutpack_v2`
  - `01_A2_cutpack_v2_final`
- future bucket:
  - deeper `TPO` engineering beyond the current root entry pack
- source-only for this cut:
  - deferred body/history trees for later isolated commits

## 裁决

- `Batch 9C` should contain only the `3` root entry files of `GROUP_06`
- do not mix `01_A2_cutpack_v2`
- do not mix `01_A2_cutpack_v2_final`
- do not reopen already committed `Batch 9A` or `Batch 9B`

## 9C 后预期结果

- `01_Kimi` inbox residue remains narrowed to the unopened group trees, but `GROUP_06` will no longer be a fully unopened directory
- `GROUP_06` will then be ready for a later split such as:
  - stable cutpack layer
  - final/history cutpack layer
- next likely cut after `9C`:
  - `Batch 9D = GROUP_06 cutpack layer`
