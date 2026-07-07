# Commit Ready Batch 5C - GROUP_09 historical copies - 2026-06-23

## Goal

- commit the historical-copy layer of `GROUP_09` as archive/history evidence
- preserve lineage without confusing it with stable entry

## Exact Files To Stage

- root historical loose files:
  - `CUTPACK__A4__*.md`
- historical directories:
  - `01_A1_cutpack_v2/`
  - `02_A3C1_cutpack_v2/`
- expected source file count:
  - `19`

## Suggested Commit Message

- `docs: add GROUP_09 historical cutpack copies as archive layer`

## Boundary

- this batch is history-only
- these files are not current stable entry
- stable entry remains:
  - root `README_放这里.md`
  - root `manifest_v2.tsv`
  - four `*_final` trees

## Stage Command

- use:
  - `docs/commit_ready_stage_batch_5C__GROUP_09_historical_copies__2026-06-23.ps1`
  - `docs/commit_ready_batch_5C__GROUP_09_historical_copies__paths.txt`
