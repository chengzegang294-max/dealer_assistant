# Batch11 Kimi Inbox Promote (GROUP_10 A5 QEPm)

## Scope

- 目的：将 incoming 中一簇 `GROUP_10_A5_财报_估值_组合管理/01_A5_cutpack_v1_final/5073_Quantitative_Equity_Portfolio_Management` 迁入 mirror。
- 口径：ARCHIVE_ONLY / historical_recovered；后续仍需在 `GROUP_10_*` 入口卡处补齐目录说明与去重策略。

## Inputs

- incoming root: `10_source_library_archive/batch_09_legacy_source_library_alignment__20260707/mirror_kimi_inbox_incoming`
- ledger: `10_source_library_archive/batch_09_legacy_source_library_alignment__20260707/mirror_gap_decision_ledger__20260707.tsv`

## Outputs

- promoted manifest: `promote_manifest__20260707.tsv`
- promote report: `promote_report__20260707.json`

