# 外部吸收与回收提升主题入口 v1

## 适用问题

- 想看外部文件夹吸收批里，哪些内容已经被对象化或提升成 runtime 入口
- 想区分 `raw snapshot / absorb index / quantize / runtime`
- 想知道 `batch_110` 该从哪里开始看

## first-hop 入口

- `../batch_110_external_folder_absorb__20260708/README.md`

## 最顺阅读顺序

- 第一步：
  - 先看 `../batch_110_external_folder_absorb__20260708/01_index/family_entry_map_v1.tsv`
- 第二步：
  - 若想看吸收索引与原路径映射，进入 `02_absorb_index/`
  - 若想看已提升代码与对象化入口，进入 `03_quantize/promoted_code_from_raw_snapshot/README.md`
  - 若想看回收的运行时证据，进入 `04_runtime/promoted_from_raw_snapshot/README.md`
- 第三步：
  - 只有在需要回看原样快照时，再进入 `00_raw_snapshot/`

## 当前边界

- 当前主题入口主要服务：
  - 外部材料吸收到来源层后的导航
  - raw snapshot 向 quantize / runtime 的提升路线
- 当前不承担：
  - 直接替代对象目录或 runtime 目录的正式入口

## 回链

- 来源库根入口：
  - `../README.md`
- 批次家族入口：
  - `../batch_110_external_folder_absorb__20260708/01_index/family_entry_map_v1.tsv`
