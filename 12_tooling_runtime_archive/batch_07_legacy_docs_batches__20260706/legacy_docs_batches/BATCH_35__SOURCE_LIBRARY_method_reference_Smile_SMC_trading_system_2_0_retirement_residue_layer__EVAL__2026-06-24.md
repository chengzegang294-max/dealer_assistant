# Batch 35 - SOURCE_LIBRARY method reference Smile SMC trading system 2.0 retirement residue layer - EVAL - 2026-06-24

## Goal

- land a clean retirement cut for the remaining `Smile_SMC交易系统2_0` deletion cluster
- keep this batch limited to the `Smile_SMC交易系统2_0` deletion-only paths plus the batch docs/scripts

## Scope

- target root:
  - `10_来源库_SOURCE_LIBRARY/02_外部视频与方法论参考`
- target subtree in this cut:
  - `10_来源库_SOURCE_LIBRARY/02_外部视频与方法论参考/Smile_SMC交易系统2_0`
- excluded in this cut:
  - any paths outside `Smile_SMC交易系统2_0`
  - any `12_工具运行时_TOOLING_RUNTIME` artifacts

## Read Result

- current working tree shows a standalone deletion cluster under `Smile_SMC交易系统2_0`
- it should be retired in one self-contained batch to avoid mixing with other cleanup lanes

## Decision

- `Batch 35` should contain only `Smile_SMC交易系统2_0` retirement deletions plus the batch docs/scripts
