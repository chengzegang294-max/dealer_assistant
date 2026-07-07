# Commit Ready Batch 4B2 - GROUP_08 txt md archive - 2026-06-23

## Goal

- commit the full `05_txt源码_md归档/` text-only archive as one batch
- keep this batch purely textual and reproducible
- do not mix in `06_pdf_retained_cut_v2/`

## Exact Files To Stage

- subtree:
  - `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_08_A股量化_数据研究/05_txt源码_md归档/`
- expected source file count:
  - `101`
- content mix:
  - `100` md
  - `1` tsv

## Why This Batch Is Stable

- `README_放这里.md` records the generation batch id and source directory
- `txt_md_index_v1.tsv` provides per-file source-to-md mapping, encoding guess, and cluster bucket
- total size is only about `1.09 MB`

## Suggested Commit Message

- `docs: add GROUP_08 txt md archive pack (05 subtree)`

## Explicit Exclusions

- `00_external_import_staging/`
- `06_pdf_retained_cut_v2/`

## Stage Command

- use:
  - `docs/commit_ready_stage_batch_4B2__GROUP_08_txt_md_archive__2026-06-23.ps1`
  - `docs/commit_ready_batch_4B2__GROUP_08_txt_md_archive__paths.txt`
