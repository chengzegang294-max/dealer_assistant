# Group08 Pipeline Batch 02

## 用途

- 这里放 `group08` 外部材料整理主流水线脚本。

## 边界

- 本目录只放流水线脚本本体与批次说明，不承载仓库级真值入口。
- 若脚本产出文件：
  - 需要长期保留的运行产物归 `12_tooling_runtime_archive/`（并带批次 README / execution card / artifact index）
  - 可复现运行时产物归 `02_runtime/`
  - 临时中间文件只允许落在本批次目录内且可迁走可删
- 若脚本沉淀出可长期复用的合同/索引/入口说明，必须提升归位到 `00_entry/02_runtime/12_tooling_runtime_archive` 对应层。

## 当前文件

- `group08_generate_external_ops_plan.py`
- `group08_external_ops_preflight.py`
- `group08_generate_materials_catalog.py`
- `group08_generate_powershell_dryrun_cmds.py`
- `group08_external_move_postcheck.py`
- `group08_external_ops_stats.py`

## 当前裁决

- 这批脚本共同构成 `group08` 的主流水线。
- 更细的清单同步与专题收尾脚本后续再开批次处理。
