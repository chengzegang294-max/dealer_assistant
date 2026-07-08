# Butler R0 OHLCV Object Cards Runtime

更新时间：2026-07-08

## 用途

- 为 `VOLFAC / BPB / VP / TKR7` 这 4 张纯 OHLCV 对象卡准备统一的最小可跑入口。
- 这里只放运行协议、参数模板、验收样本入口；不放来源文档。

## 当前范围

- 当前只覆盖 A 股日线 OHLCV 样本。
- 未来再扩到周线合成、分钟级与跨市场。

## 上游合同

- `01_active_objects/butler_r0_object_cards_p0/*_field_contract_v1.tsv`
- `01_active_objects/butler_r0_object_cards_p0/object_cards_p0_acceptance_matrix_v1.tsv`

## 当前生成入口与产物

- `GENERATOR`:
  - `run_object_card_minimal_v1.py`
- `ARTIFACT`:
  - `acceptance_outputs/*.json`
- `INDEX_NOTE`:
  - `runtime_execution_card_v1.md`
  - `acceptance_outputs/artifact_index_v1.tsv`
