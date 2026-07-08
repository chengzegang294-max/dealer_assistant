# trading_assistant

## Root Notes

- 根目录备注说明见 `ROOT_NOTES.md`
- 运行产物、脚本与备注说明的固定合同见 `00_entry\ARTIFACT_NOTE_CONTRACT.md`
- 旧仓库全场扫库与迁移任务板见 `00_entry\OLD_REPO_FILE_SWEEP_TASKBOARD.md`
- 当前“继续迁移到新仓库 + 继续全量吃透旧仓库”的统一主线规划见 `00_entry\MAINLINE_FULL_INGEST_AND_MIGRATION_PLAN__2026-06-26.md`
- `原件层` 三阶段退场与外部残余收口计划见 `00_entry\CUT_FILE_RETIREMENT_PLAN__2026-06-26.md`

## 用途

- 这是新的独立工作根目录。
- 目标是从零开始搭建一个干净、可持续扩展、可量化的工作空间。
- 旧目录当前全部冻结保留，不在这里直接继承旧混乱结构。

## 当前阶段

- 当前已建立活跃对象层、受控归档层和系统层。
- 当前不做旧仓库整包复制。
- 后续所有迁移都按“先定义边界，再按批次纳入”的顺序执行。
- 当前环境口径已统一：
  - 工作区根目录使用 `d:\Stock\trading_assistant`
  - 默认入口保持 repo-first：不把任何树外绝对路径写成“可复制即跑”的主线入口
- 当前判断：
  - 旧仓库仅作为历史溯源真源（ARCHIVE_ONLY）
  - 新仓库已进入“结构承接 + 主文档镜像承接 + 运行时批次承接”维护态
  - 若你本机需要复用旧环境（例如旧 `.venv`），只允许作为本机覆盖，不写入仓库默认入口与合同

## 目录骨架

- `00_entry`
  - 放总入口、迁移原则、结构声明
- `01_active_objects`
  - 放已经裁定为活跃对象的最小对象包
- `02_runtime`
  - 放运行时脚本、参数、样本、产物
  - 当前已新增 `mt_indicator_probes`，用于 `Volty / XBreaking` 首批 probe 批次落盘
- `03_docs`
  - 放当前活跃文档与阶段说明
- `04_active_main_docs`
  - 放从旧根目录迁入的新活跃主文档，不继续长期依赖旧根目录
- `10_source_library_archive`
  - 放按批次筛选后迁入的新来源库副本，不放整包来源库
- `11_frozen_summaries_archive`
  - 放按批次筛选后迁入的冻结总结副本，不放整包冻结层
- `12_tooling_runtime_archive`
  - 放按批次筛选后迁入的旧工具运行时材料，不放整包运行时目录
- `20_tools_workspace`
  - 放迁入后仍要继续维护的通用工具脚本
- `21_trae_system_archive`
  - 放 `.trae` 中值得保留的技能、恢复稿、系统提示副本
- `99_inbox`
  - 放尚未裁定、暂存、待分流材料

## 当前不做

- 不把 `trading_analysis` 全量复制进来。
- 不把来源库、冻结层、历史备份整包搬进来。
- 不把旧目录里的临时文件、乱码备份、无职责目录直接带进来。

## 归档原则

- 受控层不是历史仓库镜像。
- 当前受控层包括：
  - `10_source_library_archive`
  - `11_frozen_summaries_archive`
  - `12_tooling_runtime_archive`
  - `20_tools_workspace`
  - `21_trae_system_archive`
- 这些层只允许进入：
  - 已确认有价值
  - 非乱码
  - 非重复
  - 已写清迁入理由与后续职责
- 任何未完成筛选与说明的旧材料，继续留在 `trading_analysis`，不直接进入新目录。

## 当前已落地批次

- `11_frozen_summaries_archive`
  - 已完成首批实筛并迁入 `4` 份冻结总结锚点
- `04_active_main_docs`
  - 已完成首批迁入 `7` 份根目录主文档锚点
- `21_trae_system_archive`
  - 已完成首批迁入 `7` 份 `.trae` 恢复锚点
  - 已完成第二批迁入 `1` 份本地可见 agent prompt
- `20_tools_workspace`
  - 已完成首批迁入 `4` 个通用工具脚本
  - 已完成第二批迁入 `1` 组 `group08` 主流水线脚本
- `12_tooling_runtime_archive`
  - 已完成首批迁入一套 `cross_line_frozen` 顶层最小冻结链
  - 已完成第二批迁入一组 `MT 指标家族最小工程集`
- `02_runtime`
  - 已补 `mt_indicator_probes/batch_01_volty_xbreaking` 运行时批次包
  - 已补 `MT4_MT5_FIRST_RUN_PLAYBOOK.md` 与首批 probe 回收目录

## 当前阻塞

- 旧仓库默认入口已退出，当前只剩维护态止血与历史快照清理，不再存在未收口的迁移批次数。
- 新仓库镜像层已完成主入口承接；当前工作重点转为维护态同步、对象级真值增强与 legacy 残余默认入口清理。
- `MT` 子线当前仍有两个明确缺口：
  - `Volty` 缺 `DumpSeries=1` 的 fresh-run CSV
  - `XBreaking` 缺 tester `.htm` report

## 第一原则

- 这里只有两类东西可以进来：
  - 当前主线明确需要
  - 进入后放置位置和职责已经说清楚
- 任何不能说明“为什么进来、进来后放哪、由谁维护”的内容，先留在旧仓库，不进入本目录。
