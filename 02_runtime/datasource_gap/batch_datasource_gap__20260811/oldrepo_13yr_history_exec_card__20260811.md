# 旧仓13年历史数据搬运执行卡 __20260811

> 生成时间: 2026-08-11 02:35:45
> 范围: 仅旧仓 `D:\Stock\trading_assistant\` 内 3 大历史类目录
> 输出: `oldrepo_13yr_history_reusability__20260811.tsv` (明细表) + 本执行卡

---

## 0. 目录识别结果

| 编号 | 逻辑标签 | 实际目录 | 总文件 | 大小MB |
|------|----------|----------|--------|--------|
| 1 | longhubang_history | `D:\Stock\trading_assistant\10_source_library_archive\_raw_snapshot_batch09\10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库` | 144 | 1.49 |
| 2 | forex_history | `D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\孙悟空金牌` | 15 | 1.63 |
| 3 | index_history | `D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\格兰投研` | 11 | 2.45 |

---

## 1. 分类搬运裁决（绿=直接搬 / 黄=先抽样质检 / 红=不建议搬）

| 类别 | 裁决 | 评分/6 | 覆盖 | Schema一致 | 空壳率 | 新仓目标目录 | 判定理由 |
|------|------|--------|------|------------|--------|--------------|----------|
| longhubang_history | 🔴 不建议搬 | 2/6 | 0.0% | 33.33% | 0.69% | `暂不搬` | 覆盖率0.0%过低；Schema一致性33.33%低；空壳率0.69%≤5% |
| forex_history | 🟢 直接搬 | 5/6 | 100.0% | 66.67% | 0.0% | `d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\forex_daily_snapshots` | 覆盖率100.0%≥70%；Schema一致性66.67%中等；空壳率0.0%≤5% |
| index_history | 🟢 直接搬 | 5/6 | 75.0% | 72.73% | 0.0% | `d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\index_daily_snapshots` | 覆盖率75.0%≥70%；Schema一致性72.73%中等；空壳率0.0%≤5% |

---

## 2. 抽样质检清单（仅🟡项需要）

| 类别 | 质检动作 | 样本量 | 通过阈值 | 预计时间 |
|------|----------|--------|----------|----------|
| longhubang_history | 🔴 暂不质检 | - | - | - |
| forex_history | 免质检，直接进入搬运流程 | - | - | - |
| index_history | 免质检，直接进入搬运流程 | - | - | - |

---

## 3. 预估搬运时间 & 命令

### 3.1 预估时间表

| 类别 | 大小MB | 文件数 | 预计拷贝时间 | 校验时间 | 合计 |
|------|--------|--------|--------------|----------|------|
| longhubang_history | 1.49 | 144 | 0s | 0s | 0s |
| forex_history | 1.63 | 15 | 5s | 10s | 15s |
| index_history | 2.45 | 11 | 5s | 10s | 15s |
| **合计(搬绿+黄)** | **5.57** | **170** | **10s** | **20s** | **30s** |

### 3.2 搬运命令（Windows PowerShell / Robocopy）

```powershell
# ============ 旧仓→新仓 历史数据搬运脚本 ============
# 仅执行 🟢直接搬 项目；🟡需先执行 2. 质检通过后再解注释执行

$ErrorActionPreference = 'Continue'

# #1 longhubang_history  🔴 暂不搬

# #2 forex_history  🟢直接搬
robocopy 'D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\孙悟空金牌' 'd:\Stock\dealer_assistant\02_runtime\quicktiny_capture\forex_daily_snapshots' *.json *.tsv /E /COPY:DAT /R:2 /W:1 /LOG+:'D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_datasource_gap__20260811\robocopy_forex_history.log' /NP /NFL

# #3 index_history  🟢直接搬
robocopy 'D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\格兰投研' 'd:\Stock\dealer_assistant\02_runtime\quicktiny_capture\index_daily_snapshots' *.json *.tsv /E /COPY:DAT /R:2 /W:1 /LOG+:'D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_datasource_gap__20260811\robocopy_index_history.log' /NP /NFL

# ============ 搬运后完整性校验 ============
# 对每个目标目录数文件数 vs 源目录，差异>1%需重跑
Write-Host '搬运完成，请人工对照 reusability TSV 校验文件数与大小'
```

### 3.3 命令说明

- **Robocopy 参数**: `/E` 递归含空子目录；`/COPY:DAT` 保留数据+属性+时间戳；`/R:2 /W:1` 失败重试2次每次等1秒；`/LOG+` 追加日志；`/NP /NFL` 减少刷屏
- **拷贝速度假设**: 本地SSD→SSD按 ~200MB/s 估算，小文件额外开销 50ms/文件
- **校验规则**: 绿项随机抽 5% 验 md5；黄项100%验首字段存在性

---

## 4. 风险与回退

1. **Schema漂移**: 若搬运后发现字段不一致，以 `主Schema字段(前15)` 为基准做 diff，生成 `schema_drift_report__YYYYMMDD.tsv`
2. **空壳文件**: 空壳率>5% 的日期段，回退到旧仓重取或直接丢弃该段
3. **大小不一致**: robocopy 后若目标总大小比源少 > 0.5%，用 `/PURGE` 重跑一次目标目录

---

## 5. 附录：各目录抽样文件清单

### longhubang_history (D:\Stock\trading_assistant\10_source_library_archive\_raw_snapshot_batch09\10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库)

```
  D:\Stock\trading_assistant\10_source_library_archive\_raw_snapshot_batch09\10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\S_BUCKET_batch1_round2_focus_manifest_v1.tsv
  D:\Stock\trading_assistant\10_source_library_archive\_raw_snapshot_batch09\10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\S_BUCKET_batch1_round3_function_core_manifest_v1.tsv
  D:\Stock\trading_assistant\10_source_library_archive\_raw_snapshot_batch09\10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\S_BUCKET_INDEX__2026-06-17.tsv
  D:\Stock\trading_assistant\10_source_library_archive\_raw_snapshot_batch09\10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\S_BUCKET_report_representatives_v1.tsv
  D:\Stock\trading_assistant\10_source_library_archive\_raw_snapshot_batch09\10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\S_BUCKET_report_representatives_v10.tsv
  D:\Stock\trading_assistant\10_source_library_archive\_raw_snapshot_batch09\10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\S_BUCKET_report_representatives_v11.tsv
  D:\Stock\trading_assistant\10_source_library_archive\_raw_snapshot_batch09\10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\S_BUCKET_report_representatives_v12.tsv
  D:\Stock\trading_assistant\10_source_library_archive\_raw_snapshot_batch09\10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\S_BUCKET_report_representatives_v13.tsv
  D:\Stock\trading_assistant\10_source_library_archive\_raw_snapshot_batch09\10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\S_BUCKET_report_representatives_v14.tsv
  D:\Stock\trading_assistant\10_source_library_archive\_raw_snapshot_batch09\10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\S_BUCKET_report_representatives_v15.tsv
```

### forex_history (D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\孙悟空金牌)

```
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\孙悟空金牌\info_live_export__20260804_185613.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\孙悟空金牌\info_live_export__20260805_085727.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\孙悟空金牌\info_live_export__20260805_120043.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\孙悟空金牌\info_live_export__20260805_120510.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\孙悟空金牌\info_live_export__20260805_120745.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\孙悟空金牌\info_live_export__20260805_121108.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\孙悟空金牌\info_live_export__20260805_143406.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\孙悟空金牌\info_live_export__20260805_180422.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\孙悟空金牌\info_live_export__20260805_181145.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\孙悟空金牌\info_live_export__20260806_181754.json
```

### index_history (D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\格兰投研)

```
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\格兰投研\info_live_export__20260803_163508.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\格兰投研\info_live_export__20260805_182544.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\格兰投研\info_live_export__20260806_172738.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\格兰投研\info_live_incremental_export__20260803_171950.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\格兰投研\info_live_incremental_export__20260805_182738.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\格兰投研\info_live_incremental_export__20260805_182931.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\格兰投研\info_live_incremental_export__20260805_183901.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\格兰投研\info_live_incremental_export__20260806_173019.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\格兰投研\info_live_incremental_export__20260806_173325.json
  D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms\格兰投研\info_live_incremental_export__20260806_173837.json
```
