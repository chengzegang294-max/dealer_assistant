# 批次 31 - SOURCE_LIBRARY Batch9 N02 session/orb retirement layer - 评估 - 2026-06-24

## 目标

- land the smallest folder-sized retirement cut remaining under `01_外部公开指标资料_Batch9`
- keep this batch limited to `N02_时段_开盘区间结构` deletion-only paths plus the batch docs/scripts

## 范围

- target root:
  - `10_来源库_SOURCE_LIBRARY/01_外部公开指标资料_Batch9`
- target subtree in this cut:
  - `10_来源库_SOURCE_LIBRARY/01_外部公开指标资料_Batch9/N02_时段_开盘区间结构`
- excluded in this cut:
  - `N01_波动率状态机`
  - `N03_市场结构_突破质量_条件收集`
  - `batch9_sources_kimi/**`

## 阅读结果

- after `Batch 29-30`, Batch9 remaining deletions are grouped by subfolders
- `N02_时段_开盘区间结构 = 7` is the smallest folder-sized slice, so it is the cleanest next standalone cut

## 裁决

- `Batch 31` should contain only the `N02_时段_开盘区间结构` retirement deletions plus the batch docs/scripts
- do not mix `N01/N03` or `batch9_sources_kimi` into this cut

