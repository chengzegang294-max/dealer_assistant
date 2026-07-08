# XBreaking Buffer Semantics Log v1

## 目的

- 这份文件用于持续记录 `XBreaking` 各 buffer 的语义假设、probe 结果和验证结论。
- 当前先做语义日志，不把 `XBreaking` 直接接成交易信号。

## 当前家族对象

- 家族：`XBREAKING`
- 主要文件：
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreaking.ex4`
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreaking.ex5`
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreakingProbe.mq5`
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreakingProbe.ex5`
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreakingProbe.ini`

## 当前已知 probe 字段

- `handle`
- `init_err`
- `buffer`
- `copied`
- `err`
- `non_empty`
- `first_valid`
- `last_valid`

## 语义日志模板

- 批次信息：
  - `date_tag`
  - `platform`
  - `symbol`
  - `indicator_tf`
  - `bars_to_probe`
- buffer 观察：
  - `buffer_id`
  - `copied`
  - `non_empty`
  - `first_valid`
  - `last_valid`
  - `suspected_role`
  - `confidence`
- 语义裁决：
  - `unknown`
  - `candidate_level`
  - `candidate_direction`
  - `candidate_state`
  - `rejected_guess`

## 当前允许的语义状态

- 当前只允许写：
  - `unknown`
  - `candidate`
  - `rejected`
- 当前不允许直接写：
  - `buy_signal`
  - `sell_signal`
  - `hard_gate_ready`

## 当前 future 路径

- 如果后续通过仓库外、合规、可审计途径拿到：
  - 源码
  - 公式说明
  - 厂商文档
- 可以回补：
  - buffer 语义
  - 公式骨架
  - 正式字段定义

## 当前运行时落点

- 首批 probe 运行时批次：
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\`
- 本批执行卡：
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\BATCH_01_EXECUTION_CARD.md`
- 本批产物索引模板：
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\BATCH_01_ARTIFACT_INDEX_TEMPLATE.md`
- 首次实跑操作卡：
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\MT4_MT5_FIRST_RUN_PLAYBOOK.md`

## 当前状态

- 当前 `XBreaking` 仍停在 `probe-first / semantics log first` 阶段。
- 但新仓库已经补好首批 runtime batch 路径和产物索引模板。
- 当前批次已补齐一轮 `MT5` fresh-run `csv + tester report + terminal log + tester log`，因此 `report_missing` 已不再是主阻塞。

## 第一轮实际记录

- 批次信息：
  - `date_tag`: `20260626`
  - `platform`: `MT5`
  - `symbol`: `EURUSD`
  - `indicator_tf`: `PERIOD_H1`
  - `bars_to_probe`: `200`
  - `csv`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\csv\XBreaking_probe_EURUSD_H1_20250101_220500.csv`
- probe 总结：
  - `handle`: `10`
  - `init_err`: `0`
  - `status`: `DONE`
  - 解释：指标句柄成功建立，说明 `iCustom` 初始化链路可用。

## 第二轮 fresh-run 记录

- 批次信息：
  - `date_tag`: `20260701`
  - `platform`: `MT5`
  - `symbol`: `EURUSD`
  - `indicator_tf`: `PERIOD_H1`
  - `bars_to_probe`: `200`
  - `csv`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\csv\XBreaking_probe_EURUSD_H1_20250102_000030.csv`
  - `tester_report`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\tester_report\xbreaking_probe_portable.htm`
  - `tester_log`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\log\20260701_20260701T041405.log`
- probe 总结：
  - `handle`: `10`
  - `init_err`: `0`
  - `status`: `DONE`
  - `buffer_activity_profile`: `buffer0_only`
  - 解释：第二轮 fresh-run 与第一轮结论一致，说明 `buffer 0` 可读、`buffer 1..7` 返回 `4806` 的访问形态具有重复性。

## 第三轮 validation-matrix 记录

- 批次信息：
  - `date_tag`: `20260701`
  - `platform`: `MT5`
  - `symbol`: `EURUSD`
  - `chart_tf`: `PERIOD_H4`
  - `indicator_tf`: `PERIOD_H4`
  - `bars_to_probe`: `200`
  - `archive_tag`: `eurusd_h4_20260701_setmode`
  - `csv`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\eurusd_h4_20260701_setmode\csv\XBreaking_probe_EURUSD_H4_20250102_000030.csv`
  - `tester_report`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\eurusd_h4_20260701_setmode\report\xbreaking_probe_eurusd_h4.htm`
  - `tester_log`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\eurusd_h4_20260701_setmode\log\20260701.log`
  - `runtime_summary`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\eurusd_h4_20260701_setmode\run_summary.json`
- probe 总结：
  - `handle`: `10`
  - `init_err`: `0`
  - `status`: `DONE`
  - `buffer_activity_profile`: `buffer0_only`
  - 解释：在 `EURUSD / H4` 下，`buffer 0` 仍可稳定复制且全窗口值为 `0`，`buffer 1..7` 仍返回 `4806`，说明 `single_buffer_access_pattern` 并非仅限于 `H1` 单一样本。

## 第四轮 validation-matrix 记录

- 批次信息：
  - `date_tag`: `20260701`
  - `platform`: `MT5`
  - `symbol`: `GBPUSD`
  - `chart_tf`: `PERIOD_H4`
  - `indicator_tf`: `PERIOD_H4`
  - `bars_to_probe`: `200`
  - `archive_tag`: `gbpusd_h4_20260701T`
  - `csv`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\gbpusd_h4_20260701T\csv\XBreaking_probe_GBPUSD_H4_20250102_000000.csv`
  - `tester_report`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\gbpusd_h4_20260701T\report\xbreaking_probe_gbpusd_h4.htm`
  - `tester_log`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\gbpusd_h4_20260701T\log\20260701.log`
  - `runtime_summary`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\gbpusd_h4_20260701T\run_summary.json`
- probe 总结：
  - `handle`: `10`
  - `init_err`: `0`
  - `status`: `DONE`
  - `buffer_activity_profile`: `buffer0_only`
  - 解释：在 `GBPUSD / H4` 下，访问形态仍为 `buffer0_only`，说明 `single_buffer_access_pattern` 不仅跨周期重复，也开始跨 `symbol` 重复。

## 第五轮 validation-matrix 记录

- 批次信息：
  - `date_tag`: `20260701`
  - `platform`: `MT5`
  - `symbol`: `USDJPY`
  - `chart_tf`: `PERIOD_H4`
  - `indicator_tf`: `PERIOD_H4`
  - `bars_to_probe`: `200`
  - `archive_tag`: `usdjpy_h4_20260701T`
  - `csv`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\usdjpy_h4_20260701T\csv\XBreaking_probe_USDJPY_H4_20250102_000000.csv`
  - `tester_report`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\usdjpy_h4_20260701T\report\xbreaking_probe_usdjpy_h4.htm`
  - `tester_log`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\usdjpy_h4_20260701T\log\20260701.log`
  - `runtime_summary`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\usdjpy_h4_20260701T\run_summary.json`
- probe 总结：
  - `handle`: `10`
  - `init_err`: `0`
  - `status`: `DONE`
  - `buffer_activity_profile`: `buffer0_only`
  - 解释：在 `USDJPY / H4` 下，访问形态仍为 `buffer0_only`，说明该访问形态进一步跨 `symbol` 重复。

## 第六轮 validation-matrix 记录

- 批次信息：
  - `date_tag`: `20260701`
  - `platform`: `MT5`
  - `symbol`: `USDJPY`
  - `chart_tf`: `PERIOD_H1`
  - `indicator_tf`: `PERIOD_H1`
  - `bars_to_probe`: `200`
  - `archive_tag`: `usdjpy_h1_20260701T`
  - `csv`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\usdjpy_h1_20260701T\csv\XBreaking_probe_USDJPY_H1_20250102_000000.csv`
  - `tester_report`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\usdjpy_h1_20260701T\report\xbreaking_probe_usdjpy_h1.htm`
  - `tester_log`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\usdjpy_h1_20260701T\log\20260701.log`
  - `runtime_summary`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\usdjpy_h1_20260701T\run_summary.json`
- probe 总结：
  - `handle`: `10`
  - `init_err`: `0`
  - `status`: `DONE`
  - `buffer_activity_profile`: `buffer0_only`
  - 解释：在 `USDJPY / H1` 下，访问形态仍为 `buffer0_only`，说明该访问形态不仅在 `EURUSD/H1` 成立，也跨 `symbol` 成立。

## 第七轮 validation-matrix 记录

- 批次信息：
  - `date_tag`: `20260701`
  - `platform`: `MT5`
  - `symbol`: `XAUUSD`
  - `chart_tf`: `PERIOD_H4`
  - `indicator_tf`: `PERIOD_H4`
  - `bars_to_probe`: `200`
  - `archive_tag`: `xauusd_h4_20260701T`
  - `csv`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\xauusd_h4_20260701T\csv\XBreaking_probe_XAUUSD_H4_20250102_010000.csv`
  - `tester_report`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\xauusd_h4_20260701T\report\xbreaking_probe_xauusd_h4.htm`
  - `tester_log`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\xauusd_h4_20260701T\log\20260701.log`
  - `runtime_summary`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\xauusd_h4_20260701T\run_summary.json`
- probe 总结：
  - `handle`: `10`
  - `init_err`: `0`
  - `status`: `DONE`
  - `buffer_activity_profile`: `buffer0_only`
  - 解释：在 `XAUUSD / H4` 下，访问形态仍为 `buffer0_only`，说明该访问形态并不局限于外汇报价品种。

## 第八轮 validation-matrix 记录

- 批次信息：
  - `date_tag`: `20260701`
  - `platform`: `MT5`
  - `symbol`: `US30`
  - `chart_tf`: `PERIOD_H4`
  - `indicator_tf`: `PERIOD_H4`
  - `bars_to_probe`: `200`
  - `archive_tag`: `us30_h4_20260701T`
  - `csv`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\us30_h4_20260701T\csv\XBreaking_probe_US30_H4_20250102_010000.csv`
  - `tester_report`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\us30_h4_20260701T\report\xbreaking_probe_us30_h4.htm`
  - `tester_log`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\us30_h4_20260701T\log\20260701.log`
  - `runtime_summary`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\us30_h4_20260701T\run_summary.json`
- probe 总结：
  - `handle`: `10`
  - `init_err`: `0`
  - `status`: `DONE`
  - `buffer_activity_profile`: `buffer0_only`
  - 解释：在 `US30 / H4` 下，访问形态仍为 `buffer0_only`，说明该访问形态已跨外汇、黄金与股指样本重复出现。

## 第九轮 validation-matrix 记录

- 批次信息：
  - `date_tag`: `20260701`
  - `platform`: `MT5`
  - `symbol`: `EURUSD`
  - `chart_tf`: `PERIOD_H4`
  - `indicator_tf`: `PERIOD_H4`
  - `from_date`: `2025.01.03`
  - `to_date`: `2025.01.10`
  - `bars_to_probe`: `200`
  - `archive_tag`: `eurusd_h4_jan0310_20260701T124339_window_a`
  - `csv`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\eurusd_h4_jan0310_20260701T124339_window_a\csv\XBreaking_probe_EURUSD_H4_20250103_000000.csv`
  - `tester_report`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\eurusd_h4_jan0310_20260701T124339_window_a\report\xbreaking_probe_eurusd_h4_jan0310.htm`
  - `tester_log`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\eurusd_h4_jan0310_20260701T124339_window_a\log\20260701.log`
  - `runtime_summary`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\eurusd_h4_jan0310_20260701T124339_window_a\run_summary.json`
- probe 总结：
  - `handle`: `10`
  - `init_err`: `0`
  - `status`: `DONE`
  - `buffer_activity_profile`: `buffer0_only`
  - 解释：在缩窄到 `2025.01.03 ~ 2025.01.10` 的窗口后，`EURUSD / H4` 仍保持 `buffer0_only`。

## 第十轮 validation-matrix 记录

- 批次信息：
  - `date_tag`: `20260701`
  - `platform`: `MT5`
  - `symbol`: `XAUUSD`
  - `chart_tf`: `PERIOD_H4`
  - `indicator_tf`: `PERIOD_H4`
  - `from_date`: `2025.01.03`
  - `to_date`: `2025.01.10`
  - `bars_to_probe`: `200`
  - `archive_tag`: `xauusd_h4_jan0310_20260701T124339_window_a`
  - `csv`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\xauusd_h4_jan0310_20260701T124339_window_a\csv\XBreaking_probe_XAUUSD_H4_20250103_010000.csv`
  - `tester_report`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\xauusd_h4_jan0310_20260701T124339_window_a\report\xbreaking_probe_xauusd_h4_jan0310.htm`
  - `tester_log`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\xauusd_h4_jan0310_20260701T124339_window_a\log\20260701.log`
  - `runtime_summary`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\xauusd_h4_jan0310_20260701T124339_window_a\run_summary.json`
- probe 总结：
  - `handle`: `10`
  - `init_err`: `0`
  - `status`: `DONE`
  - `buffer_activity_profile`: `buffer0_only`
  - 解释：在相同窗口下，`XAUUSD / H4` 仍保持 `buffer0_only`，说明该结论并非只由外汇样本支撑。

## 第十一轮 validation-matrix 记录

- 批次信息：
  - `date_tag`: `20260701`
  - `platform`: `MT5`
  - `symbol`: `EURUSD`
  - `chart_tf`: `PERIOD_H4`
  - `indicator_tf`: `PERIOD_H4`
  - `from_date`: `2025.01.07`
  - `to_date`: `2025.01.14`
  - `bars_to_probe`: `200`
  - `archive_tag`: `eurusd_h4_jan0714_20260701T124459_window_b`
  - `csv`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\eurusd_h4_jan0714_20260701T124459_window_b\csv\XBreaking_probe_EURUSD_H4_20250107_000000.csv`
  - `tester_report`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\eurusd_h4_jan0714_20260701T124459_window_b\report\xbreaking_probe_eurusd_h4_jan0714.htm`
  - `tester_log`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\eurusd_h4_jan0714_20260701T124459_window_b\log\20260701.log`
  - `runtime_summary`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\eurusd_h4_jan0714_20260701T124459_window_b\run_summary.json`
- probe 总结：
  - `handle`: `10`
  - `init_err`: `0`
  - `status`: `DONE`
  - `buffer_activity_profile`: `buffer0_only`
  - 解释：把窗口后移到 `2025.01.07 ~ 2025.01.14` 后，`EURUSD / H4` 仍保持 `buffer0_only`。

## 第十二轮 validation-matrix 记录

- 批次信息：
  - `date_tag`: `20260701`
  - `platform`: `MT5`
  - `symbol`: `XAUUSD`
  - `chart_tf`: `PERIOD_H4`
  - `indicator_tf`: `PERIOD_H4`
  - `from_date`: `2025.01.07`
  - `to_date`: `2025.01.14`
  - `bars_to_probe`: `200`
  - `archive_tag`: `xauusd_h4_jan0714_20260701T124459_window_b`
  - `csv`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\xauusd_h4_jan0714_20260701T124459_window_b\csv\XBreaking_probe_XAUUSD_H4_20250107_010000.csv`
  - `tester_report`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\xauusd_h4_jan0714_20260701T124459_window_b\report\xbreaking_probe_xauusd_h4_jan0714.htm`
  - `tester_log`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\xauusd_h4_jan0714_20260701T124459_window_b\log\20260701.log`
  - `runtime_summary`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\xauusd_h4_jan0714_20260701T124459_window_b\run_summary.json`
- probe 总结：
  - `handle`: `10`
  - `init_err`: `0`
  - `status`: `DONE`
  - `buffer_activity_profile`: `buffer0_only`
  - 解释：在第二组后移窗口中，`XAUUSD / H4` 仍保持 `buffer0_only`，说明该访问形态对当前日期窗扰动不敏感。

## 第十三轮 validation-matrix 记录

- 批次信息：
  - `date_tag`: `20260702`
  - `platform`: `MT5`
  - `symbol`: `XTIUSD`
  - `chart_tf`: `PERIOD_H4`
  - `indicator_tf`: `PERIOD_H4`
  - `from_date`: `2024.12.01`
  - `to_date`: `2025.03.01`
  - `bars_to_probe`: `200`
  - `archive_tag`: `xtiusd_h4_tmgm_longwin_20260702T0418`
  - `csv`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\xtiusd_h4_tmgm_longwin_20260702T0418\csv\XBreaking_probe_XTIUSD_H4_20241202_010000.csv`
  - `tester_report`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\xtiusd_h4_tmgm_longwin_20260702T0418\report\xbreaking_probe_xtiusd_h4_tmgm_longwin.htm`
  - `tester_log`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\xtiusd_h4_tmgm_longwin_20260702T0418\log\20260702.log`
  - `runtime_summary`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\xtiusd_h4_tmgm_longwin_20260702T0418\run_summary.json`
- probe 总结：
  - `handle`: `10`
  - `init_err`: `0`
  - `status`: `DONE`
  - `buffer_activity_profile`: `buffer0_only`
  - 解释：在 `TradeMaxGlobal-Demo__60088394` 第二环境下，`XTIUSD / H4` 仍保持 `buffer0_only`，说明原油商品 broker alias 切到 `XTIUSD` 后，`single_buffer_access_pattern` 也能在商品 `H4` 样本上复现，而不只是停留在 `H1`。

## 第十四轮 validation-matrix 记录

- 批次信息：
  - `date_tag`: `20260702`
  - `platform`: `MT5`
  - `symbol`: `US500`
  - `chart_tf`: `PERIOD_H4`
  - `indicator_tf`: `PERIOD_H4`
  - `from_date`: `2024.12.01`
  - `to_date`: `2025.03.01`
  - `bars_to_probe`: `200`
  - `archive_tag`: `us500_h4_tmgm_longwin_20260702T1926`
  - `csv`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\us500_h4_tmgm_longwin_20260702T1926\csv\XBreaking_probe_US500_H4_20241202_010000.csv`
  - `tester_report`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\us500_h4_tmgm_longwin_20260702T1926\report\xbreaking_probe_us500_h4_tmgm_longwin.htm`
  - `runtime_summary`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\us500_h4_tmgm_longwin_20260702T1926\run_summary.json`
- probe 总结：
  - `handle`: `10`
  - `init_err`: `0`
  - `status`: `DONE`
  - `buffer_activity_profile`: `buffer0_only`
  - 解释：在 `TradeMaxGlobal-Demo__60088394` 第二环境下，`US500 / H4` 继续保持 `buffer0_only`，说明跨环境结论已从 `US30 / NAS100` 进一步扩展到另一条已购股指数据对应样本，并成为新的 `recommended_cross_environment_seed_archive_tag`

## 第十五轮 validation-matrix 记录

- 批次信息：
  - `date_tag`: `20260702`
  - `platform`: `MT5`
  - `symbol`: `GER40`
  - `chart_tf`: `PERIOD_H4`
  - `indicator_tf`: `PERIOD_H4`
  - `from_date`: `2024.12.01`
  - `to_date`: `2025.03.01`
  - `bars_to_probe`: `200`
  - `archive_tag`: `ger40_h4_tmgm_longwin_20260702T1933`
  - `csv`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\ger40_h4_tmgm_longwin_20260702T1933\csv\XBreaking_probe_GER40_H4_20241202_021500.csv`
  - `tester_report`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\ger40_h4_tmgm_longwin_20260702T1933\report\xbreaking_probe_ger40_h4_tmgm_longwin.htm`
  - `runtime_summary`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\validation_matrix\ger40_h4_tmgm_longwin_20260702T1933\run_summary.json`
- probe 总结：
  - `handle`: `10`
  - `init_err`: `0`
  - `status`: `DONE`
  - `buffer_activity_profile`: `buffer0_only`
  - 解释：在 `TradeMaxGlobal-Demo__60088394` 第二环境下，`GER40 / H4` 继续保持 `buffer0_only`，说明跨环境结论已从 `US30 / NAS100 / US500` 继续扩展到德指样本，并接替成为新的 `recommended_cross_environment_seed_archive_tag`

## 第一轮 buffer 观察

- `buffer_id=0`
  - `copied`: `200`
  - `non_empty`: `200`
  - `first_valid`: `0.00000000`
  - `last_valid`: `0.00000000`
  - `suspected_role`: `candidate_state_or_placeholder`
  - `confidence`: `low`
  - `semantics_status`: `candidate`
  - 说明：当前只能确认 `buffer 0` 可稳定复制；但全窗口值均为 `0`，还不能把它解释成方向、价位或离散信号。
- `buffer_id=1..7`
  - `copied`: `-1`
  - `err`: `4806`
  - `non_empty`: `0`
  - `suspected_role`: `not_exposed_or_invalid_buffer_index`
  - `confidence`: `medium`
  - `semantics_status`: `rejected`
  - 说明：本轮更像是 probe 读取到了不存在或未暴露的 buffer，而不是“这些 buffer 只是暂时没信号”。

## 第一轮语义裁决

- 当前可确认：
  - `handle_ok`
  - `single_buffer_access_pattern`
  - `buffer_0_readable`
  - `buffer0_only_repeated_on_fx_metal_index_samples`
  - `buffer0_only_repeated_on_shifted_date_windows`
  - `buffer0_only_repeated_across_multiple_mt5_environments`
  - `buffer0_only_repeated_on_oil_alias_samples`
- 当前不能确认：
  - `buffer_0 = buy_signal`
  - `buffer_0 = sell_signal`
  - `buffer_0 = breakout_level`
  - `buffer_0 = hard_gate_ready`
- 当前记录的 `buffer_activity_profile` 可暂记为：
  - `single_buffer`

## 日志补证状态

- 已回收：
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\log\20260609.log`
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\log\20260609__excerpt.txt`
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\log\20260701.log`
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\log\20260701__excerpt.txt`
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\log\20260701_20260701T041405.log`
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\log\20260701_20260701T041405__excerpt.txt`
- 已回收 report：
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\tester_report\xbreaking_probe_portable.htm`
- 当前判断：
  - 当前 `20260609.log` 片段更像通用迁移日志，未检出 `XBreaking / XBreakingProbe / tester` 关键词，因此不能作为强相关 `XBreakingProbe tester journal` 的硬证据
  - 当前 `20260701_20260701T041405.log` 已明确记录 `testing of Experts\XBreakingProbe.ex5`、`program file added: \Indicators\XBreaking.ex5` 与 `XBreakingProbe: DONE`，可作为强相关 tester journal
  - 当前 `xbreaking_probe_portable.htm` 已把 `Expert / Symbol / H1 / InpIndicatorName / InpBarsToProbe` 固化为可复核报告
  - 当前 `validation_matrix\eurusd_h4_20260701_setmode\log\20260701.log` 已明确记录 `EURUSD,H4`、`InpIndicatorTf=16388` 与 `XBreakingProbe: DONE`
  - 当前 `validation_matrix\gbpusd_h4_20260701T\log\20260701.log` 已明确记录 `GBPUSD,H4`、`InpIndicatorTf=16388` 与 `XBreakingProbe: DONE`
  - 当前 `validation_matrix\usdjpy_h4_20260701T\log\20260701.log` 已明确记录 `USDJPY,H4`、`InpIndicatorTf=16388` 与 `XBreakingProbe: DONE`
  - 当前 `validation_matrix\usdjpy_h1_20260701T\log\20260701.log` 已明确记录 `USDJPY,H1`、`InpIndicatorTf=16385` 与 `XBreakingProbe: DONE`
  - 当前 `validation_matrix\xauusd_h4_20260701T\log\20260701.log` 已明确记录 `XAUUSD,H4`、`InpIndicatorTf=16388` 与 `XBreakingProbe: DONE`
  - 当前 `validation_matrix\us30_h4_20260701T\log\20260701.log` 已明确记录 `US30,H4`、`InpIndicatorTf=16388` 与 `XBreakingProbe: DONE`
  - 当前 `validation_matrix\eurusd_h4_jan0310_20260701T124339_window_a\log\20260701.log` 与 `validation_matrix\eurusd_h4_jan0714_20260701T124459_window_b\log\20260701.log` 已明确记录两组日期窗口下的 `EURUSD,H4`
  - 当前 `validation_matrix\xauusd_h4_jan0310_20260701T124339_window_a\log\20260701.log` 与 `validation_matrix\xauusd_h4_jan0714_20260701T124459_window_b\log\20260701.log` 已明确记录两组日期窗口下的 `XAUUSD,H4`
  - 当前 `environment_snapshots\mt_environment_inventory_latest.json` 已确认本机已有 `2` 套 `MT5` 环境，环境标签为 `ICMarketsSC-Demo__52886989` 与 `TradeMaxGlobal-Demo__60088394`，并可直接作为 rerun 入口的 `EnvironmentSelector`
  - 当前 `validation_matrix\eurusd_h4_overridecheck_20260701T\run_summary.json` 已确认 `DataRootOverride` 显式选择链路可用，且归档内已绑定 `data_root / server / login / access_server`
  - 当前 `validation_matrix\eurusd_h4_envselect_20260701T1305\run_summary.json` 已确认 `EnvironmentInventoryJson + EnvironmentSelector` 选环境链路可用，且归档内已绑定 `selection_mode=inventory_selector / inventory_selector / inventory_match_field`
  - 当前 `validation_matrix\eurusd_h4_envselect_hard_20260701T1426\run_summary.json` 已补齐 `selection_mode=inventory_selector` 的 hard evidence（包含 `environment_inventory_*` 字段）
  - 当前 `validation_matrix\eurusd_h4_override_hard_20260701T1426\run_summary.json` 已补齐 `selection_mode=data_root_override` 的 hard evidence
  - 当前 `validation_matrix\gbpusd_h4_envselect_hard_20260701T1535\run_summary.json` 已把 selection_mode hard evidence 扩展到 `GBPUSD/H4`（inventory_selector）
  - 当前 `validation_matrix\gbpusd_h4_override_hard_20260701T1535\run_summary.json` 已把 selection_mode hard evidence 扩展到 `GBPUSD/H4`（data_root_override）
  - 当前 `validation_matrix\usdjpy_h1_envselect_hard_20260701T1608\run_summary.json` 已把 selection_mode hard evidence 扩展到 `USDJPY/H1`（inventory_selector）
  - 当前 `validation_matrix\usdjpy_h1_override_hard_20260701T1608\run_summary.json` 已把 selection_mode hard evidence 扩展到 `USDJPY/H1`（data_root_override）
  - 当前 `validation_matrix\eurusd_h4_envselect_feb_20260701T1615\run_summary.json` 已对更远日期窗 `2025.02.03~2025.02.10` 做了 `EURUSD/H4` 复跑，用于验证 `buffer0_only` 是否对日期窗扰动不敏感（selection_mode=inventory_selector）
  - 当前 `validation_matrix\usdjpy_h1_envselect_feb_20260701T1625\run_summary.json` 已对更远日期窗 `2025.02.03~2025.02.10` 做了 `USDJPY/H1` 复跑，用于确认日期窗鲁棒性结论是否跨 `symbol/timeframe` 复现（selection_mode=inventory_selector）
  - 当前 `validation_matrix\eurusd_h4_envselect_longwin_20260702T0038\run_summary.json` 已对跨月长窗口 `2024.12.01~2025.03.01` 做了 `EURUSD/H4` 复跑，用于确认 `buffer0_only` 是否在更长样本区间下仍稳定成立（selection_mode=inventory_selector）
  - 当前 `validation_matrix\usdjpy_h1_envselect_longwin_20260702T0041\run_summary.json` 已对跨月长窗口 `2024.12.01~2025.03.01` 做了 `USDJPY/H1` 复跑，用于确认长窗口鲁棒性结论是否继续跨 `symbol/timeframe` 复现（selection_mode=inventory_selector）
  - 当前 `validation_matrix\xauusd_h4_envselect_longwin_20260702T0044\run_summary.json` 已对跨月长窗口 `2024.12.01~2025.03.01` 做了 `XAUUSD/H4` 复跑，用于确认长窗口鲁棒性结论是否继续扩展到黄金品种（selection_mode=inventory_selector）
  - 当前 `validation_matrix\us30_h4_envselect_longwin_20260702T0054\run_summary.json` 已对跨月长窗口 `2024.12.01~2025.03.01` 做了 `US30/H4` 复跑，用于确认长窗口鲁棒性结论是否继续扩展到股指品种（selection_mode=inventory_selector）
  - 当前 `validation_matrix\us30_h4_tmgm_longwin_20260702T0137\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `US30/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认 `buffer0_only` 是否不是 `ICMarketsSC-Demo__52886989` 单环境特例（selection_mode=inventory_selector）
  - 当前 `validation_matrix\eurusd_h4_tmgm_longwin_20260702T0143\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `EURUSD/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论不只停留在股指样本，也能扩展到外汇主对（selection_mode=inventory_selector）
  - 当前 `validation_matrix\usdjpy_h1_tmgm_longwin_20260702T0145\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `USDJPY/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论也能扩展到日系与不同周期样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\gbpusd_h4_tmgm_longwin_20260702T0147\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `GBPUSD/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到英镑 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\xauusd_h4_tmgm_longwin_20260702T0152\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `XAUUSD/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论也能扩展到黄金 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\eurusd_h1_tmgm_longwin_20260702T0202\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `EURUSD/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到主对 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\usdjpy_h4_tmgm_longwin_20260702T0210\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `USDJPY/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到日系 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\us30_h1_tmgm_longwin_20260702T0222\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `US30/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到股指 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\xauusd_h1_tmgm_longwin_20260702T0234\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `XAUUSD/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到黄金 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\gbpusd_h1_tmgm_longwin_20260702T0250\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `GBPUSD/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到英镑 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\xagusd_h1_tmgm_longwin_20260702T0302\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `XAGUSD/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到白银 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\xagusd_h4_tmgm_longwin_20260702T0315\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `XAGUSD/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到白银 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\nas100_h1_tmgm_longwin_20260702T0332\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `NAS100/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的股指 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\nas100_h4_tmgm_longwin_20260702T0346\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `NAS100/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的股指 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\us500_h1_tmgm_longwin_20260702T1925\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `US500/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到另一条已购股指 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\us500_h4_tmgm_longwin_20260702T1926\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `US500/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到另一条已购股指 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\ger40_h1_tmgm_longwin_20260702T1932\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `GER40/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到德指 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\ger40_h4_tmgm_longwin_20260702T1933\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `GER40/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到德指 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\audusd_h1_tmgm_longwin_20260702T2022\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `AUDUSD/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\audusd_h4_tmgm_longwin_20260702T2024\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `AUDUSD/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\usdchf_h1_tmgm_longwin_20260702T2034\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `USDCHF/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\usdchf_h4_tmgm_longwin_20260702T2035\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `USDCHF/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\usdcad_h1_tmgm_longwin_20260702T2110\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `USDCAD/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\usdcad_h4_tmgm_longwin_20260702T2111\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `USDCAD/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\nzdusd_h1_tmgm_longwin_20260702T2128\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `NZDUSD/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\nzdusd_h4_tmgm_longwin_20260702T2129\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `NZDUSD/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\eurjpy_h1_tmgm_longwin_20260702T2144\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `EURJPY/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\eurjpy_h4_tmgm_longwin_20260702T2145\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `EURJPY/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\gbpjpy_h1_tmgm_longwin_20260702T2203\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `GBPJPY/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\gbpjpy_h4_tmgm_longwin_20260702T2204\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `GBPJPY/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\eurgbp_h1_tmgm_longwin_20260702T2220\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `EURGBP/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\eurgbp_h4_tmgm_longwin_20260702T2221\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `EURGBP/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\chfjpy_h1_tmgm_longwin_20260702T2233\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `CHFJPY/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\chfjpy_h4_tmgm_longwin_20260702T2234\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `CHFJPY/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\eurchf_h1_tmgm_longwin_20260702T2247\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `EURCHF/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\eurchf_h4_tmgm_longwin_20260702T2248\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `EURCHF/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\audnzd_h1_tmgm_longwin_20260702T2310\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `AUDNZD/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\audnzd_h4_tmgm_longwin_20260702T2311\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `AUDNZD/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\cadjpy_h1_tmgm_longwin_20260702T2331\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `CADJPY/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\cadjpy_h4_tmgm_longwin_20260702T2332\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `CADJPY/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\euraud_h1_tmgm_longwin_20260702T2353\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `EURAUD/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\euraud_h4_tmgm_longwin_20260702T2354\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `EURAUD/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\gbpchf_h1_tmgm_longwin_20260703T0007\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `GBPCHF/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\gbpchf_h4_tmgm_longwin_20260703T0008\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `GBPCHF/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\eurnzd_h1_tmgm_longwin_20260703T0027\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `EURNZD/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\eurnzd_h4_tmgm_longwin_20260703T0028\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `EURNZD/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\audjpy_h1_tmgm_longwin_20260703T0038\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `AUDJPY/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\audjpy_h4_tmgm_longwin_20260703T0039\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `AUDJPY/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\nzdjpy_h1_tmgm_longwin_20260703T0115\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `NZDJPY/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H1 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\nzdjpy_h4_tmgm_longwin_20260703T0116\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `NZDJPY/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认跨环境结论可继续扩展到新的已购外汇 H4 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\ger30_h1_tmgm_longwin_20260702T1942\run_summary.json` 只形成了失败别名证据：TMGM 第二环境 tester 日志明确显示 `symbol GER30 not exist`，因此该品种在当前 broker 下不能直接用 `GER30` 作为德指主线 symbol
  - 当前 `validation_matrix\usoil_h1_tmgm_longwin_20260702T0400\run_summary.json` 只形成了失败别名证据：TMGM 第二环境 tester 日志明确显示 `symbol USOIL not exist`，因此该品种在当前 broker 下不能直接用 `USOIL` 作为商品主线 symbol
  - 当前 `validation_matrix\ukoil_h1_tmgm_longwin_20260702T1918\run_summary.json` 也只形成了旧命名失败别名证据：TMGM 第二环境 tester 日志明确显示 `symbol UKOIL not exist`，因此该品种在当前 broker 下不能继续直接用 `UKOIL` 作为商品主线 symbol
  - 当前 `validation_matrix\xcuusd_h1_tmgm_longwin_20260702T1950\run_summary.json` 也只形成了失败别名证据：TMGM 第二环境 tester 日志明确显示 `symbol XCUUSD not exist`，因此该品种在当前 broker 下也不能直接用 `XCUUSD` 作为商品主线 symbol
  - 当前 `validation_matrix\coppercmdusd_h1_tmgm_longwin_20260703T0216\run_summary.json` 进一步形成了候选 alias 失败证据：TMGM 第二环境原始 tester 日志明确显示 `symbol COPPERCMDUSD not exist`，因此 `XCUUSD` 当前也不能直接收敛到 `COPPERCMDUSD`
  - 当前 TMGM 公开 `Trading Hours / Swap Free Account` 页面又把 `CHCUSD` 明确标成 `CHINA A50` 指数，而非铜类 instrument；公开 `Precious Metals` 页面则只列 `XAUUSD / XAGUSD / XPTUSD`，因此 `CHCUSD` 当前也不能作为 `XCUUSD` 的 broker alias 候选，且截至当前公共产品面仍未发现 TMGM 对外暴露的铜类 ticker
  - 当前 `validation_matrix\dollaridxusd_h1_tmgm_longwin_20260702T1959\run_summary.json` 也只形成了失败别名证据：TMGM 第二环境 tester 日志明确显示 `symbol DOLLARIDXUSD not exist`，因此该附加资产在当前 broker 下也不能直接用 `DOLLARIDXUSD` 作为主线 symbol
  - 当前 `validation_matrix\usdx_h1_tmgm_longwin_20260703T0222\run_summary.json` 与 `validation_matrix\dxy_h1_tmgm_longwin_20260703T0226\run_summary.json` 进一步形成了候选 alias 失败证据：TMGM 第二环境原始 tester 日志明确显示 `symbol USDX not exist` 与 `symbol DXY not exist`，因此 `DOLLARIDXUSD` 当前也不能直接收敛到 `USDX / DXY`
  - 当前 `validation_matrix\usidx_h1_tmgm_longwin_20260703T0247\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `USIDX/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认 `DOLLARIDXUSD` 旧命名应优先收敛到 `USIDX` 这条美元指数 broker alias（selection_mode=inventory_selector）
  - 当前 `validation_matrix\usidx_h4_tmgm_longwin_20260703T0248\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `USIDX/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认 `DOLLARIDXUSD -> USIDX` 这条 alias 对照链可继续扩展到 `H4` 样本（selection_mode=inventory_selector）
  - 当前 `validation_matrix\gbridxgbp_h1_tmgm_longwin_20260703T0125\run_summary.json` 也只形成了失败别名证据：TMGM 第二环境 tester 日志明确显示 `symbol GBRIDXGBP not exist`，因此该英股/英镑指数旧命名在当前 broker 下也不能直接用 `GBRIDXGBP` 作为主线 symbol
  - 当前 `validation_matrix\xtiusd_h1_tmgm_longwin_20260702T0406\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `XTIUSD/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认当前 broker 下原油商品的可用别名应切到 `XTIUSD`（selection_mode=inventory_selector）
  - 当前 `validation_matrix\xtiusd_h4_tmgm_longwin_20260702T0418\log\20260702.log` 已明确记录 `XTIUSD,H4`、`InpIndicatorTf=16388` 与 `XBreakingProbe: DONE`，可作为原油别名 `H4` 样本的强相关 tester journal
  - 当前 `validation_matrix\xbrusd_h1_tmgm_longwin_20260703T0159\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `XBRUSD/H1` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认 `UKOIL` 旧命名应优先收敛到 `XBRUSD` 这条 Brent 商品 broker alias（selection_mode=inventory_selector）
  - 当前 `validation_matrix\xbrusd_h4_tmgm_longwin_20260703T0200\run_summary.json` 已在第二套 `MT5` 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `XBRUSD/H4` 跨月长窗口 `2024.12.01~2025.03.01` 复跑，用于确认 `UKOIL -> XBRUSD` 这条 alias 对照链可继续扩展到 `H4` 样本（selection_mode=inventory_selector）
  - 当前已形成跨周期、跨外汇、跨黄金、跨股指、跨日期窗口、跨月长窗口与跨 `MT5` 环境的 `csv + tester report + tester journal` 复核闭环；当前 `environment_snapshots\mt_environment_inventory_latest.json` 已包含 `ICMarketsSC-Demo__52886989` 与 `TradeMaxGlobal-Demo__60088394` 两个 `MT5` 环境标签，因此 `cross_environment_ready=true`、`cross_environment_verified=true`

## 下一步

1. 继续补第二环境下剩余未覆盖的 `symbol/timeframe` 对照样本；当前已覆盖 `EURUSD / GBPUSD / USDJPY / AUDUSD / USDCHF / USDCAD / NZDUSD / EURJPY / GBPJPY / EURGBP / CHFJPY / EURCHF / AUDJPY / AUDNZD / CADJPY / EURAUD / GBPCHF / EURNZD / NZDJPY / XAUUSD / XAGUSD / US30 / NAS100 / US500 / GER40 / XTIUSD / XBRUSD / USIDX` 的 `H1/H4`，并额外保留了 `GER30/H1`、`GBRIDXGBP/H1`、`USOIL/H1`、`UKOIL/H1`、`XCUUSD/H1`、`COPPERCMDUSD/H1`、`DOLLARIDXUSD/H1`、`USDX/H1` 与 `DXY/H1` 的旧命名或候选 alias 失败证据；当前公共产品面还额外排除了 `CHCUSD -> CHINA A50` 这条假候选
2. 若后续仍只暴露 `buffer 0`，可把 `buffer0_only` 写进字段草案复核
3. 当前已具备跨环境硬证据与原油 alias 证据，可开始准备字段草案升级输入，并把已购 CSV 标准化入口作为外部对照层
4. 只在多轮验证稳定后，才升级 `XBreaking` 字段草案版本
