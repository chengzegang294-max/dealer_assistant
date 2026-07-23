# A5 G5 Covariance Body Run Prep

## 作用

- 本目录承接 `covariance_model_id` 的最小本体实跑准备工作线。
- 当前已从三类最小执行物推进到：
  - success / failure template
  - template-level smoke-run
  - first fresh-run preflight
  - first fresh-run returns input
  - first fresh-run 协方差矩阵
- 当前不做：
  - 多候选家族并跑
  - `risk_model_ready` 宣告

## 目录结构

- `runtime_execution_card_v1.md`
  - 当前执行边界、入口和推荐顺序
- `runtime_provenance_note_v1.md`
  - `GENERATOR / INDEX_NOTE / ARTIFACT` 追溯说明
- `artifact_index_v1.tsv`
  - 当前模板、脚本、产物索引
- `covariance_bodyrun_preflight_checklist_v1.md`
  - first fresh-run 前检查清单
- `covariance_bodyrun_runtime_params_template_v1.json`
  - first fresh-run 参数模板
- `data/`
  - 最小 success / failure 准备模板
- `artifacts/`
  - template-level smoke-run 输出
- `reports/`
  - 预留后续 body-run 摘要页
- `run_covariance_bodyrun_prep_v1.py`
  - 最小 template-level prep runner
- `run_covariance_bodyrun_preflight_v1.py`
  - first fresh-run preflight runner
- `fetch_covariance_benchmark_series_v1.py`
  - 抓 `CSI300` benchmark 原始日线与 benchmark return
- `build_covariance_returns_input_v1.py`
  - 从仓内 daily_tushare 资产构建 returns / active returns 输入
- `run_covariance_bodyrun_fresh_v1.py`
  - 运行 `benchmark_relative_sample_covariance` 的 first fresh-run
- `run_covariance_stability_check_v1.py`
  - 比较 current / adjacent 两窗口矩阵并输出最小稳定性检查摘要

## 当前状态

- 当前已落：
  - 最小 success 准备模板
  - 最小 failure 准备模板
  - 最小 prep runner 草案
  - 输入装配说明
  - success 输入装配模板
  - failure 输入装配模板
  - 最小输入装配脚本
- 当前将完成：
  - success template-level smoke-run
  - failure template-level smoke-run
- 当前已完成：
  - success template-level smoke-run
  - failure template-level smoke-run
  - success input assembly latest
  - failure input assembly latest
  - first fresh-run preflight latest
  - benchmark series latest
  - asset / benchmark / active returns latest
  - covariance matrix latest
  - first fresh-run latest
  - adjacent window raw / benchmark / returns / covariance latest
  - minimum stability check latest
  - minimum integration validation execution latest
- 当前还未落：
  - `risk_model_ready` 的 `yes / no` 最终裁决
  - 三段输出正式解锁判断

## repo 回链

- `00_entry/全库资料整理收口__20260713/A5_covariance_model_id_候选模型家族冻结页__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_covariance_model_id_本体实跑最小准备页__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_covariance_model_id_总瓶颈判断_多家AI回收记录与主负责人裁决__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_covariance_model_id_first_fresh_run执行页__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_covariance_model_id_最小稳定性检查准备页__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_covariance_model_id_最小稳定性检查执行页__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_covariance_model_id_唯一模型收敛主负责人裁决页__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_covariance_model_id_唯一模型最小合同页__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_covariance_model_id_唯一模型定稿主负责人裁决页__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_covariance_model_id_ready判断准备页__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_covariance_model_id_ready判断_多家AI回收记录与主负责人裁决__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_covariance_model_id_最小集成验证准备页__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_covariance_model_id_最小集成验证执行页__20260717.md`
