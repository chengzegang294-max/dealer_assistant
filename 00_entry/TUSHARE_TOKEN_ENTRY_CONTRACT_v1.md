# Tushare Token Entry Contract v1

更新时间：2026-07-08

## 目标

- 把 `Tushare Pro` 作为 `P1_primary_default` 主数据源时，token 与配置入口写死。
- 禁止把 token 写进仓库、脚本常量或 JSON 样例文件。

## 首选入口

- 首选：环境变量 `TUSHARE_TOKEN`
- 备选：用户主目录令牌文件（仅本机，不入仓）：
  - `~/.tushare/token`

## 禁止事项

- 不允许把真实 token 提交到：
  - `config/*.json`
  - `.vscode/settings.json`
  - `02_runtime/`
  - `10_source_library_archive/`
- 不允许在示例文件中放伪装成真实值的“看起来像 token”的字符串。

## 启用条件

1. 本机已安装 `tushare`
2. `TUSHARE_TOKEN` 可读取，或 `~/.tushare/token` 存在
3. `pro.daily()` 最小探测通过

## 最小探测

```powershell
$env:TUSHARE_TOKEN="PUT_YOUR_TOKEN_HERE"
python -c "import os, tushare as ts; pro=ts.pro_api(os.environ['TUSHARE_TOKEN']); df=pro.daily(ts_code='300302.SZ', start_date='20240101', end_date='20240131'); print(df.head(3).to_string(index=False))"
```

## 降级路径

- `TUSHARE_TOKEN` 缺失或调用失败：
  - 降级到 `AkShare`
- `AkShare` 也不可用：
  - 降级到 `Baostock`
- 只有验收样本需求：
  - 继续使用 `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/`

## 当前作用

- 本合同只定义 token/配置入口与启用顺序，不等于已经开始 ETL 全市场日线。
