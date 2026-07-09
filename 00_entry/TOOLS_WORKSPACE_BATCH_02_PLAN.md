# Tools Workspace Batch 02 Plan

## 批次目标

- 继续把旧 `tools` 中成体系、仍有长期整理价值的专题工具迁入新仓库。
- 本批专注 `group08` 外部材料整理流水线，不混入其他家族。

## 本批范围

- 旧位置：
  - `旧仓库\tools\`
- 首批候选：
  - `group08_generate_external_ops_plan.py`
  - `group08_external_ops_preflight.py`
  - `group08_generate_materials_catalog.py`
  - `group08_generate_powershell_dryrun_cmds.py`
  - `group08_external_move_postcheck.py`
  - `group08_external_ops_stats.py`

## 本批判断原则

- 必须共同构成一条完整整理流水线。
- 必须能说明它们在“计划 -> 预检 -> 目录 -> dry-run -> 后检 -> 统计”中的位置。
- 不把 `group08` 的所有一次性脚本全部混入，只先迁最稳定的一段主链。

## 本批验收

- `20_tools_workspace` 至少形成一份第二批回顾。
- 至少迁入一组可独立阅读的 `group08` 主流水线脚本。
