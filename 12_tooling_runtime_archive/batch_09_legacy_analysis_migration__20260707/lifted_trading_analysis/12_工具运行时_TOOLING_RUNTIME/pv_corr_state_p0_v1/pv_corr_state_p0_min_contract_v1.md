# PV Corr State P0 最小合同 v1

- ARCHIVE_ONLY_MIN_CONTRACT: 本文件只保留旧 `PV Corr State P0` 的历史最小合同，不作为当前默认接线入口。
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 历史角色

- `DIAG_ONLY`
- 用于把 `高频价量相关性因子` 固定成可审计的最小输入输出合同。
- 历史上不接入交易执行链路，不生成交易信号，不修改仓位。

## 合同目标

- 把以下三件事变成可复核字段：
  - `价量相关性得分 (pv_corr_score)`
  - `价量同步状态 (pv_sync_state)`
  - `价量压力偏向 (pv_pressure_bias)`

## 输入字段（proof_input）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 样本内唯一 id |
| symbol | string | yes | 标的 |
| timeframe | string | yes | 例如 `H1 / H4 / D1` |
| bar_time | string | yes | ISO8601 |
| window_bars | number | yes | 固定窗口长度 |
| pv_corr_score | number | yes | 固定窗口内价格收益与量变化相关性 |
| price_net_change | number | yes | 窗口内净价格变化代理 |
| volume_net_change | number | yes | 窗口内净量变化代理；FX 可允许 `tick_volume` 代理 |
| input_note | string | no | 备注 |

## 输出字段（proof_output）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 与输入对齐 |
| pv_sync_state | string | yes | `confirm / diverge / neutral / unknown` |
| pv_pressure_bias | string | yes | `up_confirm / down_confirm / mixed / none / unknown` |
| pv_extreme_flag | string | yes | `price_up_volume_down / price_down_volume_up / none / unknown` |
| pv_model_state | string | yes | `valid / invalid / unknown` |
| proof_basis | string | yes | 本行依据简述 |

## 计算口径（v1）

- 历史 proof 不重算 `pv_corr_score`，只冻结其标签映射口径。
- `pv_corr_score` 视为上游固定窗口相关性统计结果。

## 状态判定（v1）

### pv_model_state

- `valid`：
  - `window_bars > 0`
  - `pv_corr_score` 可解析
  - `price_net_change` 可解析
  - `volume_net_change` 可解析
- `invalid`：任一字段无法满足上面条件
- `unknown`：字段缺失

### pv_sync_state

在 `pv_model_state = valid` 前提下：

- `confirm`：
  - `abs(pv_corr_score) >= 0.30`
  - 且 `price_net_change` 与 `volume_net_change` 同号
- `diverge`：
  - `abs(pv_corr_score) >= 0.30`
  - 且 `price_net_change` 与 `volume_net_change` 异号
- `neutral`：
  - `abs(pv_corr_score) < 0.30`
- 否则：`unknown`

### pv_pressure_bias

在 `pv_model_state = valid` 前提下：

- `up_confirm`：
  - `pv_sync_state = confirm`
  - 且 `price_net_change > 0`
- `down_confirm`：
  - `pv_sync_state = confirm`
  - 且 `price_net_change < 0`
- `mixed`：
  - `pv_sync_state = diverge`
- `none`：
  - `pv_sync_state = neutral`
- 否则：`unknown`

### pv_extreme_flag

在 `pv_model_state = valid` 前提下：

- `price_up_volume_down`：
  - `price_net_change > 0`
  - `volume_net_change < 0`
- `price_down_volume_up`：
  - `price_net_change < 0`
  - `volume_net_change > 0`
- `none`：
  - 其余情况
- 否则：`unknown`

## 历史边界

- v1 只冻结“价量相关性 -> 标签”的最小映射，不证明最优窗口或最优阈值。
- v1 只作为：
  - `price-volume diagnostic label`
  - `confirm/diverge observation layer`
- 不直接进入：
  - 入场规则
  - 多因子打分
  - 主线默认 gate
