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
  - 宽表拼接现状：`1` 行候选宽表，`industry=1` 命中，`moneyflow / northbound / regime` 仍待接入
  - 真实源抓取实跑：`3` 条 fetcher 已尝试，`industry` 已成功，`moneyflow / northbound` 已落权限失败 metadata
- 验证范围：
  - 当前覆盖模板级链路贯通验证
  - 当前覆盖真实源抓取入口和失败态落证
- 输入口径：
  - `主力资金连续2日 + 占成交额 > 3%` 的最小执行链已可跑
- 核心结果：
  - 真实资金宽表尚未接入
  - 当前模板级结果不用于阈值判断
  - `moneyflow` 抓取已进入真实权限校验，但当前账号无 `moneyflow` 接口权限
  - `northbound` 抓取已进入真实权限校验，但当前账号无 `moneyflow_hsgt` 接口权限
  - `industry` 抓取成功，已生成 `5530` 行真实行业映射 CSV
  - preflight 已确认：`token_present = true`，`pandas` 与 `tushare` 已可用
- 抽样观察：
  - 当前模板包含完整标准列名，可作为真实输入的最小对齐合同
  - 当前宽表拼接脚本已可消费：
    - `base_ohlcv`
    - `moneyflow`
    - `northbound`
    - `regime`
    - `industry`
  - 当前只差真实源表，不差拼接入口
  - `moneyflow` metadata 已固定比例口径：
    - `main_fund_net_inflow_ratio = net_mf_amount / (daily.amount / 10.0)`
  - 当前阻塞已从“token 缺失”压成“账号权限不足”
  - 已成功把 `industry` 真源接进候选宽表，当前候选行的 `industry_name = 银行`
- 结论判断：
  - 当前建议：`暂缓`
  - 暂缓原因：`moneyflow` 仍是必需字段，但当前账号权限不足，无法生成首份真实主力资金宽表
- 下一步动作：
  - 若继续走 `Tushare` 主线：先补 `moneyflow / moneyflow_hsgt` 对应权限
  - 补权限后重新跑三条 Tushare fetcher，先拿到首份 `moneyflow` 真实 CSV
  - 回填 `data/t02_real_input_sources_manifest_v1.tsv`
  - 再用 `build_t02_real_input_v1.py` 生成首份候选真实宽表
  - 用同一链路再跑首份真实 `T02` 结果
  - 按市场阶段补 `market_regime_label`

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
- northbound 抓取 metadata：
  - `data/t02_sources/northbound_tushare/t02_northbound_tushare__20260501_20260531__metadata.json`
- industry 抓取 metadata：
  - `data/t02_sources/industry_tushare/t02_industry_map_tushare__list_status_L__metadata.json`
