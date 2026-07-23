# A5 G5 Covariance Body Run Prep Provenance Note v1

## 批次定位

- 当前目录类型：`WORKING`
- 当前主题：
  - `covariance_model_id` 本体实跑最小准备
- 当前阶段：
  - `ready_judgement_conditional__downstream_still_locked`

## 生成物分类

- `GENERATOR`
  - `run_covariance_bodyrun_prep_v1.py`
  - `run_covariance_bodyrun_preflight_v1.py`
  - `fetch_covariance_benchmark_series_v1.py`
  - `build_covariance_returns_input_v1.py`
  - `run_covariance_bodyrun_fresh_v1.py`
  - `run_covariance_stability_check_v1.py`
- `INDEX_NOTE`
  - `README.md`
  - `runtime_execution_card_v1.md`
  - `artifact_index_v1.tsv`
  - `covariance_bodyrun_preflight_checklist_v1.md`
  - `data/covariance_bodyrun_success_template_v1.json`
  - `data/covariance_bodyrun_failure_template_v1.json`
- `ARTIFACT`
  - `artifacts/covariance_bodyrun/covariance_bodyrun_success_latest.json`
  - `artifacts/covariance_bodyrun/covariance_bodyrun_failure_latest.json`
  - `artifacts/covariance_bodyrun_preflight/covariance_bodyrun_preflight_latest.json`
  - `artifacts/covariance_benchmark_series/covariance_benchmark_series__000300_SH__20260401_20260630.csv`
  - `artifacts/covariance_returns_input/asset_returns_panel_latest.csv`
  - `artifacts/covariance_returns_input/benchmark_returns_series_latest.csv`
  - `artifacts/covariance_returns_input/active_returns_panel_latest.csv`
  - `artifacts/covariance_bodyrun_fresh/covariance_matrix_latest.csv`
  - `artifacts/covariance_bodyrun_fresh/covariance_bodyrun_fresh_latest.json`
  - `artifacts/covariance_adjacent_window/...`
  - `artifacts/covariance_stability/covariance_stability_check_latest.json`

## 当前作用

- 当前模板与执行物用于验证：
  - 候选模型家族冻结后的最小 success / failure 结构
  - 既有 Tushare 日线资产能否被吸收到 first fresh-run
  - 单家族 first fresh-run 是否能跑出 PSD 协方差矩阵
  - 相邻窗口下最小稳定性检查是否通过
- 当前产物只能证明：
  - 模板级结构可执行
  - 中止路径可追溯
  - first fresh-run 入口边界未漂移
  - `benchmark_relative_sample_covariance` 可在单窗口 first fresh-run 下产出 `20 x 20` 协方差矩阵
  - 相邻 `60d` 窗口下最小稳定性检查已通过
  - 当前唯一模型最小合同已冻结到 repo-global 文档层
- 当前产物不能证明：
  - 正式风险模型已 ready
  - `risk_model_ready` 已正式判定通过
  - 更高层稳健边界已通过

## 证据强度

- 模板：`template`
- runner：`generator`
- smoke-run 输出：`hard`
- preflight 输出：`hard`
- first fresh-run 输出：`hard`
- stability check 输出：`hard`
- 但当前最新 fresh-run 仍属于：
  - `single_family`
  - `ready_judgement_conditional__downstream_still_locked`

## 红线

- 不把本目录产物写成：
  - 正式协方差本体实跑完成
  - 唯一实现模型已定稿
  - 三段输出可直接解除 `not_output_passed`
