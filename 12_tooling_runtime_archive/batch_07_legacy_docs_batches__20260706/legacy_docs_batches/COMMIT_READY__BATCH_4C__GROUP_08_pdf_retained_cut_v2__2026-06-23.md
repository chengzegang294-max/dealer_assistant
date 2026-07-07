# Commit Ready Batch 4C - GROUP_08 pdf retained cut v2 - 2026-06-23

## Goal

- commit the full `06_pdf_retained_cut_v2/` subtree as one contract-backed v2 output batch
- keep this batch separate from the txt-md archive batch

## Exact Files To Stage

- subtree:
  - `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_08_A股量化_数据研究/06_pdf_retained_cut_v2/`
- expected source file count:
  - `67`
- content mix:
  - `66` md
  - `1` tsv

## Decision Basis

- see:
  - `docs/GROUP_08__06_pdf_retained_cut_v2__EVAL__2026-06-23.md`
- decision:
  - commit whole tree

## Suggested Commit Message

- `docs: add GROUP_08 pdf retained cut v2 pack (06 subtree)`

## Explicit Exclusions

- `00_external_import_staging/`
- `05_txt源码_md归档/`

## Stage Command

- use:
  - `docs/commit_ready_stage_batch_4C__GROUP_08_pdf_retained_cut_v2__2026-06-23.ps1`
  - `docs/commit_ready_batch_4C__GROUP_08_pdf_retained_cut_v2__paths.txt`
