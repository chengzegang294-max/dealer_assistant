# Artifact Note Contract

## 目的

- 这份合同专门约束新仓库里的运行产物、生成脚本和备注说明。
- 目标是避免重演旧仓库那种“有很多 `csv / py / log / htm`，但不知道谁生成、谁维护、现在有什么用”的混乱状态。

## 适用范围

- `02_runtime` 下的新批次目录
- `artifacts\csv`
- `artifacts\log`
- `artifacts\tester_report`
- 与这些产物直接对应的：
  - `py`
  - `mq4 / mq5`
  - `ex4 / ex5`
  - `ini`
  - `README`
  - `EXECUTION_CARD`
  - `ARTIFACT_INDEX`

## 新仓库里的硬规则

1. 任何一批运行产物进入新仓库，必须同时有备注说明文件。
2. 任何一份 `csv / log / report`，必须能回指到生成入口。
3. 任何历史回收证据，都必须明确写成 `historical_recovered`。
4. 任何找不到来源或用途的文件，不直接放正式层，先留旧仓库或放 `99_inbox`。
5. 任何批次目录都不能只堆结果文件，不写入口卡。

## 每批至少要有的说明文件

- `README.md`
- `BATCH_*_EXECUTION_CARD.md`
- `BATCH_*_ARTIFACT_INDEX*.md`

没有这三类文件之一，就不算完整批次。

## 每份产物至少要写清的字段

- `producer`
  - 谁生成的：脚本、EA、probe、指标、配置
- `source_path`
  - 原始路径
- `repo_path`
  - 新仓库落点
- `scope`
  - 属于哪个对象、家族或批次
- `evidence_mode`
  - `fresh_run / historical_recovered / weak_evidence / archive_only`
- `status`
  - `pending / recovered / verified / weak / deprecated`
- `current_role`
  - 这个文件现在是：
    - 输入
    - 输出
    - 历史证据
    - 说明文件
    - 仅归档保留

## 生成脚本也必须写清

任何 `py / mq4 / mq5 / ini` 如果被纳入新仓库，至少要在备注里说明：

- 它生成什么
- 它不生成什么
- 默认输出目录
- 对应哪一批产物
- 当前是不是默认入口

## 不允许出现的情况

- 有 `csv`，但不知道对应哪个脚本
- 有 `py`，但不知道输出文件长什么样
- 有 `report`，但不知道属于哪次 probe
- 一个目录里混放多类无说明结果
- 历史证据和最新证据不区分

## 当前建议口径

- 英文文件名优先用于：
  - 根目录协调文件
  - 合同文件
  - 批次入口文件
- 中文正文优先用于：
  - 备注说明
  - 边界裁决
  - 当前作用

## 当前执行方式

- 先写批次入口，再纳入产物
- 先写索引备注，再承认“这个结果有效”
- 找到旧产物时，先标 `historical_recovered`，再决定是不是当前硬证据
- 找不到用途说明时，不强行猜测

## 一句话记忆

- 新仓库不是结果堆放区；每份结果都必须带着“它是谁、怎么来的、现在干什么”的备注一起进入。
