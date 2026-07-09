# Batch 05 Legacy MT4 Probe Assets Execution Card

## 生成入口

- `PRODUCER`: `historical_recovered_copy`
- `SOURCE_SCOPE`: `legacy MT4 portable probe assets`
- `MAIN_ENTRY`:
  - `README.md`
  - `03_MT4便携探针实例/history/`

## 当前作用

- 为旧运行时中的 `MT4` 便携探针历史大目录提供批次级执行说明。
- 本批次属于历史终端态与行情缓存快照归档，不作为当前业务 first-hop 入口。
- 若后续某个可复现模板或 probe 入口需要重新启用，必须提升归位到 `02_runtime/` 或对应的模板批次，不直接回退到本批大目录。

## 证据强度

- `evidence_mode=historical_recovered`
