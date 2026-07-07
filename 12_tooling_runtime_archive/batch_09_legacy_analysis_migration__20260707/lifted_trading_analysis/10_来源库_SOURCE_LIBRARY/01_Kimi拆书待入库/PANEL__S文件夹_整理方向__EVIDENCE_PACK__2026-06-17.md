# PANEL：S 文件夹怎么处理（不重复、不浪费额度）

TASK：

我们有一个超大来源目录 `D:\Stock\cut_file\S`，文件很多，重复多，希望做到：

- 有序：目录结构清晰、可检索
- 不重复：重复文件可自动识别与去重
- 不浪费额度：优先用非 AI 方式做盘点/去重/分桶，只把“高价值少量文件”交给 AI 深切
- 可执行：明确“第一批做什么”“输出落在哪”“如何验收”

CONSTRAINTS：

- 不能假设云端模型能访问本机路径；需要用 EVIDENCE PACK 的摘录与统计数据做决策。
- S 文件夹里主要是 PDF，很多带 `(1)`，疑似重复下载。
- 我们最终资产以仓库内 `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/...` 的 `md` 为准，源文件长期放 `D:\Stock\cut_file\...`。

---

## EVIDENCE PACK 1：目录盘点与重复证据（自动统计）

目录：`D:\Stock\cut_file\S`

### 1) 总量与类型

- FILES_TOTAL = 879
- 扩展名分布：
  - `.pdf` = 823
  - `.md` = 46
  - `.docx` = 7
  - `.doc` = 3

### 2) 顶层子目录与规模

- `券商研报`：676
- `游资交割单+悟道心法`：152
- `集合竞价教程`：50

### 3) 重复文件（按“去掉 (1)”归一化后的重复组）

- DUP_GROUPS_TOTAL = 169
- TOP_DUP_GROUPS（示例，norm | copies | total_mb | sample1 | sample2）：
  - monte carlo methods in financial engineering.pdf | 2 | 80.42 | Monte Carlo Methods in Financial Engineering(1).pdf | Monte Carlo Methods in Financial Engineering.pdf
  - option volatility and pricing.pdf | 2 | 50.9 | Option Volatility and Pricing(1).pdf | Option Volatility and Pricing.pdf
  - hands-on machine learning for algorithmic trading.pdf | 2 | 49.74 | Hands-On Machine Learning for Algorithmic Trading(1).pdf | Hands-On Machine Learning for Algorithmic Trading.pdf
  - algorithmic-and-high-frequency-trading-pdf-free.pdf | 2 | 62.25 | algorithmic-and-high-frequency-trading-pdf-free(1).pdf | algorithmic-and-high-frequency-trading-pdf-free.pdf
  - machine learning for algorithmic trading.pdf | 2 | 34.73 | Machine Learning for Algorithmic Trading(1).pdf | Machine Learning for Algorithmic Trading.pdf

推断：重复主要来自重复下载（同名+`(1)`），用哈希/大小可进一步验证并自动去重。

---

## EVIDENCE PACK 2：S 内部内容样例（md 摘录）

说明：S 里大部分是 PDF，这里提供两份 `.md` 的真实内容摘录，作为“资料风格”证据。

### 2.1 集合竞价教程（视频导出 md）摘录

文件：
`D:\Stock\cut_file\S\集合竞价教程\02.老姜《盘口集合竞价战法》共5集\01.什么是集合竞价+02.集合竞价买卖技法+03.集合竞价交易细节_merged.mp4_导出.md`

摘录（节选）：

- “9:15-9:20 允许撤单，9:20-9:25 锁定阶段，不接受撤单”
- “白点越密集代表交投越活跃；量柱放量推升预示异动”
- “集合竞价核心基于最大成交量原则撮合，产生唯一开盘价”

### 2.2 游资交割单/心法（交割单类资料已裁决删除）

说明：

- `游资交割单 游资语录\29位交割单` 已按“历史交易成绩型、难结构化、对主线价值低”的裁决删除。
- 后续 S 文件夹的处理不再以“交割单类 PDF 深切”为目标，优先处理可结构化的导出数据/研报/教程类材料。

---

## EVIDENCE PACK 3：券商研报子目录命名特征（文件名即证据）

路径：`D:\Stock\cut_file\S\券商研报\...`

文件名可见主题集中在：

- 高频/Level2/逐笔/订单簿：如“Level2行情选股因子初探”“基于逐笔成交数据的高频因子梳理”“订单失衡及价差因子”等
- 高频因子体系化：如“高频因子研究框架”“高频因子在不同周期和域下的表现”
- 机器学习 + 高频：如“基于深度学习的高频因子挖掘”“注意力机制优化高频因子”
- 指数增强/多因子：如“高频调仓对多因子模型的收益增强”“剔除空头组合后的指数增强”

同时存在大量 `(1)` 重复版本，适合先自动去重再决定深切优先级。

---

## QUESTIONS（请面板回答）

Q1：S 文件夹应该采用哪种“分层+去重+少量深切”的总体策略，才能最省额度且不乱？

- A：先自动去重+自动分桶，只对每桶 Top-N 资料做 Kimi 深切（其余只做索引）
- B：先用 AI 做目录级主题聚类，再决定去重与深切（成本更高）
- C：按资料类型分线：研报走“章节卡片+量化字段”，视频导出走“规则卡片+可观测代理”
- D：其他（请给可执行流程）

Q2：对重复文件（大量 `(1)`）的处理口径应该是什么？

- A：哈希完全一致则删重复，只留一份（节省空间）
- B：保留一份作为主源，其余改名归档到 `_duplicates/`（保留追溯）
- C：不动源文件，只在索引/manifest 里标记 keep/drop（最稳但目录仍乱）

Q3：对 `券商研报` 这种大量 PDF，AI 深切的“最低必要单位”应该是什么？

- A：每份研报都做 cutpack v2（最全但最耗额度）
- B：先做“标题+摘要+关键公式/表格字段卡片”，只深切 Top 20（更省）
- C：按主题合并成“研报专题 master”，只保留高密度摘录（删源可用）

Q4：请给出一个“第一批 10 个文件”的选择规则（不用点名具体文件），要求：

- 能直接服务 A 股主线（集合竞价/情绪/龙头/高频因子/指数增强）
- 不依赖不可得数据（或明确标 needs_extra_data）
- 可在 1-2 天内完成一轮收口（不需要跑回测）

---

## OUTPUT CONTRACT（面板输出格式）

请严格按此输出：

VOTE: Q1=<A/B/C/D>; Q2=<A/B/C>; Q3=<A/B/C>
- 证据/漏洞点1（引用上面 EVIDENCE PACK 的数字/摘录）
- 证据/漏洞点2
- 建议下一步（1-2条，可执行、可验收）

