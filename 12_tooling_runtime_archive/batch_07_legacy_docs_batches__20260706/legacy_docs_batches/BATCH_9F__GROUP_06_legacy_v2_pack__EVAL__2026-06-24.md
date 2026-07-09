# 批次 9F - GROUP_06 legacy v2 pack - 评估 - 2026-06-24

## 目标

- absorb the remaining legacy `v2` pack under `GROUP_06`
- keep the earlier usable split pack separate from the newer `v2_final` stable/history pair that are already committed
- fully close `GROUP_06` as an open source-library residue lane

## 范围

- target root:
  - `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_06_Auction_MarketProfile_价格行为/01_A2_cutpack_v2`
- target pack:
  - `README_放这里.md`
  - `BATCH_SUMMARY__A2__v2.md`
  - `manifest_v2.tsv`
  - `5` legacy cutpack markdown files

## 目标文件

- `README_放这里.md`
- `BATCH_SUMMARY__A2__v2.md`
- `manifest_v2.tsv`
- `CUTPACK__A2__CN__市场轮廓理论__part1__v2.md`
- `CUTPACK__A2__CN__市场轮廓理论__part2__v2.md`
- `CUTPACK__A2__Dalton__MarketsInProfile__v2.md`
- `CUTPACK__A2__Dalton__MindOverMarkets__v2.md`
- `CUTPACK__A2__Harris__TradingAndExchanges__v2.md`

## 阅读结果

- `README_放这里.md` explicitly defines this directory as the earlier deletable-but-usable cutpack output for `A2`
- `BATCH_SUMMARY__A2__v2.md` already contains the batch summary, coverage matrix, and A-share alignment notes for this exact pack
- `manifest_v2.tsv` tracks the `5` cutpack payload files and marks the CN split files as current usable split parts inside this legacy lane
- the newer `01_A2_cutpack_v2_final` stable layer and history residue already landed in `Batch 9D` and `Batch 9E`, so this older pack can now be committed as one isolated legacy bundle

## 四分流裁决

- absorbed now:
  - the full `01_A2_cutpack_v2` legacy pack
- reopen later:
  - none inside `GROUP_06` after this cut
- future bucket:
  - any later freeze/archive reclassification outside the current source-library intake chain
- source-only for this cut:
  - none inside `GROUP_06`

## 裁决

- `Batch 9F` should contain the whole `01_A2_cutpack_v2` directory as one legacy pack
- do not reopen already committed `Batch 9C`, `Batch 9D`, or `Batch 9E`
- keep this cut scoped to `GROUP_06` only and do not mix other unopened `GROUP_*` trees

## 9F 后预期结果

- `GROUP_06` will be fully absorbed into repo across entry, stable, history, and legacy layers
- the remaining `Batch 9` open residue will narrow to `GROUP_01 / GROUP_02 / GROUP_03 / GROUP_04 / GROUP_05 / GROUP_07`
- next likely cut after `9F`:
  - `Batch 10 = next unopened Kimi group directory`
