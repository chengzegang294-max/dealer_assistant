# Batch 141 Trend Rotation Positioning Absorb

更新时间：2026-07-12

## 批次目标

- 把仓库里已经出现但尚未收口成正式资料链的“趋势仓位 / 轮动仓位”想法整理成一个可追溯吸收批。
- 同时完成三层收口：
  - `01_index/family_entry_map_v1.tsv`：给出 first-hop 入口
  - `02_absorb_index/trend_rotation_positioning_digest_v1.md`：提炼现有资料中的可保留思想
  - `02_absorb_index/ashare_p0_positioning_bridge_decision_v1.md`：给出当前 A 股 P0 可采用与不可采用的裁决

## 收口裁决

- 当前这批不是外部原件导入批，而是：
  - 基于仓库内已存在材料的综合吸收批
  - 面向 `A股 P0` 的桥接裁决批
- 当前主负责人裁决：
  - `趋势仓位` 只先保留为 `regime -> 仓位上限` 的解释与桥接口径
  - `轮动仓位` 只先保留为 `行业集中 / 分散 + 行业暴露上限建议` 的解释与桥接口径
  - `四轴状态` 与 `VanTharp R` 暂不直接升级为 P0 默认仓位引擎

## 批次结构

- `01_index/`
  - 本批入口图
- `02_absorb_index/`
  - 趋势仓位与轮动仓位内化摘要
  - A股 P0 仓位桥接裁决

## 当前入口

- `README.md`
- `manifest_v1.tsv`
- `provenance.md`
- `01_index/family_entry_map_v1.tsv`
- `02_absorb_index/trend_rotation_positioning_digest_v1.md`
- `02_absorb_index/ashare_p0_positioning_bridge_decision_v1.md`

## 默认阅读顺序

- 先看当前 README，确认这批是“仓库内综合吸收批”，不是原始教程或 raw snapshot 回收批。
- 再看 `01_index/family_entry_map_v1.tsv`，决定是：
  - 看综合摘要
  - 看项目桥接裁决
  - 还是回到上游对象与原始资料
- 若目标是当前项目怎么使用“趋势仓位 / 轮动仓位”，优先看 `ashare_p0_positioning_bridge_decision_v1.md`。
