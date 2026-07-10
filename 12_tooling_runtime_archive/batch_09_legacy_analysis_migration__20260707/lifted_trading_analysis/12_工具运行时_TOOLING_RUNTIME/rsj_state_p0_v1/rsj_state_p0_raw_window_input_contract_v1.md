# RSJ State P0 原始窗口输入合同 v1

- ARCHIVE_ONLY_INPUT_CONTRACT: 本文件只保留旧 `RSJ State P0` 的未来输入契约草图，不作为默认接线入口。
- repo-first 历史入口参考：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 目的

- 冻结 `RSJ State P0` 未来接入外部 `raw window` 输入时的历史最小输入契约草图。
- 本历史合同只定义字段与校验边界，不代表 repo-first 已接入外部数据源。

## 对应文件

- input header：
  - `rsj_state_p0_raw_window_input_header_v1.txt`
- append interface：
  - `rsj_state_p0_append_from_raw_window_stub_v1.py`

## 输入字段

| field | type | required | notes |
|---|---|---:|---|
| trade_id | string | yes | 输入行唯一 id |
| symbol | string | yes | 标的 |
| timeframe | string | yes | 例如 `H1 / H4 / D1` |
| bar_time | string | yes | ISO8601；窗口结束时点 |
| window_bars | number | yes | 窗口长度 |
| rv_up | number | yes | 正收益侧已实现波动代理；必须 `>= 0` |
| rv_down | number | yes | 负收益侧已实现波动代理；必须 `>= 0` |
| input_source_tier | string | yes | `proof_only / synthetic_window / pending_real_binding / audited_real_binding` |
| input_note | string | no | 备注 |

## v1 校验规则

- `trade_id` 不可为空
- `window_bars > 0`
- `rv_up >= 0`
- `rv_down >= 0`
- `rv_up + rv_down > 0`
- `input_source_tier` 只允许：
  - `proof_only`
  - `synthetic_window`
  - `pending_real_binding`
    - 只表示历史合同曾预留历史外部绑定占位，不代表当前 repo-first 已接线
  - `audited_real_binding`

## 历史边界

- v1 不定义：
  - 如何从 tick/minute 序列精确重建 `rv_up / rv_down`
  - 如何绑定真实行情源
  - 如何自动落 runtime csv
- v1 只解决：
  - 将来喂给 `append_from_raw_window` 的字段长什么样
  - 哪些字段必填
  - 哪些值非法

## 历史可宣称

- 已冻结未来 `raw window` 输入契约
- 已与 `RSJ P0` 最小合同保持一致

## 历史不可宣称

- 不可宣称真实 `raw window` 已可用
- 不可宣称已完成从真实收益率序列到 `rv_up / rv_down` 的工程重建
