# N02 IB OR 突破K线证据验收 v1

## 目的

- 记录 `REOPEN_B9_N02_IB_OR_BREAK_BAR_EVIDENCE_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `n02_ib_or_first_break_relative_p0_sample_v1.csv`
  - `n02_ib_or_relation_p0_sample_v1.csv`
  - `real_input_samples\n02_first_real_input_bars_v1.csv`
- 生成脚本：
  - `n02_ib_or_break_bar_evidence_p0_build_v1.py`
- 输出：
  - `n02_ib_or_break_bar_evidence_p0_sample_v1.csv`
  - `n02_ib_or_break_bar_evidence_p0_summary_v1.json`

## 2026-07-03 fresh-run 验收

- 验收方式：
  - `python n02_ib_or_break_bar_evidence_p0_build_v1.py`
- 本轮结果：
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
  - 这层已拿到全部 `138` 行的首破当根价位证据。
  - 当前只有 `15` 行已穿过 `IB` 同侧边界，其余 `123` 行未穿过。
  - 当前发现 `1` 行上游 `direction/mode` 与 bar-level 复检不一致，已作为漂移证据保留。

## 漂移样本

- 当前唯一 `direction_mode_mismatch`：
  - `session_id=new_york`
  - `session_local_date=2026-05-07`
  - 上游 relation：`first_break_direction=down` + `first_break_mode=close`
  - bar-level 复检：`first_break_direction=down` + `first_break_mode=wick`
  - 当前处理：仅存证，不反写修正上游 relation

## 关键统计

- `cross_confirmed=15`
- `not_crossed=123`
- `cross_confirmed_ratio=0.10869565217391304`
- `direction_mode_match=137`
- `direction_mode_mismatch=1`
- `london_cross_confirmed=2`
- `newyork_cross_confirmed=13`

## 当前不通过项

- 当前尚未把 `15` 行 confirmed cross 继续扩展为 `failed breakout / retest / reject`。
- 当前 `1` 行 direction/mode 漂移尚未回写修正上游 relation，仅作证据保留。
- 当前仍只覆盖 `EURUSD M1` 的 `london/new_york` 已定义样本。
