# 批次 30 - SOURCE_LIBRARY Batch9 Ashare todo README retirement layer - 评估 - 2026-06-24

## 目标

- land the smallest isolated subfolder cleanup under `01_外部公开指标资料_Batch9` after `Batch 29`
- keep this cut limited to the `A股指标整理区_待整理_N04_N05_N06/README.md` retirement plus the batch docs/scripts

## 范围

- target path:
  - `10_来源库_SOURCE_LIBRARY/01_外部公开指标资料_Batch9/A股指标整理区_待整理_N04_N05_N06/README.md`
- excluded in this cut:
  - `N01_波动率状态机`
  - `N02_时段_开盘区间结构`
  - `N03_市场结构_突破质量_条件收集`
  - `batch9_sources_kimi/**`

## 阅读结果

- this is a single-file deletion slice, so it can be committed as a tiny standalone batch without reopening any deeper Batch9 material
- keeping this micro-cut isolated reduces noise in the next folder-sized retirement batches (`N01/N02/N03`)

## 裁决

- `Batch 30` should contain only this one deletion path plus the batch docs/scripts

