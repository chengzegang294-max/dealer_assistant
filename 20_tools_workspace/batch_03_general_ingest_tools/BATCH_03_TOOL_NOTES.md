# Batch 03 Tool Notes

## 文件 1：`s_bucketize.py`

- 文件类型：`GENERATOR`
- 原路径：`旧仓库\tools\s_bucketize.py`
- 新路径：`20_tools_workspace\batch_03_general_ingest_tools\s_bucketize.py`
- 当前作用：
  - 对来源材料做一级分桶、重复候选判断、信息密度猜测
  - 生成 inventory
  - 支持按 `bucket_l1` 或按选定 TSV 做 staging proof
- 主要输入：
  - `--root`
  - `--inventory-out`
  - 可选：`--stage-bucket-l1 / --stage-select-tsv / --stage-dest-root / --stage-proof-out`
- 主要输出：
  - inventory tsv
  - staging proof tsv
  - staging 目录副本
- 当前用途：
  - 继续服务来源库整理、S 桶或类似材料的可追溯 staging
- 适用边界：
  - 偏“目录整理与 staging 证明”
  - 不是交易执行脚本
- 证据模式：`historical_recovered_then_promoted`

## 文件 2：`ingest_ashare_txt_to_md.py`

- 文件类型：`GENERATOR`
- 原路径：`旧仓库\tools\ingest_ashare_txt_to_md.py`
- 新路径：`20_tools_workspace\batch_03_general_ingest_tools\ingest_ashare_txt_to_md.py`
- 当前作用：
  - 读取 A 股策略类 `.txt`
  - 猜编码
  - 按标题关键词分 cluster
  - 转成带元信息的 `.md`
- 主要输入：
  - `--src-dir`
  - `--out-dir`
- 主要输出：
  - cluster 子目录中的 `.md`
  - `README_放这里.md`
  - `txt_md_index_v1.tsv`
- 当前用途：
  - 把旧文本样本转成新仓库可检索、可归档、带来源说明的 md 层
- 适用边界：
  - 只处理 `.txt -> .md`
  - 不负责后续量化吸收
- 证据模式：`historical_recovered_then_promoted`

## 文件 3：`kimi_cutpack_manifest.py`

- 文件类型：`GENERATOR`
- 原路径：`旧仓库\tools\kimi_cutpack_manifest.py`
- 新路径：`20_tools_workspace\batch_03_general_ingest_tools\kimi_cutpack_manifest.py`
- 当前作用：
  - 遍历 `CUTPACK__*.md`
  - 提取 `bucket / title_short / version / retain_mode / current_repo_role / quant_rows`
  - 生成 manifest tsv
- 主要输入：
  - `--root`
  - `--out`
- 主要输出：
  - manifest tsv
- 当前用途：
  - 对 cutpack 资产做元数据盘点与索引，避免只靠文件名猜用途
- 适用边界：
  - 偏目录级资产清点
  - 不负责 cutpack 内容本身的正确性判断
- 证据模式：`historical_recovered_then_promoted`

## 文件 4：`relocate_path_prefix.py`

- 文件类型：`GENERATOR`
- 原路径：`旧仓库\tools\relocate_path_prefix.py`
- 新路径：`20_tools_workspace\batch_03_general_ingest_tools\relocate_path_prefix.py`
- 当前作用：
  - 扫描目录树下的 `.md / .tsv`
  - 将路径前缀做全量替换
- 主要输入：
  - `--root`
  - `--old`
  - `--new`
  - 可选：`--glob`
- 主要输出：
  - 原地改写文件内容（无额外产物目录）
- 适用边界：
  - 仅用于“路径锚点迁移/目录重定位”这类批量替换，不做内容裁决
- 证据模式：`historical_recovered_then_promoted`

## 文件 5：`slice_csv_tail_v1.py`

- 文件类型：`GENERATOR`
- 原路径：`旧仓库\tools\slice_csv_tail_v1.py`
- 新路径：`20_tools_workspace\batch_03_general_ingest_tools\slice_csv_tail_v1.py`
- 当前作用：
  - 读取 CSV
  - 保留 header
  - 输出末尾 `N` 行到新文件
- 主要输入：
  - `--input`
  - `--output`
  - `--tail-lines`
- 主要输出：
  - 一个新的 tail CSV 文件
- 适用边界：
  - 仅做“尾部截取”，不解析字段语义
- 证据模式：`historical_recovered_then_promoted`

## 文件 6：`tk_manual_append_rows.py`

- 文件类型：`GENERATOR`
- 原路径：`旧仓库\tools\tk_manual_append_rows.py`
- 新路径：`20_tools_workspace\batch_03_general_ingest_tools\tk_manual_append_rows.py`
- 当前作用：
  - 对 TSV 手工表追加空行模板（保留列数）
  - 支持写入 `date_tag` 前缀
- 主要输入：
  - `--sheet`
  - 可选：`--n`
  - 可选：`--date-tag`
- 主要输出：
  - 原地追加行（无额外产物目录）
- 适用边界：
  - 仅用于“人工表格填充辅助”，不做审计或回测逻辑
- 证据模式：`historical_recovered_then_promoted`

## 当前批次结论

- 这 6 个脚本都已从旧仓库明确识别为“长期可能复用的通用工具”。
- 当前不把它们归到：
  - 回测审计家族
  - 交易执行脚本
  - 一次性删除脚本
- 它们进入新仓库后，默认归 `20_tools_workspace` 维护，不再混进 `12_tooling_runtime_archive`。
