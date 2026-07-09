# GROUP_09 Historical Copies 评估 2026-06-23

## 范围

- target set:
  - root `CUTPACK__A4__*.md`
  - `01_A1_cutpack_v2/`
  - `02_A3C1_cutpack_v2/`
- goal:
  - decide whether these should be dropped, left uncommitted, or committed as history/archive layer

## 证据摘要

- root README already marks them as non-stable:
  - root A4 loose files are `重复副本，不再作为稳定入口`
  - `01_A1_cutpack_v2/` is `历史目录，不再作为 A1 正式入口`
  - `02_A3C1_cutpack_v2/` is `历史目录，不再作为 A3-C1 正式入口`
- byte-level comparison shows they are not safe-to-drop duplicates:
  - root A4 loose files do not byte-match the files in `04_A4_cutpack_v2_final/`
  - `01_A1_cutpack_v2/` files do not byte-match the files in `01_A1_cutpack_v2_final/`
  - `02_A3C1_cutpack_v2/` files do not byte-match the files in `02_A3C1_cutpack_v2_final/`

## 角色裁决

- root `CUTPACK__A4__*.md`
  - role: `HISTORICAL_DUPLICATE_COPY`
  - decision: keep as source-layer history, not stable entry
- `01_A1_cutpack_v2/`
  - role: `HISTORICAL_PRE_FINAL_A1`
  - decision: keep as source-layer history, not stable entry
- `02_A3C1_cutpack_v2/`
  - role: `HISTORICAL_PRE_FINAL_A3C1`
  - decision: keep as source-layer history, not stable entry

## 四分流裁决

- 已吸收
  - none
- 可重开
  - none
- future bucket
  - physical freeze/move to another archive tree can be done later if needed
- 仅来源库保留
  - all three historical copy clusters listed above

## 提交裁决

- decision:
  - `COMMIT_AS_HISTORY_LAYER`
- rationale:
  - these files are text-first and small
  - they preserve cutpack evolution and audit trail
  - they are explicitly demoted from stable entry already, so committing them does not blur current truth if the boundary is documented

## 边界

- commit now:
  - the three historical copy clusters above
- do not reinterpret them as:
  - current stable entry
  - current primary truth layer
- if later needed:
  - move/freeze can be done as a separate structural cleanup batch, not mixed with this evidence-preserving commit
