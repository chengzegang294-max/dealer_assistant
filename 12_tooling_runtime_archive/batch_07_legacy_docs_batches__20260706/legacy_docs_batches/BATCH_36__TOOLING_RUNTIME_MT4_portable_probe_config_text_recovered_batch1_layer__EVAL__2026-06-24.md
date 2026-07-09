# Batch 36 - TOOLING_RUNTIME MT4 portable probe config text recovered batch1 layer - EVAL - 2026-06-24

## 目标

- land the recovered MT4 portable probe config text pack as a small auditable batch
- keep this batch limited to `00_text_recovered_batch1` plus the batch docs/scripts

## 范围

- target root:
  - `12_工具运行时_TOOLING_RUNTIME/03_MT4便携探针实例/config`
- target subtree in this cut:
  - `12_工具运行时_TOOLING_RUNTIME/03_MT4便携探针实例/config/00_text_recovered_batch1`
- excluded in this cut:
  - any `10_来源库_SOURCE_LIBRARY` paths
  - any unrelated TOOLING_RUNTIME artifacts outside `00_text_recovered_batch1`

## 裁决

- `Batch 36` should contain only the recovered text files plus the batch docs/scripts
