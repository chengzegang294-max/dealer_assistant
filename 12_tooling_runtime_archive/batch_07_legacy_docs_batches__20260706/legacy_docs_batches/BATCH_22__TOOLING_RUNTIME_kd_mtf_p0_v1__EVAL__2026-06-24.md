# Batch 22 - TOOLING_RUNTIME kd_mtf_p0_v1 - EVAL - 2026-06-24

## 目标

- land the `kd_mtf_p0_v1` runtime snapshot as auditable runtime-prep evidence
- keep the batch limited to the whole snapshot directory plus batch docs/scripts

## 范围

- target root:
  - `12_工具运行时_TOOLING_RUNTIME/kd_mtf_p0_v1`

## 阅读结果

- the directory does not expose a standalone `min_contract` file like `pv_corr` / `rsj`
- the directory already contains the runtime-prep audit chain:
  - runtime notes
  - append protocol / acceptance / stub
  - proof input-output samples
  - runtime csv / header / params template
  - real input mapping draft and runtime gaps notes
- the current notes explicitly say the pack is not an execution-layer integration and not a finished live-chain proof

## 四分流裁决

- absorbed now:
  - the whole `kd_mtf_p0_v1` runtime snapshot directory
- reopen later:
  - only if a future `v2` snapshot or a true broker-chain reconstruction pack is created
- future bucket:
  - any execution-layer, broker-chain, or trading-gate integration outside this runtime pack
- source-only for this cut:
  - ignored local cache files such as `__pycache__`

## 裁决

- `Batch 22` should contain the full `kd_mtf_p0_v1` directory plus the batch docs/scripts
- do not split out only one markdown contract surrogate, because the current audit meaning lives across the whole directory
- do not mix any other runtime snapshot or the large `03_Kimi拆书待入库` deletion cluster into this cut
