# A股数据源裁决对象入口 v1

## 适用问题

- 想直接知道当前项目如何选 `Tushare / 通达信 / AKShare / 雪球`
- 不想先从批次 README 一层层下钻
- 想优先看“项目裁决”，而不是原始教程快照

## first-hop 入口

- `../../batch_140_tushare_tdx_data_source_absorb__20260712/02_absorb_index/ashare_p0_data_source_decision_v1.md`

## 默认阅读顺序

- 先看项目裁决：
  - `../../batch_140_tushare_tdx_data_source_absorb__20260712/02_absorb_index/ashare_p0_data_source_decision_v1.md`
- 再看教程内化摘要：
  - `../../batch_140_tushare_tdx_data_source_absorb__20260712/02_absorb_index/tushare_tdx_tutorial_core_digest_v1.md`
- 只有在需要核原文时，再回：
  - `../../batch_140_tushare_tdx_data_source_absorb__20260712/00_raw_snapshot/`

## 当前结论速记

- 当前优先组合是：
  - `Tushare` 负责 P0 必需缺口
  - `通达信` 作为后续 `OHLCV / 分钟线` 底表优先评估对象
  - `AKShare / 雪球` 作为补源

## 回链

- 上层主题入口：
  - `../ashare_data_source_decision_topic_entry_v1.md`
