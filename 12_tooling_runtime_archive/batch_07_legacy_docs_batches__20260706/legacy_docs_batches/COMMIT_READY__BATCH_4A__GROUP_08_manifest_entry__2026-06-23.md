# 提交就绪批次 4A - GROUP_08 manifest entry - 2026-06-23

## 目标

- commit the top-level non-binary entry layer of `GROUP_08`
- keep this batch text-first and auditable
- do not include `00_external_import_staging/` or any deeper subtree contents

## 精确暂存文件

- all top-level files directly under:
  - `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_08_A股量化_数据研究/`
- expected count:
  - `39`
- allowed extensions:
  - `.md`
  - `.tsv`
  - `.ps1`

## 显式排除项

- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_08_A股量化_数据研究/00_external_import_staging/`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_08_A股量化_数据研究/01_62份研究PDF/`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_08_A股量化_数据研究/02_pdf入门书/`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_08_A股量化_数据研究/03_txt标题聚类/`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_08_A股量化_数据研究/04_epub目录粗切/`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_08_A股量化_数据研究/05_txt源码_md归档/`
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_08_A股量化_数据研究/06_pdf_retained_cut_v2/`

## 建议提交信息

- `docs: add GROUP_08 manifest-entry pack (top-level ledgers/runbooks)`

## 暂存命令

- use:
  - `docs/commit_ready_stage_batch_4A__GROUP_08_manifest_entry__2026-06-23.ps1`
  - `docs/commit_ready_batch_4A__GROUP_08_manifest_entry__paths.txt`
