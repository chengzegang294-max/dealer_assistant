# A5 G5 Target Weight Validation Execution Card v1

## 生成入口

- 仓库级正式入口：
  - `00_entry/全库资料整理收口__20260713/A5_target_weight_validation_run_执行说明页__20260716.md`
  - `00_entry/全库资料整理收口__20260713/A5_target_weight_最小缺口补齐页__20260716.md`
  - `00_entry/全库资料整理收口__20260713/A5_target_weight_verified_with_degraded_risk后续升级判断准备页__20260717.md`
- `INDEX_NOTE`:
  - `02_runtime/a5_g5_target_weight_validation/README.md`
  - `02_runtime/a5_g5_target_weight_validation/artifact_index_v1.tsv`
  - `02_runtime/a5_g5_target_weight_validation/runtime_provenance_note_v1.md`
- `GENERATOR`:
  - `02_runtime/a5_g5_target_weight_validation/run_target_weight_validation_v1.py`
  - `02_runtime/a5_g5_target_weight_validation/generate_target_weight_v1.py`
  - `02_runtime/a5_g5_target_weight_validation/run_covariance_target_weight_same_batch_v1.py`

## 当前范围

- 当前任务：
  - 固定 success validation record 模板
  - 固定 failure validation record 模板
  - 提供最小 runner 草案
  - 完成 template-level smoke-run
  - 冻结上游真实输入模板
  - 冻结真实生成链 smoke-run 输入卡
  - 固定真实输入驱动 success/failure 结果模板
  - 完成 real-input case validation smoke-run
  - 完成 actual generation execution
  - 吸收 `verified_with_degraded_risk` 之后的后续升级判断多AI回包并形成正式状态回填
- 当前输入：
  - `data/target_weight_validation_success_template_v1.json`
  - `data/target_weight_validation_failure_template_v1.json`
  - `data/target_weight_real_input_template_v1.json`
  - `data/target_weight_real_input_success_case_template_v1.json`
  - `data/target_weight_real_input_failure_case_template_v1.json`
- 当前输出：
  - `artifacts/target_weight_validation/` 下的 fresh-run JSON
  - `artifacts/target_weight_validation/covariance_target_weight_same_batch_latest.json`
  - 后续汇总摘要页

## 当前作用

- 把 repo-global 的 `validation run` 说明接到实际 runtime 入口。
- 让 `target_weight` 的 success/failure 证据不再停在文档层。
- 当前只验证：
  - 结构是否可执行
  - 中止理由是否一致
- 当前已完成：
  - success case smoke-run
  - failure case smoke-run
  - real-input success case validation smoke-run
  - real-input failure case validation smoke-run
  - actual generation success execution
  - actual generation failure execution
  - covariance -> target_weight 同轮批次串联执行
  - verified 之后后续升级判断发包入口
  - verified 之后后续升级判断正式裁决
- 当前不验证：
  - 收益率
  - alpha 有效性
  - 风险调整后表现
  - 更强风险模型下的正式生成执行
- 当前已补下一手入口：
  - `target_weight_real_input_smoke_run_card_v1.md`

## 推荐运行顺序

1. 检查 success 模板
2. 运行 success case
3. 检查 failure 模板
4. 运行 failure case
5. 回填 repo-global 状态页
6. 推进上游真实输入驱动的 smoke-run
7. 推进 actual generation execution
8. 重开升格裁决
9. 在 covariance 最小集成验证执行后重开 verified 后续升级判断
10. 吸收 verified 后续升级判断回包并回填新状态
11. 沿同轮批次串联结果继续压缩 `not_output_passed` 的显式运行缺口

## 当前最小命令入口

- success case:
  - `python 02_runtime/a5_g5_target_weight_validation/run_target_weight_validation_v1.py --case success --template-json 02_runtime/a5_g5_target_weight_validation/data/target_weight_validation_success_template_v1.json --output-json 02_runtime/a5_g5_target_weight_validation/artifacts/target_weight_validation/tw_validation_success_latest.json`
- failure case:
  - `python 02_runtime/a5_g5_target_weight_validation/run_target_weight_validation_v1.py --case failure --template-json 02_runtime/a5_g5_target_weight_validation/data/target_weight_validation_failure_template_v1.json --output-json 02_runtime/a5_g5_target_weight_validation/artifacts/target_weight_validation/tw_validation_failure_latest.json`
- covariance -> target_weight same-batch:
  - `python 02_runtime/a5_g5_target_weight_validation/run_covariance_target_weight_same_batch_v1.py`

## 当前产物边界

- `data/`:
  - 放模板，不放 fresh-run 结果
- `artifacts/`:
  - 放 fresh-run 结果和后续日志
- 当前不把 fresh-run 结果直接回写到 `00_entry`

## 证据强度

- 当前模板：`INDEX_NOTE`
- 当前 runner：`GENERATOR`
- 后续 fresh-run JSON：`hard`
