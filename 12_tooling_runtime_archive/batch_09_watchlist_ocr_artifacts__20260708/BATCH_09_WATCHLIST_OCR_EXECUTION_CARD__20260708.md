# Batch 09 Watchlist OCR Execution Card

## 生成入口

- `GENERATOR`: `02_runtime/butler_r0_ohlcv_object_cards/promote_batch09_watchlist_tripartite_v1.py`
- `SOURCE`: `00_assets/_raw_snapshot_batch09/ashare_watchlist/`

## 当前作用

- 把 `blogroom_* / mx2025_summary_*` 一次性从合同外目录回收到 tooling runtime archive。
- 保留 OCR 与提取产物的历史证据属性，不混进 runtime 正式输入层。
