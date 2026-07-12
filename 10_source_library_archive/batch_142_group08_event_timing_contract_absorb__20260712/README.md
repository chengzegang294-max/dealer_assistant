# Batch 142 Group08 Event Timing Contract Absorb

更新时间：2026-07-12

## 批次目标

- 把 `GROUP_08` 中最贴近当前主线的两条研究线：
  - `事件驱动`
  - `市场择时`
  收成一批正式可引用的最小合同资产。
- 当前批次不复制原始 PDF，本批只做：
  - 合同层吸收
  - 字段字典冻结
  - 项目边界裁决

## 当前产物

- `01_index/family_entry_map_v1.tsv`
- `02_absorb_index/group08_event_timing_contract_digest_v1.md`
- `02_absorb_index/group08_event_timing_contract_decision_v1.md`
- `bundle/contracts/group08_event_driven_p0_min_contract_v1.md`
- `bundle/contracts/group08_market_timing_p0_min_contract_v1.md`
- `bundle/fields/group08_event_driven_field_dictionary_v1.tsv`
- `bundle/fields/group08_market_timing_field_dictionary_v1.tsv`

## 主负责人裁决

- 当前 `事件驱动` 只先冻结：
  - 业绩预告
  - 指数样本股调整
  - 大股东增持
  - 股权激励
  这四类事件的最小合同与字段字典
- 当前 `市场择时` 只先冻结：
  - 市场一致性 `R²`
  - 产业资本增减持
  这两类信号的最小合同与字段字典
- 当前明确不直接升级为：
  - A股 P0 默认执行门控
  - 真实交易信号引擎
  - 完整论文级实现

## 默认阅读顺序

- 先看 `01_index/family_entry_map_v1.tsv`
- 再看 `02_absorb_index/group08_event_timing_contract_decision_v1.md`
- 再按主题进入对应合同和字段字典

## 当前边界

- 当前批次属于 `contract_absorb_batch`
- 当前只冻结：
  - 最小输入字段
  - 最小输出字段
  - 参数边界
  - 不接线说明
- 当前不提供：
  - 完整回测
  - 正式 runtime 脚本
  - 默认参数最优解
