# GROUP_08 06_pdf_retained_cut_v2 EVAL 2026-06-23

## 范围

- target subtree:
  - `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_08_A股量化_数据研究/06_pdf_retained_cut_v2/`
- decision to make:
  - commit whole tree or split further

## 观察快照

- file count:
  - `67`
- total size:
  - `2.27 MB`
- content mix:
  - `66` md
  - `1` tsv

## 合同锚点

- README:
  - [README_放这里.md](file:///D:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_08_A股量化_数据研究/06_pdf_retained_cut_v2/README_放这里.md)
- manifest:
  - [manifest_v2.tsv](file:///D:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_08_A股量化_数据研究/06_pdf_retained_cut_v2/manifest_v2.tsv)
- upstream contracts:
  - `CUT_CONTRACT__Kimi_全文保留优先_v1.md`
  - `CUT_CONTRACT__Kimi_保留型切割_v2.md`

## 为何整树提交更好

- the tree is already small enough for one commit
- every file is text-first and reviewable
- the manifest centralizes:
  - `bucket`
  - `title_short`
  - `retain_mode`
  - `current_repo_role`
  - `quant_rows`
  - output `path`
- splitting further would add coordination cost without reducing binary risk, because there are no binaries in this subtree

## 裁决

- decision:
  - `COMMIT_WHOLE_TREE`
- rationale:
  - this subtree is already the final, contract-backed, delete-source-capable v2 output layer
  - size is moderate and contents are pure md/tsv
  - reviewability is preserved by `manifest_v2.tsv`

## 边界

- commit now:
  - whole `06_pdf_retained_cut_v2/`
- do not mix with:
  - `00_external_import_staging/`
  - `05_txt源码_md归档/`
