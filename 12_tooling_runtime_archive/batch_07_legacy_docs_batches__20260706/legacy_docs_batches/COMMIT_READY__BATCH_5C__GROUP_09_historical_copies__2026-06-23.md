# 提交就绪批次 5C - GROUP_09 historical copies - 2026-06-23

## 目标

- commit the historical-copy layer of `GROUP_09` as archive/history evidence
- preserve lineage without confusing it with stable entry

## 精确暂存文件

- root historical loose files:
  - `CUTPACK__A4__*.md`
- historical directories:
  - `01_A1_cutpack_v2/`
  - `02_A3C1_cutpack_v2/`
- expected source file count:
  - `19`

## 建议提交信息

- `docs: add GROUP_09 historical cutpack copies as archive layer`

## 边界

- this batch is history-only
- these files are not current stable entry
- stable entry remains:
  - root `README_放这里.md`
  - root `manifest_v2.tsv`
  - four `*_final` trees

## 暂存命令

- use:
  - `docs/commit_ready_stage_batch_5C__GROUP_09_historical_copies__2026-06-23.ps1`
  - `docs/commit_ready_batch_5C__GROUP_09_historical_copies__paths.txt`
