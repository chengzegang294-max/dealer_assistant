# TK-R6 IB 回撤阻挡到 TP3 后续对象定义入口 v1

## 作用

- 把 `TK-R6 = IB 回撤阻挡 -> TP3 概率增强` 从综合整理稿里的“可重开结论”推进成更明确的后续对象入口。
- 当前目标不是直接把它写成自动开单规则，而是先固定：
  - 最小语义
  - 最小输入
  - 最小输出
  - 与现有 `IB / DB / CB + Fib TP3` 主线的关系
  - 当前验收边界

## 当前定位

- 层级：
  - `TK` 后续对象层
- 当前角色：
  - `next_object_entry`
- 不是：
  - 当前硬门控
  - 当前独立策略
  - 当前已量化完成对象

## 来源锚点

- 主要来源：
  - `20231219TK外汇交易系统学习资料整理(6)_导出.md`
  - `20231219TK外汇交易系统学习资料整理(6)_吸收结论_v1.md`
- 当前已固定可引用语义：
  - `IB` 是信号最后关口
  - 若价格回撤到 `IB` 后被强力阻挡，则继续走向 `TP3` 的概率增强

## 为什么先开 TK-R6

- 它是新综合整理稿里最贴近当前 `TK` 主线的新增对象。
- 它不要求先新开一整套独立策略家族。
- 它天然连接当前已有主线：
  - `IB / DB / CB`
  - `Fib TP3`
  - `RRR / 最低胜率 / 风险控制`
- 相比：
  - `AO divergence`
  - `B 区域 qualify`
  - `简易顺势交易策略`
  当前 `TK-R6` 更接近可被后续做成诊断标签或对象映射的最小对象。

## 最小语义

- 当前保守写法：
  - 当主信号已成立后，若价格回撤到 `IB` 附近并出现“被阻挡/被拒绝”的结构，则后续延伸到 `TP3` 的概率增强。
- 当前不写成：
  - `触碰 IB 就一定做单`
  - `触碰 IB 就必到 TP3`
  - `IB rejection` 单独构成入场信号

## 最小输入

- 交易方向：
  - `long / short`
- 主信号上下文：
  - `IB / DB / CB` 中至少一个主结构已成立
- 价格结构：
  - 回撤是否到达 `IB` 附近
- `Fib` 规划：
  - `TP1 / TP2 / TP3`
  - `SL`
- 可选辅助：
  - 回撤后的拒绝蜡烛
  - 小周期回撤结束迹象

## 最小输出

- `ib_retest_present`
  - 是否发生回撤到 `IB`
- `ib_rejection_present`
  - 是否出现“被阻挡/被拒绝”的迹象
- `tp3_extension_bias`
  - 当前是否可记为“更偏向延伸到 TP3”
- `tkr6_note`
  - 文字说明当前属于：
    - `no_retest`
    - `retest_without_rejection`
    - `retest_with_rejection`

## 当前建议的派生输出

- `ib_retest_depth_bucket`
  - 回撤深度分桶
- `rejection_candle_type`
  - 拒绝蜡烛类型
- `tp3_path_quality`
  - 到 `TP3` 的路径质量
- `rrr_after_retest`
  - 回撤后重新计算的风报比

## 与现有 TK 主线的关系

- 当前更稳的关系是：
  - `TK-R6` 不替代 `IB / DB / CB`
  - `TK-R6` 也不替代 `Fib TP3`
  - 它更像“主信号已成立后，对 TP3 延伸概率的对象化补充”
- 当前更适合放在：
  - 诊断标签层
  - 后续对象层
  - 解释层
- 当前不适合直接放在：
  - 单独 entry gate
  - 强制执行条件

## 最小验收定义

- 有一份对象语义文档：
  - 说明它不是独立信号，而是主信号后的结构补充
- 有一份最小输入/输出合同：
  - 至少把 `IB retest / rejection / TP3 extension bias` 说清
- 有一份 proof-of-mapping 的证据表（可审计）：
  - `12_工具运行时_TOOLING_RUNTIME\TK_R6\tkr6_manual_audit_sheet_v1.tsv`
- 有一份可复现的汇总产物（可审计）：
  - `12_工具运行时_TOOLING_RUNTIME\TK_R6\tkr6_manual_audit_summary_v1.md`
- 有一份当前角色裁决：
  - `DIAG_ONLY_OBJECT_CANDIDATE`
  - 或 `next_object_entry`

## 当前 gaps

- `IB 附近` 的距离定义仍未冻结。
- `被阻挡/被拒绝` 的判据仍未冻结。
- 当前还没有统一样本去检验：
  - `IB retest with rejection`
  - 相比 `no retest`
  - 对 `TP3` 到达率是否真的更强。
- 当前不应把教学口径直接等同于统计显著性。

## 样本判据草案 v1（先做可审计分桶）

### 0. 样本入口

- 只在“主信号已成立”的前提下记录 `TK-R6`：
  - 主结构：`IB / DB / CB` 至少一个已成立
  - 已有 `Fib TP1/TP2/TP3 + SL` 的规划

### 1. retest 发生判定（是否进入观察）

- `ib_retest_present = 1` 的最小前提：
  - 命中 `inside_ib`（不把单纯 `near_ib` 当作 retest）
  - 参考：
    - `TK-R6_IB附近_最小距离口径_v1.md`

### 2. retest 质量分桶（四态）

- `no_retest`
  - `far_from_ib`
- `retest_touch_only`
  - `inside_ib` 但未出现明确回收/拒绝结构
- `retest_reject_weak`
  - `inside_ib` + 有回收/拒绝倾向，但不稳定
- `retest_reject_clear`
  - `inside_ib` + `close_back_to_signal_side` + `visible_rejection_hint`

### 3. TP3 偏向输出（先不写成胜率结论）

- `tp3_extension_bias`
  - `none`：`no_retest` 或 `retest_touch_only`
  - `weak`：`retest_reject_weak`
  - `strong`：`retest_reject_clear`

### 4. 最小审计清单（用来复核一致性）

- 本次样本必须能回答：
  - 发生了没有：`ib_retest_present`
  - 属于哪一桶：`ib_retest_quality`
  - 拒绝痕迹是什么：`ib_rejection_candle_hint`
  - 最后标注：`tp3_extension_bias`

## 当前裁决

- `TK-R6` 是新综合整理稿里最值得继续推进的新增对象。
- 当前应把它固定为：
  - `TK` 后续对象层第一入口
  - `IB/DB/CB + TP3` 之间的结构补充对象
- 同时继续保持边界：
  - 不直接升级成策略
  - 不直接升级成硬门控
  - 不宣称已完成量化验证

## 下一步

- 若继续推进同一条线，优先顺序应为：
  - 先补 `TK-R6` 的样本判据草案
  - 再补 `IB retest / rejection` 的最小标签定义
  - 再决定是否值得开 `TK-R6` 的 proof-of-mapping 或诊断壳
- 当前已补第一份最小标签草案：
  - `TK-R6_IB_retest_rejection_最小标签定义_v1.md`
- 当前已补第二份最小条件草案：
  - `TK-R6_IB附近_最小距离口径_v1.md`
