# rsj_state_p0_min_contract_v1

- ARCHIVE_ONLY_MIN_CONTRACT: 本文件只保留旧 `RSJ State P0` 的历史最小合同，不作为当前默认接线入口。
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 历史角色

- `DIAG_ONLY`
- 用于把 `RSJ 市场情绪冷暖剂` 固定成可审计的最小输入输出合同。
- 历史上不接入交易执行链路，不生成交易信号，不修改仓位。

## 合同目标

- 把以下三件事变成可复核字段：
  - `RSJ 数值 (rsj_score)`
  - `RSJ 状态 (rsj_state)`
  - `RSJ 择时偏向 (rsj_timing_bias)`

## 输入字段（proof_input）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 样本内唯一 id |
| symbol | string | yes | 标的 |
| timeframe | string | yes | 例如 `H1 / H4 / D1` |
| bar_time | string | yes | ISO8601 |
| window_bars | number | yes | 统计窗口长度 |
| rv_up | number | yes | 窗口内正收益侧已实现波动代理 |
| rv_down | number | yes | 窗口内负收益侧已实现波动代理 |
| input_note | string | no | 备注 |

## 输出字段（proof_output）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 与输入对齐 |
| rsj_score | number | yes | ` (rv_up - rv_down) / (rv_up + rv_down) ` |
| rsj_state | string | yes | `warm / cold / neutral / unknown` |
| rsj_extreme_flag | string | yes | `extreme_high / extreme_low / none / unknown` |
| rsj_timing_bias | string | yes | `risk_on / risk_off / wait / unknown` |
| rsj_model_state | string | yes | `valid / invalid / unknown` |
| proof_basis | string | yes | 本行依据简述 |

## 计算口径（v1）

- `rsj_score = (rv_up - rv_down) / (rv_up + rv_down)`
- 当 `rv_up + rv_down <= 0` 时：
  - `rsj_model_state = invalid`
  - 其余状态字段为 `unknown`

## 状态判定（v1）

### rsj_model_state

- `valid`：
  - `window_bars > 0`
  - `rv_up >= 0`
  - `rv_down >= 0`
  - `rv_up + rv_down > 0`
- `invalid`：任一字段不满足上面条件
- `unknown`：字段缺失或无法解析

### rsj_state

在 `rsj_model_state = valid` 前提下：

- `warm`：`rsj_score >= 0.20`
- `cold`：`rsj_score <= -0.20`
- `neutral`：`-0.20 < rsj_score < 0.20`
- 否则：`unknown`

### rsj_extreme_flag

在 `rsj_model_state = valid` 前提下：

- `extreme_high`：`rsj_score >= 0.50`
- `extreme_low`：`rsj_score <= -0.50`
- `none`：其余情况
- 否则：`unknown`

### rsj_timing_bias

在 `rsj_model_state = valid` 前提下：

- `risk_on`：`rsj_state = warm`
- `risk_off`：`rsj_state = cold`
- `wait`：`rsj_state = neutral`
- 否则：`unknown`

## 历史边界

- v1 只冻结 `RSJ` 的最小映射口径，不重建完整论文级实现。
- `rv_up / rv_down` 在历史合同里视为上游已可获得的窗口统计量；v1 proof 不展开逐笔或分钟明细重算。
- v1 只作为：
  - `volatility/emotion label`
  - `diag-only timing bias`
- 不直接进入：
  - 入场规则
  - 仓位倍率
  - 主线默认 gate
