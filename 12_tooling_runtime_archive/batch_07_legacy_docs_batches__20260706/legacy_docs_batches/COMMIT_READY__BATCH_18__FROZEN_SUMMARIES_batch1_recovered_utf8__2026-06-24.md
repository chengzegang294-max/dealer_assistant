# Commit Ready Batch 18 - FROZEN_SUMMARIES batch1 recovered utf8 - 2026-06-24

## Goal

- stage the recovered UTF-8 backup pack as frozen audit evidence
- keep it strictly inside `11_冻结总结层_FROZEN_SUMMARIES`

## Exact Files To Stage

- `11_冻结总结层_FROZEN_SUMMARIES/99_活跃主文档损坏前备份_20260611_planb_pre_rebuild/00_batch1_recovered_utf8/README_batch1.md`
- `11_冻结总结层_FROZEN_SUMMARIES/99_活跃主文档损坏前备份_20260611_planb_pre_rebuild/00_batch1_recovered_utf8/COMPARE_NOTES_round1.md`
- `11_冻结总结层_FROZEN_SUMMARIES/99_活跃主文档损坏前备份_20260611_planb_pre_rebuild/00_batch1_recovered_utf8/01_阶段一_项目记录_过去与落地_best_effort_gb18030.md`
- `11_冻结总结层_FROZEN_SUMMARIES/99_活跃主文档损坏前备份_20260611_planb_pre_rebuild/00_batch1_recovered_utf8/01_阶段一_项目记录_过去与落地_current_truth_anchor.md`
- `11_冻结总结层_FROZEN_SUMMARIES/99_活跃主文档损坏前备份_20260611_planb_pre_rebuild/00_batch1_recovered_utf8/02_阶段二_工作方向_想法库_best_effort_gb18030.md`
- `11_冻结总结层_FROZEN_SUMMARIES/99_活跃主文档损坏前备份_20260611_planb_pre_rebuild/00_batch1_recovered_utf8/02_阶段二_工作方向_想法库_current_truth_anchor.md`
- `11_冻结总结层_FROZEN_SUMMARIES/99_活跃主文档损坏前备份_20260611_planb_pre_rebuild/00_batch1_recovered_utf8/03_阶段二_当下计划_执行清单_best_effort_gb18030.md`
- `11_冻结总结层_FROZEN_SUMMARIES/99_活跃主文档损坏前备份_20260611_planb_pre_rebuild/00_batch1_recovered_utf8/03_阶段二_当下计划_执行清单_current_truth_anchor.md`
- `11_冻结总结层_FROZEN_SUMMARIES/99_活跃主文档损坏前备份_20260611_planb_pre_rebuild/00_batch1_recovered_utf8/关于日活_best_effort_gb18030.md`
- `11_冻结总结层_FROZEN_SUMMARIES/99_活跃主文档损坏前备份_20260611_planb_pre_rebuild/00_batch1_recovered_utf8/关于日活_current_truth_anchor.md`
- `docs/BATCH_18__FROZEN_SUMMARIES_batch1_recovered_utf8__EVAL__2026-06-24.md`
- `docs/COMMIT_READY__BATCH_18__FROZEN_SUMMARIES_batch1_recovered_utf8__2026-06-24.md`
- `docs/commit_ready_batch_18__frozen_summaries_batch1_recovered_utf8__paths.txt`
- `docs/commit_ready_stage_batch_18__frozen_summaries_batch1_recovered_utf8__2026-06-24.ps1`

## Included In This Pack

- recovered best-effort decode backups
- current truth anchor copies for comparison
- comparison notes and README

## Excluded In This Pack

- any active main docs under repo root
- any `12_工具运行时_TOOLING_RUNTIME/**` runtime snapshots
- the large `10_来源库_SOURCE_LIBRARY/03_Kimi拆书待入库/**` deletion cluster

## Suggested Commit Message

- `docs: add Batch 18 FROZEN_SUMMARIES batch1 recovered utf8`

## Stage Command

- use:
  - `docs/commit_ready_stage_batch_18__frozen_summaries_batch1_recovered_utf8__2026-06-24.ps1`
  - `docs/commit_ready_batch_18__frozen_summaries_batch1_recovered_utf8__paths.txt`
