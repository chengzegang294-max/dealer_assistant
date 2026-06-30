# S Bucket Repo State Table

## repo_state_goal

- `goal=把S桶可用性压成repo内已稳定的小体量真值锚点+当前仍需补齐的真值缺口两层`
- `record_boundary=不记录树外路径|只记录repo内入口_真值文件_回帖副本_可审计对账锚点`

## 当前合同层

- repo 默认入口：
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_SUMMARY__2026-06-17.md`
- repo 真值文件：
  - `00_entry\S_BUCKET_REPO_STATE_TABLE__2026-06-26.md`
  - `00_entry\CUT_FILE_RETIREMENT_PLAN__2026-06-26.md`
  - `10_source_library_archive\mirror_kimi_inbox\docs\S_BUCKET__staging__EVAL__2026-06-23.md`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_INDEX__2026-06-17.tsv`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_report_representatives_v1.tsv` 到 `S_BUCKET_report_representatives_v52.tsv`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_stage_proof__01_集合竞价教程__v1.tsv`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_stage_proof__03_券商研报__representatives_v1.tsv` 到 `S_BUCKET_stage_proof__03_券商研报__representatives_v52.tsv`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_功能映射表_v1.tsv`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_功能归类最小框架_v1.md`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_KIMI_batch1_prompt_v1.txt`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_KIMI_batch1_priority_read_prompt_v1.txt`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_batch1_round2_focus_README_v1.md`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_batch1_round2_focus_manifest_v1.tsv`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_KIMI_batch1_round2_focus_prompt_v1.txt`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_KIMI_batch1_round2_direct_message_v2.txt`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_batch1_round3_function_core_README_v1.md`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_batch1_round3_function_core_manifest_v1.tsv`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_KIMI_batch1_round3_function_core_prompt_v1.txt`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_KIMI_batch1_round3_function_core_direct_message_v1.txt`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_batch2_priority_read_README_v1.md`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_batch2_priority_read_manifest_v1.tsv`
  - `10_source_library_archive\mirror_kimi_inbox\S_BUCKET_KIMI_batch2_priority_read_prompt_v1.txt`
- repo 回帖副本：
  - `10_source_library_archive\mirror_kimi_inbox\99_回收与外部回帖_IMPORTS\S_BUCKET_functional_cards_batch1_v15_v16__draft__imported_2026-06-24.md`
  - `10_source_library_archive\mirror_kimi_inbox\99_回收与外部回帖_IMPORTS\S_BUCKET_batch1_priority_read_v1__text_review__imported_2026-06-24.md`
  - `10_source_library_archive\mirror_kimi_inbox\99_回收与外部回帖_IMPORTS\S_BUCKET_batch1_round2_focus_v1__text_review__imported_2026-06-24.md`
- 扩展字段附注：
  - `durable_truth=S桶已具备repo内入口+映射+回帖+stage_proof；同时已补齐repo内全量索引与代表作对账TSV(S_BUCKET_INDEX+representatives_v1~v52+stage_proof_v1~v52)，并已建立repo内原件层(10_source_library_archive/raw_assets)；当前S_BUCKET_INDEX四分区868条已全部在repo内raw_assets可复核，03_券商研报md/pdf 477条已全覆盖，01_集合竞价教程49条、02_游资悟道交割单341条、04_待归类1条均已入仓，repo默认使用已不依赖树外路径`
  - `state=STAGE2_MAIN_BATTLEFIELD`
  - `boundary=不整包复制868个文件，不提前删源`

## current_state_decision_keys

- `stage1_status=DEFAULT_ENTRY_IN_REPO|KEY_DOCS_MAPPING_REPLIES_IN_REPO`
- `stage2_status=SMALL_TRUTH_ANCHORS_SUFFICIENT_FOR_OBJECT_CARD_AND_FUNCTION_MAPPING`
- `staging_eval_entry=10_source_library_archive\mirror_kimi_inbox\docs\S_BUCKET__staging__EVAL__2026-06-23.md`
- `staging_truth_boundary=LOCAL_DERIVED_STAGING__NOT_REPO_TRUTH|AUDIT_TRUTH=representatives_and_stage_proof_tsv_series`

## stable_truth_anchor_groups

- `core_entry_group=S_BUCKET_SUMMARY__2026-06-17.md|S_BUCKET_INDEX__2026-06-17.tsv|S_BUCKET_功能映射表_v1.tsv|S_BUCKET_功能归类最小框架_v1.md`
- `kimi_anchor_group`
  - `first_round=S_BUCKET_KIMI_batch1_prompt_v1.txt|S_BUCKET_functional_cards_batch1_v15_v16__draft__imported_2026-06-24.md`
  - `priority_read=S_BUCKET_KIMI_batch1_priority_read_prompt_v1.txt|S_BUCKET_batch1_priority_read_v1__text_review__imported_2026-06-24.md`
  - `round2=S_BUCKET_batch1_round2_focus_README_v1.md|S_BUCKET_batch1_round2_focus_manifest_v1.tsv|S_BUCKET_KIMI_batch1_round2_focus_prompt_v1.txt|S_BUCKET_KIMI_batch1_round2_direct_message_v2.txt|S_BUCKET_batch1_round2_focus_v1__text_review__imported_2026-06-24.md`
  - `round3=S_BUCKET_batch1_round3_function_core_README_v1.md|S_BUCKET_batch1_round3_function_core_manifest_v1.tsv|S_BUCKET_KIMI_batch1_round3_function_core_prompt_v1.txt|S_BUCKET_KIMI_batch1_round3_function_core_direct_message_v1.txt`
- `stage_proof_anchor_group`
  - `staging_eval=10_source_library_archive\mirror_kimi_inbox\docs\S_BUCKET__staging__EVAL__2026-06-23.md`
  - `staging_role=LOCAL_DERIVED_STAGING__NOT_REPO_TRUTH`
  - `tutorial_stage_proof=S_BUCKET_stage_proof__01_集合竞价教程__v1.tsv`
  - `report_representatives=S_BUCKET_report_representatives_v1.tsv~v52.tsv`
  - `report_stage_proof=S_BUCKET_stage_proof__03_券商研报__representatives_v1.tsv~v52.tsv`

## raw_asset_mapping_keys

- `repo_raw_assets_root=10_source_library_archive\raw_assets\`
- `source_anchor_mapping=10_source_library_archive\raw_assets\<source_anchor>`

## retirement_decision_keys

- `tree_out_default=DELETE_READY|repo_default_use_and_audit_no_longer_depend_on_tree_out`
- `repo_raw_assets_s=HOLD_AS_REPO_TRUTH|承担S_BUCKET_INDEX四分区868条文件本体与复核职责|不属于待退场对象`
- `derived_staging_role=HISTORY_ONLY|只保留来源评估与历史追溯角色|不承担repo_truth`
- `partition_status_table`
  - `01_集合竞价教程`：`tree_out=DELETE_READY / repo_raw_assets=HOLD_AS_REPO_TRUTH / note=stage_proof_49_done`
  - `02_游资悟道交割单`：`tree_out=DELETE_READY / repo_raw_assets=HOLD_AS_REPO_TRUTH / note=341_imported`
  - `03_券商研报`：`tree_out=DELETE_READY / repo_raw_assets=HOLD_AS_REPO_TRUTH / note=representatives_408_proof+md_pdf_477_full`
  - `04_待归类`：`tree_out=DELETE_READY / repo_raw_assets=HOLD_AS_REPO_TRUTH / note=1_pdf_imported`
- `report_subset_status_table`
  - `representatives_proof`：`tree_out=DELETE_READY / repo_raw_assets=HOLD_AS_REPO_TRUTH / note=408_rows_407_unique`
  - `index_only_md_pdf`：`tree_out=DELETE_READY / repo_raw_assets=HOLD_AS_REPO_TRUTH / note=70_unique`
  - `05_其他/future_bucket`：`tree_out=DELETE_READY / repo_raw_assets=HOLD_AS_REPO_TRUTH / note=70_unique_and_equal_to_index_only`
- `report_subset_action_table`
  - `representatives_proof`：`action=HOLD_AS_REPO_TRUTH+OBJECT_CARD_FIRST`
  - `index_only_md_pdf`：`action=HOLD_AS_REPO_TRUTH+NO_AUTO_PROOF`
  - `05_其他/future_bucket`：`action=FUTURE_BUCKET+EXPLICIT_APPROVAL_ONLY`
  - `executed_objects=SBKT_F014/SBKT_F006=OBJECT_CARD_FIRST__ENTER_FUNCTION_CORE_WITH_BOUNDARY|SBKT_F002=OBJECT_CARD_FIRST__KEEP_AS_LIMITED_CANDIDATE`
- `machine_learning_branch_table`
  - `SBKT_F004=TEXT_EVIDENCE_IMPORTED__NO_OCR|role=TRAINING_RISK_METHOD|use=验证层规范`
  - `SBKT_F005=TEXT_EVIDENCE_LOCAL_PDF__NO_OCR|role=AI_SYSTEM_BLUEPRINT|use=量价AI全流程体系蓝图`
  - `SBKT_F012=TEXT_EVIDENCE_LOCAL_PDF__NO_OCR|role=LABELING_METHOD|use=标签方案对比与XGBR-Combine`
- `hf_micro_branch_table`
  - `SBKT_F009=TEXT_EVIDENCE_LOCAL_PDF__NO_OCR|role=HOLDING_INFERENCE_FILTER|use=公募持仓变化预估与偏离监测`
  - `SBKT_F010=TEXT_EVIDENCE_LOCAL_PDF__NO_OCR|role=INSTITUTION_ACTIVITY_MONITOR|use=算法单峰值与机构活跃度监测`
  - `next_text_read_queue=NONE`
- `draft_bridge_upgrade_sequence`
  - `machine_learning_first=SBKT_F012->SBKT_F005__FIRST_TEXT_EVIDENCE_PAIR_DONE`
  - `institution_behavior_second=SBKT_F009->SBKT_F010__TEXT_EVIDENCE_UPGRADE_DONE`
  - `upgrade_reason=先补F004上游机器学习链|再补F007低高频互证链|batch2四对象正文证据已齐`
- `batch2_text_read_package`
  - `repo_default_entry=S_BUCKET_batch2_priority_read_README_v1.md`
  - `repo_truth=manifest_tsv+prompt_txt+mapping_tsv+draft_import_md+excerpt_table_tsv`
  - `reply_landing=S_BUCKET_batch2_priority_read_v1__text_review__imported_2026-06-26.md`
  - `current_state=BATCH2_CLOSED_LOOP__REPO_REPLY_LANDED`
  - `probe_status=pypdf_ready|4_of_4_readable|F012_F005_F009_F010_TEXT_EVIDENCE_READY|page_excerpt_and_repo_reply_landed`
  - `evidence_table=S_BUCKET_batch2_evidence_excerpt_table_v1.tsv`
  - `excerpt_rows=14`
- `post_batch2_mainline_return_queue`：
  - `SBKT_F014=FUNCTION_LIBRARY_ENTRY__RESIDUALIZE_TURNOVER_MOMENTUM_FIRST`
  - `SBKT_F006=DEFAULT_USAGE_ORDER__ID2_STD_3M_PRIMARY+HML_R_STD_5M_SUPPORT`
  - `SBKT_F002=LIMITED_CANDIDATE_HARD_BOUNDARY__SHORT_ONLY_OR_LONG_SHORT_ONLY`
- `round3_usage_order_truth`
  - `table=S_BUCKET_round3_function_core_usage_order_v1.tsv`
  - `rank_order=SBKT_F014=function_core_primary|SBKT_F006=function_core_secondary|SBKT_F002=limited_candidate_guard`
  - `freeze_state=READY_TO_FREEZE__DEFAULT_USAGE_ORDER`
  - `boundary=usage_order_only_for_F014_F006_F002|F007_F009_F010_stay_in_supporting_mapping_evidence_object_card`
- `round3_operator_profile_truth`
  - `table=S_BUCKET_round3_function_core_operator_profile_v1.tsv`
  - `F014=residualize_turnover_momentum_first|mfd_sellord_primary|mfd_volinflowrate_open_m_support`
  - `F006=id2_std_3m_primary|hml_r_std_5m_support`
  - `F002=filter_only|fallback=limit_use_or_residualize_first`
  - `freeze_state=READY_TO_FREEZE__OPERATOR_PROFILE`
- `master_registry_truth`
  - `table=S_BUCKET_function_object_master_registry_v1.tsv`
  - `objects=SBKT_F002+F004+F005+F006+F007+F009+F010+F012+F014`
  - `freeze_state=READY_TO_FREEZE__MASTER_REGISTRY`
- `top_level_contract_schema_truth`
  - `table=S_BUCKET_top_level_contract_schema_v1.tsv`
  - `order=mapping_table->master_registry->remaining_object_decisions->function_library_entry->field_truth_index->object_field_truth`
  - `crosswalk=round3=master_registry->function_library_entry->field_truth_index|supporting=master_registry->detail_truth_anchor`
  - `freeze_state=READY_TO_FREEZE__TOP_LEVEL_CONTRACT_SCHEMA`
- `proof_mapping_queue_truth`
  - `table=S_BUCKET_proof_of_mapping_priority_queue_v1.tsv`
  - `top3=SBKT_F014->SBKT_F006->SBKT_F002`
  - `supporting_followups=SBKT_F007+F009+F010+F004+F005+F012`
  - `freeze_state=MAINLINE_PROOF_CLOSED__SUPPORTING_QUEUE_READY`
- `mainline_runtime_truths`
  - `SBKT_F014=runtime_dir:02_runtime\s_bucket_f014_proof_of_mapping_v1|real_input_csv:real_input_samples\f014_proof_input_sample_v1.csv|proof_script_py:s_bucket_f014_proof_of_mapping_v1.py|proof_output_csv:real_input_samples\f014_proof_output_v1.csv|run_result:row_count=3`
  - `SBKT_F006=runtime_dir:02_runtime\s_bucket_f006_proof_of_mapping_v1|real_input_csv:real_input_samples\f006_proof_input_sample_v1.csv|proof_script_py:s_bucket_f006_proof_of_mapping_v1.py|proof_output_csv:real_input_samples\f006_proof_output_v1.csv|run_result:row_count=3`
  - `SBKT_F002=runtime_dir:02_runtime\s_bucket_f002_proof_of_mapping_v1|real_input_csv:real_input_samples\f002_proof_input_sample_v1.csv|proof_script_py:s_bucket_f002_proof_of_mapping_v1.py|proof_output_csv:real_input_samples\f002_proof_output_v1.csv|run_result:row_count=3`
- `supporting_runtime_truths`
  - `SBKT_F007=runtime_dir:02_runtime\s_bucket_f007_proof_of_mapping_v1|real_input_csv:real_input_samples\f007_proof_input_sample_v1.csv|proof_script_py:s_bucket_f007_proof_of_mapping_v1.py|proof_output_csv:real_input_samples\f007_proof_output_v1.csv|run_result:row_count=3`
  - `SBKT_F009=runtime_dir:02_runtime\s_bucket_f009_proof_of_mapping_v1|real_input_csv:real_input_samples\f009_proof_input_sample_v1.csv|proof_script_py:s_bucket_f009_proof_of_mapping_v1.py|proof_output_csv:real_input_samples\f009_proof_output_v1.csv|run_result:row_count=3`
  - `SBKT_F010=runtime_dir:02_runtime\s_bucket_f010_proof_of_mapping_v1|real_input_csv:real_input_samples\f010_proof_input_sample_v1.csv|proof_script_py:s_bucket_f010_proof_of_mapping_v1.py|proof_output_csv:real_input_samples\f010_proof_output_v1.csv|run_result:row_count=3`
  - `SBKT_F004=runtime_dir:02_runtime\s_bucket_f004_proof_of_mapping_v1|real_input_csv:real_input_samples\f004_proof_input_sample_v1.csv|proof_script_py:s_bucket_f004_proof_of_mapping_v1.py|proof_output_csv:real_input_samples\f004_proof_output_v1.csv|run_result:row_count=3`
  - `SBKT_F005=runtime_dir:02_runtime\s_bucket_f005_proof_of_mapping_v1|real_input_csv:real_input_samples\f005_proof_input_sample_v1.csv|proof_script_py:s_bucket_f005_proof_of_mapping_v1.py|proof_output_csv:real_input_samples\f005_proof_output_v1.csv|run_result:row_count=3`
  - `SBKT_F012=runtime_dir:02_runtime\s_bucket_f012_proof_of_mapping_v1|real_input_csv:real_input_samples\f012_proof_input_sample_v1.csv|proof_script_py:s_bucket_f012_proof_of_mapping_v1.py|proof_output_csv:real_input_samples\f012_proof_output_v1.csv|run_result:row_count=3`
- `S桶` 剩余对象快裁决表：
  - `table`：`S_BUCKET_remaining_object_decisions_v1.tsv`
  - `source_only`：`SBKT_F001 + F003 + F011`
  - `future_bucket`：`SBKT_F008 + F013 + F015 + F016`
  - `freeze_state`：`DECISION_FIXED__NO_PROMOTION_WITHOUT_TEXT_REVIEW`
- `round3` 功能库入口总表：
  - `table`：`S_BUCKET_round3_function_core_function_library_entry_v1.tsv`
  - `objects`：`SBKT_F014 + SBKT_F006 + SBKT_F002`
  - `freeze_state`：`READY_TO_FREEZE__FUNCTION_LIBRARY_ENTRY`
- `round3` 三对象字段级入口总索引：
  - `table`：`S_BUCKET_round3_function_core_field_truth_index_v1.tsv`
  - `objects`：`SBKT_F014 + SBKT_F006 + SBKT_F002`
  - `freeze_state`：`READY_TO_FREEZE__FIELD_TRUTH_INDEX`
- `round3` `F014` residualize 字段真值：
  - `table`：`S_BUCKET_round3_function_core_f014_residualize_fields_v1.tsv`
  - `inputs`：`turnover_proxy + momentum_proxy + mfd_sellord_raw + mfd_volinflowrate_open_m_raw`
  - `outputs`：`mfd_sellord_resid_tm + mfd_volinflowrate_open_m_resid_tm + f014_two_factor_min_combo`
  - `freeze_state`：`READY_TO_FREEZE__F014_RESIDUALIZE_FIELD_TRUTH`
- `round3` `F006` 双因子字段真值：
  - `table`：`S_BUCKET_round3_function_core_f006_combo_fields_v1.tsv`
  - `inputs`：`daily_ohlcv_base + industry_mv_neutralizer + id2_std_3m_raw + hml_r_std_5m_raw`
  - `outputs`：`id2_std_3m_neutralized + hml_r_std_5m_neutralized + f006_two_factor_min_combo`
  - `freeze_state`：`READY_TO_FREEZE__F006_COMBO_FIELD_TRUTH`
- `round3` `F002` guard 字段真值：
  - `table`：`S_BUCKET_round3_function_core_f002_guard_fields_v1.tsv`
  - `inputs`：`return_quantile_input + active_trade_ratio_input`
  - `outputs`：`f002_short_filter_signal + f002_long_short_filter_signal + f002_guard_decision + f002_residualize_required_flag + f002_long_only_block_flag`
  - `freeze_state`：`READY_TO_FREEZE__F002_GUARD_FIELD_TRUTH`
- `03_券商研报` 首批对象卡最小字段：
  - `SBKT_F014`：`min_input=Wind_or_L2资金流向聚合；min_output=mfd_sellord+mfd_volinflowrate_open_m；forbid=尾盘类/净主动买入无效类重开；combo_boundary=10日持仓+与换手率/动量先做残差剥离`
  - `SBKT_F006`：`min_input=日频OHLCV；min_output=id2_std_3m+hml_r_std_5m；forbid=7个高相关波动率因子并行堆叠；combo_boundary=仅保留非冗余双因子+注意行业市值中性`
  - `SBKT_F002`：`min_input=收益率分位+主动成交占比映射；min_output=空头/多空过滤信号；forbid=多头增强/通用alpha；combo_boundary=与反转/波动率高相关时先限用途或残差化`
  - schema 已固化到 repo TSV：`S_BUCKET_功能映射表_v1.tsv` 新增 `card_role/input_data/output_factor/forbid_rule/combo_boundary/evidence_level`，并继续补 `master_registry_entry/primary_truth_entry/detail_truth_anchor` 三列；`S_BUCKET_batch1_round3_function_core_manifest_v1.tsv` 新增 `input_data/output_factor/role_tag/forbid_rule/combo_boundary`
  - 第二批 `priority_read` 已并回 schema：`SBKT_F007=FILTER_WITH_STYLE_BOUNDARY；SBKT_F004=TRAINING_RISK_METHOD`
  - 第三批高频微观支线已升正文证据层：`SBKT_F009=HOLDING_INFERENCE_FILTER；SBKT_F010=INSTITUTION_ACTIVITY_MONITOR；evidence=TEXT_EVIDENCE_LOCAL_PDF__NO_OCR；use=F007=低频主锚点；F009/F010=高频双证据之一；不进usage_order/round3`
  - 第四批机器学习支线已升正文证据层：`SBKT_F004=TRAINING_RISK_METHOD；SBKT_F005=AI_SYSTEM_BLUEPRINT；SBKT_F012=LABELING_METHOD；use=F004=验证层规范；F005=蓝图上位卡；F012=标注桥接层；只作机器学习支线；不进usage_order/round3`

## minimum_conclusion_keys

- `S桶` 现在不缺入口，也不缺小体量真值锚点。
 - `current_contract_layer=历史追溯层与当前合同层分层|不再保留未独立/外部保留层旧说法`
- `supporting_proof_queue=F007/F009/F010/F004/F005/F012__ALL_LANDED|legacy_migration_batch=13_ANCHORS_FIXED`
  - `ml_branch_contract=F004=验证层规范|F005=蓝图上位卡|F012=标注桥接层|只作机器学习支线|不进usage_order/round3`
  - `hf_branch_contract=F007=低频主锚点|F009/F010=高频双证据之一|不进usage_order/round3`
  - `hf_mapping_relation=F007=低频主锚点|F009/F010=高频双证据之一|不进usage_order/round3`
  - `external_delete_boundary=repo默认入口不依赖树外路径|不批量删除外部原件|仅保留历史追溯与显式批准后的分批处理`
  - `summary` 字段合同当前已固定为：`repo_default_entry / repo_truth_files / reply_copy / durable_truth / fixed_decision / import_status / review_status / review_result / first_pass_objects / object_scope / reduction_result / audit_status`
  - `summary_tail_key_blocks=entry_contract_template|routing_4way|suggested_sequence|forbid_before_independence|acceptance_rule|supporting_inventory`
  - `filled_bucket_status=02_指数增强=EXHAUSTED|03_机器学习=v41_LAST_1_USED|01_高频微观=v49_LAST_2_USED|04_多因子=v52_LAST_2_FILLED`
  - `quota_expansion_rule=FOUR_TARGET_BUCKETS_FILLED__NO_OLD_QUOTA_EXPANSION`
 - `mainline_return_sequence=SBKT_F014->SBKT_F006->SBKT_F002`
- `repo_verification_status=READY`
  - `03_券商研报`：`stage_proof__representatives_v1~v52` 合计 `408` 条，`source_exists=1` 且 `stage_status=COPIED_OR_SYNCED` 均为真；对应 `raw_assets` 原件存在性校验缺口为 `0`
  - `03_券商研报`：`S_BUCKET_INDEX__2026-06-17.tsv` 中 `md/pdf` 合计 `477` 条，`raw_assets` 原件存在性校验缺口为 `0`（本轮补齐 `index_only` 缺口 `70` 条，阈值 `size_bytes<=100995113`）
  - `S_BUCKET_INDEX__2026-06-17.tsv`：四分区合计 `868` 条（`01=49` / `02=341` / `03=477` / `04=1`），对应 `raw_assets` 原件存在性校验缺口为 `0`
  - `03_券商研报` 子集切分：`representatives_proof=408` 行、`407` 个唯一 `source_anchor`；`index_only_md_pdf=70` 个唯一 `source_anchor`；该 `70` 条与 `05_其他` 完全相等
  - `round3 function core manifest`：`SBKT_F014 / SBKT_F006 / SBKT_F002` 的对象卡动作状态已固定，不再等待树外流程
  - `mapping/manifest schema`：三对象已具备可机读字段列，可直接支撑后续功能库或对象表接入
- `closure_decision=不再继续补原件|只把repo已完全自足的新口径同步到各层入口|删源/追溯边界写清`


## next_action_keys

1. `mainline_proof_status=SBKT_F014->SBKT_F006->SBKT_F002__CLOSED_LOOP`
2. `supporting_proof_status=SBKT_F007/F009/F010/F004/F005/F012__ALL_LANDED`
3. `default_handoff=不再补supporting_proof|回到对象卡与功能映射收口|机器学习支线与高频机构行为支线用统一短句合同承接映射表/注册表/组合关系说明`
4. `position_representatives_proof=对象卡与功能映射收口|不再默认重开主线proof`
5. `position_index_only_md_pdf=NO_AUTO_PROOF|只保留repo_truth与索引复核角色`
6. `position_05_other=FUTURE_BUCKET+EXPLICIT_APPROVAL_ONLY`
7. `legacy_migration_batch=S_BUCKET_功能映射表_v1.tsv|S_BUCKET_function_object_master_registry_v1.tsv|S_BUCKET_proof_of_mapping_priority_queue_v1.tsv|S_BUCKET_batch2_evidence_excerpt_table_v1.tsv|S_BUCKET_functional_cards_batch1_v15_v16__draft__imported_2026-06-24.md|S_BUCKET_batch2_priority_read_v1__text_review__imported_2026-06-26.md|S_BUCKET_REPO_STATE_TABLE__2026-06-26.md|S_BUCKET_SUMMARY__2026-06-17.md|00_主线检索索引.md|01_阶段一_项目记录_过去与落地.md|02_阶段二_工作方向_想法库.md|03_阶段二_当下计划_执行清单.md|关于日活.md`
8. `durable_sync_targets=CUT_FILE_RETIREMENT_PLAN__2026-06-26.md|03_阶段二_当下计划_执行清单.md|关于日活.md`
