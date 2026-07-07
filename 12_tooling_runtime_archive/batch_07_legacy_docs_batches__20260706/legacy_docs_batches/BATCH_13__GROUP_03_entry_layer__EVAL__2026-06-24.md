# Batch 13 - GROUP_03 entry layer - EVAL - 2026-06-24

## Goal

- absorb the clean root entry layer under `GROUP_03`
- keep this cut limited to the `3` root master files only
- continue the validated `entry layer first` split used on `GROUP_06 / GROUP_05 / GROUP_01 / GROUP_02`

## Scope

- target root:
  - `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_03_组合管理_风险模型_交易成本`
- target files:
  - `GROUP_03_portfolio_risk_master_part_01.md`
  - `GROUP_03_portfolio_risk_master_part_02.md`
  - `GROUP_03_portfolio_risk_master_part_03.md`

## Read Result

- `part_01` is the portfolio construction pipeline, spanning alpha, risk model, constraints, cost, optimization, and monitoring
- `part_02` is the friction layer: turnover, transaction cost, impact/capacity, and feasibility constraints
- `part_03` is the research/backtest bias checklist with detection and mitigation guidance
- no separate `*_cutpack_v2_final` directory is present under `GROUP_03` at this time, so the root entry layer is also the full group payload for this batch

## Four-Way Verdict

- absorbed now:
  - `GROUP_03` root master files (parts `01/02/03`)
- reopen later:
  - none inside `GROUP_03` after this cut (no stable payload directory observed)
- future bucket:
  - later field-level implementation or runtime mapping beyond source-library intake
- source-only for this cut:
  - none inside `GROUP_03` root entry layer

## Decision

- `Batch 13` should contain only the three root master files
- do not mix any other unopened `GROUP_*` tree into this cut

## Expected Result After Batch 13

- `GROUP_03` will no longer be part of open `01_Kimi拆书待入库` residue
- the remaining unopened groups will narrow to:
  - `GROUP_04 / GROUP_07`
- next likely cut after `Batch 13`:
  - `Batch 14 = GROUP_04 entry layer`
