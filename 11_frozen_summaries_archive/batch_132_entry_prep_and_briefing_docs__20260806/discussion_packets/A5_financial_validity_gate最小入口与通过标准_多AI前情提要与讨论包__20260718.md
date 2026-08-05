# A5 financial validity gate 最小入口与通过标准 多AI前情提要与讨论包

更新时间：2026-07-18

## 用途

- 发起一轮只讨论 `financial validity gate` 的多AI框架讨论。
- 这轮不再讨论：
  - `execution-validation` 是否正确
  - 是否继续补同构 `same-batch`
  - 是否重开投票页 / 回收模板主线
- 这轮只回答：
  - `FV gate` 第一手最小入口是什么
  - 最小通过标准是什么
  - 最小失败回退规则是什么

## 一、TASK

- 讨论并收窄：
  - `A5 -> G5` 从 `execution-validation` 切到 `financial validity gate` 后，
    第一手最小入口、最小通过标准、最小失败回退规则应如何定义

## 二、BACKGROUND

- 当前已完成：
  - `covariance -> target_weight -> portfolio_tracking_error -> adjusted_position_weight`
    的 same-batch 串联执行
  - `G5 min chain success / pte_failure / apw_failure`
  - 三段 frozen 边界 `runtime_backed = true`
- 当前已正式切换为：
  - `execution-validation` 优先主线阶段性结束
  - 下一手切到：
    - `financial validity gate`
- 当前已正式写明：
  - `runtime correctness substantially de-risked`
  - `financial validity still NEED_EVIDENCE`
- 当前仓内已盘点：
  - `02_runtime/` 下尚无 `A5 -> G5` 独立 `FV gate` 最短入口

## 三、KNOWN_CONSTRAINTS

- 约束 1：
  - 不能把 `runtime-backed` 写成：
    - `financial-valid`
    - `output_passed`
- 约束 2：
  - 不能回到：
    - 投票页
    - 裁决页
    - 回收模板
    主线
- 约束 3：
  - 当前只讨论：
    - `FV gate` 最小入口
    - 最小通过标准
    - 最小失败回退规则
- 约束 4：
  - 不要一上来就铺：
    - 全量回测平台
    - 多市场并行
    - 参数网格
    - 稳健性全家桶
- 约束 5：
  - 必须区分：
    - 工程正确性已证明到哪
    - 金融有效性尚未证明到哪

## 四、DISCUSSION_SCOPE

- 本轮允许讨论：
  - `FV gate` 第一步到底是最小回测入口、最小样本外入口，还是其他更窄入口
  - 最小通过标准至少要包含哪些字段
  - 最小失败回退规则如何写，才不会把工程链和金融假设混为一谈
- 本轮不要展开：
  - execution-validation 对不对
  - 哪个 alpha 一定有效
  - 全量平台架构
  - 重新讨论 `not_output_passed` 解除裁决

## 五、FREE_GUESS_RANGE

- 允许合理推测：
  - 在当前项目上下文下，最适合的 `FV gate v0` 入口是什么
  - 最小 holdout、最小成本口径、最小成绩单长什么样
- 必须写 `NEED_EVIDENCE`：
  - 若你主张：
    - `financial-valid`
    - 样本外泛化已证明
    - 稳健性已充分
    - 冲击模型已完备

## 六、当前已收窄出的候选口径

- 当前 `Cursor` 已建议的第一手是：
  - `最小回测入口（分阶段第一手）`
- 其特点是：
  - 消费 same-batch `adjusted_position_weight`
  - holdout 作为回测内规则，不另开平行入口
  - 成本 / 冲击当前先用降级固定成本口径
  - 稳健性属于第二档，不是第一手
- 当前需要多AI讨论的不是：
  - 这条建议“能不能存在”
- 而是：
  - 它是不是最优第一手
  - 若不是，更好的最小入口是什么

## 七、希望拿到的输出

- 请至少给出 2-3 个方案：
  - 方案 A：最小回测入口
  - 方案 B：最小样本外入口
  - 方案 C：其他你认为更稳的最小入口
- 对每个方案必须说明：
  - 核心思路
  - 适用条件
  - 优点
  - 缺点
  - 风险
  - NEED_EVIDENCE
- 最后必须给出：
  - 你最推荐的方案
  - 当前唯一最小下一步

## 八、输出合同

1. 结论摘要
2. 方案对比（至少 2 个）
3. 最推荐方案
4. 当前最小下一步
5. 风险提醒

## 九、一句话口径

- 本轮不是要讨论：
  - `execution-validation` 还要不要继续
- 本轮只讨论：
  - `FV gate v0` 最小应该怎么开

## 回链

- `A5_Cursor精读路径与FV_gate框架讨论包__20260718.md`
- `A5_execution_validation到financial_validity_gate阶段切换页__20260718.md`
- `A5_Cursor_Trae_FV_gate协同分区与交接页__20260718.md`
- `A5_执行验证主线正确性与金融模型推进保证吸收页__20260718.md`
- `02_runtime/a5_g5_min_chain_validation/artifacts/a5_g5_same_batch_boundary_audit_latest.json`
