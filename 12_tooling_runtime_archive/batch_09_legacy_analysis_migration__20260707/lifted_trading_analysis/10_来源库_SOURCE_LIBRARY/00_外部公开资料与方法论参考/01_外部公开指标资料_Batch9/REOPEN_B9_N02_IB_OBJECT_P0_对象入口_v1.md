# REOPEN_B9_N02 IB OBJECT_P0 对象入口 v1

## 作用

- 把 `IB` 从 “后续对象定义入口” 升级为可独立推进的 reopen 子项。
- 该子项只负责 `IB` 对象本体与其最小 runtime 证据闭环，不改动 `N02 P0` runtime 主 CSV。

## 当前边界（写死）

- 不写入：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_p0_fields_runtime_v2.csv`
- 不包含：
  - `IB acceptance`
  - `IB failed breakout`
  - `IB retest/reject`
  - `VA / POC / Day Type`

## 入口依赖

- session binding：
  - `session_id + session_timezone + session_local_date`
- bars 输入样本：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_first_real_input_bars_v1.csv`
  - 可选补样本（按 session 定向补覆盖）：
    - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_dst_london_spring_20260327_20260331_bars.csv`
    - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_dst_newyork_spring_20260306_20260310_bars.csv`

## 当前真值组成（v1）

- `object_entry_md`：`REOPEN_B9_N02_IB_OBJECT_P0_对象入口_v1.md`
- `entry_notes_md`：`REOPEN_B9_N02_IB_后续对象定义入口_v1.md`
- `contract_notes_md`：`n02_ib_contract_notes_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_runtime_notes_v1.md`
- `real_input_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_first_real_input_bars_v1.csv`
- `proof_script_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_ib_proof_of_mapping_v1.py`
- `proof_output_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_ib_proof_of_mapping_output_v1.csv`
- `ib_runtime_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_fields_runtime_v1.csv`
- `ib_append_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_runtime_append_from_proof_v1.py`
- `object_build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_object_p0_build_v1.py`
- `object_sample_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_object_p0_sample_v1.csv`
- `object_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_object_p0_summary_v1.json`
- `relation_entry_md`：`REOPEN_B9_N02_IB_OR_RELATION_P0_关系入口_v1.md`

## 最小验收（开题级）

- 能复现 `IB proof-of-mapping` 输出（已有）
- 能把 proof 输出合并进 `ib_runtime_csv`（新增）
- 能从 `ib_runtime_csv` 派生独立 `IB_OBJECT_P0 sample + summary`
- 至少满足：
  - `london` 与 `new_york` 各有 `ib_defined=1` 的 1 个本地日期行
  - 对这些行：`bars_in_ib_window=60` 且 `ib_start_utc/ib_end_utc` 非空
  - `object_sample_csv` 中每行都有稳定 `object_id`
  - `object_summary_json` 显式记录 `producer/source_path/repo_path/evidence_mode`

## 门槛观察（coverage）

- 目标：先把“样本覆盖不足导致 `ib_defined=0`”从工程歧义里剥离出来，形成可直接跑的门槛指标。
- 覆盖指标来自：`n02_ib_runtime_append_from_proof_v1.py` 的输出
  - `ib_defined_ratio`
  - `session_id=<...> ratio=<...>`
- 当前建议门槛（用于决定是否继续扩样本，而不是加字段）：
  - `london/new_york` 各自 `weekday_defined_ratio >= 0.90`
  - 最近一次观测（`--session-input` + `--skip-partial-days` 口径）：`london=1.0；new_york=1.0`

## 下一步最顺动作

- 先生成 proof（按 session 定向采样 + 跳过边界残缺日）：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_ib_proof_of_mapping_v1.py --session-input london=n02_first_real_input_bars_v1.csv --session-input london=n02_dst_london_spring_20260327_20260331_bars.csv --session-input new_york=n02_first_real_input_bars_v1.csv --session-input new_york=n02_dst_newyork_spring_20260306_20260310_bars.csv --symbol EURUSD --timeframe M1 --skip-partial-days`
- 再运行一次 runtime append：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_runtime_append_from_proof_v1.py --persist`
- 再从 `ib_runtime_csv` 生成对象样本与摘要：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_object_p0_build_v1.py --input d:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_fields_runtime_v1.csv --output-csv d:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_object_p0_sample_v1.csv --summary-json d:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_object_p0_summary_v1.json`

## 2026-07-03 OBJECT_P0 fresh-run

- 运行入口：
  - `python n02_ib_object_p0_build_v1.py --input d:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_fields_runtime_v1.csv --output-csv d:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_object_p0_sample_v1.csv --summary-json d:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_object_p0_summary_v1.json`
- fresh-run 产物：
  - `n02_ib_object_p0_sample_v1.csv`
  - `n02_ib_object_p0_summary_v1.json`
- 关键统计：
  - `source_rows=138`
  - `source_defined_rows=138`
  - `object_rows_written=138`
  - `london object_rows=69`
  - `new_york object_rows=69`
- provenance 说明：
  - 首轮运行暴露出 `resolve()` 会把默认路径回落到旧仓；现已把 `n02_ib_object_p0_build_v1.py` 的默认目录绑定到当前脚本所在镜像层
  - 已再用默认命令复跑确认：默认输入/输出已稳定落在 `trading_assistant` 路径
- 当前裁决：
  - `REOPEN_B9_N02_IB_OBJECT_P0` 已从“入口开题”升级为“对象样本与摘要均可复现”
  - 仍不进入 `IB acceptance / failed breakout / retest-reject / day type`

## 2026-07-03 relation child 已开

- 已新增关系入口：
  - `REOPEN_B9_N02_IB_OR_RELATION_P0_关系入口_v1.md`
- 已新增关系层产物：
  - `n02_ib_or_relation_p0_sample_v1.csv`
  - `n02_ib_or_relation_p0_summary_v1.json`
- 关系层当前最小裁决：
  - `relation_rows_written=138`
  - `missing_or_match_rows=0`
  - `or_inside_ib_ratio=1.0`
- 当前含义：
  - `IB_OBJECT_P0` 不再只有对象本体样本，已经向下游关系层扩出第一条可复现子链
