# PLAYBOOK 滚动模板

## TEMPLATE_ID: REPO_OLD_FILE_SWEEP_AND_MIGRATION

- `VERSION`: `v1`
- `SCOPE`:
  - 适用于旧仓库全场扫库、`py / csv / log / report / mq4 / mq5 / ini / md` 的迁移前判定
  - 不适用于“已经明确为活跃对象最小集且可直接迁入”的紧急修复
- `INPUT`:
  - 旧仓库目录
  - 代表文件
  - 当前入口合同
  - 已有迁移批次状态
- `OUTPUT`:
  - `OLD_REPO_FILE_SWEEP_TASKBOARD.md`
  - 批次级 `README / EXECUTION_CARD / ARTIFACT_INDEX / NOTEBOARD`
  - 必要时的新仓库 `skill` 副本
- `ACCEPTANCE`:
  - 至少写清每一批的处理动作：`COPY_WITH_NOTE / NEW_IN_NEW_REPO / MOVE_LATER_AFTER_REF_CHECK / KEEP_OLD_FROZEN`
  - 至少写清该批当前为什么能迁或为什么不能迁
  - 至少写清哪些属于 `historical_recovered`
- `FAILURE_MODES`:
  - 只按文件名猜作用
  - 直接整包复制旧目录
  - 只迁产物，不迁生成入口和备注说明
  - 把历史回收证据写成最新实跑结果
- `NEXT_ITERATION`:
  - 给迁入脚本自动生成最小 provenance 备注
  - 给批次目录自动生成 `NOTEBOARD`
  - 对旧 `tools / TOOLING_RUNTIME` 做目录级批量分流

## 固定步骤

1. 先排除 `.venv / __pycache__ / site-packages`
2. 先做目录级和扩展名级盘点
3. 再按家族读代表脚本，不逐文件盲迁
4. 每批先写任务板和备注，再允许复制
5. 新仓库需要继续使用的旧 `skill`，优先建立副本，不只留旧仓库一份
6. 所有历史结果先标 `historical_recovered`

## 当前默认入口

- 任务板：`00_entry\OLD_REPO_FILE_SWEEP_TASKBOARD.md`
- 产物合同：`00_entry\ARTIFACT_NOTE_CONTRACT.md`
- 根目录备注：`ROOT_NOTES.md`

## TEMPLATE_ID: LEGACY_MIGRATION_FINITE_COUNTERS

- `VERSION`: `v1`
- `SCOPE`:
  - 适用于把“旧仓库迁移”从无限期推进，收敛成可数的剩余批次与退出条件
  - 不适用于直接删除外部原件目录
- `INPUT`:
  - `00_entry\OLD_REPO_FILE_SWEEP_TASKBOARD.md`
  - `04_active_main_docs\batch_01_selected\03_阶段二_当下计划_执行清单.md`
- `OUTPUT`:
  - `legacy_migration_remaining_batches=<...>`
  - `legacy_migration_remaining_actions=<...>`
  - `legacy_migration_exit_criteria=<...>`
- `ACCEPTANCE`:
  - 迁移工作始终可被计数：`remaining_batches_count` 与 `remaining_actions_count` 必须可从文档直接读取
  - 每个 batch 必须能落入四分流动作之一：`COPY_WITH_NOTE / NEW_IN_NEW_REPO / MOVE_LATER_AFTER_REF_CHECK / KEEP_OLD_FROZEN`
  - 当 `legacy_migration_remaining_batches_count=0` 且 `legacy_migration_remaining_actions_count=0` 时，旧仓库迁移进入“冻结维护态”，不再作为日常推进主线
- `FAILURE_MODES`:
  - 只说“继续推进”，不写剩余计数与退出条件
  - 把“未做完”的不确定性转嫁为外部目录无限期保留
- `NEXT_ITERATION`:
  - 把 `remaining_actions` 自动生成到任务板

## TEMPLATE_ID: EXTERNAL_FOLDER_DELETE_GATE

- `VERSION`: `v1`
- `SCOPE`:
  - 适用于外部目录（例如 `D:\Stock\cut_file\...`）的“可删”判定
  - 只允许逐文件判定，不允许整目录删除
- `INPUT`:
  - `10_source_library_archive\mirror_kimi_inbox\GROUP_08_A股量化_数据研究\GROUP_08_external_ops_plan_v1.tsv`
  - `10_source_library_archive\mirror_kimi_inbox\GROUP_08_A股量化_数据研究\GROUP_08_external_ops_preflight_v1.tsv`
  - `10_source_library_archive\mirror_kimi_inbox\GROUP_08_A股量化_数据研究\GROUP_08_external_move_postcheck_v1.tsv`（若有）
- `OUTPUT`:
  - `external_delete_gate_steps=4`
  - `external_delete_gate_step1=repo_refscan_outside_refs_zero`
  - `external_delete_gate_step2=preflight_source_and_staging_exist_and_sha_match`
  - `external_delete_gate_step3=postcheck_moved_ok`
  - `external_delete_gate_step4=ledger_mark_delete_allowed`
- `ACCEPTANCE`:
  - 任何文件只有在 `step1..step4` 全满足后，才允许进入 `DELETE_ALLOWED`
  - `MOVE_READY_NOT_DELETE` 永远不进入删除动作
  - 不允许对外部目录做整包删除；删除只对单文件发生
- `FAILURE_MODES`:
  - 用 “仓库里已有副本” 替代 `repo_refscan` 结果
  - 把 `DELETE_EXTERNAL_SUBSET_CANDIDATE` 误当成 “可以删整目录”
  - 未做 `postcheck` 就直接删外部文件
