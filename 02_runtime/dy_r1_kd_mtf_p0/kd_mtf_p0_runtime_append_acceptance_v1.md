# kd_mtf_p0_runtime_append_acceptance_v1

## 目的

- 记录 `trading_assistant` 新运行时层里这次 `proof -> runtime` 的最小验收结论。

## 本次验收对象

- params 模板：
  - `kd_mtf_p0_runtime_params_template_v1.json`
- append stub：
  - `kd_mtf_p0_runtime_append_stub_v1.py`
- proof 输出：
  - `real_input_samples\kd_mtf_p0_proof_output_v1.csv`
- runtime csv：
  - `kd_mtf_p0_fields_runtime_v1.csv`

## 执行命令

```bash
python 02_runtime\dy_r1_kd_mtf_p0\kd_mtf_p0_runtime_append_stub_v1.py
python 02_runtime\dy_r1_kd_mtf_p0\kd_mtf_p0_runtime_append_stub_v1.py --persist
```

## dry-run 结果

- 已成功读取：
  - `proof_output_v1.csv`
- 已成功校验：
  - runtime csv 表头与 `v1` 合同一致
- dry-run 输出：
  - `rows_before_cleanup = 12`
  - `proof_rows_loaded = 7`
  - `rows_before_append = 5`
  - `rows_after_append = 12`
  - `dry_run_only = true`

## persist 结果

- 已成功执行：
  - `--persist`
- 已成功写回：
  - `kd_mtf_p0_fields_runtime_v1.csv`
- 当前 runtime 行数：
  - `12`
- 当前 runtime 组成：
  - 历史 `5` 行手工 persist 样本
  - 最新真实 `7` 行 proof

## 当前可接受结论

- 新运行时层已具备：
  - `params template`
  - `append stub`
  - `proof -> runtime` 的最小 dry-run 验证
  - `proof -> runtime` 的最小 persist 验证

## 当前还不能宣称

- 已接入 broker 原始 bars 到 proof 的完整重建脚本
- 第一份完整 canonical H1 bars 大样本已在本目录正式导入
- 第一条真实 `b` 已补出
