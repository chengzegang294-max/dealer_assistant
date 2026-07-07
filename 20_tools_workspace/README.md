# Tools Workspace

## 用途

- 这里放从旧 `tools` 中迁入后仍要继续维护的工具脚本。
- 目标是把“长期会复用的工具”和“一次性历史脚本”分开。

## 迁入原则

- 只迁仍有明确输入输出合同的工具
- 只迁仍会继续维护和复用的工具
- 迁入时必须写清：
  - 原路径
  - 当前用途
  - 维护对象

## 当前批次

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

## 不直接迁入

- 一次性清理脚本
- 没有后续维护需求的历史脚本
- 无法说明职责边界的工具副本
