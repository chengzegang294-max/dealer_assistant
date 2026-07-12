# group08_market_timing_p0_min_contract_v1

- CONTRACT_ROLE: `CONTRACT_FROZEN / NOT_RUNTIME_DEFAULT`
- 当前只冻结 `GROUP_08` 市场择时线的最小输入输出，不直接进入主线默认执行。

## 合同目标

- 把以下内容固定成可复核字段：
  - `择时信号类型 (timing_signal_type)`
  - `信号状态 (timing_signal_state)`
  - `择时偏向 (timing_bias)`
  - `建议持有期 (hold_horizon_weeks)`
  - `择时模型状态 (timing_model_state)`

## 输入字段（proof_input）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 样本内唯一 id |
| signal_date | string | yes | 信号日期 |
| timing_signal_type | string | yes | `market_consistency_r2 / industrial_capital_flow / unknown` |
| csi300_return | number | no | 沪深300日收益或区间收益 |
| r2_value | number | no | 市场一致性指标 |
| r2_trend | string | no | `rising / falling / flat / unknown` |
| industrial_capital_net_value | number | no | 产业资本净增减持净值 |
| rolling_increase_7d | number | no | 7日累计增持 |
| rolling_decrease_7d | number | no | 7日累计减持 |
| rolling_increase_14d | number | no | 14日累计增持 |
| rolling_decrease_14d | number | no | 14日累计减持 |
| rolling_increase_30d | number | no | 30日累计增持 |
| rolling_decrease_30d | number | no | 30日累计减持 |
| input_note | string | no | 备注 |

## 输出字段（proof_output）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 与输入对齐 |
| timing_signal_state | string | yes | `greed / fear / warning / reversal / neutral / unknown` |
| timing_bias | string | yes | `trend_follow / reverse_long / reverse_short / observe / unknown` |
| hold_horizon_weeks | number | yes | 推荐持有期候选，默认 `1~10` 周 |
| confidence_note | string | yes | 参数完备度与置信说明 |
| timing_model_state | string | yes | `valid / partial / invalid / unknown` |
| proof_basis | string | yes | 本行依据简述 |

## 计算与冻结口径（v1）

- `market_consistency_r2`
  - `r2_value` 是核心输入
  - 当前只冻结：
    - `greed / fear` 状态解释
    - `warning / reversal` 两类信号
  - 不冻结：
    - 论文未披露的精确阈值
- `industrial_capital_flow`
  - 当前只冻结：
    - `7 / 14 / 30` 日累计增减持
    - 净增减持净值
    - 后验均值与不确定性作为可选扩展
  - 不冻结：
    - 完整贝叶斯相关矩阵
    - 未披露修正系数

## 状态判定（v1）

- `valid`
  - `trade_id / signal_date / timing_signal_type` 完整
  - 且对应核心输入至少一类可解析
- `partial`
  - 基础字段完整，但参数或扩展字段不足
- `invalid`
  - 核心输入缺失或信号类型无法确认
- `unknown`
  - 字段无法解析

## 历史边界

- v1 只冻结最小映射，不证明最优持有期和最优阈值。
- v1 不直接进入：
  - 主线默认择时 gate
  - 默认仓位控制器
  - 实时交易脚本
