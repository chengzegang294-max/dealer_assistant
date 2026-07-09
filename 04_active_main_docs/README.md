# Active Main Docs

## 用途

- 这里放从旧根目录迁入的新活跃主文档。
- 目标是让未来主线逐步脱离 `trading_analysis` 根目录。

## 当前规则

- 只迁仍要继续维护的主文档。
- 每次迁入前先判断：
  - 是否仍为主入口
  - 是否存在更新替代版本
  - 是否会与旧根目录形成双活跃维护
- 新仓库这层要逐步承接旧根目录同类职责：
  - `00` = 默认入口与导航
  - `01` = 已落地事实
  - `02` = 方向与边界
  - `03` = 当前动作与下一步
  - `关于日活` = 最近一轮结论与停点

## 当前角色路由

- 若你要找“从哪里开始看”：先看 `batch_01_selected\00_主线检索索引.md`
- 若你要找“已经落地了什么”：看 `batch_01_selected\01_阶段一_项目记录_过去与落地.md`
- 若你要找“为什么这样推进、哪些边界不能碰”：看 `batch_01_selected\02_阶段二_工作方向_想法库.md`
- 若你要找“当前动作、下一步、验收口径”：看 `batch_01_selected\03_阶段二_当下计划_执行清单.md`
- 若你要找“最近一轮推进结论与停点”：看 `batch_01_selected\关于日活.md`
- 若你要找“当前 runtime 聚合正式入口”：看 `..\00_entry\REGISTRY_V0_FORMAL_ENTRY_CARD__20260709.md`
- 若你要找“项目大阶段路线图与后续收口顺序”：看 `..\00_entry\BUTLER_STAGE_ROADMAP__20260709.md`
- 若你要找“新增电子书/视频/研报/产物如何并入并和旧资料对齐”：看 `..\docs\playbooks\NEW_INFO_INGEST_ALIGNMENT_PLAYBOOK__20260709.md`
- `registry_v0` 固定阅读链：
  - `..\00_entry\REGISTRY_V0_FORMAL_ENTRY_CARD__20260709.md -> ..\02_runtime\butler_r0_ohlcv_object_cards\runtime_execution_card_v1.md -> ..\02_runtime\butler_r0_ohlcv_object_cards\run_registry_v0_minimal.py`
- 若你要找“当前 trae system 过渡工作副本边界”：看 `..\00_entry\trae_system_transition\README.md`

## 当前状态

- 当前只建层级，不直接复制旧根目录全部文件。
- 旧仓库当前仍保留原件与历史追溯层；新仓库这层逐步成为未来主工作根的活跃主文档镜像层。
- 当前镜像承接也纳入统一主线规划：
  - `00_entry\MAINLINE_FULL_INGEST_AND_MIGRATION_PLAN__2026-06-26.md`
- 这意味着后续不是照搬旧长文，而是优先承接：
  - 更短的当前入口
  - 已同步的当前合同层
  - 已去重后的阶段结论
- 当前判断：
  - 旧仓库主文档仍是全量进度真源
  - 新仓库这层已经完成首批锚点承接
  - 但正文级镜像同步与第二轮去冗余仍未全部完成
- 当前补记：
  - `registry_v0` 已具备仓库级正式入口，并已与 runtime 执行卡形成自然阅读链
  - `trae_system_transition` 当前只作为 repo-global working copy，不替代 `.trae` first-hop，也不把关键回指沉到被 `.gitignore` 排除的本地修改里
- 当前镜像层的作用不是“替代旧仓库所有长文”，而是逐步接管：
  - 当前主线入口
  - 当前已落地事实
  - 当前动作与下一步
