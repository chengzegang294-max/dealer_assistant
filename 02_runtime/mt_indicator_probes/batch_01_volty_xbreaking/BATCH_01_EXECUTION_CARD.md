# Probe Batch 01 Execution Card

## 目标

- 把 `Volty / XBreaking` 从“只有模板”推进到“有统一落盘口径的首批 probe 批次”。
- 当前批次只收集平台可用性与 buffer 观察证据，不改默认执行链路。

## 对象范围

- `Volty`
  - 平台：`MT4`
  - 入口：`MT4Probe_Volty.mq4`
  - 指标本体：`VoltyChannel_Stop_v2_1M.mq4/.ex4`
- `XBreaking`
  - 平台：`MT5`
  - 入口：`XBreakingProbe.mq5`
  - 指标本体：`XBreaking.ex4/.ex5`

## 源锚点

- 代码锚点：
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\MT4Probe_Volty.mq4`
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreakingProbe.mq5`
- 文档锚点：
  - `03_docs\mt_indicator_engineering\volty_probe_result_intake_v1.md`
  - `03_docs\mt_indicator_engineering\xbreaking_buffer_semantics_log_v1.md`

## 建议产物目录

- `artifacts\volty\csv`
- `artifacts\volty\log`
- `artifacts\volty\tester_report`
- `artifacts\xbreaking\csv`
- `artifacts\xbreaking\log`
- `artifacts\xbreaking\tester_report`
- `artifacts\xbreaking\validation_matrix`
- 以上目录已在新仓库创建，可直接回收第一批实跑产物

## 首次实跑操作卡

- 参考：
  - `MT4_MT5_FIRST_RUN_PLAYBOOK.md`
- 辅助脚本：
  - `probe_artifact_ingest_v1.py`
  - `probe_batch_acceptance_v1.py`
- `Volty DumpSeries` 批次模板：
  - `MT4Probe_Volty_dumpseries_0_6.ini`
  - `mt4probe_volty_dumpseries_portable.ini`
- 当前口径：
  - 旧批次 `ini` 只作为字段与参数范围参考
  - 新仓库默认以本批目录为产物回收根

## Volty DumpSeries 快捷入口

- 最短复制路径：
  - `MT4Probe_Volty_dumpseries_0_6.ini` -> 终端 `tester\MT4Probe_Volty.ini`
  - `mt4probe_volty_dumpseries_portable.ini` -> 终端 `config\`
- 已固定参数：
  - `DumpSeries=1`
  - `DumpModeStart=0`
  - `DumpModeEnd=6`
  - `EURUSD / H1 / Open prices only / 2025.01.01 -> 2025.01.15`
- 跑完立即验收：
  - `python probe_artifact_ingest_v1.py --family volty --kind csv --copy-latest`
  - `python probe_artifact_ingest_v1.py --family volty --kind csv --normalize-volty-series`
  - `python probe_batch_acceptance_v1.py --json-only`

## 证据合同

- `Volty` 最少记录：
  - `symbol`
  - `chart_tf`
  - `indicator_tf`
  - `indicator_name`
  - `max_modes`
  - `max_shifts`
  - `used_common`
  - 每个 `mode` 的 `non_empty / err_count / first_valid / last_valid`
  - 规范化输出（新仓库内）：
    - `python probe_artifact_ingest_v1.py --family volty --kind csv --normalize-volty-summary`
  - series 输出（若开启 `DumpSeries`）：
    - `python probe_artifact_ingest_v1.py --family volty --kind csv --normalize-volty-series`
- `XBreaking` 最少记录：
  - `symbol`
  - `chart_tf`
  - `indicator_tf`
  - `indicator_name`
  - `bars_to_probe`
  - `max_buffers`
  - `handle`
  - `init_err`
  - 每个 `buffer` 的 `copied / err / non_empty / first_valid / last_valid`

## 文件命名口径

- `Volty CSV`
  - `MT4_probe_Volty_<SYMBOL>_<TF>_<STAMP>.csv`
- `XBreaking CSV`
  - `XBreaking_probe_<SYMBOL>_<TF>_<STAMP>.csv`
- `STAMP`
  - 使用平台脚本默认输出的时间戳，不手工改名

## 当前执行状态

- `Volty`
  - `status`: `fresh_run_dumpseries_closed`
  - `note`: 已补齐 `EURUSD/H1/DumpSeries=1` 的 `csv + tester report + tester log` fresh-run，并已完成 `series -> field row` 归一化闭环
- `XBreaking`
  - `status`: `fresh_run_and_validation_matrix_closed`
  - `note`: 已补齐批次级 `csv + tester report + terminal log + tester log` fresh-run，并完成多 symbol / timeframe / date window validation_matrix
  - `note_env`: 当前本机已确认 `2` 套 `MT5` 环境，环境标签为 `ICMarketsSC-Demo__52886989` 与 `TradeMaxGlobal-Demo__60088394`
  - `note_env_discovery`: `probe_mt_environment_inventory.ps1` 当前已支持 `origin.txt` 与目录结构双路径发现；若后续出现没有 `origin.txt` 的 `MT5 data_root`，inventory 也会以 `discovery_mode=structure_only` 记录候选，避免第二环境因缺少 `origin.txt` 被漏扫
  - `note_env_symbols`: 已补齐 `SymbolsTotal/SymbolName` 的真实品种清单导出（MarketWatch 与 AllSymbols），回收路径为 `environment_snapshots\mt5_symbols_*__<environment_label>__*.txt`，用于 broker alias 探测与跨环境对照前置盘点
  - `note_selector`: rerun / matrix 入口现已支持 `DataRootOverride` 与 `EnvironmentInventoryJson + EnvironmentSelector`
  - `note_index`: `validation_matrix_index_latest.json` 当前可直接总览各 archive 的 `symbol / timeframe / environment / manifest`
  - `note_cross_environment`: `validation_matrix_index_latest.json` 当前会额外给出 `inventory_mt5_environment_count / inventory_mt5_environment_labels / validation_matrix_environment_label_count / validation_matrix_environment_labels / cross_environment_ready / cross_environment_verified`，用于把“第二环境是否已就绪、是否已完成跨环境实跑”显式化
  - `note_cross_environment_seed`: `validation_matrix_index_latest.json` 当前会额外产出 `recommended_cross_environment_seed_*`，用于从现有 archive 中自动挑选更适合做第二环境对照的代表样本，而不是简单使用最新 archive；当前推荐 seed 已切到 `usidx_h4_tmgm_longwin_20260703T0248`
  - `note_cross_environment_bootstrap`: `probe_batch_acceptance_v1.py` 的 `operator_shortcuts` 当前已内置 `xbreaking_cross_environment_bootstrap`，提供“刷新 inventory -> 按第二环境 selector 复跑 -> fallback 到 InstallRoot + DataRootOverride”的最短闭环命令模板，且模板参数会优先跟随 `recommended_cross_environment_seed_*`；当前模板已随 index 自动切到 `USIDX/H4`
  - `note_cleanup`: 已清理失败遗留空 archive `eurusd_h4_jan0310_20260701T124043_window_a`（清理结论仍有效）；当前 matrix archive 数为 `90`
  - `note_manifest_backfill`: 已对历史 `validation_matrix` 归档批量补齐 `ingest_manifest.json`（标记为 `historical_recovered`）；当前 `manifest_archive_count = archive_count = 90`
  - `note_env_inference`: 对缺失 `environment` 字段的旧 `run_summary.json`，当前 `validation_matrix_index_latest.json` 会从 `run_summary.files.*.source` 提取 `MetaQuotes\\Terminal\\<hash>` 并结合 `environment_snapshots\\mt_environment_inventory_latest.json` 推断环境字段，标记 `environment_inferred=true`
  - `note_selection_mode_gap`: 当前 `validation_matrix_index_latest.json` 会统计 `selection_mode_missing_count` 并列出 `selection_mode_missing_archive_tags`，用于明确哪些 archive 仍缺“环境选择方式”信息
  - `note_manifest_provenance`: 当前 `validation_matrix_index_latest.json` 会统计 `manifest_source_backed_archive_count / manifest_full_source_backed_archive_count / manifest_mixed_provenance_archive_count / manifest_repo_existing_only_archive_count`，用于快速判断 manifest 的 source 可追溯程度
  - `note_selection_mode_hard`: 已补齐 selection_mode 硬证据归档：`eurusd_h4_envselect_hard_20260701T1426`（inventory_selector）、`eurusd_h4_override_hard_20260701T1426`（data_root_override）、`gbpusd_h4_envselect_hard_20260701T1535`（inventory_selector）、`gbpusd_h4_override_hard_20260701T1535`（data_root_override）、`usdjpy_h1_envselect_hard_20260701T1608`（inventory_selector）、`usdjpy_h1_override_hard_20260701T1608`（data_root_override）
  - `note_date_window_robustness`: 已补齐更远日期窗 `2025.02.03~2025.02.10` 的复跑归档：`eurusd_h4_envselect_feb_20260701T1615`（EURUSD/H4）、`usdjpy_h1_envselect_feb_20260701T1625`（USDJPY/H1）
  - `note_long_window_robustness`: 已新增更长窗口复跑归档 `eurusd_h4_envselect_longwin_20260702T0038`（EURUSD/H4，`2024.12.01~2025.03.01`，inventory_selector）、`usdjpy_h1_envselect_longwin_20260702T0041`（USDJPY/H1，`2024.12.01~2025.03.01`，inventory_selector）、`xauusd_h4_envselect_longwin_20260702T0044`（XAUUSD/H4，`2024.12.01~2025.03.01`，inventory_selector）与 `us30_h4_envselect_longwin_20260702T0054`（US30/H4，`2024.12.01~2025.03.01`，inventory_selector），用于继续验证 `buffer0_only` 是否在跨月长窗口下仍稳定成立，且该结论已跨外汇、黄金与股指品种复现
  - `note_cross_environment_verified`: 已新增 `us30_h4_tmgm_longwin_20260702T0137`（US30/H4，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`）、`eurusd_h4_tmgm_longwin_20260702T0143`（EURUSD/H4，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`）、`usdjpy_h1_tmgm_longwin_20260702T0145`（USDJPY/H1，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`）、`gbpusd_h4_tmgm_longwin_20260702T0147`（GBPUSD/H4，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`）、`xauusd_h4_tmgm_longwin_20260702T0152`（XAUUSD/H4，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`）、`eurusd_h1_tmgm_longwin_20260702T0202`（EURUSD/H1，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`）、`usdjpy_h4_tmgm_longwin_20260702T0210`（USDJPY/H4，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`）、`us30_h1_tmgm_longwin_20260702T0222`（US30/H1，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`）、`xauusd_h1_tmgm_longwin_20260702T0234`（XAUUSD/H1，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`）、`gbpusd_h1_tmgm_longwin_20260702T0250`（GBPUSD/H1，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`）、`xagusd_h1_tmgm_longwin_20260702T0302`（XAGUSD/H1，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`）、`xagusd_h4_tmgm_longwin_20260702T0315`（XAGUSD/H4，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`）、`nas100_h1_tmgm_longwin_20260702T0332`（NAS100/H1，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`）、`nas100_h4_tmgm_longwin_20260702T0346`（NAS100/H4，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`）、`xtiusd_h1_tmgm_longwin_20260702T0406`（XTIUSD/H1，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`）、`xtiusd_h4_tmgm_longwin_20260702T0418`（XTIUSD/H4，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`）、`us500_h1_tmgm_longwin_20260702T1925`（US500/H1，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`）与 `us500_h4_tmgm_longwin_20260702T1926`（US500/H4，`2024.12.01~2025.03.01`，inventory_selector，`TradeMaxGlobal-Demo__60088394`），当前 acceptance 已确认 `inventory_mt5_environment_count = 2`、`validation_matrix_environment_label_count = 2`、`cross_environment_ready = true`、`cross_environment_verified = true`，主线已从“第二环境阻塞”推进到“跨环境硬证据闭环”，且第二环境结论已扩展到外汇主对 H4/H1、日系 H1/H4、英镑 H4/H1、黄金 H1/H4、白银 H1/H4、股指 H1/H4 与原油别名商品 H1/H4 样本
  - `note_cross_environment_verified_latest`: 本轮再新增 `ger40_h1_tmgm_longwin_20260702T1932`（GER40/H1）与 `ger40_h4_tmgm_longwin_20260702T1933`（GER40/H4），把德指样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `GER40/H4`
  - `note_cross_environment_verified_audusd`: 本轮再新增 `audusd_h1_tmgm_longwin_20260702T2022`（AUDUSD/H1）与 `audusd_h4_tmgm_longwin_20260702T2024`（AUDUSD/H4），把旧仓 `audusd_1h.csv` 对应的外汇样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `AUDUSD/H4`
  - `note_cross_environment_verified_usdchf`: 本轮再新增 `usdchf_h1_tmgm_longwin_20260702T2034`（USDCHF/H1）与 `usdchf_h4_tmgm_longwin_20260702T2035`（USDCHF/H4），把旧仓 `usdchf_1h.csv` 对应的外汇样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `USDCHF/H4`
  - `note_cross_environment_verified_usdcad`: 本轮再新增 `usdcad_h1_tmgm_longwin_20260702T2110`（USDCAD/H1）与 `usdcad_h4_tmgm_longwin_20260702T2111`（USDCAD/H4），把旧仓 `usdcad_1h.csv` 对应的外汇样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `USDCAD/H4`
  - `note_cross_environment_verified_nzdusd`: 本轮再新增 `nzdusd_h1_tmgm_longwin_20260702T2128`（NZDUSD/H1）与 `nzdusd_h4_tmgm_longwin_20260702T2129`（NZDUSD/H4），把旧仓 `nzdusd_1h.csv` 对应的外汇样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `NZDUSD/H4`
  - `note_cross_environment_verified_eurjpy`: 本轮再新增 `eurjpy_h1_tmgm_longwin_20260702T2144`（EURJPY/H1）与 `eurjpy_h4_tmgm_longwin_20260702T2145`（EURJPY/H4），把旧仓 `eurjpy_1h.csv` 对应的外汇样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `EURJPY/H4`
  - `note_cross_environment_verified_gbpjpy`: 本轮再新增 `gbpjpy_h1_tmgm_longwin_20260702T2203`（GBPJPY/H1）与 `gbpjpy_h4_tmgm_longwin_20260702T2204`（GBPJPY/H4），把旧仓 `gbpjpy_1h.csv` 对应的外汇样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `GBPJPY/H4`
  - `note_cross_environment_verified_eurgbp`: 本轮再新增 `eurgbp_h1_tmgm_longwin_20260702T2220`（EURGBP/H1）与 `eurgbp_h4_tmgm_longwin_20260702T2221`（EURGBP/H4），把旧仓 `EURGBP_1h.csv` 对应的外汇样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `EURGBP/H4`
  - `note_cross_environment_verified_chfjpy`: 本轮再新增 `chfjpy_h1_tmgm_longwin_20260702T2233`（CHFJPY/H1）与 `chfjpy_h4_tmgm_longwin_20260702T2234`（CHFJPY/H4），把旧仓 `CHFJPY_1h.csv` 对应的外汇样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `CHFJPY/H4`
  - `note_cross_environment_verified_eurchf`: 本轮再新增 `eurchf_h1_tmgm_longwin_20260702T2247`（EURCHF/H1）与 `eurchf_h4_tmgm_longwin_20260702T2248`（EURCHF/H4），把旧仓 `EURCHF_1h.csv` 对应的外汇样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `EURCHF/H4`
  - `note_cross_environment_verified_audnzd`: 本轮再新增 `audnzd_h1_tmgm_longwin_20260702T2310`（AUDNZD/H1）与 `audnzd_h4_tmgm_longwin_20260702T2311`（AUDNZD/H4），把旧仓 `AUDNZD_1h.csv` 对应的外汇样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `AUDNZD/H4`
  - `note_cross_environment_verified_cadjpy`: 本轮再新增 `cadjpy_h1_tmgm_longwin_20260702T2331`（CADJPY/H1）与 `cadjpy_h4_tmgm_longwin_20260702T2332`（CADJPY/H4），把旧仓 `CADJPY_1h.csv` 对应的外汇样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `CADJPY/H4`
  - `note_cross_environment_verified_euraud`: 本轮再新增 `euraud_h1_tmgm_longwin_20260702T2353`（EURAUD/H1）与 `euraud_h4_tmgm_longwin_20260702T2354`（EURAUD/H4），把旧仓 `EURAUD_1h.csv` 对应的外汇样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `EURAUD/H4`
  - `note_cross_environment_verified_gbpchf`: 本轮再新增 `gbpchf_h1_tmgm_longwin_20260703T0007`（GBPCHF/H1）与 `gbpchf_h4_tmgm_longwin_20260703T0008`（GBPCHF/H4），把旧仓 `GBPCHF_1h.csv` 对应的外汇样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `GBPCHF/H4`
  - `note_cross_environment_verified_eurnzd`: 本轮再新增 `eurnzd_h1_tmgm_longwin_20260703T0027`（EURNZD/H1）与 `eurnzd_h4_tmgm_longwin_20260703T0028`（EURNZD/H4），把旧仓 `EURNZD_1h.csv` 对应的外汇样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `EURNZD/H4`
  - `note_cross_environment_verified_audjpy`: 本轮再新增 `audjpy_h1_tmgm_longwin_20260703T0038`（AUDJPY/H1）与 `audjpy_h4_tmgm_longwin_20260703T0039`（AUDJPY/H4），把旧仓 `AUDJPY_1h.csv` 对应的外汇样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `AUDJPY/H4`
  - `note_cross_environment_verified_nzdjpy`: 本轮再新增 `nzdjpy_h1_tmgm_longwin_20260703T0115`（NZDJPY/H1）与 `nzdjpy_h4_tmgm_longwin_20260703T0116`（NZDJPY/H4），把旧仓 `NZDJPY_1h.csv` 对应的外汇样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `NZDJPY/H4`
  - `note_cross_environment_verified_xbrusd`: 本轮再新增 `xbrusd_h1_tmgm_longwin_20260703T0159`（XBRUSD/H1）与 `xbrusd_h4_tmgm_longwin_20260703T0200`（XBRUSD/H4），把旧仓 `UKOIL_1h.csv` 对应的 Brent 商品样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `XBRUSD/H4`
  - `note_cross_environment_verified_usidx`: 本轮再新增 `usidx_h1_tmgm_longwin_20260703T0247`（USIDX/H1）与 `usidx_h4_tmgm_longwin_20260703T0248`（USIDX/H4），把旧仓 `dollaridxusd_1h.csv` 对应的美元指数样本也纳入第二环境跨月长窗口硬证据，并推动 `recommended_cross_environment_seed_*` 自动切到 `USIDX/H4`
  - `note_symbol_alias`: 当前已补七条商品/附加资产旧命名或候选 alias 失败证据 `usoil_h1_tmgm_longwin_20260702T0400`、`ukoil_h1_tmgm_longwin_20260702T1918`、`xcuusd_h1_tmgm_longwin_20260702T1950`、`dollaridxusd_h1_tmgm_longwin_20260702T1959`、`coppercmdusd_h1_tmgm_longwin_20260703T0216`、`usdx_h1_tmgm_longwin_20260703T0222` 与 `dxy_h1_tmgm_longwin_20260703T0226`；TMGM 第二环境日志明确显示 `symbol USOIL not exist`、`symbol UKOIL not exist`、`symbol XCUUSD not exist`、`symbol DOLLARIDXUSD not exist`、`symbol COPPERCMDUSD not exist`、`symbol USDX not exist` 与 `symbol DXY not exist`，因此当前商品/附加资产主线不能继续把 `USOIL / UKOIL / XCUUSD / DOLLARIDXUSD` 及其这批候选 alias 当默认 tester symbol 使用；同时当前又新增 `xtiusd_h1_tmgm_longwin_20260702T0406` / `xtiusd_h4_tmgm_longwin_20260702T0418`、`xbrusd_h1_tmgm_longwin_20260703T0159` / `xbrusd_h4_tmgm_longwin_20260703T0200` 与 `usidx_h1_tmgm_longwin_20260703T0247` / `usidx_h4_tmgm_longwin_20260703T0248` 三组可用原油/Brent/美元指数别名样本，用于把 `USOIL` 收敛到 `XTIUSD`、把 `UKOIL` 收敛到 `XBRUSD`、把 `DOLLARIDXUSD` 收敛到 `USIDX`；另外 TMGM 公开 `Trading Hours` / `Swap Free Account` 页面把 `CHCUSD` 明确标成 `CHINA A50`，而公开 `Precious Metals` 页面只列 `XAUUSD / XAGUSD / XPTUSD`，因此 `CHCUSD` 也不能作为 `XCUUSD` 候选 alias
  - `note_index_alias`: 本轮新增 `ger30_h1_tmgm_longwin_20260702T1942` 失败别名证据；TMGM 第二环境 tester 日志明确显示 `symbol GER30 not exist`，因此旧仓 `GER30_1h.csv` 当前不能直接映射到 `GER30` tester symbol，而应优先收敛到已跑通的 `GER40/H1/H4` 对照链
-  - `note_currency_index_alias`: 已确认 TMGM 第二环境不存在 `GBRIDXGBP`（失败别名证据：`gbridxgbp_h1_tmgm_longwin_20260703T0125`），并通过 MT5 端 `SymbolsTotal/SymbolName` 导出锁定 broker alias 为 `UK100`；本轮新增 `uk100_h1_tmgm_longwin_20260703T111446`（UK100/H1）与 `uk100_h4_tmgm_longwin_20260703T111446`（UK100/H4）两组第二环境跨月长窗口硬证据，且 probe CSV 显示 `buffer0_only` 语义成立
  - `note_purchased_data_inventory`: 已新增 `PURCHASED_MARKET_DATA_INVENTORY.md`，把旧仓 `VTMarkets-Live 2` 下的 `HST` 历史数据以及 `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\` 根目录本层的已购 `CSV/XLSX` 一并固定成仓库事实，并额外补齐“资产-周期-消费状态映射”、“文件级映射”、“P1 文件的候选消费者/字段契约入口”、首批 `P1` 字段契约草案入口、商品 broker alias 备注以及已购 CSV 标准化预览归档（`p1_contract_preview_20260702T0428` 小样本、`p1_contract_preview_20260702T0702` 扩容版、`p1_contract_preview_20260702T1730` 预设入口版、`p2_contract_preview_20260703T1115` P2 批量入口版）；当前已确认 `VTMarkets-Live 2` 下外汇 `VIP` 历史文件 `113` 个、贵金属 `VIP` 历史文件 `17` 个、同目录股指 `.hst` 文件 `28` 个，同时 `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\` 根目录本层已有 `41` 个已购 `csv/xlsx`（外汇 `19`、贵金属 `3`、股指 `6`、商品 `5`、宏观 `8`），且 `EURUSD-VIP60.hst` 已被 `fill_mt4_eurusd_h1_history_v1.py` 实际消费；`audusd_1h.csv`、`usdchf_1h.csv`、`usdcad_1h.csv`、`nzdusd_1h.csv`、`eurjpy_1h.csv`、`gbpjpy_1h.csv`、`EURGBP_1h.csv`、`CHFJPY_1h.csv`、`EURCHF_1h.csv`、`AUDJPY_1h.csv`、`AUDNZD_1h.csv`、`CADJPY_1h.csv`、`EURAUD_1h.csv`、`GBPCHF_1h.csv`、`EURNZD_1h.csv`、`NZDJPY_1h.csv`、`nas100_1h.csv`、`us500_1h.csv`、`ger40_1h.csv`、`usoil_1h.csv`、`xtiusd_1h.csv`、`UKOIL_1h.csv` 与 `dollaridxusd_1h.csv` 当前都已拥有对应的第二环境主线对照样本或别名收敛样本；其中 `GBRIDXGBP_1h.csv` 已收敛为 `UK100`（`uk100_h1_tmgm_longwin_20260703T111446` / `uk100_h4_tmgm_longwin_20260703T111446`），`GER30_1h.csv` 当前仍属于“旧命名不可直接当 tester symbol 使用”的失败别名证据；而 `XCUUSD_1h.csv` 当前除旧命名失败外，也已经补齐 `COPPERCMDUSD` 候选 alias 的失败探测证据，并通过 TMGM 公共产品面排除了 `CHCUSD` 这条 `CHINA A50` 假候选；`_xau_test_1h.csv` 当前已在标准化层显式归一到 `XAUUSD/1H`；并已新增已购 CSV 标准化预览索引与验收快照：`artifacts\\purchased_csv_contract_preview\\purchased_csv_contract_preview_index_latest.json` 与 `acceptance_snapshots\\purchased_csv_contract_preview_acceptance_latest.json`
  - `note_crypto_onramp_recorded`: 已新增 `03_docs\mt_indicator_engineering\crypto_exchange_data_onramp_plan_v1.md`，先把 `Binance / OKX` 的币圈数据接入方案、字段契约、目录建议与分阶段范围固定进 repo；当前裁决是“先记录，不改现有 `MT5 / XBreaking` 默认主线”，后续若判断实现成本合适，可优先从 `Binance public REST -> BTCUSDT/ETHUSDT -> 1h/4h -> standardized contract` 起步

## 收口规则

- 第一批实际产物落盘后：
  1. 先更新本目录的产物索引
  2. 运行 `python probe_batch_acceptance_v1.py --json-only` 做批次级验收
  3. 同步检查验收快照里的 `xbreaking_validation_matrix` 节，确认最近 archive 的 `run_summary / ingest_manifest / selection_mode` 都已可见
  4. 同步检查 `artifacts\xbreaking\validation_matrix\validation_matrix_index_latest.json` 是否已刷新
  5. 再回写 `03_docs\mt_indicator_engineering` 对应 intake 文档
  6. 最后决定哪些字段可从 `template_only` 升到 `field_ready`
  7. 若通过 `probe_artifact_ingest_v1.py --archive-tag <tag>` 回收到 `validation_matrix`，同步检查该归档下是否已生成 `ingest_manifest.json`

## 禁止事项

- 不把 `Volty` probe 直接写成默认入场门控
- 不把 `XBreaking` 任一 buffer 未验证前直接标成买卖信号
- 不把 `ex4/ex5` 二进制存在，误写成“已拿到源码”
