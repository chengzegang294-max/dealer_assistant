# N02 IB 运行说明 v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `IB`（`N02` 后续对象层）的运行时证据口径与边界。
- 当前仅对应：
  - `IB proof-of-mapping`
- 当前不对应：
  - 真实接入
  - 写入 `N02 P0` runtime 主 CSV

## 当前不含（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
- 不推进：
  - `IB acceptance`
  - `IB failed breakout`
  - `IB retest/reject`
  - `VA / POC / Day Type`

## 当前怎么用（v1）

- proof 三件套（可复现）：
  - `real_input_csv`：
    - 主样本：`real_input_samples\n02_first_real_input_bars_v1.csv`
    - 可选补样本（按 session 定向补覆盖，避免互相制造 `ib_defined=0` 噪音）：
      - `real_input_samples\n02_dst_london_spring_20260327_20260331_bars.csv`
      - `real_input_samples\n02_dst_newyork_spring_20260306_20260310_bars.csv`
  - `proof_script_py`：`real_input_samples\n02_ib_proof_of_mapping_v1.py`
  - `proof_output_csv`：`real_input_samples\n02_ib_proof_of_mapping_output_v1.csv`
- `IB runtime CSV`（不进入 N02 P0）：
  - `n02_ib_fields_runtime_v1.csv`
  - 追加脚本：`n02_ib_runtime_append_from_proof_v1.py`
  - 运行脚本会打印 `ib_defined` 覆盖概况（总比率 + 分 session）
  - 覆盖门槛（当前建议）：`london/new_york` 各自 `weekday_defined_ratio >= 0.90`
  - 可选输出 report：`--report-json <path>`
- `IB_OBJECT_P0` 派生链（仍不进入 N02 P0）：
  - 生成脚本：`n02_ib_object_p0_build_v1.py`
  - 对象样本：`n02_ib_object_p0_sample_v1.csv`
  - 对象摘要：`n02_ib_object_p0_summary_v1.json`
  - 只收 `ib_defined=1` 的 runtime 行，生成稳定 `object_id`
- `IB vs OR relation` 派生链（仍不进入 N02 P0）：
  - 生成脚本：`n02_ib_or_relation_p0_build_v1.py`
  - 关系样本：`n02_ib_or_relation_p0_sample_v1.csv`
  - 关系摘要：`n02_ib_or_relation_p0_summary_v1.json`
  - 验收说明：`n02_ib_or_relation_acceptance_v1.md`
- 合同说明：
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\n02_ib_contract_notes_v1.md`

### 推荐复现命令（门槛观察口径）

- 先生成 proof（按 session 定向采样 + 跳过边界残缺日）：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_ib_proof_of_mapping_v1.py --session-input london=n02_first_real_input_bars_v1.csv --session-input london=n02_dst_london_spring_20260327_20260331_bars.csv --session-input new_york=n02_first_real_input_bars_v1.csv --session-input new_york=n02_dst_newyork_spring_20260306_20260310_bars.csv --symbol EURUSD --timeframe M1 --skip-partial-days`
- 再 append 并打印覆盖概况：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_runtime_append_from_proof_v1.py --persist`

## 2026-07-03 fresh-run 结果

- 运行入口：
  - `python real_input_samples\n02_ib_proof_of_mapping_v1.py --session-input london=n02_first_real_input_bars_v1.csv --session-input london=n02_dst_london_spring_20260327_20260331_bars.csv --session-input new_york=n02_first_real_input_bars_v1.csv --session-input new_york=n02_dst_newyork_spring_20260306_20260310_bars.csv --symbol EURUSD --timeframe M1 --skip-partial-days`
  - `python n02_ib_runtime_append_from_proof_v1.py --persist`
- fresh-run 产物：
  - `real_input_samples\n02_ib_proof_of_mapping_output_v1.csv`
  - `n02_ib_fields_runtime_v1.csv`
- 关键统计：
  - `ib_proof_of_mapping_rows=138`
  - `runtime_rows_before=21`
  - `runtime_rows_after_append=138`
  - `ib_defined_ratio=1.0`
  - `ib_weekday_defined_ratio=1.0`
  - `session_id=london ratio=1.0`
  - `session_id=new_york ratio=1.0`
- 当前结论：
  - 这轮 `IB proof-of-mapping` 已完成 fresh-run 闭环，当前证据层覆盖已足够支撑进入 `IB_OBJECT_P0` 或继续推进 `N02 P0` 真实接入链。

## 2026-07-03 IB_OBJECT_P0 fresh-run

- 运行入口：
  - `python n02_ib_object_p0_build_v1.py --input d:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_fields_runtime_v1.csv --output-csv d:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_object_p0_sample_v1.csv --summary-json d:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_object_p0_summary_v1.json`
- fresh-run 产物：
  - `n02_ib_object_p0_sample_v1.csv`
  - `n02_ib_object_p0_summary_v1.json`
- 关键统计：
  - `source_rows=138`
  - `source_defined_rows=138`
  - `source_undefined_rows=0`
  - `object_rows_written=138`
  - `session_id=london object_rows=69 first_local_date=2026-03-09 last_local_date=2026-06-11`
  - `session_id=new_york object_rows=69 first_local_date=2026-03-09 last_local_date=2026-06-11`
- provenance 说明：
  - 首轮运行发现 `resolve()` 会把默认路径回落到旧仓 `trading_analysis`
  - 已把 `n02_ib_object_p0_build_v1.py` 改为默认使用当前脚本所在目录，并再用默认命令复跑确认：对象样本与摘要已稳定落在新仓镜像层
- 当前结论：
  - `IB_OBJECT_P0` 已具备独立的 `build -> sample_csv -> summary_json` 最小证据链
  - 该链仍保持边界：不写回 `n02_p0_fields_runtime_v2.csv`

## 2026-07-03 IB vs OR relation fresh-run

- 运行入口：
  - `python n02_ib_or_relation_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_relation_p0_sample_v1.csv`
  - `n02_ib_or_relation_p0_summary_v1.json`
- 关键统计：
  - `relation_rows_written=138`
  - `missing_or_match_rows=0`
  - `or_inside_ib_rows=138`
  - `or_inside_ib_ratio=1.0`
  - `ib_equals_or_rows=14`
  - `width_error_day_rows=0`
- 当前结论：
  - 当前全部已定义样本下，`OR` 都位于 `IB` 内部
  - 该结果已从“对象层”扩到“关系层”，但仍不升级为行为标签或门控

## 下一步最顺动作

- 仍只做“对象本体层”推进：
  - 若要继续，就补 `first_break relative to OR/IB` 或更广样本覆盖
- 继续保持不做：
  - `IB acceptance`
  - `IB failed breakout`
  - `IB retest/reject`
  - `day type`
