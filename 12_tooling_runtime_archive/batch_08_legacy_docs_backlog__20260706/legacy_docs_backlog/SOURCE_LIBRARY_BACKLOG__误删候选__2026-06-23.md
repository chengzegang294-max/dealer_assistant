# Source Library Backlog 2026-06-23 - 误删候选

## Scope

- Repository root: `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis`
- Audit target: `10_来源库_SOURCE_LIBRARY`
- This sheet only keeps deletion items that still look like `可能误删 / possible loss`.

## Current Verdict

- After the path audit in this round, there is currently `no directory-level confirmed misdelete cluster` inside the `334` deletions.
- The three clusters that previously looked suspicious are now reclassified:
  - `03_Kimi拆书待入库` -> moved to `来源层真实迁移`
  - `01_外部公开指标资料_Batch9` -> moved to `来源层真实迁移`
  - `Smile_SMC交易系统2_0` -> moved to `来源层真实迁移`
- Current bucket size:
  - active directory clusters: `0`

## Residual Hold Items

- `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_08_A股量化_数据研究`
  - `GROUP_08_external_ops_stats_v1.md` records `delete_candidate_rows = 8`
  - current meaning:
    - these are `planned final cleanup candidates` inside the new tree
    - they are not evidence that the source was lost
  - current action:
    - keep them under reference-cleanup review
    - do not reclassify as accidental deletion unless the new-tree counterpart disappears
- `10_来源库_SOURCE_LIBRARY\02_原子化拆解文件\核心技术_威科夫_弹簧Spring与上抛UT量化判定.md`
  - status is `M`, not `D`
  - it still needs manual review, but it does not belong to the deletion bucket

## Reclassification Rule

- Only keep an item here if both conditions hold:
  - the old path was deleted
  - no current tracked or untracked truth counterpart can be found
- If the current counterpart exists, move it to `来源层真实迁移`.
- If the item is a new truth-layer file or a modified tracked file, move it to `新增真值文件` or a separate manual-review note.

## Current Action

- Keep this sheet intentionally small.
- Do not invent a misdelete bucket just to fill all three categories.
- Re-open this sheet only when a deleted path cannot be explained by:
  - a tracked current root
  - an untracked incoming truth file
  - an already-audited migration ledger
