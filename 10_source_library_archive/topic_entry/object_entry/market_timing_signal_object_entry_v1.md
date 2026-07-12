# 市场择时信号对象入口 v1

## 适用问题

- 想直接进入 `市场一致性R²` 与 `产业资本增减持` 这两类补充择时信号
- 想优先看最低输入、最低输出与候选边界
- 想把择时摘要侧收成一个明确对象入口

## first-hop 入口

- `../../batch_142_group08_event_timing_contract_absorb__20260712/bundle/contracts/group08_market_timing_p0_min_contract_v1.md`

## 默认阅读顺序

- 先看合同：
  - `../../batch_142_group08_event_timing_contract_absorb__20260712/bundle/contracts/group08_market_timing_p0_min_contract_v1.md`
- 再看字段字典：
  - `../../batch_142_group08_event_timing_contract_absorb__20260712/bundle/fields/group08_market_timing_field_dictionary_v1.tsv`
- 再回看摘要候选：
  - `T-C01` 市场一致性 R² 择时模型
  - `T-C02` 产业资本增减持贝叶斯融合择时
- 若后续要对象化，优先抽：
  - 一致性指标序列
  - 预警与反转信号
  - 增减持净值滚动窗口
  - 后验预测分布

## 当前边界

- 当前对象入口已提升为“合同 first-hop + 研究回链”。
- 当前仍不代表已成为主线默认择时 gate。

## 回链

- 上层主题入口：
  - `../market_timing_signal_topic_entry_v1.md`
