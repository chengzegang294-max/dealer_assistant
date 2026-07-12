# 业绩与公告事件驱动对象入口 v1

## 适用问题

- 想直接进入 `事件驱动选股` 中最接近项目现有事件主线的一组候选
- 想优先看业绩预告、指数样本股调整、大股东增减持、股权激励
- 想先看摘要里已经提炼好的可量化字段与时间窗口

## first-hop 入口

- `../../batch_142_group08_event_timing_contract_absorb__20260712/bundle/contracts/group08_event_driven_p0_min_contract_v1.md`

## 默认阅读顺序

- 先看合同：
  - `../../batch_142_group08_event_timing_contract_absorb__20260712/bundle/contracts/group08_event_driven_p0_min_contract_v1.md`
- 再看字段字典：
  - `../../batch_142_group08_event_timing_contract_absorb__20260712/bundle/fields/group08_event_driven_field_dictionary_v1.tsv`
- 再回看摘要候选：
  - `S-017` 业绩快报与预减反弹
  - `S-018` 指数样本股调整
  - `S-020` 大股东增减持
  - `S-021` 股权激励实施收益
- 最后回看：
  - `S-016` 业绩预告事件超额收益框架
- 若后续要对象化，优先抽：
  - 事件时间窗口
  - 公告分类标签
  - 持有期与超额收益统计字段

## 当前边界

- 当前对象入口已提升为“合同 first-hop + 研究回链”。
- 当前仍不代表这些事件已经接入正式 runtime 执行链。

## 回链

- 上层主题入口：
  - `../event_driven_stock_selection_topic_entry_v1.md`
