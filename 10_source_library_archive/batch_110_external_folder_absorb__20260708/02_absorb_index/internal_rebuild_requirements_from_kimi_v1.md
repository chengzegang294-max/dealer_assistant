# Internal Rebuild Requirements From Kimi v1

更新时间：2026-07-08

## 目的

- 把 Kimi 整理的全库材料，压成“我们真正要实现的内容与技术指标清单”，用于后续：
  - 内部资料重分类
  - 对象卡与运行时验收落地
  - 再去做多 AI 讨论（只问“补缺口与字段”，不泛聊博主）

## 输入锚点（只认这几份作为主证据入口）

- `00_raw_snapshot/MASTER_INDEX_v1.0.md`
- `00_raw_snapshot/USER_IDEAS_INTEGRATION_v1.0.md`
- `00_raw_snapshot/TRADING_SYSTEM_BLUEPRINT_v1.0.md`
- `00_raw_snapshot/MING_CABINET_HYBRID_ARCHITECTURE_v1.0.md`
- `00_raw_snapshot/MASTER_PROGRAMMING_INSTRUCTION_v1.0.md`

## 现有资产清单（我们已经“有”的）

- 12 张对象卡（概念层/字段层已经写过，部分还有 `.py` 原型）：
  - `CHZL_BSD` `BPB` `TKR7` `VP` `YTC`
  - `MFLOW` `INSTB`
  - `VOLFAC` `VOLTARGET` `KELLY`
  - `PERIOD_QUEEN` `ATRATIO`（A股纯多头语境下可跳过或降级）
- 治理框架（“明柜混合架构”）：常态/牛市/熊市/震荡/危机的制度切换与审查机制。
- 回测诚实性诉求：CSCV/PBO 或等价稳健性门槛，以及未来信息泄露防线。

## 终局目标（从“纯 A 股回测”扩为“私人投资管家”）

- 多市场：A股 / 外汇 / 币圈主流币 / 期货。
- 三权分立讨论：基本面/宏观 + 技术/对象卡 + 仓管/风控 → 内阁裁决。
- 必须能覆盖：
  - 持仓诊断（组合层）
  - 关注池（watchlist/universe）
  - 每日自动化日报（可复现输出）

## 技术指标与工程要求（必须落为验收）

### 1) 数据层（允许付费，但要高性价比）

- 日线 OHLCV：全市场覆盖（A股为主；跨市场按需扩展）
- 周线：从日线合成，用于上下文注入
- 分钟级（优先 60min，其次 15min/5min）：按需加载，只对关注池保留
- 资金流向：`MFLOW` 依赖（可能需要付费数据；必须给降级路径）
- 数据质量与版本：
  - 数据可用性审计（是否可得/成本/频率/缺失策略）
  - 版本化（hash/参数/数据窗口）确保可复现

### 2) 对象卡标准输出接口（硬规则）

- 对象卡必须统一输出：`object_id/function_bucket/process_layer/timeframe/signal_type/signal_strength/signal_confidence/filter_action/risk_action/size_scalar/...`
- 验收必须包含：
  - 字段完整性
  - 不泄露未来信息
  - 数据缺失时的降级行为

### 3) 回测诚实性与不过拟合（硬规则）

- 任何纳入硬门控的规则/阈值：
  - 必须有样本外/稳健性验证（CSCV/PBO 或等价）
  - 必须写出失效模式与降级策略

### 4) 自动化日报（第一类交付）

- 日报必须固定结构输出（Markdown）：
  - 市场状态（PeriodQueen + 宏观评分）
  - 持仓诊断（风险预算/集中度/回撤梯子触发）
  - 关注池排行（对象卡投票与置信度）
  - 分歧点与下一轮实验清单（可追溯）

## 当前缺口清单（我们要补的，不靠“找博主”解决）

- `Macro 5维评分`：利率/汇率/流动性/风险偏好/政策的字段化与数据源选型
- `组合层仓管`：集中度/相关性/风险预算/回撤梯子与触发后动作
- `对象卡统一调度与联动`：registry + pipeline + 互锁规则固定化
- `偏差分析`：AI判断 vs 实际走势的可复现统计
- `跨市场适配`：哪些模块统一，哪些模块分叉，分叉后的数据与验收怎么写

## 下一步（内部重做优先级）

1. 先把 `00_raw_snapshot/` 文档按模块重分类（只做索引与路由，不改原文）。
2. 把 12 对象卡的“我们自己的版本”建立为对象包（责任卡/快入口/验收样本），Kimi 版本只作为来源证据。
3. 再启动多 AI 讨论：只允许围绕“补缺口与字段化落地”，产出必须 TSV 可吸收。
