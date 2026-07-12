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
  - 真实源抓取实跑：`moneyflow_batch=90` 行、`northbound=17` 行、`industry=5530` 行
  - 当前真实宽表：`90` 行候选宽表，`northbound=85` 命中，`industry=90` 命中
  - 当前真实扫描：`90` 行输入、`41` 条触发、`5` 个触发标的
- 验证范围：
  - 当前覆盖模板级链路贯通验证
  - 当前覆盖多标的真实源抓取、真实宽表拼接和第二轮真实扫描
- 输入口径：
  - `主力资金连续2日 + 占成交额 > 3%` 的最小执行链已可跑
- 核心结果：
  - 已拿到首份 `5` 标的真实 `moneyflow / northbound / industry` 输入链
  - 当前阈值口径 `绝对占成交额 > 3% 且连续2日` 在 `5/5` 标的样本上都出现了可解释触发
  - 当前触发分布：`000001.SZ=12`、`000002.SZ=9`、`600030.SH=8`、`600519.SH=7`、`300750.SZ=5`
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
  - 当前批量样本覆盖：`银行 / 券商 / 地产 / 消费 / 新能源`
  - 当前 `northbound` 采用 `trade_date` 级 join，`90` 行里命中 `85` 行
  - 当前最长连续触发为 `12` 个交易日，仍来自 `000001.SZ` 且方向为 `outflow`
- 结论判断：
  - 当前建议：`保留`
  - 保留原因：阈值链路已在多行业真实样本上形成一致可解释触发，当前没有被“扩样本即失效”否掉
  - 当前限制：样本仍只覆盖 `5` 个标的、`18` 个交易日，且未补 `market_regime_label`
- 下一步动作：
  - 继续扩到更多标的，优先补宽行业和大中小盘混合样本
  - 复用 `fetch_t02_moneyflow_batch_tushare_v1.py` 批量生成更多 `moneyflow` 真实 CSV
  - 补 `market_regime_label`
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
  - `data/t02_sources/moneyflow_tushare/t02_moneyflow_tushare_batch__sample5__20260501_20260531__metadata.json`
- moneyflow 真实 CSV：
  - `data/t02_sources/moneyflow_tushare/t02_moneyflow_tushare_batch__sample5__20260501_20260531.csv`
- 多标的样本清单：
  - `data/t02_multi_symbol_sample_v1.csv`
- northbound 抓取 metadata：
  - `data/t02_sources/northbound_tushare/t02_northbound_tushare__20260501_20260531__metadata.json`
- northbound 真实 CSV：
  - `data/t02_sources/northbound_tushare/t02_northbound_tushare__20260501_20260531.csv`
- industry 抓取 metadata：
  - `data/t02_sources/industry_tushare/t02_industry_map_tushare__list_status_L__metadata.json`
- industry 真实 CSV：
  - `data/t02_sources/industry_tushare/t02_industry_map_tushare__list_status_L.csv`
