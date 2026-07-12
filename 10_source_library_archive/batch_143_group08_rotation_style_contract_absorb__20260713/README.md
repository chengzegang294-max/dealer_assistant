# Batch 143 Group08 Rotation Style Contract Absorb

更新时间：2026-07-13

## 批次目标

- 把 `GROUP_08` 中最贴近当前主线的 `行业轮动 / 风格轮动` 研究线收成一批正式可引用的最小合同资产。
- 当前批次不复制原始 PDF，本批只做：
  - 合同层吸收
  - 字段字典冻结
  - 项目边界裁决

## 当前产物

- `01_index/family_entry_map_v1.tsv`
- `02_absorb_index/group08_rotation_style_contract_digest_v1.md`
- `02_absorb_index/group08_rotation_style_contract_decision_v1.md`
- `bundle/contracts/group08_rotation_style_p0_min_contract_v1.md`
- `bundle/fields/group08_rotation_style_field_dictionary_v1.tsv`

## 主负责人裁决

- 当前 `行业轮动 / 风格轮动` 只先冻结：
  - `A-C01` 残差动量多空行业配置模型
  - `A-C02` 涨跌比行业择时与轮动体系
  - `A-C03` 板块效应动量-反转交叉 Alpha
  - `A-C04` 公募基金持仓测算风格轮动模型
- 当前明确不直接升级为：
  - A股 P0 默认配置引擎
  - 默认仓位与行业暴露控制器
  - 完整论文级实现

## 默认阅读顺序

- 先看 `01_index/family_entry_map_v1.tsv`
- 再看 `02_absorb_index/group08_rotation_style_contract_decision_v1.md`
- 再进入最小合同与字段字典

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
