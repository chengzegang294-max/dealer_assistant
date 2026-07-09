# Registry V0 Formal Entry Card

## 用途

- 把 `registry_v0` 从 runtime 内部可跑入口，上提为仓库级正式聚合入口卡。
- 当前只声明“从哪里进入、看哪些合同、看哪些验收证据”，不替代 runtime 层脚本与执行卡。

## 正式入口

- 运行层索引：
  - `02_runtime/butler_r0_ohlcv_object_cards/runtime_execution_card_v1.md`
- 主 runner：
  - `02_runtime/butler_r0_ohlcv_object_cards/run_registry_v0_minimal.py`
- 单样本强验收：
  - `02_runtime/butler_r0_ohlcv_object_cards/run_registry_v0_acceptance_v1.py`
- 批量验收：
  - `02_runtime/butler_r0_ohlcv_object_cards/run_registry_v0_batch_acceptance_v1.py`

## 权威合同

- 输入合同：
  - `02_runtime/butler_r0_ohlcv_object_cards/registry_vote_input_contract_v1.tsv`
- 输出合同：
  - `02_runtime/butler_r0_ohlcv_object_cards/registry_output_contract_v1.tsv`
- 样本计划：
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/registry_v0_sample_plan_v1.tsv`

## 当前验收锚点

- 批量 JSON 摘要：
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_outputs/registry_v0_batch_acceptance_summary.json`
- 批量 TSV 摘要：
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_outputs/registry_v0_batch_acceptance_summary.tsv`
- 当前已覆盖：
  - `NO_TRADE/BLOCKED`
  - `BUY/ALLOW`
  - `SELL/EXIT`
- 当前状态：
  - `minimal_registry_ready + multi_registry_ready = 6/6 pass`

## 角色边界

- `00_entry`：
  - 负责声明仓库级正式入口与权威导航。
- `02_runtime/butler_r0_ohlcv_object_cards/`：
  - 负责具体 runner、执行卡、样本计划与验收产物。
- 当前 `registry_v0` 仍是 `runtime bridge entry`，尚未升级为最终生产 pipeline 名称或目录。
