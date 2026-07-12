# AShare P0 First Round Validation Execution Card v1

## 生成入口

- 仓库级正式入口：
  - `00_entry/A股_P0_功能合同__20260711.md`
- repo 级执行合同：
  - `00_entry/A股_P0_离线验证执行卡__20260712.md`
  - `00_entry/A股_P0_离线验证结论门槛__20260712.md`
  - `00_entry/A股_P0_GROUP_08研究合同桥接与验证映射卡__20260713.md`
- `INDEX_NOTE`:
  - `02_runtime/ashare_p0_first_round_validation/README.md`
  - `02_runtime/ashare_p0_first_round_validation/artifact_index_v1.tsv`
  - `02_runtime/ashare_p0_first_round_validation/reports/README.md`
- `GENERATOR`:
  - `02_runtime/ashare_p0_first_round_validation/run_t01_volume_price_scan_v1.py`
  - `02_runtime/ashare_p0_first_round_validation/run_t01_industry_distribution_v1.py`
  - `02_runtime/ashare_p0_first_round_validation/audit_t02_fund_flow_input_v1.py`
  - `02_runtime/ashare_p0_first_round_validation/prepare_t02_fund_flow_input_v1.py`
  - `02_runtime/ashare_p0_first_round_validation/build_t02_real_input_v1.py`
  - `02_runtime/ashare_p0_first_round_validation/check_t02_tushare_env_v1.py`
  - `02_runtime/ashare_p0_first_round_validation/fetch_t02_moneyflow_tushare_v1.py`
  - `02_runtime/ashare_p0_first_round_validation/fetch_t02_moneyflow_batch_tushare_v1.py`
  - `02_runtime/ashare_p0_first_round_validation/fetch_t02_northbound_tushare_v1.py`
  - `02_runtime/ashare_p0_first_round_validation/fetch_t02_regime_proxy_tushare_v1.py`
  - `02_runtime/ashare_p0_first_round_validation/fetch_t02_industry_map_tushare_v1.py`
  - `02_runtime/ashare_p0_first_round_validation/run_t02_fund_flow_scan_v1.py`
  - `02_runtime/ashare_p0_first_round_validation/analyze_t02_layer_stability_v1.py`
  - `02_runtime/ashare_p0_first_round_validation/analyze_t02_local_tuning_v1.py`
  - `02_runtime/ashare_p0_first_round_validation/analyze_t02_local_tuning_review_v1.py`
  - `02_runtime/ashare_p0_first_round_validation/analyze_t02_confirmation_filter_v1.py`
  - `02_runtime/ashare_p0_first_round_validation/analyze_t02_candidate_branch_v1.py`

## 当前范围

- 当前任务：
  - `T01 量价阈值触发密度`
  - `T02 主力资金主触发`
  - `T03 业绩事件可得性与降级`
  - `T04 行业轮动阈值敏感度`
  - `T05 历史类比样本门槛`
- 当前输入：
  - A 股日线行情
  - 量能字段
  - 行业映射字段
  - 资金字段
  - 业绩事件字段
  - 研究合同桥接说明
- 当前输出：
  - 单项结果页
  - 首轮汇总结论页
  - 归档统计表

## 当前作用

- 把 `00_entry` 的字段、样本、输出模板和门槛文档接到实际 runtime 工作线。
- 把 `GROUP_08` 新冻结合同限制在“执行前桥接层”，避免直接误接到默认 runtime 门控。
- 固定首轮结果页应该落在哪里，避免“脚本先跑了，结果不知道放哪”。
- 当前只提供最小执行骨架，不假装脚本已经齐全。

## 推荐运行顺序

1. `T01`
2. `T02`
3. `T04`
4. `T05`
5. `T03`
6. `first_round_summary`

## 当前结果入口

- `reports/T01_result_stub_v1.md`
- `reports/T02_result_stub_v1.md`
- `reports/T03_availability_and_downgrade_stub_v1.md`
- `reports/T04_result_stub_v1.md`
- `reports/T05_result_stub_v1.md`
- `reports/first_round_summary_stub_v1.md`

## 当前已验证入口

- `T01` 已完成一轮 smoke-run：
  - 时间窗：`2025-05-08 -> 2026-05-08`
  - 摘要：`520` 条触发、`204` 个触发日、峰值日 `19`
  - 产物：
    - `artifacts/t01_volume_price_scan/t01_volume_price_scan_summary_latest.json`
    - `artifacts/t01_volume_price_scan/t01_trigger_detail_latest.tsv`
- `T01` 已完成一轮行业分布补充统计：
  - 匹配标的：`17/44`
  - 触发权重覆盖：`181/520`
  - 当前结论：现有行业映射只适合做临时分布观察
  - 产物：
    - `artifacts/t01_industry_distribution/t01_industry_distribution_summary_latest.json`
    - `artifacts/t01_industry_distribution/t01_industry_trigger_counts_latest.tsv`
- `T02` 已完成模板级链路 smoke-run：
  - 输入审计：`contract_ready = true`
  - 输入归一化：`missing_columns = []`
  - 扫描结果：`1` 行输入、`0` 条触发
  - 当前结论：执行链已通，但还缺真实资金宽表
  - 产物：
    - `artifacts/t02_input_audit/t02_input_audit_summary_latest.json`
    - `artifacts/t02_input_prepare/t02_fund_flow_input_normalized_latest.csv`
    - `artifacts/t02_fund_flow_scan/t02_fund_flow_scan_summary_latest.json`
- `T02` 已完成真实宽表拼接入口 smoke-run：
  - 构建结果：`1200` 行候选宽表
  - join 命中：`moneyflow=1200(base)`、`northbound=1140`、`regime=1200`、`industry=1200`
  - 当前结论：`moneyflow / northbound / regime / industry` 已全部接入第三轮更宽样本的跨月真实宽表；当前仍缺正式 `OHLCV` 宽底表
  - 产物：
    - `artifacts/t02_real_input_build/t02_real_input_build_summary_latest.json`
    - `artifacts/t02_real_input_build/t02_real_input_candidate_latest.csv`
- `T02` 已补真实源抓取入口：
  - `moneyflow`：复用 `TUSHARE_TOKEN` 合同，拉 `moneyflow + daily`
  - `moneyflow_batch`：按样本清单批量拉 `moneyflow + daily` 并合并成单份 base CSV
  - `northbound`：复用 `TUSHARE_TOKEN` 合同，拉 `moneyflow_hsgt`
  - `regime`：复用 `TUSHARE_TOKEN` 合同，拉 `index_daily` 并派生 `G01 / G02 / G03`
  - `industry`：复用 `TUSHARE_TOKEN` 合同，拉 `stock_basic`
  - 已实际尝试首轮抓取：
    - `moneyflow` metadata：`data/t02_sources/moneyflow_tushare/t02_moneyflow_tushare__000001_SZ__20260501_20260531__metadata.json`
    - `northbound` metadata：`data/t02_sources/northbound_tushare/t02_northbound_tushare__20260501_20260531__metadata.json`
    - `industry` metadata：`data/t02_sources/industry_tushare/t02_industry_map_tushare__list_status_L__metadata.json`
  - 二轮实跑结果：
    - `moneyflow`：`status = success`，`rows = 18`
    - `moneyflow_batch`：`status = success`，`rows = 90`，`symbols = 5`
    - `moneyflow_batch(sample10)`：`status = success`，`rows = 180`，`symbols = 10`
    - `moneyflow_batch(sample20)`：`status = success`，`rows = 360`，`symbols = 20`
    - `moneyflow_batch(sample20_q2)`：`status = success`，`rows = 1200`，`symbols = 20`
    - `northbound`：`status = success`，`rows = 57`
    - `regime`：`status = success`，`rows = 60`，`G01=16 / G02=7 / G03=37`
    - `industry`：`status = success`，`rows = 5530`
  - 当前结论：本机 token 与积分权限均已就绪，当前已跑通单标的、多标的与阶段代理三类 Tushare 抓取入口
- `T02` 已补本机环境预检入口：
  - 预检脚本：`check_t02_tushare_env_v1.py`
  - 当前作用：先判断 token 与 `tushare`/`pandas` 依赖是否就绪，再决定是否继续跑三条 fetcher
  - 当前预检结果：
    - `token_present = true`
    - `token_source = C:\Users\91883\.tushare\token`
    - `pandas.available = true`
    - `tushare.available = true`
  - 当前结论：token 与依赖都已补齐，fetcher 已进入真实权限验证阶段
- `T02` 已完成首轮真实扫描：
  - 输入范围：`20` 个标的，`2026-04-01 -> 2026-06-30`
  - 扫描结果：`1200` 行真实输入、`493` 条触发、`20` 个触发标的
  - 触发分布：`000001.SZ=41`、`000651.SZ=34`、`600760.SH=34`、`601318.SH=30`、`000002.SZ=29`、`600900.SH=28`、`600519.SH=27`、`600276.SH=26`
  - 阶段分布：`G01_普涨=134`、`G02_普跌=54`、`G03_震荡=305`
  - 当前结论：`T02` 已在更宽行业与风格样本和 `G01 / G02 / G03` 三类阶段都形成可消费触发；从 `5 -> 10 -> 20` 标的扩样，到固定 `20` 标的再拉长到跨月窗口后，触发密度从约 `45.6%`、`46.7%`、`44.4%` 进一步回落到 `41.1%`，但仍保持稳定可消费
  - 对比产物：
    - `artifacts/t02_fund_flow_scan/t02_sample_expansion_comparison_latest.tsv`
    - `artifacts/t02_fund_flow_scan/t02_time_window_stability_latest.tsv`
- `T02` 已完成分层稳定性分析：
  - 行业大类分层：
    - `金融=49.4%`
    - `地产链=48.3%`
    - `消费防御=47.9%`
    - `资源周期=37.1%`
    - `成长科技=35.6%`
  - 资金比率波动分层：
    - `high=45.0%`
    - `mid=44.7%`
    - `low=34.1%`
  - 当前结论：全局阈值仍可保留，但穿透力明显更偏向 `金融 / 地产链 / 消费防御`；`成长科技` 与 `低资金比率波动` 组更像后续微调候选，而不是当前就要推翻全局口径
  - 分层产物：
    - `artifacts/t02_layer_stability/t02_layer_stability_summary_latest.json`
    - `artifacts/t02_layer_stability/t02_symbol_layer_stability_latest.tsv`
    - `artifacts/t02_layer_stability/t02_macro_bucket_stability_latest.tsv`
    - `artifacts/t02_layer_stability/t02_flow_volatility_bucket_stability_latest.tsv`
- `T02` 已完成局部阈值微调试算：
  - 试算场景：
    - `3.0% + 连续2日` 基线
    - `2.5% + 连续2日`
    - `3.0% + 连续1日`
    - `3.5% + 连续2日`
  - 关键裁决：
    - `3.0% + 连续1日` 虽然能显著抬高弱层密度，但会把全样本从 `41.1%` 一起推高到 `83.0%`，当前判定为全局过松，不进入局部分支候选
    - `2.5% + 连续2日` 对 `low_flow_vol` 从 `34.1%` 抬到 `38.6%`，对 `growth_tech_low_flow_vol` 从 `28.3%` 抬到 `33.3%`
    - `growth_tech` 整体从 `35.6%` 仅抬到 `38.5%`，相对全样本的超额改善只有 `0.08pct` 量级，当前不足以单独开分支
  - 当前结论：全局默认仍保留 `3% + 连续2日`；局部 watchlist 只保留 `low_flow_vol` 和 `growth_tech_low_flow_vol` 两组的 `2.5% + 连续2日` 备选口径
  - 试算产物：
    - `artifacts/t02_local_tuning/t02_local_tuning_summary_latest.json`
    - `artifacts/t02_local_tuning/t02_local_tuning_scenario_comparison_latest.tsv`
    - `artifacts/t02_local_tuning/t02_local_tuning_recommendation_latest.tsv`
- `T02` 已完成 watchlist 噪声风险复核：
  - 复核对象：
    - `low_flow_vol`
    - `growth_tech_low_flow_vol`
  - 复核结果：
    - `low_flow_vol` 新增触发 `19` 条，其中 `42.1%` 落在边缘带 `2.5%~3.0%`，`78.9%` 发生在 `G03_震荡`，北向同向支持率仅 `15.8%`
    - `growth_tech_low_flow_vol` 新增触发 `9` 条，其中 `55.6%` 落在边缘带 `2.5%~3.0%`，`77.8%` 发生在 `G03_震荡`，北向同向支持率为 `0%`
  - 当前结论：`watchlist` 可以继续保留，但只应视为弱候选，不升级为正式局部分支；如果后续真要启用 `2.5% + 连续2日`，应先补更强佐证条件，而不是直接裸放宽
  - 复核产物：
    - `artifacts/t02_local_tuning_review/t02_local_tuning_review_summary_latest.json`
    - `artifacts/t02_local_tuning_review/t02_local_tuning_group_review_latest.tsv`
    - `artifacts/t02_local_tuning_review/t02_local_tuning_added_trigger_detail_latest.tsv`
- `T02` 已完成 watchlist 确认条件过滤试算：
  - 试算对象：
    - `low_flow_vol`
    - `growth_tech_low_flow_vol`
  - 试算过滤器：
    - `排除 G03_震荡`
    - `要求北向同向`
    - `排除 G03_震荡 + 要求北向同向`
  - 关键结果：
    - `low_flow_vol` 在 `2.5% + 连续2日` 下共有 `162` 条候选；`排除 G03_震荡` 后保留 `66` 条，保留率 `40.7%`，并将 `G03` 占比从 `59.3%` 压到 `0%`
    - `growth_tech_low_flow_vol` 在 `2.5% + 连续2日` 下共有 `60` 条候选；`排除 G03_震荡` 后保留 `24` 条，保留率 `40.0%`，并将 `G03` 占比从 `60.0%` 压到 `0%`
    - 单独要求 `北向同向` 虽能把同向率提升到 `100%`，但分别只剩 `13.6%` 与 `16.7%` 候选，当前过于激进
  - 当前结论：若后续要给 watchlist 弱候选加确认条件，首选 `排除 G03_震荡`；`北向同向` 更适合作为二级加严过滤，而不是第一道主过滤
  - 过滤产物：
    - `artifacts/t02_confirmation_filter/t02_confirmation_filter_summary_latest.json`
    - `artifacts/t02_confirmation_filter/t02_confirmation_filter_scenario_comparison_latest.tsv`
    - `artifacts/t02_confirmation_filter/t02_confirmation_filter_recommendation_latest.tsv`
- `T02` 已完成弱候选分支裁决：
  - 裁决对象：
    - `2.5% + 连续2日 + 排除 G03_震荡`
  - 并排结果：
    - `low_flow_vol`：baseline `0.3405`，filtered candidate `0.1571`
    - `growth_tech_low_flow_vol`：baseline `0.2833`，filtered candidate `0.1333`
  - 当前结论：该候选虽然是弱层最优过滤型候选，但覆盖率相对 baseline 下掉过多，当前仍不足以从 `watchlist` 升级到 `微调`
  - 当前口径：
    - 全局默认仍使用 `3% + 连续2日`
    - 弱层只保留 `2.5% + 连续2日 + 排除 G03_震荡` 作为观察型候选
  - 裁决产物：
    - `artifacts/t02_candidate_branch/t02_candidate_branch_summary_latest.json`
    - `artifacts/t02_candidate_branch/t02_candidate_branch_decision_latest.tsv`
    - `reports/T02_candidate_branch_decision_v1.md`

## 当前最小命令入口

- `T01`
  - `python 02_runtime/ashare_p0_first_round_validation/run_t01_volume_price_scan_v1.py`
- `T01 行业分布`
  - `python 02_runtime/ashare_p0_first_round_validation/run_t01_industry_distribution_v1.py`
- `T02`
  - `python 02_runtime/ashare_p0_first_round_validation/run_t02_fund_flow_scan_v1.py --input-csv <fund_flow_csv>`
- `T02 输入审计`
  - `python 02_runtime/ashare_p0_first_round_validation/audit_t02_fund_flow_input_v1.py`
- `T02 输入归一化`
  - `python 02_runtime/ashare_p0_first_round_validation/prepare_t02_fund_flow_input_v1.py`
- `T02 真实宽表拼接`
  - `python 02_runtime/ashare_p0_first_round_validation/build_t02_real_input_v1.py --base-csv <base_csv> --moneyflow-csv <moneyflow_csv> --northbound-csv <northbound_csv> --regime-csv <regime_csv> --industry-csv <industry_csv>`
- `T02 Tushare 环境预检`
  - `python 02_runtime/ashare_p0_first_round_validation/check_t02_tushare_env_v1.py`
- `T02 moneyflow 拉取`
  - `python 02_runtime/ashare_p0_first_round_validation/fetch_t02_moneyflow_tushare_v1.py --symbol 000001.SZ --start-date 20260501 --end-date 20260531`
- `T02 moneyflow 批量拉取`
  - `python 02_runtime/ashare_p0_first_round_validation/fetch_t02_moneyflow_batch_tushare_v1.py --start-date 20260501 --end-date 20260531`
- `T02 northbound 拉取`
  - `python 02_runtime/ashare_p0_first_round_validation/fetch_t02_northbound_tushare_v1.py --start-date 20260501 --end-date 20260531`
- `T02 regime 拉取`
  - `python 02_runtime/ashare_p0_first_round_validation/fetch_t02_regime_proxy_tushare_v1.py --start-date 20260501 --end-date 20260531`
- `T02 industry 拉取`
  - `python 02_runtime/ashare_p0_first_round_validation/fetch_t02_industry_map_tushare_v1.py`

## 当前产物边界

- `reports/`：
  - 放结构化结果页和汇总结论
- `artifacts/`：
  - 放统计表、日志、导出文件和后续批次归档说明
- 当前不把真实结果直接回写到 `00_entry`

## 证据强度

- 当前 stub 文档：`INDEX_NOTE`
- 当前尚未生成的结果表：`not_generated_yet`
- 后续离线新跑结果：`hard`
- 若回收旧结果：`historical_recovered`
