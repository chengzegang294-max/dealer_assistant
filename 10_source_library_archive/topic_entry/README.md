# Topic Entry

## 用途

- 这里是 `10_source_library_archive` 的主题入口层。
- 当前作用是把“按批次进入”再往前收一层，变成“按主题进入”。
- 它不替代各批次 README，只负责 first-hop 导航。

## 当前主题

- `A股量化研究`
- `A股数据源决策`
- `系统吸收与正文回收`
- `外部吸收与回收提升`
- `原子方法对象孵化`
- `财报估值与组合管理`
- `事件驱动选股`
- `行业轮动与风格轮动`
- `多因子相关性选股`
- `动态因子有效性`
- `市场择时信号`

## 默认入口

- `topic_entry_index_v1.tsv`
- `TOPIC_OBJECT_OVERVIEW_v1.md`
- `topic_object_matrix_v1.tsv`
- `object_entry/README.md`
- `object_entry/object_entry_index_v1.tsv`
- `ashare_quant_research_topic_entry_v1.md`
- `ashare_data_source_decision_topic_entry_v1.md`
- `trae_system_absorb_topic_entry_v1.md`
- `external_absorb_recovery_topic_entry_v1.md`
- `atomic_method_incubation_topic_entry_v1.md`
- `finance_valuation_portfolio_topic_entry_v1.md`
- `event_driven_stock_selection_topic_entry_v1.md`
- `industry_rotation_style_topic_entry_v1.md`
- `multi_factor_correlation_stock_selection_topic_entry_v1.md`
- `dynamic_factor_validity_topic_entry_v1.md`
- `market_timing_signal_topic_entry_v1.md`

## 对象入口层

- `A股研究摘要对象`
  - `object_entry/ashare_research_summary_object_entry_v1.md`
- `A股数据源裁决对象`
  - `object_entry/ashare_data_source_decision_object_entry_v1.md`
- `系统吸收对象`
  - `object_entry/trae_system_selected_object_entry_v1.md`
- `外部吸收提升对象`
  - `object_entry/external_absorb_recovery_object_entry_v1.md`
- `多周期KD对象`
  - `object_entry/kd_mtf_object_entry_v1.md`
- `RSJ状态对象`
  - `object_entry/rsj_state_object_entry_v1.md`
- `高频价量相关性对象`
  - `object_entry/pv_corr_object_entry_v1.md`
- `四轴状态模板对象`
  - `object_entry/four_axis_state_object_entry_v1.md`
- `VanTharp R对象`
  - `object_entry/vantharp_r_object_entry_v1.md`
- `量化权益组合管理对象`
  - `object_entry/quant_equity_portfolio_object_entry_v1.md`
- `主动组合管理对象`
  - `object_entry/active_portfolio_management_object_entry_v1.md`
- `上市公司财报估值对象`
  - `object_entry/listed_company_valuation_object_entry_v1.md`
- `郭永清财报估值对象`
  - `object_entry/guo_yongqing_financial_statement_object_entry_v1.md`
- `业绩与公告事件驱动对象`
  - `object_entry/earnings_announcement_event_object_entry_v1.md`
- `行业轮动与风格轮动对象`
  - `object_entry/industry_rotation_signal_object_entry_v1.md`
- `相关性选股框架对象`
  - `object_entry/correlation_stock_selection_framework_object_entry_v1.md`
- `动态因子有效性对象`
  - `object_entry/dynamic_factor_validity_object_entry_v1.md`
- `市场择时信号对象`
  - `object_entry/market_timing_signal_object_entry_v1.md`

## 跨主题总检索

- 总说明：
  - `TOPIC_OBJECT_OVERVIEW_v1.md`
- 总表：
  - `topic_object_matrix_v1.tsv`

## 使用边界

- 想按主题找资料，先来这里。
- 想按常用对象一跳进入，再下钻批次或正文，进入 `object_entry/`
- 想横向比对主题与对象，再决定下一跳，先看 `topic_object_matrix_v1.tsv`
- 想看具体批次的完整清单、manifest、provenance，再下钻到对应批次 README 或 family entry map。
- 想找原件真值，不从这里进，直接去 `../raw_assets/README.md`。

## 回链

- 来源库根入口：
  - `../README.md`
- 根层总索引：
  - `../archive_batch_index_v1.tsv`
