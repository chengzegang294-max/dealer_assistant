# A5 Cursor 主导 FV gate second new evidence type 讨论包

更新时间：2026-07-19

## 用途

- 在 `cost_sensitivity_v0` 已完成后，请 `Cursor` 统筹判断是否进入第二个 `new evidence type` 子阶段。
- 这页不让 `Cursor` 改代码或跑命令。
- 这页只让 `Cursor` 做：
  - 阶段判断
  - 证据类型排序
  - Trae 下一手执行范围
  - 停点定义

## 一、当前已完成到哪

- `FV gate v0` 已完成：
  - `current_best`
  - `tuning_frozen`
- `FV_gate_v1_sample_boundary` 已完成：
  - 相邻窗复验
  - 标签：
    - `sample_boundary_reproduced__still_need_evidence`
- `FV_gate_new_evidence_type / cost_sensitivity_v0` 已完成：
  - `5 / 15 / 25 bps`
    小成本带
  - 标签：
    - `cost_band_stable__still_need_evidence`

## 二、现在为什么轮到第二个 new evidence type

- 当前已经不是：
  - 同窗微调
  - 再换一个相邻窗
  - 再扩同类成本带
- 当前也还不是：
  - `financial-valid`
- 当前最自然的新问题是：
  - 第二类新证据应该先开什么

## 三、当前边界

- 允许讨论：
  - 第二类新证据到底是什么
  - 是否先停在当前状态
  - Trae 的第一执行手
  - 停点与等待条件
- 不允许讨论：
  - 回头微调 `scalar`
  - 回头微调 `rank-decay`
  - 扩完整回测平台
  - 把当前结果误写成 `financial-valid`

## 四、希望 Cursor 回答的问题

1. 当前两类证据是否足以继续进入第二个 `new evidence type`？
2. 若进入，第二个子阶段名是什么？
3. 你建议先开：
   - 新评价维度
   - 新持有规则
   - 更细成本/冲击层
   - 还是其他更窄证据
4. 你建议 Trae 的第一执行手是什么？
5. 你建议当前禁止项有哪些？
6. 你建议停点与等待条件怎么写？

## 五、一句话口径

- 这轮不是让 `Cursor` 重复说“现在还不能写成 financial-valid”，而是让它判断：第二类新证据先开什么。

## 回链

- `A5_Cursor仓库熟悉度验收与new_evidence_type统筹页__20260719.md`
- `A5_FV_gate_new_evidence_type_cost_sensitivity_v0阶段页__20260719.md`
- `A5_FV_gate_v1_sample_boundary阶段页__20260719.md`
- `A5_financial_validity_gate最小入口与通过标准页__20260719.md`
