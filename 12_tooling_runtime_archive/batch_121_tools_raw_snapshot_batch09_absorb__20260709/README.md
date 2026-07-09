# Batch 121 Tools Raw Snapshot Batch09 Absorb

## 用途

- 吸收 `20_tools_workspace/_raw_snapshot_batch09` 中整包历史脚本快照。
- 这批文件统一按 `archive_only` 口径归入 tooling runtime archive，不再继续冒充活跃维护层。

## 入口

- `INDEX_NOTE`:
  - 当前文件
  - `BATCH_121_TOOLS_RAW_SNAPSHOT_ABSORB_EXECUTION_CARD__20260709.md`
  - `BATCH_121_TOOLS_RAW_SNAPSHOT_ABSORB_ARTIFACT_INDEX__20260709.tsv`
  - `01_index/tools_raw_snapshot_batch09_family_index_v1.tsv`
  - `02_decision/tools_raw_snapshot_batch09_decision_ledger_v1.tsv`

## 当前口径

- `00_raw_snapshot/tools_raw_snapshot_batch09/` 中的 `.py` 与 `.log` 统一标记为 `historical_recovered`
- 当前作用是保留旧 `tools` 快照、冻结家族裁决，并为未来可能的 reopen 提供索引
- 这批内容不是默认运行入口，只有已单独吸收进入 `20_tools_workspace/batch_*` 的脚本家族才继续视为维护对象
