# Batch 10 - GROUP_05 entry layer - EVAL - 2026-06-24

## 目标

- absorb the root entry layer of `GROUP_05`
- keep the root state-template and minimum-absorption files separate from the heavier `01_F1_cutpack_v2_final` subtree
- reuse the same clean entry-first split that already worked on `GROUP_06`

## 范围

- target root:
  - `10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/GROUP_05_趋势_系统交易`
- current clean entry residue:
  - `3` root-level markdown files

## 目标文件

- `GROUP_05_trend_systematic_trading.md`
- `GROUP_05_trend_system_trading_STATE_TEMPLATE.md`
- `GROUP_05_?????_v1.md`

## 阅读结果

- `GROUP_05_trend_systematic_trading.md` is the full trend/systematic trading root overview with state/bias/friction/risk structure
- `GROUP_05_trend_system_trading_STATE_TEMPLATE.md` is the more detailed state-template anchor with cross-book rules, parameters, and guardrails
- `GROUP_05_?????_v1.md` already fixes the current minimum absorption order and maps `GROUP_05` into diagnostic and guardrail roles
- `01_F1_cutpack_v2_final` is the heavier follow-up tree and should not be mixed into the first `GROUP_05` commit

## 四分流裁决

- absorbed now:
  - `GROUP_05` root overview
  - `GROUP_05` state-template anchor
  - `GROUP_05` minimum absorption pack
- reopen later:
  - `01_F1_cutpack_v2_final`
- future bucket:
  - any later field-level or strategy-level downflow beyond the current entry pack
- source-only for this cut:
  - deferred `GROUP_05` cutpack subtree for later isolated commits

## 裁决

- `Batch 10` should contain only the `3` root entry files of `GROUP_05`
- do not mix `01_F1_cutpack_v2_final`
- do not reopen already committed `Batch 9A` through `Batch 9F`

## Batch 10 后预期结果

- `GROUP_05` will no longer be a fully unopened group directory
- `GROUP_05` will then be ready for a later split such as:
  - stable cutpack layer
  - later archive/history residue if needed
- next likely cut after `Batch 10`:
  - `Batch 10A = GROUP_05 cutpack stable layer`
