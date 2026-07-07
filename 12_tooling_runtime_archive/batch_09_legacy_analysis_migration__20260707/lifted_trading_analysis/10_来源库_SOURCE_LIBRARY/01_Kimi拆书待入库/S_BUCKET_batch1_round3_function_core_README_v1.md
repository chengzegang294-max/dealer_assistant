# S_BUCKET batch1 round3 function core

本包用于把 `SBKT_F014 / SBKT_F006 / SBKT_F002` 从“第二轮正文收缩结果”继续推进到“第三轮功能核心对象卡”。

## 当前作用

- 不再做 OCR 检查
- 不再重复第二轮的正文收缩
- 只做功能层固化：
  - 最小输入
  - 最小输出
  - 使用场景
  - 禁用场景
  - 组合关系
  - 边界标签

## 仓库真值

- 默认执行顺序：
  - 先读本 README
  - 再读 `manifest` 和 `prompt`
  - 需要直发时再用 `S_BUCKET_KIMI_batch1_round3_function_core_direct_message_v1.txt`

- manifest:
  - `S_BUCKET_batch1_round3_function_core_manifest_v1.tsv`
- prompt:
  - `S_BUCKET_KIMI_batch1_round3_function_core_prompt_v1.txt`
- direct message:
  - `S_BUCKET_KIMI_batch1_round3_function_core_direct_message_v1.txt`
- 已有上轮回收表：
  - `S_BUCKET_功能映射表_v1.tsv`

## 外部 PDF 目录

- `D:\Stock\cut_file\data\__KIMI_batches\S_BUCKET_batch1_round3_function_core_v1`

注意：
- 外部目录只作为 PDF 读取位置。
- 文本真值仍以 repo 内文件为准。
- repo 默认入口就是本 README，不要把外部目录当成默认入口。
- 若需要直接发给 `Kimi`，优先使用：
  - `S_BUCKET_KIMI_batch1_round3_function_core_direct_message_v1.txt`
