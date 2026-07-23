# A5 FV gate evidence packet v0 冻结页

更新时间：2026-07-19

## 一、用途

- 本页只做：
  - `FV gate`
    当前证据包的冻结收口
- 本页不做：
  - 新回测
  - 新 runtime
  - 新证据类型裁决

## 二、已完成证据节点

- 当前已完成并纳入本包的节点为：
  - `v0 current_best`
  - `v1 sample_boundary`
  - `cost_sensitivity_v0`
  - `holding_rule_v0`
  - `window_consistency_v0`
  - `v2 third_window`
  - `active_underperformance_v0`

## 三、当前总标签

- 当前总标签固定为：
  - `cross_window_return_sign_majority_positive__active_sign_majority_negative__still_need_evidence`

## 四、当前包内最小结论

- 当前包内最小结论是：
  - `FV gate`
    已形成一组连续 hard evidence
  - 组合绝对收益与 holdout
    在三窗上已出现：
    - `2 正 1 负`
  - 但相对基准的
    `net active_total_return`
    仍是：
    - `1 正 2 负`
- 因此当前只能保留：
  - `still_need_evidence`

## 五、NEED_EVIDENCE 清单

- 当前仍未证明：
  - `financial-valid`
  - `output_passed`
  - `strict_out_of_time_generalization`
  - `full_impact_model`
  - `robustness_suite`
  - `cross_window_metric_alignment`

## 六、禁止升格项

- 当前明确禁止写成：
  - `financial-valid`
  - `output_passed`
  - `cross_window_consistency_passed`
  - `ready_to_deploy`

## 七、当前暂停口径

- 当前本包正式暂停于：
  - `still_need_evidence`
- 当前再开新的
  `new evidence type`
  之前，必须先由：
  - `Cursor`
    重新统筹
- 当前 `Trae`
  不自行继续开：
  - 第四窗
  - 同窗微调
  - 成本带扩网格
  - 持有规则扩网格
  - 新 runner

## 八、当前唯一入口短链

- 协同页：
  - `A5_Cursor_Trae_FV_gate协同分区与交接页__20260718.md`
- 当前解释层页：
  - `A5_FV_gate_active_underperformance_v0解释层页__20260719.md`

## 九、一句话口径

- 当前最准确写法是：
  - `FV_gate_evidence_packet_v0_frozen__still_need_evidence__new_evidence_type_requires_cursor_recoordination`
