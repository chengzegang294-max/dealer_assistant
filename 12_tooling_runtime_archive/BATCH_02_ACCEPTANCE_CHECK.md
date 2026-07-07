# Tooling Runtime Archive Batch 02 Acceptance Check

## 目的

- 这份文件用于证明 `batch_02_mt_indicator_family` 不是“看起来迁了”，而是做过文件集合与内容级校验。

## 校验范围

- 旧来源：
  - `旧仓库\12_工具运行时_TOOLING_RUNTIME\02_MT指标家族_源码与探针\`
- 新位置：
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\`

## 校验方法

- 文件集合对账：
  - 逐文件名对比旧目录与新目录
- 内容完整性：
  - 对 `mq4 / mq5 / ex4 / ex5 / ini` 逐文件计算 `sha256`
- 差异判定：
  - 若哈希不同，必须能解释为“主动改造”而不是“未知漂移”

## 校验结果

- `old_file_count`: `20`
- `new_file_count_excluding_readme`: `20`
- `missing_in_new`: `0`
- `same_hash_count`: `18`
- `different_hash_count`: `2`
- `different_files`:
  - `MT4Probe_XBreaking.ini`
  - `XBreakingProbe.ini`

## 差异解释

- `MT4Probe_XBreaking.ini`
  - 旧哈希：`6d4011fd4e0c8cff7854263987f843df4aa8f1672581c50f0790cc357d9f374d`
  - 新哈希：`9f10c4073f17400d107ecd9d2ce9b32841612d6d6dd3f61d959db187e62b9ae6`
  - 差异原因：主动把 `TestExpert` 与 `TestReport` 从旧仓绝对路径改成终端内相对路径口径
- `XBreakingProbe.ini`
  - 旧哈希：`bb32dc91d971aa7051bf52675e8d0059cf7ef94f9fb17e8f40c8d3ad835eca85`
  - 新哈希：`e6e18f8c5cdd2d75c4a5fc64f9c1ab853f8db03db47eed0534b921819656f0ab`
  - 差异原因：主动把 `Report=` 从旧仓 `backtest_out` 改成终端内相对路径

## 关键抽样

- `交易盈亏统计.ex4`
  - 旧哈希：`c197e32de631f88823b83cf78caa5009dc7faf41420e393b3ffd54e31c832118`
  - 新哈希：`c197e32de631f88823b83cf78caa5009dc7faf41420e393b3ffd54e31c832118`
  - 结论：`same`

## 当前裁决

- 本批已达到：
  - `file_set_aligned_with_old_source`
  - `content_verified_except_intentional_ini_rewrites`
- 这意味着本批进入新仓不是“未验先收”，而是：
  - 18 个文件原样一致
  - 2 个配置文件有明确、受控、可解释的工程化改造
