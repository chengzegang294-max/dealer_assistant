# A5 covariance_model_id ready 判断多家AI正式发包稿

更新时间：2026-07-16

```text
你现在参与的是一个多AI讨论，不是自由闲聊。

TASK:
讨论当前项目里，`covariance_model_id` 在已完成唯一模型冻结后，是否已足以继续推进到 `risk_model_ready`。

BACKGROUND:
- 当前项目路径：D:\Stock\trading_assistant
- 当前主线：A5 -> G5 -> covariance_model_id
- 当前不是 provider 讨论，不是分钟级，不是新家族选择
- 当前唯一模型已冻结为：
  benchmark_relative_sample_covariance__CSI300__lookback60__a5_top_liquid_20__v1
- 当前已完成：
  1) current 窗口 first fresh-run
  2) adjacent 窗口 second fresh-run
  3) 两窗口最小稳定性检查 passed
  4) 唯一活动实现候选冻结
  5) 唯一模型最小合同冻结
- 当前 fallback 已冻结为：
  - shrinkage / structured covariance = fallback
  - factor-implied covariance = observation

KNOWN_CONSTRAINTS:
- 不允许把 `risk_model_ready` 直接等同于 `三段输出已解锁`
- 不允许把 `unique_model_frozen` 直接等同于 `output_passed`
- 当前只讨论 risk-model 层 ready，不讨论 target_weight / portfolio_tracking_error / adjusted_position_weight 的实现细节

DISCUSSION_SCOPE:
- 允许讨论：
  - 当前唯一模型冻结是否足以支撑 risk-model 级 ready
  - 当前 fallback 合同是否足以支撑 ready 声明
  - 如果还不够，最小剩余缺口是什么
- 不要展开：
  - provider
  - 分钟级 / 高频
  - 重开多家族归属讨论
  - 下游三段的代码实现

FREE_GUESS_RANGE:
- 允许你基于仓内已有 hard evidence 做 ready 级判断
- 若缺证据必须明确写 NEED_EVIDENCE

EXPECTED_OUTPUT:
- 请给出保守 / 平衡 / 激进三种写法
- 并在最后明确推荐一种

OUTPUT CONTRACT:
1. 结论
- 只能在 yes / conditional / no 中三选一
2. 原因
- 用 3-5 条写清为什么
3. 缺口
- 若不是 yes，写最小剩余缺口
4. 禁止项
- 写清当前不能误写成什么
5. 焦点
- 写清下一手最该做什么
```
