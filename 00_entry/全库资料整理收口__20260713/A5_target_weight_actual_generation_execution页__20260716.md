# A5 target_weight actual generation execution 页

更新时间：2026-07-18

## 用途

- 把 `target_weight` 的最小 actual generation execution 正式收口到 repo-global。
- 这页不直接宣布：
  - `output_passed`
- 这页只回答：
  - 生成执行是否真的发生过
  - success/failure 两条路径是否都有 hard 证据
  - 当前下一手应不应该切回升格裁决

## 当前结论

- 当前 `target_weight` 仍只能写成：
  - `pass_conditions_frozen__not_output_passed`
- 但当前已经不是：
  - 只停在模板 smoke-run
  - 只停在 real-input case validation
- 当前已经推进到：
  - `actual generation execution completed`
- 因此当前最顺下一手不再是：
  - 继续补生成执行证据
- 而是：
  - 重开 `target_weight` 升格裁决

## 一、success 生成执行

- 输入：
  - `target_weight_real_input_template_v1.json`
- 产物：
  - `tw_actual_generation_success_latest.json`
- 当前可确认：
  - `generation_executed = true`
  - `weight_count = 3`
  - `within_bounds = true`
  - `gross_weight = 0.293103`
  - `allocation_method = alpha_proportional_with_single_name_cap`

## 二、failure 生成执行

- 输入：
  - `target_weight_real_input_failure_template_v1.json`
- 产物：
  - `tw_actual_generation_failure_latest.json`
- 当前可确认：
  - `generation_executed = false`
  - `observed_abort_reason = missing_constraint_set`

## 三、这轮完成后当前能写到哪

- 允许写成：
  - `actual generation execution 已完成`
  - `生成执行 success/failure 两条路径都有 hard 证据`
  - `target_weight 已具备重开升格裁决的新增票面`
- 仍不能写成：
  - `output_passed`
  - `正式优化器已 ready`
  - `covariance_model_id 已 ready`

## 四、主负责人裁决

- 当前选：
  - 把 `actual generation execution` 视为已完成的最小新增执行证据
- 为什么选这个：
  - 因为 success/failure 两条生成执行路径都已具备 hard 产物
  - 且生成行为不再只是模板校验，而是脚本对真实输入进行了实际处理
- 为什么不直接写成 `output_passed`：
  - 当前仍是最小生成器
  - 风险模型仍处于 `degraded_risk_handling`
  - 还需要对这批新证据做重开升格裁决
- 当前先做什么：
  - 吸收重开升格裁决回包并正式拍板
- 当前暂缓什么：
  - 直接升格
  - 下游两段输出升格

## 五、后续执行回填

- 已完成：
  - `A5_target_weight_重开升格裁决_多家AI回收记录与主负责人裁决__20260716.md`
- 当前正式裁决：
  - `yes，足以重开升格裁决`
- 且已继续完成：
  - `A5_target_weight_升格裁决__actual_generation后_第二轮回收记录与主负责人裁决__20260716.md`
- 当前升级判断结果：
  - `conditional`
- 当前下一手已切到：
  - `A5_degraded_risk_handling_充分性与稳健边界页__20260716.md`
  - `A5_degraded_risk_handling_边界验证清单页__20260716.md`
- 且后续已继续完成：
  - `A5_degraded_risk_handling_主负责人书面验收页__20260716.md`
  - `A5_target_weight_升级判断重开_多家AI回收记录与主负责人裁决__20260716.md`
  - `A5_covariance_model_id_最小集成验证执行页__20260717.md`
- 当前最新下一手已切到：
  - `A5_target_weight_verified_with_degraded_risk后续升级判断准备页__20260717.md`
  - `A5_target_weight_verified_with_degraded_risk后续升级判断_多家AI正式发包稿__20260717.md`
  - `A5_target_weight_verified_with_degraded_risk后续升级判断_多家AI回收记录与主负责人裁决__20260717.md`

## 五点五、2026-07-18 执行验证复跑

- 本轮已再次执行：
  - `generate_target_weight_v1.py` success 输入
  - `generate_target_weight_v1.py` failure 输入
- 本轮 success 复跑确认：
  - `generation_executed = true`
  - `weight_count = 3`
  - `gross_weight = 0.293103`
- 本轮 failure 复跑确认：
  - `generation_executed = false`
  - `observed_abort_reason = missing_constraint_set`
- 这次复跑新增证明的是：
  - 当前生成器在 success / failure 两条路径上都仍可直接运行
  - `actual generation execution` 不是只存在于历史产物里的旧证据
- 这次复跑之后又新增：
  - `actual generation` 已被纳入
    `covariance -> target_weight` 同轮批次汇总
  - 当前批次汇总确认：
    - `covariance_chain_passed = true`
    - `target_weight_chain_passed = true`
    - `real_input_and_generation_aligned = true`
- 这次复跑之后又进一步新增：
  - `actual generation` 已被继续纳入
    `covariance -> target_weight -> portfolio_tracking_error`
    同轮批次汇总
  - 当前已确认：
    - 本轮 `generated_weights` 已被下游
      `portfolio_tracking_error` success / failure 两条路径实际消费
    - 下游 same-batch 汇总中
      `pte_chain_passed = true`
- 这次复跑不新增宣称：
  - `output_passed`
  - `正式优化器已 ready`
  - 任何高于当前既有正式状态的状态名

## 六、一句话口径

- 当前 `target_weight` 已从“actual generation execution 已完成”继续推进到：
  - `verified_with_degraded_risk__not_output_passed`
  - `verified_with_degraded_risk__upstream_min_integration_verified__not_output_passed`
  - 且当前主线已切到 `portfolio_tracking_error` 的上游口径同步

## 回链

- `A5_target_weight_validation_run_执行说明页__20260716.md`
- `A5_target_weight_最小缺口补齐页__20260716.md`
- `A5_target_weight_升格裁决_多家AI回收记录与主负责人裁决__20260716.md`
- `A5_target_weight_verified_with_degraded_risk后续升级判断准备页__20260717.md`
- `A5_target_weight_verified_with_degraded_risk后续升级判断_多家AI回收记录与主负责人裁决__20260717.md`
