# Batch 142 Provenance

## 来源性质

- 当前批次是 `in-repo contract synthesis batch`。
- 当前不复制 `GROUP_08` 原始 PDF 或 cutpack，只回指仓库内已存在材料。

## 上游来源

- `10_source_library_archive/topic_entry/event_driven_stock_selection_topic_entry_v1.md`
- `10_source_library_archive/topic_entry/object_entry/earnings_announcement_event_object_entry_v1.md`
- `10_source_library_archive/topic_entry/market_timing_signal_topic_entry_v1.md`
- `10_source_library_archive/topic_entry/object_entry/market_timing_signal_object_entry_v1.md`
- `10_source_library_archive/mirror_kimi_inbox/GROUP_08_A股量化_数据研究/01_62份研究PDF/A股_量化选股_研究PDF_总摘要_v1_part1.md`
- `10_source_library_archive/mirror_kimi_inbox/GROUP_08_A股量化_数据研究/01_62份研究PDF/A股_量化择时_研究PDF_总摘要_v1.md`
- `10_source_library_archive/mirror_kimi_inbox/GROUP_08_A股量化_数据研究/06_pdf_retained_cut_v2/CUTPACK__G08__选股__事件驱动_业绩预告扭亏预减__v2.md`
- `10_source_library_archive/mirror_kimi_inbox/GROUP_08_A股量化_数据研究/06_pdf_retained_cut_v2/CUTPACK__G08__选股__事件驱动_大股东增减持__v2.md`
- `10_source_library_archive/mirror_kimi_inbox/GROUP_08_A股量化_数据研究/06_pdf_retained_cut_v2/CUTPACK__G08__择时__恐惧与贪婪择时指标__v2.md`
- `10_source_library_archive/mirror_kimi_inbox/GROUP_08_A股量化_数据研究/06_pdf_retained_cut_v2/CUTPACK__G08__择时__产业资本增减持择时__v2.md`

## 当前说明

- 本批次的合同与字段字典都属于：
  - `manual_synthesis`
  - `contract_freeze`
- 它们是“最小合同”，不是“论文完整复刻”。

## 证据边界

- `group08_event_driven_p0_min_contract_v1.md`
  - `evidence_mode = contract_freeze`
- `group08_market_timing_p0_min_contract_v1.md`
  - `evidence_mode = contract_freeze`
- 两张字段字典：
  - `evidence_mode = field_freeze`

## 当前不宣称

- 当前不宣称：
  - 所有参数已最优
  - 所有阈值都能直接复现论文结果
  - 已与主线 runtime 自动接线
