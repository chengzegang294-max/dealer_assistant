# GIT Submission Split Plan 20260707

## 目标

- 把当前工作区拆成两条主提交线：
  - `A`：`02_runtime/mt_indicator_probes/batch_01_volty_xbreaking`
  - `B`：`batch_100 ~ batch_109` 内部资料重分类整理线
- 避免把“运行时大产物”和“来源库重分类整理”混成一个超大提交。
- 保持每个提交都能独立说明：
  - 为什么要交
  - 包含什么
  - 不包含什么

## 批次 A

### 主题

- `batch_01_volty_xbreaking` 的运行时入口、生成脚本、验收说明、环境快照与产物证据归口。

### 当前工作树形态

- 已跟踪修改：
  - `BATCH_01_ARTIFACT_INDEX_TEMPLATE.md`
  - `BATCH_01_EXECUTION_CARD.md`
  - `BATCH_01_PROVENANCE_NOTEBOARD.md`
  - `MT4_MT5_FIRST_RUN_PLAYBOOK.md`
  - `README.md`
  - `probe_artifact_ingest_v1.py`
- 新增真实资产：
  - `BATCH_01_ACCEPTANCE_CHECK.md`
  - `MT4Probe_Volty_dumpseries_0_6.ini`
  - `PURCHASED_MARKET_DATA_INVENTORY.md`
  - `acceptance_snapshots/`
  - `artifacts/`
  - `environment_snapshots/`
  - `fill_mt4_eurusd_h1_history_v1.py`
  - `mt4probe_volty_dumpseries_portable.ini`
  - `normalize_purchased_csv_contract_v1.py`
  - `probe_batch_acceptance_v1.py`
  - `probe_mt_environment_inventory.ps1`
  - `purchased_csv_contract_preview_acceptance_v1.py`
  - `purchased_csv_contract_preview_index_v1.py`
  - `run_mt5_bar_export_once.ps1`
  - `run_mt5_symbol_dump_once.ps1`
  - `run_volty_dumpseries_gui_once.ps1`
  - `run_xbreaking_probe_once.ps1`
  - `run_xbreaking_validation_matrix.ps1`
  - `tools/`
- 已明确忽略：
  - `02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/_tmp_*.ini`
  - `02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/artifacts/**/runtime_config/_tmp_*.ini`

### 体量判断

- `artifacts/`：`831` files，约 `472,988,412` bytes
- `acceptance_snapshots/`：`2` files，约 `2,286,865` bytes
- `environment_snapshots/`：`17` files，约 `75,215` bytes
- `tools/`：`2` files，约 `15,390` bytes

### 推荐拆法

- `A1`：先交“入口与生成器”
  - `README.md`
  - `BATCH_01_*`
  - `MT4_MT5_FIRST_RUN_PLAYBOOK.md`
  - `PURCHASED_MARKET_DATA_INVENTORY.md`
  - 所有 `.py / .ps1 / tools/`
  - 仅显式加入 root 级 `.ini`
- `A2`：再交“运行时证据与环境快照”
  - `acceptance_snapshots/`
  - `environment_snapshots/`
  - `artifacts/`
  - 但显式排除 `artifacts/**/runtime_config/_tmp_*.ini`

### 推荐提交信息

- `A1`
  - `feat(runtime): freeze batch_01 volty/xbreaking generators and provenance`
- `A2`
  - `feat(runtime): archive batch_01 volty/xbreaking artifacts and environment evidence`

### A1 Staging Rule

- 不使用：
  - `git add 02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/*.ini`
- 原因：
  - 在当前仓库里，该 pathspec 会把 artifact 子树里的 nested `_tmp runtime ini` 一并卷入 index
- 改用显式文件：
  - `MT4Probe_Volty_dumpseries_0_6.ini`
  - `mt4probe_volty_dumpseries_portable.ini`

## 批次 B

### 主题

- `00_外部公开资料与方法论参考` 的内部资料重分类整理与长期维护包落盘。

### 必须一起提交的原因

- `batch_107 / batch_108 / batch_109` 的 `manifest/report` 都回指 `_raw_snapshot_batch09/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考`
- 如果只交 bundle，不交 raw source 子树，provenance 会断。

### 当前纳入范围

- 状态与对齐台账：
  - `00_entry/LEGACY_ALIGNMENT_STATUS__20260707.md`
  - `10_source_library_archive/batch_09_legacy_source_library_alignment__20260707/README.md`
- 边界卡：
  - `10_source_library_archive/batch_100_non_kimi_public_methods_boundary__20260707/README.md`
- 长期维护包：
  - `10_source_library_archive/batch_107_non_kimi_public_batch9_bundle__20260707/`
  - `10_source_library_archive/batch_108_non_kimi_nftradez_method_bundle__20260707/`
  - `10_source_library_archive/batch_109_non_kimi_smile_smc_method_bundle__20260707/`
- raw source 子树：
  - `10_source_library_archive/_raw_snapshot_batch09/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/`

### 已确认裁决

- `Smile_SMC` 已形成第一轮 `method_reference_bundle`
- `Smile_SMC/raw_materials/video_screenshots/` 保留 raw 侧，不单独切第二个证据包
- `00_外部公开资料与方法论参考` 活跃区内旧 `file:///d:/Stock/trading_analysis/...` 绝对链接已回指当前 repo raw snapshot

### 体量判断

- `batch_107_non_kimi_public_batch9_bundle__20260707/`：`12` files，约 `55,114` bytes
- `batch_108_non_kimi_nftradez_method_bundle__20260707/`：`11` files，约 `43,954` bytes
- `batch_109_non_kimi_smile_smc_method_bundle__20260707/`：`9` files，约 `998,807` bytes
- `00_外部公开资料与方法论参考/` raw 子树：`175` files，约 `32,364,734` bytes

### 推荐提交信息

- `B`
  - `feat(source-library): promote public methods boundary and bundles through batch_109`

## 提交前清单

- 确认 `.gitignore` 已包含：
  - `.vscode/settings.json`
  - `.trae/`
  - `debug-*.md`
  - `trae-debug-log-*.ndjson`
  - `02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/_tmp_*.ini`
  - `02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/artifacts/**/runtime_config/_tmp_*.ini`
- 确认 `A` 与 `B` 不交叉 stage
- 确认 `B` 提交时包含 raw 子树，否则 bundle 的 source path 会悬空
- 确认 `A2` 体量较大，必要时单独作为第二个提交
- 提交前再次执行：
  - `git status --short`
  - `git diff --stat --cached`
  - `git diff --cached --name-only -- "02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/artifacts/**/runtime_config/_tmp_*.ini"`

## 推荐执行顺序

1. 先提 `A1`
2. 再提 `A2`
3. 最后提 `B`

## A1 Safe Commands

```bash
git add .gitignore
git add 00_entry/GIT_SUBMISSION_SPLIT_PLAN__20260707.md
git add 02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/README.md
git add 02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/BATCH_01_*
git add 02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/MT4_MT5_FIRST_RUN_PLAYBOOK.md
git add 02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/PURCHASED_MARKET_DATA_INVENTORY.md
git add 02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/*.py
git add 02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/*.ps1
git add 02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/MT4Probe_Volty_dumpseries_0_6.ini
git add 02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/mt4probe_volty_dumpseries_portable.ini
git add 02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/tools
git diff --cached --name-only -- "02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/artifacts/**/runtime_config/_tmp_*.ini"
git commit -m "feat(runtime): freeze batch_01 volty/xbreaking generators and provenance"
```

## A2 Safe Commands

```bash
git add 02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/acceptance_snapshots
git add 02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/environment_snapshots
git add 02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/artifacts
git restore --staged "02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/artifacts/**/runtime_config/_tmp_*.ini"
git diff --cached --name-only -- "02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/artifacts/**/runtime_config/_tmp_*.ini"
git commit -m "feat(runtime): archive batch_01 volty/xbreaking artifacts and environment evidence"
```

## B Safe Commands

```bash
git add 00_entry/LEGACY_ALIGNMENT_STATUS__20260707.md
git add 10_source_library_archive/batch_09_legacy_source_library_alignment__20260707/README.md
git add 10_source_library_archive/batch_100_non_kimi_public_methods_boundary__20260707
git add 10_source_library_archive/batch_107_non_kimi_public_batch9_bundle__20260707
git add 10_source_library_archive/batch_108_non_kimi_nftradez_method_bundle__20260707
git add 10_source_library_archive/batch_109_non_kimi_smile_smc_method_bundle__20260707
git add "10_source_library_archive/_raw_snapshot_batch09/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考"
git commit -m "feat(source-library): promote public methods boundary and bundles through batch_109"
```

## Current Staging Checkpoint

- `A1`
  - 当前 cached file count：`0`
  - 当前工作树：`README.md` modified
  - 说明：当前不是“大量 A1 文件待提交”，而是只剩 `README.md` 还在工作树，需要按 `A1 Safe Commands` 重建独立 stage
- `A2`
  - 当前 cached file count：`0`
  - 说明：尚未进入 index，可在 `A1` 提交后单独推进
- `B`
  - 当前 cached file count：`210`
  - 当前分布：
    - `status=1`
    - `alignment=1`
    - `boundary=1`
    - `batch107=12`
    - `batch108=11`
    - `batch109=9`
    - `raw=175`
  - 说明：这条线已经实际进入 index，优先保持边界稳定，不要让 `A1/A2` 混入

## B Minimal Acceptance

- 已包含 repo 级状态卡：
  - `00_entry/LEGACY_ALIGNMENT_STATUS__20260707.md`
- 已包含来源库对齐入口：
  - `10_source_library_archive/batch_09_legacy_source_library_alignment__20260707/README.md`
- 已包含公开资料方法论边界卡：
  - `10_source_library_archive/batch_100_non_kimi_public_methods_boundary__20260707/README.md`
- 已包含三个长期维护包：
  - `batch_107`
  - `batch_108`
  - `batch_109`
- 已包含 provenance 所需 raw 子树：
  - `00_外部公开资料与方法论参考`
- 当前最小验收结论：
  - `B` 作为独立提交已经成形，且 bundle 与 raw source 没有断链

## 当前结论

- 当前不是“能不能提交”的问题，而是“按哪种粒度提交更稳”。
- 最稳方案不是 `A + B` 两个提交，而是：
  - `A1` 入口与生成器
  - `A2` 证据与环境快照
  - `B` 内部资料重分类整理线
