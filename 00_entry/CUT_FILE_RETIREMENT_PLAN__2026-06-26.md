# Cut File Retirement Plan

## 目标

- 这份计划用于把“原件层”从“历史上经常被直接使用的外部库”逐步压成“只保留极少数必要补核链路；默认阅读与真值锚点全部在 repo 内”。
- 当前不是直接删原件层，而是先把 repo 内承接层做完整，再让任何外部目录失去默认入口角色。

## 当前合同层

- repo 默认入口：
  - `00_entry\MAINLINE_FULL_INGEST_AND_MIGRATION_PLAN__2026-06-26.md`
- repo 真值文件：
  - `00_entry\CUT_FILE_RETIREMENT_PLAN__2026-06-26.md`
  - `04_active_main_docs\batch_01_selected\03_阶段二_当下计划_执行清单.md`
  - `04_active_main_docs\batch_01_selected\关于日活.md`
- repo 回帖副本：
  - 暂无单独 imported reply
- 扩展字段附注：
  - `goal=让新仓库先承接入口与真值锚点，再压缩外部重资产依赖`
  - `durable_truth=原件层仍可能被用于追溯，但已经不再承担默认入口`
  - `boundary=不盲目复制、不提前删源、不跳过引用检查`

## 三阶段退场

### 阶段 1：新仓库承接默认入口

- 验收定义：
  - 日常阅读、检索、继续推进都优先从 repo 内入口开始
  - 树外路径只作为来源映射或 PDF 读取位出现
- 当前状态：`IN_PROGRESS`
- 已完成：
  - `NFTRADEZ` 默认入口已切到 repo
  - `S_BUCKET priority_read / round2 / round3` 默认入口已切到 repo
  - 主线规划、扫库任务板、旧执行清单、日活都已把原件层定位为“非默认入口”
- 当前剩余：
  - 把原件层的分区状态整理成更短的执行卡
  - 继续压旧主文档里的重复树外路径叙述

### 阶段 2：新仓库承接小体量真值锚点

- 验收定义：
  - manifest / summary / README / imported reply / mapping tsv / cutpack 入口优先落到 repo
  - 外部目录不再承担“当前真值文件”职责
- 当前状态：`IN_PROGRESS`
- 已完成：
  - `NFTRADEZ` 的 `README / manifest / imported md / 吸收与分流` 已落 repo
  - `S_BUCKET` 的 `summary / mapping_tsv / prompt / round2 README / round3 README / imported reply` 已落 repo
  - `GROUP_08` 已基本脱离原件层作为日常使用入口
- 当前剩余：
  - `S` 桶主体仍有大量原件和部分来源映射在外部；repo 内分区状态表见 `S_BUCKET_REPO_STATE_TABLE__2026-06-26.md`
  - A/F 书库分桶里的 `CUTPACK / OUTPUT_MD / 原始 pdf/epub` 仍主要停在外部
  - 仍需继续筛选哪些是真值锚点、哪些只是原始重资产

### 阶段 3：只保留历史原件和极少数补核链路

- 验收定义：
  - 原件层中留下的内容能明确解释“为什么必须留在外部”
  - 仓库内已存在对应的默认入口、当前真值文件和最小索引
- 当前状态：`NOT_READY`
- 当前计划保留对象：
  - 大体量 `pdf / epub / jpg / 原始切书中间产物`
  - 已完成索引级 repo 自足、但仍保留为 repo truth 的 `S` 桶原件层
  - 仍需删源前补核的少数目录
- 当前禁止动作：
  - 不做整盘删除
  - 不做无备注移动
  - 不把外部目录直接写成 repo 默认入口

## 当前分区清单

### A. 已基本完成阶段 1

- `诺曼NFTRADEZ`
  - 当前判断：repo 内入口和小体量真值锚点已经比较完整
  - 外部侧角色：更多只剩历史导出文本与旧原件追溯
- `GROUP_08`
  - 当前判断：日常使用入口已基本不依赖原件层
  - 外部侧角色：保留 bookdir 原件与历史排序层

### B. 已进入阶段 2，但还没收完

- `S`
  - 当前判断：repo 内已有 `summary / mapping / prompt / imported reply`；`stage proof` 评估锚点已在 repo（源文件子集仍为本地 derived staging）
  - 当前执行锚点：`00_entry\S_BUCKET_REPO_STATE_TABLE__2026-06-26.md`
  - 当前下一刀：`00_entry\S_BUCKET_02_YOUZI_TRUTH_ANCHOR_CANDIDATES__2026-06-26.md`
  - 当前结论：`S_BUCKET_INDEX__2026-06-17.tsv` 四分区 `868` 条已全部在 repo 内 `raw_assets` 可复核，repo 默认使用已不依赖树外路径
  - 当前角色：`REPO_SELF_CONTAINED__DELETE_POLICY_SPLIT_FIXED`
  - 当前退场裁决：
    - `树外默认入口 / 树外读取位 = DELETE_READY`
    - `repo 内 raw_assets\S = HOLD_AS_REPO_TRUTH`
    - `derived staging 说明 = HISTORY_ONLY`
    - `01_集合竞价教程 = tree_out DELETE_READY / repo_raw_assets HOLD_AS_REPO_TRUTH`
    - `02_游资悟道交割单 = tree_out DELETE_READY / repo_raw_assets HOLD_AS_REPO_TRUTH`
    - `03_券商研报 = tree_out DELETE_READY / repo_raw_assets HOLD_AS_REPO_TRUTH`
    - `04_待归类 = tree_out DELETE_READY / repo_raw_assets HOLD_AS_REPO_TRUTH`
    - `03_券商研报 / representatives_proof = tree_out DELETE_READY / repo_raw_assets HOLD_AS_REPO_TRUTH / 408_rows_407_unique`
    - `03_券商研报 / index_only_md_pdf = tree_out DELETE_READY / repo_raw_assets HOLD_AS_REPO_TRUTH / 70_unique`
    - `03_券商研报 / 05_其他 = tree_out DELETE_READY / repo_raw_assets HOLD_AS_REPO_TRUTH / equal_to_index_only`
    - `03_券商研报 / representatives_proof / action = HOLD_AS_REPO_TRUTH + OBJECT_CARD_FIRST`
    - `03_券商研报 / index_only_md_pdf / action = HOLD_AS_REPO_TRUTH + NO_AUTO_PROOF`
    - `03_券商研报 / 05_其他 / action = FUTURE_BUCKET + EXPLICIT_APPROVAL_ONLY`

### C. 目前更像外部重资产来源库

- `A1 / A2 / A3 / A4 / A5`
  - 当前判断：外部仍承担大体量原件层，但 repo 内已经存在多份可用的稳定入口（不需要回到外部做默认入口）
    - `A2`：`10_source_library_archive\mirror_kimi_inbox\GROUP_06_Auction_MarketProfile_价格行为\01_A2_cutpack_v2_final\README_放这里.md`
    - `A3/A4/A1`：`10_source_library_archive\mirror_kimi_inbox\GROUP_09_完善体系书库_切割产物\README_放这里.md`
    - `A5`：`10_source_library_archive\mirror_kimi_inbox\GROUP_10_A5_财报_估值_组合管理\README_放这里.md`
  - 当前策略：外部只留原件与追溯位；repo 内只挑“真值锚点/入口/索引”，不整包复制
- `F1 / F2`
  - 当前判断：外部仍有原始 pdf 等重资产，但 repo 内已经存在稳定 cutpack 入口
    - `F1`：`10_source_library_archive\mirror_kimi_inbox\GROUP_05_趋势_系统交易\01_F1_cutpack_v2_final\README_放这里.md`
    - `F2`：`10_source_library_archive\mirror_kimi_inbox\GROUP_01_微观结构_交易所_HFT\01_F2_cutpack_v2_final\README_放这里.md`
  - 当前策略：外部只留原件与追溯位；repo 内继续沿“真值锚点/入口/索引”推进，不整包复制

当前 `A* / F*` 第二阶段分区状态速查表（先用短表承接，不回外部当默认入口）：

| 分区 | repo 内稳定入口（示例） | 当前外部角色 | repo 当前角色 | 下一刀 |
|------|-------------------------|--------------|---------------|--------|
| A2 | `...\\GROUP_06_Auction_MarketProfile_价格行为\\01_A2_cutpack_v2_final\\README_放这里.md` | 重资产原件与追溯位 | 稳定入口已存在，但未整理成同口径分区状态表 | 补“入口/边界/下一步”短表 |
| A3/A4/A1 | `...\\GROUP_09_完善体系书库_切割产物\\README_放这里.md` | 重资产原件与追溯位 | 组级入口已存在，但仍偏 cutpack 汇总口径 | 先拆成可读组级状态 |
| A5 | `...\\GROUP_10_A5_财报_估值_组合管理\\README_放这里.md` | 重资产原件与追溯位 | 稳定入口已存在，但未形成 repo 内状态表 | 补“入口/边界/下一步”短表 |
| F1 | `...\\GROUP_05_趋势_系统交易\\01_F1_cutpack_v2_final\\README_放这里.md` | 重资产原件与追溯位 | 稳定入口已存在，适合作为首批分区表试点 | 优先做同口径状态表 |
| F2 | `...\\GROUP_01_微观结构_交易所_HFT\\01_F2_cutpack_v2_final\\README_放这里.md` | 重资产原件与追溯位 | 稳定入口已存在，适合作为首批分区表试点 | 优先做同口径状态表 |

第二版同口径分区状态表（先做 `F1 / F2` 试点）：

| 分区 | 当前状态 | 当前入口 | 当前边界 | 下一刀 | 进入下一阶段的条件 |
|------|----------|----------|----------|--------|--------------------|
| F1 | `IN_STAGE2_READY_FOR_STATE_TABLE` | `GROUP_05_趋势_系统交易\01_F1_cutpack_v2_final\README_放这里.md` | repo 内默认只承接稳定 cutpack 入口与后续状态表；外部继续承担原始 pdf、重资产原件与追溯位，不整包复制 | 把 `F1` 的“入口/边界/下一步”从本计划抽成可单独引用的短状态块，并补回主文档停点 | repo 内能单独回答“看哪/不看哪/下一刀”，且不回外部目录做默认入口 |
| F2 | `IN_STAGE2_READY_FOR_STATE_TABLE` | `GROUP_01_微观结构_交易所_HFT\01_F2_cutpack_v2_final\README_放这里.md` | repo 内默认只承接稳定 cutpack 入口与后续状态表；外部继续承担原始 pdf、重资产原件与追溯位，不整包复制 | 把 `F2` 的“入口/边界/下一步”从本计划抽成可单独引用的短状态块，并补回主文档停点 | repo 内能单独回答“看哪/不看哪/下一刀”，且不回外部目录做默认入口 |

当前 `F1 / F2` 验收口径：

- 不要求整包复制外部原件。
- 只要求 repo 内先形成可单独阅读的状态表与稳定入口。
- 外部继续承担重资产原件层与追溯位，直到 repo 内完成第二阶段收口。

当前 `F1 / F2` 独立短状态块：

- `F1`
  - 当前入口：`GROUP_05_趋势_系统交易\01_F1_cutpack_v2_final\README_放这里.md`
  - 当前边界：repo 内默认只承接 `9` 份正式 md 与后续状态表；外部继续承担原始 pdf、重资产原件与追溯位，不整包复制。
  - 当前下一刀：保持独立短状态块写法，不回退成“待抽短表”；继续只维护主线索引、镜像层与计划层的同口径。
- `F2`
  - 当前入口：`GROUP_01_微观结构_交易所_HFT\01_F2_cutpack_v2_final\README_放这里.md`
  - 当前边界：repo 内默认只承接 `9` 份 ACTIVE md 与后续状态表；`MarketMicrostructureTheory / VWAP / AuctionMarketTheory` 以 `v2_r1` 为准，外部继续承担原件与追溯位。
  - 当前下一刀：保持独立短状态块写法，不回退成“待抽短表”；继续只维护主线索引、镜像层与计划层的同口径。

第二版同口径分区状态表（继续补 `A2 / A5`）：

| 分区 | 当前状态 | 当前入口 | 当前边界 | 下一刀 | 进入下一阶段的条件 |
|------|----------|----------|----------|--------|--------------------|
| A2 | `IN_STAGE2_READY_FOR_STATE_TABLE` | `GROUP_06_Auction_MarketProfile_价格行为\01_A2_cutpack_v2_final\README_放这里.md` | repo 内默认承接稳定入口、定义与后续状态表；外部继续承担原始 cutpack 原件、追溯位与未抽成真值锚点的历史层，不整包复制 | 把 `A2` 的“入口/边界/下一步”抽成短状态块，并和 `GROUP_06` 最小吸收包口径挂齐 | repo 内能单独回答“看哪/不看哪/下一刀”，且默认入口不再回外部 |
| A5 | `IN_STAGE2_READY_FOR_STATE_TABLE` | `GROUP_10_A5_财报_估值_组合管理\README_放这里.md` | repo 内默认承接稳定入口与后续状态表；外部继续承担原始 cutpack 原件、追溯位与重资产层，不整包复制 | 把 `A5` 的“入口/边界/下一步”抽成短状态块，并补到主线镜像层 | repo 内能单独回答“看哪/不看哪/下一刀”，且默认入口不再回外部 |

当前 `A2 / A5` 验收口径：

- 不要求复制整组书库原件。
- 只要求 repo 内先形成“入口明确、边界明确、下一刀明确”的轻量状态表。
- 外部继续保留重资产原件层，直到 repo 内完成第二阶段收口。

当前 `A2 / A5` 独立短状态块：

- `A2`
  - 当前入口：`GROUP_06_Auction_MarketProfile_价格行为\01_A2_cutpack_v2_final\README_放这里.md`
  - 当前边界：repo 内默认承接稳定入口、定义与后续状态表；`市场轮廓理论 part2` 当前仍是 `partial_anchor_cutpack`，旧版继续只作历史副本，外部继续承担原始 cutpack 原件与追溯位。
  - 当前下一刀：保持独立短状态块与 `GROUP_06_最小吸收包_v1.md` 同口径，不回退成待补状态；继续只维护主线索引、镜像层与计划层一致性。
- `A5`
  - 当前入口：`GROUP_10_A5_财报_估值_组合管理\README_放这里.md`
  - 当前边界：repo 内默认承接严格复审通过后的稳定入口与后续状态表；默认正式入口是 `01_A5_cutpack_v1_final/`，当前不重做整组，外部继续承担原件与追溯位。
  - 当前下一刀：保持独立短状态块写法，并只维护库内外一致性；不回退成待补状态，也不扩成整组重做任务。

第二版组级第二阶段状态表（补 `A3 / A4 / A1`）：

| 分区组 | 当前状态 | 当前入口 | 当前边界 | 下一刀 | 进入下一阶段的条件 |
|--------|----------|----------|----------|--------|--------------------|
| A3/A4/A1 | `IN_STAGE2_LIGHT_SPLIT_READY` | `GROUP_09_完善体系书库_切割产物\README_放这里.md` | repo 内当前承接组级稳定入口与轻量子组状态；外部继续承担 cutpack 原件、追溯位和未抽成真值锚点的历史层 | 先保留组级主入口，同时把 `A1 / A3-C1 / A3 extra / A4` 补成轻量子组状态；暂不扩成更重的逐文件状态表 | repo 内能先按“组级主入口 + 子组短状态”回答默认阅读；只有子组再出现独立删除链路或独立下一刀时才继续下沉 |

当前 `A3 / A4 / A1` 验收口径：

- 当前默认保持“组级主入口 + 轻量子组状态”，不直接下沉到更重状态表。
- 只要求 repo 内先形成“子组入口明确、子组边界明确、子组下一刀明确”的最小可读状态。
- 外部继续承担重资产原件与追溯位，直到组内需要的真值锚点与状态表补齐。

当前 `A3 / A4 / A1` 组三段式短表：

- 组级入口：
  - 当前默认先看 `GROUP_09_完善体系书库_切割产物\README_放这里.md`，不回外部目录做默认入口。
- 组级边界：
  - repo 内当前只承接组级稳定入口与后续状态表；外部继续承担 cutpack 原件、追溯位和仍未抽成真值锚点的历史层。
- 组级下一刀：
  - 当前先保持 `A1 / A3-C1 / A3 extra / A4` 的轻量子组状态模板口径；
  - 再视是否真的需要，继续细拆到更重的单子组状态表。

当前 `A3 / A4 / A1` 轻量子组状态模板：

- 子组入口清单：
  - `A1`：`GROUP_09_完善体系书库_切割产物\01_A1_cutpack_v2_final\README_放这里.md`
  - `A3-C1`：`GROUP_09_完善体系书库_切割产物\02_A3C1_cutpack_v2_final\README_放这里.md`
  - `A3 extra`：`GROUP_09_完善体系书库_切割产物\03_A3_extra_cutpack_v2_final\README_放这里.md`
  - `A4`：`GROUP_09_完善体系书库_切割产物\04_A4_cutpack_v2_final\README_放这里.md`

- `A1`
  - 当前入口：`GROUP_09_完善体系书库_切割产物\01_A1_cutpack_v2_final\README_放这里.md`
  - 当前边界：当前稳定入口只认 `v2_r2` 组；`情绪流龙头战法 part2__v2_r1` 继续只作历史副本。
  - 当前下一刀：先维持轻量子组状态并统一模板写法；若进入统一 freeze / archive，优先处理 `part2__v2_r1`。
- `A3-C1`
  - 当前入口：`GROUP_09_完善体系书库_切割产物\02_A3C1_cutpack_v2_final\README_放这里.md`
  - 当前边界：当前正式留存 `9` 份 md，以 FINAL 清单为准；旧版 `v2` 与过渡版 `r1` 不作为正式依赖。
  - 当前下一刀：先维持轻量子组状态并统一模板写法；只在出现独立真值锚点或独立下一刀时再继续细拆。
- `A3 extra`
  - 当前入口：`GROUP_09_完善体系书库_切割产物\03_A3_extra_cutpack_v2_final\README_放这里.md`
  - 当前边界：当前只认本目录正式留存文件；`日本蜡烛图技术新解 / 量价分析威科夫盘口解读方法 / 威科夫操盘法` 以 `v2_r1` 为准。
  - 当前下一刀：先维持轻量子组状态并统一模板写法；不把蜡烛图 / 威科夫再拆成更细分支。
- `A4`
  - 当前入口：`GROUP_09_完善体系书库_切割产物\04_A4_cutpack_v2_final\README_放这里.md`
  - 当前边界：当前稳定入口只认 `04_A4_cutpack_v2_final/`；`Quantitative_Trading` 以 `v2_retry_r2` 为准，根层 A4 重复副本继续只作历史层。
  - 当前下一刀：先维持轻量子组状态并统一模板写法；若进入统一归档，优先处理根层 A4 重复副本。

当前是否需要细拆到单子组的判定短表：

| 组别 | 当前是否必须细拆 | 当前判断 | 触发细拆的条件 |
|------|------------------|----------|----------------|
| A3/A4/A1 | `YES_LIGHT_SPLIT_READY` | 组内已出现 `A1 / A3-C1 / A3 extra / A4` 的独立 `README + manifest` 稳定入口，已满足轻量细拆条件；当前不必继续下沉到更重状态表 | 当子组再出现独立删除前补核链路、独立 coverage 口径、或独立下一刀明显不同且无法共用时再继续下沉 |

触发细拆的更硬示例：

- 若 `A3 / A4 / A1` 中任一子组已经形成独立 `README/manifest/真值锚点`，且默认阅读路径与其他子组不同，则进入“应拆”。
- 若任一子组已经出现独立删除前补核链路、独立 coverage 口径或独立 repo-first 入口，则进入“应拆”。
- 若用户后续明确要求按某个子组持续推进，而该子组的“当前边界/下一刀”不能再与同组其他内容共用，则进入“应拆”。

## 当前最小缺口

- `S` 已压成正式“分区状态表”（`S_BUCKET_REPO_STATE_TABLE__2026-06-26.md`），但 `A* / F*` 仍缺同口径分区表。
- 原件层第二阶段虽然方向明确，但仍需要继续把“当前结论/当前停点/下一刀”压短，减少重复长段叙述。
- `02_游资悟道交割单` 在 repo 内虽然已有 `YZ-A / YZ-B` 对象级真值锚点，但原件层与删除前补核链路仍未退场，当前仍是 `NOT_DELETE_READY`。
- 这意味着主线并未完成；当前只是把默认入口和首批真值锚点承接进 repo，还没有完成第二阶段的全分区收口。

## 下一步最顺动作

1. 先按 `S_BUCKET_REPO_STATE_TABLE__2026-06-26.md` 继续拆 `S` 的原件层。
2. 再继续统一 `A/F` 书库分区模板口径：`F1/F2/A2/A5` 保持独立短状态块，`A1/A3-C1/A3 extra/A4` 保持轻量子组状态。
3. 每完成一刀，同步回写：
   - `03_阶段二_当下计划_执行清单.md`
   - `关于日活.md`
   - `OLD_REPO_TO_NEW_REPO_PROGRESS.md`
