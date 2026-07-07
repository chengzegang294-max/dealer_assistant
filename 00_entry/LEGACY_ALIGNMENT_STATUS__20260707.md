# LEGACY Alignment Status (Batch09)

## Scope

- 旧库的“可删除无副作用”已达成：旧根已退场；当前可追溯快照位于 `batch_09` 的 `lifted_trading_analysis`。
- 本文件不把旧库当作默认入口；它只回答“旧库内容与新仓库主线如何对齐、哪些已迁入、哪些仍只在快照里”。

## Canonical Rules

- 总迁移地图：见 [FULL_REPO_MIGRATION_MAP.md](file:///d:/Stock/trading_assistant/00_entry/FULL_REPO_MIGRATION_MAP.md)
- 扫库裁决任务板：见 [OLD_REPO_FILE_SWEEP_TASKBOARD.md](file:///d:/Stock/trading_assistant/00_entry/OLD_REPO_FILE_SWEEP_TASKBOARD.md)

## Snapshot Location

- Raw snapshot root: `12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_trading_analysis`
- Inventory (dst, sha256, excluded env/cache): `inventory_v2_dst_excluded_sha256__20260707_pass2.tsv`

## Audit Outputs

- Alignment audit (full): `12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_alignment_audit__20260707.tsv`
- Alignment audit summary: `12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_alignment_audit__20260707.summary.json`
- Alignment gaps (target missing): `12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_alignment_gaps__20260707.tsv`
- Alignment gaps summary: `12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_alignment_gaps__20260707.summary.json`

## Current Alignment Summary (Counts)

- Total files in snapshot: 4061
- Category distribution (audit-derived):
  - tooling_runtime_raw_snapshot: 1376 (target_exists=1376)
  - source_library_mirror: 1279 (target_exists=1279, missing=0)
  - source_library_raw_snapshot: 937 (target_exists=937)
  - data_unclassified: 210 (target_exists=210)
  - tools_unclassified: 47 (target_exists=47)
  - frozen_summaries_raw_snapshot: 44 (target_exists=44)
  - docs_backlog_or_other: 10 (target_exists=10)
  - trae_mirror_select: 3 (target_exists=3)
  - trae_raw_snapshot: 31 (target_exists=31)
  - backtest_out_archive: 1 (target_exists=1)
  - active_main_docs: 9 (target_exists=9)
  - others: 136

## What Is Already Migrated (Canonical Exists)

- Root active docs: snapshot root docs 已由 `04_active_main_docs/batch_01_selected/` 作为主线承接（7/7）。
- `.vscode/settings.json`: 作为仓库配置存在（1/1）。
- `.trae` 的 recover 系列：`21_trae_system_archive/batch_01_selected/` 已存在一份选择性镜像（部分匹配）。
- `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库`：1279 个文件已全部在 `10_source_library_archive/mirror_kimi_inbox/` 对齐命中；已推进批次：
  - `batch_10_kimi_inbox_promote_group08_source_raw__20260707`（129 files / 249MB）
  - `batch_11_kimi_inbox_promote_group10_a5_qepm__20260707`（55 files / 1.4MB）
  - `batch_12_kimi_inbox_promote_group10_a5_active_portfolio__20260707`（25 files / 1.0MB）
  - `batch_13_kimi_inbox_promote_group10_a5_valuation__20260707`（23 files / 2.1MB）
  - `batch_14_kimi_inbox_promote_s_bucket_representatives_v50__20260707`（8 files / 94MB）
  - `batch_15_kimi_inbox_promote_s_bucket_representatives_v51__20260707`（8 files / 88MB）
  - `batch_16_kimi_inbox_promote_s_bucket_representatives_v9__20260707`（8 files / 68MB）
  - `batch_17_kimi_inbox_promote_s_bucket_representatives_v49__20260707`（8 files / 67MB）
  - `batch_18_kimi_inbox_promote_s_bucket_representatives_v10__20260707`（8 files / 55MB）
  - `batch_19_kimi_inbox_promote_s_bucket_representatives_v28__20260707`（8 files / 45MB）
  - `batch_20_kimi_inbox_promote_s_bucket_representatives_v14__20260707`（8 files / 43MB）
  - `batch_21_kimi_inbox_promote_s_bucket_representatives_v6__20260707`（8 files / 43MB）
  - `batch_22_kimi_inbox_promote_s_bucket_representatives_v12__20260707`（8 files / 42MB）
  - `batch_23_kimi_inbox_promote_auction_videos__20260707`（11 files / 0.5MB）
  - `batch_24_kimi_inbox_promote_s_bucket_representatives_v7__20260707`（8 files / 39MB）
  - `batch_25_kimi_inbox_promote_s_bucket_representatives_v36__20260707`（8 files / 37MB）
  - `batch_26_kimi_inbox_promote_s_bucket_representatives_v39__20260707`（8 files / 36MB）
  - `batch_27_kimi_inbox_promote_s_bucket_representatives_v32__20260707`（8 files / 35MB）
  - `batch_28_kimi_inbox_promote_s_bucket_representatives_v13__20260707`（8 files / 35MB）
  - `batch_29_kimi_inbox_promote_s_bucket_representatives_v26__20260707`（8 files / 33MB）
  - `batch_30_kimi_inbox_promote_s_bucket_representatives_v40__20260707`（8 files / 33MB）
  - `batch_31_kimi_inbox_promote_s_bucket_representatives_v16__20260707`（8 files / 31MB）
  - `batch_32_kimi_inbox_promote_s_bucket_representatives_v30__20260707`（8 files / 28MB）
  - `batch_33_kimi_inbox_promote_s_bucket_representatives_v11__20260707`（8 files / 27MB）
  - `batch_34_kimi_inbox_promote_s_bucket_representatives_v38__20260707`（8 files / 27MB）
  - `batch_35_kimi_inbox_promote_s_bucket_representatives_v15__20260707`（8 files / 27MB）
  - `batch_36_kimi_inbox_promote_s_bucket_representatives_v3__20260707`（8 files / 26MB）
  - `batch_37_kimi_inbox_promote_s_bucket_representatives_v23__20260707`（8 files / 24MB）
  - `batch_38_kimi_inbox_promote_s_bucket_representatives_v34__20260707`（8 files / 23MB）
  - `batch_39_kimi_inbox_promote_s_bucket_representatives_v37__20260707`（8 files / 23MB）
  - `batch_40_kimi_inbox_promote_s_bucket_representatives_v19__20260707`（8 files / 23MB）
  - `batch_41_kimi_inbox_promote_s_bucket_representatives_v35__20260707`（8 files / 22MB）
  - `batch_42_kimi_inbox_promote_s_bucket_representatives_v31__20260707`（8 files / 22MB）
  - `batch_43_kimi_inbox_promote_s_bucket_representatives_v24__20260707`（8 files / 21MB）
  - `batch_44_kimi_inbox_promote_s_bucket_representatives_v18__20260707`（8 files / 20MB）
  - `batch_45_kimi_inbox_promote_s_bucket_representatives_v22__20260707`（8 files / 19MB）
  - `batch_46_kimi_inbox_promote_s_bucket_representatives_v21__20260707`（8 files / 19MB）
  - `batch_47_kimi_inbox_promote_s_bucket_representatives_v29__20260707`（8 files / 18MB）
  - `batch_48_kimi_inbox_promote_s_bucket_representatives_v33__20260707`（8 files / 18MB）
  - `batch_49_kimi_inbox_promote_s_bucket_representatives_v20__20260707`（8 files / 17MB）
  - `batch_50_kimi_inbox_promote_s_bucket_representatives_v44__20260707`（8 files / 16MB）
  - `batch_51_kimi_inbox_promote_s_bucket_representatives_v17__20260707`（8 files / 16MB）
  - `batch_52_kimi_inbox_promote_s_bucket_representatives_v5__20260707`（8 files / 15MB）
  - `batch_53_kimi_inbox_promote_s_bucket_representatives_v27__20260707`（8 files / 14MB）
  - `batch_54_kimi_inbox_promote_s_bucket_representatives_v8__20260707`（8 files / 14MB）
  - `batch_55_kimi_inbox_promote_s_bucket_representatives_v46__20260707`（8 files / 12MB）
  - `batch_56_kimi_inbox_promote_s_bucket_representatives_v47__20260707`（8 files / 12MB）
  - `batch_57_kimi_inbox_promote_s_bucket_representatives_v4__20260707`（8 files / 12MB）
  - `batch_58_kimi_inbox_promote_s_bucket_representatives_v42__20260707`（8 files / 11MB）
  - `batch_59_kimi_inbox_promote_s_bucket_representatives_v43__20260707`（8 files / 10MB）
  - `batch_60_kimi_inbox_promote_s_bucket_representatives_v1__20260707`（6 files / 8MB）
  - `batch_61_kimi_inbox_promote_s_bucket_representatives_v48__20260707`（5 files / 15MB）
  - `batch_62_kimi_inbox_promote_s_bucket_representatives_v41__20260707`（6 files / 18MB）
  - `batch_63_kimi_inbox_promote_s_bucket_representatives_v45__20260707`（7 files / 15MB）
  - `batch_64_kimi_inbox_promote_s_bucket_representatives_v2__20260707`（7 files / 25MB）
  - `batch_65_kimi_inbox_promote_s_bucket_representatives_v52__20260707`（2 files / 10MB）
  - `batch_66_kimi_inbox_promote_auction_course_04_zhuxuan__20260707`（3 files / 2.9MB）
  - `batch_67_kimi_inbox_promote_auction_course_05_fengye__20260707`（5 files / 1.4MB）
  - `batch_69_kimi_inbox_promote_auction_course_07_zhoushangren__20260707`（4 files / 0.2MB）
  - `batch_70_kimi_inbox_promote_auction_course_02_laojiang__20260707`（4 files / 0.2MB）
  - `batch_71_kimi_inbox_promote_auction_course_10_shouban__20260707`（6 files / 0.2MB）
  - `batch_73_kimi_inbox_promote_auction_course_03_laobanzhang__20260707`（3 files / 0.1MB）
  - `batch_74_kimi_inbox_promote_auction_course_01_basic_rules__20260707`（1 files / 0.1MB）
  - `batch_76_kimi_inbox_promote_auction_course_08_fanbo__20260707`（3 files / 0.07MB）
  - `batch_77_kimi_inbox_promote_auction_course_09_daiqiang__20260707`（6 files / 0.07MB）
  - `batch_78_kimi_inbox_promote_auction_course_06_zhangxinyuan__20260707`（3 files / 0.03MB）
  - `batch_80_kimi_inbox_promote_v25_ml__20260707`（3 files / 9.4MB）
  - `batch_81_kimi_inbox_promote_v25_hft_microstructure__20260707`（2 files / 4.5MB）
  - `batch_82_kimi_inbox_promote_v25_multifactor__20260707`（3 files / 4.4MB）
  - `batch_83_kimi_inbox_promote_group09_cutpack_products__20260707`（42 files / 1.8MB）
  - `batch_84_kimi_inbox_promote_group01_f2_cutpack_final__20260707`（10 files / 0.5MB）
  - `batch_85_kimi_inbox_promote_group06_a2_cutpack_v2_final__20260707`（10 files / 0.4MB）
  - `batch_86_kimi_inbox_promote_group05_f1_cutpack_v2_final__20260707`（9 files / 0.3MB）
  - `batch_87_kimi_inbox_promote_group10_a5_fin_statement_valuation__20260707`（7 files / 0.3MB）
  - `batch_88_kimi_inbox_promote_root_misc__20260707`（10 copied / 0.3MB; 25 already existed）
  - `batch_89_kimi_inbox_promote_group06_a2_cutpack_v2__20260707`（6 files / 0.2MB）
  - `batch_90_kimi_inbox_promote_group04_stat_arb_ml__20260707`（3 files / 0.1MB）
  - `batch_91_kimi_inbox_promote_group06_market_profile_root__20260707`（3 files / 0.1MB）
  - `batch_92_kimi_inbox_promote_group05_trend_system_root__20260707`（3 files / 0.1MB）
  - `batch_93_kimi_inbox_promote_group01_microstructure_root__20260707`（3 files / 0.1MB）
  - `batch_94_kimi_inbox_promote_group02_options_volatility_root__20260707`（3 files / 0.1MB）
  - `batch_95_kimi_inbox_promote_group03_portfolio_risk_root__20260707`（3 files / 0.05MB）
  - `batch_96_kimi_inbox_promote_group07_history_story_root__20260707`（1 files / 0.03MB）
  - `batch_97_kimi_inbox_duplicate_target_fill__20260707`（59 files / 39.6MB）
  - `batch_98_kimi_inbox_name_collision_target_fill__20260707`（22 files / 1.7MB）

## What Is Not Yet Aligned (Needs Reclassification / Decision)

- `10_来源库_SOURCE_LIBRARY` 的非 `01_Kimi拆书待入库` 部分（937 文件）：已归档到 `10_source_library_archive/_raw_snapshot_batch09`，但仍需要按批次去重与重分类，才能进入“可持续维护”的归档层。
- `11_冻结总结层_FROZEN_SUMMARIES`（44 文件）：已归档到 `11_frozen_summaries_archive/_raw_snapshot_batch09`，仍需要去乱码/去重复后再按批次迁入可读归档层。
- `tools/`（47 文件）：已归档到 `20_tools_workspace/_raw_snapshot_batch09`，仍需要按 KEEP/COPY/NEW 分流后再进入 `20_tools_workspace` 可维护层。
- `data/`（210 文件）：已归档到 `00_assets/_raw_snapshot_batch09`，仍需要资产归属口径与 provenance 后再进入长期资产层。
- `docs/`（10 文件）：已归档到 `12_tooling_runtime_archive/batch_08_legacy_docs_backlog__20260706/legacy_docs_backlog`，仍需要后续“入口卡+归属说明”裁决。
- `.trae` 非精选部分（31 文件）：已归档到 `21_trae_system_archive/_raw_snapshot_batch09/.trae`，`batch_01_selected/batch_02_selected` 仍是“精选可用子集”。

## Next Closure Items

- `source_library_mirror` 已清零；后续只需保留 duplicate/collision 审单作为裁决证据，不再阻塞旧来源库对齐口径。
- `source_library_raw_snapshot` 下一步已切成目录级推进：`non_kimi_raw_snapshot_prefix_summary__20260707.tsv` 将 937 files 压成 7 个顶层前缀；第一顺位先处理 `00_TK外汇`、`00_外部公开资料与方法论参考`、`02_原子化拆解文件` 的默认入口与最小搬迁清单。
- 上述第一顺位三目录已分别建立批次入口卡：`batch_99_non_kimi_tkfx_boundary__20260707`、`batch_100_non_kimi_public_methods_boundary__20260707`、`batch_101_non_kimi_atomic_rules_boundary__20260707`。
- 其中 `batch_100` 已完成第一轮目录治理，并已产出两个长期维护包：
  - `batch_107_non_kimi_public_batch9_bundle__20260707`（9 files；`research_contract_ready / reopen_ready`）
  - `batch_108_non_kimi_nftradez_method_bundle__20260707`（8 files；`method_reference_bundle`）
- `batch_100` 本轮继续推进出第三个长期维护包：
  - `batch_109_non_kimi_smile_smc_method_bundle__20260707`（6 files；`method_reference_bundle`）
- `00_外部公开资料与方法论参考` 当前已形成：
  - `Batch9` 作为正式吸收包入口
  - `NFTRADEZ` 作为方法参考稳定包入口
  - `Smile_SMC交易系统2_0` 作为方法参考稳定包入口
- 为收口 Markdown 语言服务报错，已清理 `00_外部公开资料与方法论参考` 活跃区中的旧 `file:///d:/Stock/trading_analysis/...` 绝对链接，并补了 VSCode settings 模板中的 trace / archive exclude 建议。
- 其中 `batch_101` 已完成第一轮目录治理：`02_原子化拆解文件` 已补默认主入口、默认索引入口、最小搬迁清单，后续可直接按 `多周期KD -> RSJ -> 高频价量相关性 -> 四轴状态模板 -> VanTharp` 顺序拆成对象束。
- 其中 `多周期KD` 已先落成首个非 Kimi 原子对象包：`batch_102_non_kimi_atomic_kd_mtf_bundle__20260707`（7 files，分成 `rules / objects / contracts` 三层，raw snapshot 原位保留不动）。
- 同轮已继续落四个对象包：`batch_103_non_kimi_atomic_rsj_state_bundle__20260707`、`batch_104_non_kimi_atomic_pv_corr_bundle__20260707`、`batch_105_non_kimi_atomic_four_axis_state_bundle__20260707`、`batch_106_non_kimi_atomic_vantharp_r_bundle__20260707`。
- 其中 `batch_103` 与 `batch_104` 已升级为第二层可验证包：从旧 runtime 快照吸入 `min_contract + proof_of_mapping + fields_output_header + runtime_notes + proof_input/output samples`，当前口径为 `diag-only / proof-ready / contract-frozen`。
- `batch_105` 与 `batch_106` 也已升级为第二层可验证包：`batch_105` 由对象入口补出最小 `contract + proof + samples`；`batch_106` 从旧 runtime 快照吸入 `min_contract + proof_of_mapping + v2 field header + proof_input/output samples`。至此 `02_原子化拆解文件` 已形成 `1` 个成包对象束加 `4` 个第二层可验证包。
- 为 `10_source_library_archive/_raw_snapshot_batch09`、`11_frozen_summaries_archive/_raw_snapshot_batch09`、`00_assets/_raw_snapshot_batch09`、`20_tools_workspace/_raw_snapshot_batch09` 定义“批次入口卡 + 去重/裁决表”，再逐批迁入。
