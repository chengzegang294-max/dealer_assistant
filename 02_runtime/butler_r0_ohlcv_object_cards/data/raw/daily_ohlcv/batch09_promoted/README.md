# Batch09 Promoted Daily Inputs

## 用途

- 存放从 `00_assets/_raw_snapshot_batch09/` 正式归位提升到 runtime 原始输入层的历史日线 CSV。
- 当前目录只收 `ashare_clean` 与 `ashare_watchlist/kline_1d` 这两批边界最清楚的历史输入。

## 入口

- `GENERATOR`:
  - `02_runtime/butler_r0_ohlcv_object_cards/promote_batch09_daily_to_runtime_raw_v1.py`
- `INDEX_NOTE`:
  - 当前文件
  - `batch09_promotion_map_v1.tsv`
  - `../catalog_v1.tsv`

## 当前口径

- 这里的文件是 `historical_recovered`，不是当前终端在线拉取。
- 这些 CSV 允许被后续 runtime 直接引用，但必须通过 `catalog_v1.tsv` 与 `batch09_promotion_map_v1.tsv` 回链到原始批次。
- 若后续再提升更多 batch09 子块，继续追加到当前 family，不另开根层目录。
