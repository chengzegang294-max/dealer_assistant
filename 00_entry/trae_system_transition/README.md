# Trae System Transition (Working)

## 用途

- 承接 `21_trae_system_archive` 当前仍参与路由裁决的索引材料的“工作副本”。
- 旧路径继续作为 `legacy archive router` 保持不动，避免打断 `.trae` 的现行三跳规则。

## 当前内容

- `TRAE_SYSTEM_SKILLS_INDEX__20260709.md`
- `TRAE_SYSTEM_SKILLS_GROUP_VIEW__20260709.md`
- `TRAE_SYSTEM_TRANSITION_EXECUTION_CARD__20260709.md`
- `TRAE_SYSTEM_TRANSITION_ARTIFACT_INDEX__20260709.tsv`
- `trae_system_transition_family_index_v1.tsv`
- `promotion_map_v1.tsv`

## 口径

- 本目录属于 `REPO_GLOBAL / WORKING`，用于承接“仓库级治理与迁移中间态”
- 不作为当前 `.trae` first-hop router，避免引入双入口
- 当前 `.trae/` 目录受 `.gitignore` 约束：
  - repo 内可追踪的治理/迁移 working copy 继续以 `00_entry` 与 `21_trae_system_archive` 为准，不把关键回指只写进本地 `.trae` 修改
