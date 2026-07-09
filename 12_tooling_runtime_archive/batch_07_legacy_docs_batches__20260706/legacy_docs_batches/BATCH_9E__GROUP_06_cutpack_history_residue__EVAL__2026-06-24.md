# 批次 9E - GROUP_06 cutpack history residue - 评估 - 2026-06-24

## 目标

- absorb the explicit history-only residue inside `GROUP_06/01_A2_cutpack_v2_final`
- keep the history-only copies separate from both the stable cutpack layer and the older `01_A2_cutpack_v2` subtree
- finish the archive residue that the final README already classifies as non-stable

## 范围

- target root:
  - `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_06_Auction_MarketProfile_价格行为/01_A2_cutpack_v2_final`
- target residue:
  - `5` history-only markdown files already listed in `README_放这里.md`

## 目标文件

- `CUTPACK__A2__CN__市场轮廓理论__part1__v2.md`
- `CUTPACK__A2__CN__市场轮廓理论__part2__v2_r1.md`
- `CUTPACK__A2__Dalton__MarketsInProfile__v2.md`
- `CUTPACK__A2__Dalton__MindOverMarkets__v2.md`
- `CUTPACK__A2__Harris__TradingAndExchanges__v2.md`

## 阅读结果

- `README_放这里.md` already classifies these `5` files as kept history copies rather than stable entry
- these files remain in the same final directory only as archive residue and should not be mixed into the stable-layer commit
- the stable entry contract and `5` stable files already landed in `Batch 9D`
- the older `01_A2_cutpack_v2` subtree still has its own batch summary, manifest, and early usable split pack, so it should stay separate from this pure history cut

## 四分流裁决

- absorbed now:
  - the explicit history-only residue listed by the final README
- reopen later:
  - `01_A2_cutpack_v2` as its own legacy cutpack pack
- future bucket:
  - any later relocation into a dedicated frozen history/archive lane
- source-only for this cut:
  - `01_A2_cutpack_v2`

## 裁决

- `Batch 9E` should contain only the `5` history-only files under `01_A2_cutpack_v2_final`
- do not reopen the stable files already committed in `Batch 9D`
- do not mix `README_放这里.md` or `manifest_v2.tsv`, because they already belong to the stable-layer contract committed in `9D`
- do not mix the older `01_A2_cutpack_v2` subtree

## 9E 后预期结果

- `GROUP_06/01_A2_cutpack_v2_final` will be fully absorbed into repo with stable and history layers separated cleanly
- the remaining `GROUP_06` residue will narrow to `01_A2_cutpack_v2` only
- next likely cut after `9E`:
  - `Batch 9F = GROUP_06 legacy v2 pack`
