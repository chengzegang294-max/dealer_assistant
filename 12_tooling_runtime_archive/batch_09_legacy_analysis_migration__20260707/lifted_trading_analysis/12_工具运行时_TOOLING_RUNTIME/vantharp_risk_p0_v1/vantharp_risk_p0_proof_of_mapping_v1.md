# VanTharp Risk P0 映射证明 v1

## 目的

- 用一组手工样本证明 `vantharp_risk_p0_min_contract_v1` 的字段映射可复核。
- 当前 proof 样本不代表真实 broker 交割单或真实运行时落盘，只用于映射核对。

## 文件

- proof_input：
  - `real_input_samples\vantharp_risk_p0_proof_input_v1.csv`
  - `real_input_samples\vantharp_risk_p0_proof_input_v2.csv`（双口径对照）
- proof_output：
  - `real_input_samples\vantharp_risk_p0_proof_output_v1.csv`
  - `real_input_samples\vantharp_risk_p0_proof_output_v2.csv`（双口径对照）
- 输出表头冻结：
  - `vantharp_risk_p0_fields_output_header_v1.txt`
  - `vantharp_risk_p0_fields_output_header_v2.txt`

## proof 样本组

- expectancy_group_id：`VT_RISK_P0_PROOF_V1`
- trade_count：`5`
- expectancy_r：`0.5`
- expectancy_confidence_state：`low`

v2 双口径对照：

- `VT_RISK_P0_V2_STATEMENT`
  - `initial_risk_source_mode=statement_amount`
  - trade_count：`3`
  - expectancy_r：`0.5833`
  - expectancy_confidence_state：`low`
- `VT_RISK_P0_V2_ENTRY_STOP`
  - `initial_risk_source_mode=entry_stop_calc`
  - trade_count：`3`
  - expectancy_r：`0.1667`
  - expectancy_confidence_state：`low`

## 映射核对点

- `net_pnl = gross_pnl - commission - slippage`
- `max_risk_amount = account_equity * risk_percent`
- `initial_risk_amount_used`：
  - `statement_amount`：`initial_risk_amount_used = initial_risk_amount`
  - `entry_stop_calc`：`initial_risk_amount_used = abs(entry_price - stop_price) * position_size * risk_value_per_price_unit`
- `risk_usage_ratio = initial_risk_amount_used / max_risk_amount`
- `r_multiple = net_pnl / initial_risk_amount_used`
- `position_sizing_state`：
  - `risk_usage_ratio < 0.7` -> `conservative`
  - `0.7 <= risk_usage_ratio <= 1.1` -> `acceptable`
  - `risk_usage_ratio > 1.1` -> `aggressive`

## 当前边界

- v1/v2 均不重建品种点值库或汇率换算，`risk_value_per_price_unit` 必须由输入方保证自洽。
- v1 的 `expectancy_r` 只做样本组均值，不做置信区间。
