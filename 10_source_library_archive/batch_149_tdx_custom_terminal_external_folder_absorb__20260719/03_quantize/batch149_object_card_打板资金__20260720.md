# Batch149 对象卡 打板资金

更新时间：2026-07-20

## 一、对象卡头部

```text
object_id                : B149_OBJ_002_BOARD_CAPITAL
object_family            : batch_149
object_version           : v1
object_scope             : ashare_p0_home_event_flow
maturity_level           : object_card_minimal
card_status              : FROZEN_FOR_FIELD_BRIDGE
primary_view             : JOINT_VIEW
owner_decision           : keep_as_event_summary_input
date_tag                 : 2026-07-20
```

## 二、对象定位

- 对象定位：
  - 把 `打板资金` 这条系统公式，收成首页事件流可消费的 `封板质量 / 热点承接` 对象。
- 当前解决的问题：
  - 提醒层回答：
    - 今天打板资金是在加强还是减弱
  - 解释层回答：
    - 热点延续背后是有承接还是只是表面涨停
- 当前不解决的问题：
  - 不直接输出个股打板策略
  - 不决定是否追高
  - 不替代人工题材理解

## 三、公式语义摘要

- 当前可直接读取的核心语义：
  - `封板成功资金`
  - `封单额`
  - `封板失败资金`
- 这条公式的真正价值，是把：
  - 板上承接
  - 封板质量
  - 炸板压力
  压成一个可解释的热点热度信号。

## 四、最小来源状态

| 层级 | 代表字段 | 当前状态 | 说明 |
|---|---|---|---|
| `formalizable_now` | `封板成功资金 / 封单额 / 封板失败资金` | `yes` | 系统公式正文已回收 |
| `proxy` | `封板质量强弱` | `yes` | 由三项相对强弱代理 |
| `rules_engine_derivable` | `承接增强 / 炸板增多` | `yes` | 可由成功与失败资金对比派生 |
| `future_only` | `细分到题材板块的封板结构` | `yes` | 当前批次没有细分题材链 |

## 五、P0 映射

### 5.1 EventSummary

```text
eventId         : market-board-capital-<date>
title           : 封板资金强弱发生变化
subject         : 全市场打板
occurredAt      : 当次触发时间
holdingRelation : 其它
processStatus   : pending
disclosureFlag  : still_need_evidence
```

### 5.2 ExplanationPayload

```text
eventId          : 同 EventSummary.eventId
title            : 同 EventSummary.title
subject          : 同 EventSummary.subject
logic            : 封板成功资金、封单额与封板失败资金的相对变化，反映热点承接和封板质量变化
impact           : 解释为什么热点强化、炸板增多或题材承接减弱，不直接给交易动作建议
historyAnalogy   : 可选；仅做活跃题材阶段轻类比
nextReviewPoint  : 复查封板成功资金是否继续放大、封板失败资金是否同步恶化
```

## 六、提醒 / 解释 / 记录 / 回看

- 提醒层：
  - `封板承接增强`
  - `封板承接减弱`
  - `炸板压力抬升`
- 解释层：
  - 解释热点持续性是否具备资金支撑
- 记录层：
  - 只记录压缩语义：
    - `封板质量强`
    - `封板质量弱`
    - `炸板风险升`
- 回看层：
  - 回看资金承接信号是否能过滤假热点

## 七、禁止照搬项

- 禁止把公式里的全部资金变量原样堆到解释卡。
- 禁止把打板信号写成确定性“可打/不可打”。
- 禁止把这张卡抬成首页唯一主角，它只是一条解释增强输入。

## 八、主负责人裁决

- 这张卡适合进入：
  - `首页事件流`
  - `热点解释卡`
- 这张卡当前不应进入：
  - `个股决策草稿默认动作`
  - `问答页里的确定性建议`
