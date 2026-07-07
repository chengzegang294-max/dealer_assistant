# n02_p0_runtime_append_protocol v2

## 目的

- 规定向 `n02_p0_fields_runtime_v2.csv` 追加 v2 真实数据时的最小流程。

## v2 表头约束

- v2 在 v1 基础上新增：
  - `first_break_mode`
- v2 不允许新增其他字段；若需新增，必须开 v3。

## 追加前检查

1. 检查表头是否与 `n02_p0_fields_runtime_header_v2.txt` 一致
2. 确认 `first_break_mode` 枚举只在：
   - `close / wick / none / ambiguous`
3. 继续遵守 v1 的 session binding 与 DST 推导要求

