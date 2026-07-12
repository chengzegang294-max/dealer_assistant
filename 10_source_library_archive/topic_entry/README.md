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

## 对象入口层

- `A股研究摘要对象`
  - `object_entry/ashare_research_summary_object_entry_v1.md`
- `A股数据源裁决对象`
  - `object_entry/ashare_data_source_decision_object_entry_v1.md`
- `系统吸收对象`
  - `object_entry/trae_system_selected_object_entry_v1.md`
- `外部吸收提升对象`
  - `object_entry/external_absorb_recovery_object_entry_v1.md`

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
