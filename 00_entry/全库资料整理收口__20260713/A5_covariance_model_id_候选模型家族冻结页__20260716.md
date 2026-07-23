# A5 covariance_model_id 候选模型家族冻结页

更新时间：2026-07-16

## 用途

- 把 `covariance_model_id` 从“总瓶颈判断已可裁”正式推进到“候选模型家族已冻结”。
- 这页不是协方差模型实现页。
- 这页也不是在宣布：
  - `covariance_model_id ready`
  - `协方差模型已闭合`
- 这页只负责：
  - 冻结当前允许保留的候选模型家族
  - 写清当前排除项
  - 写清 `NEED_EVIDENCE`
  - 为后续本体实跑最小准备提供统一入口

## 当前结论

- 当前 `covariance_model_id` 当前不能写成：
  - `ready`
  - `closed`
- 当前可以正式写成：
  - `candidate_model_family_frozen__not_ready`
- 当前最稳口径不是：
  - 已确定唯一实现模型
- 当前最稳口径是：
  - 候选模型家族已冻结
  - 但仍待本体实跑与唯一实现模型定稿

## 一、当前冻结的候选模型家族

### 家族 1：benchmark-relative sample covariance

- 当前定位：
  - `主候选`
- 用途：
  - 服务于 `benchmark_id`
  - `tracking_error_limit`
  - `active_risk_aversion`
- 当前保留原因：
  - 与 `portfolio_tracking_error` 的 benchmark 风险输出链最一致

### 家族 2：shrinkage / structured covariance

- 当前定位：
  - `次候选`
- 用途：
  - 作为样本协方差不稳时的结构化替代
- 当前保留原因：
  - 适合后续降低噪声与改善估计稳健性

### 家族 3：factor-implied covariance

- 当前定位：
  - `候选观察位`
- 用途：
  - 若后续确认组合层需更强解释性或压缩维度时再评估
- 当前保留原因：
  - 允许保留讨论位，但不作为本轮最小实跑第一顺位

## 二、当前排除项

- 当前排除：
  - 把纯均值-方差最优化直接写成唯一已定主实现
  - 把高复杂度多因子风险模型直接写成当前第一顺位本体实跑方案
  - 在没有 benchmark / risk budget 对齐前扩大候选面

## 三、当前最小输入要求

- 当前至少要求：
  - `portfolio_date`
  - `benchmark_id` 或明确 `nonbenchmark_mode`
  - `tracking_error_limit`
  - `active_risk_aversion`
  - `candidate_model_family`
- 当前不要求：
  - 协方差矩阵本体已实跑
  - 唯一实现模型已定稿
  - 参数已最终定稿

## 四、NEED_EVIDENCE

- `NEED_EVIDENCE 1`：
  - 协方差矩阵本体实跑
- `NEED_EVIDENCE 2`：
  - 唯一实现模型定稿
- `NEED_EVIDENCE 3`：
  - 家族内参数边界的最小稳定性验证

## 五、当前允许写法

- 允许写成：
  - `covariance_model_id 候选模型家族已冻结`
  - `covariance_model_id 当前属于 candidate_model_family_frozen__not_ready`
- 禁止写成：
  - `covariance_model_id ready`
  - `协方差模型已闭合`
  - `正式风险模型已完成`

## 六、主负责人裁决

- 当前正式裁决是：
  - 允许把 `covariance_model_id` 推进到：
    - `candidate_model_family_frozen__not_ready`
- 当前下一手切到：
  - `A5_covariance_model_id_本体实跑最小准备页__20260716.md`

## 七、一句话口径

- 当前 `covariance_model_id` 已从纯判断层前推到：
  - `候选模型家族冻结层`
- 但当前仍未到：
  - `ready`

## 回链

- `A5_covariance_model_id_实现前口径判断页__20260716.md`
- `A5_covariance_model_id_总瓶颈判断_多家AI回收记录与主负责人裁决__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
