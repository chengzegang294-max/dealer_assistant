# Sensitivity 27 Combos: Purity × T1 触发矩阵（按 sec5_billion 分页）

- 参数空间: t1_mul∈[0.9, 1.0, 1.1] × purity_thr∈[0.55, 0.6, 0.65] × sec5_billion∈[80, 100, 120] = 27 组合
- 数据日: 20260810（8/10 真实数据 calc_day，prev=None）
- 记号: `T1_PASS` / `T1_WAIT` · `PURITY_YES` / `PURITY_NO` · 单元格为 `(T1状态, Purity状态)`

---

## Page: sec5_billion = 80 亿

低离散条件: sector_top5_sum_yi < 80 亿  （8/10 实际值 = 72.5 亿）

| purity_thr \\ t1_mul | 0.9 | 1 | 1.1 |
|---|---|---|---|
| 0.55 | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/18.0%<br>Pur=61.5%/55% | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/20.0%<br>Pur=61.5%/55% | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/22.0%<br>Pur=61.5%/55% |
| 0.6 | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/18.0%<br>Pur=61.5%/60% | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/20.0%<br>Pur=61.5%/60% | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/22.0%<br>Pur=61.5%/60% |
| 0.65 | `(T1_WAIT, PURITY_NO)`<br>T1=12.1%/18.0%<br>Pur=61.5%/65% | `(T1_WAIT, PURITY_NO)`<br>T1=12.1%/20.0%<br>Pur=61.5%/65% | `(T1_WAIT, PURITY_NO)`<br>T1=12.1%/22.0%<br>Pur=61.5%/65% |

### 本页单独计数

- T1 触发: 0/9
- 抱团满足: 6/9

---

## Page: sec5_billion = 100 亿

低离散条件: sector_top5_sum_yi < 100 亿  （8/10 实际值 = 72.5 亿）

| purity_thr \\ t1_mul | 0.9 | 1 | 1.1 |
|---|---|---|---|
| 0.55 | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/18.0%<br>Pur=61.5%/55% | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/20.0%<br>Pur=61.5%/55% | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/22.0%<br>Pur=61.5%/55% |
| 0.6 | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/18.0%<br>Pur=61.5%/60% | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/20.0%<br>Pur=61.5%/60% | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/22.0%<br>Pur=61.5%/60% |
| 0.65 | `(T1_WAIT, PURITY_NO)`<br>T1=12.1%/18.0%<br>Pur=61.5%/65% | `(T1_WAIT, PURITY_NO)`<br>T1=12.1%/20.0%<br>Pur=61.5%/65% | `(T1_WAIT, PURITY_NO)`<br>T1=12.1%/22.0%<br>Pur=61.5%/65% |

### 本页单独计数

- T1 触发: 0/9
- 抱团满足: 6/9

---

## Page: sec5_billion = 120 亿

低离散条件: sector_top5_sum_yi < 120 亿  （8/10 实际值 = 72.5 亿）

| purity_thr \\ t1_mul | 0.9 | 1 | 1.1 |
|---|---|---|---|
| 0.55 | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/18.0%<br>Pur=61.5%/55% | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/20.0%<br>Pur=61.5%/55% | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/22.0%<br>Pur=61.5%/55% |
| 0.6 | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/18.0%<br>Pur=61.5%/60% | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/20.0%<br>Pur=61.5%/60% | `(T1_WAIT, PURITY_YES)`<br>T1=12.1%/22.0%<br>Pur=61.5%/60% |
| 0.65 | `(T1_WAIT, PURITY_NO)`<br>T1=12.1%/18.0%<br>Pur=61.5%/65% | `(T1_WAIT, PURITY_NO)`<br>T1=12.1%/20.0%<br>Pur=61.5%/65% | `(T1_WAIT, PURITY_NO)`<br>T1=12.1%/22.0%<br>Pur=61.5%/65% |

### 本页单独计数

- T1 触发: 0/9
- 抱团满足: 6/9

---

## 全局汇总

| sec5_billion | T1 触发 /9 | 抱团满足 /9 |
|---|---|---|
| 80 亿 | 0/9 | 6/9 |
| 100 亿 | 0/9 | 6/9 |
| 120 亿 | 0/9 | 6/9 |

**合计**: T1=0/27 · 抱团=18/27 · 低离散=27/27 · 背离≥2天=0/27 · 假强=0/27

