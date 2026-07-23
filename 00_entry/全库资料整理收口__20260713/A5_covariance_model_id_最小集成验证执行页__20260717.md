# A5 covariance_model_id 最小集成验证执行页

更新时间：2026-07-17

## 用途

- 在 `ready_judgement_conditional__downstream_still_locked` 后，
  把“下游消费边界一致性校验”的实际执行结果正式收口到一页。
- 这页记录的是：
  - `target_weight / portfolio_tracking_error / adjusted_position_weight`
    对当前 `covariance_model_id` 状态的消费边界是否一致
  - 当前是否仍需保留 `downstream_still_locked`
  - 执行后为什么仍不能写成 `risk_model_ready`
- 这页不负责：
  - 宣称 `risk_model_ready`
  - 宣称三段输出已自动解锁
  - 代替后续各输出段自己的 `output_passed` 判断

## 当前结论

- 当前最小集成验证已完成：
  - `passed`
- 当前验证通过的含义不是：
  - `risk_model_ready`
  - `three_outputs_unlocked`
- 当前验证通过的含义是：
  - 下游三段对 `covariance_model_id` 的消费边界没有出现相互冲突
  - `ready_judgement_conditional__downstream_still_locked`
    这一层级已能被下游页一致消费
- 当前正式状态保持：
  - `ready_judgement_conditional__downstream_still_locked`

## 一、本轮验证对象

- 上游正式页：
  - `A5_covariance_model_id_实现前口径判断页__20260716.md`
  - `A5_covariance_model_id_ready判断_多家AI回收记录与主负责人裁决__20260716.md`
- 下游消费页：
  - `A5_target_weight_输出闭合判断页__20260716.md`
  - `A5_portfolio_tracking_error_covariance最小输入层页__20260716.md`
  - `A5_portfolio_tracking_error_输出闭合判断页__20260716.md`
  - `A5_adjusted_position_weight_输出闭合判断页__20260716.md`
- 总表页：
  - `A5_实现阻塞项拆解表__20260716.tsv`
  - `A5_G5主链闭合状态页__20260716.md`
  - `A5_G5_输出闭合判断页__20260716.md`

## 二、检查点 1：target_weight 消费边界

- 当前核对结果：
  - `target_weight` 仍只要求
    `covariance_model_id >= ready_judgement_conditional__downstream_still_locked`
  - 但没有把它写成：
    - `risk_model_ready`
    - `target_weight 已可稳定输出`
- 当前说明：
  - `target_weight` 消费的是“上游风险输入已推进到可判断层”
  - 不是“风险模型已正式 ready”
- 当前判断：
  - `pass`

## 三、检查点 2：portfolio_tracking_error 消费边界

- 当前核对结果 1：
  - `portfolio_tracking_error covariance_model_id 最小输入层页`
    已允许消费：
    - `candidate_model_family_frozen__not_ready`
    - `unique_model_frozen__not_ready`
    - `ready_judgement_conditional__downstream_still_locked`
- 当前核对结果 2：
  - `portfolio_tracking_error 输出闭合判断页`
    仍显式写明：
    - 上游虽更高一档，但仍保留 `downstream_still_locked`
    - 当前不能写成正式风险输出已闭合
- 当前说明：
  - `portfolio_tracking_error` 已能吸收当前更高一档上游状态
  - 但没有借此越界到 `output_passed`
- 当前判断：
  - `pass`

## 四、检查点 3：adjusted_position_weight 间接依赖边界

- 当前核对结果：
  - `adjusted_position_weight` 仍只经由 `target_weight`
    间接受上游风险模型影响
  - 当前页没有把 `covariance_model_id` 直接拔高成
    最终融合输出的独立解锁条件
- 当前说明：
  - 第三段仍被正确限制在：
    - `target_weight 未正式 output_closed`
    - `final_size_scalar` 边界未最终放开
- 当前判断：
  - `pass`

## 五、本轮执行结果

- 当前最小集成验证结果为：
  - `integration_validation_passed = true`
- 当前未发现：
  - 下游三段对 `covariance_model_id` 状态名的冲突引用
  - 把 `conditional` 误写成 `risk_model_ready`
  - 把 `downstream_still_locked` 偷换成自动解锁
- 当前仍保留：
  - 下游三段各自的 `not_output_passed`
  - 各段单独判断、单独升格的顺序

## 六、为什么通过后仍不升级状态名

- 原因 1：
  - 本轮验证的是“合同是否一致”
  - 不是“风险模型是否已完全 ready”
- 原因 2：
  - 本轮没有新增：
    - 优化器正式输出
    - tracking error 正式数值输出
    - 最终权重正式运行结果
- 原因 3：
  - 即便边界一致，也只说明：
    - `covariance_model_id` 的 conditional 状态已被下游正确理解
  - 不说明：
    - 下游任一段已可自动升格
- 所以当前仍保持：
  - `ready_judgement_conditional__downstream_still_locked`

## 七、主负责人裁决

- 当前先做什么：
  - 正式承认最小集成验证已执行且通过
  - 把 `covariance_model_id` 的主线剩余缺口，
    从“下游页口径可能漂移”收缩为“继续等待各输出段自身证据”
  - 回填主链状态页、阻塞表与 README
- 当前不做什么：
  - 发明新的 ready 状态名
  - 把 `conditional` 直接升成 `yes`
  - 把三段输出写成已自动解锁
- 当前下一手切到：
  - 回到 `G5` 第一输出段
    `target_weight` 的 `not_output_passed` 剩余缺口收缩

## 七点五、2026-07-18 执行验证复跑

- 本轮已再次执行：
  - `covariance_bodyrun_fresh`
  - `covariance minimum stability check`
- 本轮 fresh 复跑确认：
  - `fresh_run_passed = true`
  - `candidate_family = benchmark_relative_sample_covariance`
  - `matrix_shape = [20, 20]`
- 本轮 stability 复跑确认：
  - `stability_check_passed = true`
  - `structural_pass = true`
  - `scale_gap_within_guardrail = true`
- 这次复跑新增证明的是：
  - 当前 `covariance_model_id` 的最小集成验证依赖不是历史孤证
  - `fresh -> stability -> downstream consumption` 这条最短可运行链当前仍可直接复现
- 这次复跑不新增宣称：
  - `risk_model_ready`
  - `three_outputs_unlocked`
  - 任何高于 `ready_judgement_conditional__downstream_still_locked` 的状态名

## 七点六、2026-07-18 同轮串联批次执行

- 本轮已新增一份同轮 hard 汇总产物：
  - `02_runtime/a5_g5_target_weight_validation/artifacts/target_weight_validation/covariance_target_weight_same_batch_latest.json`
- 这份批次汇总当前确认：
  - `covariance_chain_passed = true`
  - `target_weight_chain_passed = true`
- 这意味着本轮已经不是“仅 covariance 单段 fresh/stability 仍可跑”，而是：
  - `current fresh -> adjacent fresh -> stability -> target_weight validation -> real_input -> actual generation`
    已在同一批次内顺序复现
- 这次批次执行新增证明的是：
  - 当前 `covariance_model_id` 对 `target_weight` 的最小下游消费，已经具备同轮串联证据
  - 上游不是孤立单段 hard 产物，而是可在本轮直接接到 `target_weight`
- 这次批次执行仍不新增宣称：
  - `risk_model_ready`
  - `downstream_fully_unlocked`
  - 任何高于 `ready_judgement_conditional__downstream_still_locked` 的状态名

## 七点七、2026-07-18 同轮串联继续下探到 portfolio_tracking_error

- 本轮又新增一份更下游的同轮 hard 汇总产物：
  - `02_runtime/a5_g5_portfolio_tracking_error_validation/artifacts/portfolio_tracking_error_validation/covariance_target_weight_pte_same_batch_latest.json`
- 这份批次汇总当前确认：
  - `covariance_target_weight_chain_passed = true`
  - `pte_chain_passed = true`
- 这意味着当前已经不是只到：
  - `covariance -> target_weight`
- 而是已经继续推进到：
  - `covariance -> target_weight -> portfolio_tracking_error`
    在同一批次内顺序复现
- 这次继续下探新增证明的是：
  - 当前 `covariance_model_id` 的最小下游消费已不只停在第一输出段
  - 第二输出段 `portfolio_tracking_error` 当前也能消费这轮 fresh 上游链
- 这次继续下探仍不新增宣称：
  - `risk_model_ready`
  - `all_downstream_ready`
  - 任何高于 `ready_judgement_conditional__downstream_still_locked` 的状态名

## 七点八、2026-07-18 下游单段边界 same-batch audit

- 本轮又新增一份链级 boundary audit 产物：
  - `02_runtime/a5_g5_min_chain_validation/artifacts/a5_g5_same_batch_boundary_audit_latest.json`
- 当前 audit 已确认：
  - `target_weight` frozen 边界 `runtime_backed = true`
  - `portfolio_tracking_error` frozen 边界 `runtime_backed = true`
  - `adjusted_position_weight` frozen 边界 `runtime_backed = true`
  - `all_segment_boundaries_runtime_backed = true`
- 这次 audit 新增证明的是：
  - 当前 `covariance_model_id downstream_still_locked`
    所指向的“下游单段正式边界”已经不再只是页面冻结
  - 而是已具备 same-batch hard 证据支撑
- 这次 audit 仍不新增宣称：
  - `covariance_model_id ready`
  - `risk_model_ready`
  - `downstream 已正式释放`

## 八、一句话口径

- 当前 `covariance_model_id` 已完成：
  - `最小集成验证执行`
- 但当前最稳正式写法仍是：
  - `ready_judgement_conditional__downstream_still_locked`

## 回链

- `A5_covariance_model_id_最小集成验证准备页__20260716.md`
- `A5_covariance_model_id_ready判断_多家AI回收记录与主负责人裁决__20260716.md`
- `A5_covariance_model_id_实现前口径判断页__20260716.md`
- `A5_target_weight_输出闭合判断页__20260716.md`
- `A5_portfolio_tracking_error_covariance最小输入层页__20260716.md`
- `A5_portfolio_tracking_error_输出闭合判断页__20260716.md`
- `A5_adjusted_position_weight_输出闭合判断页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
