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
- `T02` 已贯通真实源抓取、真实宽表拼接、扩样验证和长窗稳定性复核。
- `T02` 当前已形成项目裁决：
  - 全局保留 `3% + 连续2日`
  - `2.5% + 连续2日 + 排除 G03_震荡` 只保留为 `watchlist_only`
- `T03 / T04 / T05` 当前仍在待推进状态。
- 当前已新增桥接参考：
  - `00_entry/A股_P0_趋势仓位与轮动仓位桥接卡__20260712.md`
  - `00_entry/A股_P0_GROUP_08研究合同桥接与验证映射卡__20260713.md`
  - 只作为解释层与风险预算层参考，不直接改写默认 runtime 门控

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
3. 若涉及趋势仓位或轮动仓位，再看 `00_entry/A股_P0_趋势仓位与轮动仓位桥接卡__20260712.md`
4. 若涉及 `GROUP_08` 新冻结合同，再看 `00_entry/A股_P0_GROUP_08研究合同桥接与验证映射卡__20260713.md`
5. 再看 `runtime_execution_card_v1.md`
6. 最后把结果落到 `reports/` 和 `artifacts/`

## 当前回链

- 功能合同：
  - `00_entry/A股_P0_功能合同__20260711.md`
- 验证任务单：
  - `00_entry/A股_P0_验证任务单__20260711.md`
- 离线验证执行卡：
  - `00_entry/A股_P0_离线验证执行卡__20260712.md`
- 趋势仓位与轮动仓位桥接卡：
  - `00_entry/A股_P0_趋势仓位与轮动仓位桥接卡__20260712.md`
- GROUP_08 研究合同桥接与验证映射卡：
  - `00_entry/A股_P0_GROUP_08研究合同桥接与验证映射卡__20260713.md`
- 离线验证产出落点说明：
  - `00_entry/A股_P0_离线验证产出落点说明__20260712.md`
