# T02 主力资金主触发结果页 stub v1

## 对应验证项

- `T02`
- `V02`

## 当前预留结构

- 输入模板：
  - `data/t02_fund_flow_input_contract_v1.csv`
- 当前链路验证：
  - 输入审计通过：`contract_ready = true`
  - 归一化通过：`missing_columns = []`
  - 模板级 smoke-run：`1` 行输入、`0` 条触发
  - 真实源抓取实跑：`moneyflow_batch=180` 行、`northbound=17` 行、`regime=18` 行、`industry=5530` 行
  - 当前真实宽表：`180` 行候选宽表，`northbound=170` 命中，`regime=180` 命中，`industry=180` 命中
  - 当前真实扫描：`180` 行输入、`84` 条触发、`10` 个触发标的
- 验证范围：
  - 当前覆盖模板级链路贯通验证
  - 当前覆盖第二批更宽样本的真实源抓取、真实宽表拼接和第三轮真实扫描
- 输入口径：
  - `主力资金连续2日 + 占成交额 > 3%` 的最小执行链已可跑
- 核心结果：
  - 已拿到首份 `10` 标的真实 `moneyflow / northbound / regime / industry` 输入链
  - 当前阈值口径 `绝对占成交额 > 3% 且连续2日` 在 `10/10` 标的样本上都出现了可解释触发
  - 当前触发分布：`000001.SZ=12`、`601318.SH=11`、`000002.SZ=9`、`000651.SZ=9`、`600030.SH=8`、`600276.SH=8`、`601899.SH=8`、`600050.SH=7`、`600519.SH=7`、`300750.SZ=5`
  - 当前阶段分布：`G01_普涨=23`、`G02_普跌=17`、`G03_震荡=44`
  - 从 `5` 标的 `41/90` 到 `10` 标的 `84/180`，触发密度约从 `45.6%` 变到 `46.7%`
  - 当前扩样结论：阈值没有在 `5 -> 10` 标的扩样时明显失真
  - preflight 已确认：`token_present = true`，`pandas` 与 `tushare` 已可用
- 抽样观察：
  - 当前模板包含完整标准列名，可作为真实输入的最小对齐合同
  - 当前宽表拼接脚本已可消费：
    - `base_ohlcv`
    - `moneyflow`
    - `northbound`
    - `regime`
    - `industry`
  - `moneyflow` metadata 已固定比例口径：
    - `main_fund_net_inflow_ratio = net_mf_amount / (daily.amount / 10.0)`
  - 当前批量样本覆盖：`银行 / 券商 / 地产 / 消费 / 新能源 / 保险 / 家电 / 医药 / 有色 / 通信`
  - 当前 `northbound` 采用 `trade_date` 级 join，`180` 行里命中 `170` 行
  - 当前 `regime` 采用 `trade_date` 级代理表，`180` 行里命中 `180` 行
  - 当前 `symbol x regime` 交叉分布已落盘，可直接看哪个标的只在单一阶段触发
  - 当前最长连续触发为 `12` 个交易日，仍来自 `000001.SZ` 且方向为 `outflow`
- 结论判断：
  - 当前建议：`保留`
  - 保留原因：阈值链路已在更宽行业真实样本上形成一致可解释触发，并且在 `G01 / G02 / G03` 三类阶段都有可消费信号
  - 当前限制：样本仍只覆盖 `10` 个标的、`18` 个交易日；当前 `regime` 仍是宽基指数代理，不是完整 breadth engine
- 下一步动作：
  - 继续扩到更多标的，优先补宽行业和大中小盘混合样本
  - 复用 `fetch_t02_moneyflow_batch_tushare_v1.py` 批量生成更多 `moneyflow` 真实 CSV
  - 若继续增强 `regime`，可再补上涨/下跌家数或更细宽基代理
  - 在更大样本上复核 `3% + 连续2日` 是否过宽或过严

## 回链

- 输出模板：
  - `00_entry/A股_P0_离线验证输出模板__20260712.md`
- 结论门槛：
  - `00_entry/A股_P0_离线验证结论门槛__20260712.md`
- 输入审计摘要：
  - `artifacts/t02_input_audit/t02_input_audit_summary_latest.json`
- 输入归一化结果：
  - `artifacts/t02_input_prepare/t02_fund_flow_input_normalized_latest.csv`
- 宽表拼接摘要：
  - `artifacts/t02_real_input_build/t02_real_input_build_summary_latest.json`
- 候选真实宽表：
  - `artifacts/t02_real_input_build/t02_real_input_candidate_latest.csv`
- 模板级 scan 摘要：
  - `artifacts/t02_fund_flow_scan/t02_fund_flow_scan_summary_latest.json`
- Tushare 环境预检：
  - `artifacts/t02_tushare_preflight/t02_tushare_preflight_latest.json`
- moneyflow 抓取 metadata：
  - `data/t02_sources/moneyflow_tushare/t02_moneyflow_tushare_batch__sample10__20260501_20260531__metadata.json`
- moneyflow 真实 CSV：
  - `data/t02_sources/moneyflow_tushare/t02_moneyflow_tushare_batch__sample10__20260501_20260531.csv`
- 多标的样本清单：
  - `data/t02_multi_symbol_sample_v2.csv`
- northbound 抓取 metadata：
  - `data/t02_sources/northbound_tushare/t02_northbound_tushare__20260501_20260531__metadata.json`
- northbound 真实 CSV：
  - `data/t02_sources/northbound_tushare/t02_northbound_tushare__20260501_20260531.csv`
- regime 抓取 metadata：
  - `data/t02_sources/regime/t02_regime_proxy_tushare__000300_SH__20260501_20260531__metadata.json`
- regime 真实 CSV：
  - `data/t02_sources/regime/t02_regime_proxy_tushare__000300_SH__20260501_20260531.csv`
- industry 抓取 metadata：
  - `data/t02_sources/industry_tushare/t02_industry_map_tushare__list_status_L__metadata.json`
- industry 真实 CSV：
  - `data/t02_sources/industry_tushare/t02_industry_map_tushare__list_status_L.csv`
- symbol x regime 统计：
  - `artifacts/t02_fund_flow_scan/t02_symbol_regime_trigger_counts_latest.tsv`
- 扩样稳定性对比：
  - `artifacts/t02_fund_flow_scan/t02_sample_expansion_comparison_latest.tsv`
