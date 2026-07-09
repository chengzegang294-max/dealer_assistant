# Trae System Archive

## 用途

- 这里放从旧 `.trae` 中迁入后仍有系统级作用的材料。
- 包括：
  - 技能定义
  - 恢复稿
  - 关键提示模板

## 迁入原则

- 只迁仍会继续在新仓库使用的系统材料
- 迁入后必须能说清：
  - 是技能
  - 还是恢复稿
  - 还是系统提示
- 一次性残留和旧问题临时稿默认不迁

## 当前状态

- 当前只建层级，不直接复制 `.trae` 全部内容。
- 本目录是 repo 内部归档与迁移索引层，不作为当前 first-hop 入口。
- 当前 skill 查找顺序固定为：`active router -> decision index -> group router -> legacy archive`
- 当前旧 skill 全量清单、迁移裁决与入口规则已统一收口到：
  - `SKILLS_INDEX.md`
- 当前 agent prompt 归档入口继续看：
  - `batch_02_selected\p0-exec-evidence-officer_PROMPT.md`
- 当前 recover 镜像入口继续看：
  - `batch_01_selected\`
- `batch_01_selected / batch_02_selected` 的正文实体已同步吸收到：
  - `10_source_library_archive\batch_131_trae_system_selected_absorb__20260709\`
- 首两批迁移台账已冻结到：
  - `11_frozen_summaries_archive\batch_130_trae_system_transition__20260709\`
- 当前仓内仍无 `.trae\commands` 实体目录：
  - 不单列 command router
  - 不伪造命令副本或命令索引壳

## 四分流入口

- `active router`
  - `.trae\README.md`
  - `.trae\skills\INDEX.md`

- `recover`
  - `21_trae_system_archive\batch_01_selected\README.md`
- `prompt`
  - `21_trae_system_archive\batch_02_selected\p0-exec-evidence-officer_PROMPT.md`
- `skill decision`
  - `21_trae_system_archive\SKILLS_INDEX.md`
- `skill group router`
  - `21_trae_system_archive\SKILLS_GROUP_VIEW.md`
- `legacy archive`
  - `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\README__ARCHIVE_ONLY.md`
- 固定三跳顺序：
  - `active router -> decision index -> group router -> legacy archive`
