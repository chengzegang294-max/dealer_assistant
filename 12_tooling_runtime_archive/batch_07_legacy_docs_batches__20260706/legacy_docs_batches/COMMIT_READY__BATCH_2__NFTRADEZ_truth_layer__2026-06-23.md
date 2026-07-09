# 提交就绪批次 2 - NFTRADEZ truth layer only - 2026-06-23

## 目标

- Stage only the `NFTRADEZ` truth-layer files that reflect the completed dual-agent intake.
- Keep this batch independent from source-library migration batches.
- Preserve the `method_reference` boundary while landing the imported template layer.

## 精确暂存文件

1. `10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/02_外部视频与方法论参考/Norman_NFTRADEZ_ICT_Trader_NYC/README.md`
2. `10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/02_外部视频与方法论参考/Norman_NFTRADEZ_ICT_Trader_NYC/NFTRADEZ_KIMI_batch_README_v1.md`
3. `10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/02_外部视频与方法论参考/Norman_NFTRADEZ_ICT_Trader_NYC/NFTRADEZ_AGENT_STATUS__2026-06-23.md`
4. `10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/02_外部视频与方法论参考/Norman_NFTRADEZ_ICT_Trader_NYC/NFTRADEZ_KIMI_premarket_template_OUTBOUND__agentB__copy_paste_v1.txt`
5. `10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/02_外部视频与方法论参考/Norman_NFTRADEZ_ICT_Trader_NYC/NFTRADEZ_KIMI_concept_glossary_shrink_v1__imported.md`
6. `10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/02_外部视频与方法论参考/Norman_NFTRADEZ_ICT_Trader_NYC/NFTRADEZ_KIMI_premarket_template_v1__imported.md`

## 保留作上下文的真值文件

- `NFTRADEZ_KIMI_concept_glossary_manifest_v1.tsv`
- `NFTRADEZ_KIMI_concept_glossary_prompt_v1.txt`
- `NFTRADEZ_KIMI_premarket_template_manifest_v1.tsv`
- `NFTRADEZ_KIMI_premarket_template_prompt_v1.txt`
- `NFTRADEZ_KIMI_concept_glossary_direct_message_v2__agentA.txt`
- `NFTRADEZ_KIMI_premarket_template_direct_message_v2__agentB.txt`

## 显式排除项

- all `*_导出.md` source captures
- any other source-library directories
- any source-library migration batches under `01_Kimi拆书待入库`
- `临时粘贴区_外部AI与终端输出.md`

## 为何存在该批次

- It closes the first full `NFTRADEZ` dual-agent intake.
- It lands both imported replies as repo truth.
- It keeps `NFTRADEZ` separate from the much larger source-library migration backlog.

## 建议提交信息

- `docs: import NFTRADEZ premarket template and close dual-agent intake`

## 暂存命令

- Use:
  - `docs/commit_ready_stage_batch_2__NFTRADEZ_truth_layer__2026-06-23.ps1`
  - `docs/commit_ready_batch_2__NFTRADEZ_truth_layer__paths.txt`

## 验证

- Run the script once with `-DryRun`.
- Confirm that only the `6` files above are targeted.
- Confirm that no raw `*_导出.md` files and no other source-library trees enter this batch.
