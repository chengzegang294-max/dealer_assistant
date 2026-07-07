# SKILL Directory Triage

日期：`2026-06-24`

## 目标

- 对当前 `.trae/skills` 做一次目录级裁决。
- 明确哪些 `skill` 保留、哪些按套件协同、哪些继续迭代升级、哪些暂不直接删除但进入弃用观察。
- 避免功能相近的 `skill` 在后续对话里继续无边界重叠。

## 当前裁决总则

- 先做 `边界收紧`，后做 `物理合并`。
- 当前不直接删除任何已有 `skill`，除非已经有完整替代物和回退方案。
- 允许“同域多 skill”，但前提是：
  - 入口条件不同
  - 产物不同
  - 收口职责不同
- 若只是同域但分工已足够清晰，则先保留并补边界，不急于物理合并。

## 边界短句

- `main-doc-contract-mirror-cn`
  - 只负责把 `repo-first` 合同、当前/历史分层和 `00 / 01 / 02 / 03 / 关于日活` 压成镜像口径。
- `proof-of-mapping-standard-cn`
  - 只负责把 `proof-of-mapping` 做成可复现证据与落盘口径，不代写四件套镜像，也不替代主线总编排。
- `SKILL_DIRECTORY_TRIAGE`
  - 只负责目录级裁决：`保留 / 合并编排组 / 迭代升级 / 弃用说明`。
- 两者边界固定为：
  - 前者改主文档镜像，不裁决整份 `skill` 目录。
  - 后者裁决 `skill` 目录，不代写四件套主文档合同。

## 第一跳路由（默认）

- 用户说“继续推/多推几步/主线不能丢”：先调 `mainline-full-ingest-cn`
- 用户说“扫库/全量吃透来源库/开下一批”：先调 `source-sweep-batch-cn`
- 用户说“同步 00/01/02/03/日活/入口合同镜像”：先调 `main-doc-contract-mirror-cn`
- 用户说“补 proof-of-mapping/先做映射证据/不污染主合约”：先调 `proof-of-mapping-standard-cn`
- 需要改代码/脚本/CSV 合约：先调 `dev-guardrails`
- 用户明确要求多 AI：先调 `multi-ai-suite-entry-cn`
- 用户要跑 P0 基线/实跑/证据摘录：先调 `p0-suite-entry-cn`

## 一、保留

- `mainline-full-ingest-cn`
  - 角色：主线推进总编排
  - 原因：负责“继续推 / 多推几步 / 主线不散”的总调度，不替代批次扫库或文档镜像
- `source-sweep-batch-cn`
  - 角色：来源库批次扫库与四分流
  - 原因：负责目录级收口与批次流程，不替代主线总编排
- `main-doc-contract-mirror-cn`
  - 角色：`repo-first` 合同、当前/历史分层、四件套镜像同步
  - 原因：刚补上此前缺口，和其他主线 skill 已形成清晰边界
- `multi-ai-suite-entry-cn`
  - 角色：多 AI 三件套统一第一入口
  - 原因：补上“先调哪个多 AI skill”的第一跳缺口
- `p0-suite-entry-cn`
  - 角色：`P0` 域统一第一入口
  - 原因：补上“先走 lab / exec / outbound 哪个”的第一跳缺口
- `rolling-playbook-cn`
  - 角色：模板沉淀与版本滚动
  - 原因：只负责模板，不负责主线推进或文档镜像
- `dev-guardrails`
  - 角色：改动护栏与验证闸门
  - 原因：所有代码/脚本/合同改动都需要这一层安全护栏
- `proof-of-mapping-standard-cn`
  - 角色：proof-of-mapping 标准化与证据落盘
  - 原因：涉及 “先做映射证据/不污染主合约/全库对齐” 时，需要统一三件套与回写口径
- `knowledge-intake-quantize-cn`
  - 角色：新增知识点入库、分层、量化边界
  - 原因：入口条件明确，和来源库批次收口不同
- `tool-idea-ingest-guard`
  - 角色：外部交易/金融工具想法入库
  - 原因：是 `knowledge-intake-quantize-cn` 的“工具想法专项版”，当前仍有独立价值
- `dual-epub-pdf-truth-anchor-cn`
  - 角色：双 EPUB / PDF 真值锚点
  - 原因：处理难用 PDF 与 OCR 冲突时有明确专项边界
- `mt-indicator-engineering-cn`
  - 角色：MT 指标工程闭环
  - 原因：专项工程链条清楚，不能和通用来源库 skill 混掉
- `mt5-audit`
  - 角色：MT5 实盘/执行审计
  - 原因：高风险闸门，必须单独保留
- `ashare-ops-guard`
  - 角色：A 股流水线与冻结区守卫
  - 原因：项目边界与风控规则高度专用
- `p0-lab`
  - 角色：P0 基线实验与规则对齐
  - 原因：实验口径独立，不能混进 sweep 后处理
- `indicator-audit-shrink-loop-cn`
  - 角色：指标家族批量收缩
  - 原因：服务对象与节奏均不同于主线文档镜像

## 二、合并编排组

- `panel-multi-ai-cn` + `multi-ai-discussion-guard` + `multi-ai-orchestrator-cn`
  - 当前裁决：保留三件套，不做物理合并；新增 suite 第一入口，并把旧 first-hop 习惯升级为 `DEPRECATED` 包装层
  - 固定分工：
    - `multi-ai-suite-entry-cn`：只负责第一跳路由
    - `panel-multi-ai-cn`：决定默认参会模型与统一发包模板
    - `multi-ai-discussion-guard`：约束证据包与输出合同
    - `multi-ai-orchestrator-cn`：维护 `OUTBOUND / DIFF / BATCH_CLOSE`
  - 后续动作：第一跳默认只走 `multi-ai-suite-entry-cn`；三件套继续只承担二跳专项职责
- `p0-exec-evidence-officer` + `p0-sweep-outbound-guard`
  - 当前裁决：保留三段分工，不做物理合并；新增 suite 第一入口，并把旧 first-hop 习惯升级为 `DEPRECATED` 包装层
  - 固定分工：
    - `p0-suite-entry-cn`：只负责第一跳路由
    - `p0-lab`：负责基线实验与规则对齐
    - `p0-exec-evidence-officer`：实际运行 sweep/action/eval 与落盘
    - `p0-sweep-outbound-guard`：把现有产物压成对外证据摘录
  - 后续动作：第一跳默认只走 `p0-suite-entry-cn`；`p0-lab / exec / outbound` 继续只承担二跳专项职责

## 三、迭代升级

- `main-doc-contract-mirror-cn`
  - 当前升级点：已支持 `5 字段主合同 + 扩展字段附注`
  - 下一步：把更多来源线压成同一镜像结构
- `rolling-playbook-cn`
  - 当前升级点：已接住 `MAIN_DOC_CONTRACT_MIRROR__REPO_FIRST`
  - 下一步：继续只保留模板沉淀，不再混入主线判断
- `source-sweep-batch-cn`
  - 当前升级点：已明确和 `main-doc-contract-mirror-cn` 的协同顺序
  - 下一步：扫库结束后默认进入镜像同步，不再散写
- `knowledge-intake-quantize-cn`
  - 当前升级点：继续保留“新增知识点入库”总入口
  - 下一步：和 `tool-idea-ingest-guard` 保持“通用入库 / 工具专项”边界

## 四、弃用说明

- 当前无“立即删除”的 `skill`
  - 原因：现阶段重心仍是 `边界收紧 + 迁移包装`，不是物理删目录
- 以下对象正式进入“DEPRECATED 包装层（仅指 generic first-hop 入口）”：
  - `panel-multi-ai-cn`
  - `multi-ai-discussion-guard`
  - `multi-ai-orchestrator-cn`
  - `p0-lab`
  - `p0-exec-evidence-officer`
  - `p0-sweep-outbound-guard`
- 包装层规则固定为：
  - 这些 skill 的功能不弃用，只弃用“用户泛泛描述时直接把它们当第一跳入口”的旧习惯
  - 用户若只是泛泛说“多 AI 一起讨论 / 投票 / 复审”，第一跳必须改走 `multi-ai-suite-entry-cn`
  - 用户若只是泛泛说“跑 P0 / 做基线实验 / 继续 sweep / 整理证据”，第一跳必须改走 `p0-suite-entry-cn`
  - 只有当用户已经明确指定“开 panel / 立证据合同 / 收口回帖 / 规则对齐 / 实际执行 / 对外摘录”时，才允许直接进入对应旧 skill
- 当前仍保持“非 DEPRECATED”的口径：
  - 旧 skill 作为二跳专项能力继续有效
  - 其他非 suite 域 skill 暂不进入 `DEPRECATED` 包装层

## 下一步

- 后续若继续做 `skill` 整理，优先顺序固定为：
  1. 先补边界
  2. 再补协同顺序
  3. 再决定是否物理合并
  4. 最后才写弃用与删除
