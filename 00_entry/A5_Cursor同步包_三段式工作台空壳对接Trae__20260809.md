# A5 Cursor同步包｜三段式工作台空壳对接 Trae

更新时间：2026-08-09  
给谁：Trae / 其他执行位（也可 Cursor 续跑）  
仓库：`d:\Stock\dealer_assistant`

## 0. 先看结论

1. Cursor 已在新仓落下**三段式工作台空壳**（盘前 / 盘中 / 盘后）
2. 当前只做阶段1边界：空壳 + 字段合同 + 日文件落点
3. 不做：实时信号、自动判断句、完整 UI
4. Trae 若接手，先读字段合同，再按「可做 / 不做」推进；不要重开形态讨论

正式空壳页：

- [A5_私人短线工作台三段式空壳与字段合同__20260809.md](file:///d:/Stock/dealer_assistant/00_entry/全库资料整理收口__20260713/A5_私人短线工作台三段式空壳与字段合同__20260809.md)

上游裁决：

- [A5_私人短线工作台与最终输出形态_多家AI回收记录与主负责人裁决__20260809.md](file:///d:/Stock/dealer_assistant/00_entry/全库资料整理收口__20260713/A5_私人短线工作台与最终输出形态_多家AI回收记录与主负责人裁决__20260809.md)

## 1. Trae 必读顺序

1. 本同步包（先看可做 / 不做）
2. 空壳字段合同页（上一节链接）
3. runtime README：
   - [batch_01_three_card_shell README](file:///d:/Stock/dealer_assistant/02_runtime/shortline_workbench/batch_01_three_card_shell__20260809/README.md)
4. 字段 TSV：
   - [three_card_field_contract__20260809.tsv](file:///d:/Stock/dealer_assistant/02_runtime/shortline_workbench/batch_01_three_card_shell__20260809/derived/three_card_field_contract__20260809.tsv)
5. 日用模板：
   - [three_card_day__template.md](file:///d:/Stock/dealer_assistant/02_runtime/shortline_workbench/batch_01_three_card_shell__20260809/templates/three_card_day__template.md)
6. 相关日常线（只引用，不合并）：
   - [P1 日常口令页](file:///d:/Stock/dealer_assistant/00_entry/全库资料整理收口__20260713/A5_P1与sector日常执行口令页__20260809.md)
   - [直播间正式短名单](file:///d:/Stock/dealer_assistant/00_entry/全库资料整理收口__20260713/A5_直播间长期保留_vs_片段优先正式短名单__20260809.md)
   - [C/D 降权落地清单](file:///d:/Stock/dealer_assistant/00_entry/全库资料整理收口__20260713/A5_直播间C_D桶降权落地清单__20260809.md)

## 2. 已完成（不要重开）

- 工作台形态已裁决为：三段式卡片 + 分阶段自动化
- 空壳三张卡字段合同已落盘
- 日文件命名：`workbench_day__{YYYYMMDD}.md`
- 与 `P1` / `sector` 日常线的分工已钉死：工作台引用，不替代
- `C/D` 降权落地清单已存在；工作台不把这 7 房放进主视野

## 3. Trae 可做 / 不做

### 可做

1. 按模板生成某一交易日空壳日文件（判断格留空）
2. 运行 / 续写阶段2事实预填（已有设计稿 + `prefill_workbench_day_facts_v1.py`）
3. 把空壳字段和现有 `prefill_p1_day_facts_v1.py` 的映射关系写清楚
4. 若主负责人要求：回填其他入口索引里的工作台链接

### 不做

1. 不改三段式形态，不改成实时信号面板
2. 不自动写 `bias_preopen` / `judge_ok` 等判断格
3. 不合并删除 `P1` 日记录或 `sector` 快照独立链
4. 不把 C/D 降权房重新拉回主视野
5. 不在大仓 `trading_assistant` 上重开平行空壳（以本仓 `dealer_assistant` 为准）
6. 不排障 Nikki/代理（项目侧默认用 Cursor）

## 4. Cursor 已落痕迹（对接用路径表）

| 用途 | 路径 |
|------|------|
| 空壳合同入口 | `00_entry/全库资料整理收口__20260713/A5_私人短线工作台三段式空壳与字段合同__20260809.md` |
| 阶段2事实预填设计 | `00_entry/全库资料整理收口__20260713/A5_工作台阶段2事实预填设计稿__20260810.md` |
| 本同步包 | `00_entry/A5_Cursor同步包_三段式工作台空壳对接Trae__20260809.md` |
| runtime 批目录 | `02_runtime/shortline_workbench/batch_01_three_card_shell__20260809/` |
| 日文件目录 | `.../daily/workbench_day__{YYYYMMDD}.md` |
| 工作台事实预填脚本 | `20_tools_workspace/batch_08_quicktiny_capture_tools/prefill_workbench_day_facts_v1.py` |
| 合卡模板 | `.../templates/three_card_day__template.md` |
| 字段合同 TSV | `.../derived/three_card_field_contract__20260809.tsv` |

## 5. 建议 Trae 下一手（最小）

若额度/索引恢复后要续：

```text
按 dealer_assistant 三段式工作台空壳对接包继续。
只做：为空壳补「事实预填设计稿」或生成指定交易日空壳日文件。
不做：自动判断、实时面板、重开形态讨论。
交易日：YYYYMMDD（若需要生成日文件）。
```

## 6. 一句话转交

> 三段式工作台空壳已在 `dealer_assistant` 落盘；Trae 接手时先读本同步包与字段合同，只允许在空壳上做事实预填设计或日文件生成，不要重开形态、不要自动写判断。
