# Batch 32 - SOURCE_LIBRARY Batch9 batch9_sources_kimi retirement layer - EVAL - 2026-06-24

## 目标

- land a clean sublane retirement cut inside `01_外部公开指标资料_Batch9`
- keep this batch limited to `batch9_sources_kimi` deletion-only paths plus the batch docs/scripts

## 范围

- target root:
  - `10_来源库_SOURCE_LIBRARY/01_外部公开指标资料_Batch9`
- target subtree in this cut:
  - `10_来源库_SOURCE_LIBRARY/01_外部公开指标资料_Batch9/batch9_sources_kimi`
- excluded in this cut:
  - `N01_波动率状态机`
  - `N03_市场结构_突破质量_条件收集`
  - any other Batch9 subfolders outside `batch9_sources_kimi`

## 阅读结果

- after `Batch 29-31`, Batch9 remaining deletions are `31`, with a clean sublane boundary:
  - `batch9_sources_kimi = 9`
- this sublane can be retired without mixing `N01` or `N03` folder retirements

## 裁决

- `Batch 32` should contain only the `batch9_sources_kimi` retirement deletions plus the batch docs/scripts
- do not mix `N01/N03` folder retirements into this cut

