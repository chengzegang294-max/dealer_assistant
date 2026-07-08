# Batch 110 External Folder Absorb

更新时间：2026-07-08

## 批次目标

- 把外部文件夹 `E:\downloads\Desktop\找系统\特征` 作为“一次性吸收材料”纳入 repo 可追溯链路：来源快照 -> 吸收索引 -> 可量化对象/规则 -> 运行时/验收 -> 冻结总结层。

## 收口裁决（2B）

- 外部快照只作为阶段性追溯位，不作为长期默认入口。
- 吸收完成后，保留：
  - `02_absorb_index/`：可检索索引与证据锚点
  - `03_quantize/`：对象卡/规则壳/字段合同
  - `04_runtime/`：最小可复现脚本与样本（必要时迁入 `02_runtime` / `12_tooling_runtime_archive`）
- 可删除或降级为 `ARCHIVE_ONLY`：
  - `00_raw_snapshot/`（若确认所有结论已可追溯回链）

## 批次结构

- `00_raw_snapshot/`：外部文件夹原样快照（阶段性）
- `01_kimi_outputs/`：Kimi 或用户想法生成的衍生产物（带 provenance）
- `02_absorb_index/`：对象卡到资源的索引/筛选与证据锚点
- `03_quantize/`：对象化规则候选与字段化落点
- `04_runtime/`：最小可跑与验收

## 当前入口

- `01_kimi_outputs/TRADING_BLOGGER_REFERENCE_v1.0.md`
- `manifest_v1.tsv`
- `provenance.md`
