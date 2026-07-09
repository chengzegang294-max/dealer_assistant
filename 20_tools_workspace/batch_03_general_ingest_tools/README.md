# General Ingest Tools Batch 03

## 用途

- 这里放从旧 `tools` 中筛出来、仍有长期复用价值的“通用整理/入库/manifest 工具”。
- 这批不是一次性清理脚本，也不是强绑定旧回测输出的审计脚本。

## 边界

- 本目录只放工具脚本本体与批次说明，不承载仓库级真值入口。
- 若脚本产出文件：
  - 可复现运行时产物归 `02_runtime/`
  - 大体量工具运行时归档归 `12_tooling_runtime_archive/`
  - 临时中间文件只允许落在本批次目录内且可迁走可删
- 若脚本沉淀出可长期复用的合同/索引/入口说明，必须提升归位到 `00_entry/02_runtime/12_tooling_runtime_archive` 对应层。

## 当前文件

- `s_bucketize.py`
- `ingest_ashare_txt_to_md.py`
- `kimi_cutpack_manifest.py`
- `relocate_path_prefix.py`
- `slice_csv_tail_v1.py`
- `tk_manual_append_rows.py`

## 当前裁决

 - 这 6 个脚本都属于：
  - 输入输出相对明确
  - 对新仓库后续整理、入库、索引仍有价值
  - 可以脱离旧 `backtest_out` 主线独立复用
- 它们进入新仓库时，不只复制脚本本体，还必须同时带：
  - 原路径
  - 当前用途
  - 输入输出备注
  - 适用边界

## 备注入口

- 批次备注见：`BATCH_03_TOOL_NOTES.md`
