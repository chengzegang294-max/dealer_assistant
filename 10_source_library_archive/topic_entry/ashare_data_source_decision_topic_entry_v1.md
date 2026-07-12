# A股数据源决策主题入口 v1

## 适用问题

- 想知道当前 A 股 P0 数据源到底怎么选
- 想区分 `Tushare / 通达信 / AKShare / 雪球` 的项目内角色
- 想找教程内化摘要，而不是先回原始导出稿

## first-hop 入口

- `../batch_140_tushare_tdx_data_source_absorb__20260712/README.md`

## 最顺阅读顺序

- 第一步：
  - 先看 `../batch_140_tushare_tdx_data_source_absorb__20260712/01_index/family_entry_map_v1.tsv`
- 第二步：
  - 若想看教程核心内化摘要，进入 `02_absorb_index/tushare_tdx_tutorial_core_digest_v1.md`
  - 若想看项目最终裁决，进入 `02_absorb_index/ashare_p0_data_source_decision_v1.md`
- 第三步：
  - 只有在需要核对原始导出稿时，再进入 `00_raw_snapshot/`

## 当前边界

- 当前主题入口主要服务：
  - A 股 P0 的数据源选择
  - 教程吸收后的项目化裁决
  - 后续数据源分层使用的 first-hop 导航
- 当前不承担：
  - runtime 执行入口本身
  - T02 真实链结果页本身

## 当前结论速记

- 当前最重要的项目化结论是：
  - `Tushare` 承担必需缺口
  - `通达信` 承担后续 `OHLCV / 分钟线` 底表优先评估对象
  - `AKShare / 雪球` 作为补源，不先升格为唯一真值源

## 回链

- 来源库根入口：
  - `../README.md`
- 批次家族入口：
  - `../batch_140_tushare_tdx_data_source_absorb__20260712/01_index/family_entry_map_v1.tsv`
