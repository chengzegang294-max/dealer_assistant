# Legacy MT4 Probe Assets Batch 05

## 用途

- 这里放旧运行时里的 `MT4` 便携探针历史大目录与终端态快照。
- 本批次只承担历史回收与追溯作用，不作为当前默认运行入口。

## 当前包含

- `03_MT4便携探针实例/history/`
  - `ICMarketsSC-Demo03/`
  - `VTMarkets-Live 2/`
  - `default/`
  - `mailbox/`
  - `books.dat`

## 当前裁决

- 整批目录按 `ARCHIVE_ONLY / historical_recovered` 口径保留。
- 这些文件属于历史终端态与行情缓存快照，不冒充“当前可复现 probe 入口”。
- 若后续需要当前可复现入口，继续以 `batch_02_mt_indicator_family` 与 `batch_03_mt4_portable_probe_templates` 为默认阅读链，不回退到本批历史大目录。
- 原 `mt4_probe_instance/` 在新仓中是失效 `Junction`，不承载真实归档内容，已删除以消除 Git 扫描警告。

## 备注入口

- `BATCH_05_LEGACY_MT4_PROBE_ASSETS_EXECUTION_CARD__20260709.md`
- `BATCH_05_LEGACY_MT4_PROBE_ASSETS_ARTIFACT_INDEX__20260709.tsv`
