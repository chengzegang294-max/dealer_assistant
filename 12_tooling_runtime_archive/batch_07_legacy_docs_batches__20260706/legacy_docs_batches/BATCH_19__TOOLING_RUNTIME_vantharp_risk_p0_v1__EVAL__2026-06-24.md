# Batch 19 - TOOLING_RUNTIME vantharp_risk_p0_v1 - EVAL - 2026-06-24

## Goal

- land the `vantharp_risk_p0_v1` runtime snapshot as auditable DIAG_ONLY evidence
- keep it strictly inside `12_工具运行时_TOOLING_RUNTIME`

## Scope

- target root:
  - `12_工具运行时_TOOLING_RUNTIME/vantharp_risk_p0_v1`
- target files:
  - `vantharp_risk_p0_min_contract_v1.md`
  - `vantharp_risk_p0_proof_of_mapping_v1.md`
  - `vantharp_risk_p0_fields_output_header_v1.txt`
  - `vantharp_risk_p0_fields_output_header_v2.txt`
  - `real_input_samples/vantharp_risk_p0_proof_input_v1.csv`
  - `real_input_samples/vantharp_risk_p0_proof_input_v2.csv`
  - `real_input_samples/vantharp_risk_p0_proof_output_v1.csv`
  - `real_input_samples/vantharp_risk_p0_proof_output_v2.csv`

## Read Result

- `vantharp_risk_p0_min_contract_v1.md` explicitly marks the role as `DIAG_ONLY`
- the snapshot provides:
  - minimal input/output contract
  - proof-of-mapping notes
  - sample inputs and outputs for audit

## Four-Way Verdict

- absorbed now:
  - the full `vantharp_risk_p0_v1` runtime snapshot pack
- reopen later:
  - follow-up iterations only when the contract version increments
- future bucket:
  - any integration into trading execution (not part of this batch)
- source-only for this cut:
  - none

## Decision

- `Batch 19` should contain only this runtime snapshot pack plus the batch docs/scripts
- do not mix the large `03_Kimi拆书待入库` deletion cluster into this batch
