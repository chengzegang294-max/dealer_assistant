# A5 covariance_model_id downstream_still_locked 唯一剩余锁定原因准备页

更新时间：2026-07-18

## 用途

- 把 `covariance_model_id downstream_still_locked` 后续判断中的唯一附加条件，
  继续压成下一轮唯一新题。
- 这页不宣布：
  - `covariance_model_id ready`
  - `risk_model_ready`
  - 三段输出自动解锁
- 这页只负责：
  - 固定“唯一剩余锁定原因到底是哪一条”
  - 限定候选边界
  - 把下一手收缩到唯一原因裁决

## 当前结论

- 当前 `covariance_model_id` 仍保持：
  - `ready_judgement_conditional__downstream_still_locked`
- 当前后续判断已正式裁为：
  - `conditional`
- 当前已冻结的唯一附加条件是：
  - `唯一剩余锁定原因需收敛为单条正式边界`
- 且该单条正式边界当前已正式裁定为：
  - `下游单段仍未形成可解除 not_output_passed 的正式边界`
- 因此当前最顺下一手不是：
  - 再讨论 ready 旧题
  - 再问输出段是否自动解锁
- 而是：
  - 只问这条单条正式边界到底是什么

## 一、这轮新题是什么

- 这轮新题不是：
  - `covariance_model_id` 是否已 ready
  - `portfolio_tracking_error` 是否再升一档
  - `adjusted_position_weight` 是否解锁
- 这轮新题是：
  - 在当前边界下，
    `downstream_still_locked` 的唯一剩余锁定原因，
    到底应该正式冻结成哪一条

## 二、允许候选方向

- 当前允许候选方向只限于：
  - `下游最小解锁条件尚未书面定义`
  - `下游单段仍未形成可解除 not_output_passed 的正式边界`
  - 与上面等价、但更稳更短的一条正式写法
- 当前不允许：
  - 回到 `ready / not ready` 大题
  - 回到“继续观察/继续验证”的泛化答法
  - 把多个原因一起并列

## 三、主负责人裁决

- 当前先做：
  - 把唯一剩余锁定原因正式冻结为：
    - `下游单段仍未形成可解除 not_output_passed 的正式边界`
  - 把主线切到第一个下游单段：
    - `target_weight`
- 当前暂缓：
  - 继续重问 `covariance_model_id`
- 当前下一手切到：
  - `A5_covariance_model_id_downstream_still_locked唯一剩余锁定原因_回包与主负责人裁决__20260718.md`
  - `A5_target_weight解除not_output_passed正式边界准备页__20260718.md`
  - `A5_target_weight解除not_output_passed正式边界_超窄纯文本正式发包稿__20260718.md`
  - `A5_target_weight解除not_output_passed正式边界_超窄纯文本回收记录模板__20260718.md`

## 四、一句话口径

- 当前主线已进一步压缩到：
  - `target_weight` 的解除 `not_output_passed` 正式边界裁决

## 回链

- `A5_covariance_model_id_downstream_still_locked后续判断_超窄纯文本回包与主负责人裁决__20260718.md`
- `A5_covariance_model_id_最小集成验证执行页__20260717.md`
