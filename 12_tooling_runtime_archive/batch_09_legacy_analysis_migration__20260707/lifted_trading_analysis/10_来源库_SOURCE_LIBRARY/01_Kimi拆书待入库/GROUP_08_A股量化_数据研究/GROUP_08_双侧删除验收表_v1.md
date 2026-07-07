# GROUP_08 双侧删除验收表 v1

更新时间：2026-06-21

## 本表作用

- 这张表用于正式回答：
  - 仓库内 `GROUP_08_A股量化_数据研究__SOURCE_RAW\新的参考书` 现在能不能删
  - 外部 `D:\Stock\cut_file\S` 现在能不能删
- 本轮不做真实删除，只做验收裁决。

## 验收口径

- `DELETE_READY`
  - 已有稳定替代产物
  - 回指关系完整
  - 当前没有其他仓库路径继续直接引用该源
- `PARTIAL_DELETE_READY`
  - 只能按子集或子目录局部删
  - 不能按整组或整目录删
- `NOT_DELETE_READY`
  - 仍缺回指、仍缺替代产物，或仍被其他资产线直接引用

## 双侧对象

- 仓库内侧：
  - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_08_A股量化_数据研究__SOURCE_RAW\新的参考书`
- 外部侧：
  - `D:\Stock\cut_file\S`

## 总裁决

| 侧别 | 对象 | 当前状态 | 裁决 |
|---|---|---|---|
| 仓库内侧 | `GROUP_08_A股量化_数据研究__SOURCE_RAW\新的参考书` | `txt` 线已基本对齐；`research pdf` 已有逐条映射；`pdf 入门书 / epub` 仍未完成删源审计 | `PARTIAL_DELETE_READY` |
| 外部侧 | `D:\Stock\cut_file\S` | `S` 不是只服务 `GROUP_08` 的单用途源仓，仍被别的来源线直接引用 | `NOT_DELETE_READY` |

## A. 仓库内侧验收

### A1. 当前可删边界

| 源线 | 当前状态 | 验收结论 | 原因 |
|---|---|---|---|
| `txt` | `99` 条源 `txt -> md_path` 已由 `txt_md_index_v1.tsv` 逐条保存 | `DELETE_READY` | 已存在稳定 `md` 归档索引，且当前 `GROUP_08` 主线已不再依赖原 `txt` 逐条阅读 |
| `research pdf` | 已有 `标题锚点 -> v2 md` 逐条映射清单，并新增 `逐文件删除勾验行_v1.md` | `PARTIAL_DELETE_READY` | 逐文件勾验骨架已成，但还缺最终删除勾选 |
| `pdf 入门书` | 只有索引层、章节卡层 | `NOT_DELETE_READY` | 尚未完成逐册删源审计 |
| `epub` | 仍是粗切/解释层 | `NOT_DELETE_READY` | 尚未完成可替代真值锚定 |

### A2. 当前仓库内侧结论

- 可以进入“删源候选”的，仅限：
  - `txt` 线
  - `research pdf` 中已经进到 `v2` 且后续最终删除勾选通过的条目
- 当前不能整目录删除：
  - `GROUP_08_A股量化_数据研究__SOURCE_RAW\新的参考书`
- 原因：
  - `pdf 入门书`
  - `epub`
  - 以及 `research pdf` 的逐文件勾验
  - 还没有全部完成

## B. 外部侧验收

### B1. 当前不能按整目录删 `D:\Stock\cut_file\S`

| 外部对象 | 当前状态 | 验收结论 | 原因 |
|---|---|---|---|
| `D:\Stock\cut_file\S` 整目录 | 仍服务多个来源线 | `NOT_DELETE_READY` | 不是 `GROUP_08` 单独占用 |
| `D:\Stock\cut_file\S\01_集合竞价教程` | 仍被 `02_原子化拆解文件` 多张规则卡直接引用 | `NOT_DELETE_READY` | 当前仓库还有绝对路径锚点 |
| `D:\Stock\cut_file\S\02_游资悟道交割单` | 历史上已有局部删除案例，但不是整目录可删 | `PARTIAL_DELETE_READY` | 只能沿已裁决的低价值子目录局部清理 |
| `D:\Stock\cut_file\S\03_券商研报` | 才是 `GROUP_08 research pdf` 的主要外部真值源候选 | `PARTIAL_DELETE_READY` | 未来只可能做 `GROUP_08` 子集局部删除，不是整棵 `S` 可删 |

### B2. 当前外部侧结论

- 当前绝对不能写成：
  - `D:\Stock\cut_file\S` 整理后可删
- 当前只能写成：
  - `D:\Stock\cut_file\S\03_券商研报` 中与 `GROUP_08 research pdf` 一一对应、并且完成勾验的那部分，未来可局部删
- 当前还不能删的直接证据：
  - 仓库内 `02_原子化拆解文件` 仍直接引用：
    - `D:\Stock\cut_file\S\01_集合竞价教程\...`
  - `GROUP_08` 当前虽然已有逐文件删除勾验行，但外部侧还没逐条补精确路径

## C. 本轮正式验收结论

- `仓库内侧`
  - 当前状态：`PARTIAL_DELETE_READY`
  - 可推进删除候选：`txt` 线、后续勾验完成的 `research pdf`
  - 不可整目录删除：`source_raw\新的参考书`
- `外部侧`
  - 当前状态：`NOT_DELETE_READY`
  - `S` 整目录不可删
  - 未来只能考虑：
    - `03_券商研报` 下与 `GROUP_08 research pdf` 一一对应的局部子集

## D. 下一步只剩什么

- 若继续，不再回头重扫：
  - 给仓库内侧补最终删除勾选
  - 给 `D:\Stock\cut_file\S\03_券商研报` 对应子集补精确路径 + 最终删除勾选
- 做完这两步后，才能把“整理后可删”从口头判断升级成正式删除口令。
