# Batch149 对象卡 HYDB行业对比

更新时间：2026-07-20

## 一、对象卡头部

```text
object_id                : B149_OBJ_004_INDUSTRY_STRENGTH_CONTEXT
object_family            : batch_149
object_version           : v1
object_scope             : ashare_p0_home_event_flow
maturity_level           : object_card_minimal
card_status              : FROZEN_FOR_FIELD_BRIDGE
primary_view             : JOINT_VIEW
owner_decision           : keep_as_context_input
date_tag                 : 2026-07-20
```

## 二、对象定位

- 对象定位：
  - 把 `HYDB行业对比` 收成首页事件流可消费的 `行业强弱环境` 对象。
- 当前解决的问题：
  - 提醒层回答：
    - 当前事件所处行业背景是在增强还是走弱
  - 解释层回答：
    - 该事件更像个股独立异动，还是行业共振中的一环
- 当前不解决的问题：
  - 不做行业轮动预测
  - 不做多行业横截面排序中心
  - 不做全量板块引擎

## 三、公式语义摘要

- 当前可直接读取的核心语义：
  - `行业指数K线`
  - `行业涨幅`
- 这条公式的真正价值，不是叠加画在主图上的行业线，而是：
  - 给单个事件补“行业环境顺逆风”
  - 区分个股触发是孤立行为还是板块共振

## 四、最小来源状态

| 层级 | 代表字段 | 当前状态 | 说明 |
|---|---|---|---|
| `formalizable_now` | `行业涨幅 / 行业K线位置` | `yes` | 系统公式正文已回收 |
| `proxy` | `行业环境强 / 弱` | `yes` | 可由行业涨幅与走势方向代理 |
| `rules_engine_derivable` | `行业共振 / 个股独立异动` | `yes` | 可结合个股事件触发做解释判断 |
| `future_only` | `行业内成分股扩散度` | `yes` | 当前批次无更细分板块扩散数据 |

## 五、P0 映射

### 5.1 EventSummary

```text
eventId         : market-industry-context-<date>
title           : 所属行业强弱出现明显偏移
subject         : 相关行业
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
logic            : 行业指数走势与行业涨幅出现明显偏移，说明当前事件更可能处在行业顺风或逆风环境中
impact           : 用于解释事件为何更容易扩散、承接更强或持续性偏弱，不直接给板块轮动建议
historyAnalogy   : 可选；与近期同类行业活跃/退潮阶段做轻类比
nextReviewPoint  : 复查行业涨幅、行业趋势方向与事件所在个股是否继续同向
```

## 六、提醒 / 解释 / 记录 / 回看

- 提醒层：
  - `行业顺风`
  - `行业逆风`
  - `行业共振增强`
- 解释层：
  - 解释事件是否具备行业背景支撑
- 记录层：
  - 只记录压缩语义：
    - `行业强`
    - `行业弱`
    - `行业共振`
- 回看层：
  - 回看行业顺逆风过滤是否降低误判

## 七、禁止照搬项

- 禁止把行业K线叠加样式直接搬进产品。
- 禁止把行业强弱直接写成行业配置建议。
- 禁止在 P0 阶段扩成板块轮动总览页。

## 八、主负责人裁决

- 这张卡适合进入：
  - `ExplanationPayload.logic`
  - `EventSummary.subject` 的行业语境补充
- 这张卡当前不应进入：
  - `首页主轴`
  - `行业研究页`
