# Watchlist Inputs

## 用途

- 存放可被 runtime 直接消费的关注池结构化输入。
- 当前目录区分“历史回收结构化输入”和未来可能新增的正式生成输入。

## 入口

- `GENERATOR`:
  - `02_runtime/butler_r0_ohlcv_object_cards/promote_batch09_watchlist_tripartite_v1.py`
- `INDEX_NOTE`:
  - 当前文件
  - `catalog_v1.tsv`

## 当前口径

- `batch09_promoted/structured_inputs/` 中的文件属于 `historical_recovered`
- 它们是结构化的 watchlist 输入，不冒充原始快照，也不归到 OCR 产物层
