# AShare P0 First Round Validation Runtime

更新时间：2026-07-12

## 用途

- 这里放 A 股 P0 首轮离线验证的 runtime 骨架、执行卡、结果页 stub 和后续脚本入口。
- 这一层负责把 repo 级验证合同接到可执行工作线，不直接替代 `00_entry` 的真值文档。

## 当前范围

- 当前只覆盖 `T01`、`T02`、`T03`、`T04`、`T05` 的首轮离线验证工作线。
- 当前先落：
  - `runtime_execution_card_v1.md`
  - `reports/`
  - `artifacts/`
- 当前不含：
  - 正式扫描脚本
  - 真实统计结果
  - 自动化 pipeline

## 当前状态

- `T01` 已有 fresh-run 结果和行业分布补充统计。
- `T02` 已贯通模板级 scan、真实宽表拼接 smoke-run 和真实源抓取入口。
- `T02` 真实源抓取已尝试一轮：
  - `moneyflow / northbound / industry` 三条 fetcher 均已落 failure metadata
  - 当前统一阻塞：`failure_reason = tushare_token_missing`
- 当前新增 `check_t02_tushare_env_v1.py`，用于先判定 token 与依赖，再决定是否继续 fetcher。
- 首轮 preflight 结果：
  - `token_present = false`
  - `pandas.available = true`
  - `tushare.available = false`

## 当前文件

- `runtime_execution_card_v1.md`
- `artifact_index_v1.tsv`
- `runtime_provenance_note_v1.md`
- `run_t01_volume_price_scan_v1.py`
- `run_t01_industry_distribution_v1.py`
- `audit_t02_fund_flow_input_v1.py`
- `prepare_t02_fund_flow_input_v1.py`
- `build_t02_real_input_v1.py`
- `check_t02_tushare_env_v1.py`
- `fetch_t02_moneyflow_tushare_v1.py`
- `fetch_t02_northbound_tushare_v1.py`
- `fetch_t02_industry_map_tushare_v1.py`
- `run_t02_fund_flow_scan_v1.py`
- `data/README.md`
- `data/t02_fund_flow_input_contract_v1.csv`
- `data/t02_real_input_sources_manifest_v1.tsv`
- `data/t02_real_input_assembly_note_v1.md`
- `data/t02_sources/README.md`
- `reports/README.md`
- `reports/T01_result_stub_v1.md`
- `reports/T02_result_stub_v1.md`
- `reports/T03_availability_and_downgrade_stub_v1.md`
- `reports/T04_result_stub_v1.md`
- `reports/T05_result_stub_v1.md`
- `reports/first_round_summary_stub_v1.md`
- `artifacts/README.md`

## Git 归口裁决

- `INDEX_NOTE`，应跟踪：
  - `README.md`
  - `runtime_execution_card_v1.md`
  - `artifact_index_v1.tsv`
  - `runtime_provenance_note_v1.md`
  - `reports/*.md`
  - `artifacts/README.md`
- `GENERATOR`，后续应跟踪：
  - `run_t01_volume_price_scan_v1.py`
  - `run_t01_industry_distribution_v1.py`
  - `audit_t02_fund_flow_input_v1.py`
  - `prepare_t02_fund_flow_input_v1.py`
  - `build_t02_real_input_v1.py`
  - `fetch_t02_moneyflow_tushare_v1.py`
  - `fetch_t02_northbound_tushare_v1.py`
  - `fetch_t02_industry_map_tushare_v1.py`
  - `run_t02_fund_flow_scan_v1.py`
  - 后续新增的汇总脚本、验收脚本
- `ARTIFACT`，后续按验证批次决定是否跟踪：
  - `artifacts/**`
- `IGNORE_LOCAL_TEMP`，应忽略：
  - 一次性调试摘录
  - 临时中转 csv
  - 本地 scratch 备注

## 当前默认读法

1. 先看 `00_entry/A股_P0_功能合同__20260711.md`
2. 再看 `00_entry/A股_P0_离线验证执行卡__20260712.md`
3. 再看 `runtime_execution_card_v1.md`
4. 最后把结果落到 `reports/` 和 `artifacts/`

## 当前回链

- 功能合同：
  - `00_entry/A股_P0_功能合同__20260711.md`
- 验证任务单：
  - `00_entry/A股_P0_验证任务单__20260711.md`
- 离线验证执行卡：
  - `00_entry/A股_P0_离线验证执行卡__20260712.md`
- 离线验证产出落点说明：
  - `00_entry/A股_P0_离线验证产出落点说明__20260712.md`
