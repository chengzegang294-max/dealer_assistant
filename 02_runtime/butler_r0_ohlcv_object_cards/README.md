# Butler R0 OHLCV Object Cards Runtime

更新时间：2026-07-08

## 用途

- 为 `VOLFAC / BPB / VP / TKR7 / VOLTARGET / PERIOD_QUEEN` 等对象卡准备最小可跑入口。
- 这里只放运行协议、参数模板、验收样本入口；不放来源文档。

## 当前范围

- 当前已覆盖 A 股日线 OHLCV 样本、由日线合成的周线样本，以及 `YTC / CHZL_BSD / VOLTARGET / PERIOD_QUEEN` 的最小降级或半自动运行入口。
- 未来再扩到分钟级、更多对象卡真实外部输入，以及跨市场。

## 上游合同

- `01_active_objects/butler_r0_object_cards_p0/*_field_contract_v1.tsv`
- `01_active_objects/butler_r0_object_cards_p0/object_cards_p0_acceptance_matrix_v1.tsv`

## 当前生成入口与产物

- `GENERATOR`:
  - `run_object_card_minimal_v1.py`
  - `tushare_daily_probe_v1.py`
  - `akshare_daily_probe_v1.py`
  - `baostock_daily_probe_v1.py`
  - `baostock_daily_fetch_to_raw_v1.py`
  - `build_weekly_from_daily_v1.py`
  - `build_chzl_structure_series_v1.py`
  - `run_ytc_daily_weekly_minimal_v1.py`
  - `run_chzl_bsd_sample_stub_v1.py`
  - `run_voltarget_minimal_v1.py`
  - `run_period_queen_proxy_minimal_v1.py`
- `ARTIFACT`:
  - `acceptance_outputs/*.json`
  - `probe_outputs/*`
  - `data/raw/daily_ohlcv/*`
- `INDEX_NOTE`:
  - `runtime_execution_card_v1.md`
  - `acceptance_outputs/artifact_index_v1.tsv`
  - `probe_outputs/artifact_index_v1.tsv`
  - `data/raw/daily_ohlcv/catalog_v1.tsv`
  - `acceptance_samples/sample_provenance_index_v1.tsv`
  - `acceptance_samples/ytc_daily_weekly_sample_plan_v1.tsv`
  - `acceptance_samples/voltarget_sample_plan_v1.tsv`
  - `acceptance_samples/period_queen_proxy_sample_plan_v1.tsv`
  - `acceptance_samples/chzl_bsd_structure_bundle/bundle_index_v1.tsv`
