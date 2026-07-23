# A5 G5 Covariance Body Run Prep Execution Card v1

## 生成入口

- 仓库级正式入口：
  - `00_entry/全库资料整理收口__20260713/A5_covariance_model_id_候选模型家族冻结页__20260716.md`
  - `00_entry/全库资料整理收口__20260713/A5_covariance_model_id_本体实跑最小准备页__20260716.md`
- `INDEX_NOTE`:
  - `02_runtime/a5_g5_covariance_bodyrun/README.md`
  - `02_runtime/a5_g5_covariance_bodyrun/artifact_index_v1.tsv`
  - `02_runtime/a5_g5_covariance_bodyrun/runtime_provenance_note_v1.md`
  - `02_runtime/a5_g5_covariance_bodyrun/covariance_bodyrun_preflight_checklist_v1.md`
- `GENERATOR`:
  - `02_runtime/a5_g5_covariance_bodyrun/run_covariance_bodyrun_prep_v1.py`
  - `02_runtime/a5_g5_covariance_bodyrun/build_covariance_bodyrun_input_v1.py`
  - `02_runtime/a5_g5_covariance_bodyrun/run_covariance_bodyrun_preflight_v1.py`
  - `02_runtime/a5_g5_covariance_bodyrun/fetch_covariance_benchmark_series_v1.py`
  - `02_runtime/a5_g5_covariance_bodyrun/build_covariance_returns_input_v1.py`
  - `02_runtime/a5_g5_covariance_bodyrun/run_covariance_bodyrun_fresh_v1.py`
  - `02_runtime/a5_g5_covariance_bodyrun/run_covariance_stability_check_v1.py`
- `PARAM_TEMPLATE`:
  - `02_runtime/a5_g5_covariance_bodyrun/covariance_bodyrun_runtime_params_template_v1.json`

## 当前范围

- 当前任务：
  - 固定 success 准备模板
  - 固定 failure 准备模板
  - 提供最小 prep runner 草案
  - 完成 template-level smoke-run
  - 固定 success / failure 输入装配模板
  - 产出第一手 latest 输入装配包
  - 固定 first fresh-run preflight checklist
  - 产出 first preflight latest
  - 抓取 benchmark series latest
  - 产出 asset / benchmark / active returns latest
  - 产出 first fresh-run covariance latest
  - 产出 adjacent window covariance latest
  - 产出 minimum stability check latest
- 当前输入：
  - `data/covariance_bodyrun_success_template_v1.json`
  - `data/covariance_bodyrun_failure_template_v1.json`
  - `data/covariance_bodyrun_input_template_v1.json`
  - `data/covariance_bodyrun_input_failure_template_v1.json`
- 当前输出：
  - `artifacts/covariance_bodyrun/` 下的 prep smoke-run JSON
  - `artifacts/covariance_bodyrun_input/` 下的 latest 输入装配 JSON
  - `artifacts/covariance_bodyrun_preflight/` 下的 preflight latest JSON
  - `artifacts/covariance_benchmark_series/` 下的 benchmark latest CSV
  - `artifacts/covariance_returns_input/` 下的 returns latest CSV/JSON
  - `artifacts/covariance_bodyrun_fresh/` 下的 covariance matrix latest CSV/JSON
  - `artifacts/covariance_adjacent_window/` 下的相邻窗口 raw / benchmark / returns / covariance latest
  - `artifacts/covariance_stability/` 下的稳定性检查 latest JSON

## 当前作用

- 把 repo-global 的“本体实跑最小准备”接到实际 runtime 入口。
- 让 `covariance_model_id` 的 success / failure 准备证据不再停在文档层。
- 当前只验证：
  - 输入结构是否可执行
  - 候选家族是否与冻结口径一致
  - 中止理由是否一致
- 当前已完成：
  - success template-level smoke-run
  - failure template-level smoke-run
  - success input assembly latest
  - failure input assembly latest
  - first fresh-run preflight latest
  - benchmark series latest
  - asset / benchmark / active returns latest
  - first fresh-run covariance latest
  - adjacent window covariance latest
  - minimum stability check latest
- 当前不验证：
  - 矩阵数值正确性
  - shrinkage 参数表现
  - 唯一模型优选

## 推荐运行顺序

1. 检查 success 模板
2. 运行 success case
3. 检查 failure 模板
4. 运行 failure case
5. 回填 repo-global 状态页
6. 生成第一手 latest 输入装配包
7. 回填 repo-global 输入装配页
8. 冻结 first fresh-run 参数模板
9. 准备 first fresh-run 入口
10. 运行 first fresh-run preflight
11. 抓取 benchmark series latest
12. 生成 returns / active returns latest
13. 运行 first fresh-run covariance
14. 回填 repo-global 执行页与状态页
15. 运行 adjacent window fresh-run
16. 运行 minimum stability check
17. 回填 repo-global 稳定性检查执行页
18. 回填唯一模型收敛裁决页
19. 回填唯一模型最小合同页
20. 吸收 ready 判断多AI回包
21. 回填 conditional 且 downstream_still_locked 裁决
22. 转入最小集成验证准备
23. 执行最小集成验证并保持 `ready_judgement_conditional__downstream_still_locked`

## 当前最小命令入口

- success case:
  - `python 02_runtime/a5_g5_covariance_bodyrun/run_covariance_bodyrun_prep_v1.py --case success --template-json 02_runtime/a5_g5_covariance_bodyrun/data/covariance_bodyrun_success_template_v1.json --output-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun/covariance_bodyrun_success_latest.json`
- failure case:
  - `python 02_runtime/a5_g5_covariance_bodyrun/run_covariance_bodyrun_prep_v1.py --case failure --template-json 02_runtime/a5_g5_covariance_bodyrun/data/covariance_bodyrun_failure_template_v1.json --output-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun/covariance_bodyrun_failure_latest.json`
- first preflight:
  - `python 02_runtime/a5_g5_covariance_bodyrun/run_covariance_bodyrun_preflight_v1.py --runtime-params-json 02_runtime/a5_g5_covariance_bodyrun/covariance_bodyrun_runtime_params_template_v1.json --success-assembly-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_input/covariance_bodyrun_input_success_latest.json --failure-assembly-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_input/covariance_bodyrun_input_failure_latest.json --success-prep-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun/covariance_bodyrun_success_latest.json --failure-prep-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun/covariance_bodyrun_failure_latest.json --output-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_preflight/covariance_bodyrun_preflight_latest.json`
- benchmark series:
  - `python 02_runtime/a5_g5_covariance_bodyrun/fetch_covariance_benchmark_series_v1.py --benchmark-id CSI300 --index-code 000300.SH --start-date 20260401 --end-date 20260630`
- returns input:
  - `python 02_runtime/a5_g5_covariance_bodyrun/build_covariance_returns_input_v1.py --runtime-params-json 02_runtime/a5_g5_covariance_bodyrun/covariance_bodyrun_runtime_params_template_v1.json --asset-ohlcv-csv 02_runtime/ashare_p0_first_round_validation/data/t02_sources/daily_tushare/t02_daily_tushare_batch__sample20_q2__20260401_20260630.csv --benchmark-series-csv 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_benchmark_series/covariance_benchmark_series__000300_SH__20260401_20260630.csv --universe-csv 02_runtime/ashare_p0_first_round_validation/data/t02_multi_symbol_sample_v3.csv --asset-returns-csv 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_returns_input/asset_returns_panel_latest.csv --benchmark-returns-csv 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_returns_input/benchmark_returns_series_latest.csv --active-returns-csv 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_returns_input/active_returns_panel_latest.csv --summary-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_returns_input/covariance_returns_input_summary_latest.json`
- first fresh-run:
  - `python 02_runtime/a5_g5_covariance_bodyrun/run_covariance_bodyrun_fresh_v1.py --runtime-params-json 02_runtime/a5_g5_covariance_bodyrun/covariance_bodyrun_runtime_params_template_v1.json --active-returns-csv 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_returns_input/active_returns_panel_latest.csv --output-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_fresh/covariance_bodyrun_fresh_latest.json --matrix-csv 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_fresh/covariance_matrix_latest.csv`
- adjacent fresh-run:
  - `python 02_runtime/ashare_p0_first_round_validation/fetch_t02_daily_batch_tushare_v1.py --start-date 20251215 --end-date 20260331 --symbol-list-csv 02_runtime/ashare_p0_first_round_validation/data/t02_multi_symbol_sample_v3.csv --batch-label sample20_adjacent60 --output-dir 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/raw_daily`
  - `python 02_runtime/a5_g5_covariance_bodyrun/fetch_covariance_benchmark_series_v1.py --benchmark-id CSI300 --index-code 000300.SH --start-date 20251215 --end-date 20260331 --output-dir 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/benchmark`
  - `python 02_runtime/a5_g5_covariance_bodyrun/build_covariance_returns_input_v1.py --runtime-params-json 02_runtime/a5_g5_covariance_bodyrun/covariance_bodyrun_runtime_params_template_v1.json --asset-ohlcv-csv 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/raw_daily/t02_daily_tushare_batch__sample20_adjacent60__20251215_20260331.csv --benchmark-series-csv 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/benchmark/covariance_benchmark_series__000300_SH__20251215_20260331.csv --universe-csv 02_runtime/ashare_p0_first_round_validation/data/t02_multi_symbol_sample_v3.csv --asset-returns-csv 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/returns/asset_returns_panel_adjacent_latest.csv --benchmark-returns-csv 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/returns/benchmark_returns_series_adjacent_latest.csv --active-returns-csv 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/returns/active_returns_panel_adjacent_latest.csv --summary-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/returns/covariance_returns_input_adjacent_summary_latest.json`
  - `python 02_runtime/a5_g5_covariance_bodyrun/run_covariance_bodyrun_fresh_v1.py --runtime-params-json 02_runtime/a5_g5_covariance_bodyrun/covariance_bodyrun_runtime_params_template_v1.json --active-returns-csv 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/returns/active_returns_panel_adjacent_latest.csv --output-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/fresh/covariance_bodyrun_fresh_adjacent_latest.json --matrix-csv 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/fresh/covariance_matrix_adjacent_latest.csv`
- stability check:
  - `python 02_runtime/a5_g5_covariance_bodyrun/run_covariance_stability_check_v1.py --current-fresh-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_fresh/covariance_bodyrun_fresh_latest.json --current-matrix-csv 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_fresh/covariance_matrix_latest.csv --adjacent-fresh-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/fresh/covariance_bodyrun_fresh_adjacent_latest.json --adjacent-matrix-csv 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/fresh/covariance_matrix_adjacent_latest.csv --output-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_stability/covariance_stability_check_latest.json`

## 当前产物边界

- `data/`:
  - 放模板，不放 fresh-run 结果
- `artifacts/`:
  - 放 prep smoke-run、input assembly latest、preflight latest 和后续日志
- 当前已把 first fresh-run 结果回写到 repo-global 执行页

## 证据强度

- 当前模板：`INDEX_NOTE`
- 当前 runner：`GENERATOR`
- 后续 fresh-run JSON：`hard`
- preflight latest：`hard`
- 当前 fresh-run latest：`hard`
- 当前 stability latest：`hard`
- 当前结论层级：`ready_judgement_conditional__downstream_still_locked`
