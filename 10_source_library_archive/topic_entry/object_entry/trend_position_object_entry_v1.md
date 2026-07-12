# 趋势仓位对象入口 v1

## 适用问题

- 想直接看当前 `A股 P0` 可采用的趋势仓位桥接口径
- 想确认 `regime -> 仓位上限` 当前怎么用
- 想区分它与四轴状态、VanTharp R 的关系

## first-hop 入口

- `../../batch_141_trend_rotation_positioning_absorb__20260712/02_absorb_index/ashare_p0_positioning_bridge_decision_v1.md`

## 默认阅读顺序

- 先看项目裁决：
  - `../../batch_141_trend_rotation_positioning_absorb__20260712/02_absorb_index/ashare_p0_positioning_bridge_decision_v1.md`
- 再看综合摘要：
  - `../../batch_141_trend_rotation_positioning_absorb__20260712/02_absorb_index/trend_rotation_positioning_digest_v1.md`
- 再回看上游对象：
  - `four_axis_state_object_entry_v1.md`
  - `vantharp_r_object_entry_v1.md`

## 当前结论速记

- 当前只接受 `regime -> position_cap` 桥接口径
- 当前不代表：
  - 四轴状态已变成默认仓位引擎
  - VanTharp R 已变成 P0 默认风控引擎

## 回链

- 上层主题入口：
  - `../trend_rotation_positioning_topic_entry_v1.md`
