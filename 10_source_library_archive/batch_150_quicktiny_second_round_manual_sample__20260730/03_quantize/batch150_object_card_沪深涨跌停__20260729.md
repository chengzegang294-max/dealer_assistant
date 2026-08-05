# Batch150 对象卡 沪深涨跌停

更新时间：2026-07-30

## 一、对象卡头部

```text
object_id                : B150_OBJ_001_LIMIT_BOARD_BREADTH
object_family            : batch_150
object_version           : v1
object_scope             : ashare_a5_second_round_sample
maturity_level           : object_card_minimal
card_status              : FROZEN_FOR_SECOND_ROUND_BRIDGE
primary_view             : PAGE_SCREENSHOT
owner_decision           : keep_as_background_width_input
date_tag                 : 2026-07-29
```

## 二、对象定位

- 对象定位：
  - 把 `市场宽度涨停跌停` 页面收成第二轮样本里的 `沪深涨跌停` 背景对象。
- 当前解决的问题：
  1. 回答市场宽度/涨停跌停环境是否可被当作同日背景
  2. 给第二轮记录卡提供 `沪深涨跌停` 的同日来源锚点
- 当前不解决的问题：
  - 不做题材级连板结构细分
  - 不直接给个股动作建议

## 三、页面语义摘要

- 当前页面可直接承载的核心语义：
  - 市场宽度
  - 涨停/跌停分布
  - 热度与风险偏好的总体变化

- 这页真正价值是：
  - 把第一轮里的 `沪深涨跌停`
    在第二轮新日期上重新挂到真实页面证据

## 四、最小来源状态

| 层级 | 代表字段 | 当前状态 | 说明 |
|---|---|---|---|
| `formalizable_now` | `市场宽度 / 涨停跌停` | `yes` | 已有同日页面截图吸收进 batch150 |
| `proxy` | `热度升温 / 降温 / 分化` | `yes` | 可作为宽度代理语义 |
| `rules_engine_derivable` | `背景增强 / 背景转弱` | `yes` | 可进入第二轮背景层判断 |
| `future_only` | `更细题材级连板结构` | `yes` | 当前截图未细到题材分层 |

## 五、当前来源锚点

- `00_raw_snapshot/user_screenshots/2026-07-29__市场宽度涨停跌停.png`
- `../README.md`
- `../provenance.md`

## 六、主负责人裁决

- 这张卡适合直接进入：
  - 第二轮 `background_objects`
  - `沪深涨跌停` 同日来源回链

- 这张卡当前不应直接进入：
  - 金融有效性
  - 个股动作建议

## 七、一句话口径

- batch150 已经把 `市场宽度涨停跌停`
  正式桥接回第二轮的 `沪深涨跌停` 背景对象。
