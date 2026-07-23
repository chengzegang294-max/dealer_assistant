# A5 G5 Financial Validity Gate v0 Runtime Execution Card

## 生成入口

- repo-global 正式入口：
  - `00_entry/全库资料整理收口__20260713/A5_financial_validity_gate最小入口与通过标准页__20260719.md`
- `INDEX_NOTE`:
  - `02_runtime/a5_g5_financial_validity_gate_v0/README.md`
  - `02_runtime/a5_g5_financial_validity_gate_v0/artifact_index_v1.tsv`
- `PARAM_TEMPLATE`:
  - `02_runtime/a5_g5_financial_validity_gate_v0/fv_gate_v0_runtime_params_template_v1.json`
- `DATA_TEMPLATE`:
  - `02_runtime/a5_g5_financial_validity_gate_v0/data/fv_gate_v0_scorecard_template_v1.json`
- `GENERATOR`:
  - `02_runtime/a5_g5_financial_validity_gate_v0/run_fv_gate_v0_minimal_backtest_v1.py`
  - `02_runtime/a5_g5_financial_validity_gate_v0/run_fv_gate_holding_rule_minimal_backtest_v1.py`
  - `02_runtime/a5_g5_financial_validity_gate_v0/run_fv_gate_holding_rule_v0_probe_v1.py`

## 当前范围

- 当前只验证：
  - same-batch APW 静态权重在最小历史窗口上的 gross / net 成绩单
  - `holdout` 作为回测内规则的最小存在性
  - `degraded_fixed_cost` 固定成本口径
- 当前不验证：
  - 多次调仓
  - 冲击模型完备性
  - 稳健性全家桶
  - 严格 out-of-time 泛化

## 当前最小命令入口

- minimal backtest:
  - `python 02_runtime/a5_g5_financial_validity_gate_v0/run_fv_gate_v0_minimal_backtest_v1.py --runtime-params-json 02_runtime/a5_g5_financial_validity_gate_v0/fv_gate_v0_runtime_params_template_v1.json`
- holding rule v0 probe:
  - `python 02_runtime/a5_g5_financial_validity_gate_v0/run_fv_gate_holding_rule_v0_probe_v1.py --probe-template-json 02_runtime/a5_g5_financial_validity_gate_v0/fv_gate_holding_rule_v0_probe_template_v1.json`
- v2 third window replay:
  - `python 02_runtime/a5_g5_financial_validity_gate_v0/run_fv_gate_v0_minimal_backtest_v1.py --runtime-params-json 02_runtime/a5_g5_financial_validity_gate_v0/fv_gate_v2_third_window_runtime_params_template_v1.json`

## 当前禁止误写

- 禁止写成：
  - `financial-valid`
  - `output_passed`
  - `ready to deploy`
- 当前通过只允许写成：
  - `FV_gate_v0_evidence_produced`
