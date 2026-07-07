# MT4/MT5 安装与数据目录定位 v1

## 你刚才的报错是什么

- `FileNotFoundError: D:\export\eurusd_m1.csv`
- 这不是 MT4/MT5 安装问题，而是：你在命令里写的 `--input` 路径下没有这个文件。
- 解决方式是：
  - 让 MT4/MT5 真的把 CSV 导出到那个路径；或者
  - 把 `--input` 改成你实际导出的文件路径

## 最推荐的做法：把导出文件放到仓库的固定投递区

- 投递区：
  - `.\data\mt_exports_drop\`（从仓库根目录执行时）
- 好处：
  - 路径稳定
  - 脚本 README 可以直接复制粘贴跑

## MT4/MT5 的两个“路径”概念

- 安装目录（terminal.exe 在哪里）
- 数据目录（账号/历史/脚本/Files 等在哪里）

大多数情况下，你真正需要的是“数据目录”，因为：
- 你从终端或脚本输出的文件，常落在数据目录下的 `MQL4\Files` / `MQL5\Files`

## 如何在 MT4/MT5 里直接定位（最可靠）

- 在终端菜单里：
  - `File -> Open Data Folder`
- 打开后你会看到：
  - `MQL4\Files` 或 `MQL5\Files`

## 如何导出“历史 bars CSV”（用于本仓库 N01/N02 proof-of-mapping）

目标是得到一个包含 `Date/Time/Open/High/Low/Close` 的 CSV 文件，并且你知道它保存到了哪里。

### 最关键的一步：保存对话框里把路径“粘贴到地址栏”

- 在导出弹出的 “保存为” 对话框中：
  - 直接把下面这个路径粘贴到对话框的地址栏（上方那条路径栏）并回车：
    - `.\data\mt_exports_drop`
  - 然后再输入文件名保存（例如：`eurusd_m1_export.csv` / `eurusd_h1_export.csv`）
- 保存成功后，立刻回到 PowerShell 验收：

```powershell
Get-ChildItem -LiteralPath ".\data\mt_exports_drop" -File | Select-Object Name,Length,LastWriteTime
```

### MT5（常见路径）

- 打开 `History Center`（通常 `F2`）
- 选择品种（例如 `EURUSD`）与周期（例如 `M1` 或 `H1`）
- 先确认历史已下载（没有数据就先下载/加载）
- 选择 `Export`，保存为 CSV
- 保存位置推荐直接选：
  - `.\data\mt_exports_drop\`

### MT4（常见路径）

- 打开 `History Center`（通常 `F2`）
- 选择品种与周期
- 确认历史已下载
- `Export` 保存为 CSV
- 保存位置同样推荐：
  - `.\data\mt_exports_drop\`

### 导出后的最小验收

- 在 PowerShell 里确认文件真的存在且不是 0 字节：

```powershell
Get-ChildItem -LiteralPath ".\data\mt_exports_drop" -File | Select-Object Name,Length,LastWriteTime
```

## 常见默认数据目录（Windows）

- 通常在用户目录下（不一定在 D 盘）：
  - `%APPDATA%\MetaQuotes\Terminal\{hash}\MQL4\Files`
  - `%APPDATA%\MetaQuotes\Terminal\{hash}\MQL5\Files`

## 本仓库里已知的 MT4 便携实例

- 仓库内已有一个 MT4 便携探针实例：
  - `12_工具运行时_TOOLING_RUNTIME\03_MT4便携探针实例\terminal.exe`
- 这类便携实例的“安装目录”和“数据目录”可能在同一文件夹附近，但仍以终端菜单的 Data Folder 为准。
