# Batch 8C - Batch9 full tree - EVAL - 2026-06-24

## Goal

- absorb the remaining `Batch9` residue as one clean source-library batch under `Batch 8`
- keep `Batch9` separate from `Smile_SMC`
- preserve `Batch9` internal four-way split instead of re-splitting the tree into smaller commit fragments

## Scope

- target directory:
  - `10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9`
- current file count:
  - `66` files
- current directory count:
  - `9` subdirectories

## Read Result

- `Batch9_批次收口与四分流_v1.md` already defines:
  - `已吸收`
  - `可重开`
  - `future bucket`
  - `仅来源库保留`
- `00_本批说明与多AI能力画像.md` already explains why:
  - `N01 / N02 / N03` are the active contract lanes
  - `N04 / N05 / N06` stay in the tree as deferred A-share holding area
  - `batch9_sources_kimi` is a secondary structured-note layer, not fake raw truth
- no default dependency on `D:\Stock\cut_file` remains inside this tree

## Decision

- use the whole `Batch9` directory as `Batch 8C`
- do not carve out `A股指标整理区_待整理_N04_N05_N06`
- do not carve out `batch9_sources_kimi`
- do not carve out `Batch9_待用户手动补网页清单_v1.md`
- reason:
  - these items are already explicitly downgraded inside the tree itself
  - keeping the full tree preserves auditability and avoids creating an artificial half-tree commit

## No-Mix Rule

- stage the full `Batch9` directory
- stage the `Batch 8C` doc pack
- do not stage `Smile_SMC`
- do not reopen `NFTRADEZ`
- do not touch completed `Batch 7`, `Batch 8A`, or `Batch 8B`

## Next Result After 8C

- `Batch 8` remaining residue should narrow to:
  - `Smile_SMC ??1`
- next lane after this batch:
  - `Batch 8D = Smile_SMC trace layer`
