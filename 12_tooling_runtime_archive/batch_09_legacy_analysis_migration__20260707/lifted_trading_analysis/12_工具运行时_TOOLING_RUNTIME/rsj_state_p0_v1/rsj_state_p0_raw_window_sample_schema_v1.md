# RSJ State P0 原始窗口样本结构 v1

- ARCHIVE_ONLY_SAMPLE_SCHEMA: 本文件只保留旧 `RSJ State P0` 的历史样例结构说明，不作为当前默认接线入口。
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 目的

- 把 `raw window input contract` 再下压一层，给出可直接喂给后续接口壳的历史样例行结构。
- 历史上只冻结样例格式与字段语义，不代表已经接入真实收益率序列重建。

## 对应文件

- input contract：
  - `rsj_state_p0_raw_window_input_contract_v1.md`
- input header：
  - `rsj_state_p0_raw_window_input_header_v1.txt`
- sample input：
  - `real_input_samples\rsj_state_p0_raw_window_sample_input_v1.csv`
- append interface：
  - `rsj_state_p0_append_from_raw_window_stub_v1.py`

## 样例行定义

- 每一行表示一个已经汇总完成的 `raw window summary`，不是逐 bar 明细表。
- `bar_time` 表示该窗口结束时点。
- `window_bars` 表示形成该窗口时实际使用的 bar 数量。
- `rv_up / rv_down` 只要求满足当前 `RSJ P0` 合同，不在本文件中定义其工程重建方法。
- `input_source_tier` 在历史样例里优先允许使用：
  - `synthetic_window`
  - `pending_real_binding`
  - 只表示历史样例曾预留历史外部绑定占位，不代表当前 repo-first 已接线

## 推荐校验

- `trade_id` 全文件唯一。
- `bar_time` 使用 `ISO8601`。
- `window_bars > 0`。
- `rv_up >= 0` 且 `rv_down >= 0`。
- `rv_up + rv_down > 0`。
- `input_note` 说明该样例用于哪一种状态验证。

## 示例行说明

| trade_id | target_state | interpretation |
|---|---|---|
| `RSJ_RAW_SAMPLE_001` | `warm` | 上行波动明显高于下行波动 |
| `RSJ_RAW_SAMPLE_002` | `neutral` | 正负波动接近平衡 |
| `RSJ_RAW_SAMPLE_003` | `cold` | 下行波动明显高于上行波动 |

## 历史边界

- v1 不把样例 csv 当成真实行情回放结果。
- v1 不要求 `append_from_raw_window` 已能读取并写入 runtime csv。
- v1 只负责让未来历史外部绑定前，字段样子与样例内容先冻结下来。
