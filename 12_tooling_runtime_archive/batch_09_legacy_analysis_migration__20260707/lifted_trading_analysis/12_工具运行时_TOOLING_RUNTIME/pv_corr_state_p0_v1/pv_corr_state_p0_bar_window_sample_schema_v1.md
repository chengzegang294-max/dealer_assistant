# pv_corr_state_p0_bar_window_sample_schema_v1

- ARCHIVE_ONLY_SAMPLE_SCHEMA: 本文件只保留旧 `PV Corr State P0` 的历史样例结构说明，不作为当前默认接线入口。
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 目的

- 把 `bar window input contract` 再下压一层，给出可直接喂给后续接口壳的历史样例行结构。
- 历史上只冻结样例格式与字段语义，不代表已经接入真实 `bar window` 源。

## 对应文件

- input contract：
  - `pv_corr_state_p0_bar_window_input_contract_v1.md`
- input header：
  - `pv_corr_state_p0_bar_window_input_header_v1.txt`
- sample input：
  - `real_input_samples\pv_corr_state_p0_bar_window_sample_input_v1.csv`
- append interface：
  - `pv_corr_state_p0_append_from_bar_window_stub_v1.py`

## 样例行定义

- 每一行表示一个已经汇总完成的 `bar window summary`，不是逐根 bar 原始明细。
- `bar_time` 表示该窗口结束时点。
- `pv_corr_score`、`price_net_change`、`volume_net_change` 都是窗口级汇总结果。
- `input_volume_kind` 用来区分 `real / tick / synthetic` 三类量能口径。
- `input_source_tier` 在历史样例里优先允许使用：
  - `synthetic_window`
  - `pending_real_binding`
  - 只表示历史样例曾预留历史外部绑定占位，不代表当前 repo-first 已接线

## 推荐校验

- `trade_id` 全文件唯一。
- `bar_time` 使用 `ISO8601`。
- `window_bars > 0`。
- `pv_corr_score` 落在 `[-1, 1]`。
- `price_net_change` 与 `volume_net_change` 必须可解析为数字。
- `input_note` 要说明该样例用于验证 `confirm / diverge / neutral` 中哪一类。

## 示例行说明

| trade_id | target_state | interpretation |
|---|---|---|
| `PVC_BAR_SAMPLE_001` | `confirm` | 价量同向且相关性较强 |
| `PVC_BAR_SAMPLE_002` | `diverge` | 价格与量变化异向但相关性较强 |
| `PVC_BAR_SAMPLE_003` | `neutral` | 相关性较弱，不形成有效状态 |

## 历史边界

- v1 不把样例 csv 当成真实 broker/bar 链路产物。
- v1 不要求 `append_from_bar_window` 已能读取并写入 runtime csv。
- v1 只负责让未来历史外部绑定前，字段样子与样例内容先冻结下来。
