# n02_p0_runtime_append_protocol v1

## 目的

- 规定未来脚本向 `n02_p0_fields_runtime_v1.csv` 追加第一批真实数据时应遵守的最小流程。
- 避免把占位样本行、真实运行行和后续版本升级混在一起。

## 当前前提

- 当前 CSV 已有：
  - `1` 行表头
  - 已 append 的第一批真实 proof 行
- 当前真实行来自：
  - `real_input_samples\n02_proof_of_mapping_output_v1.csv`
- 当前 append 动作通过：
  - `n02_p0_runtime_append_from_proof_v1.py`
  已完成一次正式 persist 证据。
- 当前运行时目录还已新增：
  - `n02_p0_runtime_params_template_v1.json`
  - `n02_p0_runtime_append_stub_v1.py`
  - `n02_p0_runtime_append_from_proof_v1.py`

## 追加真实数据前先做什么

1. 检查表头是否仍与 `n02_p0_fields_runtime_header_v1.txt` 一致
2. 检查本次仍只输出 `N02 P0` 的 `12` 个字段
3. 删除或覆盖当前示例行
4. 在 `n02_p0_runtime_notes_v1.md` 记录本次 session 参数来源
5. 按 `n02_p0_runtime_params_template_v1.json` 检查本次配置口径
6. 对 `session_id / session_timezone / opening_range_window_minutes` 逐项检查：
   - `source_tier`
   - `source_basis`
   - `evidence_anchor`
   - `upgrade_rule`
7. 追加前优先检查 `session_binding_registry`：
   - `london -> Europe/London`
   - `new_york -> America/New_York`
8. 当前若落 `london` 或 `new_york`，应视为 Batch9 v1 已冻结 binding；若要新增 session，必须先补 registry 和来源说明
9. 对 registry 中命中的 session，还要确认：
   - `calendar_basis` 是否按该时区的本地日期解释
   - `dst_handling` 是否由时区规则推导，而不是手写固定 UTC 偏移
10. 真正接第一份数据前，先逐项过一遍：
   - `n02_p0_runtime_session_calendar_dst_checklist_v1.md`
11. 再核对真实输入是否符合：
   - `n02_p0_real_input_mapping_draft_v1.md`

## 第一批真实数据最小要求

- 至少有：
  - `symbol`
  - `timeframe`
  - `bar_time`
  - `session_id`
  - `session_timezone`
  - `opening_range_window_minutes`
- 对 OR 尚未定义的 bar：
  - 允许 `opening_range_* = na`
  - `opening_range_defined = 0`
  - `first_break_direction = none`
- 对 OR 已定义的 bar：
  - 应给出稳定的 `opening_range_high / low / mid / width`

## 不允许

- 不允许把当前示例行和真实数据长期混放
- 不允许偷偷加入 `IB` 字段
- 不允许改表头却还沿用 `v1` 文件名
- 不允许把 `close` vs `wick` 未拆的状态写成“已完成”

## 若需要升级到 v2

- 触发条件示例：
  - 表头变更
  - 新增运行时主键列
  - 新增经过正式裁决的字段
- 升级动作：
  - 新建 `n02_p0_fields_runtime_v2.csv`
  - 新建对应 `header / notes / gaps / append_protocol`
  - 保留 `v1` 不覆盖

## 当前结论

- 这份协议落地后，`REOPEN_B9_N02_SESSION_OR_P0` 已不仅有运行时空壳，还具备了“如何从占位过渡到真实追加”的最小执行约束。
- 当前再向前一步后，已经具备：
  - 参数模板
  - 追加脚本 stub
  - 从 proof 正式 append 到 runtime csv 的脚本
  - dry-run 可复现验证
  - persist 到 runtime csv 的正式证据
  - 因此可以进入“脚本接入前置件已齐”的状态
