# group08_rotation_style_p0_min_contract_v1

- CONTRACT_ROLE: `CONTRACT_FROZEN / NOT_RUNTIME_DEFAULT`
- 当前只冻结 `GROUP_08` 行业轮动与风格轮动线的最小输入输出，不直接进入主线默认执行。

## 合同目标

- 把以下内容固定成可复核字段：
  - `信号家族 (rotation_signal_family)`
  - `轮动状态 (rotation_signal_state)`
  - `轮动偏向 (rotation_bias)`
  - `组合输出 (portfolio_side / long_short_bucket)`
  - `建议持有期 (hold_horizon_weeks)`
  - `模型状态 (rotation_model_state)`

## 输入字段（proof_input）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 样本内唯一 id |
| signal_date | string | yes | 信号日期 |
| rotation_signal_family | string | yes | `residual_momentum / up_down_ratio / sector_effect_cross_alpha / fund_holding_style_rotation / unknown` |
| market_scope | string | yes | `industry / style / mixed / unknown` |
| ranking_window_weeks | number | no | 观察期，如 `3` 周 |
| holding_horizon_weeks | number | no | 持有期，如 `2` 周 |
| gap_window_weeks | number | no | 间隔期，如 `1` 周 |
| up_down_ratio_value | number | no | 涨跌比指标 |
| upper_threshold | number | no | 上阈值，默认候选 `0.6` |
| lower_threshold | number | no | 下阈值，默认候选 `0.3` |
| residual_momentum_score | number | no | 残差动量排序分数 |
| turnover_delta | number | no | 换手率相对变化 |
| sector_effect_label | string | no | `strong_sector_weak_stock / strong_sector_strong_stock / weak_sector_strong_stock / weak_sector_weak_stock / unknown` |
| fund_holding_relative_exposure | number | no | 相对持仓或其均值 |
| hedge_required | string | no | `yes / no / optional / unknown` |
| input_note | string | no | 备注 |

## 输出字段（proof_output）

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 与输入对齐 |
| rotation_signal_state | string | yes | `long_short_rotation / long_only_rotation / style_switch / observe / unknown` |
| rotation_bias | string | yes | `industry_long_short / industry_follow / style_growth / style_value / observe / unknown` |
| portfolio_side | string | yes | `long_short / long_only / market_neutral / observe / unknown` |
| long_short_bucket | string | yes | 如 `top2_bottom2 / threshold_cross / strong_sector_weak_stock / growth_vs_mainboard / unknown` |
| hold_horizon_weeks | number | yes | 推荐持有期候选，默认 `1~4` 周 |
| confidence_note | string | yes | 参数完备度与置信说明 |
| rotation_model_state | string | yes | `valid / partial / invalid / unknown` |
| proof_basis | string | yes | 本行依据简述 |

## 计算与冻结口径（v1）

- `residual_momentum`
  - 当前只冻结：
    - 观察期 `3` 周
    - 持有期 `2` 周
    - 间隔期 `1` 周
    - 前 `2` 做多、后 `2` 做空
    - 残差动量与换手率相对变化
  - 不冻结：
    - 全量行业池构造细节
    - 完整标准化与回归实现
- `up_down_ratio`
  - 当前只冻结：
    - `T=20` 日涨跌比
    - `0.6 / 0.3` 上下阈值
    - 上穿买入 / 下穿卖出
    - 行业择时与轮动复用口径
  - 不冻结：
    - 全市场多指数扩展参数
- `sector_effect_cross_alpha`
  - 当前只冻结：
    - 行业间动量排序
    - 行业内相对强弱排序
    - `强业弱势股` 作为默认正向筛选标签
    - 对冲后 alpha 作为可选输出说明
  - 不冻结：
    - 具体对冲执行细节
    - 全量股票池筛选步骤
- `fund_holding_style_rotation`
  - 当前只冻结：
    - 公募基金板块持仓测算序列
    - `20` 日平均相对持仓
    - 创业板 vs 主板的风格切换信号
  - 不冻结：
    - 基金净值回推算法细节
    - 更广泛风格对的统一扩展

## 状态判定（v1）

- `valid`
  - `trade_id / signal_date / rotation_signal_family / market_scope` 完整
  - 且对应核心输入至少一类可解析
- `partial`
  - 基础字段完整，但参数或扩展字段不足
- `invalid`
  - 核心输入缺失或信号家族无法确认
- `unknown`
  - 字段无法解析

## 历史边界

- v1 只冻结最小映射，不证明最优持有期、最优行业池和最优对冲方案。
- v1 不直接进入：
  - 主线默认配置引擎
  - 默认仓位控制器
  - 实时交易脚本
