# Mainline Full Ingest And Migration Plan

## 目的

- 这份规划用于把当前新主线固定成一条并行主线，而不是“迁移一条线”和“全量吃透一条线”各走各的。
- 当前统一主线是：
  - 继续把旧仓库中作用明确、可长期维护、已补说明的内容迁入新仓库
  - 同时继续全量吃透旧仓库，压平重复结论、冗余过程和被后续覆盖的旧说法
  - 让新仓库逐步成为未来主工作根，旧仓库保留为历史大仓库与来源锚点层

## 当前主线一句话

- 新主线不是“先整理完旧仓库再迁移”，也不是“先迁移一批再说”；而是边全量吃透、边做四分流、边把可复用对象迁入新仓库。

## 当前判断

- 旧仓库“全量吃透”至少已经推进到 `Batch 36`，说明问题不在于“没做”，而在于：
  - 当前默认入口仍然偏长
  - 重复结论散在多份长文
  - 部分工具和流程已经明确有价值，但还没系统迁入新仓库
- 当前环境口径已经统一：
  - 工作区根目录固定为 `d:\Stock\trading_assistant`
  - 默认解释器固定为 `d:\Stock\trading_assistant\.venv\Scripts\python.exe`
  - 树外 `.venv` 只允许作为本机临时覆盖，不再写成仓库默认入口
- 当前仓库分工也已更明确：
  - `trading_analysis` = 内容真源 / 历史追溯真源
  - `trading_assistant` = 结构承接仓 / 主文档镜像仓 / 运行时批次承接仓
- 因而这一轮不追求照搬旧文件，而是优先做三件事：
  - 继续吃透
  - 继续迁移
  - 继续压缩冗余
- 当前阶段锚点：
  - `00_entry\BUTLER_STAGE_ROADMAP__20260709.md`
- 当前新增资讯并入锚点：
  - `docs\playbooks\NEW_INFO_INGEST_ALIGNMENT_PLAYBOOK__20260709.md`

## 当前主线任务

- 继续压旧主文档 `01` 正文追溯层剩余重复背景句，优先清 `Kimi / S桶` 段还能并短的句子。
- 继续维持 `S_BUCKET_02` 的 `YZ-A / YZ-B` 对象级真值锚点与主题簇证据增强，并把单体对象卡 / manifest / README / 顶层入口保持同步。
- 保持 `00/02/03/关于日活` 与镜像 `batch_01_selected/00/01/02/03/关于日活` 同口径同步。
- 保持“原件层”第二阶段当前口径：`F1/F2/A2/A5` 独立短状态块，`A3/A4/A1` 轻量子组状态。
- `Batch9` 继续保持 `NO failed breakout` 与 Hold，不扩 `or_break_only beyond multi-session all-closes` 新分支。
- `MT` 子线继续保持“证据先行”：
  - `Volty` 先补 `DumpSeries=1` 的 fresh-run CSV
  - `XBreaking` 先补 tester `.htm` report
  - 未补齐前不升级成“字段已闭合 / 语义已完成”
- 每轮同步回写任务板 / 进度板 / `MAINLINE`，并做 diagnostics 收口。
- 当前新增资讯（电子书 / 视频 / 研报 / 网页摘录 / 运行产物）不再现场临时判定，统一按：
  - `docs\playbooks\NEW_INFO_INGEST_ALIGNMENT_PLAYBOOK__20260709.md`
  先落来源层、补 provenance、再判断是否提升到 `00/01/02/04`。

## 原件层当前角色

- 当前结论：`D:\Stock\cut_file` 已退出当前合同层；repo 内 `10_source_library_archive\raw_assets` 与 `10_source_library_archive\mirror_kimi_inbox` 已接管默认入口、原件复核与继续推进。
- 当前角色应固定为：
  - repo 内 `raw_assets`：正式原件复核层
  - repo 内 `mirror_kimi_inbox`：稳定入口与镜像承接层
  - 树外目录若仍保留：历史追溯与 provenance 快照
- 当前已经基本脱离原件层的部分：
  - `GROUP_08 research pdf` 的日常使用入口已基本转到仓库内 staging
  - `NFTRADEZ` 已完成首轮入库，外部目录更多只保留来源映射与历史追溯作用
- 当前仍需继续收口的部分：
  - `S桶` 的删源裁决与对象级证据增强
  - `GROUP_08` 的 repo 内原件侧逐文件删除勾验
  - 若保留树外目录，只能作为 provenance 快照，不再进入当前执行面
  - `GROUP_08` 下仍保留旧绝对路径的 `路径勾验/前后路径台账/dryrun ps1` 统一归入 `ARCHIVE_ONLY__HISTORICAL_PROVENANCE_SNAPSHOT`
- 当前固定策略：
  - 不把 `D:\Stock\cut_file` 当 repo 默认入口
  - 不再把 `D:\Stock\cut_file` 写成当前执行路径
  - 继续把删源裁决、对象锚点和原件复核统一收在 repo 内

## 原件层退场路线

- 当前目标不是长期依赖原件层，而是让 `D:\Stock\cut_file` 完全退出当前工作流，只保留 repo 内承接层。
- 当前执行锚点：
  - `00_entry\CUT_FILE_RETIREMENT_PLAN__2026-06-26.md`
- 固定顺序：
  1. 先让新仓库承接默认入口
  2. 再让新仓库承接小体量真值锚点
  3. 最后把树外目录降成历史快照与 provenance 备份
- 当前默认工作流已完成这一步；后续只继续清理文档口径与历史脚本残留。

## 固定原则

- 不简单复制旧文件。
- 允许按需要重命名、换批次名或换目录名，但必须同时回写原路径、现路径和作用说明。
- 允许把部分源文件移到新仓库，但前提是先完成作用卡、输入输出和引用边界确认。
- 不让新增资讯绕开来源层与 playbook 直接进入默认入口。
- 不把历史过程长文继续当默认入口。
- 不把已完成批次重新写成“待继续拆”。
- 不把旧仓库一次性搬空。
- 不因为想整理得漂亮就牺牲可追溯性。
- 不为了图省事盲目复制源文件。

## 四条并行线

### A 线：旧主文档第二轮清理

- 目标：
  - 把 `00/01/02/03/关于日活` 从“已有首轮当前合同层”推进到“第二轮去冗余”
- 重点动作：
  - 合并重复结论
  - 删去错误试探过程
  - 删去被后续裁决覆盖的旧说法
  - 保留已完成批次、当前边界、当前对象、下一步
- 当前验收：
  - 用户不需要翻长文就能知道“做到哪一步、先看哪里、下一步干嘛”

### B 线：旧 tools / py 全场扫库继续推进

- 目标：
  - 继续按作用清晰度把旧脚本分成 `COPY_WITH_NOTE / NEW_IN_NEW_REPO / MOVE_LATER_AFTER_REF_CHECK / KEEP_OLD_FROZEN`
- 当前重点：
  - `PY-03` 已完成首批迁入
  - `PY-04 = tk_r6~r8` 手工表家族已完成新仓迁入与模板级 smoke 验收
- `PY-04` 当前顺序：
  1. `tk_r6_make/summarize`：已迁入且 smoke 通过
  2. `tk_r7_make/summarize`：已迁入且 smoke 通过
  3. `tk_r8_make/summarize`：已迁入且 smoke 通过
  4. 后续只补真实人工审计样本，不再重复做模板级验证
- 当前验收：
  - 已形成 `R6/R7/R8` 三组完整可对账迁入链，并确认新仓可独立完成“模板生成 -> 汇总输出”最小闭环

### C 线：迁移进度与任务板同步

- 目标：
  - 每推进一批，都让旧仓库和新仓库都能看见最新状态
- 必同步文件：
  - `00_entry\OLD_REPO_FILE_SWEEP_TASKBOARD.md`
  - `04_active_main_docs\README.md`
- 当前验收：
  - 不依赖聊天记忆也能知道主线、进度和下一刀

## 迁移有限计数

- 当前不再允许把“旧仓迁移”写成无限主线；必须持续收敛为可数的剩余批次与剩余动作。
- 当前口径：
  - `legacy_migration_current_state_v1=OLD_REPO_FROZEN_MAINTENANCE_ONLY`
  - `legacy_migration_remaining_batches=NONE`
  - `legacy_migration_remaining_batches_count=0`
  - `legacy_migration_remaining_actions=NONE`
  - `legacy_migration_remaining_actions_count=0`
  - `legacy_migration_exit_criteria=remaining_batches_count=0_and_remaining_actions_count=0=>OLD_REPO_FROZEN_MAINTENANCE_ONLY`
- 解释：
  - `old_main_docs_round2_tail` = 已完成；`12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_trading_analysis/01/02/00` 已收成“兼容入口 + 顶部合同层 + 最小历史锚点”
  - `active_main_docs_body_sync_tail` = 已完成；新仓 `04_active_main_docs\batch_01_selected` 的 `00/01/02/03/关于日活` 已完成正文级镜像同步并切回统一入口口径
  - `source_library_stage2_minimal_return_batch` = 已完成；`S_BUCKET` 的 `13` 个锚点回迁批次与 `A/F` 第二阶段状态表都已写硬到 repo-first 入口
  - `tools_long_tail_and_high_risk_role_cards` = 已完成；`PY-03` 长尾工具已入 `20_tools_workspace`，`backtest_p0 / mt5_exit_assistant / ashare_preprocess` 已补高风险作用卡并继续 `KEEP_OLD_FROZEN`
  - `finite_counter_sync_and_freeze_gate` = 所有迁移入口文档统一剩余计数口径，并在归零前禁止写成“已冻结维护态”

### D 线：新仓库主文档镜像层继续承接

- 目标：
  - 让 `trading_assistant\04_active_main_docs` 不只是首批复制层，而是未来主工作根的镜像入口层
- 当前重点：
  - 继续承接旧根目录 `00/01/02/03/关于日活` 的同类职责
  - 不要求照搬旧长文，优先承接“短入口 + 当前合同层 + 已同步结论”
- 当前验收：
  - 新仓库入口能独立说明当前主线、已落地事实、方向边界和最近停点

## 每轮固定推进顺序

1. 先做一份旧主文档的第二轮去冗余。
2. 同时推进一组 `PY-04` 代表脚本作用卡与迁入裁决。
3. 再同步旧仓库进度板和主文档清理任务板。
4. 最后同步新仓库主文档镜像说明。

## 当前不做

- 不把 `TK-R1 ~ TK-R4` 审计家族整组迁入新仓库。
- 不把来源库、冻结层、运行时层做整包复制。
- 不为保留历史而保留所有碎过程。
- 不在没有作用卡和输入输出口径时直接迁脚本。

## 最近两轮的最顺动作

### Round 1

- 旧主文档：
  - 继续对 `03_阶段二_当下计划_执行清单.md` 和 `关于日活.md` 做第二轮压缩
- `PY-04`：
  - 完成 `tk_r6_make_manual_sheet.py`
  - 完成 `tk_r6_summarize_manual_sheet.py`
  - 若边界清楚，同轮开 `batch_04` 迁入目录与备注

### Round 2

- 旧主文档：
  - 继续对 `01_阶段一_项目记录_过去与落地.md` 和 `02_阶段二_工作方向_想法库.md` 做第二轮压缩
- `PY-04`：
  - 推进 `tk_r7_*`
  - 再推进 `tk_r8_*`
- 同步：
  - 回写本仓库进度板
  - 回写本仓库任务板
  - 回写本仓库镜像入口说明

### Round 3

- 旧主文档：
  - 继续压 `03` 和 `关于日活` 顶层重复段，确保一眼能看懂原件层退场路线和 `PY-04` 完整链
- `PY-04`：
  - 完成 `tk_r8_*`

### Round 4

- `S`：
  - 继续沿 `02_游资悟道交割单` 的小体量真值锚点推进
  - `YZ-A01/A02/A03 -> Mxx` 显式映射检查已落盘，当前结论：`NO_EXPLICIT_MAPPING_FOUND_YET`
  - `YZ-B03` 已完成首批真实摘录卡
  - `YZ-B01` 已改用 `epub` 并完成首批真实摘录卡
- 旧主文档：
  - 继续压 `03` 与 `关于日活` 顶层重复段，把“当前主线 / 当前对象 / 下一刀”再收短
- 同步：
  - 回写旧库进度板
  - 回写旧库主文档清理任务板
  - 保持新库批次壳与主线规划同口径

### Round 5

- `S`：
  - `YZ-B02` 已完成首批真实摘录卡（`pdf` 可抽正文）
  - `YZ-B` 当前已具备三张对象级锚点：`YZ-B01 / YZ-B02 / YZ-B03`
  - 下一刀转去验证 `YZ-B04` 的默认载体
- 旧主文档：
  - 继续压 `03` 与 `关于日活` 顶层重复段，优先合并可合并的重复句
- 同步：
  - 回写旧库进度板与旧库清理任务板
  - 更新批次 README/manifest，确保新旧口径一致

### Round 6

- `S`：
  - `YZ-B04` 已完成首批真实摘录卡（`pdf` 可抽正文）
  - `YZ-B` 当前已具备四张对象级锚点：`YZ-B01 / YZ-B02 / YZ-B03 / YZ-B04`
  - 下一刀把 `YZ-B` 汇总成对象组入口短摘要（不升级成硬门控）
- 旧主文档：
  - 继续压 `03` 与 `关于日活` 顶层重复段，保持“主线/当前对象/下一刀”一眼能读
- 同步：
  - 回写旧库进度板与旧库清理任务板
  - 更新批次 README/manifest 与候选表，保持对账一致

### Round 7

- `S`：
  - `YZ-B` 对象组入口短摘要已落盘：`YZ_B_GROUP_SUMMARY__2026-06-26.md`
  - `YZ-B` 主题簇映射证据已落盘：`YZ_B_THEME_CLUSTER_MAPPING__2026-06-26.tsv`
  - `YZ-B` 与旧冻结层主题簇对照检查已落盘：`YZ_B_TO_OLD_FROZEN_THEME_ALIGNMENT_CHECK__2026-06-26.md`
  - `YZ-B` 每簇旧冻结层同主题证据表已落盘：`YZ_B_OLD_FROZEN_THEME_EVIDENCE__2026-06-26.tsv`（仍不并旧卡号）
  - 已把对照结论压短回写到 `S_BUCKET_02` 的“可复用旧事实”段
  - `YZ-A` 主题簇映射与旧冻结层同主题证据表已落盘（仍不并旧卡号）
  - 已把 `YZ-A` 的主题簇对照结论压短回写到 `S_BUCKET_02` 的“可复用旧事实”段
- 旧主文档：
  - 继续压 `03` 与 `关于日活` 顶层重复段，优先删掉可以由“入口卡/索引卡”替代的长段
- 同步：
  - 回写旧库进度板与旧库清理任务板
  - 回写 `S_BUCKET_02_YOUZI_TRUTH_ANCHOR_CANDIDATES__2026-06-26.md`

### Round 8

- `A* / F*`：
  - 固定口径：外部只留重资产原件与追溯位；repo 内已有稳定入口的不回外部当默认入口
  - 已把 `A* / F*` 的 repo 内稳定入口指向补进 `CUT_FILE_RETIREMENT_PLAN__2026-06-26.md`
  - `F1 / F2 / A2 / A5` 已从第一版草案推进到第二版同口径状态表：当前入口、当前边界、下一刀与进入下一阶段条件都已补齐
  - `A3 / A4 / A1` 已满足轻量细拆条件，默认保持“组级主入口 + A1 / A3-C1 / A3 extra / A4 轻量子组状态”，不下沉到更重状态表
  - 已把旧库 `01` 的 `Batch 16-18 / 19-23 / 24-35 / 36` 压成组级事实结论，并同步到 `04_active_main_docs/batch_01_selected/01`
- `S`：
  - `YZ-A` 的旧冻结层同主题证据表已继续加厚（等待/停手/风险与仓位上限/回撤触发/系统性风险应对等行号证据），提升可对账性
- 旧主文档：
  - 已把 `03` 与 `关于日活` 的顶层重复段继续压短
  - 已把 `00` 里 `NFTRADEZ / S_BUCKET` 的长合同段继续压回 `上位入口 / 包级固定顺序 / 当前裁决 / 补充入口` 短导航结构，避免索引页重新变成长合同堆叠
  - 已把 `00` 里 `A/F 第二阶段入口` 挂回主线索引，现在可直接从索引页进入 `F1/F2/A2/A5/A3-A4-A1` 的当前入口、边界与下一刀
  - 已把 `F1/F2/A2/A5/A3-A4-A1` 的当前分区短状态继续挂回 `00`，让索引页直接可读，不再只是目录指针
  - 已把 `CUT_FILE_RETIREMENT_PLAN__2026-06-26.md` 里的 `F1 / F2 / A2 / A5` 继续补成各自独立短状态块，计划层也能直接回答“入口 / 边界 / 下一刀”
  - 已确认 `A3 / A4 / A1` 组内存在独立 `README + manifest` 稳定入口，并已前推到“组级主入口 + A1 / A3-C1 / A3 extra / A4 轻量子组状态”
  - 已继续把 `A3 / A4 / A1` 的轻量子组状态统一成同模板口径，当前优先是统一模板，不急着下沉到更重状态表
  - 已开始把 `01` 的“当前合同层 / 历史追溯层”分界写硬：默认阅读顺序与追溯层压缩边界已补入旧库 `01` 与镜像 `01`
  - 已把 `01` 的 `Batch 16-36` 补成一段组级历史追溯压缩版，先把 `Batch 15` 之后的断档接回可读追溯层
  - 已把 `01` 里 `Batch 8 / Batch 9A-15` 的重复“当前下一刀已固定为”序列压回组级追溯事实，避免 `2026-06-23 来源库总台账收口` 中段重新膨胀
  - 已把 `01` “当前已落地事实”里的来源库整理背景压成 `目录级收口 / GROUP_06+05 / GROUP_08` 三组稳定结论，减少与后文重复
  - 已把 `01` 里 `Kimi` 线尾部的 `GROUP_05/06` 吸收壳、批次检查锚点与最小吸收包三条重复句并成一组落地锚点
  - 已把 `01` 里 `Kimi` 线下一步事实锚点从两条子句压成一条固定动作句
  - 已把 `01` 里“全项目最终整理已拆成三部分”压成一条三块式停点句
  - 已把 `01` 里 `GROUP_08` 的重复历史长段继续压成四组事实块，降低新开对话后重新解释上下文的成本
  - 已继续把 `01` 里 `GROUP_08` 之后的 `Kimi / S桶` 大段枚举压成 `独立化边界 / batch1 四包 / NFTRADEZ 双包 / backlog 与 GROUP_08 锚点` 四组事实块，进一步降低新开对话后的重建成本
  - 已把 `00/02` 的“当前合同层 / 历史追溯层”分界继续写硬：默认使用边界与追溯层压缩边界已补入旧库与镜像；其中 `02` 已明确 `S_BUCKET / NFTRADEZ` 旧长合同不再充当默认方向入口
  - 当前结论：`01/02/00` 的第二轮剪枝与 `00/01/02/03/关于日活` 的正文级镜像同步都已完成，后续只保留兼容入口维护与必要的历史追溯
- 新仓库镜像层：
  - `batch_01_selected` 的 `00/01/02/03/关于日活` 已完成顶层合同层与正文级镜像同步
  - `batch_01_selected/01` 已固定为“顶层合同层 + 追溯层边界 + Batch 16-36 历史追溯压缩版 + Batch 8/9A-15 组级追溯事实 + Kimi/S桶 四组事实块”同口径
  - `batch_01_selected/00/02` 也已固定为“默认使用边界 + 追溯层压缩边界”同口径，`00` 已稳定承接短导航结构
  - 后续只做维护态同步，不再把镜像同步写成未完成缺口
- 同步：
  - 回写 `S_BUCKET_REPO_STATE_TABLE__2026-06-26.md` 与 `CUT_FILE_RETIREMENT_PLAN__2026-06-26.md`
  - 回写 `关于日活.md`、`OLD_MAIN_DOC_CLEANUP_TASKBOARD.md` 与 `OLD_REPO_TO_NEW_REPO_PROGRESS.md`

### Round 9

- `A* / F*`：
  - `A3 / A4 / A1` 的 `A1 / A3-C1 / A3 extra / A4` 子组入口清单已挂回 `00_主线检索索引.md`，并补进 `CUT_FILE_RETIREMENT_PLAN__2026-06-26.md` 的轻量子组状态模板段
  - `CUT_FILE_RETIREMENT_PLAN__2026-06-26.md` 里已把上一轮完成后的旧“待抽短表”表述更新为当前真实停点：`F1 / F2 / A2 / A5` 保持独立短状态块，`A3 / A4 / A1` 下一刀固定为统一轻量模板口径
- 旧主文档：
  - 已把 `02/03/关于日活` 的口径改成一致描述：`A3/A4/A1=轻量子组状态；下一刀=统一模板口径`
- 同步：
  - 已把旧库进度板与旧库任务板补上 `A3/A4/A1` 子组入口清单锚点

## 2026-07-09 durable sync 补记

- `registry_v0` 已从 runtime 内部聚合能力上提为仓库级正式入口：
  - `00_entry\REGISTRY_V0_FORMAL_ENTRY_CARD__20260709.md`
- 当前正式阅读链路已固定为：
  - `00_entry formal entry -> 02_runtime runtime_execution_card_v1.md -> run_registry_v0_minimal.py`
- `trae_system_transition` 已明确保持“working copy / 治理中间态”角色：
  - `21_trae_system_archive` 继续承担 `decision index / group router`
  - `00_entry\trae_system_transition\` 继续承担 repo-global working copy
- 当前 `.trae/` 目录受 `.gitignore` 约束：
  - 不把关键治理回指只写进本地 `.trae` 修改
  - repo 内可追踪真值继续以 `00_entry / 21_trae_system_archive / 04_active_main_docs` 为准

## 验收标准

- 新主线能同时回答四件事：
  - 当前主线是什么
  - 这轮并行推进哪几条线
  - 哪些结论已经 durable sync
  - 下一刀最顺做什么
- 旧仓迁移必须能直接读出：
  - `remaining_batches_count`
  - `remaining_actions_count`
  - `exit_criteria`
- 旧主文档越来越短，不再继续无上限堆长。
- 新仓库迁入越来越像“有入口、有说明、有边界”的长期工作根。

## 一句话记忆

- 当前新主线就是：继续迁移到新仓库，同时继续全量吃透旧仓库；不照搬旧长文，而是边吃透、边去冗余、边把真正值得维护的东西迁进来。
