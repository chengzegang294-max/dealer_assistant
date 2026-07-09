# Butler R0 OHLCV Object Cards Runtime

更新时间：2026-07-09

## 用途

- 为 `VOLFAC / BPB / VP / TKR7 / YTC / CHZL_BSD / VOLTARGET / PERIOD_QUEEN` 等对象卡准备最小可跑入口。
- 这里只放运行协议、参数模板、验收样本入口；不放来源文档。

## 当前范围

- 当前已覆盖 A 股日线 OHLCV 样本、由日线合成的周线样本，以及 `YTC / CHZL_BSD / VOLTARGET / PERIOD_QUEEN / VP / TKR7 / registry_v0` 的最小降级、半自动或聚合运行入口。
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
  - `run_vp_minimal_v1.py`
  - `run_tkr7_minimal_v1.py`
  - `run_registry_v0_minimal.py`
  - `run_registry_v0_acceptance_v1.py`
  - `promote_batch09_daily_to_runtime_raw_v1.py`
- `ARTIFACT`:
  - `acceptance_outputs/*.json`
  - `probe_outputs/*`
  - `data/raw/daily_ohlcv/*`
- `INDEX_NOTE`:
  - `runtime_execution_card_v1.md`
  - `acceptance_outputs/artifact_index_v1.tsv`
  - `probe_outputs/artifact_index_v1.tsv`
  - `data/raw/daily_ohlcv/catalog_v1.tsv`
  - `data/raw/watchlist_inputs/README.md`
  - `data/raw/watchlist_inputs/catalog_v1.tsv`
  - `acceptance_samples/sample_provenance_index_v1.tsv`
  - `acceptance_samples/ytc_daily_weekly_sample_plan_v1.tsv`
  - `acceptance_samples/voltarget_sample_plan_v1.tsv`
  - `acceptance_samples/period_queen_proxy_sample_plan_v1.tsv`
  - `acceptance_samples/vp_sample_plan_v1.tsv`
  - `acceptance_samples/tkr7_sample_plan_v1.tsv`
  - `acceptance_samples/registry_v0_sample_plan_v1.tsv`
  - `acceptance_samples/chzl_bsd_structure_bundle/bundle_index_v1.tsv`
  - `registry_vote_input_contract_v1.tsv`
  - `registry_output_contract_v1.tsv`

## 本轮推进

- `registry_v0` 已从“6 张卡串跑”推进到“有显式输入/输出合同”的最小正式聚合入口。
- `acceptance_outputs/registry_v0_601991_sh_output.json` 现已显式输出 `vote_input_snapshot / aggregate_summary / final_decision_card / size_policy_card`。
- `run_registry_v0_acceptance_v1.py` 用样本计划校验 `final_signal / trade_gate / blockers / permission / hard_block / size_policy`，把 registry 验收从“人工看 JSON”推进到“机器可复核”。
- `00_assets/_raw_snapshot_batch09/ashare_watchlist` 剩余非 `kline_1d` 文件已完成三分流：
  - 结构化 watchlist 输入归 `data/raw/watchlist_inputs/`
  - 文本快照归 `10_source_library_archive/.../ashare_watchlist_text_snapshot/`
  - `blogroom_* / mx2025_summary_*` 归 `12_tooling_runtime_archive/.../batch_09_watchlist_ocr_artifacts__20260708/`
