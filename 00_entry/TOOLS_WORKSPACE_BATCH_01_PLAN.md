# Tools Workspace Batch 01 Plan

## 批次目标

- 先把旧 `tools` 中仍有明确复用价值的通用脚本迁入新仓库。
- 本批只收“小而通用”的脚本，不把一次性历史脚本整批带进来。

## 本批范围

- 旧位置：
  - `旧仓库\tools\`
- 首批候选：
  - `generate_p0_subset.py`
  - `relocate_path_prefix.py`
  - `slice_csv_tail_v1.py`
  - `tk_manual_append_rows.py`

## 本批判断原则

- 必须能清楚说明输入、输出和职责。
- 必须不是只服务一次性历史清理的脚本。
- 必须对新仓库后续整理、裁剪、路径迁移或手工补行仍有价值。

## 本批验收

- `20_tools_workspace` 至少形成一份首批回顾。
- 至少迁入 3 到 4 个高复用通用脚本。
- 明确哪些 `tools` 脚本仍暂留旧仓库，后续再分批处理。
