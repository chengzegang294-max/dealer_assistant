# Full Repo Migration Map

## 目的

- 这份文件定义 `旧仓库` 到 `仓库根目录` 的总迁移地图。
- 目标不是复制旧仓库，而是把未来真正要继续维护的层级逐步迁入新仓库。

## 总体裁决

- `trading_analysis`
  - 继续保留为历史大仓库
  - 负责旧材料、旧路径、旧证据保留
- `trading_assistant`
  - 负责未来活跃工作
  - 只接收已筛选、已说明、已定责的材料

## 根目录映射

- 旧根目录活跃主文档：
  - `00_主线检索索引.md`
  - `01_阶段一_项目记录_过去与落地.md`
  - `02_阶段二_工作方向_想法库.md`
  - `03_阶段二_当下计划_执行清单.md`
  - `关于日活.md`
  - `PLAYBOOK_滚动模板.md`
  - `ashare_daily_ops.md`
- 新位置：
  - `04_active_main_docs`
- 规则：
  - 只迁仍有活跃维护价值的主文档
  - 不把旧根目录其他杂项直接平移

## `.trae` 映射

- 旧位置：
  - `.trae\`
- 新位置：
  - `21_trae_system_archive`
- 规则：
  - 只迁仍要继续使用的技能、恢复稿、提示材料
  - 不迁一次性残留或无后续用途内容

## 来源库映射

- 旧位置：
  - `10_来源库_SOURCE_LIBRARY\`
- 新位置：
  - `10_source_library_archive`
- 规则：
  - 只按批次迁入高价值、非重复、非乱码材料
  - 默认不整包复制

## 冻结总结层映射

- 旧位置：
  - `11_冻结总结层_FROZEN_SUMMARIES\`
- 新位置：
  - `11_frozen_summaries_archive`
- 规则：
  - 先做去乱码、去重复、保留总结锚点
  - 默认不整包复制

## 工具运行时映射

- 旧位置：
  - `12_工具运行时_TOOLING_RUNTIME\`
- 新位置：
  - `12_tooling_runtime_archive`
  - 或活跃对象对应的 `02_runtime`
- 规则：
  - 活跃对象真正运行中的最小集进入 `02_runtime`
  - 历史运行时材料按批次筛入 `12_tooling_runtime_archive`
  - 不整包复制旧运行时层

## 工具脚本映射

- 旧位置：
  - `tools\`
- 新位置：
  - `20_tools_workspace`
- 规则：
  - 只迁仍要继续维护和复用的工具
  - 历史一次性脚本先留在旧仓库

## `legacy_analysis`（旧库镜像）定位

- 位置：
  - `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\`
- 角色：
  - 旧仓库关键层的只读镜像与迁移工作区
  - 不再作为当前默认入口；只用于“吃透/对账/迁移/冻结”
- 规则：
  - 任何旧绝对路径示例，只允许作为 `ARCHIVE_ONLY / historical_recovered` 追溯字段
  - 任何删除/移动类脚本必须显式阻断，除非人工设置允许开关后刻意运行
- 近期止血动作（已做）：
  - `ROOT_VSCODE_SETTINGS_TEMPLATE.jsonc` 与 `pyrightconfig.json` 已改为 repo-first（不再把树外旧根写成默认解释器/venvPath；本机若需覆盖仅允许本机侧改动）
  - `DY_R1_KD_MTF_P0/README` 推荐命令切回本仓库路径
  - `DY_R1_KD_MTF_P0/kd_mtf_p0_runtime_params_template_v1.json` 的 `runtime_dir` 去除旧根绝对路径，改为 repo 内相对路径
  - `DY_R1_KD_MTF_P0/kd_mtf_p0_runtime_append_acceptance_v1.md` 的命令去除旧根绝对路径，改为 repo 内相对路径
  - `02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/run_volty_dumpseries_gui_once.ps1` 已移除对旧根的 fallback，改为要求显式设置 `MT4_PORTABLE_ROOT`
  - `docs/MT4_MT5_安装与数据目录定位_v1.md` 的 `mt_exports_drop` 推荐投递区去除旧根绝对路径，改为 repo 内相对路径
  - `docs/TK-R4_USD_half_risk_SchemeB_Quickstart.md` 的一键复跑命令去除旧根绝对路径，并增加 `ALLOW_ARCHIVE_ONLY_RUN` 明示开关
  - `docs/P0_规则子表_v0.1.md` 的来源字段去除旧根绝对路径，改为 repo 内真实文件路径
  - `docs/commit_ready_stage_batch_*` 不再 `Set-Location 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis`，改为定位到 `legacy_analysis` 根
  - `GROUP_08` 两个 `*dryrun*.ps1` 增加 `ALLOW_ARCHIVE_ONLY_RUN` 保险开关
  - `Batch9_reopen_n02_session_or_p0_v1` 下 `second_fx` 若干脚本把旧 `DATA_ROOT` 改为环境变量可覆盖（默认仍保留历史值）
  - `tools/group08_*` 系列脚本去除硬编码 `D:\Stock\cut_file`，并加装 `ALLOW_ARCHIVE_ONLY_RUN + CUT_FILE_ROOT` 显式开关
  - `tk_r4_usd_half_risk_scheme_b_runner.py` 加装 `ALLOW_ARCHIVE_ONLY_RUN` 显式开关
  - `12_工具运行时_TOOLING_RUNTIME/VTMarkets-Live 2` 原 tree-out junction 已移除，并改为 `ARCHIVE_ONLY` 指针（真实历史数据在 `12_tooling_runtime_archive/batch_05_legacy_mt4_probe_assets__20260706/.../VTMarkets-Live 2`）
  - `12_工具运行时_TOOLING_RUNTIME/pv_corr_state_p0_v1` 与 `rsj_state_p0_v1` 一组 acceptance/index 文档的旧根 `python d:\Stock\trading_analysis\...` 命令已改为 repo 内相对路径，并显式标注 `ARCHIVE_ONLY`
  - `11_冻结总结层_FROZEN_SUMMARIES` 中残留的旧根 `python d:\Stock\trading_analysis\...` 命令已统一改为 repo 内相对路径，并显式标注 `ARCHIVE_ONLY`
  - `Batch9_reopen_n02_session_or_p0_v1` 相关运行说明/验收文档中残留的旧根路径（如 `data`、`mt_exports_drop`、proof 复现命令）已逐步改为 `TRADING_ANALYSIS_DATA_ROOT` 或 repo 内相对路径，降低误把旧仓当默认入口的风险
  - `12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_trading_analysis/backtest_out` 已迁入 `12_tooling_runtime_archive/batch_04_legacy_backtest_out__20260706/backtest_out` 并在原位保留 `ARCHIVE_ONLY` 入口壳
  - `12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_trading_analysis/12_工具运行时_TOOLING_RUNTIME` 下的 `mt4_probe_instance` 与 `03_MT4便携探针实例/history` 已迁入 `12_tooling_runtime_archive/batch_05_legacy_mt4_probe_assets__20260706` 并在原位保留 `ARCHIVE_ONLY` 入口壳
  - `12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_trading_analysis/docs` 下的 `commit_ready_stage_batch_*.ps1` 与 `commit_ready_batch_*__paths.txt` 已迁入 `12_tooling_runtime_archive/batch_06_legacy_commit_helpers__20260706` 并补齐 `BATCH_06_EXECUTION_CARD/BATCH_06_ARTIFACT_INDEX`
  - `12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_trading_analysis/docs` 下的 `*__EVAL__*.md` 与 `COMMIT_READY__BATCH_*.md` 已迁入 `12_tooling_runtime_archive/batch_07_legacy_docs_batches__20260706` 并在原位落盘迁移说明卡
  - `12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_trading_analysis/run_p0_sweep.ps1` 已切到 `ARCHIVE_ONLY + 显式开关` 模式，默认阻断旧根依赖
  - `12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_trading_analysis/docs` 下的 backlog/职责说明/阶段性批次审阅等历史文档已迁入 `12_tooling_runtime_archive/batch_08_legacy_docs_backlog__20260706` 并在原位落盘迁移说明卡

## 当前优先顺序

1. 旧主文档第二轮清理与 `04_active_main_docs` 镜像承接
2. `10_source_library_archive` 继续按“先吃透、再迁入”的批次方式推进；当前来源库主刀维持 `S_BUCKET_02` 的 `YZ-A / YZ-B` 对象级真值锚点与主题簇证据增强，不扩新书、不升级成硬门控
3. `20_tools_workspace` 保持 `PY-04 = tk_r6~r8` 手工表家族的新仓维护态；`Batch9` 当前已完成 `runtime/ref-check` 与 `GBPUSD/M15 slice downstream + or_break_only beyond multi-session persistence` 收口，停点固定 `gbpusd_m15_slice_downstream_plus_or_break_only_beyond_multi_session_persistence_done_without_failed_breakout`，继续保持 `NO failed breakout` 与 Hold
4. `12_tooling_runtime_archive` 与活跃对象 runtime 家族按对象入口分批迁入
5. `21_trae_system_archive` 继续补合适 skill 副本
6. 每一批都同步旧仓库进度板与旧主文档清理任务板
