# Batch150 对象卡 上榜资金

更新时间：2026-07-30

## 一、对象卡头部

```text
object_id                : B150_OBJ_003_TOP_LIST_CAPITAL
object_family            : batch_150
object_version           : v1
object_scope             : ashare_a5_second_round_sample
maturity_level           : object_card_minimal
card_status              : FROZEN_FOR_SECOND_ROUND_BRIDGE
primary_view             : PAGE_SCREENSHOT
owner_decision           : keep_as_trigger_or_explanation_input
date_tag                 : 2026-07-29
```

## 二、对象定位

- 对象定位：
  - 把 `龙虎榜异动资金` 页面收成第二轮样本里的 `上榜资金` 对象。
- 当前解决的问题：
  1. 给 `上榜资金` 提供新日期的真实页面锚点
  2. 让第二轮能够重新判断：
     - 这一天榜单资金是增强、退潮还是仅剩解释价值
- 当前不解决的问题：
  - 不做席位级拆分
  - 不把榜单异动直接写成交易结论

## 三、页面语义摘要

- 当前页面可直接承载的核心语义：
  - 龙虎榜/上榜异动
  - 异动原因
  - 资金背书强弱的页面级提示

- 这页真正价值是：
  - 把第一轮 `上榜资金`
    在第二轮新日期上重新挂到可回链的页面证据

## 四、最小来源状态

| 层级 | 代表字段 | 当前状态 | 说明 |
|---|---|---|---|
| `formalizable_now` | `龙虎榜异动资金` | `yes` | 已有同日页面截图吸收进 batch150 |
| `proxy` | `资金背书增强 / 撤离` | `yes` | 可作为榜单资金强弱代理 |
| `rules_engine_derivable` | `触发保留 / 降级职责` | `yes` | 可为第二轮动作判断提供对象输入 |
| `future_only` | `席位细分 / 明细净额` | `yes` | 当前截图未细到更深字段层 |

## 五、当前来源锚点

- `00_raw_snapshot/user_screenshots/2026-07-29__龙虎榜异动资金.png`
- `../README.md`
- `../provenance.md`

## 六、主负责人裁决

- 这张卡适合直接进入：
  - 第二轮 `trigger_objects`
  - `上榜资金` 同日来源回链

- 这张卡当前不应直接进入：
  - 席位细分
  - 龙虎榜深度拆解

## 七、一句话口径

- batch150 已经把 `龙虎榜异动资金`
  正式桥接回第二轮的 `上榜资金` 对象。
