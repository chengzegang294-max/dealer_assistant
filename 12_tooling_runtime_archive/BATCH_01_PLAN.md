# Tooling Runtime 归档批次 01 计划

## 批次目标

- 先把旧运行时层中最稳定、最紧凑、最能说明跨线冻结口径的顶层材料迁入新仓库。
- 本批不碰大目录、不碰活跃对象运行时副本，只收 `cross_line_frozen` 顶层最小冻结链。

## 本批范围

- 旧位置：
  - `旧仓库\12_工具运行时_TOOLING_RUNTIME\`
- 首批候选：
  - `cross_line_frozen_current_manifest_v1.md`
  - `cross_line_frozen_manifest_index_v1.py/.md`
  - `cross_line_frozen_acceptance_compare_v1.py/.md`
  - `cross_line_frozen_manifest_acceptance_v1.py/.md`
  - `cross_line_frozen_acceptance_chain_index_v1.py/.md`
  - `cross_line_frozen_chain_acceptance_compare_v1.py/.md`
  - `cross_line_frozen_chain_manifest_acceptance_v1.py/.md`

## 本批判断原则

- 只迁顶层冻结链锚点，不迁 `super...` 长链历史扩展。
- 只迁仍能说明跨线冻结顺序与可接受结论的只读材料。
- 不与 `02_runtime` 中当前活跃对象运行时形成重复维护。

## 本批验收

- `12_tooling_runtime_archive` 至少形成一份首批回顾。
- 至少迁入一套可读、可追溯的 `cross_line_frozen` 最小冻结链。
- 明确哪些运行时大目录继续暂留旧仓库。
