# A5 covariance_model_id 最小集成验证准备页

更新时间：2026-07-16

## 用途

- 在 `ready_judgement_conditional__downstream_still_locked` 后，
  把下一手正式收缩到“最小集成验证准备”。
- 这页不直接宣布：
  - `risk_model_ready`
  - 三段输出解锁
- 这页只负责：
  - 明确当前最小集成验证到底验证什么
  - 说明为什么它是当前最小剩余缺口

## 当前结论

- 当前 `covariance_model_id` 已推进到：
  - `ready_judgement_conditional__downstream_still_locked`
- 当前最顺下一手不是：
  - 回头重开多家族
  - 继续补 fresh-run
- 当前最顺下一手是：
  - 做一轮最小集成验证，
    检查下游三段对当前上游状态的消费边界是否一致

## 一、最小集成验证只看什么

- 只看：
  - `target_weight` 是否仍只要求“上游风险输入已可判断”
  - `portfolio_tracking_error` 是否允许消费当前更高一档的 `covariance_model_id` 状态
  - `adjusted_position_weight` 是否仍只经由 `target_weight` 间接受影响
- 不看：
  - 优化器真实数值输出
  - tracking error 正式数值输出
  - 最终权重真实运行

## 二、当前已经发现的最小缺口

- 当前已发现：
  - `A5_portfolio_tracking_error_covariance最小输入层页__20260716.md`
    仍停在旧状态集合，
    尚未吸收 `unique_model_frozen__not_ready`
    与 `ready_judgement_conditional__downstream_still_locked`
- 当前未发现：
  - `target_weight` 对 `covariance_model_id` 的消费边界出现相反口径

## 三、当前必须守住的边界

- 即便最小集成验证通过，也不能直接写成：
  - `risk_model_ready`
  - `三段输出已自动解锁`
- 最小集成验证的价值只是：
  - 确认合同未漂移
  - 把旧状态口径修正到当前主线真实状态

## 四、主负责人裁决

- 当前先做：
  - 修正 `portfolio_tracking_error` 页里的旧状态集合
  - 把“下游仍锁定”的禁止性条款同步写入上游正式页
- 当前下一手切到：
  - `最小集成验证执行`

## 五、一句话口径

- 当前 `covariance_model_id` 已不再缺：
  - 模型本体证据
- 当前最小剩余缺口已压缩为：
  - `下游消费边界的一致性校验`

## 回链

- `A5_covariance_model_id_ready判断_多家AI回收记录与主负责人裁决__20260716.md`
- `A5_covariance_model_id_实现前口径判断页__20260716.md`
- `A5_portfolio_tracking_error_covariance最小输入层页__20260716.md`
