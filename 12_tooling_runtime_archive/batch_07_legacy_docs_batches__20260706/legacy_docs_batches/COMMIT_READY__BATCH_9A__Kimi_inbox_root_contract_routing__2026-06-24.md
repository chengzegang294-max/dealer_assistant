# Commit Ready Batch 9A - Kimi inbox root contract routing - 2026-06-24

## Goal

- stage the cleanest first cut inside `01_Kimi拆书待入库`
- keep this pack limited to the durable root contract and routing files
- avoid mixing group body trees or audit residue into the opening commit of `Batch 9`

## Exact Files To Stage

- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/README_放这里.md`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/Kimi拆书待入库_批次检查_v1.md`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/CUT_CONTRACT__Kimi_保留型切割_v2.md`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/CUT_CONTRACT__Kimi_全文保留优先_v1.md`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_05_GROUP_06_统一吸收壳_v1.md`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_05_GROUP_06_首批可吸收清单_v1.md`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_06_to_N02_对象候选清单_v1.md`
- `docs/BATCH_9A__Kimi_inbox_root_contract_routing__EVAL__2026-06-24.md`
- `docs/COMMIT_READY__BATCH_9A__Kimi_inbox_root_contract_routing__2026-06-24.md`
- `docs/commit_ready_batch_9A__kimi_inbox_root_contract_routing__paths.txt`
- `docs/commit_ready_stage_batch_9A__kimi_inbox_root_contract_routing__2026-06-24.ps1`

## Included In This Pack

- inbox root `README`
- root-level batch inspection and group priority file
- two Kimi cut contracts
- `GROUP_05 / GROUP_06` cross-group absorb shell and absorb list
- `GROUP_06 -> N02` object candidate routing file

## Excluded In This Pack

- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/PANEL__*`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_DUP_*`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_stage_proof__01_集合竞价教程__v1.tsv`
- all `GROUP_01 ~ GROUP_07` directories

## Suggested Commit Message

- `docs: add Batch 9A Kimi inbox root contract routing`

## Stage Command

- use:
  - `docs/commit_ready_stage_batch_9A__kimi_inbox_root_contract_routing__2026-06-24.ps1`
  - `docs/commit_ready_batch_9A__kimi_inbox_root_contract_routing__paths.txt`
