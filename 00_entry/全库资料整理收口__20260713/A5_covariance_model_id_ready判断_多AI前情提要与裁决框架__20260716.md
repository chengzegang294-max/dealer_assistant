# A5 covariance_model_id ready 判断多AI前情提要与裁决框架

更新时间：2026-07-16

## TASK

- 讨论当前 `covariance_model_id` 在已完成：
  - 唯一模型冻结
  - 参数边界冻结
  - fallback 最小合同冻结
  后，是否已足以继续推进到：
  - `risk_model_ready`

## BACKGROUND

- 当前主线：
  - `A5 -> G5 -> covariance_model_id`
- 当前不是：
  - provider 讨论
  - 多家族并跑
  - 三段输出直接升格
- 当前已完成：
  - `benchmark_relative_sample_covariance` 的 current / adjacent 两窗口 fresh-run
  - `20 x 20` 协方差矩阵 latest
  - `minimum_stability_checked__not_ready`
  - `sole_implementation_candidate_frozen__not_ready`
  - `unique_model_frozen__not_ready`
- 当前唯一模型：
  - `benchmark_relative_sample_covariance__CSI300__lookback60__a5_top_liquid_20__v1`

## KNOWN_CONSTRAINTS

- 不允许把：
  - `risk_model_ready`
  直接等同于：
  - `三段输出已解锁`
- 不允许把：
  - 唯一模型已冻结
  直接写成：
  - `output_passed`
  - `ready for all downstream`
- 当前 fallback 写法已冻结为：
  - `shrinkage / structured covariance = fallback`
  - `factor-implied covariance = observation`

## DISCUSSION_SCOPE

- 本轮允许讨论：
  - 当前唯一模型冻结是否足以支撑 `risk_model_ready`
  - 当前 fallback 合同是否足以支撑 ready 级声明
  - 若还不够，最小剩余缺口是什么
- 本轮不要展开：
  - 分钟级 / 高频
  - 新 provider
  - 重新讨论候选家族归属
  - 三段输出细节实现

## FREE_GUESS_RANGE

- 允许基于当前仓内证据做 ready 级判断推演
- 若缺证据必须明确写：
  - `NEED_EVIDENCE`

## EXPECTED_OUTPUT

- 请至少给出：
  - 保守写法
  - 平衡写法
  - 激进写法
- 并明确：
  - 当前推荐哪一种
  - 为什么
  - 当前最小下一步是什么

## OUTPUT CONTRACT

1. 结论
- 只能在以下三类中选一类：
  - `yes`
  - `conditional`
  - `no`
2. 原因
- 3-5 条
3. 缺口
- 若不是 `yes`，必须写最小剩余缺口
4. 禁止项
- 写清当前不能误写成什么
5. 焦点
- 写清下一手最该做什么
