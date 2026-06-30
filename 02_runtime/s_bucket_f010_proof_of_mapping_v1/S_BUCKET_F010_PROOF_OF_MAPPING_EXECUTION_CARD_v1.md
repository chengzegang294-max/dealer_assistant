# S_BUCKET_F010_PROOF_OF_MAPPING_EXECUTION_CARD_V1

## 对象

- `object_id`：`SBKT_F010`
- `current_role`：`INSTITUTION_ACTIVITY_MONITOR`
- `mapping_target`：`supporting_object_mapping`

## 生成入口

- `source_path`：`10_source_library_archive\mirror_kimi_inbox\S_BUCKET_batch2_evidence_excerpt_table_v1.tsv`
- `detail_truth_anchor`：`10_source_library_archive\mirror_kimi_inbox\99_回收与外部回帖_IMPORTS\S_BUCKET_batch2_priority_read_v1__text_review__imported_2026-06-26.md`
- `producer`：`02_runtime\s_bucket_f010_proof_of_mapping_v1\s_bucket_f010_proof_of_mapping_v1.py`
- `scope`：`supporting proof-of-mapping only`
- `status`：`diag_only_proof`

## 当前三件套

- `real_input_csv`：`02_runtime\s_bucket_f010_proof_of_mapping_v1\real_input_samples\f010_proof_input_sample_v1.csv`
- `proof_script_py`：`02_runtime\s_bucket_f010_proof_of_mapping_v1\s_bucket_f010_proof_of_mapping_v1.py`
- `proof_output_csv`：`02_runtime\s_bucket_f010_proof_of_mapping_v1\real_input_samples\f010_proof_output_v1.csv`

## 当前作用

- 证明 `F010` 的机构活跃度监测 supporting 合同可被 repo 内样本和脚本稳定复现。
- 为 `F009/F007` 的低高频互证层补齐第二个高频监测入口。
- 不把 `proof_output_csv` 写入任何主 runtime CSV。

## 当前禁令

- 不宣称 `F010` 的峰值监测特征可直接下单。
- 不宣称所有高频交易都来自机构。
- 不宣称 `F010` 已接入任何主 runtime CSV。
