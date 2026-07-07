# Commit Ready Batch 7B - Spring UT object entry upgrade - 2026-06-23

## Goal

- commit the tracked `Spring / UT` file as a standalone follow-up batch
- keep this batch separate from `Batch 7A`
- preserve the new `DIAG_ONLY` object-entry and minimal-contract append

## Exact Files To Stage

- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/核心技术_威科夫_弹簧Spring与上抛UT量化判定.md`
- `docs/COMMIT_READY__BATCH_7B__Spring_UT_object_entry_upgrade__2026-06-23.md`
- `docs/commit_ready_batch_7B__spring_ut_object_entry__paths.txt`
- `docs/commit_ready_stage_batch_7B__spring_ut_object_entry__2026-06-23.ps1`

## Why Separate

- `Batch 7A` was intentionally limited to the `18` untracked files
- this file is a tracked modification and therefore deserves its own review/commit boundary

## Suggested Commit Message

- `docs: upgrade Spring UT object entry contract`

## Stage Command

- use:
  - `docs/commit_ready_stage_batch_7B__spring_ut_object_entry__2026-06-23.ps1`
  - `docs/commit_ready_batch_7B__spring_ut_object_entry__paths.txt`
