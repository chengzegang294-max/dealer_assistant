# A5 degraded_risk_handling 充分性与稳健边界页

更新时间：2026-07-16

## 用途

- 把 `target_weight actual_generation后` 升级判断所缺的唯一附加条件正式冻结下来。
- 这页不宣布：
  - `covariance_model_id ready`
  - `output_passed`
- 这页只回答：
  - 在 `covariance_model_id` 仍未闭合时，
  - 为什么 `degraded_risk_handling` 可能足以支撑当前升级判断，
  - 以及它的稳健边界必须写到哪里。

## 当前结论

- 当前主负责人已裁决：
  - `actual_generation后` 升级判断结果为 `conditional`
- 当前唯一附加条件已冻结为：
  - 正式冻结并验证 `degraded_risk_handling` 的充分性与稳健边界

## 一、当前必须写清的三件事

- 1. 为什么 `covariance_model_id` 未闭合不必然阻断当前升级判断
- 2. `degraded_risk_handling` 在当前阶段到底覆盖到哪
- 3. 哪些情况下一旦越界，就必须停止并不得继续写成可升级

## 二、当前最小充分性口径

- 当前允许的最小充分性口径是：
  - `target_weight` 的当前升级判断只要求：
    - 成功/失败生成执行路径可审计
    - 冻结约束集不越界
    - failure 路径有明确 `abort_reason`
  - 当前不要求：
    - 正式协方差模型已闭合
    - 正式风险模型 ready

## 三、当前最小稳健边界

- 当前必须明确写出：
  - `degraded_risk_handling` 只覆盖当前最小生成器与冻结约束集范围
  - 它不覆盖：
    - 正式风险预算最优性
    - 正式协方差稳定性
    - 更高阶风险暴露闭合
- 一旦需要写到上述任一项：
  - 必须停止当前升级判断
  - 不得继续外推

## 四、当前可验证边界

- 当前最小可验证边界必须至少包含：
  - `success` 路径仍保持：
    - `within_bounds = true`
    - `allocation_method` 与已冻结最小生成器一致
    - 不出现超出 `constraint_set` 的越界生成
  - `failure` 路径仍保持：
    - `observed_abort_reason` 可回链
    - 与既定失败触发器一致
  - `covariance_model_id` 未闭合这一事实被显式保留
    - 而不是被结果文件悄悄抹掉

## 五、通过 / 不通过 / 即停规则

- 允许继续推进到下一轮升级判断的最小条件：
  - `success` 路径不越界
  - `failure` 路径可复现
  - `degraded_risk_handling` 覆盖范围被显式写清
- 当前判为不通过的情况：
  - 成功样例依赖未声明的风险模型假设
  - 失败样例与 `abort_reason` 对不上
  - 输出结果暗含正式协方差已闭合
- 当前必须立即停止并不得外推的情况：
  - 把降级风险处理写成正式风险模型替代
  - 把最小生成器结果写成最优性证明
  - 把当前升级判断写成 `output_passed`

## 六、当前先做什么

- 当前先做：
  - 把这页作为唯一附加条件冻结页
  - 再补一张“边界验证清单页”
  - 再补一张“主负责人书面验收页”
  - 回填到主链状态页、阻塞表与证据总表
- 当前暂缓：
  - 再开第三轮同层多AI
  - 直接改写为 `yes`

## 七、一句话口径

- 当前 `target_weight actual_generation后` 升级判断并未被否决，而是被正式裁成：
  - `conditional`
  - 唯一附加条件是：
    - `degraded_risk_handling` 在 `covariance_model_id` 未闭合时的充分性与稳健边界必须先正式冻结
