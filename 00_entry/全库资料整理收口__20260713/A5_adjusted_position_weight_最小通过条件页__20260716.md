# A5 adjusted_position_weight 最小通过条件页

更新时间：2026-07-16

## 用途

- 把 `adjusted_position_weight` 从“输出闭合判断层”继续推进到“最小通过条件可判断层”。
- 这页不是在宣布最终融合输出已经通过。
- 这页只负责：
  - 明确最小输入条件
  - 明确最小输出条件
  - 明确依赖链
  - 明确禁止性表述

## 当前结论

- `adjusted_position_weight` 当前不能写成：
  - `output_passed`
  - `ready`
- `adjusted_position_weight` 当前可以写成：
  - `pass_conditions_frozen__not_output_passed`
- 原因：
  - 通过条件已冻结
  - 但上游 `target_weight` 仍未正式 passed
  - 最终融合仍未进入正式输出通过

## 一、最小输入条件

- 条件 1：
  - 必须存在：
    - `target_weight`
    - `final_size_scalar`
- 条件 2：
  - `target_weight` 当前至少应满足：
    - `pass_conditions_frozen__not_output_passed`
  - 不允许回退到未命名上游输出
- 条件 3：
  - `final_size_scalar` 必须仍满足核心断言：
    - `min(kelly_size_scalar, vt_size_scalar, pq_position_max_size, 1.0)`
- 条件 4：
  - 若任一上游走降级模式
    - 必须显式带：
      - `degrade_flags`

## 二、最小输出条件

- 条件 1：
  - 输出必须能显式标记：
    - `adjusted_position_weight`
- 条件 2：
  - 输出必须能回溯到：
    - `target_weight * final_size_scalar`
- 条件 3：
  - 若最终结果来自降级链
    - 必须显式带：
      - `degrade_flags`
- 条件 4：
  - 若不可生成
    - 必须显式带：
      - `abort_reason`

## 三、当前依赖关系

- `adjusted_position_weight` 不能跳过：
  - `target_weight`
  - `final_size_scalar`
  - 上游降级边界
- 因此当前这页只够支撑：
  - `通过条件已能命名`
- 还不够支撑：
  - `最终融合输出已通过`

## 四、当前证据状态

- 已补 1：
  - `final_size_scalar` 在降级模式下的可审计样例
- 已补 2：
  - 最终融合输出的失败样例与 `abort_reason` 触发样例
- 当前仍缺：
  - `target_weight` 的正式通过证据
- 当前下一手：
  - 切回 `covariance_model_id` 的总瓶颈判断准备

## 五、禁止误写

- 禁止写成：
  - `adjusted_position_weight 已可正式运行`
  - `组合层最终权重已通过`
  - `target_weight 已随之通过`
  - `final_size_scalar 已完成运行闭合`
- 禁止把：
  - `pass_conditions_drafted`
  写成：
  - `output_passed`

## 六、主负责人裁决

- 当前这一步的定位是：
  - 为最终融合输出升格准备最小通过条件骨架
- 当前不做：
  - 通过裁决
  - runtime 实现
- 当前正确口径应写成：
  - `pass_conditions_frozen__not_output_passed`
- 当前已不再缺：
  - 同层样例页
  - 单点升级判断回包
- 当前开始缺的是：
  - frozen 状态如何在不制造 ready 幻觉的前提下解锁总瓶颈判断

## 七、一句话口径

- 当前 `adjusted_position_weight` 已到：
  - `通过条件已冻结层`
- 但仍未到：
  - `正式最终输出通过`

## 回链

- `A5_adjusted_position_weight_输出闭合判断页__20260716.md`
- `A5_target_weight_通过后仍需证据清单页__20260716.md`
- `A5_portfolio_tracking_error_最小通过条件页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
