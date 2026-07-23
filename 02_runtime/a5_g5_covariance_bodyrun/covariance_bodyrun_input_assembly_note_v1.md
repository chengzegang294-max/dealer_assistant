# A5 G5 Covariance Body Run Input Assembly Note v1

## 用途

- 说明 `covariance_model_id` 第一手最小本体实跑输入包应该由哪些字段拼出来。
- 固定主候选、字段来源和中止边界，避免一到 fresh-run 前又重新临时定口径。

## 当前主候选

- 当前统一只装配：
  - `benchmark_relative_sample_covariance`

## 最小主键

- 当前统一主键：
  - `portfolio_date`
  - `benchmark_id`
  - `asset_universe_id`

## 字段来源建议

- 装配模板 `bodyrun_base_template`
  - 提供：
    - `portfolio_date`
    - `benchmark_id`
    - `asset_universe_id`
    - `returns_window_spec.lookback_days`
    - `returns_window_spec.frequency`
    - `tracking_error_limit`
    - `active_risk_aversion`
- 候选家族冻结页
  - 提供：
    - `candidate_model_family`
    - `candidate_priority`
- 本体实跑最小准备页
  - 提供：
    - `required_success_fields`
    - `required_failure_fields`

## Join / 组装规则

- 当前 success 输入包必须同时满足：
  - `benchmark_id != ""`
  - `asset_universe_id != ""`
  - `lookback_days > 0`
  - `frequency != ""`
- 当前 failure 输入包默认触发：
  - `benchmark_id = ""`
  - `abort_reason = invalid_benchmark_context`

## 允许留空

- 当前可留空：
  - `notes`
  - `candidate_priority`
- 当前不应留空：
  - `portfolio_date`
  - `benchmark_id` for success case
  - `asset_universe_id`
  - `returns_window_spec.lookback_days`
  - `returns_window_spec.frequency`
  - `tracking_error_limit`
  - `active_risk_aversion`

## 当前运行入口

- 组装脚本：
  - `02_runtime/a5_g5_covariance_bodyrun/build_covariance_bodyrun_input_v1.py`
- 当前模板输入：
  - `02_runtime/a5_g5_covariance_bodyrun/data/covariance_bodyrun_input_template_v1.json`
  - `02_runtime/a5_g5_covariance_bodyrun/data/covariance_bodyrun_input_failure_template_v1.json`
- 当前 latest 输出：
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_input/covariance_bodyrun_input_success_latest.json`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_input/covariance_bodyrun_input_failure_latest.json`

## 当前状态

- 当前仅完成：
  - template-level 输入装配
- 当前还未完成：
  - 协方差矩阵 fresh-run
  - returns 历史样本真实加载
  - PSD 检查实跑

## 当前回链

- `00_entry/全库资料整理收口__20260713/A5_covariance_model_id_本体实跑输入装配页__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_covariance_model_id_本体实跑最小准备页__20260716.md`
- `02_runtime/a5_g5_covariance_bodyrun/runtime_execution_card_v1.md`
