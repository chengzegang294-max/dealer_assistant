# TK 第一批新增对象入口索引 v1

## 作用

- 用于把 `20231219TK外汇交易系统学习资料整理(6)` 带来的新增后续对象入口集中收口。
- 防止 `TK-R6 / TK-R8 / TK-R7` 分散在不同文件后再次失联。

## 当前来源锚点

- 总入口：
  - `20231219TK外汇交易系统学习资料整理(6)_吸收结论_v1.md`
- 当前这一批新增后续对象都来自：
  - `20231219TK外汇交易系统学习资料整理(6)_导出.md`

## 当前优先级

### 第一优先

- `TK-R6 = IB 回撤阻挡 -> TP3 概率增强`
- 入口文件：
  - `TK-R6_IB回撤阻挡到TP3_后续对象定义入口_v1.md`
- 最小标签草案：
  - `TK-R6_IB_retest_rejection_最小标签定义_v1.md`
- 最小距离口径：
  - `TK-R6_IB附近_最小距离口径_v1.md`
- proof-of-mapping 证据表（诊断壳入口）：
  - `12_工具运行时_TOOLING_RUNTIME\TK_R6\tkr6_manual_audit_sheet_v1.tsv`
- proof-of-mapping 汇总（可审计产物）：
  - `12_工具运行时_TOOLING_RUNTIME\TK_R6\tkr6_manual_audit_summary_v1.md`
- 当前继续补到：
  - `inside_ib` 的最小 candle 触达定义
  - `reject_clear` 的最少价格行为特征
  - `inside_ib -> touch_only / reject_weak / reject_clear` 的更细映射
- 当前角色：
  - `next_object_entry`
- 当前更像：
  - 主信号成立后的结构补充对象

### 第二优先

- `TK-R8 = B 区域 qualify 壳`
- 入口文件：
  - `TK-R8_B区域qualify壳_后续对象定义入口_v1.md`
- 最小判据草案：
  - `TK-R8_B区域_最小判据草案_v1.md`
- 结构失效条件：
  - `TK-R8_ABC结构失效_最小条件_v1.md`
- proof-of-mapping 证据表（诊断壳入口）：
  - `12_工具运行时_TOOLING_RUNTIME\TK_R8\tkr8_manual_audit_sheet_v1.tsv`
- proof-of-mapping 汇总（可审计产物）：
  - `12_工具运行时_TOOLING_RUNTIME\TK_R8\tkr8_manual_audit_summary_v1.md`
- 当前继续补到：
  - `structure_break` 的最小可见价格行为特征
  - `b_zone_miss` 的最小距离口径
  - `continuation_lost` 的最小可见环境特征
- 当前角色：
  - `qualify_shell_entry`
- 当前更像：
  - `ABC / B 位挂单` 的结构 qualify 壳

### 第三优先

- `TK-R7 = AO divergence 风险调整标签`
- 入口文件：
  - `TK-R7_AO背离风险调整标签_后续对象定义入口_v1.md`
- proof-of-mapping 证据表（诊断壳入口）：
  - `12_工具运行时_TOOLING_RUNTIME\TK_R7\tkr7_manual_audit_sheet_v1.tsv`
- proof-of-mapping 汇总（可审计产物）：
  - `12_工具运行时_TOOLING_RUNTIME\TK_R7\tkr7_manual_audit_summary_v1.md`
- 当前角色：
  - `risk_adjust_label_entry`
- 当前更像：
  - 主结构之后的风险修正标签

## 三者分工

- `TK-R6`
  - 看 `IB retest / rejection` 是否增强去 `TP3` 的延伸偏向
- `TK-R8`
  - 看某次回撤是否仍算有效 `B 区域`
- `TK-R7`
  - 看 `AO divergence` 是否提示风险上升或延伸衰竭

## 当前共同边界

- 三者都不是：
  - 当前硬门控
  - 当前独立策略
  - 当前已量化完成对象
- 三者当前都更适合：
  - diag-only
  - 后续对象层
  - 解释/结构补充层

## 当前推荐推进顺序

- 若继续沿 `TK` 主线推进：
  - 先补 `TK-R6` 的样本判据草案
  - 再补 `TK-R8` 的 `B 区域` 最小判据
  - 再补 `TK-R7` 的 `AO divergence` 最小判据

## 与 Batch1 的关系

- 当前 `TKFX_12` 不只是“综合整理扩展稿”。
- 它已经成为：
  - `TK Batch1` 的新增对象入口来源单元
  - 后续 `R6 / R8 / R7` 的总锚点
