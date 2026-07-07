# Batch 9A - Kimi inbox root contract routing - EVAL - 2026-06-24

## Goal

- open `Batch 9 = 01_Kimi拆书待入库` with the cleanest possible first cut
- commit only the durable root-layer contract and routing files
- keep large group trees and audit residue out of the first knife

## Scope

- target root:
  - `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库`
- current visible residue in this lane:
  - `?? 19`
- first-cut target:
  - `7` root-level `md` files

## Read Result

- `README_放这里.md` defines the root directory contract for the whole inbox lane
- `Kimi拆书待入库_批次检查_v1.md` already gives directory-level batch verdicts and group priorities
- `CUT_CONTRACT__Kimi_保留型切割_v2.md` and `CUT_CONTRACT__Kimi_全文保留优先_v1.md` are stable intake contracts
- `GROUP_05_GROUP_06_统一吸收壳_v1.md`
- `GROUP_05_GROUP_06_首批可吸收清单_v1.md`
- `GROUP_06_to_N02_对象候选清单_v1.md`
  together form the cross-group routing layer from inbox notes into later source-library reopen candidates

## Split Decision

- `Batch 9A = root contract + routing layer`
  - `README_放这里.md`
  - `Kimi拆书待入库_批次检查_v1.md`
  - `CUT_CONTRACT__Kimi_保留型切割_v2.md`
  - `CUT_CONTRACT__Kimi_全文保留优先_v1.md`
  - `GROUP_05_GROUP_06_统一吸收壳_v1.md`
  - `GROUP_05_GROUP_06_首批可吸收清单_v1.md`
  - `GROUP_06_to_N02_对象候选清单_v1.md`
- hold out of `9A`:
  - `PANEL__*`
  - `S_DUP_*`
  - `S_BUCKET_stage_proof__01_集合竞价教程__v1.tsv`
  - all `GROUP_01 ~ GROUP_07` directories

## Four-Way Verdict

- 已吸收:
  - root-layer inbox contract
  - root-layer batch routing
  - `GROUP_05 / GROUP_06 -> N02` crosswalk entry
- 可重开:
  - `GROUP_05`
  - `GROUP_06`
  - later audit residue pack from root layer
- future bucket:
  - `GROUP_02`
  - `GROUP_03`
- 仅来源库保留:
  - `GROUP_07`
  - current audit traces until staged separately

## Why This Is The Cleanest First Knife

- all files are pure text
- all files sit at the root of the inbox lane
- all files define durable structure rather than transient execution evidence
- no group tree body is mixed into the first commit

## Expected Result After 9A

- `01_Kimi拆书待入库` residue narrows from mixed root + group trees into:
  - root audit residue
  - group trees
- next likely cut:
  - `Batch 9B = root audit residue`
