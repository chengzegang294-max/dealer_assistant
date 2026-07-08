# 系统性一致性审查报告

> **审查时间**: 2026-07-07 17:48 CST
> **审查范围**: `E:\downloads\Desktop\找系统\特征`
> **总文档数**: 92

---

## 审查汇总

| 维度 | 状态 | 问题数 | 严重程度 |
|------|------|--------|----------|
| **1. 命名规范** | 失败 | 1 | 高 |
| **2. 状态标记** | 警告 | 3 | 低 |
| **3. 引用完整性** | 通过 | 0 | 无 |
| **4. 对象卡字段** | 失败 | 14 | 高 |
| **5. 版本声明** | 警告 | 5 | 中 |
| **6. 术语一致性** | 警告 | 10 | 中 |
| **7. ABORT编码** | 警告 | 2 | 中 |
| **8. 量化标注** | 警告 | 10 | 低 |

**汇总**: 严重问题 `15` 个 | 警告 `20` 个 | 建议 `7` 个

---

## 1. 命名规范检查

**标准格式**: `{CATEGORY}_{NAME}_{VERSION}.md`

**版本分布**:
- v1.0: 64 份
- v2.0: 6 份
- 其他版本:
  - `EXTERNAL_STRATEGY_RAW_MATERIAL_v3.0.md` -> v3.0
  - `EXTERNAL_STRATEGY_RAW_MATERIAL_v4.0.md` -> v4.0
  - `EXTERNAL_STRATEGY_RAW_MATERIAL_v5.0.md` -> v5.0
  - `EXTERNAL_STRATEGY_RAW_MATERIAL_v6.0.md` -> v6.0
  - `EXTERNAL_STRATEGY_RAW_MATERIAL_v7.0.md` -> v7.0
  - `EXTERNAL_SYSTEM_FUNCTION_MAP_v0.1.md` -> v0.1
  - `MTF_SEB_v0.1.md` -> v0.1

**发现的问题**:

- `INDEX_v2.0.md` -> 不符合标准命名格式

---

## 2. 状态标记一致性

**标准状态标记**（来自 INDEX_v2.0.md 第4节）:
- 冻结 = 核心逻辑已确定，编程必须遵循
- 可编码 = 内容完整，可开始实现
- 审查 = 内容需进一步验证
- 待实现 = 已设计但等待数据/条件成熟
- 废弃 = 不再使用，仅存档

**Emoji 使用统计**:
- : 约 300 次 | : 约 81 次 | : 约 74 次 | : 约 9 次
- : 约 50 次 | : 约 29 次 | : 约 37 次 | : 约 1 次

**发现的扩展/变体标记**:
- `DAILY_REPORT_GENERATOR_v1.0.md` 使用 合规/关注/预警/充足 等扩展标记 -- 这是日报场景的特殊设计，属正常
- `BACKTEST_REPORT_TEMPLATE_v1.0.md` 使用 / 组合标记 -- 模板表格内使用，属正常
- 个别文档出现  和  重复emoji -- 建议改为单个+文字强调

---

## 3. 引用完整性

**通过**: 未发现 dangling reference。

**INDEX_v2.0.md 中引用但未找到的文件** (7 个):

- `OBJECT_CARD_CHZL_FX_P0_S__Chanlun_Fenxing_v1.0.md`
- `OBJECT_CARD_CHZL_BI_P0_S__Chanlun_Bi_v1.0.md`
- `OBJECT_CARD_CHZL_ZS_P0_S__Chanlun_Zhongshu_v1.0.md`
- `OBJECT_CARD_CHZL_TREND_P0_S__Chanlun_Trend_v1.0.md`
- `OBJECT_CARD_TK_R6_P0_E__TK_Forex_Pattern_v1.0.md`
- `OBJECT_CARD_TK_R7_P0_E__TK_Forex_Pattern_v1.0.md`
- `OBJECT_CARD_TK_R8_P0_E__TK_Forex_Pattern_v1.0.md`

---

## 4. 对象卡输出字段一致性

**标准字段**: `object_id`, `signal_type`, `signal_strength`, `confidence`, `lock_status`, `filter_action`, `risk_action`, `size_scalar`

**对象卡总数**: 14

**字段缺失情况**:

| 文件名 | 缺失字段数 | 缺失字段 |
|--------|-----------|----------|
| `GLM_TASK_02_CHANLUN_OBJECT_CARD.md` | 7 | signal_type, signal_strength, confidence, lock_status, filter_action, risk_action, size_scalar |
| `OBJECT_CARD_ATRATIO_P0_A__ActiveTradeRatio_v1.0.md` | 6 | object_id, signal_strength, confidence, lock_status, risk_action, size_scalar |
| `OBJECT_CARD_BACKTEST_SCHEDULE_v1.0.md` | 5 | object_id, signal_strength, lock_status, filter_action, risk_action |
| `OBJECT_CARD_BPB_P0_E__Brooks_Breakout_Pullback_v1.0.md` | 5 | object_id, lock_status, filter_action, risk_action, size_scalar |
| `OBJECT_CARD_CHZL_BSD_P0_E__Chanlun_Buy_Sell_Signals_v1.0.md` | 8 | object_id, signal_type, signal_strength, confidence, lock_status, filter_action, risk_action, size_scalar |
| `OBJECT_CARD_INSTB_P0_A__InstitutionalBehavior_v1.0.md` | 6 | object_id, signal_strength, confidence, lock_status, risk_action, size_scalar |
| `OBJECT_CARD_KELLY_P0_R__KellyCriterion_v1.0.md` | 6 | object_id, signal_type, lock_status, filter_action, risk_action, size_scalar |
| `OBJECT_CARD_MFLOW_P0_A__MoneyFlow_v1.0.md` | 5 | object_id, confidence, lock_status, risk_action, size_scalar |
| `OBJECT_CARD_PERIOD_QUEEN_P0_F__CycleStateSystem_v1.0.md` | 4 | object_id, lock_status, filter_action, risk_action |
| `OBJECT_CARD_TKR7_P0_E__AO_Divergence_v1.0.md` | 5 | object_id, lock_status, filter_action, risk_action, size_scalar |
| `OBJECT_CARD_VOLFAC_P0_A__VolatilityFactor_v1.0.md` | 7 | object_id, signal_type, signal_strength, confidence, lock_status, risk_action, size_scalar |
| `OBJECT_CARD_VOLTARGET_P0_R__VolatilityTargeting_v1.0.md` | 8 | object_id, signal_type, signal_strength, confidence, lock_status, filter_action, risk_action, size_scalar |
| `OBJECT_CARD_VP_P0_E__VolumeProfile_v1.0.md` | 6 | object_id, confidence, lock_status, filter_action, risk_action, size_scalar |
| `OBJECT_CARD_YTC_P0_E__YTC_Microstructure_v1.0.md` | 6 | object_id, confidence, lock_status, filter_action, risk_action, size_scalar |

> **说明**: 很多对象卡使用字段别名（如 `signal_confidence` 代替 `confidence`），或字段嵌入在伪代码/JSON中导致字符串匹配失败。建议统一输出格式为显式的字段列表。

---

## 5. 版本声明（元信息块）

**标准元信息应包含**: 文档信息/版本号/状态/最后更新/生产者

**缺少元信息的文件** (5 个):

- `EXTERNAL_SYSTEM_FUNCTION_MAP_v0.1.md`
- `EXTERNAL_SYSTEM_REFERENCE_v2.0.md`
- `E_DIRECTION_EXTRA_SEARCH_v1.0.md`
- `MTF_SEB_v0.1.md`
- `全仓库功能映射大表_v1.0.md`

---

## 6. 术语一致性

### 6.1 PeriodQueen 变体

| 变体 | 出现次数 | 出现位置示例 | 建议 |
|------|----------|-------------|------|
| `PeriodQueen` | 138 | 正文/描述 | 保留（正文用语） |
| `PERIOD_QUEEN` | 71 | 字段名/常量 | 保留（代码/字段用语） |
| `周期女王` | 26 | 中文描述 | 建议统一为 `PeriodQueen` |
| `period_queen` | 18 | 变量名/JSON键 | 建议统一为 `PERIOD_QUEEN` 或 `PeriodQueen` |

### 6.2 对象卡术语

- 中文 `对象卡`: 868 次 -- 主导术语
- 英文 `Object Card`: 4 次 -- 仅出现在 `BACKTEST_FRAMEWORK_DESIGN_v1.0.md` 和 `PROGRAMMING_AI_ULTIMATE_TASK_PACKAGE_v1.0.md`

**建议**: 统一使用中文 `对象卡`，仅在代码/字段中使用 `OBJECT_CARD` 前缀。

---

## 7. ABORT 原因编码一致性

**VOTE_DECISION_TABLE_P0_E_v1.0.md 第5.1节 定义的标准编码**（14种）:

1. `missing_ohlcv`
2. `period_queen_halt`
3. `period_queen_unclear`
4. `no_votes`
5. `all_blocked`
6. `votes_insufficient`
7. `van_tharp_limit`
8. `position_too_small`
9. `no_positions_to_exit`
10. `insufficient_exit_signals`
11. `global_block`
12. `maturity_unverified`
13. `level2_missing`
14. `market_halt`

**发现 2 个非标准 ABORT 编码**:

- `abort_reason`
- `period_queen_unknown_permission`

---

## 8. 量化标注一致性

**标准标注**: `proxy_quantizable_now` / `needs_extra_data` / `future_bucket` / `shell_only` / `NOT_QUANT_YET`

**使用统计**:

| 标注 | 出现次数 | 含义 |
|------|----------|------|
| `proxy_quantizable_now` | 103 | 可直接量化（A股数据已普及） |
| `needs_extra_data` | 49 | 需要额外数据（Level-2/龙虎榜等） |
| `shell_only` | 22 | 仅概念壳（不可直接编码） |
| `future_bucket` | 19 | 未来实现（条件不成熟） |
| `NOT_QUANT_YET` | 3 | 明确不可量化 |

**大小写/格式变体**:

- `BACKTEST_FRAMEWORK_DESIGN_v1.0.md` 第133行 -- 使用 `PROXY_QUANTIZABLE` 或 `proxy_quantizable`（缺少 `_now` 后缀）
- `BACKTEST_FRAMEWORK_DESIGN_v1.0.md` 第292行 -- 使用 `PROXY_QUANTIZABLE` 或 `proxy_quantizable`（缺少 `_now` 后缀）
- `BACKTEST_REPORT_TEMPLATE_v1.0.md` 第166行 -- 使用 `PROXY_QUANTIZABLE` 或 `proxy_quantizable`（缺少 `_now` 后缀）
- `BACKTEST_REPORT_TEMPLATE_v1.0.md` 第167行 -- 使用 `PROXY_QUANTIZABLE` 或 `proxy_quantizable`（缺少 `_now` 后缀）
- `EXTERNAL_SYSTEM_REFERENCE_v1.0.md` 第366行 -- 使用 `PROXY_QUANTIZABLE` 或 `proxy_quantizable`（缺少 `_now` 后缀）

**建议**: 统一使用小写带后缀格式 `proxy_quantizable_now`。

---

## 问题清单汇总

### 严重问题（需优先修复）

1. **`GLM_TASK_02_CHANLUN_OBJECT_CARD.md`** -- 对象卡缺少标准输出字段: signal_type, signal_strength, confidence, lock_status, filter_action, risk_action, size_scalar
2. **`OBJECT_CARD_ATRATIO_P0_A__ActiveTradeRatio_v1.0.md`** -- 对象卡缺少标准输出字段: object_id, signal_strength, confidence, lock_status, risk_action, size_scalar
3. **`OBJECT_CARD_BACKTEST_SCHEDULE_v1.0.md`** -- 对象卡缺少标准输出字段: object_id, signal_strength, lock_status, filter_action, risk_action
4. **`OBJECT_CARD_BPB_P0_E__Brooks_Breakout_Pullback_v1.0.md`** -- 对象卡缺少标准输出字段: object_id, lock_status, filter_action, risk_action, size_scalar
5. **`OBJECT_CARD_CHZL_BSD_P0_E__Chanlun_Buy_Sell_Signals_v1.0.md`** -- 对象卡缺少标准输出字段: object_id, signal_type, signal_strength, confidence, lock_status, filter_action, risk_action, size_scalar
6. **`OBJECT_CARD_INSTB_P0_A__InstitutionalBehavior_v1.0.md`** -- 对象卡缺少标准输出字段: object_id, signal_strength, confidence, lock_status, risk_action, size_scalar
7. **`OBJECT_CARD_KELLY_P0_R__KellyCriterion_v1.0.md`** -- 对象卡缺少标准输出字段: object_id, signal_type, lock_status, filter_action, risk_action, size_scalar
8. **`OBJECT_CARD_MFLOW_P0_A__MoneyFlow_v1.0.md`** -- 对象卡缺少标准输出字段: object_id, confidence, lock_status, risk_action, size_scalar
9. **`OBJECT_CARD_PERIOD_QUEEN_P0_F__CycleStateSystem_v1.0.md`** -- 对象卡缺少标准输出字段: object_id, lock_status, filter_action, risk_action
10. **`OBJECT_CARD_TKR7_P0_E__AO_Divergence_v1.0.md`** -- 对象卡缺少标准输出字段: object_id, lock_status, filter_action, risk_action, size_scalar
11. **`OBJECT_CARD_VOLFAC_P0_A__VolatilityFactor_v1.0.md`** -- 对象卡缺少标准输出字段: object_id, signal_type, signal_strength, confidence, lock_status, risk_action, size_scalar
12. **`OBJECT_CARD_VOLTARGET_P0_R__VolatilityTargeting_v1.0.md`** -- 对象卡缺少标准输出字段: object_id, signal_type, signal_strength, confidence, lock_status, filter_action, risk_action, size_scalar
13. **`OBJECT_CARD_VP_P0_E__VolumeProfile_v1.0.md`** -- 对象卡缺少标准输出字段: object_id, confidence, lock_status, filter_action, risk_action, size_scalar
14. **`OBJECT_CARD_YTC_P0_E__YTC_Microstructure_v1.0.md`** -- 对象卡缺少标准输出字段: object_id, confidence, lock_status, filter_action, risk_action, size_scalar
15. **`INDEX_v2.0.md`** -- 文件名不符合命名规范

### 警告（建议修复）

1. **`EXTERNAL_SYSTEM_FUNCTION_MAP_v0.1.md`** -- 缺少版本/状态/更新日期元信息
2. **`EXTERNAL_SYSTEM_REFERENCE_v2.0.md`** -- 缺少版本/状态/更新日期元信息
3. **`E_DIRECTION_EXTRA_SEARCH_v1.0.md`** -- 缺少版本/状态/更新日期元信息
4. **`MTF_SEB_v0.1.md`** -- 缺少版本/状态/更新日期元信息
5. **`全仓库功能映射大表_v1.0.md`** -- 缺少版本/状态/更新日期元信息
6. **`INDEX_v2.0.md`** -- 引用不存在的对象卡 `OBJECT_CARD_CHZL_FX_P0_S__Chanlun_Fenxing_v1.0.md`
7. **`INDEX_v2.0.md`** -- 引用不存在的对象卡 `OBJECT_CARD_CHZL_BI_P0_S__Chanlun_Bi_v1.0.md`
8. **`INDEX_v2.0.md`** -- 引用不存在的对象卡 `OBJECT_CARD_CHZL_ZS_P0_S__Chanlun_Zhongshu_v1.0.md`
9. **`INDEX_v2.0.md`** -- 引用不存在的对象卡 `OBJECT_CARD_CHZL_TREND_P0_S__Chanlun_Trend_v1.0.md`
10. **`INDEX_v2.0.md`** -- 引用不存在的对象卡 `OBJECT_CARD_TK_R6_P0_E__TK_Forex_Pattern_v1.0.md`
11. **`INDEX_v2.0.md`** -- 引用不存在的对象卡 `OBJECT_CARD_TK_R7_P0_E__TK_Forex_Pattern_v1.0.md`
12. **`INDEX_v2.0.md`** -- 引用不存在的对象卡 `OBJECT_CARD_TK_R8_P0_E__TK_Forex_Pattern_v1.0.md`
13. **术语不一致** -- `周期女王` 出现 26 次，建议统一为 `PeriodQueen`（正文）或 `PERIOD_QUEEN`（代码）
14. **术语不一致** -- `period_queen` 出现 18 次，建议统一为 `PeriodQueen`（正文）或 `PERIOD_QUEEN`（代码）
15. **`BACKTEST_FRAMEWORK_DESIGN_v1.0.md`** 第133行 -- `proxy_quantizable` 大小写/后缀不一致
16. **`BACKTEST_FRAMEWORK_DESIGN_v1.0.md`** 第292行 -- `proxy_quantizable` 大小写/后缀不一致
17. **`BACKTEST_REPORT_TEMPLATE_v1.0.md`** 第166行 -- `proxy_quantizable` 大小写/后缀不一致

### 建议（可选优化）

1. **INDEX_v2.0.md** 中 `STRATEGY_DESIGN_REFERENCE_v1.0.md` 重复列出两次（第102行和第103行）
2. **全仓库功能映射大表** 存在 v1.0 / v2.0 / v2.2 三个版本，建议清理废弃版本或明确标记
3. **EXTERNAL_STRATEGY_RAW_MATERIAL** v1.0-v7.0 共 7 个版本，建议合并或建立版本索引
4. **GLM_TASK 系列** 9 个文件无版本号后缀，建议统一添加 `_v1.0.md`

---

> **报告生成**: 2026-07-07 | 审查工具: 自动化脚本 + 人工复核
> **免责声明**: 本报告基于字符串匹配和正则表达式分析，部分缺失字段可能是由于字段以不同形式出现（如嵌入JSON/伪代码中）。建议人工复核后再做修改。