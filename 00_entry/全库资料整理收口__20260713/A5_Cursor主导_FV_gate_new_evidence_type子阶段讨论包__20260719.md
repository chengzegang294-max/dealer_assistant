# A5 Cursor 主导 FV gate new evidence type 子阶段讨论包

更新时间：2026-07-19

## 用途

- 在 `FV_gate_v1_sample_boundary` 已完成后，请 `Cursor` 统筹判断是否进入：
  - `new evidence type` 子阶段
- 这页不让 `Cursor` 直接改代码或跑命令。
- 这页只让 `Cursor` 领导：
  - 阶段判断
  - 规划排序
  - Trae 执行顺序
  - 停点定义

## 一、当前已完成到哪

- `FV gate v0` 已完成：
  - 最小回测入口
  - A/B 对照
  - strict filter 失败验证
  - risk-lite
  - rank-decay + risk-lite
  - `current_best` 冻结
  - `tuning_frozen`
- `FV_gate_v1_sample_boundary` 已完成：
  - 用 `current_best` 冻结合同在相邻窗复跑
  - 相邻窗结果为：
    - `net total_return = 0.00197364`
    - `holdout net total_return = 0.00485478`
    - `net active_total_return = 0.03054991`
    - `net max_drawdown = -0.00983588`
- 当前标签只能写成：
  - `sample_boundary_reproduced__still_need_evidence`

## 二、现在为什么要讨论 new evidence type

- 当前已经不是：
  - 同窗继续微调
  - 相邻窗重复复跑
- 当前也还不是：
  - `financial-valid`
- 当前最自然的新问题是：
  - 在样本边界已给出正向复验后，
    下一类“新增证据类型”应该先开什么

## 三、当前边界

- 允许讨论：
  - 下一类证据应该是什么
  - 是否需要先停在当前阶段
  - Trae 的第一手执行物是什么
  - 停点与等待条件
- 不允许讨论：
  - 把当前结果写成 `financial-valid`
  - 再回去调 `scalar`
  - 再回去调 `rank-decay`
  - 再开完整回测平台

## 四、希望 Cursor 回答的六个问题

1. 当前 `sample_boundary_reproduced` 是否足以进入新子阶段？
2. 若进入，下一子阶段名是什么？
3. 你建议先开哪类新证据：
   - 新评价维度
   - 新持有规则
   - 新成本/冲击层
   - 还是其他更窄证据
4. 你建议 Trae 的第一执行手是什么？
5. 你建议当前禁止项有哪些？
6. 你建议停点与等待条件怎么写？

## 五、一句话口径

- 这轮不是让 `Cursor` 复读“v1 跑得不错”，而是让它决定：下一类新证据到底先开什么。

## 回链

- `A5_FV_gate_v1_sample_boundary阶段页__20260719.md`
- `A5_financial_validity_gate最小入口与通过标准页__20260719.md`
- `A5_FV_gate_v0_当前最佳最小口径冻结页__20260719.md`
- `A5_Cursor_Trae_FV_gate协同分区与交接页__20260718.md`
