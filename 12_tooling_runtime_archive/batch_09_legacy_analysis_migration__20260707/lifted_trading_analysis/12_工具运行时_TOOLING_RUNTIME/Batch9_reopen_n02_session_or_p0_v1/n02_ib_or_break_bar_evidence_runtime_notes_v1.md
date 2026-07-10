# N02 IB OR 突破K线证据运行说明 v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `IB_OR first break` 的当根价位证据口径。

## 当前边界

- 不写回：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `n02_ib_or_relation_p0_sample_v1.csv`
  - `n02_ib_or_first_break_relative_p0_sample_v1.csv`
- 当前只落：
  - `n02_ib_or_break_bar_evidence_p0_sample_v1.csv`
  - `n02_ib_or_break_bar_evidence_p0_summary_v1.json`
- 当前不推进：
  - `IB acceptance`
  - `IB failed breakout`
  - `IB retest/reject`
  - `day type`

## 当前怎么用（v1）

- 输入：
  - `n02_ib_or_first_break_relative_p0_sample_v1.csv`
  - `n02_ib_or_relation_p0_sample_v1.csv`
  - `real_input_samples\n02_first_real_input_bars_v1.csv`
  - `real_input_samples\n02_or_proof_config_v1.json`
- 生成脚本：
  - `n02_ib_or_break_bar_evidence_p0_build_v1.py`
- 输出：
  - `n02_ib_or_break_bar_evidence_p0_sample_v1.csv`
  - `n02_ib_or_break_bar_evidence_p0_summary_v1.json`
- 当前字段会给出：
  - `break_bar_time_utc`
  - `break_bar_open/high/low/close`
  - `break_trigger_price`
  - `break_trigger_source`
  - `ib_same_side_cross_confirmed`
  - `direction_mode_match_to_relation`

## 推荐复现命令

- `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_break_bar_evidence_p0_build_v1.py`

## 2026-07-03 fresh-run 结果

- 运行入口：
  - `python n02_ib_or_break_bar_evidence_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_break_bar_evidence_p0_sample_v1.csv`
  - `n02_ib_or_break_bar_evidence_p0_summary_v1.json`
- 关键统计：
  - `input_rows=138`
  - `output_rows_written=138`
  - `ib_same_side_cross_confirmed_rows=15`
  - `ib_same_side_not_crossed_rows=123`
  - `ib_same_side_cross_confirmed_ratio=0.10869565217391304`
  - `direction_mode_match_rows=137`
  - `direction_mode_mismatch_rows=1`
  - `london cross_confirmed_rows=2`
  - `new_york cross_confirmed_rows=13`
- 当前结论：
  - `break price / bar-level break evidence` 已完成 fresh-run 闭环。
  - `requires_break_price_for_ib_confirmation` 这一层已被真实当根价位证据取代。
  - 当前只有 `15` 行可确认已穿过 `IB` 同侧边界。
  - 当前保留 `1` 行 direction/mode 漂移证据，不能继续假定上游 relation 永远无误。
  - 漂移样本当前定位为：`new_york / 2026-05-07`，上游写成 `down+close`，bar-level 复检为 `down+wick`

## 2026-07-03 cross outcome split child fresh-run

- 运行入口：
  - `python n02_ib_or_cross_outcome_split_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_confirmed_cross_candidates_p0_sample_v1.csv`
  - `n02_ib_or_or_break_only_candidates_p0_sample_v1.csv`
  - `n02_ib_or_confirmed_cross_outcome_shell_p0_sample_v1.csv`
  - `n02_ib_or_cross_outcome_split_p0_summary_v1.json`
- 关键统计：
  - `confirmed_cross_rows=15`
  - `or_break_only_rows=123`
  - `outcome_shell_rows=15`
  - `direction_mode_mismatch_rows=1`
- 当前结论：
  - 当前主线已从“拿到 break 当根证据”进入“按 cross/not-cross 稳定分流”
  - `outcome_shell` 当前只是 post-cross 跟踪入口，不等于结果定义

## 当前最顺动作

- 若继续推进，优先补：
  - `confirmed cross` 分支的 post-cross path 定义
  - 或 `OR break only` 分支的稳定说明卡
- 继续保持不做：
  - `acceptance`
  - `retest / reject`
  - `day type`
