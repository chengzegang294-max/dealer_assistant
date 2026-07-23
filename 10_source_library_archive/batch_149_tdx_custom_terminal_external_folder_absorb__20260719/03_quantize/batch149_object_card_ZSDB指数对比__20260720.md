# Batch149 对象卡 ZSDB指数对比

更新时间：2026-07-20

## 一、对象卡头部

```text
object_id                : B149_OBJ_005_INDEX_STRENGTH_CONTEXT
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
  - 把 `ZSDB指数对比` 收成首页事件流可消费的 `指数环境强弱` 对象。
- 当前解决的问题：
  - 提醒层回答：
    - 当前大盘环境是在配合事件还是压制事件
  - 解释层回答：
    - 这条事件更像环境驱动还是逆势异动
- 当前不解决的问题：
  - 不做指数择时系统
  - 不做全市场仓位模型
  - 不做多指数复杂切换面板

## 三、公式语义摘要

- 当前可直接读取的核心语义：
  - `指数K线`
  - `指数涨幅`
- 这条公式的真正价值，是把大盘环境压缩成：
  - `顺风`
  - `中性`
  - `逆风`
  三档解释背景。

## 四、最小来源状态

| 层级 | 代表字段 | 当前状态 | 说明 |
|---|---|---|---|
| `formalizable_now` | `指数涨幅 / 指数K线位置` | `yes` | 系统公式正文已回收 |
| `proxy` | `指数环境强 / 弱` | `yes` | 可由涨幅与走势方向代理 |
| `rules_engine_derivable` | `环境顺风 / 中性 / 逆风` | `yes` | 可直接下沉到解释层 |
| `future_only` | `多指数相对强弱细分` | `yes` | 当前批次不做复杂指数面板 |

## 五、P0 映射

### 5.1 EventSummary

```text
eventId         : market-index-context-<date>
title           : 指数环境强弱发生变化
subject         : 全市场指数环境
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
logic            : 指数涨幅与指数走势方向发生明显变化，说明当前事件所处的大盘环境正在顺风、转弱或逆风
impact           : 用于解释事件为何更容易扩散、承接不足或逆势独立，不直接给择时建议
historyAnalogy   : 可选；与近期市场风险偏好阶段做轻类比
nextReviewPoint  : 复查指数涨幅、指数方向与事件热度是否继续同向
```

## 六、提醒 / 解释 / 记录 / 回看

- 提醒层：
  - `指数顺风`
  - `指数逆风`
  - `环境转弱`
- 解释层：
  - 解释事件处于什么大盘环境
- 记录层：
  - 只记录压缩语义：
    - `环境顺风`
    - `环境中性`
    - `环境逆风`
- 回看层：
  - 回看指数环境过滤是否提升事件解释质量

## 七、禁止照搬项

- 禁止把指数主图叠加样式直接放进产品。
- 禁止把环境信号写成确定性仓位建议。
- 禁止在当前 P0 阶段扩成指数监控中台。

## 八、主负责人裁决

- 这张卡适合进入：
  - `ExplanationPayload.impact`
  - `首页事件流` 的环境背景
- 这张卡当前不应进入：
  - `首页主轴替代`
  - `仓位控制器`
