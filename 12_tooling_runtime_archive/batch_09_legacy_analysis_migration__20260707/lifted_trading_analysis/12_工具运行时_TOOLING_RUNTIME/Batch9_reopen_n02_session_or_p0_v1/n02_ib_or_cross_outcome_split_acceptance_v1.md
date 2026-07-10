# N02 IB OR 过交叉结果分桶验收 v1

## 目的

- 记录 `REOPEN_B9_N02_IB_OR_CROSS_OUTCOME_SPLIT_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `n02_ib_or_break_bar_evidence_p0_sample_v1.csv`
- 生成脚本：
  - `n02_ib_or_cross_outcome_split_p0_build_v1.py`
- 输出：
  - `n02_ib_or_confirmed_cross_candidates_p0_sample_v1.csv`
  - `n02_ib_or_or_break_only_candidates_p0_sample_v1.csv`
  - `n02_ib_or_confirmed_cross_outcome_shell_p0_sample_v1.csv`
  - `n02_ib_or_cross_outcome_split_p0_summary_v1.json`

## 2026-07-03 fresh-run 验收

- 验收方式：
  - `python n02_ib_or_cross_outcome_split_p0_build_v1.py`
- 本轮结果：
  - `input_rows=138`
  - `confirmed_cross_rows=15`
  - `or_break_only_rows=123`
  - `outcome_shell_rows=15`
  - `direction_mode_mismatch_rows=1`
  - `london confirmed_cross_rows=2`
  - `new_york confirmed_cross_rows=13`
- 当前结论：
  - `138` 行已全部进入 `confirmed cross / OR break only` 两支之一。
  - `15` 行 `confirmed cross` 已补齐最小 `outcome_shell`。
  - `123` 行 `OR break only` 已与 `confirmed cross` 完成分流。
  - 当前仍仅存证 `1` 行 direction/mode 漂移，不回写上游。

## 关键统计

- `confirmed_cross=15`
- `or_break_only=123`
- `outcome_shell=15`
- `direction_mode_mismatch=1`
- `london_confirmed_cross=2`
- `newyork_confirmed_cross=13`

## 当前不通过项

- 当前还没有为 `confirmed_cross_outcome_shell` 补 post-cross path 结果定义。
- 当前还没有把 `OR break only` 分支扩展成独立 outcome。
- 当前仍不进入 `failed breakout / retest / reject / day type`。
