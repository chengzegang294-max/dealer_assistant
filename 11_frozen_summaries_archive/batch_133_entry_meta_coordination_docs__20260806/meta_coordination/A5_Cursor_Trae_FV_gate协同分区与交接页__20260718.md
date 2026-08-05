# A5 Cursor Trae FV gate 协同分区与交接页

更新时间：2026-07-19

## 用途

- 把 `Cursor` 与 `Trae` 的协同边界、写作者锁、唯一下一手正式冻结到 repo-global。
- 这页不替代：
  - `02_runtime/` 下的执行卡
  - 各段执行页
  - `financial validity gate` 正式切换页
- 这页只回答：
  - 用户当前要什么
  - `Cursor` 负责什么
  - `Trae` 负责什么
  - 哪些文件不能并改
  - 当前唯一下一手是什么

## 一、当前主线

- 当前主线不是：
  - 继续补同构 `execution evidence`
  - 回到投票页 / 裁决页 / 回收模板
- 当前主线是：
  - `execution-validation` 优先结束
  - 打开 `financial validity gate`
  - 状态名不升格

## 二、已收敛结论

- 多家 AI 主流已收敛为：
  - 不再无限补 `execution evidence`
  - 不把 `runtime-backed` 写成 `financial-valid`
  - 采用分阶段切换，打开 `financial validity gate`
- `Cursor` 本轮同意：
  - `execution-validation` 主线是对的，且对层 1-3 已基本完成
  - 下一手应切到 `financial validity gate`
- 2026-07-19 本轮补充吸收后又收敛为：
  - `Cursor`、`Kimi`、`GLM` 主流支持：
    - `最小回测入口`
  - `GPT`、`DeepSeek` 主流强调：
    - 先冻结最小合同
    - 先冻结最小成绩单字段
  - 主负责人最终收口为：
    - `contract-first minimal backtest entry`
- `Cursor` 本轮不同意：
  - 把“用户再确认一句”设为硬门槛
  - 再开一轮投票才允许切换
  - 把阶段切换误写成 `output_passed`
  - 一切 gate 就铺完整回测平台

## 三、禁止项

- 禁止项 1：
  - 继续把投票页 / 裁决页 / 回收模板当主线
- 禁止项 2：
  - 继续默认补同构 `same-batch` 证明
- 禁止项 3：
  - 把 `runtime-backed` 偷换成：
    - `financial-valid`
    - `output_passed`
    - `ready to deploy`
- 禁止项 4：
  - `Cursor` 直接改代码、跑命令、接管执行
- 禁止项 5：
  - `Trae` 在无运行证据时自行升格状态名

## 四、状态名冻结表

| 字段 | 当前正式状态 | 当前允许总口径 | 禁止误写 |
|---|---|---|---|
| `covariance_model_id` | `ready_judgement_conditional__downstream_still_locked` | `runtime correctness substantially de-risked` | `risk_model_ready` |
| `target_weight` | `verified_with_degraded_risk__upstream_min_integration_verified__not_output_passed` | `financial validity still NEED_EVIDENCE` | `output_passed` |
| `portfolio_tracking_error` | `pass_conditions_frozen__not_output_passed` | `financial validity still NEED_EVIDENCE` | `financial-valid` |
| `adjusted_position_weight` | `pass_conditions_frozen__not_output_passed` | `financial validity still NEED_EVIDENCE` | `implementation ready` |

## 五、分区表

### Cursor 独占写

- 统筹判断、同意 / 不同意、多家 AI 对照、禁止项、状态名冻结表。
- 只产出：
  - 讨论判断
  - 统筹口径
  - 分区建议
- 不产出：
  - `02_runtime/**` 代码与运行产物

### Trae 独占写

- `02_runtime/**`
  - 脚本
  - 运行卡
  - 产物
  - 索引
- `A5_execution_validation到financial_validity_gate阶段切换页__20260718.md`
- 各段运行回填及主链页中的执行侧更新

### 共享但不能并改

- `A5_G5主链闭合状态页__20260716.md`
- `A5_执行验证主线正确性与金融模型推进保证吸收页__20260718.md`
- `A5_G5_输出闭合判断页__20260716.md`
- 本页

### 旧主线冷冻

- `*多家AI正式发包稿*`
- `*多家AI回收记录模板*`
- `*解除not_output_passed*发包*`

## 六、Cursor 待办与产出回链

- 当前 `Cursor` 本轮已完成：
  - 用户需求理解
  - `Trae` 职责理解
  - 分区方案
  - 协同文件设计
  - 下一手安排
- 当前 `Cursor` 下一手不是：
  - 直接执行
- 当前 `Cursor` 下一手是：
  - 如后续需要，仅继续提供统筹修订稿
- 回链：
  - `A5_Cursor精读路径与FV_gate框架讨论包__20260718.md`
  - `A5_financial_validity_gate最小入口与通过标准_多AI前情提要与讨论包__20260718.md`

## 七、Trae 待办与产出回链

- 当前 `Trae` 待办：
  - 回填第二轮最小信号组合卡 / 评价卡 / round2 params
  - 若后续生成新 APW，则执行第二轮最小成绩单
  - 保持失败留在 `FV gate`，不回退否定工程链
- 当前 `Trae` 当前不做：
  - 重开投票页
  - 在无新运行证据时升格状态名

## 八、当前写作者锁

| 文件路径 | 当前写作者 | 当前状态 | 预计释放 |
|---|---|---|---|
| `A5_Cursor_Trae_FV_gate协同分区与交接页__20260718.md` | `Trae` | `writing_execution_side` | `本轮正式落盘后` |
| `A5_financial_validity_gate最小入口与通过标准页__20260719.md` | `Trae` | `writing` | `本轮正式落盘后` |
| `02_runtime/a5_g5_financial_validity_gate_v0/README.md` | `Trae` | `writing_runtime_skeleton` | `本轮正式落盘后` |
| `A5_G5主链闭合状态页__20260716.md` | `Trae` | `pending_next_hand_backfill` | `回填完成后` |
| `README.md` | `Trae` | `pending_index_backfill` | `回填完成后` |

## 九、当前唯一下一手

- 当前唯一下一手是：
  - `Trae` 已正式冻结：
    - `FV gate v0` 最小入口与最小通过标准
  - `Trae` 已创建：
    - `02_runtime/a5_g5_financial_validity_gate_v0/README.md`
    - `fv_gate_v0_runtime_params_template_v1.json`
    - `fv_gate_v0_scorecard_template_v1.json`
    - `run_fv_gate_v0_minimal_backtest_v1.py`
  - `Trae` 已实跑：
    - `fv_gate_v0_scorecard_latest.json`
  - 当前下一手推进到：
    - 当前先冻结第四轮 `rank-decay + risk-lite` 为最佳最小口径
    - 并以 `current_best` 独立基线继续后续比较
    - 当前已吸收 `Cursor` 裁决为：
      - `tuning_frozen__no_further_scalar_or_rankdecay_microtune`
    - 当前再推进一手已完成：
      - `FV_gate_v1_sample_boundary` 相邻窗复跑
      - 标签：
        - `sample_boundary_reproduced__still_need_evidence`
    - 当前再推进一手又已完成：
      - `cost_sensitivity_v0` 小成本带
      - 标签：
        - `cost_band_stable__still_need_evidence`
    - 当前下一手改写为：
      - 由 `Cursor` 统筹是否进入第二个 `new evidence type` 子阶段
      - 当前已吸收 `Cursor` 熟悉度与首个证据类型统筹：
        - `A5_Cursor仓库熟悉度验收与new_evidence_type统筹页__20260719.md`
      - 讨论入口：
        - `A5_Cursor主导_FV_gate_second_new_evidence_type讨论包__20260719.md`
      - `Trae` 在第二个证据类型统筹结论前暂不直接开新执行线
    - 当前已按该统筹结论正式落地：
      - `A5_FV_gate_new_evidence_type_holding_rule_v0阶段页__20260719.md`
      - `fv_gate_holding_rule_v0_summary_latest.json`
      - `fv_gate_holding_rule_v0_fixed_period_rebalance_v0_20d_scorecard_latest.json`
    - 当前第二个 `new evidence type` 标签已更新为：
      - `holding_rule_stable__still_need_evidence`
    - 当前下一手再次改写为：
      - 先由 `Trae` 吸收 `Cursor` 新回包并正式落地：
        - `FV_gate_window_consistency_v0`
    - 当前又已按该统筹结论正式落地：
      - `A5_FV_gate_window_consistency_v0阶段页__20260719.md`
      - `fv_gate_window_consistency_v0_summary_latest.json`
    - 当前跨窗标签已更新为：
      - `cross_window_sign_divergence__still_need_evidence`
    - 当前下一手再次改写为：
      - 已先由 `Trae` 备好：
        - `window_consistency_v0`
          后续方向多AI三件套
      - 当前先等待：
        - `GPT / DeepSeek / Kimi / GLM / Qwen`
          回包
    - 当前又已完成：
      - `A5_FV_gate_window_consistency_v0后续方向_多家AI回收记录与主负责人裁决__20260719.md`
      - `A5_FV_gate_v2_third_window准备页__20260719.md`
    - 当前主负责人已裁定并完成：
      - `FV_gate_v2_third_window_preparation`
      - `FV_gate_v2_third_window`
        实跑
    - 当前第三窗正式采用为：
      - `20250909 -> 20251212`
    - 当前三窗最新标签为：
      - `cross_window_return_sign_majority_positive__active_sign_majority_negative__still_need_evidence`
    - 当前 `Cursor` 已统筹并选定：
      - 先开：
        - `active underperformance`
          极窄解释层
    - 当前 `Trae` 已正式落地：
      - `A5_FV_gate_active_underperformance_v0解释层页__20260719.md`
      - `fv_gate_active_underperformance_v0_summary_latest.json`
    - 当前下一手再次改写为：
      - 当前解释层已完成
      - 当前可正式停在：
        - `still_need_evidence`
      - 后续若再推进，
        再由 `Cursor`
        统筹是否切回新的
        `new evidence type`
    - `trend_pullback_confirmation_v1` 保持主候选
    - `breakout_close_volume_confirmation_v1` 保持最小对照
    - 不回退否定工程链

## 九点一、2026-07-19 产品原型侧最新同步

- 当前在
  `FV gate evidence packet v0`
  冻结后，
  `Trae`
  已继续把
  `A股 P0`
  推进到原型合同层
- 当前已正式落盘：
  - `A5_A股P0原型阶段金融披露与条件式门禁页__20260719.md`
  - `A5_A股P0原型合同细化页__20260719.md`
  - `A5_A股P0首页入口页__20260719.md`
  - `A5_A股P0首页四卡细化页__20260719.md`
  - `A5_A股P0标的分析页与问答下钻页__20260719.md`
- 当前其含义是：
  - 产品原型侧已不再缺抽象口径
  - 当前更自然的问题改写为：
    - 由 `Cursor`
      统筹原型阶段第一手最该继续细化的唯一对象
- 当前为便于快速同步，
  `Trae`
  又已补出：
  - `A5_Cursor同步包_A股P0原型最新进展与下一手问题__20260719.md`

## 十、四停点触发记录

- 当前四停点触发记录：
  - `none`

## 十一、回链

- `A5_financial_validity_gate最小入口与通过标准页__20260719.md`
- `A5_执行验证主线正确性与金融模型推进保证吸收页__20260718.md`
- `A5_G5主链闭合状态页__20260716.md`
- `02_runtime/a5_g5_min_chain_validation/artifacts/a5_g5_same_batch_boundary_audit_latest.json`
