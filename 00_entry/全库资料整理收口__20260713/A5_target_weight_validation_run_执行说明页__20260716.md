# A5 target_weight validation run 执行说明页

更新时间：2026-07-16

## 用途

- 把 `explicit validation run` 用通俗口径解释清楚。
- 把“怎么获得成功/失败两类记录”写成可执行说明。
- 这页不宣布：
  - `output_passed`
- 这页只负责：
  - 说明要跑什么
  - 说明为什么跑
  - 说明跑完后什么才算拿到证据

## 当前结论

- `explicit validation run` 通俗地说，不是大回测。
- 它更像一次：
  - 小样本试跑
  - 过闸门检查
  - 让纸面规则真的跑一遍
- 当前要拿到的不是：
  - 收益率曲线
  - 超额收益结论
  - 大规模参数优化
- 当前要拿到的是：
  - 一次成功记录
  - 一次失败记录
  - 并证明失败原因和 `abort_reason` 对得上
- 当前已新增：
  - runtime 模板
  - 最小 runner 草案
  - 两份 template-level smoke-run 结果
  - 上游真实输入模板
  - 真实生成链 smoke-run 输入卡
  - real-input success/failure 结果模板
  - real-input case validation smoke-run 结果
  - actual generation generator
  - actual generation success/failure 执行结果

## 一、通俗解释这东西到底是什么

- 现在我们已经有了：
  - 约束规则
  - 一份能看的权重样例
  - 一份失败样例
- 但这些还停在：
  - 文档层
- `validation run` 的意思就是：
  - 用同样的输入
  - 按同样的规则
  - 真跑一次最小生成过程
  - 看它是不是会产出跟文档一致的结果

- 你可以把它理解成：
  - 不是“上战场”
  - 是“先空枪上膛演练一次”

## 二、为什么现在必须先做这个

- 因为当前卡点已经不是：
  - 多AI怎么判断
- 当前卡点是：
  - 我们写出来的规则到底只是描述
  - 还是已经能被一次最小流程执行出来
- 所以当前最值钱的证据不是更多讨论
- 而是：
  - 成功时能不能真的给出一份合规权重
  - 失败时会不会真的按我们写的原因中止

## 三、怎么获得成功记录

- 成功记录要做的事很简单：
  - 给它一份可追溯的 `alpha_input`
  - 给它一份已经冻结的 `constraint_set`
  - 让流程吐出一份 `target_weight`
- 跑完后至少检查三件事：
  - 权重不是空的
  - 每个权重在上下界内
  - 权重和是可追溯的

- 通俗版输入就是：
  - 几只股票
  - 一组排序分数
  - 一套最小约束

- 通俗版输出就是：
  - “系统确实给出了一份像样的权重表”

## 四、怎么获得失败记录

- 失败记录不是报错就行。
- 失败记录要求：
  - 故意喂一个不合法输入
  - 然后看系统是不是按我们文档里写的原因停下

- 当前最合适的失败触发器就是：
  - `missing_constraint_set_or_untraceable_alpha_input`

- 通俗地说就是：
  - 要么不给约束
  - 要么给一个不可追溯的 `alpha_input`
  - 看流程会不会老老实实拒绝继续往下跑

## 五、拿到证据的最低完成标准

- 只有同时满足下面三条，才算真正拿到 `validation run` 证据：
  - 有一份成功记录
  - 有一份失败记录
  - 失败记录里的 `observed_abort_reason` 和文档里的 `abort_reason` 一致

- 如果只是：
  - 手写一段 JSON
  - 但没有实际跑过
- 那仍然不算。

## 六、当前最顺执行顺序

- 第一步：
  - 固定最小输入样例
- 第二步：
  - 跑成功样例
- 第三步：
  - 跑失败样例
- 第四步：
  - 把成功/失败结果正式落成两份验证记录
- 第五步：
  - 回填 `A5_target_weight_最小缺口补齐页__20260716.md`
- 当前仓内执行落点已固定为：
  - `02_runtime/a5_g5_target_weight_validation/`
- 当前下一手输入入口已固定为：
  - `data/target_weight_real_input_template_v1.json`
  - `target_weight_real_input_smoke_run_card_v1.md`
- 当前已新增的结果入口为：
  - `data/target_weight_real_input_success_case_template_v1.json`
  - `data/target_weight_real_input_failure_case_template_v1.json`

## 七、当前不是什么时候开始回测

- 现在还不是做策略收益回测的时候。
- 因为当前连：
  - `target_weight` 的最小运行证据
  - 都还没拿齐
- 如果现在直接开回测：
  - 会把“生成权重是否可靠”
  - 和“策略收益是否优秀”
  - 混成一团

## 八、一句话口径

- `explicit validation run` 通俗地说，就是：
  - 用最小输入真跑一次成功案例和一次失败案例
  - 证明当前 `target_weight` 不只是纸面定义
- 当前已完成的只是：
  - template-level smoke-run
- 当前已继续推进到：
  - real-input case validation smoke-run
- 当前已继续推进到：
  - actual generation execution
- 当前已在 2026-07-18 继续复跑：
  - validation success / failure
  - real-input validation success / failure
  - actual generation success / failure
- 当前已进一步明确：
  - template-level failure 路径一致性使用
    `missing_constraint_set_or_untraceable_alpha_input`
  - real-input failure 路径一致性使用
    `missing_constraint_set`
  - actual generation 的具体失败中止原因为
    `missing_constraint_set`
  - 它们共同说明：
    - template-level 是广义失败口径
    - real-input 与 actual generation 已在默认失败触发器上收敛到
      `missing_constraint_set`
  - 三者是“模板层广义失败口径”到“真实输入/生成层具体 abort_reason”的分层一致，
    不是相互冲突
- 当前已进一步新增：
  - `covariance -> target_weight` 同轮批次汇总已完成
  - 批次汇总产物为
    `artifacts/target_weight_validation/covariance_target_weight_same_batch_latest.json`
  - 当前批次已确认：
    - `covariance_chain_passed = true`
    - `target_weight_chain_passed = true`
    - `real_input_and_generation_aligned = true`
- 当前又已新增：
  - `a5_g5_same_batch_boundary_audit_latest.json`
    已确认：
    - `target_weight_boundary.runtime_backed = true`
  - 这意味着当前第一段解除 `not_output_passed` 的 frozen 边界，
    已不只是书面冻结，而是已有 same-batch hard 证据支撑
- 当前下一手已切到：
  - `degraded_risk_handling` 唯一附加条件验证
  - `A5_degraded_risk_handling_边界验证清单页__20260716.md`

## 回链

- `A5_target_weight_最小缺口补齐页__20260716.md`
- `A5_target_weight_升格证据补齐页__20260716.md`
- `A5_target_weight_升格裁决_多家AI回收记录与主负责人裁决__20260716.md`
- `02_runtime/a5_g5_target_weight_validation/README.md`
