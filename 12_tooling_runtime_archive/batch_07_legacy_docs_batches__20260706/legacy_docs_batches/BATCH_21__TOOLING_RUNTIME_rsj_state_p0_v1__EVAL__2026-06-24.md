# Batch 21 - TOOLING_RUNTIME rsj_state_p0_v1 - EVAL - 2026-06-24

## 目标

- land the `rsj_state_p0_v1` runtime snapshot as auditable `DIAG_ONLY` evidence
- keep the batch limited to the whole snapshot directory plus batch docs/scripts

## 范围

- target root:
  - `12_工具运行时_TOOLING_RUNTIME/rsj_state_p0_v1`

## 阅读结果

- `rsj_state_p0_min_contract_v1.md` explicitly marks the role as `DIAG_ONLY`
- the directory already contains the full audit chain:
  - minimal contract
  - runtime notes
  - append protocol / stub / validation scripts
  - replay / chain summary acceptance docs
  - sample input/output evidence

## 四分流裁决

- absorbed now:
  - the whole `rsj_state_p0_v1` runtime snapshot directory
- reopen later:
  - only if a future `v2` snapshot is created
- future bucket:
  - any execution-layer or strategy integration outside this runtime pack
- source-only for this cut:
  - ignored local cache files such as `__pycache__`

## 裁决

- `Batch 21` should contain the full `rsj_state_p0_v1` directory plus the batch docs/scripts
- do not mix any other runtime snapshot or the large `03_Kimi拆书待入库` deletion cluster into this cut
