# Batch 147 YTC Sample Intake Absorb

更新时间：2026-07-14

## 批次目标

- 为 `YTC` 补齐 `60m/5m` 小样本入口与来源说明，确保最小运行线可继续降级与追溯。
- 当前阶段只做资料整理，不扩成全量执行线。

## 已知仓内入口

- 运行侧最小脚本：
  - `02_runtime/butler_r0_ohlcv_object_cards/run_ytc_daily_weekly_minimal_v1.py`
- 对象依赖矩阵：
  - `01_active_objects/butler_r0_object_cards_p0/object_cards_p1_runtime_dependency_matrix_v1.tsv`

## 当前产物

- `manifest_v1.tsv`
- `provenance.md`
- `YTC_SAMPLE_REQUIREMENT_v1.tsv`
- `BATCH_147_EXECUTION_CARD.md`
- `BATCH_147_ARTIFACT_INDEX_v1.md`
- `00_raw_snapshot/YTC_existing_daily_weekly_runtime_anchor__historical_recovered.md`
- `00_raw_snapshot/YTC_intraday_sample_provider_and_downgrade_note__20260713.md`
- `00_raw_snapshot/YTC_intraday_repo_search_status__20260713.md`
- `00_raw_snapshot/YTC_intraday_provider_candidate_matrix__20260713.md`
- `00_raw_snapshot/YTC_intraday_minimal_intake_path__20260713.md`
- `00_raw_snapshot/YTC_intraday_sample_acceptance_contract__20260713.md`
- `00_raw_snapshot/YTC_intraday_provenance_note_template__20260713.md`
- `00_raw_snapshot/YTC_601991_SH_60m_tushare_live_probe_excerpt__20260713.md`
- `00_raw_snapshot/YTC_intraday_provider_rate_limit_blocker__20260713.md`
- `00_raw_snapshot/601991_SH_5m.csv`
- `00_raw_snapshot/601991_SH_60m.csv`
- `00_raw_snapshot/601991_SH_5m_provenance_note__20260714.md`
- `00_raw_snapshot/601991_SH_60m_provenance_note__20260714.md`

## 默认阅读顺序

- 1. 先看本 README
- 2. 再看 `YTC_SAMPLE_REQUIREMENT_v1.tsv`
- 3. 再按该表落样本并补 provenance

## 当前补件进展

- 已通过外部历史分钟数据包吸收：
  - `601991_SH_5m.csv`
  - `601991_SH_60m.csv`
- `Tushare stk_mins` 的限频阻塞保留为历史阻塞说明，不再作为当前唯一落盘路径。

## 当前边界

- 本批次只负责样本补采与追溯，不负责：
  - 新增指标实现
  - 扩展执行链
  - 回测产物生成
