# Batch150 对象卡 市场情绪总览

更新时间：2026-07-30

## 一、对象卡头部

```text
object_id                : B150_OBJ_000_MARKET_OVERVIEW
object_family            : batch_150
object_version           : v1
object_scope             : ashare_a5_second_round_sample
maturity_level           : object_card_minimal
card_status              : FROZEN_FOR_DATE_ANCHOR_BRIDGE
primary_view             : PAGE_OVERVIEW
owner_decision           : keep_as_date_anchor_and_overview_input
date_tag                 : 2026-07-29
```

## 二、对象定位

- 对象定位：
  - 把 `市场情绪总览` 页面收成第二轮新日期样本的总览锚点对象。
- 当前解决的问题：
  1. 确认新日期真实存在于来源链中
  2. 让后续对象卡和记录卡能回链到同一交易日
  3. 给 `沪深涨跌停 / 上榜资金 / 打板资金` 提供同日总览背景
- 当前不解决的问题：
  - 不直接替代五条代表指标对象
  - 不做买卖建议
  - 不做金融有效性判断

## 三、页面语义摘要

- 当前可直接读取的页面级语义：
  - 交易日总览
  - 盘面概览
  - 多区块同屏观察入口

- 这页真正价值不是“信息最多”，
  而是：
  - 作为新日期锚点
  - 作为同日页面组的总入口

## 四、最小来源状态

| 层级 | 代表字段 | 当前状态 | 说明 |
|---|---|---|---|
| `formalizable_now` | `date_tag` | `yes` | 已有同日总览截图吸收进 batch150 |
| `proxy` | `市场总览背景` | `yes` | 可为后续对象卡提供总览上下文 |
| `rules_engine_derivable` | `none` | `no` | 当前不从该页直接派生动作判断 |
| `future_only` | `情绪分段精细阈值` | `yes` | 当前无更细字段抽取链 |

## 五、当前来源锚点

- `00_raw_snapshot/user_screenshots/2026-07-29__市场情绪总览.png`
- `../README.md`
- `../provenance.md`

## 六、主负责人裁决

- 这张卡承担的是：
  - `第二轮新日期锚点`
  - `同日页面总览入口`

- 这张卡当前不承担：
  - A5 五条代表指标中的直接对象职责

## 七、一句话口径

- `市场情绪总览`
  在 batch150 中首先是日期锚点和总览页，
  先负责把第二轮新日期立住。
