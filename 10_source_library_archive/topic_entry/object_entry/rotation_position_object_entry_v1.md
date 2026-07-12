# 轮动仓位对象入口 v1

## 适用问题

- 想直接看当前 `A股 P0` 可采用的轮动仓位桥接口径
- 想确认 `行业集中 / 分散 + 行业暴露上限` 当前怎么用
- 想区分它与行业轮动研究摘要、正式组合优化器的边界

## first-hop 入口

- `../../batch_141_trend_rotation_positioning_absorb__20260712/02_absorb_index/ashare_p0_positioning_bridge_decision_v1.md`

## 默认阅读顺序

- 先看项目裁决：
  - `../../batch_141_trend_rotation_positioning_absorb__20260712/02_absorb_index/ashare_p0_positioning_bridge_decision_v1.md`
- 再看综合摘要：
  - `../../batch_141_trend_rotation_positioning_absorb__20260712/02_absorb_index/trend_rotation_positioning_digest_v1.md`
- 再回看上游研究对象：
  - `industry_rotation_signal_object_entry_v1.md`

## 当前结论速记

- 当前只接受：
  - `行业集中 -> 单行业上限 20%`
  - `行业分散 -> 至少 3 个行业`
- 当前不代表：
  - 已形成正式行业轮动配置引擎
  - 已接入主线默认组合优化

## 回链

- 上层主题入口：
  - `../trend_rotation_positioning_topic_entry_v1.md`
