# 来源库下一批次选择 2026-06-23

## 目标

- Select the next source-library directory from the current remaining backlog.
- Make the choice from the total-ledger layer instead of drifting back into already completed `GROUP_08 / GROUP_09 / GROUP_10`.
- Keep the selection auditable against the latest repository snapshot.

## 当前快照

- latest repository-wide visible status:
  - `M = 0`
  - `D = 42`
  - `?? = 2`
- latest source-library visible status:
  - `D = 42`
- source-library top-level backlog split:
  - `01_外部公开指标资料_Batch9 D 11`
  - `02_外部视频与方法论参考 D 31`
  - `01_Kimi拆书待入库` committed and closed as truth lane
  - `03_Kimi拆书待入库` retirement lane closed (`Batch 24-28`)

## 选择规则

- Prefer the smallest directory that can form a clean, reviewable next batch.
- Prefer a directory whose edge is mostly text truth rather than mixed exports plus migration residue.
- Avoid reopening a directory whose current visible status is mostly legacy migration evidence rather than new incoming truth.
- Keep the lone modified tracked file under separate manual review even if the surrounding directory becomes the next batch.

## 候选复核

### Candidate A - `03_Kimi拆书待入库`

- current visible status:
  - `D = 0`
- strengths:
  - `Batch 24` removed the old-root retirement layer as a clean first cut
  - `Batch 25` removed the dominant `GROUP_08` old-tree retirement slice
  - `Batch 26` removed the `GROUP_09` old-tree retirement slice
  - `Batch 27-28` closed the remaining residue (`GROUP_06` + small fragments)
  - the lane is now fully closed and should not occupy the next-batch slot
  - the lane is already classified in backlog as `真实迁移 / relayout`, not accidental loss
- risks:
  - none inside this lane after closure
- current verdict:
  - closed
  - not a next-batch candidate

### Candidate A1 - `01_外部公开指标资料_Batch9`

- current visible status:
  - `D = 11`
- strengths:
  - it is the dominant remaining deletion cluster in the source-library backlog after closing the `03_Kimi` retirement lane
  - it can be split into clean staged cuts using exact-path lists
- risks:
  - it likely needs multiple sub-batches; avoid bulk staging
- current verdict:
  - current main lane

### Candidate A1a - `01_外部公开指标资料_Batch9/N03_市场结构_突破质量_条件收集`

- current visible status:
  - `D = 0`
- strengths:
  - the only remaining folder-sized retirement slice under Batch9 after `Batch 33`
  - can be audited as a clean final Batch9 deletion cut
- current verdict:
  - completed in `Batch 34` and no longer a next-cut candidate

### Candidate B - `00_外部公开资料与方法论参考`

- current visible status:
  - completed through `Batch 8D`
- strengths:
  - no longer blocks next-batch selection
  - fully absorbed with auditable sub-batch boundaries
- risks:
  - should not be reopened immediately after:
    - `Batch 8A`
    - `Batch 8B`
    - `Batch 8C`
    - `Batch 8D`
- current verdict:
  - `Priority 2`
  - now part of completed ledger rather than candidate list

### Candidate C - `02_原子化拆解文件`

- current visible status:
  - completed in `Batch 7`
- strengths:
  - no longer blocks the next-directory decision
- risks:
  - should not be reopened immediately after:
    - `Batch 7A`
    - `Batch 7B`
    - `Batch 7C`
- current verdict:
  - `Priority 3`
  - now part of completed ledger rather than candidate list

## 建议裁决

- Treat `Batch 7 = 02_原子化拆解文件` as closed and completed.
- Treat `Batch 8 = 10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考` as closed and completed.
- Treat `Batch 8A = NFTRADEZ export text layer` as completed and committed.
- Treat `Batch 8B = NFTRADEZ KIMI contract residue` as completed and committed.
- Treat `Batch 8C = Batch9 full tree` as completed and committed.
- Treat `Batch 8D = Smile_SMC trace layer` as completed and committed.
- Treat `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库` as completed and committed, not the next-batch candidate.
- Treat `Batch 24 = SOURCE_LIBRARY 03_Kimi old root retirement layer` as completed and committed.
- Treat `Batch 25 = SOURCE_LIBRARY 03_Kimi GROUP_08 old-tree retirement layer` as completed and committed.
- Treat `Batch 26 = SOURCE_LIBRARY 03_Kimi GROUP_09 old-tree retirement layer` as completed and committed.
- Treat `Batch 27-28` as completed and committed, and treat `03_Kimi拆书待入库` as closed retirement lane.
- Select `10_来源库_SOURCE_LIBRARY\01_外部公开指标资料_Batch9` as the next main source-library lane.
- Treat `Batch 29 = Batch9 root contracts/lists retirement layer` as completed and committed.
- Treat `Batch 30 = Batch9 Ashare todo README retirement layer` as completed and committed.
- Treat `Batch 31 = Batch9 N02 session/orb retirement layer` as completed and committed.
- Treat `Batch 32 = Batch9 batch9_sources_kimi retirement layer` as completed and committed.
- Treat `Batch 33 = Batch9 N01 volatility regimes retirement layer` as completed and committed.
- Treat `Batch 34 = Batch9 N03 market structure breakout quality conditions retirement layer` as completed and committed, and treat Batch9 as closed retirement lane.
- Treat `Batch 9A = Kimi inbox root contract routing` as completed and committed.
- Treat `Batch 9B = Kimi inbox root audit residue` as completed and committed.
- Treat `Batch 9C = GROUP_06 entry layer` as completed and committed.
- Treat `Batch 9D = GROUP_06 cutpack stable layer` as completed and committed.
- Treat `Batch 9E = GROUP_06 cutpack history residue` as completed and committed.
- Treat `Batch 9F = GROUP_06 legacy v2 pack` as completed and committed.
- Treat `Batch 10 = GROUP_05 entry layer` as completed and committed.
- Treat `Batch 10A = GROUP_05 cutpack stable layer` as completed and committed.
- Treat `Batch 11 = GROUP_01 entry layer` as completed and committed.
- Treat `Batch 11A = GROUP_01 cutpack stable layer` as completed and committed.
- Treat `Batch 12 = GROUP_02 entry layer` as completed and committed.
- Treat `Batch 13 = GROUP_03 entry layer` as completed and committed.
- Treat `Batch 14 = GROUP_04 entry layer` as completed and committed.
- Treat `Batch 15 = GROUP_07 entry layer` as completed and committed.

## 为何这是最顺的一步

- `Batch 8` is now fully closed, so there is no value in staying inside the method-reference lane.
- the already committed `01_Kimi拆书待入库/GROUP_08 / GROUP_09 / GROUP_10` truth trees are complete enough under the fixed entry/body/archive pattern.
- `02_原子化拆解文件` and `00_外部公开资料与方法论参考` are both now completed ledger items.
- The smoothest next move is therefore to shift from the now-closed `01_Kimi拆书待入库` truth lane to the remaining migration-retirement lane under `03_Kimi拆书待入库`.
- The smoothest next move is therefore to shift away from the now-closed `03_Kimi拆书待入库` lane to the remaining deletion-heavy source-library backlog under `01_外部公开指标资料_Batch9`.

## 下一动作合同

- Next batch target:
  - `10_来源库_SOURCE_LIBRARY`
- current next cut:
  - pause Batch9 lane: no remaining deletions under `01_外部公开指标资料_Batch9`
- do not mix:
  - old-root deletions already committed in `Batch 24`
  - `GROUP_08` old-tree retirement already committed in `Batch 25`
  - `GROUP_09` old-tree retirement already committed in `Batch 26`
  - `GROUP_06` old-tree retirement already committed in `Batch 27`
  - `03_Kimi` small fragments already committed in `Batch 28`
  - already committed `Batch 9A`
  - already committed `Batch 9B`
  - already committed `Batch 9C`
  - already committed `Batch 9D`
  - already committed `Batch 9E`
  - already committed `Batch 9F`
  - already committed `Batch 10`
  - already committed `Batch 10A`
  - `GROUP_06` root entry files already landed in `9C`
  - `GROUP_06` stable cutpack files already landed in `9D`
  - `GROUP_06` history-only files already landed in `9E`
  - `GROUP_06` legacy `v2` pack already landed in `9F`
  - `GROUP_05` root entry files already landed in `10`
  - `GROUP_05` stable cutpack files already landed in `10A`
  - `GROUP_01` root master files already landed in `11`
  - `GROUP_01` stable cutpack files already landed in `11A`
  - `GROUP_02` root master files already landed in `12`
  - `GROUP_03` root master files already landed in `13`
  - `GROUP_04` root master files already landed in `14`
  - `GROUP_07` root index file already landed in `15`
  - unrelated deletion clusters outside the closed Batch9 lane
  - any completed `Batch 8A / 8B / 8C / 8D` files
  - already completed `01_Kimi拆书待入库/GROUP_08 / GROUP_09 / GROUP_10` truth trees
  - already completed `Batch 7`
  - already committed `Batch 8A`
  - already committed `Batch 8B`
  - already committed `Batch 8C`
  - already committed `Batch 8D`

## 同步目标

- completed-range anchor:
  - `docs/SOURCE_LIBRARY_COMPLETED_BATCH_INDEX__2026-06-23.md`
- batch-order contract:
  - `docs/SOURCE_LIBRARY_BACKLOG__staged_commit_ready_plan__2026-06-23.md`
- source-control triage contract:
  - `docs/SOURCE_CONTROL_BACKLOG_TRIAGE__2026-06-23.md`
- main docs to sync:
  - `01_阶段一_项目记录_过去与落地.md`
  - `02_阶段二_工作方向_想法库.md`
  - `03_阶段二_当下计划_执行清单.md`
  - `关于日活.md`
