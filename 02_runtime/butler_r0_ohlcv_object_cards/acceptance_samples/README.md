# Acceptance Samples

## 目的

- 存放 `VOLFAC / BPB / VP / TKR7 / YTC / CHZL_BSD / VOLTARGET / PERIOD_QUEEN` 的最小样本与样本合同入口。
- 当前只放真实样本、由真实样本合成的周线样本、以及结构标注模板；不伪造信号数据。

## 约束

- 只放最小样本，不放整市场大数据。
- 每个样本必须能对齐 `object_cards_p0_acceptance_matrix_v1.tsv`。

## 当前样本策略

- `clean_subset/`：从 `00_assets/_raw_snapshot_batch09/ashare_clean/` 提升的真实 A 股 `1d` 样本。
- `watchlist_subset/`：从 `00_assets/_raw_snapshot_batch09/ashare_watchlist/kline_1d/` 提升的关注池 `1d` 样本。
- `weekly_subset/`：由 `build_weekly_from_daily_v1.py` 从真实日线样本合成的 `1w` 样本，优先服务 `YTC` 的 `daily + weekly` 降级运行。
- `chzl_bsd_structure_bundle/`：`CHZL_BSD` 的结构样本包、索引和标注模板。
- `ytc_daily_weekly_sample_plan_v1.tsv`：`YTC` 多周期样本计划。
- `voltarget_sample_plan_v1.tsv`：`VOLTARGET` 的最小风险缩放样本计划。
- `period_queen_proxy_sample_plan_v1.tsv`：`PERIOD_QUEEN` 的单标的代理情绪样本计划。
- `vp_sample_plan_v1.tsv`：`VP` 的最小 volume profile 样本计划。
- `tkr7_sample_plan_v1.tsv`：`TKR7` 的最小 AO 背离样本计划。
- `object_cards_aux_input_sample_contract_v1.tsv`：`MFLOW / INSTB` 的最小外部输入样本合同。
- 不改原始 CSV；来源回链、生成入口与作用见 `sample_provenance_index_v1.tsv`。
