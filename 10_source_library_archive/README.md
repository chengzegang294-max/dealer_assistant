# Source Library Archive

## 用途

- 这里放按批次筛选后迁入的新来源库材料。
- 这里不是 `10_来源库_SOURCE_LIBRARY` 的镜像副本。

## 默认入口

- 根层总导航：
  - `archive_batch_index_v1.tsv`
- 主题入口层：
  - `topic_entry/README.md`
  - `topic_entry/topic_entry_index_v1.tsv`
  - `topic_entry/TOPIC_OBJECT_OVERVIEW_v1.md`
  - `topic_entry/topic_object_matrix_v1.tsv`
  - `topic_entry/object_entry/README.md`
  - `topic_entry/object_entry/object_entry_index_v1.tsv`

## 三级导航

- 必看：
  - `batch_01_youzi_truth_anchors/README.md`
  - `batch_09_legacy_source_library_alignment__20260707/README.md`
  - `archive_batch_index_v1.tsv`
  - `topic_entry/README.md`
- 可选看：
  - `batch_100_non_kimi_public_methods_boundary__20260707/README.md`
  - `batch_101_non_kimi_atomic_rules_boundary__20260707/README.md`
  - `batch_102_non_kimi_atomic_kd_mtf_bundle__20260707/README.md`
  - `batch_103_non_kimi_atomic_rsj_state_bundle__20260707/README.md`
  - `batch_104_non_kimi_atomic_pv_corr_bundle__20260707/README.md`
  - `batch_105_non_kimi_atomic_four_axis_state_bundle__20260707/README.md`
  - `batch_106_non_kimi_atomic_vantharp_r_bundle__20260707/README.md`
  - `batch_107_non_kimi_public_batch9_bundle__20260707/README.md`
  - `batch_108_non_kimi_nftradez_method_bundle__20260707/README.md`
  - `batch_109_non_kimi_smile_smc_method_bundle__20260707/README.md`
  - `batch_110_external_folder_absorb__20260708/README.md`
  - `batch_120_tools_workspace_absorb__20260709/README.md`
  - `batch_131_trae_system_selected_absorb__20260709/README.md`
  - `batch_140_tushare_tdx_data_source_absorb__20260712/README.md`
  - `batch_141_trend_rotation_positioning_absorb__20260712/README.md`
- `archive_only / staging / raw_truth_side`：
  - `batch_132_trae_system_raw_snapshot_batch09_absorb__20260709/README.md`
  - `mirror_kimi_inbox/README_放这里.md`
  - `mirror_kimi_inbox/GROUP_08_A股量化_数据研究/GROUP_08_短索引入口_v1.md`
  - `raw_assets/README.md`

## 允许进入

- 对当前活跃对象有直接参考价值的来源材料
- 已确认非乱码、非重复、非临时副本的材料
- 已写清原路径与迁入理由的材料

## 不允许进入

- 整包来源库复制
- 只是“可能以后有用”的材料
- 已被活跃对象目录完全吸收的重复副本
- 乱码文件、损坏文件、无来源说明副本

## 当前状态

- 当前仍不批量迁入旧来源库内容。
- 当前已形成多批次归档：
  - `batch_01_youzi_truth_anchors` 作为首批真值锚点
  - `batch_09 / batch_100 / batch_101` 继续承担历史对齐与边界批职责
  - `batch_102 ~ batch_106` 已形成原子方法对象束，承接 `KD / RSJ / 高频价量相关性 / 四轴状态 / VanTharp R`
  - `batch_107 / batch_108 / batch_109` 已形成公开资料与方法参考稳定 bundle
  - `batch_110 / batch_120 / batch_131 / batch_132 / batch_140 / batch_141` 继续承接外部吸收批、工具工作区回收批、系统材料、数据源吸收批与仓位桥接吸收批
- `batch_01_youzi_truth_anchors` 仍是首批锚点，不再是唯一批次。
- 后续每一批迁入都要先完成四分流，再进入本层。

## 你该怎么进

- 想先看来源层全局结构：
  - 先看 `archive_batch_index_v1.tsv`
- 想按主题而不是按批次找资料：
  - 先看 `topic_entry/README.md`
  - 再看 `topic_entry/topic_entry_index_v1.tsv`
- 想横向比对主题、对象、primary target 和推荐阅读顺序：
  - 先看 `topic_entry/TOPIC_OBJECT_OVERVIEW_v1.md`
  - 再看 `topic_entry/topic_object_matrix_v1.tsv`
- 想按高频对象一跳进入：
  - 先看 `topic_entry/object_entry/README.md`
  - 再看 `topic_entry/object_entry/object_entry_index_v1.tsv`
- 想直接找 `KD / RSJ / 高频价量相关性 / 四轴状态 / VanTharp R` 这组原子方法对象：
  - 先看 `topic_entry/atomic_method_incubation_topic_entry_v1.md`
  - 再按对象进入 `topic_entry/object_entry/`
- 想直接找 `财报 / 估值 / 组合管理` 这组稳定切分对象：
  - 先看 `topic_entry/finance_valuation_portfolio_topic_entry_v1.md`
  - 再按对象进入 `topic_entry/object_entry/`
- 想直接找 `GROUP_08` 里的研究子簇：
  - `事件驱动` 先看 `topic_entry/event_driven_stock_selection_topic_entry_v1.md`
  - `行业轮动 / 风格轮动` 先看 `topic_entry/industry_rotation_style_topic_entry_v1.md`
  - `多因子相关性选股` 先看 `topic_entry/multi_factor_correlation_stock_selection_topic_entry_v1.md`
  - `动态因子有效性` 先看 `topic_entry/dynamic_factor_validity_topic_entry_v1.md`
  - `市场择时信号` 先看 `topic_entry/market_timing_signal_topic_entry_v1.md`
- 想直接找 `趋势仓位 / 轮动仓位` 这组桥接资料：
  - 先看 `topic_entry/trend_rotation_positioning_topic_entry_v1.md`
  - 再按对象进入 `topic_entry/object_entry/`
- 想找稳定真值锚点与历史对齐边界：
  - 先看 `batch_01` 与 `batch_09`
- 想看较新的吸收批：
  - 先看对应批次 README，再看批次内的 `family_entry_map_v1.tsv`
- 想看待入库资料而不是正式来源层：
  - 先去 `mirror_kimi_inbox/README_放这里.md`
  - 若当前就是 A 股量化资料，直接进 `GROUP_08_短索引入口_v1.md`
- 想找原件真值：
  - 直接去 `raw_assets/README.md`

## 批次分组

- `truth_anchor`
  - 首批真值锚点；优先看 `batch_01`
- `alignment_boundary`
  - 历史来源库对齐、边界判断、最小搬迁判断；优先看 `batch_09 / batch_100 / batch_101`
- `stable_bundle`
  - 已从边界批中提升出来、可以直接作为方法参考入口的稳定包；原子方法对象束优先看 `batch_102 ~ batch_106`，公开方法参考优先看 `batch_107 / batch_108 / batch_109`
- `absorb_batch`
  - 新近吸收的外部材料、系统材料、工作区回收批与仓位桥接批；优先看 `batch_110 / batch_120 / batch_131 / batch_140 / batch_141`
- `archive_only_absorb`
  - 只保留追溯价值，不作为 first-hop 默认入口；当前看 `batch_132`
- `staging_area / raw_truth_side`
  - `mirror_kimi_inbox` 是待入库与中转侧
  - `raw_assets` 是原件真值侧

## 主题入口

- `A股量化研究`
  - `topic_entry/ashare_quant_research_topic_entry_v1.md`
- `A股数据源决策`
  - `topic_entry/ashare_data_source_decision_topic_entry_v1.md`
- `系统吸收与正文回收`
  - `topic_entry/trae_system_absorb_topic_entry_v1.md`
- `外部吸收与回收提升`
  - `topic_entry/external_absorb_recovery_topic_entry_v1.md`
- `原子方法对象孵化`
  - `topic_entry/atomic_method_incubation_topic_entry_v1.md`
- `财报估值与组合管理`
  - `topic_entry/finance_valuation_portfolio_topic_entry_v1.md`
- `事件驱动选股`
  - `topic_entry/event_driven_stock_selection_topic_entry_v1.md`
- `行业轮动与风格轮动`
  - `topic_entry/industry_rotation_style_topic_entry_v1.md`
- `多因子相关性选股`
  - `topic_entry/multi_factor_correlation_stock_selection_topic_entry_v1.md`
- `动态因子有效性`
  - `topic_entry/dynamic_factor_validity_topic_entry_v1.md`
- `市场择时信号`
  - `topic_entry/market_timing_signal_topic_entry_v1.md`
- `趋势仓位与轮动仓位`
  - `topic_entry/trend_rotation_positioning_topic_entry_v1.md`

## 对象入口

- `A股研究摘要对象`
  - `topic_entry/object_entry/ashare_research_summary_object_entry_v1.md`
- `A股数据源裁决对象`
  - `topic_entry/object_entry/ashare_data_source_decision_object_entry_v1.md`
- `系统吸收对象`
  - `topic_entry/object_entry/trae_system_selected_object_entry_v1.md`
- `外部吸收提升对象`
  - `topic_entry/object_entry/external_absorb_recovery_object_entry_v1.md`
- `多周期KD对象`
  - `topic_entry/object_entry/kd_mtf_object_entry_v1.md`
- `RSJ状态对象`
  - `topic_entry/object_entry/rsj_state_object_entry_v1.md`
- `高频价量相关性对象`
  - `topic_entry/object_entry/pv_corr_object_entry_v1.md`
- `四轴状态模板对象`
  - `topic_entry/object_entry/four_axis_state_object_entry_v1.md`
- `VanTharp R对象`
  - `topic_entry/object_entry/vantharp_r_object_entry_v1.md`
- `量化权益组合管理对象`
  - `topic_entry/object_entry/quant_equity_portfolio_object_entry_v1.md`
- `主动组合管理对象`
  - `topic_entry/object_entry/active_portfolio_management_object_entry_v1.md`
- `上市公司财报估值对象`
  - `topic_entry/object_entry/listed_company_valuation_object_entry_v1.md`
- `郭永清财报估值对象`
  - `topic_entry/object_entry/guo_yongqing_financial_statement_object_entry_v1.md`
- `业绩与公告事件驱动对象`
  - `topic_entry/object_entry/earnings_announcement_event_object_entry_v1.md`
- `行业轮动与风格轮动对象`
  - `topic_entry/object_entry/industry_rotation_signal_object_entry_v1.md`
- `相关性选股框架对象`
  - `topic_entry/object_entry/correlation_stock_selection_framework_object_entry_v1.md`
- `动态因子有效性对象`
  - `topic_entry/object_entry/dynamic_factor_validity_object_entry_v1.md`
- `市场择时信号对象`
  - `topic_entry/object_entry/market_timing_signal_object_entry_v1.md`
- `趋势仓位对象`
  - `topic_entry/object_entry/trend_position_object_entry_v1.md`
- `轮动仓位对象`
  - `topic_entry/object_entry/rotation_position_object_entry_v1.md`

## 批次记录模板

- 批次名：
- 原路径：
- 新路径：
- 当前关联对象：
- 去重结论：
- 迁入理由：
