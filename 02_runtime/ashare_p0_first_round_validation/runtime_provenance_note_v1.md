# AShare P0 First Round Validation Provenance Note v1

更新时间：2026-07-12

## 用途

- 记录本目录当前 `GENERATOR / INDEX_NOTE / ARTIFACT` 的最小追溯关系。
- 防止后续新增脚本和结果后，只看到文件名，看不出谁生成、给谁用、证据强弱如何。

## 当前文件分类

### GENERATOR

- `run_t01_volume_price_scan_v1.py`
  - 当前作用：
    - 扫描日线 OHLCV CSV，输出 `T01` 触发密度摘要
  - 默认输入：
    - `02_runtime/butler_r0_ohlcv_object_cards/data/raw/daily_ohlcv/batch09_promoted/ashare_clean/`
  - 默认产物：
    - `artifacts/t01_volume_price_scan/`
  - 证据强度：
    - `hard`（当前终端新跑结果时）
- `run_t01_industry_distribution_v1.py`
  - 当前作用：
    - 基于 `T01` 标的级触发统计和临时行业映射，输出行业分布摘要
  - 默认输入：
    - `artifacts/t01_volume_price_scan/t01_symbol_trigger_counts_latest.tsv`
    - `02_runtime/butler_r0_ohlcv_object_cards/data/raw/watchlist_inputs/batch09_promoted/structured_inputs/factors_ladder_20260508.csv`
  - 默认产物：
    - `artifacts/t01_industry_distribution/`
  - 证据强度：
    - `hard`（当前终端新跑结果时）
- `audit_t02_fund_flow_input_v1.py`
  - 当前作用：
    - 审计候选资金宽表是否满足 `T02` 字段合同
  - 默认输入：
    - `data/t02_fund_flow_input_contract_v1.csv`
  - 默认产物：
    - `artifacts/t02_input_audit/`
  - 证据强度：
    - `hard`（当前终端新跑结果时）
- `prepare_t02_fund_flow_input_v1.py`
  - 当前作用：
    - 把候选资金宽表归一化为 `T02` 统一列名
  - 默认输入：
    - `data/t02_fund_flow_input_contract_v1.csv`
  - 默认产物：
    - `artifacts/t02_input_prepare/`
  - 证据强度：
    - `hard`（当前终端新跑结果时）
- `build_t02_real_input_v1.py`
  - 当前作用：
    - 把底表与 moneyflow、northbound、regime、industry 源表拼成候选真实宽表
  - 默认输入：
    - `artifacts/t02_input_prepare/t02_fund_flow_input_normalized_latest.csv`
    - 真实源表到位后再传入 `--moneyflow-csv`、`--northbound-csv`、`--regime-csv`、`--industry-csv`
  - 默认产物：
    - `artifacts/t02_real_input_build/`
  - 证据强度：
    - `hard`（当前终端新跑结果时）
- `check_t02_tushare_env_v1.py`
  - 当前作用：
    - 先检查本机 `TUSHARE_TOKEN`、`pandas` 和 `tushare` 依赖是否就绪，避免 fetcher 直接撞环境错误
  - 默认输入：
    - 本机环境变量和 `~/.tushare/token`
  - 默认产物：
    - `artifacts/t02_tushare_preflight/`
  - 证据强度：
    - `hard`（当前终端新跑结果时）
- `fetch_t02_moneyflow_tushare_v1.py`
  - 当前作用：
    - 复用 `TUSHARE_TOKEN` 合同，拉取 `moneyflow + daily` 并直接计算 `main_fund_net_inflow_ratio`
  - 默认输入：
    - `--symbol`
    - `--start-date`
    - `--end-date`
  - 默认产物：
    - `data/t02_sources/moneyflow_tushare/`
  - 证据强度：
    - `hard`（成功 CSV 或失败 metadata 均为当前终端新跑证据）
- `fetch_t02_northbound_tushare_v1.py`
  - 当前作用：
    - 复用 `TUSHARE_TOKEN` 合同，拉取 `moneyflow_hsgt` 北向资金时间序列
  - 默认输入：
    - `--start-date`
    - `--end-date`
  - 默认产物：
    - `data/t02_sources/northbound_tushare/`
  - 证据强度：
    - `hard`（成功 CSV 或失败 metadata 均为当前终端新跑证据）
- `fetch_t02_industry_map_tushare_v1.py`
  - 当前作用：
    - 复用 `TUSHARE_TOKEN` 合同，拉取 `stock_basic` 生成行业映射表
  - 默认输入：
    - `--list-status`
  - 默认产物：
    - `data/t02_sources/industry_tushare/`
  - 证据强度：
    - `hard`（成功 CSV 或失败 metadata 均为当前终端新跑证据）
- `run_t02_fund_flow_scan_v1.py`
  - 当前作用：
    - 扫描资金字段 CSV，输出 `T02` 连续主力资金触发摘要
  - 默认输入：
    - 运行时显式传入的资金 CSV
  - 默认产物：
    - `artifacts/t02_fund_flow_scan/`
  - 证据强度：
    - `hard`（当前终端新跑结果时）

### INDEX_NOTE

- `README.md`
- `runtime_execution_card_v1.md`
- `artifact_index_v1.tsv`
- `data/README.md`
- `data/t02_fund_flow_input_contract_v1.csv`
- `reports/*.md`
- `artifacts/README.md`

### ARTIFACT

- 当前尚未默认跟踪真实统计产物。
- 当 runner 首次生成结果后，至少要补：
  - `producer`
  - `scope`
  - `status`
  - `evidence_mode`

## 当前结果与缺口

- 当前已补第一份 `T01` fresh-run 结果：
  - `artifacts/t01_volume_price_scan/t01_volume_price_scan_summary_latest.json`
  - `artifacts/t01_volume_price_scan/t01_trigger_detail_latest.tsv`
  - `artifacts/t01_volume_price_scan/t01_daily_trigger_counts_latest.tsv`
  - `artifacts/t01_volume_price_scan/t01_symbol_trigger_counts_latest.tsv`
- `T01` 当前 smoke-run 口径：
  - 时间窗：`2025-05-08 -> 2026-05-08`
  - 输入目录：`butler_r0_ohlcv_object_cards/data/raw/daily_ohlcv/batch09_promoted/ashare_clean`
  - 当前摘要：`46` 个文件、`520` 条触发、`204` 个触发日、峰值日 `19`
- 当前已补第一份 `T01` 行业分布结果：
  - `artifacts/t01_industry_distribution/t01_industry_distribution_summary_latest.json`
  - `artifacts/t01_industry_distribution/t01_industry_trigger_counts_latest.tsv`
  - `artifacts/t01_industry_distribution/t01_symbol_industry_join_latest.tsv`
  - `artifacts/t01_industry_distribution/t01_unmatched_symbols_latest.tsv`
- `T01` 当前行业映射覆盖：
  - 匹配标的：`17/44`
  - 触发权重覆盖：`181/520`
  - 当前结论：仅适合做临时行业分布观察，不足以作为正式行业统计真值
- `T02` 当前已补统一输入合同模板：
  - `data/t02_fund_flow_input_contract_v1.csv`
- `T02` 当前已完成模板级 smoke-run 链：
  - 审计：`artifacts/t02_input_audit/t02_input_audit_summary_latest.json`
  - 归一化：`artifacts/t02_input_prepare/t02_fund_flow_input_normalized_latest.csv`
  - 扫描：`artifacts/t02_fund_flow_scan/t02_fund_flow_scan_summary_latest.json`
- `T02` 当前已完成宽表拼接 smoke-run：
  - 构建摘要：`artifacts/t02_real_input_build/t02_real_input_build_summary_latest.json`
  - 候选宽表：`artifacts/t02_real_input_build/t02_real_input_candidate_latest.csv`
- `T02` 当前模板级结论：
  - 字段合同已满足
  - 归一化链已贯通
  - runner 已能消费标准化输入
  - 仍缺真实资金宽表，模板级结果不用于阈值判断
- `T02` 当前拼接级结论：
  - 底表拼接链已贯通
  - 当前 `industry` 真源已接入，join 命中 `1`
  - 当前仍缺 `moneyflow / northbound / regime`
  - 下一步只差必需资金源和剩余增强源
- `T02` 当前抓取级结论：
  - 已补 `moneyflow / northbound / industry` 三条真实源抓取入口
  - 当前已补二轮实跑 metadata：
    - `data/t02_sources/moneyflow_tushare/t02_moneyflow_tushare__000001_SZ__20260501_20260531__metadata.json`
    - `data/t02_sources/northbound_tushare/t02_northbound_tushare__20260501_20260531__metadata.json`
    - `data/t02_sources/industry_tushare/t02_industry_map_tushare__list_status_L__metadata.json`
  - 当前实跑结果：
    - `moneyflow`：`failure_reason = tushare_api_error`，无 `moneyflow` 权限
    - `northbound`：`failure_reason = tushare_api_error`，无 `moneyflow_hsgt` 权限
    - `industry`：`status = success`，并已生成真实 CSV
- `T02` 当前预检级结论：
  - 已补 `artifacts/t02_tushare_preflight/t02_tushare_preflight_latest.json`
  - 当前作用是把 token/依赖阻塞前置成单独检查入口
  - 当前结果：
    - `token_present = true`
    - `pandas.available = true`
    - `tushare.available = true`
    - `token_source = C:\Users\91883\.tushare\token`
- `T02` 还缺首份真实资金字段输入 CSV
- 还未补统一批次汇总脚本

## 当前回链

- `artifact_index_v1.tsv`
- `runtime_execution_card_v1.md`
- `00_entry/A股_P0_离线验证执行卡__20260712.md`
