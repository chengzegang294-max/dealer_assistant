# A5 Cursor 仓库熟悉度验收与 new evidence type 统筹页

更新时间：2026-07-19

## 用途

- 吸收 `Cursor` 本轮对仓库主线、真值入口、冻结线与下一阶段方向的回包。
- 这页不替代：
  - runtime 成绩单
  - 阶段执行页
- 这页只回答：
  - `Cursor` 是否已达到当前仓库熟悉度要求
  - `Cursor` 作为统筹负责人当前拍板了什么

## 一、熟悉度验收结论

- 当前主负责人结论是：
  - `Cursor` 本轮已通过当前仓库熟悉度验收
- 理由不是：
  - 它说了一句“建议进入下一阶段”
- 理由是：
  - 它已正确复述：
    - `execution-validation` 如何结束优先主线
    - `FV gate v0` 为什么必须 `tuning_frozen`
    - `FV_gate_v1_sample_boundary` 为什么仍不能写成 `financial-valid`
  - 它已正确区分：
    - 正式裁决页
    - runtime 真证据
    - 讨论包
  - 它已正确指出：
    - 当前唯一真值入口文件
    - 当前已冻结旧线
    - 当前下一手不该由 `Trae` 盲开新执行线

## 二、当前统筹结论

- `Cursor` 当前正式拍板：
  - 应进入：
    - `FV_gate_new_evidence_type`
- 当前首个 new evidence type 不是：
  - 再开第二个相邻窗
  - 再回去调 `scalar`
  - 再回去调 `rank-decay`
- 当前首个 new evidence type 选为：
  - `cost_sensitivity_v0`

## 三、为什么先选 cost_sensitivity_v0

- 原因 1：
  - 当前 `v1 sample boundary` 已给出新样本边界上的正向复验
- 原因 2：
  - 下一步更值钱的不是继续换窗，
    而是确认：
    - `degraded_fixed_cost`
      的结论是否对小成本带敏感
- 原因 3：
  - 这属于：
    - 新证据类型
  - 但又不需要：
    - 解冻信号
    - 解冻排序
    - 解冻暴露
    - 扩完整平台

## 四、对 Trae 的执行授权

- 当前 `Cursor` 已明确允许 `Trae` 做：
  - 先落：
    - `cost_sensitivity_v0` 阶段页
  - 再用唯一冻结合同跑：
    - 预声明小成本带
  - 再把结果回填为：
    - 成本敏感性是否稳定
- 当前 `Cursor` 仍明确禁止 `Trae` 做：
  - 裁决页前盲开新证据线
  - 同窗微调
  - breakout / 过滤 / 扩池
  - 平台化
  - 状态名升格

## 五、当前唯一下一手

- 当前唯一下一手是：
  - 进入：
    - `FV_gate_new_evidence_type / cost_sensitivity_v0`
  - 并使用：
    - `FV_gate_v1_sample_boundary`
      的冻结合同与样本边界
  - 只改变：
    - `one_way_cost_bps`

## 六、一句话口径

- 当前最准确口径是：`Cursor_repository_familiarity_passed__new_evidence_type_cost_sensitivity_v0_selected`。

## 回链

- `A5_Cursor主导_FV_gate_new_evidence_type子阶段讨论包__20260719.md`
- `A5_FV_gate_v1_sample_boundary阶段页__20260719.md`
- `A5_financial_validity_gate最小入口与通过标准页__20260719.md`
- `A5_Cursor_Trae_FV_gate协同分区与交接页__20260718.md`
