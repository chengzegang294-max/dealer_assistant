# 批次 9D - GROUP_06 cutpack stable layer - 评估 - 2026-06-24

## 目标

- absorb the stable cutpack layer under `GROUP_06`
- keep the final stable entry set separate from older body/history copies
- leave the archive/history residue for a later isolated commit

## 范围

- target root:
  - `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_06_Auction_MarketProfile_价格行为/01_A2_cutpack_v2_final`
- stable entry contract:
  - `README_放这里.md`
  - `manifest_v2.tsv`
  - `5` stable cutpack markdown files

## 目标文件

- `README_放这里.md`
- `manifest_v2.tsv`
- `CUTPACK__A2__CN__市场轮廓理论__part1__v2_r1.md`
- `CUTPACK__A2__CN__市场轮廓理论__part2__v2_r2.md`
- `CUTPACK__A2__Dalton__MarketsInProfile__v2_r1.md`
- `CUTPACK__A2__Dalton__MindOverMarkets__v2_r1.md`
- `CUTPACK__A2__Harris__TradingAndExchanges__v2_r1.md`

## 阅读结果

- `README_放这里.md` explicitly says this directory is the only stable entry set for later use
- `manifest_v2.tsv` records only the stable entry files and their current repo roles
- the stable set contains `2` CN files and `3` English files, each already marked as current usable versions
- the same directory also keeps `5` history copies, but the README already classifies them as retained history rather than stable entry

## 四分流裁决

- absorbed now:
  - stable entry contract for `A2` cutpack under `GROUP_06`
  - manifest-tracked stable cutpack payload
- reopen later:
  - history-only copies in the same `01_A2_cutpack_v2_final` directory
- future bucket:
  - any deeper field-level quantization beyond this stable-layer intake
- source-only for this cut:
  - `01_A2_cutpack_v2`
  - legacy files inside `01_A2_cutpack_v2_final` that are explicitly marked as history-only

## 裁决

- `Batch 9D` should contain only the stable entry contract and the `5` stable cutpack files
- do not mix the `5` history copies listed in `README_放这里.md`
- do not mix the older `01_A2_cutpack_v2` directory
- do not reopen already committed `Batch 9C`

## 9D 后预期结果

- `GROUP_06` will have both its entry layer and stable cutpack layer committed
- the remaining `GROUP_06` residue will become a much cleaner archive/history-only lane
- next likely cut after `9D`:
  - `Batch 9E = GROUP_06 cutpack history residue`
