# Batch149 对象卡 启动点

更新时间：2026-07-20

## 一、对象卡头部

```text
object_id                : B149_OBJ_006_STOCK_TRIGGER_POINT
object_family            : batch_149
object_version           : v1
object_scope             : ashare_p0_home_event_flow
maturity_level           : object_card_minimal
card_status              : FROZEN_FOR_FIELD_BRIDGE
primary_view             : JOINT_VIEW
owner_decision           : keep_as_action_candidate_input
date_tag                 : 2026-07-20
```

## 二、对象定位

- 对象定位：
  - 把 `启动点` 收成首页事件流可消费的 `个股动作触发` 对象。
- 当前解决的问题：
  - 提醒层回答：
    - 个股是否出现值得关注的启动/转强信号
  - 解释层回答：
    - 当前事件更偏向观察、跟踪还是已出现转强迹象
- 当前不解决的问题：
  - 不直接给买入指令
  - 不替代完整选股器
  - 不做自动化交易信号

## 三、公式语义摘要

- 当前可直接读取的核心语义：
  - `启动买点`
  - `MACD启动信号`
- 这条公式的真正价值，是把复杂个股图形判断压成：
  - `启动候选`
  - `继续观察`
  - `尚未成立`
  三档动作语义。

## 四、最小来源状态

| 层级 | 代表字段 | 当前状态 | 说明 |
|---|---|---|---|
| `formalizable_now` | `启动买点 / MACD启动信号` | `yes` | 用户公式正文已回收 |
| `proxy` | `个股转强候选` | `yes` | 可由启动信号代理 |
| `rules_engine_derivable` | `观察 / 转强 / 暂缓` | `yes` | 可直接下沉到记录层动作语义 |
| `future_only` | `多信号叠加确认` | `yes` | 当前批次不做多公式综合裁决器 |

## 五、P0 映射

### 5.1 EventSummary

```text
eventId         : stock-trigger-point-<date>-<symbol>
title           : 个股出现启动候选信号
subject         : 相关个股
occurredAt      : 当次触发时间
holdingRelation : 关注相关
processStatus   : pending
disclosureFlag  : still_need_evidence
```

### 5.2 ExplanationPayload

```text
eventId          : 同 EventSummary.eventId
title            : 同 EventSummary.title
subject          : 同 EventSummary.subject
logic            : 个股出现启动买点或 MACD 启动信号，说明走势有转强候选，但仍需结合环境与事件背景复核
impact           : 用于解释为什么当前事件值得跟踪、观察或准备进入记录，而不直接下结论买入
historyAnalogy   : 可选；与近期同类启动后是否延续做轻类比
nextReviewPoint  : 复查后续量价延续、环境是否顺风、信号是否失效
```

## 六、提醒 / 解释 / 记录 / 回看

- 提醒层：
  - `启动候选`
  - `转强观察`
  - `信号待确认`
- 解释层：
  - 解释为什么当前个股值得继续观察
- 记录层：
  - 只记录压缩语义：
    - `继续观察`
    - `可跟踪`
    - `暂缓动作`
- 回看层：
  - 回看启动候选在不同环境下的有效性

## 七、禁止照搬项

- 禁止把“启动点”直接写成买入建议。
- 禁止把 MACD 细节参数整段堆到解释卡。
- 禁止在当前 P0 阶段扩成自动选股器。

## 八、主负责人裁决

- 这张卡适合进入：
  - `个股事件解释层`
  - `记录动作候选输入`
- 这张卡当前不应进入：
  - `自动交易`
  - `首页默认动作结论`
