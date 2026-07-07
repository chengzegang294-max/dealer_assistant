# NFTRADEZ KIMI Concept Glossary Shrink v1 Imported

## External Reply

- External saved file: `D:\Stock\cut_file\诺曼NFTRADEZ\NFTRADEZ_concept_glossary_shrink_v1.md`
- Source handoff mode: `Agent A`
- Import basis: pasted reply summary in `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\临时粘贴区_外部AI与终端输出.md`

## Scope

- Strictly limited to the `6` manifest objects:
  - `NFTZ_G001`
  - `NFTZ_G002`
  - `NFTZ_G003`
  - `NFTZ_G004`
  - `NFTZ_G005`
  - `NFTZ_G006`
- No extra directories, extra videos, trading advice, or win-rate claims were added.

## Output Contract Confirmed

- Each object keeps:
  - `plain_definition`
  - `core_mechanics`
  - `must_have_conditions`
  - `invalid_when`
  - `confusable_with`
  - `best_role`
- Final output also includes:
  - `glossary_crosswalk`

## Imported Boundaries

- `NFTZ_G002`
  - `BOS` keeps the `实体收盘确认` boundary.
  - Must not be confused with a simple `Liquidity Sweep`.
- `NFTZ_G004`
  - Isolated `FVG` is treated as noise.
  - Valid use requires `流动性清扫 + 结构转变 + Kill Zone` background.
- `NFTZ_G005`
  - `OB` keeps the three-step boundary: `流动性清扫 -> Displacement -> 50% 中点验证`.
  - Must not label any last candle as `OB`.
- `NFTZ_G006`
  - `SMT` is only a `偏见工具 / 预警层`.
  - Must wait for `MSS + Displacement` confirmation and is not a direct entry signal.

## Crosswalk Imported

- Natural learning order:
  - `NFTZ_G001 -> NFTZ_G002 -> NFTZ_G003 -> NFTZ_G004 -> NFTZ_G005 -> NFTZ_G006`
- Confusion handling:
  - `5` confusion pairs were explicitly collected in `glossary_crosswalk`.
- Current role summary:
  - All `6` objects are marked as `不能直接入场`.

## Current Status

- Current import status: `IMPORTED__KIMI_GLOSSARY_SHRINK_SUMMARY_OK`
- Current evidence status: `TEXT_EVIDENCE_IMPORTED__NO_OCR`
- Current repository role: `method_reference`
- Current boundary:
  - Keep as glossary / explanation / bias-support layer.
  - Do not upgrade to validated quant objects.
  - Do not convert to direct execution signals.

## Next Step

- Wait for `Agent B` to return `premarket_template`.
- After both replies are present, merge them back into:
  - glossary layer
  - premarket template layer
  - event-day / discipline template candidates
