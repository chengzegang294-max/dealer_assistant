# Batch 147 Raw Snapshot

更新时间：2026-07-14

## 用途

- 存放 `YTC` 分钟级样本补采材料，以及当前已回收的历史样本锚点说明。
- 当前先纳入仓内已存在的 `daily+weekly` 降级路径锚点，不冒充目标分钟级样本。

## 当前已纳入

- `YTC_existing_daily_weekly_runtime_anchor__historical_recovered.md`
- `YTC_intraday_sample_provider_and_downgrade_note__20260713.md`
- `YTC_intraday_repo_search_status__20260713.md`
- `YTC_intraday_provider_candidate_matrix__20260713.md`
- `YTC_intraday_minimal_intake_path__20260713.md`
- `YTC_intraday_sample_acceptance_contract__20260713.md`
- `YTC_intraday_provenance_note_template__20260713.md`
- `YTC_601991_SH_60m_tushare_live_probe_excerpt__20260713.md`
- `YTC_intraday_provider_rate_limit_blocker__20260713.md`
- `601991_SH_5m.csv`
- `601991_SH_60m.csv`
- `601991_SH_5m_provenance_note__20260714.md`
- `601991_SH_60m_provenance_note__20260714.md`

## 当前补件说明

- `2026-07-14` 已从项目外外部数据仓：
  - `E:\股票历史数据\分钟K线-股票241\2000-2025\按年\5分钟\2024.zip`
  吸收 `2024/sh601991.csv`
- 已截取窗口：
  - `2024-03-01 09:30:00`
  - `2024-04-10 15:00:00`
- 已落：
  - `5m` 真实样本
  - `60m` 聚合样本
  - 两份 provenance note

## 当前仍缺

- 卖家商品页/店铺元信息若后续可回补，可再加强 provenance
