本目录用于存放 A1 / A3 / A4 等删源仍可用的切割产物（md）。

当前稳定入口：

- A1：`01_A1_cutpack_v2_final/`
- A3-C1：`02_A3C1_cutpack_v2_final/`
- A3 extra：`03_A3_extra_cutpack_v2_final/`
- A4：`04_A4_cutpack_v2_final/`

当前非稳定入口 / 历史副本：

- 根层 4 份 A4 md：重复副本，不再作为稳定入口。
- `01_A1_cutpack_v2/`：历史目录，不再作为 A1 正式入口。
- `02_A3C1_cutpack_v2/`：历史目录，不再作为 A3-C1 正式入口。

索引：

- `manifest_v2.tsv`
- `01_A1_cutpack_v2_final/manifest_v2.tsv`
- `02_A3C1_cutpack_v2_final/manifest_v2.tsv`
- `03_A3_extra_cutpack_v2_final/manifest_v2.tsv`
- `04_A4_cutpack_v2_final/manifest_v2.tsv`

说明：

- A1 当前正式版以 `01_A1_cutpack_v2_final` 中的 r2 组为准。
- A4 当前正式版只认 `04_A4_cutpack_v2_final`；`Quantitative_Trading` 以 `v2_retry_r2` 为准。
- 后续若做 freeze / archive，应优先处理根层 A4 重复副本与旧版目录。

freeze / archive 说明：

- 以下根层 A4 md 当前视为重复副本，不再作为稳定入口：
  - `CUTPACK__A4__AFML__v2.md`
  - `CUTPACK__A4__Algorithmic_Trading__v2.md`
  - `CUTPACK__A4__Quantitative_Trading__v2_retry.md`
  - `CUTPACK__A4__Successful_Algorithmic_Trading__v2_retry.md`
- 当前动作：保留，不删除。
- 后续动作：若开始统一归档，优先将这 4 份根层副本移入历史层，稳定入口继续只认 `04_A4_cutpack_v2_final/`。
