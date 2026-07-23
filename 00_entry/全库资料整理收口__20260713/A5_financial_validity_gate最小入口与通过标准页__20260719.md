# A5 financial validity gate 最小入口与通过标准页

更新时间：2026-07-19

## 用途

- 把 `FV gate v0` 的最小入口、最小通过标准、最小失败回退规则正式冻结。
- 本页吸收 2026-07-19 本轮多家 AI 回包，但不把临时粘贴路径当正式真值来源。
- 本页不宣布：
  - `financial-valid`
  - `output_passed`
  - `implementation ready`
- 本页只回答：
  - `FV gate v0` 第一手最小入口到底是什么
  - v0 通过到底最小要产出什么
  - v0 失败后应该回退到哪里

## 一、主负责人裁决

- 当前选：
  - `最小回测入口`
- 但当前选的不是：
  - 直接铺完整回测平台
  - 单独把 `样本外入口` 作为平行第一主线
  - 先跑结果、再临时解释怎么算通过
- 当前正式口径是：
  - `入口形态 = 最小回测入口`
  - `执行前置 = 先冻结最小合同与最小成绩单字段`
  - `holdout = 回测内规则，不另开平行入口`
  - `成本口径 = degraded_fixed_cost`

## 二、为什么这样选

- 原因 1：
  - `Cursor`、`Kimi`、`GLM` 主流都支持先开 `最小回测入口`
- 原因 2：
  - `GPT`、`DeepSeek` 共同强调：
    - 先冻结合同
    - 先冻结成绩单字段
    - 防止 `v0` 滑成大平台或口径漂移
- 原因 3：
  - 当前仓内已经有：
    - same-batch `adjusted_position_weight`
    - 历史 OHLCV
    - benchmark series
    - returns panel
  - 适合开最小回测，而不是继续停在纯讨论
- 原因 4：
  - 当前真正缺的是：
    - 独立 `FV gate` 入口合同
    - 最小成绩单合同
  - 不是再补同构 `execution evidence`

## 三、为什么不选另外两类第一手

- 当前不选：
  - `最小样本外入口` 作为独立第一主线
- 原因：
  - 它应作为 `最小回测入口` 内嵌的 `holdout` 规则先出现
  - 当前不需要再开第二条并行主线
- 当前不选：
  - `最小合同冻结入口` 作为唯一终点
- 原因：
  - 合同冻结是当前必须先做的前置动作
  - 但它本身不是金融验证入口的最终形态
- 因此当前最准确写法是：
  - `contract-first minimal backtest entry`

## 四、FV gate v0 最小入口定义

- 消费对象固定为：
  - `02_runtime/a5_g5_adjusted_position_weight_validation/artifacts/adjusted_position_weight_validation/covariance_target_weight_pte_apw_same_batch_latest.json`
- 上游回链必须可追溯到：
  - `covariance -> target_weight -> portfolio_tracking_error -> adjusted_position_weight`
- 最小输入层至少包含：
  - 一段可复现历史 OHLCV
  - 一段可复现 benchmark series
  - 同窗口 returns / active returns 口径
  - same-batch APW 权重产物
- 当前内嵌规则固定为：
  - 最小时间窗先冻结，不追求长历史
  - `holdout` 作为回测内规则必须存在
  - 成本 / 冲击当前只允许写成：
    - `degraded_fixed_cost`
- 当前第一手不做：
  - 稳健性全家桶
  - 参数网格
  - 多市场并行
  - 完整平台化

## 五、FV gate v0 最小成绩单合同

### 必填字段

| 字段 | 含义 |
|---|---|
| `run_id` | 本轮 FV gate 运行 ID |
| `consumed_artifact_id` | 所消费 same-batch APW 产物 ID |
| `window_start` | 回测起点 |
| `window_end` | 回测终点 |
| `benchmark_id` | 基准 ID |
| `holdout_split_rule` | 样本切分规则 |
| `cost_model` | 当前只能是 `degraded_fixed_cost` |
| `gross_metrics` | 无成本指标集合 |
| `net_metrics` | 有成本指标集合 |
| `in_sample_metrics` | 样本内最小指标集合 |
| `holdout_metrics` | holdout 最小指标集合 |
| `turnover` | 换手或等价交易强度指标 |
| `max_drawdown` | 最大回撤或等价回撤指标 |
| `run_status` | `success` 或 `contract_abort` |
| `abort_reason` | 失败时必填 |
| `forbidden_claim_check` | 显式确认未写 `financial-valid` / `output_passed` |
| `need_evidence_items` | 仍未证明的事项列表 |

### 最小通过

- `FV gate v0` 的通过当前只允许写成：
  - `FV_gate_v0_evidence_produced`
- 通过必须同时满足：
  - same-batch APW 产物被成功消费
  - 成绩单字段完整可审计
  - `in_sample` 与 `holdout` 都有结果
  - 有成本 / 无成本各一版结果
  - 成功 / 失败路径合同清晰
- 通过当前仍不等于：
  - `financial-valid`
  - `output_passed`
  - 样本外泛化已证明

### 最小不通过

- 任一情况都应判为：
  - `FV_gate_v0_not_passed`
- 包括：
  - 吃不到链产物
  - 成绩单字段缺失
  - 没有 `holdout`
  - 成本口径缺失
  - 结果不可复现
  - 偷写禁止宣称

## 六、最小失败回退规则

| 失败类型 | 回退到 | 当前不做什么 |
|---|---|---|
| 工程/合同断裂 | 回修层 1-3 对应 runtime 缺口 | 不重开投票页 / 裁决页 / 回收模板；不升格状态名 |
| 金融假设失败 | 留在 `FV gate` 内调整最小信号组合、评价卡、降级成本假设 | 不把 runtime 链判废；不写成 `financial-valid` |
| 范围越界 | 打回本页冻结范围 | 不把越界方案当成必须扩 scope |

- 当前总原则是：
  - 工程失败与金融失败分轨处理
  - 不因金融失败否定已通过的工程链

## 七、NEED_EVIDENCE 清单

- 当前必须继续保留：
  - `financial-valid`
  - `output_passed`
  - 冲击模型已完备
  - 稳健性已充分
  - 严格 out-of-time 泛化已证明
  - 可投产 / ready to deploy

## 八、禁止项

- 禁止项 1：
  - 把 `runtime-backed` 写成 `financial-valid`
- 禁止项 2：
  - 把 `FV_gate_v0_evidence_produced` 写成 `output_passed`
- 禁止项 3：
  - 在 `v0` 第一手就铺完整回测平台
- 禁止项 4：
  - 把 `holdout` 单独偷换成第二条平行主线
- 禁止项 5：
  - 用一次最小成绩单结果宣布 alpha 已被证明

## 九、当前下一手

- 当前正式下一手是：
  - 基于首轮 `FV gate v0` 成绩单，留在 `FV gate` 内调整：
    - 最小信号组合
    - 最小评价卡
    - 降级成本假设
  - 当前已新增：
    - `A5_FV_gate_v0_最小信号组合卡__20260719.md`
    - `A5_FV_gate_v0_最小评价卡__20260719.md`
    - `fv_gate_v0_runtime_params_round2_template_v1.json`
  - 当前不回退去否定工程链
  - 当前也不扩大成完整回测平台

## 九点一、2026-07-19 首轮 FV gate v0 最小执行结果

- 本轮已新增 runtime 入口：
  - `02_runtime/a5_g5_financial_validity_gate_v0/`
- 本轮已新增首轮成绩单：
  - `fv_gate_v0_scorecard_latest.json`
  - `fv_gate_v0_scorecard_latest.tsv`
- 本轮执行结果是：
  - `run_status = success`
  - `gate_result = FV_gate_v0_evidence_produced`
- 这说明当前已经证明：
  - `FV gate v0` 不是空转合同
  - same-batch APW 已可被最小回测入口真实消费
  - `holdout` 与 `degraded_fixed_cost` 已进入真实成绩单
- 但本轮成绩单同时显示：
  - `gross total_return = -0.01824819`
  - `net total_return = -0.01860149`
  - `holdout net total_return = -0.00764334`
  - `net active_total_return = -0.13756576`
- 因此当前最准确判断是：
  - 工程上：
    - `FV gate v0` 入口已执行成功
  - 金融上：
    - 当前首轮最小成绩单未支持正向金融结论
- 这触发的应是：
  - `金融假设失败留在 FV gate`
- 当前为第二轮已冻结：
  - 最小信号组合卡
  - 最小评价卡
  - round2 runtime params 挂点
- 这不触发：
  - 回退否定层 1-3 工程链
  - 把当前结果误写成 `financial-valid`
  - 把当前结果误写成 `output_passed`

## 九点二、2026-07-19 第二轮 A/B 最小对照结果

- 本轮又新增：
  - `run_fv_gate_v0_round2_chain_v1.py`
  - `fv_gate_v0_round2_scorecard_latest.json`
  - `fv_gate_v0_round2_breakout_scorecard_latest.json`
- 本轮已实跑的第二轮候选是：
  - A：`trend_pullback_confirmation_v1`
  - B：`breakout_close_volume_confirmation_v1`
- 当前对照结果是：
  - A 的 `net total_return = -0.01708055`
  - A 的 `holdout net total_return = -0.00622454`
  - A 的 `net active_total_return = -0.13604482`
  - B 的 `net total_return = -0.0185599`
  - B 的 `holdout net total_return = -0.0076204`
  - B 的 `net active_total_return = -0.13752417`
- 当前新增含义：
  - A 相比首轮 proxy 基线有方向性改善
  - B 虽相对首轮略有改善，但弱于 A，且回撤更差
  - 当前最佳口径仍是：
    - `improved_but_still_negative`
- 因此当前主负责人继续选：
  - 留在 `FV gate`
  - 继续细化 A 候选的过滤层 / 排序逻辑
- 当前不选：
  - 把 B 升成主候选
  - 回退否定工程链
  - 扩成完整策略池

## 九点三、2026-07-19 第三轮过滤失败与 risk-lite 改善

- 本轮又新增：
  - `fv_gate_v0_runtime_params_round3_trend_filter_template_v1.json`
  - `fv_gate_v0_runtime_params_round3_trend_risklite_template_v1.json`
  - `fv_gate_v0_round3_risklite_scorecard_latest.json`
- 本轮先试的第三轮过滤版触发：
  - `non_positive_alpha_sum`
- 其含义是：
  - 当前更严趋势稳定过滤把三只样本整体筛空
  - 失败对象是过滤假设，不是工程链
- 本轮随后改为：
  - 保留 A 候选原始排序
  - 不加过滤器
  - 只把 `final_size_scalar` 从 `0.82` 下调到 `0.6`
- risk-lite 第三轮结果显示：
  - `net total_return = -0.01247598`
  - `holdout net total_return = -0.00454041`
  - `net active_total_return = -0.13144024`
  - `net max_drawdown = -0.02229168`
- 相比第二轮 A 候选：
  - 收益继续改善
  - holdout 继续改善
  - active return 继续改善
  - drawdown 继续改善
- 因此当前主负责人最新裁决是：
  - A 候选继续保留为主候选
  - 当前优先继续细化：
    - 风险暴露收缩
    - 排序逻辑
  - 当前暂不优先继续加严过滤层

## 九点四、2026-07-19 第四轮 rank-decay + risk-lite 当前最佳结果

- 本轮又新增：
  - `fv_gate_v0_runtime_params_round4_rankdecay_risklite_template_v1.json`
  - `fv_gate_v0_round4_rankdecay_risklite_scorecard_latest.json`
- 本轮第四轮最小修正是：
  - 保留 A 主候选与 `filter_layer_id = none`
  - 引入：
    - `weight_logic_id = filtered_alpha_rank_to_target_weight_rank_decay_v2`
  - 同时把：
    - `final_size_scalar = 0.5`
- 当前真实输入已明确：
  - rank1 保留原始分数
  - rank2 乘以 `0.72`
  - rank3 乘以 `0.45`
- 第四轮结果是：
  - `net total_return = -0.00947495`
  - `holdout net total_return = -0.00291711`
  - `net active_total_return = -0.12843922`
  - `net max_drawdown = -0.01794461`
- 相比第三轮 risk-lite：
  - 收益继续改善
  - holdout 继续改善
  - active return 继续改善
  - drawdown 继续改善
- 当前因此更新为：
  - 第四轮 `rank-decay + risk-lite` 是当前最佳最小口径
  - 当前最准确标签仍是：
    - `improved_but_still_negative`
- 当前又已独立复跑为：
  - `fv_gate_v0_current_best_scorecard_latest.json`
- 这说明当前最佳最小口径不再只是：
  - `round4 latest`
- 而是已经成为：
  - 可单独引用、可继续对比的 `current_best` 基线
- 当前主负责人裁决收口为：
  - 先冻结当前最佳最小口径
  - 暂不继续切主候选
  - 暂不继续追加更严过滤
  - 暂不继续微调：
    - `final_size_scalar`
    - `rank-decay`

## 九点五、2026-07-19 current_best 后续方向裁决吸收

- 本轮已吸收 `Cursor` 的方向回包。
- 当前正式选的是：
  - 方案 C：
    - 先冻结，不再继续微调
- 当前正式不选的是：
  - 方案 A：
    - 继续压风险暴露
  - 方案 B：
    - 继续细化 `rank-decay`
- 当前新的正式写法是：
  - `current_best = tuning_frozen__no_further_scalar_or_rankdecay_microtune`
- 当前新增含义是：
  - 在本窗口 / 本 benchmark / 本 holdout / 本成本口径下，
    不再继续跑：
    - 更低 `final_size_scalar`
    - 更细 `rank-decay`
- 当前冻结不是：
  - `financial-valid`
  - `output_passed`
- 当前冻结只是：
  - 微调停止
  - 基线保留
  - 等新的证据类型或新的样本边界

## 九点六、2026-07-19 v1 sample boundary 相邻窗复跑

- 本轮已按 `Cursor` 规划进入：
  - `FV_gate_v1_sample_boundary`
- 当前已使用：
  - `current_best` 冻结四元组
  - 相邻窗口 OHLCV / benchmark / covariance fresh 输入
  复跑最小成绩单
- 当前相邻窗结果为：
  - `net total_return = 0.00197364`
  - `holdout net total_return = 0.00485478`
  - `net active_total_return = 0.03054991`
  - `net max_drawdown = -0.00983588`
- 相比 `v0 current_best`：
  - `net total_return` 由负转正
  - `holdout net total_return` 由负转正
  - `net active_total_return` 由大负转正
  - `max_drawdown` 继续收敛
- 当前新增含义是：
  - `current_best` 冻结合同在新样本边界上没有崩塌
  - 当前已获得：
    - `sample boundary reproduced` 型新证据
- 当前最准确标签是：
  - `sample_boundary_reproduced__still_need_evidence`
- 当前仍不能写成：
  - `financial-valid`
  - `output_passed`
- 当前主负责人裁决更新为：
  - `v1 sample boundary` 这一段已完成
  - 当前下一手不再是继续相邻窗复跑
  - 当前下一手应切到：
    - 是否进入 `new evidence type` 子阶段的统筹判断

## 九点七、2026-07-19 cost_sensitivity_v0 小成本带

- 本轮已按 `Cursor` 统筹进入：
  - `FV_gate_new_evidence_type`
  - 首个子阶段：
    - `cost_sensitivity_v0`
- 当前使用的是：
  - `v1 sample boundary`
    的冻结合同与样本边界
- 当前预声明小成本带为：
  - `5bps`
  - `15bps`
  - `25bps`
- 当前 band summary 为：
  - `min_net_total_return = 0.00184768`
  - `max_net_total_return = 0.0020996`
  - `min_holdout_net_total_return = 0.00485478`
  - `max_holdout_net_total_return = 0.00485478`
  - `min_net_active_total_return = 0.03042395`
  - `max_net_active_total_return = 0.03067587`
  - `worst_net_max_drawdown = -0.00983588`
- 当前 band label 为：
  - `cost_band_stable__still_need_evidence`
- 当前新增含义是：
  - 在预声明小成本带内，
    当前正向结果没有塌掉
  - 这为：
    - `degraded_fixed_cost`
      在小带内不脆弱
    提供了第一手新证据
- 当前仍不能写成：
  - `financial-valid`
  - `output_passed`
- 当前主负责人裁决更新为：
  - `cost_sensitivity_v0` 已完成第一手最小带验证
  - 当前下一手不再是继续扩成本带
  - 当前下一手应切到：
    - 是否进入第二个 `new evidence type` 子阶段的统筹判断

## 九点八、2026-07-19 holding_rule_v0 最小持有规则对照

- 本轮已按 `Cursor` 统筹进入：
  - `FV_gate_new_evidence_type`
  - 第二个子阶段：
    - `holding_rule_v0`
- 当前使用的是：
  - `v1 sample boundary + 15bps`
    的冻结合同
- 当前静态基线为：
  - `net total_return = 0.00197364`
  - `holdout net total_return = 0.00485478`
  - `net active_total_return = 0.03054991`
  - `net max_drawdown = -0.00983588`
- 当前唯一新档为：
  - `fixed_period_rebalance_v0`
  - `rebalance_every_trade_days = 20`
- 当前新档结果为：
  - `net total_return = 0.00149584`
  - `holdout net total_return = 0.00461705`
  - `net active_total_return = 0.03007211`
  - `net max_drawdown = -0.00966033`
  - `rebalance_turnover_total = 0.00655254`
  - `rebalance_event_count = 3`
- 当前标签为：
  - `holding_rule_stable__still_need_evidence`
- 当前新增含义是：
  - 在单一预声明的 `20 trade days`
    定期再平衡下，
    冻结合同没有塌到负值
  - 这说明当前正向结果不只绑死在：
    - `single_entry_static_weight_minimal_backtest`
  - 但当前仍不能写成：
    - `financial-valid`
    - `output_passed`
- 当前主负责人裁决更新为：
  - `holding_rule_v0` 已完成第一手最小持有规则对照
  - 当前下一手应再次交回：
    - `Cursor`
      统筹是否进入第三类 `new evidence type`

## 九点九、2026-07-19 window_consistency_v0 跨窗符号对照

- 本轮已按 `Cursor` 新统筹进入：
  - `FV_gate_window_consistency_v0`
- 当前使用的是：
  - `v0 current_best window`
  - `v1 adjacent window`
    的同一冻结合同对照
- 当前 `v0 current_best window` 为：
  - `net total_return = -0.00947495`
  - `holdout net total_return = -0.00291711`
  - `net active_total_return = -0.12843922`
  - `net max_drawdown = -0.01794461`
- 当前 `v1 adjacent window` 为：
  - `net total_return = 0.00197364`
  - `holdout net total_return = 0.00485478`
  - `net active_total_return = 0.03054991`
  - `net max_drawdown = -0.00983588`
- 当前标签为：
  - `cross_window_sign_divergence__still_need_evidence`
- 当前新增含义是：
  - 相邻窗正向复验依然成立
  - 但同一冻结合同在两窗上没有保持同符号
  - 因而当前最诚实的跨窗结论不是：
    - `cross_window_stable`
  - 而是：
    - 正式出现跨窗符号分歧
- 当前仍不能写成：
  - `financial-valid`
  - `output_passed`
- 当前主负责人裁决更新为：
  - 当前下一手不默认进入第三类 `new evidence type`
  - 当前已完成：
    - `FV_gate_v2_third_window`
      实跑
  - 当前正式采用第三窗为：
    - `20250909 -> 20251212`
  - 当前三窗标签更新为：
    - `cross_window_return_sign_majority_positive__active_sign_majority_negative__still_need_evidence`
- 当前已按 `Cursor`
  裁决正式新增：
  - `A5_FV_gate_active_underperformance_v0解释层页__20260719.md`
  - `fv_gate_active_underperformance_v0_summary_latest.json`
- 当前不再继续默认抓第四窗
- 当前可正式停在：
  - `still_need_evidence`
- 当前若后续再推进，
  再由 `Cursor`
  统筹是否切回新的
  `new evidence type`

## 十、一句话口径

- 当前最准确写法是：
  - `cross_window_sign_divergence__still_need_evidence`

## 回链

- `A5_financial_validity_gate最小入口与通过标准_多AI前情提要与讨论包__20260718.md`
- `A5_execution_validation到financial_validity_gate阶段切换页__20260718.md`
- `A5_Cursor_Trae_FV_gate协同分区与交接页__20260718.md`
- `A5_执行验证主线正确性与金融模型推进保证吸收页__20260718.md`
- `A5_FV_gate_v0_最小信号组合卡__20260719.md`
- `A5_FV_gate_v0_最小评价卡__20260719.md`
- `A5_FV_gate_v0_当前最佳最小口径冻结页__20260719.md`
- `A5_FV_gate_v0_current_best后续推进主负责人裁决页__20260719.md`
- `A5_FV_gate_v1_sample_boundary阶段页__20260719.md`
- `A5_Cursor仓库熟悉度验收与new_evidence_type统筹页__20260719.md`
- `A5_FV_gate_new_evidence_type_cost_sensitivity_v0阶段页__20260719.md`
- `A5_FV_gate_new_evidence_type_holding_rule_v0阶段页__20260719.md`
- `A5_FV_gate_window_consistency_v0阶段页__20260719.md`
- `A5_FV_gate_window_consistency_v0后续方向_多家AI回收记录与主负责人裁决__20260719.md`
- `A5_FV_gate_v2_third_window准备页__20260719.md`
- `A5_FV_gate_v2_third_window阶段页__20260719.md`
- `A5_FV_gate_active_underperformance_v0解释层页__20260719.md`
- `02_runtime/a5_g5_min_chain_validation/artifacts/a5_g5_same_batch_boundary_audit_latest.json`
