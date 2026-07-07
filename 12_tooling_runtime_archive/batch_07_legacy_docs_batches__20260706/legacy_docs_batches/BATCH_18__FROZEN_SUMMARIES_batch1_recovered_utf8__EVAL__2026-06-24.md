# Batch 18 - FROZEN_SUMMARIES batch1 recovered utf8 - EVAL - 2026-06-24

## Goal

- land the `batch1 recovered utf8` backup pack as a frozen audit reference
- keep it strictly inside the frozen summaries layer

## Scope

- target root:
  - `11_冻结总结层_FROZEN_SUMMARIES/99_活跃主文档损坏前备份_20260611_planb_pre_rebuild/00_batch1_recovered_utf8`
- target files:
  - `README_batch1.md`
  - `COMPARE_NOTES_round1.md`
  - `01_阶段一_项目记录_过去与落地_best_effort_gb18030.md`
  - `01_阶段一_项目记录_过去与落地_current_truth_anchor.md`
  - `02_阶段二_工作方向_想法库_best_effort_gb18030.md`
  - `02_阶段二_工作方向_想法库_current_truth_anchor.md`
  - `03_阶段二_当下计划_执行清单_best_effort_gb18030.md`
  - `03_阶段二_当下计划_执行清单_current_truth_anchor.md`
  - `关于日活_best_effort_gb18030.md`
  - `关于日活_current_truth_anchor.md`

## Read Result

- this pack is explicitly a backup + comparison aid:
  - best-effort reverse decode for damaged mojibake text
  - current truth anchor copies for side-by-side comparison
  - notes to explain irrecoverable loss cases
- it should not replace the current active main docs; it stays as frozen evidence

## Four-Way Verdict

- absorbed now:
  - the full `00_batch1_recovered_utf8` pack
- reopen later:
  - none
- future bucket:
  - only add new recovered packs when new damaged backups are discovered
- source-only for this cut:
  - none

## Decision

- `Batch 18` should contain the whole recovered pack plus the batch docs/scripts
- do not mix runtime snapshots or the large `03_Kimi拆书待入库` deletion cluster into this batch
