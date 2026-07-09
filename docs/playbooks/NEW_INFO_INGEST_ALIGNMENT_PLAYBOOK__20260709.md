# New Info Ingest Alignment Playbook

## TEMPLATE_ID: NEW_INFO_INGEST_ALIGNMENT

- `VERSION`: `v1`
- `SCOPE`:
  - 适用于新进入仓库的电子书、视频、文章、研报、网页摘录、运行产物、配置模板与历史回收材料
  - 不适用于已经明确属于当前活跃 runtime 且只需小修的紧急代码变更
- `INPUT`:
  - 新资料或新产物本体
  - 现有目录角色合同
  - 当前主文档入口
  - 现有对象卡 / runtime / 批次 README / execution card / artifact index
- `OUTPUT`:
  - `10_source_library_archive/<batch>/00_raw_snapshot/...`
  - 批次 `README / manifest / provenance note`
  - 必要时提升后的 `00_entry / 01_active_objects / 02_runtime / 04_active_main_docs` 回写
- `ACCEPTANCE`:
  - 新资料先有来源层落点，再讨论是否提升
  - 至少写清 `source_path / repo_path / producer / evidence_mode / scope / status`
  - 至少能回答“它与仓库里已有哪一层对齐”
  - 至少保留一条从原始快照到提升后入口的回链
- `FAILURE_MODES`:
  - 资料一来就直接塞进默认入口
  - 不写 provenance 就直接当真值
  - 同类资料每次都临时起名、临时放路径
  - 只收总结，不留来源快照
  - 只收产物，不写生成入口与当前作用
- `NEXT_ITERATION`:
  - 给常见资料家族补标准 batch 模板
  - 给电子书 / 视频小结补对象卡映射模板
  - 给 runtime artifact ingest 补自动化校验

## 资料类型四分流

1. `SOURCE_SNAPSHOT`
   - 原始电子书、视频整理稿、网页摘录、研报、文章、历史说明文档
   - 默认先落 `10_source_library_archive/<batch>/00_raw_snapshot`
2. `INDEX_NOTE`
   - `README / INDEX / EXECUTION_CARD / ARTIFACT_INDEX / NOTE / CONTRACT`
   - 放在对应批次目录或 repo-global 入口层
3. `GENERATOR_OR_RUNTIME`
   - 脚本、配置、runner、probe、样本计划、验收脚本
   - 进入 `02_runtime/` 或 `20_tools_workspace/`，再按成熟度提升
4. `ARTIFACT_OR_HISTORY`
   - `csv / log / htm / html / png / gif / txt excerpt`
   - 默认进 `12_tooling_runtime_archive/<batch>` 或来源批次的附属说明层

## 固定步骤

1. 先判断目录角色
   - `来源快照` 进 `10`
   - `活跃入口/合同` 进 `00`
   - `可复现运行入口` 进 `02`
   - `日常当前动作与停点` 进 `04`
   - `历史运行时或大体量产物` 进 `12`
2. 先落最小来源快照
   - 统一先建 `10_source_library_archive/<batch>/00_raw_snapshot/...`
   - 不确定时宁可先归来源层，不直接挤进活跃入口
3. 立刻补最小说明
   - `README`
   - `manifest / provenance`
   - 必要时 `execution card / artifact index`
4. 判断影响层
   - 若只是原始资料：停在 `10`
   - 若形成稳定规则：提升到 `00_entry` 或 `01_active_objects`
   - 若形成可运行验证入口：提升到 `02_runtime`
   - 若改变当前推进顺序：回写到 `04_active_main_docs`
5. 建立回链
   - 从 `04/00/02/01` 的新入口，能回到原始来源快照
   - 从来源批次 README，能回到被提升的正式入口
6. 明确状态
   - `historical_recovered / archive_only / hard / weak_evidence / active_reference`
   - 禁止模糊写法

## 电子书并入专段

- 默认入口：
  - 先落 `10_source_library_archive/<batch>/00_raw_snapshot/books/...`
- 第一轮只做：
  - 目录归位
  - 书目说明
  - 载体可读性判断
  - 与现有主题的映射占位
- 不直接做：
  - 大段正文总结
  - 大量规则提炼
  - 未经映射的对象卡提升
- 只有当资料整理阶段收口后，才进入：
  - 摘录
  - 小结
  - 可量化规则抽取

## 视频并入专段

- 默认入口：
  - 先落 `10_source_library_archive/<batch>/00_raw_snapshot/videos/...`
- 第一轮只做：
  - 视频主题说明
  - 来源链接或原始摘录
  - 与现有对象/主题簇的映射占位
- 若已有逐帧稿或转写：
  - 仍先作为 `SOURCE_SNAPSHOT`
  - 不直接跳过来源层进入主文档

## 研报 / 文章 / 网页摘录并入专段

- 默认入口：
  - 先落 `10_source_library_archive/<batch>/00_raw_snapshot/reports_or_articles/...`
- 第一轮只做：
  - 来源说明
  - family / topic / symbol / timeframe 标签
  - 与当前对象卡或主题簇的映射占位

## 运行产物并入专段

- 若是当前主线新跑产物：
  - 先判断是否应进入 `02_runtime/.../artifacts` 或 `12_tooling_runtime_archive/<batch>`
- 若是旧仓历史回收：
  - 必标 `historical_recovered`
  - 必写原路径、生成入口、当前作用
- 每批至少要能回答：
  - 谁生成的
  - 用什么生成的
  - 是当前硬证据还是历史回收

## 提升门槛

- 只有满足以下条件才允许从 `10` 提升到活跃层：
  - 已有最小来源说明
  - 已能确定它影响哪一层
  - 已有稳定命名
  - 已能回链到来源快照
- 否则继续停留在来源层，不为了“看起来整齐”强行提升

## 当前默认回链

- 阶段路线图：`00_entry\BUTLER_STAGE_ROADMAP__20260709.md`
- 日常执行清单：`04_active_main_docs\batch_01_selected\03_阶段二_当下计划_执行清单.md`
- 目录角色合同：`00_entry\DIRECTORY_ROLE_CONTRACT_v1.md`
