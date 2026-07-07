# CUT_CONTRACT__Kimi_全文保留优先_v1

目标：把资料切成“删源也可用”的 md。优先保留全文，其次保留高密度原文片段，并同时给出可量化映射表。

适用：短 pdf（文本型）、研报、讲义、帖子集、短书章节。扫描版/图片型文本优先 OCR 后再执行。

## 入口规则（先判定走哪条）

- 若 `source_file_size_mb <= 5` 且正文可直接复制（非严重扫描图）：
  - 走 `FULL_TEXT_RETAIN`：尽量保留全文到 md（保留层级标题与表格）
- 否则：
  - 走 `EXCERPT_RETAIN`：保留 25–60 条高密度原文片段卡片（覆盖定义/规则/边界/公式/反例）

不允许只输出目录索引或纯摘要。

## 输出合同（必须严格按此结构输出）

### MATERIAL_CARD
- title:
- author_or_source:
- material_type:
- domain_tags:
- file_scope:
- source_file_size_mb:
- retain_mode: FULL_TEXT_RETAIN / EXCERPT_RETAIN

### ROUTING_DECISION
- current_repo_role:
  - A_SHARES_FEATURE_POOL
  - A_SHARES_EVENT_DRIVEN
  - A_SHARES_SECTOR_ROTATION
  - A_SHARES_TIMING
  - A_SHARES_DATA_ENGINEERING_GUARD
  - SOURCE_LIBRARY_ONLY
- quantizable_now_ratio_estimate: 0-100%
- needs_extra_data_ratio_estimate: 0-100%
- biggest_leakage_risks:

### CONTENT_CLUSTERS
3–12 个主题簇，每簇写：
- cluster_name:
- what_it_is:
- keep_level: 高/中/低
- repo_mapping:

### QUANTIZATION_TABLE
Markdown 表格，至少 20 行。表头必须是：
`concept | type | minimal_definition | observable_proxy | min_data_requirement | confirmation_timing | quant_status | repo_target | leakage_risk | notes`

### FULL_TEXT
仅当 retain_mode=FULL_TEXT_RETAIN 时必须输出。

要求：
- 尽量保留全文（不要省略到只剩摘要）
- 用 Markdown 标题层级重建结构
- 表格用 Markdown 表格或等宽块保留

### RETAINED_EXCERPTS
仅当 retain_mode=EXCERPT_RETAIN 时必须输出。

要求：
- 25–60 条
- 每条包含：
  - excerpt_id:
  - source_hint:
  - quote:
  - why_kept:
  - quant_link:

### FORMULAS_AND_ALGOS
- 公式/变量定义/步骤（尽量保留原文定义）
- 适用条件与失效条件

### NOT_QUANT_YET
3–12 条，写清楚原因与需要的额外数据/证据。

### NEXT_ACTION
5–12 条，必须可执行。

## 量化状态枚举（必须使用）

- quant_status:
  - proxy_quantizable_now
  - needs_extra_data
  - shell_only
  - future_bucket
  - index_only
