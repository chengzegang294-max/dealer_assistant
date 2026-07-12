# group08_correlation_stock_selection_p0_min_contract_v1

- CONTRACT_ROLE: `CONTRACT_FROZEN / NOT_RUNTIME_DEFAULT`
- 当前只冻结 `GROUP_08` 相关性选股线的最小输入输出，不直接进入主线默认执行。

## 合同目标

- 把以下内容固定成可复核字段：
  - `因子家族 (factor_family)`
  - `筛选窗口 (rolling_window_months)`
  - `有效因子列表 (selected_factors)`
  - `个股综合得分 (stock_score)`
  - `组合分层输出 (portfolio_bucket)`
  - `模型状态 (selection_model_state)`

## 输入字段（proof_input）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 样本内唯一 id |
| rebalance_date | string | yes | 调仓日期 |
| symbol | string | yes | 标的 |
| industry_name | string | no | 行业分类 |
| factor_family | string | yes | `fundamental / valuation / technical / size / mixed / unknown` |
| factor_name | string | yes | 因子名称 |
| factor_value | number | yes | 因子值 |
| factor_significance_level | number | no | 显著性水平 |
| correlation_value | number | no | 历史相关性 |
| rolling_window_months | number | yes | 滚动窗口长度，默认 `24~60` 月 |
| scoring_method | string | no | `correlation_rank / weighted_score / unknown` |
| top_bucket_ratio | number | no | 组合分层比例，如 `0.1 / 0.2` |
| input_note | string | no | 备注 |

## 输出字段（proof_output）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 与输入对齐 |
| selected_factors | string | yes | 当期有效因子列表 |
| stock_score | number | yes | 个股综合得分 |
| stock_rank | number | yes | 排名 |
| portfolio_bucket | string | yes | `top10 / top20 / observe / unknown` |
| expected_bias | string | yes | `long_only_selection / observe / unknown` |
| confidence_note | string | yes | 参数完备度与置信说明 |
| selection_model_state | string | yes | `valid / partial / invalid / unknown` |
| proof_basis | string | yes | 本行依据简述 |

## 计算与冻结口径（v1）

- 当前只冻结：
  - `24` 因子基础库作为默认上游家族
  - `24~60` 月滚动窗口
  - 相关性与显著性联合筛选
  - 因子加总打分
  - `TOP10% / TOP20%` 组合输出
- 当前不冻结：
  - 所有行业的独立参数最优解
  - 每个因子的具体标准化实现
  - 真实交易成本与调仓约束

## 状态判定（v1）

- `valid`
  - `trade_id / rebalance_date / symbol / factor_family / factor_name / factor_value / rolling_window_months` 完整
  - 且可形成有效因子列表和得分输出
- `partial`
  - 基础字段完整，但显著性或排序信息不足
- `invalid`
  - 核心输入缺失或无法形成排序输出
- `unknown`
  - 字段无法解析

## 历史边界

- v1 只冻结最小映射，不证明最优权重与最优行业扩展方案。
- v1 不直接进入：
  - 主线默认多因子选股引擎
  - 默认因子池管理器
  - 实时交易脚本
