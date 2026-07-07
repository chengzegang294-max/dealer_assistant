# NFTRADEZ KIMI Premarket Template v1 Imported

## External Reply

- External saved file: `D:\Stock\cut_file\诺曼NFTRADEZ\NFTRADEZ_premarket_template_v1.md`
- Source handoff mode: `Agent B`
- Import basis:
  - pasted reply in `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\临时粘贴区_外部AI与终端输出.md`
  - saved external markdown file under `D:\Stock\cut_file\诺曼NFTRADEZ`

## Scope

- Strictly limited to the `4` manifest objects:
  - `NFTZ_P001`
  - `NFTZ_P002`
  - `NFTZ_P003`
  - `NFTZ_P004`
- No concept glossary objects were mixed in.
- No extra directories, extra videos, trade calls, or win-rate claims were added.

## Output Contract Confirmed

- Each object keeps:
  - `object_id`
  - `template_contribution`
- Final merged output keeps:
  - `premarket_template_v1`
- The merged template explicitly includes:
  - `bias_check`
  - `dol_check`
  - `timeframe_alignment`
  - `if_then_branches`
  - `do_not_trade_when`
  - `event_day_exception`

## Imported Template Boundaries

- `bias_check`
  - Keeps `交付源头检查 -> FG 尊重/无视过滤器 -> 高时间周期确认` order.
  - Keeps the downgrade path: `日线 -> 4H -> 1H`.
  - If bias is still unclear after downgrade, the day becomes `停止交易`.
- `dol_check`
  - Keeps `Bias` and `DOL` explicitly separated.
  - `Bias = 方向`, `DOL = 目的地`.
  - `Bias != DOL` is treated as `分歧状态`, not as a direct reversal call.
- `timeframe_alignment`
  - Keeps fixed pairing logic across trading timeframes.
  - Low timeframe signals must be checked against higher-timeframe `FVG / FG` context.
- `if_then_branches`
  - Keeps `统一状态 / 分歧状态 / Judas Swing narrative_only` split.
  - Does not allow direct conversion of narrative branches into hard execution signals.
- `do_not_trade_when`
  - Explicitly lists the forced no-trade states:
    - no clear bias
    - no clear DOL
    - long-lasting bias/DOL divergence
    - severe timeframe conflict
    - event day without pre-plan
    - only one timeframe looks clean while the others conflict
- `event_day_exception`
  - Keeps `FOMC` event-day handling inside `AAMD = Accumulation -> Manipulation -> Distribution`.
  - Explicitly forbids generalizing this time segmentation to normal trading days.

## Imported Role Summary

- `NFTZ_P001`
  - contributes the multi-timeframe premarket sequencing and `Judas Swing` narrative branch
- `NFTZ_P002`
  - contributes the strict split between `Daily Bias` and `DOL`
- `NFTZ_P003`
  - contributes the `If-Then` branch structure and `Bias/DOL` convergence vs divergence handling
- `NFTZ_P004`
  - contributes the event-day `AAMD` structure and post-news waiting discipline

## Current Status

- Current import status: `IMPORTED__KIMI_PREMARKET_TEMPLATE_V1_OK`
- Current evidence status: `TEXT_EVIDENCE_IMPORTED__NO_OCR`
- Current repository role: `method_reference`
- Current boundary:
  - Keep as premarket template / event-day reference / discipline-support layer.
  - Do not upgrade to validated quant objects.
  - Do not convert to direct execution signals.

## Next Step

- With both replies now present, `NFTRADEZ` has completed the first dual-agent intake:
  - glossary layer
  - premarket template layer
- The next optional extraction, if reopened later, should stay inside:
  - event-day template refinement
  - discipline / do-not-trade rules
  - execution grading language
