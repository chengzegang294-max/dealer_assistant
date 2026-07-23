# A5 G5 Target Weight Validation

## 作用

- 本目录承接 `target_weight` 的最小 `validation run` 工作线。
- 当前只做两类最小执行证据：
  - success validation
  - failure validation
- 当前不做：
  - 收益回测
  - 参数搜索
  - 多策略并行比较

## 目录结构

- `runtime_execution_card_v1.md`
  - 当前执行边界、入口和推荐顺序
- `runtime_provenance_note_v1.md`
  - `GENERATOR / INDEX_NOTE / ARTIFACT` 追溯说明
- `artifact_index_v1.tsv`
  - 当前模板、脚本、产物索引
- `data/`
  - 最小成功/失败验证记录模板
  - 上游真实输入模板
  - real-input success/failure 结果模板
- `reports/`
  - 预留后续验证摘要页
- `artifacts/`
  - 预留后续 fresh-run 真实结果
- `run_target_weight_validation_v1.py`
  - 最小 validation runner 草案
- `generate_target_weight_v1.py`
  - 最小 actual generation generator
- `target_weight_real_input_smoke_run_card_v1.md`
  - 上游真实输入驱动的 smoke-run 输入卡

## 当前状态

- 当前已落：
  - 最小 success 记录模板
  - 最小 failure 记录模板
  - 最小 validation runner 草案
  - 最小 actual generation generator
  - 上游真实输入模板
  - 真实生成链 smoke-run 输入卡
  - real-input success/failure 结果模板
- 当前已完成：
  - success template-level smoke-run
  - failure template-level smoke-run
  - real-input success case validation smoke-run
  - real-input failure case validation smoke-run
  - actual generation success execution
  - actual generation failure execution
- 当前已继续回填到：
  - `verified_with_degraded_risk__upstream_min_integration_verified__not_output_passed`
  - `covariance_model_id` 最小集成验证执行后的后续升级判断正式裁决
- 当前还未落：
  - 新状态同步到下游消费口径后的下一轮输出段判断结果

## repo 回链

- `00_entry/全库资料整理收口__20260713/A5_target_weight_validation_run_执行说明页__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_target_weight_最小缺口补齐页__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_target_weight_升格裁决_多家AI回收记录与主负责人裁决__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_target_weight_verified_with_degraded_risk后续升级判断准备页__20260717.md`
- `00_entry/全库资料整理收口__20260713/A5_target_weight_verified_with_degraded_risk后续升级判断_多家AI正式发包稿__20260717.md`
- `00_entry/全库资料整理收口__20260713/A5_target_weight_verified_with_degraded_risk后续升级判断_多家AI回收记录与主负责人裁决__20260717.md`
