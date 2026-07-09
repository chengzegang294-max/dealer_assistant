# Batch 12 - GROUP_02 entry layer - EVAL - 2026-06-24

## 目标

- absorb the clean root entry layer under `GROUP_02`
- keep this cut limited to the `3` root master files only
- continue the validated `entry layer first` split used on `GROUP_06 / GROUP_05 / GROUP_01`

## 范围

- target root:
  - `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_02_期权_波动率_波动率微笑`
- target files:
  - `GROUP_02_options_volatility_master_part_01.md`
  - `GROUP_02_options_volatility_master_part_02.md`
  - `GROUP_02_options_volatility_master_part_03.md`

## 阅读结果

- `part_01` is the group overview plus unified terminology across options, volatility, and volatility smile
- `part_02` is a strategy template library with explicit entry/adjust/risk/data requirements
- `part_03` is the conflict-resolution layer with recommended repo conventions and proposed field names
- no separate `*_cutpack_v2_final` directory is present under `GROUP_02` at this time, so the root entry layer is also the full group payload for this batch

## 四分流裁决

- absorbed now:
  - `GROUP_02` root master files (parts `01/02/03`)
- reopen later:
  - none inside `GROUP_02` after this cut (no stable payload directory observed)
- future bucket:
  - later field-level implementation or runtime mapping beyond source-library intake
- source-only for this cut:
  - none inside `GROUP_02` root entry layer

## 裁决

- `Batch 12` should contain only the three root master files
- do not mix any other unopened `GROUP_*` tree into this cut

## 批次 12 后预期结果

- `GROUP_02` will no longer be part of open `01_Kimi拆书待入库` residue
- the remaining unopened groups will narrow to:
  - `GROUP_03 / GROUP_04 / GROUP_07`
- next likely cut after `Batch 12`:
  - `Batch 13 = GROUP_03 entry layer`
