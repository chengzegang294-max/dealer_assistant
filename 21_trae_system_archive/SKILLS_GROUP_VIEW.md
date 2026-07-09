# Skills Group View

## 当前工作副本

- 当前 repo-global 工作副本见：
  - `00_entry\trae_system_transition\TRAE_SYSTEM_SKILLS_GROUP_VIEW__20260709.md`
- 本文件继续承担 `group router` 角色，不改 `.trae` first-hop。

## 角色

- 本文件是 `21_trae_system_archive\SKILLS_INDEX.md` 的主题分组视图。
- 目标是给旧仓 skill 提供一个按主题浏览的 router，不伪造 skill 副本，不替代逐 skill 明细索引。
- 本文件只负责 `group router`，不替代 `active router` 或 `decision index`。

## 分组规则

- `ACTIVE`
  - 已在新仓 `.trae` 落盘，可直接从当前 router 进入
- `CAN_MIRROR_LATER`
  - 旧仓仍有 `SKILL.md`，但当前只保留裁决与回指；若重新成为 first-hop 或需要显式合同副本，再开 mirror 批次

## 主题分组

- `G01 文档与证据合同`
  - `artifact-provenance-note-guard-cn` `ACTIVE`
  - `main-doc-contract-mirror-cn` `CAN_MIRROR_LATER`
  - `proof-of-mapping-standard-cn` `CAN_MIRROR_LATER`

- `G02 主线推进`
  - `mainline-full-ingest-cn` `CAN_MIRROR_LATER`
  - `source-sweep-batch-cn` `CAN_MIRROR_LATER`

- `G03 切割与来源吸收`
  - `tool-idea-ingest-guard` `CAN_MIRROR_LATER`
  - `rolling-playbook-cn` `CAN_MIRROR_LATER`
  - `knowledge-intake-quantize-cn` `CAN_MIRROR_LATER`
  - `dual-epub-pdf-truth-anchor-cn` `CAN_MIRROR_LATER`

- `G04 多 AI 讨论`
  - `multi-ai-suite-entry-cn` `CAN_MIRROR_LATER`
  - `panel-multi-ai-cn` `CAN_MIRROR_LATER`
  - `multi-ai-discussion-guard` `CAN_MIRROR_LATER`
  - `multi-ai-orchestrator-cn` `CAN_MIRROR_LATER`

- `G05 实证与回测（P0）`
  - `p0-suite-entry-cn` `CAN_MIRROR_LATER`
  - `p0-lab` `CAN_MIRROR_LATER`
  - `p0-exec-evidence-officer` `CAN_MIRROR_LATER`
  - `p0-sweep-outbound-guard` `CAN_MIRROR_LATER`

- `G06 工程与风险`
  - `dev-guardrails` `CAN_MIRROR_LATER`
  - `mt5-audit` `CAN_MIRROR_LATER`
  - `mt-indicator-engineering-cn` `CAN_MIRROR_LATER`
  - `indicator-audit-shrink-loop-cn` `CAN_MIRROR_LATER`

- `G07 A 股流水线`
  - `ashare-ops-guard` `CAN_MIRROR_LATER`

## 当前入口

- 当前新仓 workspace 入口：
  - `.trae\README.md`
- 当前新仓 active router：
  - `.trae\skills\INDEX.md`
- 逐 skill 明细索引：
  - `21_trae_system_archive\SKILLS_INDEX.md`
- 当前 legacy archive：
  - `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\README__ARCHIVE_ONLY.md`
- 固定查找顺序：
  - `active router -> decision index -> group router -> legacy archive`
- 当前仓内仍无 `.trae\commands` 实体目录：
  - 本页不伪造 command 分组入口
