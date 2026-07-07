# Source Library Backlog 2026-06-23 - staged commit ready plan

## Goal

- Stop treating `10_来源库_SOURCE_LIBRARY` as one giant cleanup blob.
- Convert remaining backlog into small, reviewable stage batches.
- Keep `真实迁移 / 新增真值 / 单独人工确认` separated.
- Maintain a clean distinction between:
  - completed batches already committed
  - next candidate batch still to be opened

## Ledger Anchors

- completed batch index:
  - `docs/SOURCE_LIBRARY_COMPLETED_BATCH_INDEX__2026-06-23.md`
- next batch selection:
  - `docs/SOURCE_LIBRARY_NEXT_BATCH_SELECTION__2026-06-23.md`
- migration ledger:
  - `docs/SOURCE_LIBRARY_BACKLOG__来源层真实迁移__2026-06-23.md`
- misdelete ledger:
  - `docs/SOURCE_LIBRARY_BACKLOG__误删候选__2026-06-23.md`
- incoming truth ledger:
  - `docs/SOURCE_LIBRARY_BACKLOG__新增真值文件__2026-06-23.md`

## Completed Range

### Batch 1 - docs only

- status:
  - completed and committed
- role:
  - land the interpretation layer first
- commit-ready pack:
  - `docs/COMMIT_READY__BATCH_1__docs_only__2026-06-23.md`
  - `docs/commit_ready_stage_batch_1__docs_only__2026-06-23.ps1`
  - `docs/commit_ready_batch_1__docs_only__paths.txt`

### Batch 2 - NFTRADEZ truth layer only

- status:
  - completed and committed
- role:
  - keep `NFTRADEZ` independently auditable
- commit-ready pack:
  - `docs/COMMIT_READY__BATCH_2__NFTRADEZ_truth_layer__2026-06-23.md`
  - `docs/commit_ready_stage_batch_2__NFTRADEZ_truth_layer__2026-06-23.ps1`
  - `docs/commit_ready_batch_2__NFTRADEZ_truth_layer__paths.txt`

### Batch 3 - S_BUCKET incoming truth

- status:
  - completed and committed
- completed sub-batches:
  - `Batch 3A` = core truth anchors
  - `Batch 3B1` = representatives and proof
  - `Batch 3B2` = `KIMI` contracts
  - `Batch 3C` = derived `S_BUCKET__staging` no-commit decision

### Batch 4 - GROUP_08

- status:
  - completed and committed
- completed sub-batches:
  - `Batch 4A` = manifest-entry layer
  - `Batch 4B1` = text summary pack
  - `Batch 4B2` = txt/md archive pack
  - `Batch 4C` = retained pdf cut pack

### Batch 5 - GROUP_09

- status:
  - completed and committed
- completed sub-batches:
  - `Batch 5A` = entry layer
  - `Batch 5B1` = stable final trees
  - `Batch 5C` = historical copies archive layer

### Batch 6 - GROUP_10

- status:
  - completed and committed
- completed sub-batches:
  - `Batch 6A` = entry layer
  - `Batch 6B1` = stable body
  - `Batch 6C` = auxiliary traces

## Next Open Batch

### Batch 7 - `02_原子化拆解文件`

- status:
  - completed and committed
- source:
  - `10_来源库_SOURCE_LIBRARY\02_原子化拆解文件\`
- completed sub-batches:
  - `Batch 7A` = `18` untracked truth files only
  - `Batch 7B` = `Spring / UT` object-entry contract upgrade
  - `Batch 7C` = auction-rule local evidence anchors
- pack files:
  - `docs/02_原子化拆解文件__EVAL__2026-06-23.md`
  - `docs/BATCH_7__02_原子化拆解文件__M_FILE_REVIEW__2026-06-23.md`
  - `docs/COMMIT_READY__BATCH_7A__02_原子化拆解文件__untracked_truth__2026-06-23.md`
  - `docs/commit_ready_batch_7A__atomic_untracked_truth__paths.txt`
  - `docs/commit_ready_stage_batch_7A__atomic_untracked_truth__2026-06-23.ps1`
  - `docs/COMMIT_READY__BATCH_7B__Spring_UT_object_entry_upgrade__2026-06-23.md`
  - `docs/commit_ready_batch_7B__spring_ut_object_entry__paths.txt`
  - `docs/commit_ready_stage_batch_7B__spring_ut_object_entry__2026-06-23.ps1`
  - `docs/COMMIT_READY__BATCH_7C__auction_rule_local_evidence__2026-06-23.md`
  - `docs/commit_ready_batch_7C__auction_rule_local_evidence__paths.txt`
  - `docs/commit_ready_stage_batch_7C__auction_rule_local_evidence__2026-06-23.ps1`
- completion result:
  - no remaining `??` or `M` under `02_原子化拆解文件`
  - `A股竞价规则` cards now use repo-local source anchors

## Next Open Batch

### Batch 8 - `00_外部公开资料与方法论参考`

- status:
  - closed batch
- source:
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\`
- current visible scope:
  - `0` open residue
- boundary:
  - `Batch 8A` committed the repo-local `NFTRADEZ` export text layer
  - `Batch 8B` committed the repo-local `NFTRADEZ` KIMI contract residue
  - `Batch 8C` committed the full `Batch9` tree
  - `Batch 8D` committed the full `Smile_SMC` trace tree
- completed sub-batches:
  - `Batch 8A` = `NFTRADEZ` export text layer
  - `Batch 8B` = `NFTRADEZ` `KIMI` contract residue
  - `Batch 8C` = `Batch9` full tree
  - `Batch 8D` = `Smile_SMC` trace layer
- next cut:
  - none inside `Batch 8`

## Deferred Candidates

### Closed intake lane - `01_Kimi拆书待入库`

- reason to defer:
  - the root residue is already gone and `GROUP_06` is now fully absorbed
  - the whole lane is now committed as source-library truth and no longer needs a next-cut slot
- latest cut result:
  - `Batch 9A` committed the root contract + routing layer
  - `Batch 9B` committed the root audit residue
  - `Batch 9C` committed the `GROUP_06` entry layer
  - `Batch 9D` committed the `GROUP_06` cutpack stable layer
  - `Batch 9E` committed the `GROUP_06` cutpack history residue
  - `Batch 9F` committed the `GROUP_06` legacy v2 pack
  - `Batch 10` committed the `GROUP_05` entry layer
  - `Batch 10A` committed the `GROUP_05` cutpack stable layer
  - `Batch 11` committed the `GROUP_01` entry layer
  - `Batch 11A` committed the `GROUP_01` cutpack stable layer
  - `Batch 12` committed the `GROUP_02` entry layer
  - `Batch 13` committed the `GROUP_03` entry layer
  - `Batch 14` committed the `GROUP_04` entry layer
  - `Batch 15` committed the `GROUP_07` entry layer
- next cut:
  - none inside `01_Kimi拆书待入库`

### Residual migration lane - `03_Kimi拆书待入库`

- reason to keep open:
  - this lane is not new incoming truth but a large old-path retirement cluster tied to `03_Kimi拆书待入库 -> 01_Kimi拆书待入库`
  - the cleanest first cut was the old-root retirement slice, not the grouped subtrees
- latest cut result:
  - `Batch 24` committed the old-root retirement layer:
    - `13` root-level deletions
    - `4` commit-ready docs/scripts
    - commit `01ba380`
  - `Batch 25` committed the `GROUP_08` old-tree retirement layer:
    - `178` deletion paths under `GROUP_08_A股量化_数据研究`
    - `4` commit-ready docs/scripts
    - commit `0ccae2f`
  - `Batch 26` committed the `GROUP_09` old-tree retirement layer:
    - `21` deletion paths under `GROUP_09_完善体系书库_切割产物`
    - `4` commit-ready docs/scripts
    - commit `1774d60`
  - `Batch 27` committed the `GROUP_06` old-tree retirement layer:
    - `10` deletion paths under `GROUP_06_Auction_MarketProfile_价格行为`
    - `4` commit-ready docs/scripts
    - commit `8b4e27f`
  - `Batch 28` committed the remaining small fragments:
    - `15` deletion paths across `GROUP_01/02/03/04/05/07`
    - `4` commit-ready docs/scripts
    - commit `4a6b285`
- current visible scope:
  - `0` remaining deletions under `03_Kimi拆书待入库`
- next cut:
  - pick the next source-library lane outside `03_Kimi拆书待入库`

### Deletion-heavy lane - `01_外部公开指标资料_Batch9`

- reason to keep open:
  - this lane is a large external-indicator evidence pack and requires strict exact-path staging instead of bulk deletes
  - it contains multiple research subtrees (`N01/N02/N03`) plus a `batch9_sources_kimi` sublane and should be split by folder boundaries
- latest cut result:
  - `Batch 29` committed the Batch9 root contracts/lists retirement slice:
    - `27` root-level deletions
    - `4` commit-ready docs/scripts
    - commit `b2e3aba`
  - `Batch 30` committed the single-file `A股指标整理区_待整理_N04_N05_N06/README.md` retirement slice:
    - `1` deletion path
    - `4` commit-ready docs/scripts
    - commit `e50c954`
  - `Batch 31` committed the `N02_时段_开盘区间结构` folder retirement slice:
    - `7` deletion paths
    - `4` commit-ready docs/scripts
    - commit `d71d39a`
  - `Batch 32` committed the `batch9_sources_kimi` sublane retirement slice:
    - `9` deletion paths
    - `4` commit-ready docs/scripts
    - commit `99e49a2`
  - `Batch 33` committed the `N01_波动率状态机` folder retirement slice:
    - `11` deletion paths
    - `4` commit-ready docs/scripts
    - commit `351f14f`
  - `Batch 34` committed the `N03_市场结构_突破质量_条件收集` folder retirement slice:
    - `11` deletion paths
    - `4` commit-ready docs/scripts
    - commit `fde843b`
- current visible scope:
  - `0` remaining deletions under `01_外部公开指标资料_Batch9`
- next cut:
  - pause Batch9 lane: no remaining deletions to retire

## Do Not Mix

- Do not mix `11_冻结总结层_FROZEN_SUMMARIES` into these batches.
- Do not mix `.trae/skills` or `docs/playbooks` into source-library commits.
- Do not bulk stage all `10_来源库_SOURCE_LIBRARY` files at once.
- Do not treat old-root deletions as cleanup noise.
- Do not reopen `GROUP_08 / GROUP_09 / GROUP_10` as the next main batch after they are already in the completed ledger.

## Current Operator Move

- Treat `Batch 1-6` as completed ledger, not open work.
- Treat `Batch 7 = 02_原子化拆解文件` as completed.
- Treat `Batch 8 = 00_外部公开资料与方法论参考` as fully completed.
- Use `01_外部公开指标资料_Batch9` as the current controlled source-library deletion lane.
- Keep the fixed group split order:
  - entry layer first
  - cutpack stable layer second
  - history residue third when needed
  - legacy pack last when needed
- `01_Kimi拆书待入库` is now fully closed as a source-library truth lane.
- Treat `Batch 24-28` as committed retirement cuts under `03_Kimi拆书待入库`.
- Treat `03_Kimi拆书待入库` as closed retirement lane.
- Treat `Batch 29-34` as committed Batch9 retirement slices, and keep Batch9 lane closed unless new truth inputs appear.
- Keep the four main docs synced to:
  - completed-range summary
  - next batch selection
  - latest source-control snapshot
