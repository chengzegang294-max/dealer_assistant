# Batch149 对象卡 沪深涨跌停

更新时间：2026-07-20

## 一、对象卡头部

```text
object_id                : B149_OBJ_001_LIMIT_BOARD_BREADTH
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
  - 把 `沪深涨跌停` 这条系统公式，收成首页事件流可消费的 `热点热度 / 风险偏好` 宽度对象。
- 当前解决的问题：
  - 提醒层回答：
    - 今天市场情绪是在升温、退潮还是分化
  - 解释层回答：
    - 为什么今天事件流会偏热或偏冷
- 当前不解决的问题：
  - 不做个股买点
  - 不做板块轮动细节
  - 不做连板龙头挑选器

## 三、公式语义摘要

- 当前可直接读取的核心语义：
  - `涨停家数`
  - `连板家数`
  - `跌停家数`
- 这条公式的真正价值不是画副图本身，而是给出：
  - 全市场风险偏好宽度
  - 热点持续性强弱
  - 情绪分化是否加剧

## 四、最小来源状态

| 层级 | 代表字段 | 当前状态 | 说明 |
|---|---|---|---|
| `formalizable_now` | `涨停家数 / 连板家数 / 跌停家数` | `yes` | 已有系统公式正文，可稳定理解 |
| `proxy` | `热点热度升降` | `yes` | 由三项宽度共同代理，不要求单一阈值 |
| `rules_engine_derivable` | `热度升温 / 降温 / 分化` | `yes` | 可由宽度变化方向和相对强弱派生 |
| `future_only` | `题材级连板结构细分` | `yes` | 当前批次无题材细分公式链 |

## 五、P0 映射

### 5.1 EventSummary

```text
eventId         : market-limit-board-<date>
title           : 涨停/连板热度出现异常变化
subject         : 全市场
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
logic            : 当日涨停家数、连板家数、跌停家数出现突变，市场风险偏好与热点热度发生变化
impact           : 解释今日事件流为何偏热、偏冷或分化，不直接给个股买卖建议
historyAnalogy   : 可选；仅做情绪阶段轻类比
nextReviewPoint  : 收盘前复查涨停家数、连板高度、跌停扩散是否继续同向
```

## 六、提醒 / 解释 / 记录 / 回看

- 提醒层：
  - `热度升温`
  - `热度降温`
  - `分化加剧`
- 解释层：
  - 用于解释当前市场环境
- 记录层：
  - 只记录压缩语义：
    - `热点热度升`
    - `热点热度降`
    - `风险偏好收缩`
- 回看层：
  - 回看情绪宽度变化是否对事件后续有解释力

## 七、禁止照搬项

- 禁止把原始三项数值整段塞入首页卡片。
- 禁止把副图样式直接搬进产品。
- 禁止把这条公式写成“涨停就该追”的建议器。

## 八、主负责人裁决

- 这张卡适合直接进入：
  - `首页事件流`
  - `解释卡环境摘要`
- 这张卡当前不应进入：
  - `个股动作建议`
  - `记录草稿默认动作`
