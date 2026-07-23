# A5 target_weight 最小缺口补齐页

更新时间：2026-07-16

## 用途

- 把 `target_weight` 在第二轮窄裁决后的最小剩余缺口正式写死。
- 这页不宣布：
  - `output_passed`
- 这页只负责：
  - 把下一手执行物从“继续追问”切到“补最小证据”
  - 固定 `explicit validation run` 的最小交付口径
  - 给主负责人留下可回填的四问书面答案

## 当前结论

- 当前 `target_weight` 仍只能写成：
  - `pass_conditions_frozen__not_output_passed`
- 当前已经不是：
  - 第一手证据完全没补
  - 第二轮票面仍然不清
- 当前已经推进到：
  - `第一手升格证据已补齐`
  - `第二轮更窄裁决已正式给出 no`
  - runtime 模板与最小 runner 已落
  - success/failure 两份 template-level smoke-run 已完成
  - 上游真实输入模板与 smoke-run 输入卡已冻结
  - real-input success/failure 结果模板已冻结
  - real-input case validation smoke-run 已完成
- 当前进一步推进到：
  - `actual generation execution 已完成`
- 当前又继续推进到：
  - `重开升格裁决已获批准`
  - `actual_generation后 升级判断已裁成 conditional`
- 因此当前最顺下一手是：
  - 补唯一附加条件：
    - `degraded_risk_handling` 充分性与稳健边界验证

## 一、最小缺口正式定义

- 当前正式冻结的唯一最小缺口是：
  - `explicit validation run`
- 这不是泛化要求：
  - 再补一批新样例
  - 再开第三轮多AI
  - 再抽象讨论优化器概念
- 这一步只要求证明：
  - 已冻结的 `constraint_set` 不是纸面结构
  - 已给出的可审计权重样例可对应到一次显式验证记录
  - 失败样例的 `abort_reason` 能对应到显式失败记录

## 二、最小成功验证记录

- 最小成功验证记录至少要包含：
  - `run_id`
  - `input_assumption`
  - `constraint_set_id`
  - `risk_handling_mode`
  - `result_summary`
  - `checks`
- 最小成功记录建议结构：

```json
{
  "run_id": "TW_VALIDATION_RUN_OK_V1",
  "input_assumption": {
    "alpha_input_mode": "ranked_scores",
    "constraint_set_id": "TW_MIN_CONSTRAINT_SET_V1"
  },
  "risk_handling_mode": "degraded_risk_handling",
  "result_summary": {
    "weight_count": 3,
    "weight_sum_traceable": true,
    "non_empty": true,
    "within_bounds": true
  },
  "checks": [
    "single_name_cap_applied",
    "long_only_enforced",
    "turnover_control_checked"
  ],
  "abort_reason": ""
}
```

## 三、最小失败验证记录

- 最小失败验证记录至少要包含：
  - `run_id`
  - `failure_trigger`
  - `observed_abort_reason`
  - `path_consistency_note`
- 最小失败记录建议结构：

```json
{
  "run_id": "TW_VALIDATION_RUN_FAIL_V1",
  "failure_trigger": "missing_constraint_set_or_untraceable_alpha_input",
  "observed_abort_reason": "missing_constraint_set_or_untraceable_alpha_input",
  "path_consistency_note": "failure_sample_and_abort_reason_are_consistent",
  "weights": []
}
```

## 四、主负责人四问书面答案

- 问 1：
  - 当前票面是否已足以支持新的升格裁决
- 答：
  - `no`
- 问 2：
  - 当前已拥有的最强证据是什么
- 答：
  - `constraint_set` 最小正式形式
  - 可审计权重样例
  - 失败样例与 `abort_reason`
  - 第二轮窄裁决的有效 `no` 票面
- 问 3：
  - 当前唯一最小新增缺口是什么
- 答：
  - `explicit validation run`
- 问 4：
  - 当前绝不能误写成什么
- 答：
  - `target_weight 已可发起新升格裁决`
  - `target_weight = output_passed`
  - `风险模型已 ready`

## 五、当前先做什么

- 当前先做：
  - 保留当前 success/failure smoke-run 结果
  - 保留当前 real-input case validation 结果
  - 保留当前 actual generation success/failure 结果
  - 以 `A5_degraded_risk_handling_边界验证清单页__20260716.md` 作为下一手书面验收清单
- 当前不先做：
  - 下游两段输出升格

## 五点五、2026-07-18 执行验证复跑

- 本轮已再次执行：
  - `target_weight validation` success
  - `target_weight validation` failure
  - `target_weight real-input validation` success
  - `target_weight real-input validation` failure
  - `target_weight actual generation` success
  - `target_weight actual generation` failure
- 本轮 validation 复跑确认：
  - success 仍为 `validation_passed = true`
  - failure 仍为 `validation_passed = true`
  - 且 `observed_abort_reason = missing_constraint_set_or_untraceable_alpha_input`
- 本轮 real-input validation 复跑确认：
  - success 仍为 `validation_passed = true`
  - failure 仍为 `validation_passed = true`
  - 且 `observed_abort_reason = missing_constraint_set`
  - 且 `path_consistency_note = real_input_failure_path_is_consistent`
- 本轮 actual generation 复跑确认：
  - success 仍为 `generation_executed = true`
  - failure 仍为 `generation_executed = false`
  - 且 `observed_abort_reason = missing_constraint_set`
- 这次复跑新增证明的是：
  - 当前 `explicit validation run` 不是旧产物残留
  - failure 路径已同时具备：
    - 模板层广义失败口径
    - real-input 层默认失败触发器
    - 生成层具体中止原因
  - 且后两层当前已共同收敛到：
    - `missing_constraint_set`
- 这次复跑不新增宣称：
  - `output_passed`
  - `正式优化器已 ready`
  - 任何高于当前正式状态的状态名

## 六、禁止误写

- 禁止把：
  - `有验证记录模板`
  - 写成：
    - `已经完成验证运行`
- 禁止把：
  - `degraded_risk_handling`
  - 写成：
    - `formalized_risk_model 已完成`
- 禁止把：
  - `最小缺口已命名`
  - 写成：
    - `升格条件已全部满足`

## 七、一句话口径

- 当前 `target_weight` 已从“票面不足”推进到“缺口已收窄并命名”。
- 当前下一手正式固定为：
  - `补唯一附加条件的边界验证`

## 回链

- `A5_target_weight_升格裁决_多家AI回收记录与主负责人裁决__20260716.md`
- `A5_target_weight_升格证据补齐页__20260716.md`
- `A5_target_weight_通过后仍需证据清单页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
- `A5_target_weight_validation_run_执行说明页__20260716.md`
