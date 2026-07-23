# A5 G5 Target Weight Validation Provenance Note v1

更新时间：2026-07-16

## 用途

- 记录本目录当前 `GENERATOR / INDEX_NOTE / ARTIFACT` 的最小追溯关系。
- 防止后续只看到 JSON 或脚本名，不知道是谁生成、给谁用、当前证据强度如何。

## 当前文件分类

### GENERATOR

- `run_target_weight_validation_v1.py`
  - 当前作用：
    - 基于 success/failure 模板生成最小 validation record
  - 默认输入：
    - `data/target_weight_validation_success_template_v1.json`
    - `data/target_weight_validation_failure_template_v1.json`
  - 默认产物：
    - `artifacts/target_weight_validation/`
  - 证据强度：
    - `hard`（当前终端新跑结果时）
- `generate_target_weight_v1.py`
  - 当前作用：
    - 基于 real-input 模板执行最小 target_weight 生成
  - 默认输入：
    - `data/target_weight_real_input_template_v1.json`
    - `data/target_weight_real_input_failure_template_v1.json`
  - 默认产物：
    - `artifacts/target_weight_validation/`
  - 证据强度：
    - `hard`（当前终端新跑结果时）

### INDEX_NOTE

- `README.md`
- `runtime_execution_card_v1.md`
- `runtime_provenance_note_v1.md`
- `artifact_index_v1.tsv`
- `data/target_weight_validation_success_template_v1.json`
- `data/target_weight_validation_failure_template_v1.json`
- `data/target_weight_real_input_template_v1.json`
- `data/target_weight_real_input_success_case_template_v1.json`
- `data/target_weight_real_input_failure_case_template_v1.json`
- `data/target_weight_real_input_failure_template_v1.json`
- `target_weight_real_input_smoke_run_card_v1.md`

### ARTIFACT

- `artifacts/target_weight_validation/tw_validation_success_latest.json`
  - 当前作用：
    - 记录 success case 的 template-level smoke-run 结果
  - 证据强度：
    - `hard`
- `artifacts/target_weight_validation/tw_validation_failure_latest.json`
  - 当前作用：
    - 记录 failure case 的 template-level smoke-run 结果
  - 证据强度：
    - `hard`
- `artifacts/target_weight_validation/tw_real_input_success_latest.json`
  - 当前作用：
    - 记录 real-input success case 的 validation smoke-run 结果
  - 证据强度：
    - `hard`
- `artifacts/target_weight_validation/tw_real_input_failure_latest.json`
  - 当前作用：
    - 记录 real-input failure case 的 validation smoke-run 结果
  - 证据强度：
    - `hard`
- `artifacts/target_weight_validation/tw_actual_generation_success_latest.json`
  - 当前作用：
    - 记录 actual generation success 执行结果
  - 证据强度：
    - `hard`
- `artifacts/target_weight_validation/tw_actual_generation_failure_latest.json`
  - 当前作用：
    - 记录 actual generation failure 执行结果
  - 证据强度：
    - `hard`

## 当前结果与缺口

- 当前已补：
  - success validation record 模板
  - failure validation record 模板
  - 上游真实输入模板
  - real-input success/failure 结果模板
  - 真实生成链 smoke-run 输入卡
  - 最小 validation runner 草案
  - 最小 actual generation generator
- 当前已补第一批 fresh-run：
  - success smoke-run JSON
  - failure smoke-run JSON
  - real-input success case smoke-run JSON
  - real-input failure case smoke-run JSON
- 当前已补第二批 generation execution：
  - actual generation success JSON
  - actual generation failure JSON
- 当前仍缺：
  - 升格裁决回包

## 当前回链

- `artifact_index_v1.tsv`
- `runtime_execution_card_v1.md`
- `00_entry/全库资料整理收口__20260713/A5_target_weight_validation_run_执行说明页__20260716.md`
