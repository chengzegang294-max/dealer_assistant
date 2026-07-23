# A5 portfolio_tracking_error 最小通过条件页

更新时间：2026-07-16

## 用途

- 把 `portfolio_tracking_error` 从“输出闭合判断层”继续推进到“最小通过条件已明确到可判断层”。
- 这页不是在宣布通过。
- 这页只负责：
  - 明确最小输入条件
  - 明确最小输出条件
  - 明确依赖关系
  - 明确禁止性表述

## 当前结论

- `portfolio_tracking_error` 当前不能写成：
  - `output_passed`
  - `ready`
- `portfolio_tracking_error` 当前可以写成：
  - `pass_conditions_frozen__not_output_passed`
- 原因：
  - 通过条件已冻结
  - 且单点升级判断已正式吸收
  - 但仍未进入正式风险输出通过

## 一、最小输入条件

- 条件 1：
  - 必须显式声明：
    - `benchmark_mode`
    - 或 `nonbenchmark_mode`
- 条件 2：
  - 必须存在可命名的风险口径来源：
    - `formalized_risk_model`
    - 或 `degraded_risk_handling`
- 条件 3：
  - 必须存在：
    - `target_weight`
    - 当前持仓或基准持仓参照
- 条件 4：
  - 若使用 `covariance_model_id`
    - 当前只能写成：
      - `under_judgement`
      - 或 `implementation_prep_candidate`
    - 不允许写成：
      - `risk_model_ready`

## 二、最小输出条件

- 条件 1：
  - 输出必须能显式标记：
    - `portfolio_tracking_error`
- 条件 2：
  - 输出必须带：
    - 使用的风险口径
    - 是否为降级模式
- 条件 3：
  - 若当前风险口径仅是降级模式
    - 必须显式带：
      - `degrade_flags`
- 条件 4：
  - 若无法计算
    - 必须显式带：
      - `abort_reason`

## 三、当前依赖关系

- `portfolio_tracking_error` 不能跳过：
  - `target_weight`
  - `benchmark` 风险口径
  - `covariance_model_id` 的更明确状态
- 因此当前这页只够支撑：
  - `通过条件已能命名`
- 还不够支撑：
  - `正式风险输出已通过`

## 四、当前证据状态

- 已补 1：
  - `benchmark` 风险输出的最小正式口径
- 已补 2：
  - `covariance_model_id` 的最小输入层
- 已补 3：
  - 在降级风险口径下的可审计样例
- 当前下一手：
  - 起 `portfolio_tracking_error` 单点升级判断

## 五、禁止误写

- 禁止写成：
  - `portfolio_tracking_error 已可正式消费`
  - `portfolio_tracking_error 已有正式 benchmark 风险输出`
  - `covariance_model_id 已 ready`
- 禁止把：
  - `pass_conditions_drafted`
  写成：
  - `output_passed`

## 六、主负责人裁决

- 当前这一步的定位是：
  - 为后续风险输出升格准备正式判断入口
- 当前不做：
  - 通过裁决
  - runtime 实现
- 当前正确口径应写成：
  - `pass_conditions_frozen__not_output_passed`
- 当前已不再缺：
  - 同层口径页
  - 同层样例页
- 当前开始缺的是：
  - frozen 状态如何解锁下游判断而不制造 ready 幻觉

## 七、一句话口径

- 当前 `portfolio_tracking_error` 已到：
  - `通过条件已冻结层`
- 但仍未到：
  - `正式输出通过`

## 回链

- `A5_portfolio_tracking_error_输出闭合判断页__20260716.md`
- `A5_target_weight_通过后仍需证据清单页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
