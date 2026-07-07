# PLAYBOOK_滚动模板

## TEMPLATE: CUTPACK_V2

VERSION: v2

SCOPE:
- 适用：书籍/研报/pdf/epub 的“删源可用”切割
- 不做：强行把需要 Level2/逐笔/DOM 的内容当成当前可量化

INPUT:
- 单个文件（pdf/epub）或单批文件
- 对应 CUT_CONTRACT

OUTPUT:
- `CUTPACK__<GROUP>__<TITLE_SHORT>__v2.md`
- 太长可拆：`_part1/_part2/_part3`
- 每批生成 `manifest_v2.tsv`

ACCEPTANCE:
- 必须包含 `QUANTIZATION_TABLE`
- 必须包含 `FULL_TEXT` 或 `RETAINED_EXCERPTS`
- `RETAINED_EXCERPTS.quote` 不允许为空

FAILURE_MODES:
- 只切目录索引：拒收
- quote 为空：补切或重切
- 扫描版无文本：标 `NEEDS_OCR`，不假装全文可用

NEXT_ITERATION:
- 把 QUANTIZATION_TABLE 汇总成跨书字段池（去重 + 规范化）

---

## TEMPLATE: SOURCE_INGEST__KIMI_OUTPUT_TO_REPO

VERSION: v1

SCOPE:
- 把 `~kimi输出` 等临时目录的成果迁入 `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库`

INPUT:
- 临时目录下的 md

OUTPUT:
- 按组落盘到对应 `GROUP_XX`
- 产物层与草稿层分离（例如：`06_pdf_retained_cut_v2`、`01_A2_cutpack_v2`）

ACCEPTANCE:
- 临时目录可删除
- 仓库内存在：
  - 产物 md
  - manifest
  - README 说明

FAILURE_MODES:
- 只搬运不验收：拒收
- 文件命名不可追溯：补命名与 manifest

NEXT_ITERATION:
- 增加自动化质量扫描（缺章节/缺表/空 quote）

---

## TEMPLATE: S_BUCKET_FUNCTIONAL_OBJECT_CARD__KIMI_BATCH

VERSION: v1

SCOPE:
- 适用：`S桶 -> 03_券商研报` 已进入代表作 proof 的对象
- 目标：把“来源资料”转成“功能对象卡草稿”
- 不做：删源裁决、最终可用性裁决、伪造公式与输入输出

INPUT:
- 一批 `S_BUCKET_report_representatives_v*.tsv` 中的对象
- 对应的仓库内 staging 文件
- 已有摘要/索引/主线口径

OUTPUT:
- 每篇输出 1 张对象卡草稿，至少含：
  - `object_name`
  - `source_anchor`
  - `function_bucket`
  - `process_layer`
  - `scope_tags`
  - `maturity_level`
  - `input_requirement`
  - `output_form`
  - `best_use_case`
  - `cannot_do_yet`
  - `combines_with`
  - `overlaps_with`
  - `failure_modes`
  - `evidence_note`
- 结尾补一个 `本批归纳摘要`

ACCEPTANCE:
- 不允许只复述标题
- 每篇都必须给出 `function_bucket` 和 `maturity_level`
- 每篇都必须写清 `输入` 和 `输出`，若无法确认必须明确写 `未知/待核`
- 必须显式区分：
  - `alpha/filter/risk/execution/explanation`

FAILURE_MODES:
- 只按标题猜用途：拒收
- 把“看起来像”写成“已实现”：拒收
- 不区分功能角色与成熟度：拒收

NEXT_ITERATION:
- 把对象卡草稿落成仓库内功能映射表
- 增加跨批次去重字段

PROMPT_TEMPLATE:
```text
你现在是“金融研报功能归类助手”，不是写书评，也不是泛泛总结。

任务：
我会给你一批已进入仓库 staging 的研报/书籍对象。请你把它们转成“功能对象卡草稿”，用于后续把来源库逐步转成功能库。

强约束：
1. 不能只复述标题。
2. 不能把推测写成确定结论。
3. 不能把“值得研究”写成“已经可用”。
4. 如果输入/输出/公式无法确认，必须明确写“待核”。
5. 必须显式判断它更像：
   - alpha
   - filter
   - risk
   - execution
   - explanation

请对每个对象输出以下结构：
- object_name:
- source_anchor:
- function_bucket:
- process_layer:
- scope_tags:
- maturity_level:
- role_type:
- input_requirement:
- output_form:
- best_use_case:
- cannot_do_yet:
- combines_with:
- overlaps_with:
- failure_modes:
- evidence_note:

最后再输出：
- 本批共同主题
- 本批可复用对象
- 本批仍然只是概念层的对象
- 建议优先进入下一轮仓库功能映射表的对象
```

---

## TEMPLATE: S_BUCKET_SERIES_MAP__KIMI_BATCH

VERSION: v1

SCOPE:
- 适用：同一系列或同一主题的一批对象，例如：
  - `华泰人工智能系列`
  - `华泰多因子系列`
  - `长江高频因子系列`
- 目标：做系列内部地图、去重、顺序和功能分流

INPUT:
- 同系列 `5-12` 篇对象
- 对应的标题、来源路径、必要摘录

OUTPUT:
- `系列总览`
- `按篇定位表`
- `去重/替代关系`
- `推荐阅读顺序`
- `建议功能分流`

ACCEPTANCE:
- 必须指出每篇在系列中的角色差异
- 必须指出：
  - 哪些互补
  - 哪些基本重复
  - 哪些更适合先进入功能层
- 不允许把整个系列一股脑写成“都很重要”

FAILURE_MODES:
- 只有篇目列表、没有差异判断：拒收
- 没有阅读顺序和分流建议：拒收
- 用模糊词替代功能判断：拒收

NEXT_ITERATION:
- 把系列地图转成功能映射树
- 增加“可组合链路”字段

PROMPT_TEMPLATE:
```text
你现在是“系列研报去重与功能分流助手”。

任务：
我会给你同一系列或同一主题的一批研报。请你不要逐篇孤立总结，而是从“系列地图”的角度输出：
- 每篇在系列中的功能位置
- 哪些内容重复
- 哪些内容递进
- 哪些适合先进入功能库

输出格式固定为：

一、系列总览
- 这个系列主要解决什么问题
- 它更偏：选股 / 择时 / 执行 / 风控 / 归因解释
- 它当前最值得先吸收的 3 个对象

二、按篇定位表
每篇一行，字段为：
- file_name
- 核心主题
- 在系列中的角色
- 与前文重复/递进关系
- 功能标签
- 成熟度判断

三、去重与替代
- 强重复对象
- 可互补对象
- 不建议优先处理对象

四、建议顺序
- 推荐先读顺序
- 推荐先进入功能映射表顺序

五、收口结论
- 这个系列最适合沉淀到哪些功能桶
- 哪些仍然只应停留在来源层
```

---

## TEMPLATE: S_BUCKET_ENTRY_CONTRACT__REPO_FIRST

VERSION: v1

SCOPE:
- 适用：`01_Kimi拆书待入库` 中的 `S_BUCKET` 批次入口文件
- 目标：统一把入口写成“repo 优先、外部目录只作读取位/追溯位”
- 适用对象：
  - 第一轮对象卡批次
  - `priority_read`
  - `round2_focus`
  - `round3_function_core`

REQUIRED_FIELDS:
- `repo 默认入口`
- `repo 真值文件`
- `repo 回帖副本`
- `外部 PDF 读取目录`
- `外部目录角色`

OPTIONAL_EXTENSION_FIELD:
- `扩展字段附注`

SECTION_SIGNAL:
- `本层只收：当前生效入口 / 包级角色 / 固定顺序 / 扩展附注`
- `当前合同层固定顺序：first_round -> priority_read -> round2 -> round3`

PACKAGE_ROLE_RULES:
- 每个包在五字段主合同前，默认先补一行 `包级角色：X包；用于Y`
- 若已形成稳定目标短句，默认再补一行 `包级目标：...`
- 若已形成稳定真值构成，默认再补一行 `包级真值组成：...`
- 若已形成稳定回收态，默认再补一行 `包级回收结果：...`
- 若需闭环回收链路，默认再补一行 `包级回收入口：...` 或 `包级回收来源：...`
- 当前 `S_BUCKET` 推荐角色短句：
  - `first_round`：`文件名初筛包；用于挂接首轮草稿与基础真值映射`
  - `priority_read`：`正文优先精读包；用于锁定可读对象与稳定真值`
  - `round2`：`正文收缩验证包；用于做代表因子与共线性收缩`
  - `round3`：`功能核心固化包；用于把收缩结论压成对象核心卡`
- 当前 `S_BUCKET` 推荐目标短句：
  - `first_round`：`完成文件名初筛，产出对象卡草稿占位`
  - `priority_read`：`完成正文精读，锁定可读对象与稳定真值`
  - `round2`：`完成代表作收缩验证与共线性收缩`
  - `round3`：`固化功能核心对象卡与边界标签`
- 当前 `S_BUCKET` 推荐真值组成：
  - `first_round`：`summary_md + prompt_txt + mapping_tsv + imported_reply_md`
  - `priority_read`：`summary_md + prompt_txt + mapping_tsv + imported_reply_md`
  - `round2`：`readme_md + manifest_tsv + prompt_txt + direct_message_txt + mapping_tsv + imported_reply_md`
  - `round3`：`readme_md + manifest_tsv + prompt_txt + direct_message_txt + mapping_tsv`
- 当前 `S_BUCKET` 推荐回收结果：
  - `first_round`：`imported_reply_in_repo`
  - `priority_read`：`imported_reply_in_repo`
  - `round2`：`imported_reply_in_repo`
  - `round3`：`merged_into_repo_truth`
- 当前 `S_BUCKET round3` 推荐回收来源短句：
  - `round3`：`Kimi 回帖已并回 summary+映射表，暂无单独 imported reply`
- 当前 `S_BUCKET round3` 推荐回收入口短句：
  - `round3`：`summary：S_BUCKET_SUMMARY__2026-06-17.md；mapping_tsv：S_BUCKET_功能映射表_v1.tsv`
- 当前 `NFTRADEZ` 推荐角色短句：
  - `concept_glossary`：`术语真值收缩包；用于统一概念定义与回帖收缩结果`
  - `premarket_template`：`盘前模板收缩包；用于统一模板要素与回帖收缩结果`
- 当前 `NFTRADEZ` 推荐目标短句：
  - `concept_glossary`：`把 ICT 的基础概念收成最小词典条目`
  - `premarket_template`：`把盘前偏见 / DOL / If-Then / 事件日边界收成模板骨架`
- 当前 `NFTRADEZ` 推荐真值组成：
  - `concept_glossary`：`manifest_tsv + prompt_txt + direct_message_txt + batch_readme_md + imported_reply_md`
  - `premarket_template`：`manifest_tsv + prompt_txt + direct_message_txt + batch_readme_md + imported_reply_md`
- 当前 `NFTRADEZ` 推荐回收结果：
  - `concept_glossary`：`imported_reply_in_repo`
  - `premarket_template`：`imported_reply_in_repo`

WRITE_ORDER:
- 先写 `repo 默认入口`
- 再写 `repo 真值文件`
- 再写 `repo 回帖副本`
- 最后才写 `外部 PDF 读取目录` 与 `外部目录角色`

FIELD_RULES:
- `repo 默认入口`
  - 指当前这层推进时默认先打开的 repo 内文件
  - 只能有一个主入口；如需补充，放进 `repo 真值文件`
- `repo 真值文件`
  - 允许列出 `manifest / prompt / README / 回收表`
  - 只写当前层推进真正依赖的 repo 内文件
- `repo 回帖副本`
  - 若已有 imported reply，必须写清路径
  - 若尚无 imported reply，明确写“暂无 repo 回帖副本”，不得拿外部 md 冒充
- `外部 PDF 读取目录`
  - 只写实际需要读取 PDF 的外部目录
  - 不写外部 md、外部 prompt、外部执行入口
- `外部目录角色`
  - 默认写法：`仅作为 PDF 读取位置，不作为默认入口`
  - 若只为历史追溯，不再直接读取 PDF，则写：`仅作为历史追溯位，不作为默认入口`
- `扩展字段附注`
  - 只用于写 `durable truth / 当前对象 / 当前裁决 / 当前结论 / 当前固化结果`
  - 必须放在五字段主合同之后，不能插进主合同中间
  - 不允许新增为第六个主字段；它只是附注层
  - 默认改写成 `key=value` 短句；推荐键名：
    - `decision`
    - `review_status`
    - `durable_truth`
    - `objects`
    - `focus`
    - `result`
    - `ranking`
    - `goal`
    - `state`
    - `fallback`
    - `boundary`
  - 多个键之间用 `；` 分隔；单个键内若有多个值，优先用 `/` 或 `|`，避免整句自然语言扩散
- `proof-of-mapping`（运行时证据产物）
  - 只用于证明“输入字段 -> 输出字段”的可复现映射，不宣称真实接入已完成
  - 默认落点：`12_工具运行时_TOOLING_RUNTIME\<topic>\real_input_samples\`
  - 默认要求：同时给出 `proof_script_py` 与 `proof_output_csv`，并在日活记录一条可复现命令

ACCEPTANCE:
- 同一层的入口文件、README、prompt、direct_message 字段顺序一致
- `03_执行清单` 与来源锚点文档中的入口合同顺序一致
- 外部路径不再承担“先看这里再做”的默认入口语义
- 扩展信息统一收在 `扩展字段附注`，不再散落成多种自由写法

FAILURE_MODES:
- 只有外部目录，没有 repo 默认入口：拒收
- 外部目录和 repo 真值文件混写成一个字段：拒收
- 把 imported reply 写进 `repo 真值文件` 却不单列 `repo 回帖副本`：拒收
- 把外部目录写成“默认入口 / 输入目录 / 请先读取这里”：拒收

NEXT_ITERATION:
- 为 `S_BUCKET` 各轮入口增加统一的 `状态标签 / 当前对象 / durable truth` 扩展字段
- 把该模板推广到 `NFTRADEZ` 等后续 `Kimi` 承接批次

---

## TEMPLATE: MAIN_DOC_CONTRACT_MIRROR__REPO_FIRST

VERSION: v1

SCOPE:
- 适用：`00 / 01 / 02 / 03 / 关于日活` 中需要把同一主线压成镜像结构的场景
- 目标：把 `repo-first` 合同、`当前合同层`、`历史追溯层` 和 `独立化方案` 写成固定顺序
- 当前优先适用：
  - `S_BUCKET`
  - `NFTRADEZ`
  - 后续同类 `Kimi` 承接批次

INPUT:
- 来源锚点文档
- 当前主入口文件
- 当前真值文件列表
- 当前 imported reply 或缺口说明
- 外部目录路径与角色判定

OUTPUT:
- `00_主线检索索引.md` 中的包级入口块
- `01_阶段一_项目记录_过去与落地.md` 中的事实合同块
- `02_阶段二_工作方向_想法库.md` 中的方向合同短块
- `03_阶段二_当下计划_执行清单.md` 中的 `当前合同层 / 历史追溯层`
- `关于日活.md` 中的本轮同步记录

CURRENT_LAYER_RULES:
- 只写当前生效的入口合同和当前结论
- 当前合同层默认先补一行：`本层只收：当前生效入口 / 包级角色 / 固定顺序 / 扩展附注`
- 若当前层包含多包串联，默认再补一行：`当前合同层固定顺序：first_round -> priority_read -> round2 -> round3`
- 若当前层是 `NFTRADEZ` 双包结构，默认也可写：`当前合同层固定顺序：concept_glossary -> premarket_template`
- 字段顺序固定为：
  - `repo 默认入口`
  - `repo 真值文件`
  - `repo 回帖副本`
  - `外部 PDF 读取目录`
  - `外部目录角色`
- 每个包进入五字段主合同前，默认先补：`包级角色：X包；用于Y`
- 若当前主题已有稳定短句，默认继续按顺序补：`包级目标：...`、`包级真值组成：...`、`包级回收结果：...`

HISTORY_LAYER_RULES:
- 只写准备记录、偏差修正、旧回收节点和来源沿革
- 标题必须显式包含：
  - `历史追溯层`
  - 或 `不再作为默认入口说明`
- 不得继续使用：
  - `当前已准备`
  - `当前已完成`
  - `当前默认入口`

INDEPENDENCE_LAYER_RULES:
- 独立化方案只回答：
  - 现在哪些已经脱离外部默认入口
  - 哪些还只是在 repo 内有最小自有子集
  - 哪些外部目录仍只保留为追溯位或 PDF 读取位
- 不把“部分独立”误写成“整体完全脱离外部”

ACCEPTANCE:
- 同一主题在 `00 / 01 / 02 / 03` 中字段顺序一致
- `03` 当前合同层与历史追溯层显式分离
- 外部路径只出现在 `外部 PDF 读取目录` 或历史追溯说明中
- `关于日活.md` 写明这轮同步了哪些层

SUPPLEMENT_ENTRY_RULES:
- 若当前主题存在 `补充入口` 层，默认先补一行：`本层只收：入口类型...`
- 默认再补一行：`固定顺序：...`
- 入口项默认写成：`入口类型：短名：路径`
- 当前推荐入口类型：
  - `总览入口 / 证据入口 / 交接入口`
  - `检查入口 / 证据入口 / 吸收入口 / 候选入口 / 验收入口`
- 当前推荐顺序：
  - `NFTRADEZ`：`总览 -> 证据 -> 交接`
  - `S_BUCKET`：`检查 -> 证据 -> 吸收 -> 候选 -> 验收`

FAILURE_MODES:
- 只改一层文档，没做镜像同步：拒收
- 把 imported reply 混进 `repo 真值文件`：拒收
- 历史段仍写成当前动作：拒收
- 外部目录仍承担默认入口语义：拒收

NEXT_ITERATION:
- 给镜像合同增加统一的 `durable truth / 当前对象 / 状态标签`
- 把更多来源线按同一模板收成 `包级合同块`
- 视需要升级成跨项目通用版

---

## TEMPLATE: KNOWLEDGE_INTAKE_TO_QUANT_PIPELINE_CN

VERSION: v1

SCOPE:
- 适用：新增文件夹 / 视频导出 / 零散方法论笔记 / 外部课程资料
- 目标：把新增知识点收成 `真值副本 -> 分类 -> 量化边界 -> 功能层入口`
- 不做：把主观叙事直接写成可用策略，把案例回放直接写成已验证 alpha

INPUT:
- 外部目录或单批文件
- 最少的来源说明（是谁 / 来自哪 / 大概讲什么）
- 若已有回帖或摘要，一并作为辅助证据

OUTPUT:
- repo 内新目录
- `README.md`
- `manifest_v1.tsv`
- `吸收与分流_v1.md`
- 若能进入功能层，再更新对象卡 / 功能映射表

ACCEPTANCE:
- 外部材料已在 repo 内有真值副本
- 每条材料至少有：
  - `primary_theme`
  - `repo_role`
  - `ingest_decision`
  - `note`
- 必须显式区分：
  - `method_reference`
  - `quant_candidate`
  - `case_replay_only`
- 必须写清：
  - 现在能做什么
  - 现在不能做什么
  - 哪些可继续量化
  - 哪些只应保留为解释层

FAILURE_MODES:
- 只看不入库：拒收
- 只复制文件不写 manifest / README：拒收
- 把视频主观叙事写成量化信号：拒收
- 把案例复盘写成稳定系统：拒收
- 没有输入/输出边界就直接谈组合：拒收

NEXT_ITERATION:
- 增加“从方法论参考到对象卡”的自动桥接字段
- 增加事件日模板 / 盘前偏见模板 / 纪律红线模板
- 增加与既有功能映射表的去重关系
