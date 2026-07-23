# A5 alpha_score 正式代理合同页

更新时间：2026-07-16

## 用途

- 把 `alpha_score` 从“模糊 proxy 描述”推进到“正式代理合同”层。
- 这页不是 alpha 模型实现页。
- 这页也不是在宣布唯一稳定主源已闭合。
- 这页只负责：
  - 冻结当前允许的代理口径
  - 写清允许输入、允许表述与禁止误写
  - 为后续 `covariance_model_id` 讨论提供稳定上游

## 当前结论

- `alpha_score` 当前正式状态应写成：
  - `contract_frozen_proxy`
- 不能写成：
  - `formal_primary_source_closed`
- 当前允许的最小正式口径是：
  - `alpha_model_or_factor_rank_proxy`
- 当前不允许的写法是：
  - 把任何单一排序值或单一因子直接写成：
    - `已闭合正式 alpha 主源`

## 一、当前字段定义冻结

- 字段名：
  - `alpha_score`
- 所属层：
  - `portfolio_policy_inputs`
- 字段角色：
  - `单标的预期超额收益代理输入`
- 当前类型：
  - `float`
- 必填性：
  - `yes`
- 当前合同定位：
  - `proxy`

## 二、当前允许的代理来源

- 允许来源族：
  - `alpha_model_output_proxy`
  - `factor_rank_proxy`
  - `multi_factor_rank_proxy`
- 当前统一写法：
  - `alpha_model_or_factor_rank_proxy`

### 解释

- 这意味着当前只允许把 `alpha_score` 写成：
  - 来自既有 alpha 评分合同
  - 或来自因子排序后的标准化代理值
- 不意味着：
  - 我们已经选定唯一 alpha 模型
  - 我们已经完成历史验证
  - 我们已经完成优化器消费闭合

## 三、最小输入要求

- 至少需要满足以下任一类：
  - 已有 alpha 评分结果
  - 已有可复核的因子排序结果
- 若使用排序代理：
  - 必须写清：
    - 排序依据
    - 标准化方式
    - 时间点
    - 是否存在缺失补位

## 四、最小验收要求

- 验收 1：
  - `alpha_score` 必须是数值型输入
- 验收 2：
  - `alpha_score` 必须能回链到：
    - `alpha_model_output_proxy`
    - 或 `factor_rank_proxy`
- 验收 3：
  - 必须显式带上来源说明
- 验收 4：
  - 若来源只是代理排序，不得写成：
    - `正式 alpha 主源已闭合`
- 验收 5：
  - 若 `alpha_score` 缺失：
    - 必须触发 `abort_if_missing`

## 五、允许写法

- 允许写成：
  - `alpha_score 当前按正式代理合同接入`
  - `alpha_score 当前来源为 alpha_model_or_factor_rank_proxy`
  - `alpha_score 可作为实现前讨论的上游代理输入`

## 六、禁止误写

- 禁止写成：
  - `alpha_score 已有唯一稳定主源`
  - `alpha_score 已完成正式 alpha 模型闭合`
  - `alpha_score 已完成历史验证`
  - `alpha_score 已可直接代表最终可执行预期收益`
- 禁止把：
  - 排序值
  - 代理值
  写成：
  - `已验证的正式 alpha 预测值`

## 七、降级与中止口径

- 若 `alpha_score` 缺失：
  - `ABORT`
- 若 `alpha_score` 只有代理来源但来源说明不完整：
  - `mark_degraded`
  - 并禁止进入下游强表述
- 若 `alpha_score` 的代理口径漂移：
  - 当前动作：
    - 停在合同层
    - 重新冻结代理合同

## 八、与下游的关系

- 当前这页解决的是：
  - `G5` 的第一手阻塞
- 当前这页还没有解决：
  - `covariance_model_id`
  - `target_weight`
  - `portfolio_tracking_error`
- 但它已经能把后续问题从：
  - `alpha_score 到底是什么`
  推进到：
  - `有了正式代理合同后，covariance 是否值得进入实现前口径`

## 九、主负责人裁决

- 当前正式裁决：
  - `alpha_score` 不再只写成松散 proxy 描述
  - 而是升级为：
    - `contract_frozen_proxy`
- 这样做的目的不是提前开实现。
- 这样做的目的只是：
  - 给 `G5` 提供稳定第一步
  - 避免后续继续围绕 alpha 输入定义空转

## 十、一句话口径

- 当前 `alpha_score` 的正确写法是：
  - `formal_proxy_contract_frozen__not_primary_source_closed`

## 回链

- `A_REQ_003_字段映射表__20260715.tsv`
- `A5_字段真实来源状态表__20260715.tsv`
- `A5_统一对象接口草案__20260715.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
- `A5_G5G6_多家AI回收记录与主负责人裁决__20260716.md`
