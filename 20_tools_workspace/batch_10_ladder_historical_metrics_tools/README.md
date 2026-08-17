# batch_10 — 连板天梯历史指标工具

## 用途

从已落盘的 `ladder_day_min__YYYYMMDD.json` + `sector_capital_flow_snapshot__YYYYMMDD.json` 批量计算 P1/P3 用结构指标，append 到历史 TSV。

公式来源（冻结，脚本内不改算法）：

- `00_entry/.../A5_连板天梯盘后3分钟怎么看__极简版__20260809.md` 第 7 大节 7.1–7.6
- `02_runtime/quicktiny_capture/batch_04_min_contract__20260808/A5_最小字段合同__20260808.md` 7.2 公式表 + 7.3 缺字段兜底
- 旧仓单日实现：`trading_assistant/90_SCRATCH.../calc_810_metrics.py`（DI / Purity / T1 / T3 / 对齐度 / 风险档）

## 依赖

- Python 3.10+
- 仅标准库：`argparse` / `json` / `csv` / `pathlib` / `collections` / `dataclasses`
- 无第三方包，无网络请求

## 输入

| 文件 | 命名 | 说明 |
|------|------|------|
| 天梯 min | `ladder_day_min__YYYYMMDD.json`（或 `ladder_day_min_YYYYMMDD.json`） | 含 `dates[].boards[].stocks[]` |
| 板块资金 | `sector_capital_flow_snapshot__YYYYMMDD.json` 或 `sector_capital_flow_min__YYYYMMDD.json` | 含 `data.rows[]` 或顶层 `rows` |

目录参数：

- `--ladder-dir` / `--sector-dir`：显式目录
- 都不传：在 `02_runtime/quicktiny_capture/` 下递归搜各 batch / `*_daily_snapshots`

缺字段兜底（合同 7.3）：

- `open_num` null/缺 → 0
- `primary_theme` 缺 → `UNKNOWN`
- 缺 `order_amount`/`trading_amount` → 风险档不算封单比条件
- 缺 `turnover_rate` → 风险档不算换率条件

## 输出 TSV 列（固定顺序）

```
date | max_level | total_stocks | ge2_stocks | first_panel_count | T1_dynamic_threshold | T1_pct | T3_pct | Purity_ge2_pct | sector_top5_sum_yi | align_top3_top5_count | consecutive_divergence_days | top4_di_list | top4_risk_list | p1_position_advice | fake_strength_warning
```

- 默认路径：`02_runtime/quicktiny_capture/metrics_history.tsv`
- 文件不存在 → 写 header；已存在 → append（不重写 header）

跨日字段：

- `consecutive_divergence_days`：对齐度=0 且 sector 前 5 合计 <100 亿 且天梯情绪高 → 连续天数
- `T1_dynamic_threshold`：首板 >80 → 20；<60 → 30；中间 → 25
- `Purity_ge2` 3 日滚动平均在内存计算（窗口不足 3 日则为空，不单独出列）
- `fake_strength_warning`：前 5 <100 亿 且最高板抬升 → `1`，否则 `0`

## 命令样例

### dry-run（8/10 金标，与 calc_810 对齐）

```powershell
python "d:\Stock\dealer_assistant\20_tools_workspace\batch_10_ladder_historical_metrics_tools\calc_ladder_metrics_batch_v1.py" --dry-run
```

或显式指定 8/10 文件：

```powershell
python "d:\Stock\dealer_assistant\20_tools_workspace\batch_10_ladder_historical_metrics_tools\calc_ladder_metrics_batch_v1.py" `
  --dry-run `
  --ladder-file "d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\ladder_daily_snapshots\ladder_day_min__20260810.json" `
  --sector-file "d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\sector_daily_snapshots\sector_capital_flow_snapshot__20260810.json"
```

期望（与 calc_810 一致）：`T1=12.1` `T3=23.2` `Purity_ge2=61.5` `align=0` `DI=0,15,0,12` `risk=G,R,Y,R`，相对误差 >0.1% 则 exit 1。

### 批量写入历史 TSV

```powershell
python "d:\Stock\dealer_assistant\20_tools_workspace\batch_10_ladder_historical_metrics_tools\calc_ladder_metrics_batch_v1.py" `
  --ladder-dir "d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\ladder_daily_snapshots" `
  --sector-dir "d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\sector_daily_snapshots" `
  --output-tsv "d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\metrics_history.tsv" `
  --start-date 20260810 `
  --end-date 20260810
```

## 当前一句话

- 先有冻结公式 + 真实 8/10 dry-run 对齐，再 append 历史 TSV；不抓站、不改合同阈值。
