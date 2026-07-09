# 提交就绪批次 6B1 - GROUP_10 stable body - 2026-06-23

## 目标

- commit the stable text body of `01_A5_cutpack_v1_final/`
- exclude `.tmp_*.json` auxiliary traces

## 精确暂存文件

- subtree:
  - `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_10_A5_财报_估值_组合管理/01_A5_cutpack_v1_final/`
- include:
  - all non-`.tmp_*.json` files
- expected source file count:
  - `109`

## 建议提交信息

- `docs: add GROUP_10 stable cutpack body`

## 显式排除项

- `Active_Portfolio_Management/.tmp_chapter_boundaries.json`
- `财务报表分析与股票估值_郭永清/.tmp_chapter_map.json`
- `财务报表分析与股票估值_郭永清/.tmp_chapter_map2.json`

## 暂存命令

- use:
  - `docs/commit_ready_stage_batch_6B1__GROUP_10_stable_body__2026-06-23.ps1`
  - `docs/commit_ready_batch_6B1__GROUP_10_stable_body__paths.txt`
