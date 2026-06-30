# Probe Batch 01 Volty XBreaking

## 用途

- 这里放 `Volty / XBreaking` 首批 probe 的执行卡、产物索引和后续证据路径。

## 当前文件

- `BATCH_01_EXECUTION_CARD.md`
- `BATCH_01_ARTIFACT_INDEX_TEMPLATE.md`
- `BATCH_01_PROVENANCE_NOTEBOARD.md`
- `MT4_MT5_FIRST_RUN_PLAYBOOK.md`
- `probe_artifact_ingest_v1.py`

## 当前状态

- 这批已经把运行时落盘口径固定下来。
- `XBreaking` 首份 `csv` 已回收到 `artifacts\xbreaking\csv`。
- `Volty` 首份历史 `csv` 与 `tester report` 已回收到 `artifacts\volty\...`。
- `XBreaking` 已额外回收一份弱相关终端日志和摘录，但仍缺明确 `tester log / report`。
- `Volty` 本机终端目录仍未发现新的 `csv`，且 `log` 仍待继续回收。
- `XBreaking tester_report` 仍待继续回收。
- `artifacts\volty\*` 与 `artifacts\xbreaking\*` 回收目录已建好。
- 已补一个专用 ingest 脚本，用来扫描 `MetaQuotes` 终端目录并复制候选产物到本批 `artifacts`。
- 其中 `log` 现在支持按家族默认关键词和手动 `--log-keyword` 做内容筛选。
- 其中 `log` 还支持 `--log-filename-keyword`、`--log-tail-lines` 和摘录 `.txt` 自动落盘。
- 当前已补一份批次级备注总表，用于说明每个核心文件的来源、作用和证据强弱。
