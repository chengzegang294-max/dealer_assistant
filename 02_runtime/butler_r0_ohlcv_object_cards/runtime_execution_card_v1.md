# Runtime Execution Card v1

## 生成入口

- `GENERATOR`:
  - `02_runtime/butler_r0_ohlcv_object_cards/run_object_card_minimal_v1.py`
  - `02_runtime/butler_r0_ohlcv_object_cards/run_vp_minimal_v1.py`
  - `02_runtime/butler_r0_ohlcv_object_cards/run_tkr7_minimal_v1.py`
  - `02_runtime/butler_r0_ohlcv_object_cards/run_voltarget_minimal_v1.py`
  - `02_runtime/butler_r0_ohlcv_object_cards/run_period_queen_proxy_minimal_v1.py`
  - `02_runtime/butler_r0_ohlcv_object_cards/run_registry_v0_minimal.py`
- `INDEX_NOTE`: 当前文件 + `acceptance_samples/sample_provenance_index_v1.tsv`

## 当前范围

- 当前已支持：
  - `VOLFAC_P0_A`
  - `BPB_P0_E`
  - `VP_P0_E`
  - `TKR7_P0_E`
  - `VOLTARGET_P0_R`
  - `PERIOD_QUEEN_P0_F`（单标的代理模式）
  - `registry_v0_minimal`
- 输入：单标的 `1d` OHLCV CSV；`registry_v0` 可附带单独 `market_proxy_csv`
- 输出：单卡 JSON 或最小聚合 JSON

## 当前作用

- 用最小 runner 把真实样本 CSV 跑通，验证字段合同不是空文档。
- 用 `registry_v0_minimal` 把已可跑卡串起来，验证 `permission / size / vote` 的统一聚合入口。
- 不替代未来正式 pipeline；只是从“样本驱动”进入“主数据源驱动”的桥接层。

## 证据强度

- 样本 CSV：`historical_recovered`
- runner 输出 JSON：`hard`（当前终端重新生成）
