# A5 target_weight 升级判断重开准备页

更新时间：2026-07-16

## 用途

- 把 `actual_generation后` 升级判断从“唯一附加条件已补到可判断层”继续推进到“可直接重开判断”。
- 这页不宣布：
  - `output_passed`
  - `正式优化器 ready`
  - `covariance_model_id ready`
- 这页只回答：
  - 为什么现在值得重开判断
  - 重开时唯一该裁的焦点是什么
  - 哪些内容仍然禁止误写

## 当前结论

- 当前主负责人已完成：
  - `A5_degraded_risk_handling_主负责人书面验收页__20260716.md`
- 当前正式推进结果是：
  - `唯一附加条件已补到可判断层`
- 且当前又新增：
  - `A5_covariance_model_id_最小集成验证执行页__20260717.md`
  - 已正式证明 `ready_judgement_conditional__downstream_still_locked`
    可被下游一致消费
- 因此当前最顺下一手不再是：
  - 继续补边界说明
  - 继续做同层书面验收
- 而是：
  - 重开 `target_weight actual_generation后` 升级判断

## 一、为什么现在值得重开

- 因为当前已经同时具备：
  - `actual generation execution` 的 success / failure hard 证据
  - `conditional` 的唯一附加条件冻结页
  - 边界验证清单
  - 主负责人书面验收页
- 这意味着当前已经不再缺：
  - 条件命名
  - 条件具体化
  - 条件书面验收

## 二、重开时唯一该裁的焦点

- 当前重开判断时唯一该裁的焦点是：
  - 在 `degraded_risk_handling` 与 `covariance_model_id` 仍未闭合的边界下，
  - `target_weight` 是否已足以从“附加条件已补到可判断层”继续推进到下一档正式升级判断结论

## 三、当前不要再讨论什么

- 当前不要再回到：
  - 是否足以重开升格裁决
- 当前不要再回到：
  - 唯一附加条件叫什么
- 当前不要展开：
  - 回测
  - 信号组合
  - 下游字段升格

## 四、当前禁止误写

- 禁止写成：
  - `output_passed`
  - `正式优化器 ready`
  - `covariance_model_id ready`
- 禁止把：
  - `可判断层`
  - 写成：
    - `已通过升级判断`

## 五、一句话口径

- 当前 `target_weight actual_generation后` 的最稳正式写法是：
  - `唯一附加条件已补到可判断层`
  - `下一手已切到升级判断重开准备`
  - 且当前已继续前推到：
    - `verified_with_degraded_risk` 后续升级判断包准备
