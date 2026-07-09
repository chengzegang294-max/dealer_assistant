# N02 P0 运行说明 v1

## 角色

- 这份文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `REOPEN_B9_N02_SESSION_OR_P0` 真实运行产物的当前运行口径。

## 当前状态

- 当前目录已创建。
- 当前主 CSV 已不再只是示例行。
- 已通过：
  - `real_input_samples\n02_proof_of_mapping_output_v1.csv`
  - `n02_p0_runtime_append_from_proof_v1.py`
  把第一批真实 proof 行正式 append 到：
  - `n02_p0_fields_runtime_v1.csv`
- 当前 runtime csv 中为：
  - 真实 `EURUSD M1`
  - `london + new_york` session OR proof 行
- 当前仍不应把本目录内容描述为“已跑完”或“已有策略结论”。

## 当前固定表头

- `symbol`
- `timeframe`
- `bar_time`
- `session_id`
- `session_timezone`
- `opening_range_window_minutes`
- `opening_range_high`
- `opening_range_low`
- `opening_range_mid`
- `opening_range_width`
- `opening_range_width_pct_open`
- `session_open_price`
- `opening_range_defined`
- `first_break_direction`
- `width_error_day`

## 当前固定边界

- 只覆盖 `N02 P0` 的 `12` 个字段。
- 当前不含：
  - `IB`
  - `acceptance`
  - `ib_failed_breakout_event`
  - `or_break_high`
  - `or_break_low`
  - `target_trigger_source`

## 运行时默认口径

- `session_id`：待未来脚本接入时显式传入或配置。
- `session_timezone`：待未来脚本接入时显式传入或配置。
- `opening_range_window_minutes`：待未来脚本接入时显式传入或配置。
- `first_break_direction`：当前枚举只允许 `up / down / none`。
- `width_error_day`：当前仍只保留 `0/1` 结果位。

## 参数来源收严版

- 当前 `n02_p0_runtime_params_template_v1.json` 已新增：
  - `parameter_source_contract`
  - `parameter_source_detail`
- 当前按四类来源层级记录参数：
  - `source_excerpt_or_open_source`
  - `project_contract_default`
  - `stub_only_default`
  - `pending_real_binding`
- `session_id`
  - 当前值：`london`
  - 当前层级：`project_contract_default`
  - 含义：Batch9 v1 已把 `london` 冻结为当前 runtime skeleton 的默认 session binding
- `session_timezone`
  - 当前值：`Europe/London`
  - 当前层级：`project_contract_default`
  - 含义：已与 `london -> Europe/London` 的 v1 binding registry 一起冻结，但真实接入时仍需核验 DST
- `opening_range_window_minutes`
  - 当前值：`30`
  - 当前层级：`project_contract_default`
  - 含义：这是当前 Batch9 v1 运行时骨架冻结的默认窗口，不等于所有市场都只能用 30
- `session_binding_registry`
  - 当前已冻结：
    - `london -> Europe/London`
    - `new_york -> America/New_York`
  - 含义：当前 v1 已不只是单条 session 默认值，而是有了最小可复用的 session 绑定表
  - 当前还补充了两类边界：
    - `calendar_basis`
    - `dst_handling`
  - 当前要求：
    - `london` 必须按 `Europe/London` 本地日期解释 session 日历
    - `new_york` 必须按 `America/New_York` 本地日期解释 session 日历
    - DST 必须由时区规则推导，不能手写固定 UTC 偏移
- 当前约束：
  - 只有写清 `source_tier + source_basis + evidence_anchor + upgrade_rule` 的参数，才允许进入更严格的运行口径说明
  - 已升级为 `project_contract_default` 的 session 绑定，可以写成“Batch9 v1 冻结口径”

## 当前脚本接入前置件

- 已新增：
  - `n02_p0_runtime_params_template_v1.json`
  - `n02_p0_runtime_append_stub_v1.py`
  - `n02_p0_runtime_append_from_proof_v1.py`
  - `n02_p0_runtime_session_calendar_dst_checklist_v1.md`
  - `n02_p0_real_input_mapping_draft_v1.md`
  - `real_input_samples\`
- 作用：
  - 前者固定最小参数口径
  - 后者提供删除占位行并追加第一批真实行的脚本骨架
  - checklist 提供 session calendar / DST 接入前验收清单
  - mapping draft 说明真实 bar 输入如何映射到当前 N02 P0 字段
  - real_input_samples 提供第一份可跑通 bars 输入样本
- 当前仍不代表：
  - 已接入主项目执行链路
  - 已进入策略 gate / 自动执行链路

## 当前真实 append 证据

- 当前 proof 输入：
  - `real_input_samples\n02_proof_of_mapping_output_v1.csv`
- 当前 append 脚本：
  - `n02_p0_runtime_append_from_proof_v1.py`
- 当前 append 后主 CSV：
  - `n02_p0_fields_runtime_v1.csv`
- 当前结果摘要：
  - `proof_rows = 22`
  - `runtime_rows_after_append = 22`
  - 示例行已移除

## 当前可复现 dry-run

- 可复现命令：

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_p0_runtime_append_stub_v1.py
```

- 当前预期：
  - 只打印示例行
  - 不写回 CSV

## 当前可复现 persist 示例行

- 可复现命令：

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_p0_runtime_append_stub_v1.py --persist
```

- 当前预期：
  - 先清理占位行
  - 再清理同一条示例行的旧副本
  - 最后只保留 `1` 条示例行写回 CSV
- 这一步仍然只是脚本骨架验证，不代表真实运行数据已接入。

## 示例行规则

- 当前示例行使用：
  - `symbol = EURUSD`
  - `timeframe = H1`
  - `session_id = london`
- 这行的作用是：
  - 验证列顺序
  - 验证 `na` 写法
  - 验证默认枚举写法
- 当第一份真实运行数据准备写入时：
  - 优先删除或覆盖这条示例数据
  - 不要把示例行和真实行长期混放

## 下一步

- 真正接入脚本或运行链路时：
  - 先处理当前占位行
  - 再往 `n02_p0_fields_runtime_v1.csv` 追加真实数据行
  - 若表头变更，必须新增 `v2`，不覆盖 `v1`
