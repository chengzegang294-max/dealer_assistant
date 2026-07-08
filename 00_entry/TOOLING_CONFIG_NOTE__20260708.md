# Root Tooling Config Note

## 为什么要借鉴旧仓库配置

- 旧仓库已经沉淀出一套最小可用的解释器和分析边界配置。
- 新仓库如果完全不接这些配置，IDE 很容易把：
  - `legacy_analysis`
  - `.venv`
  - `backtest_out`
  - `.dc_cache`
  一起卷进分析范围，导致误报、导入噪音和工作区边界混乱。

## 当前决定

- 借鉴并保留：
  - `python.defaultInterpreterPath`
  - `python.analysis.exclude`
  - `venvPath`
  - `venv`
- 不直接照搬：
  - `typeCheckingMode = off`
  - `reportMissingImports = none`
  - `reportMissingModuleSource = none`
  - `reportGeneralTypeIssues = none`

## 原因

- 解释器路径和分析排除项属于“必要配置”。
- 把所有类型检查直接关掉，虽然干净，但会把真实问题一起藏掉。
- 新仓更适合：
  - 保留运行相关错误
  - 只压掉已知噪音

## 当前已落盘

- `pyrightconfig.json`
  - 已补：
    - `pythonVersion = 3.12`
    - `reportImplicitRelativeImport = none`
    - `exclude` 中加入 `.dc_cache / backtest_out / legacy_analysis`
    - `venvPath = .`
- `basedpyrightconfig.json`
  - 已补：
    - `reportDeprecated = none`
- `ruff.toml`
  - 已补：
    - `UP007`
    - `UP045`
- `ROOT_VSCODE_SETTINGS_TEMPLATE.jsonc`
  - 作为可复制到 `.vscode/settings.json` 的模板

## 当前状态

- `ROOT_VSCODE_SETTINGS_TEMPLATE.jsonc` 已改为 repo-first 模板口径：
  - `python.defaultInterpreterPath = ${workspaceFolder}\.venv\Scripts\python.exe`
- 若你本机的 `.vscode/settings.json` 仍写了树外绝对路径（例如 `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.venv\Scripts\python.exe`），建议手动改为模板口径（只做本机覆盖，不要把树外路径当默认入口写进主线文档）
  - `python.terminal.activateEnvironment = true`
  - `python.analysis.exclude` 已排除 `.dc_cache / backtest_out / .venv / __pycache__ / legacy_analysis`
- 当前阶段推荐优先保证 repo-first：默认入口不依赖树外绝对路径；解释器若需复用旧环境，仅作为本机覆盖策略。
- Trae 底部状态栏若仅显示 `('.venv': venv)`，可能同时对应：
  - `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.venv`
  - `d:\Stock\trading_assistant\.venv`
  - `d:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\.venv`
  不能只看简称，必须用完整路径确认。

## 当前裁决

- 默认口径只保证 repo-first：不把树外绝对路径当作当前入口。
- 若你本机确实需要复用旧仓 `.venv`，只在本机侧覆盖（例如手动激活或本机 settings.json），不要把树外路径写进 repo 合同/入口。
- 当前若仍看到零散黄线，优先判为：
  - `basedpyright / pyright / ruff` 的检查器提示
  - 历史缓存未刷新
  - 同名 `.venv` 的显示歧义
- 当前不应再把“解释器选错”当作首要问题。

## 一句话裁决

- 应该借旧仓库的“必要配置”。
- 但不要借旧仓库那种“把类型检查几乎全关掉”的消音方式。
