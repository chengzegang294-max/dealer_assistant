# Skills Index

## 角色

- 本文件用于承接旧仓 `.trae/skills` 的全量清单、迁移裁决和当前入口规则。
- 目标不是把所有旧 skill 立即复制进新仓，而是先把“哪些还活着、哪些只保留旧仓、哪些后续按需镜像”说清楚。

## 迁移裁决规则

- 本文件不是当前调用入口，而是旧 skill 的迁移裁决索引。
- 当前新仓可直接调用的 `.trae` skill 只有：
  - `artifact-provenance-note-guard-cn`
- 旧 skill 若尚未镜像到新仓，不在 `.trae` 目录制造伪副本。
- 需要追溯旧 skill 正文时：
  - 先看 `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\INDEX.md`
  - 再按本文件的 `decision/status` 判断是否值得重开镜像批次

## 当前状态总览

- `old_repo_trae_skills_inventory_count=22`
- `new_repo_has_copy=1`
- `mirror_later=21`
- 当前唯一已在新仓 `.trae` 落盘的 skill：
  - `artifact-provenance-note-guard-cn`

## 逐技能回指规则

- `legacy_skill_file_template=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\<skill_name>\SKILL.md`
- `active_router=.trae\skills\INDEX.md`
- `decision_router=21_trae_system_archive\SKILLS_INDEX.md`
- `group_router=21_trae_system_archive\SKILLS_GROUP_VIEW.md`
- `mirror_trigger`
  - 只有当某个旧 skill 重新成为当前 first-hop、或需要 repo 内显式合同副本时，才重开 mirror 批次
- `same_name_disambiguation`
  - `p0-exec-evidence-officer` 同时存在 `skill` 与 `agent prompt`
  - `skill` 看：`12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\p0-exec-evidence-officer\SKILL.md`
  - `prompt` 看：`21_trae_system_archive\batch_02_selected\p0-exec-evidence-officer_PROMPT.md`

## 升级维护规则

- 当前 skill 维护采用“原位增强”，不通过 `v2/v3` 叠版本壳制造新入口。
- 当前已吸收进 router 的 Trae 升级点：
  - `nested rules / 子目录 rules`：规则允许分层挂到 router，而不是继续堆成单页长合同
  - `slash commands / .trae/commands 多层目录`：当前仓内仍无 `.trae\commands` 实体目录，因此不建立 command router，不伪造命令副本
  - `.agents/skills` 加载：旧 skill 是否继续作为可调用候选，先由本索引裁决
  - `RunCommand` 体验增强：可执行入口优先补 repo-first 路径与边界说明
- 当前固定查找顺序：
  - `active router=.trae\skills\INDEX.md`
  - `decision index=21_trae_system_archive\SKILLS_INDEX.md`
  - `group router=21_trae_system_archive\SKILLS_GROUP_VIEW.md`

## 全量清单与裁决

- `artifact-provenance-note-guard-cn`
  - decision: `NEW_IN_NEW_REPO`
  - status: `NEW_REPO_HAS_COPY`
- `ashare-ops-guard`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `dev-guardrails`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `dual-epub-pdf-truth-anchor-cn`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `indicator-audit-shrink-loop-cn`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `knowledge-intake-quantize-cn`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `main-doc-contract-mirror-cn`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `mainline-full-ingest-cn`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `mt5-audit`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `mt-indicator-engineering-cn`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `multi-ai-discussion-guard`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `multi-ai-orchestrator-cn`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `multi-ai-suite-entry-cn`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `p0-exec-evidence-officer`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `p0-lab`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `p0-suite-entry-cn`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `p0-sweep-outbound-guard`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `panel-multi-ai-cn`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `proof-of-mapping-standard-cn`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `rolling-playbook-cn`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `source-sweep-batch-cn`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`
- `tool-idea-ingest-guard`
  - decision: `MIRROR_LATER_AS_NEEDED`
  - status: `OLD_ONLY`

## 逐 skill 明细索引

- `artifact-provenance-note-guard-cn`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\artifact-provenance-note-guard-cn\SKILL.md`
  - `current_router=.trae\skills\INDEX.md`
  - `reopen_condition=已在新仓active，无需重开mirror`
- `ashare-ops-guard`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\ashare-ops-guard\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `dev-guardrails`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\dev-guardrails\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `dual-epub-pdf-truth-anchor-cn`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\dual-epub-pdf-truth-anchor-cn\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `indicator-audit-shrink-loop-cn`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\indicator-audit-shrink-loop-cn\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `knowledge-intake-quantize-cn`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\knowledge-intake-quantize-cn\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `main-doc-contract-mirror-cn`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\main-doc-contract-mirror-cn\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `mainline-full-ingest-cn`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\mainline-full-ingest-cn\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `mt5-audit`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\mt5-audit\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `mt-indicator-engineering-cn`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\mt-indicator-engineering-cn\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `multi-ai-discussion-guard`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\multi-ai-discussion-guard\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `multi-ai-orchestrator-cn`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\multi-ai-orchestrator-cn\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `multi-ai-suite-entry-cn`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\multi-ai-suite-entry-cn\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `p0-exec-evidence-officer`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\p0-exec-evidence-officer\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `p0-lab`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\p0-lab\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `p0-suite-entry-cn`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\p0-suite-entry-cn\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `p0-sweep-outbound-guard`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\p0-sweep-outbound-guard\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `panel-multi-ai-cn`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\panel-multi-ai-cn\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `proof-of-mapping-standard-cn`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\proof-of-mapping-standard-cn\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `rolling-playbook-cn`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\rolling-playbook-cn\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `source-sweep-batch-cn`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\source-sweep-batch-cn\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`
- `tool-idea-ingest-guard`
  - `legacy_path=12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\tool-idea-ingest-guard\SKILL.md`
  - `current_router=.trae\README.md -> .trae\skills\INDEX.md`
  - `reopen_condition=重新成为当前first-hop|需要repo内显式合同副本`

## 相关入口

- 当前新仓最小 active skill 入口：
  - `d:\Stock\trading_assistant\.trae\skills\INDEX.md`
- 主题分组视图：
  - `d:\Stock\trading_assistant\21_trae_system_archive\SKILLS_GROUP_VIEW.md`
- 旧仓 skill 原位索引：
  - `d:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.trae\skills\INDEX.md`
- 旧仓 sweep 裁决来源：
  - `d:\Stock\trading_assistant\00_entry\OLD_REPO_FILE_SWEEP_TASKBOARD.md`

