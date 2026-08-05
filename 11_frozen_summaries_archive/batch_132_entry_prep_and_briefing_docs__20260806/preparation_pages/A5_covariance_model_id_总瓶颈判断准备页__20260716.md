# A5 covariance_model_id 总瓶颈判断准备页

更新时间：2026-07-16

## 用途

- 在三段输出都已前推一档后，
  把 `covariance_model_id` 从“实现前口径判断层”继续推进到“当前总瓶颈判断准备层”。
- 这页不宣布：
  - `covariance_model_id ready`
  - `风险模型已闭合`
- 这页只回答：
  - 为什么现在应把主线切回它
  - 当前唯一该裁的焦点是什么
  - 下一手应该起哪组判断材料

## 当前结论

- 当前 `covariance_model_id` 仍只能写成：
  - `candidate_model_family_frozen__not_ready`
- 但当前已经不是：
  - 只会卡住某一个输出段的局部瓶颈
- 当前已推进到：
  - 三段输出都已分别进入 `verified` 或 `frozen` 的 not_output_passed 状态
  - 且候选模型家族已正式冻结
- 因此当前最顺下一手不再是：
  - 继续做总瓶颈是否值得推进的判断
- 而是：
  - 转入 `本体实跑最小准备`

## 一、为什么现在轮到它

- 原因 1：
  - `target_weight` 已推进到：
    - `verified_with_degraded_risk__not_output_passed`
- 原因 2：
  - `portfolio_tracking_error` 已推进到：
    - `pass_conditions_frozen__not_output_passed`
- 原因 3：
  - `adjusted_position_weight` 已推进到：
    - `pass_conditions_frozen__not_output_passed`
- 原因 4：
  - 三段输出当前都还不能继续外推的共同上游瓶颈，
    已重新收缩到：
    - `covariance_model_id`

## 二、当前唯一该裁的焦点

- 当前总瓶颈判断时唯一该裁的焦点是：
  - 在三段输出都已前推一档后，
    `covariance_model_id` 是否已足以从
    `future_only_but_under_judgement`
    继续推进到更明确的候选模型家族冻结或升级判断写法，
    从而为后续总链继续解锁下一段判断

## 三、当前不要再讨论什么

- 当前不要再回到：
  - `target_weight` 是否还能继续升一档
- 当前不要再回到：
  - `portfolio_tracking_error / adjusted_position_weight` 是否已经 ready
- 当前不要展开：
  - runtime 实现
  - 回测
  - G6 粒度扩展

## 四、当前先做什么

- 当前先做：
  - 已新增并吸收：
    - `A5_covariance_model_id_总瓶颈判断_多AI前情提要与裁决框架__20260716.md`
    - `A5_covariance_model_id_总瓶颈判断_多家AI正式发包稿__20260716.md`
    - `A5_covariance_model_id_总瓶颈判断_多家AI回收记录模板__20260716.md`
    - `A5_covariance_model_id_总瓶颈判断_多家AI回收记录与主负责人裁决__20260716.md`
    - `A5_covariance_model_id_候选模型家族冻结页__20260716.md`
    - `A5_covariance_model_id_本体实跑最小准备页__20260716.md`
- 当前暂缓：
  - 直接改写 `covariance_model_id` 正式状态名
  - 直接发起实现

## 五、一句话口径

- 当前最值钱下一手已从单段输出收口，
  切回到：
  - `covariance_model_id 本体实跑最小准备`

## 回链

- `A5_covariance_model_id_实现前口径判断页__20260716.md`
- `A5_G5_输出升格证据总表__20260716.tsv`
- `A5_G5主链闭合状态页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
