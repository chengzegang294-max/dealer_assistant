# Batch 147 Artifact Index v1

更新时间：2026-07-14

## 当前批次产物

| 文件类型 | 原路径 | 新路径 | 生成入口 | 适用对象 | 当前作用 | 证据强度 | 状态 | 缺口 |
|---|---|---|---|---|---|---|---|---|
| `INDEX_NOTE` | `batch_147/README.md` | `batch_147/README.md` | `manual_batch_setup` | `YTC` | 批次入口 | `hard` | `active` | 无 |
| `INDEX_NOTE` | `batch_147/provenance.md` | `batch_147/provenance.md` | `manual_batch_setup` | `YTC` | 来源追溯说明 | `hard` | `active` | 无 |
| `ARTIFACT` | `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/watchlist_subset/601991_SH_1d.csv` | `historical_recovered_reference_only` | `historical_runtime_sample` | `YTC` | 现有日线基座样本 | `historical_recovered` | `referenced` | 非 60m/5m |
| `ARTIFACT` | `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/weekly_subset/601991_SH_1w.csv` | `historical_recovered_reference_only` | `build_weekly_from_daily_v1.py` | `YTC` | 现有 weekly 降级样本 | `hard_derived_from_runtime` | `referenced` | 非 60m/5m |
| `ARTIFACT` | `02_runtime/butler_r0_ohlcv_object_cards/acceptance_outputs/ytc_601991_sh_daily_weekly_output.json` | `historical_recovered_reference_only` | `run_ytc_daily_weekly_minimal_v1.py` | `YTC` | 现有最小运行输出 | `hard` | `referenced` | 仍缺分钟级样本 |
| `ARTIFACT` | `batch_147/00_raw_snapshot/YTC_existing_daily_weekly_runtime_anchor__historical_recovered.md` | `batch_147/00_raw_snapshot/YTC_existing_daily_weekly_runtime_anchor__historical_recovered.md` | `historical_recovered_runtime_reference` | `YTC` | 批次内历史锚点说明 | `historical_recovered` | `active` | 仍缺分钟级真样本 |
| `INDEX_NOTE` | `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/ytc_daily_weekly_sample_plan_v1.tsv + sample_provenance_index_v1.tsv` | `batch_147/00_raw_snapshot/YTC_intraday_sample_provider_and_downgrade_note__20260713.md` | `manual_batch_absorb_note` | `YTC` | 分钟样本 provider 与降级口径说明 | `weak_evidence` | `active` | 已固定口径，仍缺真实样本 |
| `INDEX_NOTE` | `repo-wide search over 02_runtime + 12_tooling_runtime_archive` | `batch_147/00_raw_snapshot/YTC_intraday_repo_search_status__20260713.md` | `manual_repo_search_note` | `YTC` | 分钟样本仓内搜索状态 | `weak_evidence` | `active` | 已确认当前仓内无 A 股 `60m/5m` 实物 |
| `INDEX_NOTE` | `daily probe/fetch scripts + legacy minute references` | `batch_147/00_raw_snapshot/YTC_intraday_provider_candidate_matrix__20260713.md` | `manual_provider_decision_note` | `YTC` | 分钟样本 provider 候选矩阵 | `weak_evidence` | `active` | 已固定候选顺序，仍未执行 provider |
| `INDEX_NOTE` | `batch_147 intake target definition` | `batch_147/00_raw_snapshot/YTC_intraday_minimal_intake_path__20260713.md` | `manual_intake_path_note` | `YTC` | 分钟样本最小补采路径 | `weak_evidence` | `active` | 已固定命名/字段/落点/更新顺序 |
| `INDEX_NOTE` | `batch_147 intake acceptance policy` | `batch_147/00_raw_snapshot/YTC_intraday_sample_acceptance_contract__20260713.md` | `manual_acceptance_contract_note` | `YTC` | 分钟样本接收合同 | `weak_evidence` | `active` | 已固定最小通过标准 |
| `INDEX_NOTE` | `batch_147 provenance fill template` | `batch_147/00_raw_snapshot/YTC_intraday_provenance_note_template__20260713.md` | `manual_provenance_template_note` | `YTC` | 分钟样本 provenance 模板 | `weak_evidence` | `active` | 后续实物到位后可直接套用 |
| `ARTIFACT` | `Tushare live probe terminal output` | `batch_147/00_raw_snapshot/YTC_601991_SH_60m_tushare_live_probe_excerpt__20260713.md` | `manual_terminal_capture_from_tushare_probe` | `YTC` | `601991.SH 60m` 实探摘录 | `weak_live_probe_excerpt` | `active` | 已证明 provider 可出 `60m`，仍缺完整 csv |
| `INDEX_NOTE` | `Tushare minute interface rate-limit response` | `batch_147/00_raw_snapshot/YTC_intraday_provider_rate_limit_blocker__20260713.md` | `manual_terminal_blocker_note` | `YTC` | 分钟样本 provider 限频阻塞历史说明 | `weak_evidence` | `active` | 已保留历史阻塞记录；当前已改由外部历史分钟包完成样本吸收 |
| `ARTIFACT` | `E:\股票历史数据\分钟K线-股票241\2000-2025\按年\5分钟\2024.zip::2024/sh601991.csv` | `batch_147/00_raw_snapshot/601991_SH_5m.csv` | `external_vendor_package_window_extract` | `YTC` | 真实 5m 窗口样本 | `external_vendor_package_snapshot` | `active` | 卖家元信息暂未回填，但最小字段与时间窗已满足接收合同 |
| `INDEX_NOTE` | `external_vendor_package_window_extract` | `batch_147/00_raw_snapshot/601991_SH_5m_provenance_note__20260714.md` | `manual_provenance_fill_after_external_absorb` | `YTC` | 5m 样本来源追溯说明 | `hard` | `active` | 若后续拿到卖家信息，可继续增强 provenance |
| `ARTIFACT` | `derived from batch_147/00_raw_snapshot/601991_SH_5m.csv` | `batch_147/00_raw_snapshot/601991_SH_60m.csv` | `aggregate_5m_to_60m_session_buckets_v1` | `YTC` | 真实 60m 聚合样本 | `hard_derived_from_external_5m` | `active` | 已满足最小运行线样本补件；保留聚合关系说明 |
| `INDEX_NOTE` | `aggregate_5m_to_60m_session_buckets_v1` | `batch_147/00_raw_snapshot/601991_SH_60m_provenance_note__20260714.md` | `manual_provenance_fill_after_local_aggregation` | `YTC` | 60m 样本来源追溯说明 | `hard` | `active` | 已固定上游 5m 来源与聚合模式 |

## 当前说明

- 仓内已存在的是 `daily+weekly` 降级路径证据。
- 当前批次已补分钟样本 provider 与降级口径说明。
- 当前批次已补仓内搜索状态、provider 候选矩阵和最小补采路径。
- 当前已落真实分钟级样本，不把历史降级样本伪装成目标样本。
