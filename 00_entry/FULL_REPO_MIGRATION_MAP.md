# Full Repo Migration Map

## 目的

- 这份文件定义 `旧仓库` 到 `仓库根目录` 的总迁移地图。
- 目标不是复制旧仓库，而是把未来真正要继续维护的层级逐步迁入新仓库。

## 总体裁决

- `trading_analysis`
  - 继续保留为历史大仓库
  - 负责旧材料、旧路径、旧证据保留
- `trading_assistant`
  - 负责未来活跃工作
  - 只接收已筛选、已说明、已定责的材料

## 根目录映射

- 旧根目录活跃主文档：
  - `00_主线检索索引.md`
  - `01_阶段一_项目记录_过去与落地.md`
  - `02_阶段二_工作方向_想法库.md`
  - `03_阶段二_当下计划_执行清单.md`
  - `关于日活.md`
  - `PLAYBOOK_滚动模板.md`
  - `ashare_daily_ops.md`
- 新位置：
  - `04_active_main_docs`
- 规则：
  - 只迁仍有活跃维护价值的主文档
  - 不把旧根目录其他杂项直接平移

## `.trae` 映射

- 旧位置：
  - `.trae\`
- 新位置：
  - `21_trae_system_archive`
- 规则：
  - 只迁仍要继续使用的技能、恢复稿、提示材料
  - 不迁一次性残留或无后续用途内容

## 来源库映射

- 旧位置：
  - `10_来源库_SOURCE_LIBRARY\`
- 新位置：
  - `10_source_library_archive`
- 规则：
  - 只按批次迁入高价值、非重复、非乱码材料
  - 默认不整包复制

## 冻结总结层映射

- 旧位置：
  - `11_冻结总结层_FROZEN_SUMMARIES\`
- 新位置：
  - `11_frozen_summaries_archive`
- 规则：
  - 先做去乱码、去重复、保留总结锚点
  - 默认不整包复制

## 工具运行时映射

- 旧位置：
  - `12_工具运行时_TOOLING_RUNTIME\`
- 新位置：
  - `12_tooling_runtime_archive`
  - 或活跃对象对应的 `02_runtime`
- 规则：
  - 活跃对象真正运行中的最小集进入 `02_runtime`
  - 历史运行时材料按批次筛入 `12_tooling_runtime_archive`
  - 不整包复制旧运行时层

## 工具脚本映射

- 旧位置：
  - `tools\`
- 新位置：
  - `20_tools_workspace`
- 规则：
  - 只迁仍要继续维护和复用的工具
  - 历史一次性脚本先留在旧仓库

## 当前优先顺序

1. 旧主文档第二轮清理与 `04_active_main_docs` 镜像承接
2. `20_tools_workspace` 保持 `PY-04 = tk_r6~r8` 手工表家族的新仓维护态；模板级 smoke 已通过，`Batch9` 当前已完成 `IB fresh-run + N02 P0 latest persist + IB_OBJECT_P0 sample/summary fresh-run + IB_OR relation sample/summary fresh-run + conservative first_break relative sample/summary fresh-run + break_bar evidence sample/summary fresh-run + cross outcome split sample/summary fresh-run + post-cross path / OR break only card fresh-run + return_inside / session_close split fresh-run + session_close branch cards fresh-run + next session continuation / pullback stability fresh-run + next session branch cards fresh-run + multi-session persistence / stability fresh-run + multi-session branch cards fresh-run + third same-session persistence / stability fresh-run + third same-session branch cards fresh-run + third same-session terminal summary fresh-run + other timeframe validation(EURUSD M5 fall DST) fresh-run + wider history validation(EURUSD M5 from main M1) fresh-run + other symbol validation(XAUUSD M1 tail) fresh-run + other symbol + other timeframe validation(XAUUSD M5 jobs) fresh-run + second FX symbol input gate(GBPUSD H1) fresh-run + second FX sub-hour input gate fresh-run + second FX sub-hour input acquisition fresh-run + second FX sub-hour input cache recovery ready fresh-run`，下一步固定 `TradeMaxGlobal-Demo__60088394: terminal export -> n02_mt5_export_ingest_v1`，若失败再退 `hcc reader`，仍不进 `failed breakout`
3. `10_source_library_archive` 继续按“先吃透、再迁入”的批次方式推进
4. `12_tooling_runtime_archive` 与活跃对象 runtime 家族按对象入口分批迁入
5. `21_trae_system_archive` 继续补合适 skill 副本
6. 每一批都同步旧仓库进度板与旧主文档清理任务板
