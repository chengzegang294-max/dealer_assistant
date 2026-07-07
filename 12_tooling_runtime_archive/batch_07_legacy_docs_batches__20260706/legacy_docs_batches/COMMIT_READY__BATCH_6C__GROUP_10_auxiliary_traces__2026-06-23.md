# Commit Ready Batch 6C - GROUP_10 auxiliary traces - 2026-06-23

## Goal

- commit the auxiliary split-trace files of `GROUP_10` separately
- preserve lineage without mixing them into stable body

## Exact Files To Stage

- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_10_A5_财报_估值_组合管理/01_A5_cutpack_v1_final/Active_Portfolio_Management/.tmp_chapter_boundaries.json`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_10_A5_财报_估值_组合管理/01_A5_cutpack_v1_final/财务报表分析与股票估值_郭永清/.tmp_chapter_map.json`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_10_A5_财报_估值_组合管理/01_A5_cutpack_v1_final/财务报表分析与股票估值_郭永清/.tmp_chapter_map2.json`

## Suggested Commit Message

- `docs: add GROUP_10 auxiliary split traces`

## Boundary

- these files are not stable entry
- these files are not stable text body
- these files are kept as auxiliary trace layer only

## Stage Command

- use:
  - `docs/commit_ready_stage_batch_6C__GROUP_10_auxiliary_traces__2026-06-23.ps1`
  - `docs/commit_ready_batch_6C__GROUP_10_auxiliary_traces__paths.txt`
