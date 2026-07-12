# group08_event_driven_p0_min_contract_v1

- CONTRACT_ROLE: `CONTRACT_FROZEN / NOT_RUNTIME_DEFAULT`
- 当前只冻结 `GROUP_08` 事件驱动线的最小输入输出，不直接进入主线默认执行。

## 合同目标

- 把以下内容固定成可复核字段：
  - `事件类型 (event_type)`
  - `事件确认时点 (event_confirm_date)`
  - `事件驱动偏向 (event_bias)`
  - `建议持有期 (hold_horizon_days)`
  - `事件模型状态 (event_model_state)`

## 输入字段（proof_input）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 样本内唯一 id |
| symbol | string | yes | 标的 |
| event_type | string | yes | `earnings_preview / index_rebalance / shareholder_increase / equity_incentive / unknown` |
| announcement_date | string | yes | 公告日 |
| confirmation_date | string | yes | 事件可交易确认日，通常不早于公告后首个交易日 |
| market_regime_label | string | no | `bull / bear / range / unknown` 或项目映射标签 |
| pre_event_excess_return_5d | number | no | 公告前5日超额收益，用于反转过滤 |
| shareholder_type | string | no | 大股东事件使用，如 `executive / company / person / unknown` |
| position_change_ratio | number | no | 增持变动比例 |
| original_holding_ratio | number | no | 原始持股占比 |
| input_note | string | no | 备注 |

## 输出字段（proof_output）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 与输入对齐 |
| event_bias | string | yes | `positive_reversal / positive_follow / negative_or_skip / observe / unknown` |
| hold_horizon_days | number | yes | 推荐持有期，默认候选 `1 / 3 / 5 / 10 / 14` |
| entry_timing_rule | string | yes | `next_trading_day_avg / t_plus_1_close / weekly_open / unknown` |
| event_filter_tag | string | yes | `turnaround / pre_decline_reversal / high_ratio_increase / executive_signal / unknown` |
| event_model_state | string | yes | `valid / partial / invalid / unknown` |
| proof_basis | string | yes | 本行依据简述 |

## 计算与冻结口径（v1）

- `earnings_preview`
  - 优先关注：`扭亏 / 预减反转`
  - 建议持有期优先：`5`
- `index_rebalance`
  - 事件确认时点按样本股调整公告与生效日处理
- `shareholder_increase`
  - 优先关注：
    - `shareholder_type in {executive, person}`
    - `position_change_ratio >= 0.8_quantile`
    - `original_holding_ratio <= 0.02`
  - 建议持有期优先：`14`
- `equity_incentive`
  - 当前只冻结为可观察事件，不扩写完整定价模型

## 状态判定（v1）

- `valid`
  - `trade_id / symbol / event_type / announcement_date / confirmation_date` 完整
- `partial`
  - 基础字段完整，但事件过滤字段不完整
- `invalid`
  - 基础字段缺失或无法确认事件类型
- `unknown`
  - 字段无法解析

## 历史边界

- v1 只冻结最小映射，不复刻论文完整收益曲线。
- v1 不直接进入：
  - 默认选股执行器
  - 默认事件组合止损器
  - 默认 runtime 门控
