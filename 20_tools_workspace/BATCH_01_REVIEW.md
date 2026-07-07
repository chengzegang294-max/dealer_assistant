# Tools Workspace Batch 01 Review

## 批次结论

- 本批已完成 `20_tools_workspace` 首批迁入。
- 当前已迁入新仓库的通用工具脚本共 `4` 个，位置：
  - `20_tools_workspace\batch_01_selected\`
- 本批优先保留的是“以后还会反复用”的轻量通用工具，不是历史一次性清理脚本。

## 本批迁入文件

- `generate_p0_subset.py`
- `relocate_path_prefix.py`
- `slice_csv_tail_v1.py`
- `tk_manual_append_rows.py`

## 为什么这 4 个先进

- `generate_p0_subset.py`
  - 作用：从原子规则表里抽出可审计的 P0 子表
- `relocate_path_prefix.py`
  - 作用：批量替换路径前缀，适合未来仓库去旧路径化
- `slice_csv_tail_v1.py`
  - 作用：稳定裁剪 CSV 尾部样本，适合做最小样本副本
- `tk_manual_append_rows.py`
  - 作用：向 TSV 手工表追加空白行，适合保留为人工处理工具

## 本批裁决

- 已吸收：
  - 上述 4 个通用脚本
- 可重开：
  - `s_bucketize.py`
  - `s_dedup_report.py`
  - `s_dedup_delete_list.py`
  - 原因：它们偏整理线通用工具，但本批先不扩
- future bucket：
  - `group08_*`
  - `tk_r*`
  - 原因：更多是某批项目或某轮审计的专用脚本，后续按专题再拆
- 仅旧仓库保留：
  - 无法说明长期维护职责的一次性历史脚本

## 下一步建议

1. 单开 `group08` 系列工具批次
2. 单开 `tk_r*` 审计工具批次
3. 继续把与新仓库直接有关的通用小工具优先迁入
