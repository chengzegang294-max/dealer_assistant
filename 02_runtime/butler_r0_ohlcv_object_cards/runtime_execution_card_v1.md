# Runtime Execution Card v1

## 生成入口

- `GENERATOR`: `02_runtime/butler_r0_ohlcv_object_cards/run_object_card_minimal_v1.py`
- `INDEX_NOTE`: 当前文件 + `acceptance_samples/sample_provenance_index_v1.tsv`

## 当前范围

- 当前只支持：
  - `VOLFAC_P0_A`
  - `BPB_P0_E`
- 输入：单标的 `1d` OHLCV CSV
- 输出：单次运行 JSON

## 当前作用

- 用最小 runner 把真实样本 CSV 跑通，验证字段合同不是空文档。
- 不替代未来正式 pipeline；只是从“样本驱动”进入“主数据源驱动”的桥接层。

## 证据强度

- 样本 CSV：`historical_recovered`
- runner 输出 JSON：`hard`（当前终端重新生成）
