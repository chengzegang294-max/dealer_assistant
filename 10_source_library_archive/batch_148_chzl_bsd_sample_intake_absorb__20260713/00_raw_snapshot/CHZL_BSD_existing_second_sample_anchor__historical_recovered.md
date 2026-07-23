# CHZL BSD Existing Second Sample Anchor Historical Recovered

更新时间：2026-07-14

- 文件类型：`ARTIFACT`
- 原路径：`02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/chzl_bsd_structure_bundle/auto_series/601991_SH_structure_series_v1.tsv` + `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/watchlist_subset/601991_SH_1d.csv`
- 新路径：`10_source_library_archive/batch_148_chzl_bsd_sample_intake_absorb__20260713/00_raw_snapshot/CHZL_BSD_existing_second_sample_anchor__historical_recovered.md`
- 生成入口：`historical_recovered_runtime_reference`
- 适用对象：`CHZL_BSD`
- 当前作用：说明仓内已存在第二只样本的 auto series 与输入数据锚点
- 证据强度：`historical_recovered`
- 缺口：当前已补第二只样本 seed 与 stub 校验，但仍缺完整结构真值

## 已有锚点

- `601991_SH_1d.csv`
- `601991_SH_structure_series_v1.tsv`
- 第一只样本半自动输出参考：
  - `chzl_bsd_300302_sz_semi_auto_output.json`
- 第二只样本半自动输出：
  - `chzl_bsd_601991_sh_semi_auto_output.json`
- 对应生成入口：
  - `build_chzl_structure_series_v1.py`
  - `run_chzl_bsd_sample_stub_v1.py`

## 当前判断

- 仓内已经证明：
  - 第二只样本的 `auto series` 可以存在
- 仓内还没有证明：
  - 第二只样本的完整结构真值已经形成
- 当前已额外证明：
  - 第二只样本的 `manual seed` 已正式落盘并进入 runtime bundle
  - 第二只样本已能输出 `semi_auto_structure_with_seed_override` 的最小 JSON
- 所以下一刀不再是补 seed 文件，而是决定是否继续补更强校验记录或结构真值增强。
