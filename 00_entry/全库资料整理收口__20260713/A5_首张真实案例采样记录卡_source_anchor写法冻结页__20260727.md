# A5 首张真实案例采样记录卡 source_anchor 写法冻结页

更新时间：2026-07-27

## 一、这页用途

- 本页只做：
  - 把首张真实案例采样记录卡当前可用的 `source_anchor` 写法正式冻结
  - 避免后续首张记录卡再临时改写来源字段

## 二、当前 source_anchor 怎么分层写

- 当前建议固定写成两段：

1. `batch_source_anchor`
2. `object_source_anchor`

- 当前不建议只写一个合并长句，
  因为这样会把：
  - 批次来源
  - 对象样本来源
  混成一层

## 三、当前 batch_source_anchor 固定写法

- 当前固定写法建议为：

```text
batch_source_anchor:
- 10_source_library_archive/batch_149_tdx_custom_terminal_external_folder_absorb__20260719/README.md
- 10_source_library_archive/batch_149_tdx_custom_terminal_external_folder_absorb__20260719/provenance.md
- 10_source_library_archive/batch_149_tdx_custom_terminal_external_folder_absorb__20260719/BATCH_149_EXECUTION_CARD.md
```

## 四、当前 object_source_anchor 固定写法

- 当前固定写法建议为：

```text
object_source_anchor:
- A5_代表性可编辑指标源码导出清单与要求__20260722.md
- A5_截图区五任务首批三条双证据吸收页__20260723.md
- A5_HYDB行业对比职责切换与典型失效样式细化页__20260727.md
- A5_沪深涨跌停职责切换与典型失效样式细化页__20260727.md
- A5_上榜资金职责切换与典型失效样式细化页__20260727.md
```

## 五、当前首张记录卡里怎么用

- 当前首张记录卡若先不写 `sample_date`，
  仍可以先把 `source_anchor` 字段按上面固定格式预留好

- 这意味着：
  - `source_anchor`
    当前已经可冻结
  - `sample_date`
    继续保持
    `still_need_evidence`

## 六、当前禁止写法

- 当前禁止写成：
  - `source_anchor: batch_149`
  - `source_anchor: 截图区五任务`
  - `source_anchor: 见上文`

- 原因是：
  - 太粗
  - 不可回查
  - 不够正式

## 七、主负责人裁决

- 当前正式裁决为：
  1. 首张真实案例采样记录卡的 `source_anchor` 写法已经正式冻结
  2. 当前剩余唯一硬缺口继续维持为：
     `sample_date`
  3. 后续若要真正落首张记录卡，
     优先补时间锚点，
     不再重定来源写法

## 八、一句话口径

- 当前首张真实案例采样记录卡的 `source_anchor` 已经可以正式写死，
  后续真正落卡时，
  不再缺“来源怎么写”，只缺“时间写哪一条”。
