## Frozen Summaries Raw Snapshot (Batch09)

### 用途

- 这里保留旧 `11_冻结总结层_FROZEN_SUMMARIES` 的 batch09 原样快照工作区。
- 当前只承担历史回收与待筛选中转作用，不作为默认阅读入口。

### 当前状态

- 当前落点：`11_frozen_summaries_archive/_raw_snapshot_batch09`
- 历史来源：`12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_trading_analysis/11_冻结总结层_FROZEN_SUMMARIES`
- 当前仍按 `raw snapshot / waiting for selection` 口径保留，尚未整体提升为批次级可读归档包。

### 当前边界

- 后续需要先做去乱码、去重复与价值判断，再按批次迁入 `11_frozen_summaries_archive/<batch>/` 可读归档层。
- 在完成筛选前，不把本目录当作 repo 内默认冻结总结入口。
