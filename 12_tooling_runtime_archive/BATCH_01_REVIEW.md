# Tooling Runtime 归档批次 01 审查

## 批次结论

- 本批已完成 `12_tooling_runtime_archive` 首批迁入。
- 当前已迁入新仓库的是一套 `cross_line_frozen` 顶层最小冻结链，位置：
  - `12_tooling_runtime_archive\batch_01_selected\cross_line_frozen_min_set\`
- 这批材料是只读运行时锚点，不是活跃对象执行目录。

## 本批迁入文件

- `cross_line_frozen_current_manifest_v1.md`
- `cross_line_frozen_manifest_index_v1.py`
- `cross_line_frozen_manifest_index_v1.md`
- `cross_line_frozen_acceptance_compare_v1.py`
- `cross_line_frozen_acceptance_compare_v1.md`
- `cross_line_frozen_manifest_acceptance_v1.py`
- `cross_line_frozen_manifest_acceptance_v1.md`
- `cross_line_frozen_acceptance_chain_index_v1.py`
- `cross_line_frozen_acceptance_chain_index_v1.md`
- `cross_line_frozen_chain_acceptance_compare_v1.py`
- `cross_line_frozen_chain_acceptance_compare_v1.md`
- `cross_line_frozen_chain_manifest_acceptance_v1.py`
- `cross_line_frozen_chain_manifest_acceptance_v1.md`

## 为什么这批先进

- 它们共同保留了：
  - 当前跨线冻结阶段说明
  - 顶层 manifest index
  - acceptance compare
  - manifest acceptance
  - chain index
  - chain compare
  - chain manifest acceptance
- 这批材料足够说明一条最小冻结链是如何组织和验收的。
- 同时它们体量小、边界清楚，不会把整个旧运行时层一起带乱。

## 本批裁决

- 已吸收：
  - 上述 `cross_line_frozen` 顶层最小冻结链
- 可重开：
  - `cross_line_frozen_super*`
  - 原因：属于长链历史扩展，需要后续按版本层次再处理
- future bucket：
  - `02_MT指标家族_源码与探针`
  - `03_MT4便携探针实例`
  - 各对象运行时子目录
  - 原因：体量大、专题强，不适合混在首批
- 仅旧仓库保留：
  - 无当前归档价值的散乱运行时中间产物

## 当前边界

- 本批不是把旧运行时目录迁完。
- 本批只是先给新仓库放入一套可代表运行时冻结体系的只读锚点。
- 当前活跃对象执行仍在：
  - `02_runtime`

## 下一步建议

1. 单开 `MT 指标家族` 批次
2. 单开 `MT4 便携探针实例` 批次
3. 单开各对象运行时历史材料批次
