# vantharp_risk_p0_min_contract_v1

## 当前角色

- `DIAG_ONLY`
- 用于把 `VanTharp` 的 `R乘数 / 期望 / 头寸规模（风险额度对齐）` 固定成可审计的最小输入输出合同。
- 当前不接入交易执行链路，不生成下单建议，不修改仓位。

## 合同目标

- 把以下三件事变成可复核字段：
  - `R乘数 (r_multiple)`
  - `期望值 (expectancy_r)`
  - `头寸规模是否按风险额度对齐 (position_sizing_state)`

## 输入字段（proof_input）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 样本内唯一 id |
| symbol | string | yes | 标的 |
| entry_time | string | yes | ISO8601 |
| exit_time | string | yes | ISO8601 |
| account_equity | number | yes | 账户权益（货币单位自洽） |
| risk_percent | number | yes | 例如 `0.01` 代表 `1%` |
| initial_risk_source_mode | string | no | `statement_amount / entry_stop_calc`；缺省视为 `statement_amount` |
| initial_risk_amount | number | yes | 当 `initial_risk_source_mode=statement_amount` 时为真值输入；当 `entry_stop_calc` 时可留空 |
| entry_price | number | no | 当 `initial_risk_source_mode=entry_stop_calc` 时需要 |
| stop_price | number | no | 当 `initial_risk_source_mode=entry_stop_calc` 时需要 |
| position_size | number | no | 当 `initial_risk_source_mode=entry_stop_calc` 时需要（单位由 `risk_value_per_price_unit` 自洽） |
| risk_value_per_price_unit | number | no | 当 `initial_risk_source_mode=entry_stop_calc` 时需要：每 1.0 价格单位变动对应的盈亏金额 |
| gross_pnl | number | yes | 毛收益金额 |
| commission | number | yes | 手续费金额 |
| slippage | number | yes | 滑点金额 |
| expectancy_group_id | string | no | v2 proof 用于分组对照 |
| input_note | string | no | 备注 |

## 输出字段（proof_output）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 与输入对齐 |
| net_pnl | number | yes | `gross_pnl - commission - slippage` |
| max_risk_amount | number | yes | `account_equity * risk_percent` |
| initial_risk_amount_used | number | no | v2 proof 输出：用于计算的初始风险金额 |
| risk_usage_ratio | number | yes | `initial_risk_amount_used / max_risk_amount` |
| r_multiple | number | yes | `net_pnl / initial_risk_amount_used` |
| risk_model_state | string | yes | `valid / invalid / unknown` |
| position_sizing_state | string | yes | `conservative / acceptable / aggressive / unknown` |
| expectancy_group_id | string | yes | 当前 proof 样本组 id |
| expectancy_r | number | yes | 组内 `r_multiple` 的均值 |
| trade_count | number | yes | 组内交易数 |
| expectancy_confidence_state | string | yes | `low / medium / high` |
| proof_basis | string | yes | 本行依据简述 |

## 计算口径（v1）

- `net_pnl = gross_pnl - commission - slippage`
- `max_risk_amount = account_equity * risk_percent`
- `initial_risk_amount_used` 的确定：
  - `statement_amount`：`initial_risk_amount_used = initial_risk_amount`
  - `entry_stop_calc`：`initial_risk_amount_used = abs(entry_price - stop_price) * position_size * risk_value_per_price_unit`
- `risk_usage_ratio = initial_risk_amount_used / max_risk_amount`
- `r_multiple = net_pnl / initial_risk_amount_used`

## initial_risk_amount 口径冻结：两种最小合同补丁（v2）

### 模式 A：statement_amount（来自交割单/成交明细的金额字段）

- 必填输入（交易级）：
  - `initial_risk_source_mode=statement_amount`
  - `initial_risk_amount > 0`
- 必填输入（样本级）：
  - `account_equity > 0`
  - `risk_percent > 0`
  - `gross_pnl / commission / slippage`
- 输出冻结：
  - `initial_risk_amount_used = initial_risk_amount`

### 模式 B：entry_stop_calc（来自 entry/stop 换算）

- 必填输入（交易级）：
  - `initial_risk_source_mode=entry_stop_calc`
  - `entry_price` 与 `stop_price` 均可解析且 `entry_price != stop_price`
  - `position_size > 0`
  - `risk_value_per_price_unit > 0`
- 必填输入（样本级）：
  - `account_equity > 0`
  - `risk_percent > 0`
  - `gross_pnl / commission / slippage`
- 输出冻结：
  - `initial_risk_amount_used = abs(entry_price - stop_price) * position_size * risk_value_per_price_unit`

## 状态判定（v1）

### risk_model_state

- `valid`：
  - `account_equity > 0`
  - `risk_percent > 0`
- 且满足其一：
  - `initial_risk_source_mode=statement_amount` 且 `initial_risk_amount > 0`
  - `initial_risk_source_mode=entry_stop_calc` 且：
    - `position_size > 0`
    - `risk_value_per_price_unit > 0`
    - `entry_price` 与 `stop_price` 均可解析且 `entry_price != stop_price`
- `invalid`：任一为 `<= 0`
- `unknown`：字段缺失或无法解析

### position_sizing_state

在 `risk_model_state = valid` 前提下：

- `conservative`：`risk_usage_ratio < 0.7`
- `acceptable`：`0.7 <= risk_usage_ratio <= 1.1`
- `aggressive`：`risk_usage_ratio > 1.1`

否则为 `unknown`。

### expectancy_confidence_state

- `low`：`trade_count < 30`
- `medium`：`30 <= trade_count < 100`
- `high`：`trade_count >= 100`

## 当前边界

- `initial_risk_amount` 当前允许两种口径：
  - `statement_amount`：直接输入金额
  - `entry_stop_calc`：由 `entry/stop/position_size/risk_value_per_price_unit` 换算
- v1 不引入品种点值库或汇率换算，`risk_value_per_price_unit` 必须由输入方保证自洽。
- `expectancy_r` 当前按“proof 样本组内均值”冻结，不引入 bootstrap/置信区间。
