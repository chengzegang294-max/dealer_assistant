# Batch149 对象卡 上榜资金

更新时间：2026-07-20

## 一、对象卡头部

```text
object_id                : B149_OBJ_003_TOP_LIST_CAPITAL
object_family            : batch_149
object_version           : v1
object_scope             : ashare_p0_home_event_flow
maturity_level           : object_card_minimal
card_status              : FROZEN_FOR_FIELD_BRIDGE
primary_view             : JOINT_VIEW
owner_decision           : keep_as_explanation_enhancer
date_tag                 : 2026-07-20
```

## 二、对象定位

- 对象定位：
  - 把 `上榜资金` 这条系统公式，收成首页解释增强层可消费的 `榜单资金异动` 对象。
- 当前解决的问题：
  - 提醒层回答：
    - 今天是否出现明显榜单资金异动
  - 解释层回答：
    - 事件背后是否存在主动资金背书
- 当前不解决的问题：
  - 不替代龙虎榜明细页
  - 不做席位级拆分
  - 不直接给“跟榜”建议

## 三、公式语义摘要

- 当前可直接读取的核心语义：
  - `资金净额柱`
- 这条公式的真正价值，不是柱体样式，而是：
  - 判断榜单资金净流入/净流出是否异常
  - 给事件解释增加“是否有资金背书”的证据

## 四、最小来源状态

| 层级 | 代表字段 | 当前状态 | 说明 |
|---|---|---|---|
| `formalizable_now` | `榜单资金净额` | `yes` | 系统公式正文已回收 |
| `proxy` | `榜单资金异动强弱` | `yes` | 由净额方向与幅度代理 |
| `rules_engine_derivable` | `主动资金背书 / 资金撤离` | `yes` | 可由净额方向与变化幅度派生 |
| `future_only` | `席位细分、上榜原因细分` | `yes` | 当前批次未吸到榜单明细层 |

## 五、P0 映射

### 5.1 EventSummary

```text
eventId         : market-top-list-capital-<date>
title           : 榜单资金出现异动
subject         : 全市场榜单资金
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
logic            : 榜单资金净额明显变化，说明有主动资金集中出现或撤离
impact           : 用于解释事件背后是否存在资金背书，而不只是价格波动
historyAnalogy   : 可选；与近期榜单活跃阶段做轻类比
nextReviewPoint  : 次日复查榜单净额是否延续，同题材是否同步扩散
```

## 六、提醒 / 解释 / 记录 / 回看

- 提醒层：
  - `榜单净流入增强`
  - `榜单净流出扩大`
- 解释层：
  - 解释某类事件是被主动资金推动还是缺乏资金背书
- 记录层：
  - 只记录压缩语义：
    - `资金背书强`
    - `资金背书弱`
    - `资金撤离`
- 回看层：
  - 回看榜单资金异动对后续事件演化的解释力

## 七、禁止照搬项

- 禁止把榜单资金异动直接写成可买卖结论。
- 禁止把净额柱的视觉样式搬进产品。
- 禁止在当前 P0 阶段扩成龙虎榜深度分析中心。

## 八、主负责人裁决

- 这张卡适合进入：
  - `ExplanationPayload.impact` 的资金背书段
  - `首页事件流` 的解释增强项
- 这张卡当前不应进入：
  - `首页主轴`
  - `个股页席位拆分`
