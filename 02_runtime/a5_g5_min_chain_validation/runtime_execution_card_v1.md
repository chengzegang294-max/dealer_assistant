# A5 G5 Minimal Chain Validation Execution Card v1

## 入口

- `INDEX_NOTE`:
  - `02_runtime/a5_g5_min_chain_validation/README.md`
  - `02_runtime/a5_g5_min_chain_validation/artifact_index_v1.tsv`
- `GENERATOR`:
  - `02_runtime/a5_g5_min_chain_validation/run_a5_g5_min_chain_v1.py`
  - `02_runtime/a5_g5_min_chain_validation/run_g5_same_batch_boundary_audit_v1.py`

## 当前范围

- 当前任务：
  - 跑 success 链
  - 跑 `pte_failure` 链
  - 跑 `apw_failure` 链
  - 跑 same-batch boundary audit
  - 回填 repo-global 主链页
- 当前输出：
  - `artifacts/a5_g5_min_chain_success_latest.json`
  - `artifacts/a5_g5_min_chain_pte_failure_latest.json`
  - `artifacts/a5_g5_min_chain_apw_failure_latest.json`
  - `artifacts/a5_g5_same_batch_boundary_audit_latest.json`

## 推荐运行顺序

1. 运行 success 链
2. 运行 `pte_failure` 链
3. 运行 `apw_failure` 链
4. 运行 same-batch boundary audit
5. 回填 repo-global 执行页

## 当前最小命令入口

- success:
  - `python 02_runtime/a5_g5_min_chain_validation/run_a5_g5_min_chain_v1.py --chain-case success --output-json 02_runtime/a5_g5_min_chain_validation/artifacts/a5_g5_min_chain_success_latest.json`
- `pte_failure`:
  - `python 02_runtime/a5_g5_min_chain_validation/run_a5_g5_min_chain_v1.py --chain-case pte_failure --output-json 02_runtime/a5_g5_min_chain_validation/artifacts/a5_g5_min_chain_pte_failure_latest.json`
- `apw_failure`:
  - `python 02_runtime/a5_g5_min_chain_validation/run_a5_g5_min_chain_v1.py --chain-case apw_failure --output-json 02_runtime/a5_g5_min_chain_validation/artifacts/a5_g5_min_chain_apw_failure_latest.json`
- same-batch boundary audit:
  - `python 02_runtime/a5_g5_min_chain_validation/run_g5_same_batch_boundary_audit_v1.py`
