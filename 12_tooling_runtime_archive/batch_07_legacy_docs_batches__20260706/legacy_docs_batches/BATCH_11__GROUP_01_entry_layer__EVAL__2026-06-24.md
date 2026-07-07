# Batch 11 - GROUP_01 entry layer - EVAL - 2026-06-24

## Goal

- absorb the clean root entry layer under `GROUP_01`
- keep the root thematic overview separate from the later final cutpack payload directory
- continue the validated `entry layer first` split used on `GROUP_06` and `GROUP_05`

## Scope

- target root:
  - `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_01_微观结构_交易所_HFT`
- target files:
  - `GROUP_01_microstructure_master_part_01.md`
  - `GROUP_01_microstructure_master_part_02.md`
  - `GROUP_01_microstructure_master_part_03.md`

## Read Result

- `part_01` is the group overview plus unified terminology layer across market microstructure, exchanges, and HFT
- `part_02` is the candidate field layer, including P0 / P1 / diag-only / source-only classifications
- `part_03` is the model-family, checklist, conflict-resolution, and YAML index layer
- together these three files form a full root contract for `GROUP_01`, while `01_F2_cutpack_v2_final` remains a separate stable payload directory

## Four-Way Verdict

- absorbed now:
  - `GROUP_01` root overview + field contract + model/checklist layer
- reopen later:
  - `01_F2_cutpack_v2_final` as the next stable cutpack layer
- future bucket:
  - later field-level implementation or runtime mapping beyond source-library intake
- source-only for this cut:
  - none inside the root entry layer

## Decision

- `Batch 11` should contain only the three root master files
- do not mix `01_F2_cutpack_v2_final` into this first cut
- do not reopen already completed `GROUP_05` or `GROUP_06` lanes

## Expected Result After Batch 11

- `GROUP_01` becomes an opened, staged lane instead of a full unopened directory
- the next clean cut becomes:
  - `Batch 11A = GROUP_01 cutpack stable layer`
- the remaining unopened groups stay narrowed to:
  - `GROUP_02 / GROUP_03 / GROUP_04 / GROUP_07`
