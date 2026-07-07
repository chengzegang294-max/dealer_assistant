关于A5
1. **同书/不同书关系**
   - `上市公司财报分析与股票估值.epub` 与 `财务报表分析与股票估值郭永清著.epub`：**不同书**。作者不同（舒泰峰 vs 郭永清），出版社不同（中国纺织出版社 vs 机械工业出版社），目录结构完全不同。
   - `5073 Quantitative Equity Portfolio Management, Second Ed.epub` 与 `Active portfolio management ...pdf`：**不同书**。作者不同（Chincarini/Kim vs Grinold/Kahn），书名不同，出版社不同。

2. **四类优先级重排**
   - `直接可切`：3 本（5073、Active portfolio、上市公司财报）
   - `先人工抽查`：1 本（郭永清）
   - `必须先确认是否图片版PDF`：0 本（Active portfolio PDF 文字层已验证）
   - `暂不满足双EPUB条件`：0 本（A5 无 `*_bycalibre.epub`，且已确认无同书配对需求）

3. **可执行方案表**

| book_name | now_status | first_action | split_plan | why |
|---|---|---|---|---|
| 5073 Quantitative Equity Portfolio Management, Second Ed.epub | ready_to_cut | cut_now | by_chapter | 55个html已按chapter01-08和appendix拆分，toc.ncx和nav.xhtml完整 |
| Active portfolio management  a quantitative approach for providing superior returns and controlling risk.pdf | ready_to_cut | cut_now | by_chapter | PDF文字层已验证，632页可直接按目录书签切分 |
| 上市公司财报分析与股票估值.epub | ready_to_cut | cut_now | by_part_then_chapter | 21个html文件，四大部分结构清晰，章节已拆分 |
| 财务报表分析与股票估值郭永清著.epub | hold | manual_spot_check | hold | 仅5个html大文件，218个锚点未验证，先抽查前3个锚点是否准确定位章节边界 |


关于A2
| md_file | final_role | main_source | cross_check_source | pdf_role | action | notes |
|---|---|---|---|---|---|---|
| CUTPACK__A2__CN__市场轮廓理论__part1__v2_r1.md | knowledge_draft | none | none | layout_anchor_only | downgrade | 扫描版PDF零文字层；FineReader EPUB无Part1章节；calibre EPUB纯图片无文字；全文基于英文companion books知识推断重构 |
| CUTPACK__A2__CN__市场轮廓理论__part2__v2_r2.md | partial_anchor_cutpack | FineReaderOCR_epub | calibre_epub_unusable | layout_anchor_only | keep_current_with_audit_note | FineReader OCR EPUB 可覆盖第1-9章与附录，OCR质量不均；19条 RETAINED_EXCERPTS 已完成 spot check，其中 1-14/16-19 可按 OCR 锚定使用，15 为 partial_ocr_support（A股时段映射属于后加适配）；calibre EPUB 为239张图片的伪 EPUB |
| CUTPACK__A2__Dalton__MarketsInProfile__v2_r1.md | formal_cutpack | pdf_text | none | main_text_source | patch_source_audit | PDF有可用文字层（extracted_MarketsInProfile.txt约422k字符）；无EPUB源；需补BASIC_INFO中SOURCE_AUDIT字段说明主源为PDF文字层提取 |
| CUTPACK__A2__Dalton__MindOverMarkets__v2_r1.md | formal_cutpack | pdf_text | none | main_text_source | patch_source_audit | PDF有可用文字层（extracted_MindOverMarkets.txt约620k字符，混合EN/CN双语）；无EPUB源；需补BASIC_INFO中SOURCE_AUDIT字段说明主源为PDF文字层提取 |
| CUTPACK__A2__Harris__TradingAndExchanges__v2_r1.md | formal_cutpack | pdf_text | none | main_text_source | patch_source_audit | PDF有可用文字层（extracted_TradingAndExchanges.txt约1.6M字符）；无EPUB源；需补BASIC_INFO中SOURCE_AUDIT字段说明主源为PDF文字层提取 |



关于F1
| md_file | patch_scope | main_source | cross_check_source | pdf_role | keep_or_patch | note |
|---|---|---|---|---|---|---|
| CUTPACK__F1__HeikinAshi_剥头皮很有趣__part1__v2_r1.md | source_audit_and_version_log | FineReaderOCR_epub | calibre_epub_unusable | layout_anchor_only | patch_now | frontmatter 补写主源、校对源、PDF 角色；version_log 补记 calibre 不可用 |
| CUTPACK__F1__HeikinAshi_剥头皮很有趣__part2__v2_r1.md | source_audit_and_version_log | FineReaderOCR_epub | calibre_epub_unusable | layout_anchor_only | patch_now | 同上 |
| CUTPACK__F1__HeikinAshi_剥头皮很有趣__part3__v2_r1.md | source_audit_and_version_log | FineReaderOCR_epub | calibre_epub_unusable | layout_anchor_only | patch_now | 同上 |
| CUTPACK__F1__HeikinAshi_剥头皮很有趣__part4__v2_r1.md | source_audit_and_version_log | FineReaderOCR_epub | calibre_epub_unusable | layout_anchor_only | patch_now | 同上 |
| CUTPACK__F1__WyckoffMethod_赠送__v2_r1.md | source_audit_and_version_log | FineReaderOCR_epub | calibre_epub_unusable | layout_anchor_only | patch_now | 同上 |
| CUTPACK__F1__CN__外汇日内交易与波段交易__v2_r1.md | no_change | single_epub | none | layout_anchor_only | keep_current | 单 EPUB 无 calibre 版本，source 记录已正确 |
| CUTPACK__F1__CN__外汇超短线交易_技术结构与价格行为原理__v2_r1.md | no_change | single_epub | none | layout_anchor_only | keep_current | 同上 |
| CUTPACK__F1__ForexPriceActionScalping__v2_r1.md | no_change | pdf_text | none | main_text_source | keep_current | PDF 原生文字版，无 EPUB，source 记录已正确 |
| CUTPACK__F1__TradesAboutToHappen__v2_r1.md | no_change | pdf_text | none | main_text_source | keep_current | 同上 |



关于A3
# A3 审计结论

## 一、逐文件表

| md_file | book_name | current_quality | main_source | cross_check_source | deprecated_source | pdf_role | decision | reason | next_action |
|---|---|---|---|---|---|---|---|---|---|
| CUTPACK__A3__VolumeProfile__v2_r1.md | 投资者交易指南 Volume Profile | good | FineReaderOCR_epub | calibre_epub | old_wrong_epub | layout_anchor_only | keep_current | 双EPUB已交叉校验，内容高度一致，source_audit完整，正文质量高（333行结构化摘录） | no_action |
| CUTPACK__A3C1__筹码分布_陈浩完整版__v2.md | 筹码分布（陈浩完整版） | good | unclear | calibre_epub | none | unclear | patch_source_audit | 当前内容质量高（31KB+结构化摘录+完整公式），但source_audit未指明具体源文件（存在两组命名不同的EPUB+txt），且未记录新发现的valid calibre版。单OCR文本已较稳定（OCR_clean.txt 294KB），无需重切 | patch_source_audit |
| CUTPACK__A3C1__筹码形态手册_part1__v2_r2.md | 筹码分布典型形态查询手册（Part1） | good | FineReaderOCR_epub | none | none | layout_anchor_only | patch_source_audit | 当前内容质量高（42KB结构化），但source_type标注"PDF扫描版OCR"与实际源不符。实际主源为同名非calibre EPUB（7.5MB，含10个xhtml有效文本）；calibre版（4.2MB）已验证为空。需修正source_audit | patch_source_audit |
| CUTPACK__A3C1__筹码形态手册_part2__v2_r2.md | 筹码分布典型形态查询手册（Part2） | good | FineReaderOCR_epub | none | none | layout_anchor_only | patch_source_audit | 同part1，内容质量高（43KB结构化），source_type需修正为EPUB文本提取，并注明calibre版为空 | patch_source_audit |
| CUTPACK__A3C1__跟我学筹码分布_part1__v2_r1.md | 跟我学筹码分布从入门到精通 | good | FineReaderOCR_epub | none | none | none | keep_current | EPUB解压后提取文本完整（extracted_跟我学筹码分布，ch_000-ch_079，最大文件18KB），当前CUTPACK 73KB结构化质量高。无calibre版可用。source_audit可补充提取方法 | no_action |
| CUTPACK__A3C1__从零开始学筹码分布_part1__v2_r1.md | 从零开始学筹码分布 | good | FineReaderOCR_epub | none | none | none | keep_current | EPUB解压后提取文本完整（extracted_congling，ch_000-ch_054，最大文件14KB），当前CUTPACK 65KB结构化质量高。无calibre版可用 | no_action |
| CUTPACK__A3C1__擒住大牛筹码_part1__v2_r1.md | 擒住大牛——筹码分布图入门与技巧（Part1） | good | FineReaderOCR_epub | none | none | none | keep_current | 单EPUB源提取完整（extracted_擒住大牛，ch_01-ch_17，最大文件34KB），CUTPACK 47KB结构化质量高。无calibre版可用 | no_action |
| CUTPACK__A3C1__擒住大牛筹码_part2__v2_r1.md | 擒住大牛——筹码分布图入门与技巧（Part2） | good | FineReaderOCR_epub | none | none | none | keep_current | 同part1，结构化质量高（26KB），source清晰 | no_action |

---

## 二、现在就该动的名单

### 1. 必须双 EPUB 重切
- 无

### 2. 只需重 OCR
- 无

### 3. 只改措辞或 source_audit
- `CUTPACK__A3C1__筹码分布_陈浩完整版__v2.md`：补全 source_audit，明确记录具体使用的源文件（`陈浩筹码分布(完整版).epub` 或 `陈浩筹码分布_OCR_clean.txt`），并注明 valid calibre 版（`陈浩筹码分布(完整版) - Acampo GmbH_bycalibre.epub`，index.html 350KB 有效文本）可用于交叉校验
- `CUTPACK__A3C1__筹码形态手册_part1__v2_r2.md`：修正 source_type 为 "EPUB 文本提取"，注明主源为 `筹码分布典型形态查询手册：一本书把筹码的底细深挖到底!.epub`（main-1.xhtml ~ main-10.xhtml 有效文本），calibre 版已验证为空
- `CUTPACK__A3C1__筹码形态手册_part2__v2_r2.md`：同 part1，修正 source_type 并注明 calibre 版为空

### 4. 当前不动
- `CUTPACK__A3__VolumeProfile__v2_r1.md`：双 EPUB 已完备，source_audit 完整，无需任何动作
- `CUTPACK__A3C1__跟我学筹码分布_part1__v2_r1.md`
- `CUTPACK__A3C1__从零开始学筹码分布_part1__v2_r1.md`
- `CUTPACK__A3C1__擒住大牛筹码_part1__v2_r1.md`
- `CUTPACK__A3C1__擒住大牛筹码_part2__v2_r1.md`

---

## 三、重点说明

### VolumeProfile 为什么保留当前版本
`VolumeProfile` 的 `v2_r1` 是当前 A3 中 source_audit 最完整的一本。它在 VERSION_LOG 中明确记录了：
- 主源：`投资者交易指南 Volume Profile_byFineReaderOCR.epub`（18 个 xhtml 文件，约 197K 字符）
- 校对源：`Volume-Profile-A4 - user_bycalibre.epub`（单 index.html，约 231K 字符）
- 废弃源：`投资者交易指南 Volume Profile.epub`（实为《和谐交易》重复文本，已明确废弃）
- 双版本比对结论：差异 < 5%，内容无实质性冲突

当前版本正文以 FineReaderOCR 版为主源、calibre 版标点校正，已完整覆盖核心概念（POC、四种形状、三种设置、价格行为、交易风格、资金管理）。因此保留当前版本，无需任何改动。

### 陈浩《筹码分布》完整版为什么现在不该做双 EPUB 重切
虽然目录下发现了 valid calibre 版（`陈浩筹码分布(完整版) - Acampo GmbH_bycalibre.epub`，index.html 350KB，有效中文文本），但当前 `CUTPACK__A3C1__筹码分布_陈浩完整版__v2.md` 质量已经很高：
1. 内容量：31KB 结构化摘录，包含完整公式（CKDP、CKDW、CBW、ASR、CYS、博弈K线等）
2. 提取深度：四章核心内容全部覆盖，选股定式（天狐1号）和回测数据保留
3. 单OCR稳定性：非 calibre 版 EPUB（`陈浩筹码分布(完整版).epub`）解压后含 13 个 main-xhtml 有效文本；另有 `陈浩筹码分布_OCR_clean.txt`（294KB）可作为纯文本校验

"当前质量差 + PDF难用 + 单OCR仍不稳" 三个条件均不满足。当前最紧迫的问题不是重切，而是 source_audit 未指明具体使用了哪一组源文件（存在两组不同命名版本）。因此决策为 **只改 source_audit，不做双 EPUB 重切**。

### 筹码形态手册为什么只是 source_audit 问题，不是双 EPUB 问题
经验证：
- 非 calibre 版 EPUB（`筹码分布典型形态查询手册：一本书把筹码的底细深挖到底!.epub`，7.5MB）解压后含 **main-1.xhtml ~ main-10.xhtml**，去标签后中文正文完整（如 main-5.xhtml 含"有迹可循：典型单峰筹码形态"等核心章节），**是有效文本源**
- calibre 版（`... - 未知_bycalibre.epub`，4.2MB）解压后仅 index.html 21KB，去标签后几乎无正文，**已验证为空**
- PDF（41MB）为扫描图版，无文字层

因此：
1. 该书**不存在可用的双 EPUB**（calibre 版无效），所以根本不是"是否该做双 EPUB 重切"的问题
2. 当前 CUTPACK 内容质量高（part1 42KB + part2 43KB），正文提取完整
3. 唯一问题是 source_type 错误标注为"PDF扫描版 OCR"，实际应为"EPUB 文本提取（main-xhtml）"。所以决策为 **只改 source_audit 修正措辞**。
## 2026-06-18 A1-A2-A3-A4-F1-F2 去 cut_file 依赖第二阶段

### 已完成

- 修正 stable entry 索引漂移：`A1 final` 与 `A2 final` 的 `README_放这里.md / manifest_v2.tsv` 已改成只指向当前最新版。
- 修正 `GROUP_09` 根层口径：`A4` 只认 `04_A4_cutpack_v2_final`；根层 4 份 md 视为重复副本，不再作为稳定入口。
- 明确 `A1 / A4 / F2` 的显式检查结论：
  - `A1`：`情绪流龙头战法 part2` 只认 `v2_r2`
  - `A4`：只认 `04_A4_cutpack_v2_final`
  - `F2`：继续只认 `01_F2_cutpack_v2_final`

### 当前待办顺序

1. `A2 part2`：OCR spot check 与 `11 / 12 / 13` 深查均已完成；当前仅保留 `15` 的 A股时段映射为后加适配说明。
2. 旧版冻结：`A1 / A2` 旧副本与 `GROUP_09` 根层 A4 重复副本已补 freeze / archive 说明；当前先保留，不删除。
3. `A3 / F1`：继续只按 `final` 使用，不再回退到 `cut_file` 路径。

### 验收口径

- `README / manifest` 不再指向旧版或根层副本。
- 后续引用 `A1 / A2 / A4 / F2` 时，默认只认 `*_final`。
- `cut_file` 继续仅承担源书与施工辅助角色。

## 2026-06-18 并行主线补充：Batch9

### 当前定位

- `Batch9` 继续纳入当前主线，与 `A1/A2/A3/A4/F1/F2` 并行推进。
- 当前不是目录重构问题，而是“资料是否独立 + 是否已全量吃透 + 还缺哪些源码级证据”问题。

### 当前结论

- `Batch9` 已基本独立，不依赖 `cut_file`。
- `Batch9` 已吃透到批次决策层：已有 `source_manifest / 四分流 / 字段草案 / 重开入口 / 外部AI补源评估`。
- `Batch9` 仍未源码级补全；后续只补缺口，不重做整批结构。

### 当前待办

1. 把 `Batch9` 作为并行批次写进长期主文档与日活。
2. 后续继续按 `batch9_source_manifest.csv` 与 `Batch9_外部AI补源评估_v1.md` 补源码级缺口备注。
3. 保持 `batch9_sources_kimi` 只作补强层，不上升为原始真值层。

## 2026-06-18 本轮收口补充

### 已完成

- `A2 part2`：Excerpts `11 / 12 / 13` 已通过第八章正文上下文深查，从 `knowledge_inference` 回升为 `direct_ocr_support`。
- `Batch9`：已把 Kimi 二次整理稿统一压成 `secondary_structured_note / secondary_structured_note_conflict` 两类标签，并写回 `batch9_source_manifest.csv` 的 `notes`。

### 下一步顺序

1. 任务六：继续按目录层推进更远资料与旧来源库四分流，优先 `TK / 原子化拆解 / 交易系统书籍 / Batch9`。
2. `Batch9`：继续只按 `source_manifest` 补源码级缺口备注，不重做结构。
3. `A3 / F1`：继续只认 `final` 目录与稳定入口。

## 2026-06-18 任务六当前版

### 当前四分流

- 已吸收：
  - `Batch9` 的最小合同层
  - `TK` 的 `IB/DB/CB + Fib + TK-R6/7/8` 来源锚点
  - `交易系统书籍` 中已成型的方法学/规则壳
- 可重开：
  - `02_原子化拆解文件`
  - `交易系统书籍` 的海龟 / VanTharp / 资金管理
  - `大隐体系` 的 `stochastic / B转A / 楔形与内部子浪`
  - `周期女王` 的 `状态机 / 10日区间前十 / 包容度与领涨持续`
- future bucket：
  - `大隐体系` 的超短频率层
  - `周期女王` 的案例/临盘视频
  - `Smile_SMC交易系统2_0`
- 仅来源库保留：
  - 图片资产
  - 纯教学转写
  - `batch9_sources_kimi`
  - `01_Kimi拆书待入库` 中的 `secondary_structured_note / inbox_only`
  - `S桶` 交割单成绩型资料（已裁决删除，不入库、不切）

### Kimi 职责

- `A1/A2/A3/A4/F1/F2`：不再常驻负责，不必继续养旧对话框。
- 默认只在这三类情况再叫：
  - 新资料初扫
  - 外部网页补源
  - 我点名的证据缺口补强
  - `S桶`：基于索引做 `03_券商研报` 主题聚类与“研报卡片”框架、以及 `01_集合竞价教程` 的规则卡片目录

### S 桶下一步

1. 冻结 `final_selected_v2` 为 `03_券商研报` 第一批正式候选池：
   - `30` 份总池
   - `27` 份进入 `extract_text_then_card`
   - `3` 份进入 `future_bucket`
2. 对这 `27` 份统一按 `8` 字段模板提取：
   - `one_line_theme`
   - `core_hypothesis`
   - `data_dependency`
   - `candidate_fields`
   - `frequency`
   - `market_scope`
   - `can_map_to_fx`
   - `why_or_why_not`
3. `01_集合竞价教程` 先只验证 `p0` 级卡片：
   - `R01 / R02 / R09 / R05 / R08 / R16 / R19`
4. `02_游资悟道交割单(epub/docx)` 先只验证 `p0` 级方法论卡片：
   - `M01 / M02 / M03 / M08 / M05 / M06 / M11`
5. 当前不允许把 `title_or_folder_inference` 直接当成可入库锚点卡片。
6. 当前已可先收第一批“准入库候选”：
   - 规则卡片：
     - `R01 / R02 / R03 / R22` 作为 `direct_text_support` 首批候选
     - `R04 / R11 / R21 / R23 / R25` 作为 `excerpt_support_but_not_full_rule` 次级候选
   - 当前已先完成独立落盘的首批执行面：
     - `R01 / R02 / R03 / R04 / R21 / R22 / R23 / R25`
     - 已写入 `10_来源库_SOURCE_LIBRARY\02_原子化拆解文件`
     - 其中 `R03` 明确保留为观察卡，不升级为单一买点公式
   - 方法论卡片：
     - `M01 / M02 / M03 / M05 / M08 / M10 / M11 / M12 / M13 / M15 / M16 / M17` 进入首批候选复核池
7. 当前优先补的缺口：
   - `R09`：已降级为 `title_or_folder_inference`，当前先不再继续抬高
   - `M06 / M07 / M14`：已确认是空壳 `epub`，除非单开 `spot_ocr`，否则不再继续追
   - `M18 / M20`：当前正文与目标卡片概念不够贴合，先保留低证据壳
8. `03_券商研报` 的 `27` 份 `8` 字段表已完成，下一步只做二次收缩：
   - `yes = 9`
   - `partial = 4`
   - `no = 14`
9. 当前最顺动作不是“把 9 份一起上主线”，而是：
   - 从 `yes = 9` 中再挑 `1-2` 个最纯时间序列对象
   - 先做 `diag-only / proof-of-mapping`
10. 当前继续保留的首批候选复核池更新为：
   - 方法论卡片新增：
     - `M04 / M19` 已从低证据壳提升到 `excerpt_support_but_not_full_rule`
11. `yes = 9` 当前已完成首批对象收缩：
   - `RSJ 市场情绪冷暖剂`
   - `高频价量相关性因子`
12. 这两条线当前只推进到：
   - `后续对象定义入口`
   - `P0 最小合同`
   - `proof-of-mapping`
   - `runtime notes`
   - `output header`
   - `params template`
   - `append stub`
   - `runtime csv`
   - 且已完成 `dry-run + persist`
   - `raw/bar window 接口空壳`
   - 且已完成一次只读 `--dry-run`
   - `raw/bar window input contract`
13. 这两条线当前不再叫 `Kimi` 主导，只保留我继续往下推：
   - 下一步优先：
     - 若继续 `RSJ`：再决定 raw-window 真实绑定所需 schema/样本
     - 若继续 `价量相关性`：再决定 bar-window 真实绑定所需 schema/样本
     - 否则转回主线，继续从 `yes=9` 的剩余对象里再选下一条
14. `S桶` 当前状态固定写法：
   - 已完成目录级收口
   - 已完成候选池收口
   - 已完成首批对象收口与 runtime 化
   - 未做全桶全文切分，也不以此为当前目标
15. `Kimi` 在 `S桶` 当前只保留：
   - 补源
   - 补正文锚点
   - 不再主导首批对象选择与主推进

## 2026-06-18 任务六下一轮执行顺序

### 首批明确可重开对象

- `00_大隐体系`
  - `stochastic oscillator 指标组`
  - `B转A失败 -> B浪C反手 / 天王山 / 中枢反手`
- `00_周期女王`
  - `周期状态系统规则壳`
  - `10日区间前十 + 前交易日领涨 + 包容度/补位协同`
- `02_原子化拆解文件`
  - `技术指标_随机指标_多周期KD共振与过滤规则`
  - `核心技术_威科夫_弹簧Spring与上抛UT量化判定`（已补 DIAG_ONLY 对象入口 + 最小合同 v1 草案）

### 当前推进顺序

1. 先从 `02_原子化拆解文件` 的 `多周期KD` 与 `Spring/UT` 里各选一个最小实现入口。
2. 再把 `周期女王` 的 `状态机规则壳` 压成 `A股状态标签 / 观察清单`，先不碰案例层。
3. `大隐体系` 先做 `stochastic`，`B转A失败` 仅保留为 `diag-only candidate`。

### 当前不抢做

- `ALBrooks 趋势强度评分`
- `题材标选_中军筛选五维量化模型`

## 2026-06-18 多周期KD 下一步

### 已完成

- 已落 `多周期KD` 三层文件：
  - 对象定义入口
  - `P0` 最小实施草案
  - 真实字段输出路径草案
- 已补第一版输出证据：
  - `kd_mtf_p0_field_header_v1.txt`
  - `kd_mtf_p0_contract_notes_v1.md`
  - `kd_mtf_p0_field_sample_v1.csv`
- 已补运行时空壳：
  - `kd_mtf_p0_fields_runtime_v1.csv`
  - `kd_mtf_p0_fields_runtime_header_v1.txt`
  - `kd_mtf_p0_runtime_notes_v1.md`
  - `kd_mtf_p0_runtime_gaps_v1.md`
  - `kd_mtf_p0_runtime_append_protocol_v1.md`
  - `kd_mtf_p0_real_input_mapping_draft_v1.md`
- 已补第一份手工 proof 样本：
  - `real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `real_input_samples\kd_mtf_p0_proof_output_v1.csv`
- 已补 runtime 参数与 dry-run 验收：
  - `kd_mtf_p0_runtime_params_template_v1.json`
  - `kd_mtf_p0_runtime_append_stub_v1.py`
  - `kd_mtf_p0_runtime_append_acceptance_v1.md`
- 已完成首批 persist：
  - `kd_mtf_p0_fields_runtime_v1.csv` 已写入 `3` 行 proof 行

### 第一版字段范围

- 只做 `6` 个字段：
  - `kd_week_bias`
  - `kd_day_signal`
  - `kd_4h_confirm`
  - `kd_alignment_tier`
  - `kd_direction_filter`
  - `kd_week_extreme_zone`

### 下一步顺序

1. 补第二批 proof 样本
2. 若继续推进，再补 `append_from_proof` 独立脚本
3. 最后再看是否值得扩到 `M15/H4` 或第二品种

### 当前不做

- `month bias`
- `1h refine`
- `背离 / 离散 / 完美`
- 仓位倍率字段

## 2026-06-18 A5 接回承接 + 多周期KD 第二批 proof

### 已完成

- `A5` 已接回来源库候审承接区：
  - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_10_A5_财报_估值_组合管理\01_A5_cutpack_v1_final`
- 已完成 `4` 本书的非破坏式复制与候审入口收口：
  - `5073` 以 `contents.md` 为入口
  - 其余 `3` 本继续以 `INDEX.md` 为入口
- 已新增：
  - `README_放这里.md`
  - `manifest_v2.tsv`
- `多周期KD` 第二批 proof 已补入 `v1`：
  - 新增 `GBPUSD` 的 `down + short_preferred + s tier`
  - 新增 `USDJPY` 的 `week = unknown + day/4h 同向 + a tier`
- 已再次完成 dry-run：
  - `rows_before_cleanup = 3`
  - `proof_rows_loaded = 5`
  - `rows_after_append = 5`
- 已完成第二次 `--persist`：
  - `kd_mtf_p0_fields_runtime_v1.csv` 当前已写回 `5` 行

### 当前状态

- `A5` 当前已进入“来源库正式通过并入库完成”状态。
- `A5` 当前严格验收结论为：
  - `5073 / Active Portfolio / 上市公司财报分析与股票估值 / 财务报表分析与股票估值_郭永清` 当前均已通过
  - `郭永清` 这本的第10章当前已通过：
    - `PDF_text_layer` 主文字源
    - `bycalibre_epub` 文字校对
    - `EPUB_remake` 表格结构辅助
    - `表10-6` 已根据图版 + 用户贴回数字手工重排成 md 表格
- `多周期KD` 当前已进入“第二批 proof 已 persist，runtime csv = 5 行”状态。
- `A2 / A3` 本轮严格复核后，当前结论收紧为：
  - `A2`：继续维持 `keep_current / keep_current_with_audit_note`，不扩到整组重切
  - `A3`：继续维持“主规则可用、案例图注降级为辅助、只补 residual source_audit”
- `A3` 的 residual source_audit 当前已补齐：
  - `陈浩完整版`
  - `筹码形态手册 part1`
  - `筹码形态手册 part2`
- 任务六 Batch4（`00_交易系统书籍`）本轮重新收口为：
  - `已吸收`：`墨菲 / Kaufman / 海龟`
  - `可重开`：`VanTharp`、`海龟`
  - `future bucket`：`Kaufman` 压力轴细化、`墨菲` 图表形态系统化
  - `仅来源库保留`：`archive / vt_images / 99_流程模板`

### 下一步顺序

1. 任务六下一步继续从 `00_交易系统书籍` 的 `可重开` 中做首批对象层推进：
   - `VanTharp -> R乘数/期望/头寸规模`（已落对象入口 + 最小合同 + 首份 proof-of-mapping）
   - `海龟 -> 破产风险/单位规模/灾难压力测试`
2. `VanTharp` 当前只做 `diag-only / proof-of-mapping`，不提前接入真实头寸控制。
3. `VanTharp` 的 `initial_risk_amount` 当前已冻结为双口径并提供 v2 对照样本：
   - `statement_amount`（来自交割单金额字段）
   - `entry_stop_calc`（来自 entry/stop 换算）
4. `多周期KD` 当前暂不值得补 `append_from_proof` 独立脚本，优先保留现有 `append stub`。
5. 之后再看是否值得扩到 `M15/H4` 或第二品种。
6. `GROUP_05` 的“四轴状态模板”已建立后续对象入口：
   - `10_来源库_SOURCE_LIBRARY\02_原子化拆解文件\趋势系统交易_四轴状态模板_后续对象定义入口_v1.md`
   - 下一步只选 `1-2` 个字段做 `diag-only` 的最小 proof-of-mapping，不直接进门控。

## 2026-06-19 双线并行当前轮

### 已完成

- `RSJ` 已新增：
  - `rsj_state_p0_raw_window_sample_schema_v1.md`
  - `real_input_samples\rsj_state_p0_raw_window_sample_input_v1.csv`
  - `rsj_state_p0_validate_raw_window_sample_v1.py`
  - `rsj_state_p0_raw_window_sample_acceptance_v1.md`
  - `rsj_state_p0_validate_raw_window_mapping_v1.py`
  - `rsj_state_p0_raw_window_mapping_acceptance_v1.md`
  - `rsj_state_p0_validate_append_compatibility_v1.py`
  - `rsj_state_p0_append_compatibility_acceptance_v1.md`
  - `rsj_state_p0_simulate_append_diff_v1.py`
  - `rsj_state_p0_simulate_append_diff_acceptance_v1.md`
  - `rsj_state_p0_export_replay_preview_v1.py`
  - `rsj_state_p0_replay_preview_rows_v1.csv`
  - `rsj_state_p0_replay_preview_acceptance_v1.md`
  - `rsj_state_p0_validate_replay_preview_acceptance_v1.py`
  - `rsj_state_p0_replay_preview_acceptance_validation_v1.md`
- `PV Corr` 已新增：
  - `pv_corr_state_p0_bar_window_sample_schema_v1.md`
  - `real_input_samples\pv_corr_state_p0_bar_window_sample_input_v1.csv`
  - `pv_corr_state_p0_validate_bar_window_sample_v1.py`
  - `pv_corr_state_p0_bar_window_sample_acceptance_v1.md`
  - `pv_corr_state_p0_validate_bar_window_mapping_v1.py`
  - `pv_corr_state_p0_bar_window_mapping_acceptance_v1.md`
  - `pv_corr_state_p0_validate_append_compatibility_v1.py`
  - `pv_corr_state_p0_append_compatibility_acceptance_v1.md`
  - `pv_corr_state_p0_simulate_append_diff_v1.py`
  - `pv_corr_state_p0_simulate_append_diff_acceptance_v1.md`
  - `pv_corr_state_p0_export_replay_preview_v1.py`
  - `pv_corr_state_p0_replay_preview_rows_v1.csv`
  - `pv_corr_state_p0_replay_preview_acceptance_v1.md`
  - `pv_corr_state_p0_validate_replay_preview_acceptance_v1.py`
  - `pv_corr_state_p0_replay_preview_acceptance_validation_v1.md`
- `临时粘贴区_外部AI与终端输出.md` 已补一份新的 `S桶收缩任务书 v_next`，可直接发给 `Kimi`。
- `Kimi` 最新贴回已形成 4 张可直接吸收的收口表：
  - `detach_now_queue_v1`
  - `normalize_target_names_v1`
  - `minimal_reopen_queue_v1`
  - `freeze_confirm_v1`

### 当前顺序

1. 继续保持 `RSJ / PV Corr` 只在 `cross-line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance layer`，不升级为 live binding。
   - 已补：
     - `rsj_state_p0_validate_replay_chain_v1.py`
     - `pv_corr_state_p0_validate_replay_chain_v1.py`
   - 已补：
     - `rsj_state_p0_replay_chain_acceptance_v1.md`
     - `pv_corr_state_p0_replay_chain_acceptance_v1.md`
   - 已补：
     - `rsj_state_p0_export_chain_summary_index_v1.py`
     - `pv_corr_state_p0_export_chain_summary_index_v1.py`
     - `rsj_state_p0_chain_summary_index_v1.md`
     - `pv_corr_state_p0_chain_summary_index_v1.md`
   - 已补：
     - `rsj_state_p0_validate_chain_summary_acceptance_compare_v1.py`
     - `pv_corr_state_p0_validate_chain_summary_acceptance_compare_v1.py`
     - `rsj_state_p0_chain_summary_acceptance_compare_v1.md`
     - `pv_corr_state_p0_chain_summary_acceptance_compare_v1.md`
     - `rsj_state_p0_export_manifest_freeze_v1.py`
     - `pv_corr_state_p0_export_manifest_freeze_v1.py`
     - `rsj_state_p0_manifest_freeze_v1.md`
     - `pv_corr_state_p0_manifest_freeze_v1.md`
   - 已补：
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_manifest_index_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_manifest_index_v1.md`
   - 已补：
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_compare_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_compare_v1.md`
   - 已补：
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_manifest_acceptance_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_manifest_acceptance_v1.md`
   - 已补：
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_chain_index_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_chain_index_v1.md`
   - 已补：
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_chain_acceptance_compare_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_chain_acceptance_compare_v1.md`
   - 已补：
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_chain_manifest_acceptance_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_chain_manifest_acceptance_v1.md`
   - 已补：
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_index_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_index_v1.md`
   - 已补：
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_acceptance_compare_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_acceptance_compare_v1.md`
   - 已补：
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_manifest_acceptance_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_manifest_acceptance_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_chain_index_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_chain_index_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_chain_acceptance_compare_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_chain_acceptance_compare_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_chain_manifest_acceptance_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_chain_manifest_acceptance_v1.md`
   - 已补：
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_index_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_index_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_acceptance_compare_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_acceptance_compare_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_manifest_acceptance_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_manifest_acceptance_v1.md`
   - 已补：
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_chain_index_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_chain_index_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_chain_acceptance_compare_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_chain_acceptance_compare_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_chain_manifest_acceptance_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_chain_manifest_acceptance_v1.md`
   - 已补：
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_index_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_index_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_acceptance_compare_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_acceptance_compare_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_manifest_acceptance_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_manifest_acceptance_v1.md`
   - 已补：
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_chain_index_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_chain_index_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_chain_acceptance_compare_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_chain_acceptance_compare_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_chain_manifest_acceptance_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_chain_manifest_acceptance_v1.md`
   - 已补：
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_index_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_index_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_acceptance_compare_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_acceptance_compare_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_manifest_acceptance_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_manifest_acceptance_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_chain_index_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_chain_index_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_chain_acceptance_compare_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_chain_acceptance_compare_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_chain_manifest_acceptance_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_chain_manifest_acceptance_v1.md`
   - 已补：
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_index_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_index_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_acceptance_compare_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_acceptance_compare_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_manifest_acceptance_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_manifest_acceptance_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_chain_index_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_chain_index_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_chain_acceptance_compare_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_chain_acceptance_compare_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_chain_manifest_acceptance_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_chain_manifest_acceptance_v1.md`
   - 已补：
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_index_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_index_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_acceptance_compare_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_acceptance_compare_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_manifest_acceptance_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_manifest_acceptance_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_chain_index_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_chain_index_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
     - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
  - 已补：
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_chain_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_chain_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
  - 已补：
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_chain_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_chain_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
  - 已补：
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
  - 已补：
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
  - 已补：
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
  - 已补：
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
  - 已补：
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
  - 已补：
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
  - 已补：
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
  - 已补：
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
  - 已补：
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
  - 已补：
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
  - 已补：
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
2. 第二条线已先把 `detach_now_queue_v1` 落到最小执行面：
   - 已新建首批 `8` 张 `A股竞价规则卡片`
   - 已从“回查锚点”推进到“独立卡片落盘”
3. 若继续第二条线，优先决定：
   - 是继续补 `R05-R20` 的低成本重开
   - 还是切到 `A股心法方法论卡片` 首批落盘
4. `S桶` 继续保留为可持续第二条线：
   - 可继续追
   - 可分发给 `Kimi` 做补缺口与收缩
   - 若需要重做 `OCR`，必须先报用户确认
5. `minimal_reopen_queue_v1 / freeze_confirm_v1` 继续作为本周期边界，不做整桶重扫。
6. 若继续主线，最顺动作优先看：
  - 直接平移并补齐一层 `cross-line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super index / compare / manifest acceptance`
  - 再接同层 `chain index / chain acceptance compare / chain manifest acceptance`
  - 若阶段性停靠，则当前冻结顶应改认 `super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance`
7. 编码抢救 `batch1` 已开只读诊断，下一步优先顺序：
  - 先处理 `99_活跃主文档损坏前备份_20260611_planb_pre_rebuild` 的 `4` 个主文档
  - 再处理两套 config 中可直接按文本看的文件：`mt4probe_volty*.ini`、`terminal.ini`、`servers.ini`
  - 暂不直接硬转：`accounts.ini`、`community.ini`、`email.ini`、`notifications.ini`、`publish.ini`、`server.ini` 与部分私有配置
