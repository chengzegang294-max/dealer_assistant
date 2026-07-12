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
  - 真实源抓取实跑：`moneyflow=18` 行、`northbound=17` 行、`industry=5530` 行
  - 首轮真实宽表：`18` 行候选宽表，`northbound=17` 命中，`industry=18` 命中
  - 首轮真实扫描：`18` 行输入、`12` 条触发、`1` 个触发标的
- 验证范围：
  - 当前覆盖模板级链路贯通验证
  - 当前覆盖真实源抓取、真实宽表拼接和首轮真实扫描
- 输入口径：
  - `主力资金连续2日 + 占成交额 > 3%` 的最小执行链已可跑
- 核心结果：
  - 已拿到首份真实 `moneyflow / northbound / industry` 输入链
  - 首轮真实窄样本显示：`000001.SZ` 在 `2026-05` 出现持续主力资金净流出
  - 当前阈值口径 `绝对占成交额 > 3% 且连续2日` 在该样本上被多次触发
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
  - 当前已成功把 `industry` 真源接进候选宽表，样本标的行业为 `银行`
  - 当前 `northbound` 采用 `trade_date` 级 join，`18` 行里命中 `17` 行
  - 当前最长连续触发为 `12` 个交易日，方向均为 `outflow`
- 结论判断：
  - 当前建议：`保留`
  - 保留原因：阈值链路已在真实样本上形成可解释触发，下一步应扩样本而不是回退模板级
  - 当前限制：样本仍只覆盖 `1` 个标的、`18` 个交易日，不足以直接外推出全市场门槛
- 下一步动作：
  - 扩到多标的样本，先覆盖银行、券商、地产等高资金敏感行业
  - 按相同链路批量生成更多 `moneyflow` 真实 CSV
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
  - `data/t02_sources/moneyflow_tushare/t02_moneyflow_tushare__000001_SZ__20260501_20260531__metadata.json`
- moneyflow 真实 CSV：
  - `data/t02_sources/moneyflow_tushare/t02_moneyflow_tushare__000001_SZ__20260501_20260531.csv`
- northbound 抓取 metadata：
  - `data/t02_sources/northbound_tushare/t02_northbound_tushare__20260501_20260531__metadata.json`
- northbound 真实 CSV：
  - `data/t02_sources/northbound_tushare/t02_northbound_tushare__20260501_20260531.csv`
- industry 抓取 metadata：
  - `data/t02_sources/industry_tushare/t02_industry_map_tushare__list_status_L__metadata.json`
- industry 真实 CSV：
  - `data/t02_sources/industry_tushare/t02_industry_map_tushare__list_status_L.csv`
