# Tools Workspace Batch 01 Selected

## 用途

- 这里放 `20_tools_workspace` 首批迁入的新通用工具脚本。

## 边界

- 本目录只放工具脚本本体与批次说明，不承载仓库级真值入口。
- 若脚本产出文件：
  - 可复现运行时产物归 `02_runtime/`
  - 大体量工具运行时归档归 `12_tooling_runtime_archive/`
  - 临时中间文件只允许落在本批次目录内且可迁走可删
- 若脚本沉淀出可长期复用的合同/索引/入口说明，必须提升归位到 `00_entry/02_runtime/12_tooling_runtime_archive` 对应层。

## 当前文件

- `generate_p0_subset.py`
- `relocate_path_prefix.py`
- `slice_csv_tail_v1.py`
- `tk_manual_append_rows.py`

## 当前裁决

- 这 4 个脚本都是轻量、通用、可重复使用的工具。
- 更强项目绑定的一次性脚本继续暂留旧仓库，后续按专题另开批次。
