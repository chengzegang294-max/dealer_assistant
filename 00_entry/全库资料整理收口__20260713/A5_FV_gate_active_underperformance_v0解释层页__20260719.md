# A5 FV gate active underperformance v0 解释层页

更新时间：2026-07-19

## 一、当前解释层用途

- 本页用途是：
  - 对
    `FV_gate_v2_third_window`
    之后暴露出的
    `active underperformance`
    主张力
    做正式解释层收口
- 本页不做：
  - 新回测
  - 新 runtime
  - 新参数搜索
  - 新证据类型扩线

## 二、当前唯一解释问题

- 当前唯一解释问题是：
  - 为什么三窗里：
    - `net total_return`
      与
      `holdout net total_return`
      已形成
      `2 正 1 负`
    - 但
      `net active_total_return`
      却形成
      `1 正 2 负`
- 当前本页只回答：
  - active underperformance
    是否已被正式点名
  - 它为什么仍然构成
    `still_need_evidence`
- 当前本页不回答：
  - 这个策略是否已金融有效
  - 是否应立即切到 impact /
    robustness /
    新 evidence type

## 三、证据边界

- 当前只复用既有 hard 产物：
  - `fv_gate_v0_current_best_scorecard_latest.json`
  - `fv_gate_v1_sample_boundary_scorecard_latest.json`
  - `fv_gate_v2_third_window_scorecard_latest.json`
  - `fv_gate_v2_third_window_summary_latest.json`
- 当前新增的 derived summary 为：
  - `fv_gate_active_underperformance_v0_summary_latest.json`
- 当前明确禁止：
  - 以解释层名义重跑新窗
  - 以解释层名义新增信号
  - 以解释层名义扩大成本带
  - 以解释层名义做参数微调

## 四、三窗固定对照表

| window | period | benchmark_total_return | net_total_return | holdout_net_total_return | net_active_total_return | net_max_drawdown |
|---|---|---:|---:|---:|---:|---:|
| `v0_current_best` | `20260401 -> 20260630` | `0.11896427` | `-0.00947495` | `-0.00291711` | `-0.12843922` | `-0.01794461` |
| `v1_adjacent` | `20251215 -> 20260331` | `-0.02857627` | `0.00197364` | `0.00485478` | `0.03054991` | `-0.00983588` |
| `v2_third` | `20250909 -> 20251212` | `0.02537539` | `0.00740809` | `0.00072619` | `-0.0179673` | `-0.00699902` |

## 五、当前主张力

- 当前主张力不是：
  - 组合收益已经完全失真
- 当前主张力是：
  - 组合绝对收益
    在三窗中已出现：
    - `2 positive / 1 negative`
      的多数恢复
  - holdout
    也出现：
    - `2 positive / 1 negative`
      的多数恢复
  - 但相对基准的
    `net active_total_return`
    仍然出现：
    - `1 positive / 2 negative`
      的多数偏负
- 当前最准确口径因此是：
  - 组合在绝对收益层面
    不再是单向失败
  - 但相对基准表现
    仍未形成跨窗一致的正向支持

## 六、为什么仍然只能写 still_need_evidence

- 当前不能写成：
  - `cross_window_consistency_passed`
  - `financial-valid`
  - `output_passed`
- 当前不能升格的原因是：
  - `cross_window_metric_alignment`
    仍未形成
  - 当前三窗并没有同时支持：
    - 绝对收益
    - holdout
    - active return
      的统一正向结论
  - 当前解释层只是把
    `active_sign_majority_negative`
    这个新停点正式点名，
    不是把它消除

## 七、主负责人解释结论

- 当前正式解释结论为：
  - `active underperformance`
    已成为
    `FV gate`
    第三窗之后最需要被明确写出的主张力
  - 它说明：
    - 当前 frozen contract
      在跨窗绝对收益层面
      已出现多数恢复
    - 但在相对基准层面
      仍存在多数偏负的未闭合问题
- 当前解释层标签继续保持：
  - `cross_window_return_sign_majority_positive__active_sign_majority_negative__still_need_evidence`

## 八、停止规则

- 当前本页落盘并回填后即停
- 当前不顺手做：
  - 第四窗
  - 新 runtime
  - 新 evidence type
  - impact / robustness
    全家桶

## 九、回链

- `A5_FV_gate_v2_third_window阶段页__20260719.md`
- `A5_Cursor主导_FV_gate_post_third_window_next_hand讨论包__20260719.md`
- `02_runtime/a5_g5_financial_validity_gate_v0/artifacts/fv_gate_active_underperformance_v0/fv_gate_active_underperformance_v0_summary_latest.json`

## 十、一句话口径

- 当前最准确写法是：`active_underperformance_is_now_formally_named_as_the_primary_post_third_window_tension__still_need_evidence`。
