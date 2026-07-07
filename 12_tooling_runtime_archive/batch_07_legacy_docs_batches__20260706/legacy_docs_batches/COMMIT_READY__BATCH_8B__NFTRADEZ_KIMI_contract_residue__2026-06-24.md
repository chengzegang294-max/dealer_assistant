# Commit Ready Batch 8B - NFTRADEZ KIMI contract residue - 2026-06-24

## Goal

- stage the remaining `NFTRADEZ` `KIMI` contract residue after `Batch 8A`
- keep this pack limited to the `8` contract files used for `concept_glossary` and `premarket_template`
- make the contract layer repo-first so it no longer defaults to `D:\Stock\cut_file\诺曼NFTRADEZ`

## Exact Files To Stage

- `10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/02_外部视频与方法论参考/Norman_NFTRADEZ_ICT_Trader_NYC/NFTRADEZ_KIMI_concept_glossary_direct_message_v1.txt`
- `10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/02_外部视频与方法论参考/Norman_NFTRADEZ_ICT_Trader_NYC/NFTRADEZ_KIMI_concept_glossary_direct_message_v2__agentA.txt`
- `10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/02_外部视频与方法论参考/Norman_NFTRADEZ_ICT_Trader_NYC/NFTRADEZ_KIMI_concept_glossary_manifest_v1.tsv`
- `10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/02_外部视频与方法论参考/Norman_NFTRADEZ_ICT_Trader_NYC/NFTRADEZ_KIMI_concept_glossary_prompt_v1.txt`
- `10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/02_外部视频与方法论参考/Norman_NFTRADEZ_ICT_Trader_NYC/NFTRADEZ_KIMI_premarket_template_direct_message_v1.txt`
- `10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/02_外部视频与方法论参考/Norman_NFTRADEZ_ICT_Trader_NYC/NFTRADEZ_KIMI_premarket_template_direct_message_v2__agentB.txt`
- `10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/02_外部视频与方法论参考/Norman_NFTRADEZ_ICT_Trader_NYC/NFTRADEZ_KIMI_premarket_template_manifest_v1.tsv`
- `10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/02_外部视频与方法论参考/Norman_NFTRADEZ_ICT_Trader_NYC/NFTRADEZ_KIMI_premarket_template_prompt_v1.txt`
- `docs/COMMIT_READY__BATCH_8B__NFTRADEZ_KIMI_contract_residue__2026-06-24.md`
- `docs/commit_ready_batch_8B__nftradez_kimi_contract_residue__paths.txt`
- `docs/commit_ready_stage_batch_8B__nftradez_kimi_contract_residue__2026-06-24.ps1`

## Included Changes

- `direct_message` files now point to the repo-local `NFTRADEZ` directory
- `manifest_v1.tsv` rows now use repo-local `current_path` values
- `prompt_v1.txt` files stay unchanged and are included as part of the contract set

## Excluded In This Pack

- `NFTRADEZ` export text layer already committed in `Batch 8A`
- `NFTRADEZ_KIMI_*__imported.md`
- `NFTRADEZ_KIMI_*OUTBOUND*`
- `NFTRADEZ_KIMI_batch_README_v1.md`
- `Batch9`
- `Smile_SMC`

## Suggested Commit Message

- `docs: add Batch 8B NFTRADEZ KIMI contract residue`

## Stage Command

- use:
  - `docs/commit_ready_stage_batch_8B__nftradez_kimi_contract_residue__2026-06-24.ps1`
  - `docs/commit_ready_batch_8B__nftradez_kimi_contract_residue__paths.txt`
