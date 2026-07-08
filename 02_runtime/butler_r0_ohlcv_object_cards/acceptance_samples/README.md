# Acceptance Samples

## 目的

- 存放 `VOLFAC / BPB / VP / TKR7` 的最小 OHLCV 样本。
- 当前只建入口，不伪造样本数据；等本地真实数据目录核清后再回填。

## 约束

- 只放最小样本，不放整市场大数据。
- 每个样本必须能对齐 `object_cards_p0_acceptance_matrix_v1.tsv`。

## 当前样本策略

- `clean_subset/`：从 `00_assets/_raw_snapshot_batch09/ashare_clean/` 提升的真实 A 股 `1d` 样本。
- `watchlist_subset/`：从 `00_assets/_raw_snapshot_batch09/ashare_watchlist/kline_1d/` 提升的关注池 `1d` 样本。
- 不改原始 CSV，只复制最小子集；来源回链与作用见 `sample_provenance_index_v1.tsv`。
