# Tools Workspace

## 用途

- 这里放从旧 `tools` 中迁入后仍要继续维护的工具脚本。
- 目标是把“长期会复用的工具”和“一次性历史脚本”分开。

## 边界

- 本目录是 `工具工作台`，不是仓库级真值入口。
- 工具运行产物默认不落在本目录：
  - 可复现运行时产物归 `02_runtime/`
  - 大体量工具运行时归档归 `12_tooling_runtime_archive/`
- 若某批工具需要暂存中间文件，必须放在对应 `batch_*` 子目录下，并能被迁走或删除。
- 若工具脚本沉淀出可长期复用的合同/索引/入口说明，必须提升归位到对应层：
  - 合同台账与入口卡归 `00_entry/`
  - 可复现运行入口归 `02_runtime/`
  - 历史归档与大体量产物归 `12_tooling_runtime_archive/`

## 迁入原则

- 只迁仍有明确输入输出合同的工具
- 只迁仍会继续维护和复用的工具
- 迁入时必须写清：
  - 原路径
  - 当前用途
  - 维护对象

## 当前批次

- `a5_p0_home_batch1_frontend`
  - A股 P0 首页工作台 Batch1 最小前端实现工作台
- `batch_01_selected`
  - 4 个轻量通用工具
- `batch_02_group08_pipeline`
  - `group08` 主流水线
- `batch_03_general_ingest_tools`
  - `s_bucketize.py`
  - `ingest_ashare_txt_to_md.py`
  - `kimi_cutpack_manifest.py`
- `batch_04_tk_r6_manual_sheet_tools`
  - `tk_r6_make_manual_sheet.py`
  - `tk_r6_summarize_manual_sheet.py`
- `batch_05_tk_r7_manual_sheet_tools`
  - `tk_r7_make_manual_sheet.py`
  - `tk_r7_summarize_manual_sheet.py`
- `batch_06_tk_r8_manual_sheet_tools`
  - `tk_r8_make_manual_sheet.py`
  - `tk_r8_summarize_manual_sheet.py`

## 额外指针

- `_raw_snapshot_batch09`
  - 当前只保留 archive-only 回指入口
  - 整包历史快照已吸收到 `12_tooling_runtime_archive/batch_121_tools_raw_snapshot_batch09_absorb__20260709`

## 不直接迁入

- 一次性清理脚本
- 没有后续维护需求的历史脚本
- 无法说明职责边界的工具副本
