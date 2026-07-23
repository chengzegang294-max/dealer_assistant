# A5 target_weight 升级判断重开 多家AI回收记录与主负责人裁决

更新时间：2026-07-16

## 用途

- 吸收 `target_weight` 升级判断重开这一轮多AI回包。
- 这页不讨论：
  - `output_passed`
  - `正式优化器 ready`
  - `covariance_model_id ready`
- 这页只讨论：
  - 在唯一附加条件已补到可判断层后
  - 当前最稳的正式升级写法应写到哪一档

## 一、回收总表

| 模型 | 有效性 | 推荐方案 | 最终倾向 | 核心理由 | READY 幻觉风险 | 当前最小下一步 | 备注 |
|---|---|---|---|---|---|---|---|
| `GPT` | `有效` | `平衡` | `继续推进一档，但不写 passed` | 已具备进入下一档正式升级判断结论的条件 | `中低` | 主负责人正式收口当前最稳升级写法 | 对题且边界最稳 |
| `DeepSeek` | `有效` | `平衡` | `verified_with_degraded_risk__not_output_passed` | 书面验收已消化唯一附加条件 | `中等` | 更新 `target_weight` 状态并显式保留 `future_only` 风险边界 | 对题且给出可执行状态名 |
| `Kimi` | `有效但偏激进` | `平衡` | `implementation_prep_candidate_with_degraded_risk_constraint` | 附加条件已满足，应打开实现前准备入口 | `中等` | 准备 implementation_prep 文档 | 方向有效，但命名偏激进 |
| `GLM` | `有效` | `平衡` | `升级判断成立，但保留 pass_conditions_frozen 写法` | 书面验收已通过，应正式确认升级判断 | `低` | 在总表中保留当前状态并备注“降级模式升级判断已通过” | 对题但推进感偏弱 |
| `Qwen` | `有效但保守` | `平衡` | `先等 covariance 闭合再最终裁决` | 当前未闭合项仍可能引发回退 | `低` | 等待 `covariance_model_id` 正式闭合 | 对题，但低估了当前已完成收口 |

## 二、单模型吸收

### 1. `GPT`

- 有效性：
  - `有效`
- 推荐方案：
  - `平衡`
- 最终倾向：
  - 把当前状态从“纯 `conditional`”推进到：
    - `已具备进入下一档正式升级判断结论的条件`
- 主负责人备注：
  - 这是当前最稳的文字口径。
  - 但它没有给出仓内更利于回填的状态枚举名。

### 2. `DeepSeek`

- 有效性：
  - `有效`
- 推荐方案：
  - `平衡`
- 最终倾向：
  - `verified_with_degraded_risk__not_output_passed`
- 主负责人备注：
  - 这是当前最适合作为仓内状态名的提案。
  - 它体现了“已推进一档”，同时保留：
    - `degraded_risk`
    - `not_output_passed`

### 3. `Kimi`

- 有效性：
  - `有效但偏激进`
- 推荐方案：
  - `平衡`
- 最终倾向：
  - `implementation_prep_candidate_with_degraded_risk_constraint`
- 主负责人备注：
  - 方向上承认当前确有推进。
  - 但该命名过于接近：
    - `implementation_ready`
  - 与当前仓内总边界：
    - `contract_layer_ready_but_not_implementation_ready`
    不够稳妥。

### 4. `GLM`

- 有效性：
  - `有效`
- 推荐方案：
  - `平衡`
- 最终倾向：
  - 升级判断成立，但状态枚举继续保留：
    - `pass_conditions_frozen__not_output_passed`
- 主负责人备注：
  - 这是最保守的可推进写法。
  - 但它会低估“已推进一档”的新增事实。

### 5. `Qwen`

- 有效性：
  - `有效但保守`
- 推荐方案：
  - `平衡`
- 最终倾向：
  - 先等 `covariance_model_id` 闭合后再做最终裁决
- 主负责人备注：
  - 它没有串题。
  - 但它把“当前最稳升级写法”退回成“继续等待”，低估了：
    - 边界页
    - 验证清单
    - 书面验收
    已完成这一事实。

## 三、主负责人裁决

- 当前有效票面不是：
  - 是否通过 `output_passed`
- 当前有效票面是：
  - 是否足以从 `conditional` 再推进一档
- 当前正式裁决为：
  - 采用：
    - `平衡写法`
  - 正式状态名冻结为：
    - `verified_with_degraded_risk__not_output_passed`

## 四、为什么选这个

- 原因 1：
  - 它吸收了 `GPT` 的稳妥口径：
    - 已具备进入下一档正式升级判断结论的条件
- 原因 2：
  - 它吸收了 `DeepSeek` 的状态表达优势：
    - 能形成仓内明确可回填的状态名
- 原因 3：
  - 它不采纳 `Kimi` 的 `implementation_prep_candidate` 命名
  - 因为该命名容易与当前仓内硬边界冲突：
    - `not_implementation_ready`
- 原因 4：
  - 它比 `GLM` 的“继续保留原状态仅加备注”更能反映实际推进

## 五、当前先做什么

- 当前先做：
  - 把 `target_weight` 的当前状态从：
    - `pass_conditions_frozen__not_output_passed`
    推进到：
    - `verified_with_degraded_risk__not_output_passed`
  - 回填到：
    - `A5_G5主链闭合状态页__20260716.md`
    - `A5_实现阻塞项拆解表__20260716.tsv`
    - `A5_G5_输出升格证据总表__20260716.tsv`
    - `README.md`
- 当前暂缓：
  - 直接写成 `output_passed`
  - 直接写成 `implementation_ready`
  - 直接切下游字段升格

## 六、一句话口径

- 当前 `target_weight actual_generation后` 的最稳正式写法是：
  - `verified_with_degraded_risk__not_output_passed`

## 回链

- `A5_target_weight_升级判断重开准备页__20260716.md`
- `A5_degraded_risk_handling_主负责人书面验收页__20260716.md`
- `A5_target_weight_升级判断重开_多AI前情提要与裁决框架__20260716.md`
- `A5_target_weight_升级判断重开_多家AI正式发包稿__20260716.md`
- `A5_target_weight_升级判断重开_多家AI回收记录模板__20260716.md`
