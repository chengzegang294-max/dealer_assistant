# A5 Cursor 主导 FV gate 下一阶段规划讨论包

更新时间：2026-07-19

## 用途

- 把 `Cursor` 提升为当前阶段的统筹负责人，请它对 `FV gate` 的下一阶段给出正式规划。
- 这页不是执行页。
- 这页不让 `Cursor` 直接改代码或跑命令。
- 这页只要求 `Cursor` 做：
  - 阶段判断
  - 方向规划
  - 分工安排
  - 停点定义

## 一、为什么现在进入下一步

- 当前已完成：
  - `FV gate v0` 最小回测入口
  - 首轮成绩单
  - A/B 对照
  - 第三轮 strict filter 失败验证
  - 第三轮 risk-lite 改善
  - 第四轮 `rank-decay + risk-lite` 当前最佳结果
  - `current_best` 独立冻结
  - `tuning_frozen__no_further_scalar_or_rankdecay_microtune`
- 这说明当前阶段已经不是：
  - “继续在同一窗口里拧参数”
- 当前阶段已经变成：
  - “下一阶段应该如何开”

## 二、当前已冻结事实

- 当前 `current_best` 为：
  - `signal_hypothesis_id = trend_pullback_confirmation_v1`
  - `filter_layer_id = none`
  - `weight_logic_id = filtered_alpha_rank_to_target_weight_rank_decay_v2`
  - `final_size_scalar = 0.5`
- 当前成绩单为：
  - `net total_return = -0.00947495`
  - `holdout net total_return = -0.00291711`
  - `net active_total_return = -0.12843922`
  - `net max_drawdown = -0.01794461`
- 当前标签只能写成：
  - `improved_but_still_negative`
- 当前禁止误写：
  - `financial-valid`
  - `output_passed`

## 三、现在请 Cursor 占领导位做什么

- `Cursor` 当前要领导的不是：
  - 再试一轮 `scalar`
  - 再拧一轮 `rank-decay`
  - 直接改代码
- `Cursor` 当前要领导的是：
  - 判断下一阶段应该开哪种“新证据类型”
  - 判断是否要换“新样本边界”
  - 判断 Trae 的执行顺序
  - 判断什么情况下该停、什么情况下该继续

## 四、必须让 Cursor 回答的四个问题

1. 当前是否已经应该从 `FV gate v0 tuning_frozen` 切到下一阶段？
2. 下一阶段最应该开的是什么：
   - 新样本边界
   - 新证据类型
   - 新评价维度
   - 还是先停在当前基线
3. 若继续，Trae 的第一执行手是什么？
4. 若不继续，当前应如何正式写停点与等待条件？

## 五、给 Cursor 的边界

- 允许 `Cursor` 讨论：
  - 阶段切换
  - 规划排序
  - 分工设计
  - 停点与继续条件
- 不允许 `Cursor` 讨论：
  - 把当前结果误写成 `financial-valid`
  - 回到同一窗口内继续微调 `scalar` / `rank-decay`
  - 直接接管 `02_runtime/**`
  - 直接执行命令

## 六、希望 Cursor 给出的输出格式

1. 你如何理解当前已经完成到哪
2. 你如何理解为什么当前不能再继续 current_best 微调
3. 你建议的下一阶段名是什么
4. 你建议先做哪一手
5. 你建议 Trae 执行什么，禁止 Trae 执行什么
6. 你建议当前停点怎么写

## 七、主负责人预期

- 若 `Cursor` 判断：
  - 现在该进入下一阶段
- 那它要明确：
  - 阶段名
  - 唯一下一手
  - Trae 执行清单
  - 停点
- 若 `Cursor` 判断：
  - 还不该进入下一阶段
- 那它要明确：
  - 为什么
  - 应停在什么状态
  - 等什么新输入或新证据

## 八、一句话口径

- 这轮不是让 `Cursor` 评论回测成绩好不好，而是让它正式接管“下一阶段规划权”。

## 回链

- `A5_financial_validity_gate最小入口与通过标准页__20260719.md`
- `A5_FV_gate_v0_当前最佳最小口径冻结页__20260719.md`
- `A5_FV_gate_v0_current_best后续推进主负责人裁决页__20260719.md`
- `A5_Cursor_Trae_FV_gate协同分区与交接页__20260718.md`
