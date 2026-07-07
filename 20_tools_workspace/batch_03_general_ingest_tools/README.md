# General Ingest Tools Batch 03

## 用途

- 这里放从旧 `tools` 中筛出来、仍有长期复用价值的“通用整理/入库/manifest 工具”。
- 这批不是一次性清理脚本，也不是强绑定旧回测输出的审计脚本。

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
