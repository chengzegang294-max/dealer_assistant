# group08_dynamic_factor_validity_p0_min_contract_v1

- CONTRACT_ROLE: `CONTRACT_FROZEN / NOT_RUNTIME_DEFAULT`
- 当前只冻结 `GROUP_08` 动态因子有效性线的最小输入输出，不直接进入主线默认执行。

## 合同目标

- 把以下内容固定成可复核字段：
  - `动态评估家族 (dynamic_eval_family)`
  - `Spearman 序列 (spearman_corr_series)`
  - `Kalman 状态 (kalman_state)`
  - `因子强弱指数 (factor_strength_index)`
  - `净换手率候选输入 (net_turnover_ratio)`
  - `模型状态 (dynamic_model_state)`

## 输入字段（proof_input）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 样本内唯一 id |
| signal_date | string | yes | 信号日期 |
| factor_name | string | yes | 因子名称 |
| dynamic_eval_family | string | yes | `kalman_tracking / strength_index / net_turnover_candidate / unknown` |
| spearman_corr_value | number | no | 截面 Spearman 相关系数 |
| kalman_state_value | number | no | Kalman 估计状态值 |
| p_value | number | no | 对比基准可选输入 |
| factor_strength_index | number | no | 因子有效性强弱指数 |
| net_turnover_ratio | number | no | 净换手率定义值 |
| market_scope | string | no | `hs300 / sh_market / all_market / unknown` |
| input_note | string | no | 备注 |

## 输出字段（proof_output）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 与输入对齐 |
| dynamic_factor_state | string | yes | `effective / weakening / ineffective / observe / unknown` |
| factor_selection_bias | string | yes | `keep / add / drop / observe / unknown` |
| recommended_action | string | yes | `use_in_selection / watchlist_only / future_only / unknown` |
| confidence_note | string | yes | 参数完备度与置信说明 |
| dynamic_model_state | string | yes | `valid / partial / invalid / unknown` |
| proof_basis | string | yes | 本行依据简述 |

## 计算与冻结口径（v1）

- `kalman_tracking`
  - 当前只冻结：
    - Spearman 相关系数时间序列
    - Kalman Filter 状态跟踪
    - 每期有效因子列表的映射口径
  - 不冻结：
    - 论文未披露的完整状态空间参数
- `strength_index`
  - 当前只冻结：
    - 因子有效性强弱指数
    - 分组检验得到的有效/失效判断
  - 不冻结：
    - 尾部相关系数的风控接线
- `net_turnover_candidate`
  - 当前只冻结：
    - 净换手率定义
    - 作为候选输入可供后续验证
  - 不冻结：
    - 全市场推广
    - 完整 Level-2 数据工程

## 状态判定（v1）

- `valid`
  - `trade_id / signal_date / factor_name / dynamic_eval_family` 完整
  - 且三类核心输入至少一类可解析
- `partial`
  - 基础字段完整，但动态评估参数不足
- `invalid`
  - 核心输入缺失或无法判断有效性
- `unknown`
  - 字段无法解析

## 历史边界

- v1 只冻结最小映射，不证明最优 Kalman 参数与最优因子更新频率。
- v1 不直接进入：
  - 主线默认因子评估器
  - 默认组合风险控制器
  - 实时交易脚本
