# Acceptance Outputs

## 用途

- 存放 `run_object_card_minimal_v1.py` 对验收样本的当前终端实跑输出。
- 这些 JSON 都属于当前终端实跑输出，不是历史回收。
- `evidence_mode` 可能是 `hard / weak_manual_seed / semi_auto_structure_with_seed_override`，以索引和文件内容为准，不统一冒充 `hard`。

## 当前范围

- `volfac_300302_sz_1d_output.json`
- `bpb_601991_sh_1d_output.json`
- `ytc_601991_sh_daily_weekly_output.json`
- `chzl_bsd_300302_sz_seed_output.json`
- `chzl_bsd_300302_sz_semi_auto_output.json`
- `voltarget_300302_sz_1d_output.json`
- `period_queen_601991_sh_proxy_output.json`

## 生成入口

- `02_runtime/butler_r0_ohlcv_object_cards/run_object_card_minimal_v1.py`
- `02_runtime/butler_r0_ohlcv_object_cards/run_ytc_daily_weekly_minimal_v1.py`
- `02_runtime/butler_r0_ohlcv_object_cards/run_chzl_bsd_sample_stub_v1.py`
- `02_runtime/butler_r0_ohlcv_object_cards/run_voltarget_minimal_v1.py`
- `02_runtime/butler_r0_ohlcv_object_cards/run_period_queen_proxy_minimal_v1.py`
