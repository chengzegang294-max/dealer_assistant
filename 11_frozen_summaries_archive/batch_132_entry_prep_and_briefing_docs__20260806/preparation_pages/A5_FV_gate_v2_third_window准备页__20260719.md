# A5 FV gate v2 third window 准备页

更新时间：2026-07-19

## 用途

- 这页用于把：
  - `window_consistency_v0`
    后续方向
    正式切到：
    - `FV_gate_v2_third_window_preparation`
- 这页不直接声称：
  - 第三窗已可执行
  - 第三窗已得分
  - 第三窗已支持
    `cross_window_consistency_passed`
- 这页只做三件事：
  - 锁唯一候选第三窗
  - 锁当前输入缺口
  - 锁执行前停止规则

## 一、为什么现在进入第三窗准备

- 当前已完成：
  - `sample_boundary_reproduced__still_need_evidence`
  - `cost_band_stable__still_need_evidence`
  - `holding_rule_stable__still_need_evidence`
  - `cross_window_sign_divergence__still_need_evidence`
- 当前最核心未决点是：
  - 同一冻结合同在两窗上出现：
    - `1 : 1`
      的符号分歧
- 当前主负责人已裁定：
  - 第三窗不是立即实跑
  - 但它是当前唯一主线
    的下一手准备对象

## 二、当前冻结合同

- 当前冻结不变的是：
  - `signal_hypothesis_id = trend_pullback_confirmation_v1`
  - `filter_layer_id = none`
  - `weight_logic_id = filtered_alpha_rank_to_target_weight_rank_decay_v2`
  - `final_size_scalar = 0.5`
  - `cost_model = degraded_fixed_cost`
  - `one_way_cost_bps = 15.0`
  - `holdout_trade_days = 15`
- 当前第三窗准备阶段唯一允许变化的是：
  - 时间窗输入

## 三、唯一候选第三窗

- 当前唯一候选第三窗冻结为：
  - `20250701 -> 20250930`
- 当前命名冻结为：
  - `sample20_q3_20250701_20250930`
- 当前选择它的原因是：
  - 与：
    - `20251215 -> 20260331`
    - `20260401 -> 20260630`
    都不重叠
  - 已经完整结束，
    不依赖未来数据
  - 比再向后抓
    `2026Q3`
    更稳，
    不会引入未结束窗口

## 四、当前已存在输入

- 当前已确认存在：
  - `02_runtime/ashare_p0_first_round_validation/data/t02_sources/daily_tushare/t02_daily_tushare_batch__sample20_q2__20260401_20260630.csv`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/raw_daily/t02_daily_tushare_batch__sample20_adjacent60__20251215_20260331.csv`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/raw_daily/t02_daily_tushare_batch__sample20_q1__20260102_20260331.csv`

## 五、当前输入缺口

- 当前尚未发现：
  - `t02_daily_tushare_batch__sample20_q3__20250701_20250930.csv`
  - `covariance_benchmark_series__000300_SH__20250701_20250930.csv`
  - 第三窗对应的
    `covariance_bodyrun_fresh`
    产物
- 当前因此不能直接进入：
  - `FV_gate_v2_third_window`
    实跑

## 六、当前执行前合同

- 当前进入执行前必须先补齐：
  - 第三窗日线样本 csv
  - 第三窗 benchmark csv
  - 第三窗 covariance fresh json
- 当前补齐后唯一允许做的是：
  - 复用现有 frozen contract
  - 生成第三窗最小成绩单
  - 与现有两窗形成三窗对照 summary
- 当前补齐前不允许做的是：
  - 新信号
  - 新排序
  - 新持有规则
  - 新成本带
  - 环境归因分支扩写
  - 第四窗

## 七、当前停止规则

- 若第三窗输入仍不存在：
  - 当前线停在：
    - `input_gated`
  - 这是合法停点，
    不伪装成“已执行”
- 若第三窗执行完成：
  - 本轮立即停止
  - 不顺手继续抓第四窗
- 若第三窗结果仍然造成新的分歧：
  - 当前先回主负责人裁决
  - 不直接把状态写成失败或通过

## 八、当前下一手

- 当前下一手是：
  - 先找第三窗输入是否可直接从仓内或既有来源装配
- 当前不是：
  - 立即重跑
  - 立即环境归因
  - 立即开第三类 `new evidence type`

## 九、状态回填

- 当前本页状态已从：
  - `preparation`
  进入：
  - `executed_with_candidate_switch`
- 当前正式执行页已新增：
  - `A5_FV_gate_v2_third_window阶段页__20260719.md`
- 当前本页继续保留的用途是：
  - 记录候选 A 失败、
    候选 B 采用
    的准备态审计链

## 一句话口径

- 当前最准确写法是：`third_window_preparation_is_closed_with_candidate_switch_and_formal_execution_landed`。
