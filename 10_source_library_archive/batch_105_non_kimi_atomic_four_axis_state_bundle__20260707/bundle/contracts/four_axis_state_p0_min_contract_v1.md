# four_axis_state_p0_min_contract_v1

## 当前角色

- `DIAG_ONLY`
- 用于把“四轴状态模板”固定成可审计的最小诊断输入输出合同。
- 当前不接入交易门控，不生成仓位建议，不修改执行链路。

## 合同目标

- 把以下六个状态字段收成可复核输出：
  - `trend_existence_state`
  - `breakout_validity_state`
  - `volatility_regime_state`
  - `crowd_extremity_state`
  - `transaction_cost_load_state`
  - `liquidity_adequacy_state`

## 输入字段（proof_input）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 样本内唯一 id |
| symbol | string | yes | 标的 |
| bar_time | string | yes | ISO8601 |
| timeframe | string | yes | 例如 `H1 / D1` |
| close_price | number | yes | 当前价格 |
| atr_pct_20 | number | yes | 20 窗口 ATR 占收盘价比例 |
| breakout_strength_20 | number | yes | 突破强度代理，`0-1` |
| crowd_extremity_z | number | yes | 情绪/拥挤度代理 z-score |
| spread_bps | number | yes | 点差成本，bps |
| liquidity_depth_ratio | number | yes | 流动性深度代理，`>1` 越充足 |
| trend_slope_20 | number | yes | 20 窗口斜率代理，正负代表方向 |
| input_note | string | no | 备注 |

## 输出字段（proof_output）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 与输入对齐 |
| trend_existence_state | string | yes | `trend_up / trend_down / no_trend / unknown` |
| breakout_validity_state | string | yes | `valid / false_breakout_risk / unknown` |
| volatility_regime_state | string | yes | `low / normal / high / shock` |
| crowd_extremity_state | string | yes | `overbought / oversold / neutral / unknown` |
| transaction_cost_load_state | string | yes | `acceptable / heavy / unknown` |
| liquidity_adequacy_state | string | yes | `adequate / thin / unknown` |
| proof_basis | string | yes | 本行判定依据简述 |

## 最小判定口径（v1）

- `trend_existence_state`
  - `trend_up`: `trend_slope_20 > 0.002`
  - `trend_down`: `trend_slope_20 < -0.002`
  - `no_trend`: `abs(trend_slope_20) <= 0.002`
- `breakout_validity_state`
  - `valid`: `breakout_strength_20 >= 0.7` 且 `liquidity_depth_ratio >= 1.0`
  - `false_breakout_risk`: `breakout_strength_20 < 0.7` 或 `liquidity_depth_ratio < 1.0`
- `volatility_regime_state`
  - `low`: `atr_pct_20 < 0.005`
  - `normal`: `0.005 <= atr_pct_20 < 0.015`
  - `high`: `0.015 <= atr_pct_20 < 0.03`
  - `shock`: `atr_pct_20 >= 0.03`
- `crowd_extremity_state`
  - `overbought`: `crowd_extremity_z >= 1.0`
  - `oversold`: `crowd_extremity_z <= -1.0`
  - `neutral`: 其余
- `transaction_cost_load_state`
  - `acceptable`: `spread_bps <= 8`
  - `heavy`: `spread_bps > 8`
- `liquidity_adequacy_state`
  - `adequate`: `liquidity_depth_ratio >= 1.0`
  - `thin`: `liquidity_depth_ratio < 1.0`

## 当前边界

- 所有阈值当前都是 `proof-ready proxy threshold`，不是正式实盘阈值。
- v1 只验证“字段能否冻结成合同”，不验证这些阈值是否最优。
- 若后续进入 runtime 层，必须补来源锚点段落与失败条件。
