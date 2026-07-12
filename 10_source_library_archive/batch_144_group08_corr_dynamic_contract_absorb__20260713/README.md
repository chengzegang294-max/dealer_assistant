# Batch 144 Group08 Corr Dynamic Contract Absorb

更新时间：2026-07-13

## 批次目标

- 把 `GROUP_08` 中最贴近当前主线的两条研究线：
  - `多因子相关性选股`
  - `动态因子有效性`
  收成一批正式可引用的最小合同资产。
- 当前批次不复制原始 PDF，本批只做：
  - 合同层吸收
  - 字段字典冻结
  - 项目边界裁决

## 当前产物

- `01_index/family_entry_map_v1.tsv`
- `02_absorb_index/group08_corr_dynamic_contract_digest_v1.md`
- `02_absorb_index/group08_corr_dynamic_contract_decision_v1.md`
- `bundle/contracts/group08_correlation_stock_selection_p0_min_contract_v1.md`
- `bundle/contracts/group08_dynamic_factor_validity_p0_min_contract_v1.md`
- `bundle/fields/group08_correlation_stock_selection_field_dictionary_v1.tsv`
- `bundle/fields/group08_dynamic_factor_validity_field_dictionary_v1.tsv`

## 主负责人裁决

- 当前 `多因子相关性选股` 只先冻结：
  - `S-028 ~ S-033` 收成的 `S-C04` 全市场相关性选股框架
- 当前 `动态因子有效性` 只先冻结：
  - `S-039` Kalman Filter 动态因子选择
  - `S-040` 因子有效性强弱指数
  - `S-041` 净换手率作为候选扩展输入
- 当前明确不直接升级为：
  - A股 P0 默认多因子选股引擎
  - 默认因子评估器
  - 完整论文级实现

## 默认阅读顺序

- 先看 `01_index/family_entry_map_v1.tsv`
- 再看 `02_absorb_index/group08_corr_dynamic_contract_decision_v1.md`
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
