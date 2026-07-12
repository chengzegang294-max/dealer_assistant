# Source Library Archive

## 用途

- 这里放按批次筛选后迁入的新来源库材料。
- 这里不是 `10_来源库_SOURCE_LIBRARY` 的镜像副本。

## 默认入口

- 根层总导航：
  - `archive_batch_index_v1.tsv`

## 三级导航

- 必看：
  - `batch_01_youzi_truth_anchors/README.md`
  - `batch_09_legacy_source_library_alignment__20260707/README.md`
  - `archive_batch_index_v1.tsv`
- 可选看：
  - `batch_100_non_kimi_public_methods_boundary__20260707/README.md`
  - `batch_101_non_kimi_atomic_rules_boundary__20260707/README.md`
  - `batch_107_non_kimi_public_batch9_bundle__20260707/README.md`
  - `batch_108_non_kimi_nftradez_method_bundle__20260707/README.md`
  - `batch_109_non_kimi_smile_smc_method_bundle__20260707/README.md`
  - `batch_110_external_folder_absorb__20260708/README.md`
  - `batch_120_tools_workspace_absorb__20260709/README.md`
  - `batch_131_trae_system_selected_absorb__20260709/README.md`
  - `batch_140_tushare_tdx_data_source_absorb__20260712/README.md`
- `archive_only / staging / raw_truth_side`：
  - `batch_132_trae_system_raw_snapshot_batch09_absorb__20260709/README.md`
  - `mirror_kimi_inbox/README_放这里.md`
  - `mirror_kimi_inbox/GROUP_08_A股量化_数据研究/GROUP_08_短索引入口_v1.md`
  - `raw_assets/README.md`

## 允许进入

- 对当前活跃对象有直接参考价值的来源材料
- 已确认非乱码、非重复、非临时副本的材料
- 已写清原路径与迁入理由的材料

## 不允许进入

- 整包来源库复制
- 只是“可能以后有用”的材料
- 已被活跃对象目录完全吸收的重复副本
- 乱码文件、损坏文件、无来源说明副本

## 当前状态

- 当前仍不批量迁入旧来源库内容。
- 当前已形成多批次归档：
  - `batch_01_youzi_truth_anchors` 作为首批真值锚点
  - `batch_09 / batch_100 / batch_101` 继续承担历史对齐与边界批职责
  - `batch_107 / batch_108 / batch_109` 已形成公开资料与方法参考稳定 bundle
  - `batch_110 / batch_120 / batch_131 / batch_132 / batch_140` 继续承接外部吸收批、工具工作区回收批、系统材料与数据源吸收批
- `batch_01_youzi_truth_anchors` 仍是首批锚点，不再是唯一批次。
- 后续每一批迁入都要先完成四分流，再进入本层。

## 你该怎么进

- 想先看来源层全局结构：
  - 先看 `archive_batch_index_v1.tsv`
- 想找稳定真值锚点与历史对齐边界：
  - 先看 `batch_01` 与 `batch_09`
- 想看较新的吸收批：
  - 先看对应批次 README，再看批次内的 `family_entry_map_v1.tsv`
- 想看待入库资料而不是正式来源层：
  - 先去 `mirror_kimi_inbox/README_放这里.md`
  - 若当前就是 A 股量化资料，直接进 `GROUP_08_短索引入口_v1.md`
- 想找原件真值：
  - 直接去 `raw_assets/README.md`

## 批次分组

- `truth_anchor`
  - 首批真值锚点；优先看 `batch_01`
- `alignment_boundary`
  - 历史来源库对齐、边界判断、最小搬迁判断；优先看 `batch_09 / batch_100 / batch_101`
- `stable_bundle`
  - 已从边界批中提升出来、可以直接作为方法参考入口的稳定包；优先看 `batch_107 / batch_108 / batch_109`
- `absorb_batch`
  - 新近吸收的外部材料、系统材料与工作区回收批；优先看 `batch_110 / batch_120 / batch_131 / batch_140`
- `archive_only_absorb`
  - 只保留追溯价值，不作为 first-hop 默认入口；当前看 `batch_132`
- `staging_area / raw_truth_side`
  - `mirror_kimi_inbox` 是待入库与中转侧
  - `raw_assets` 是原件真值侧

## 批次记录模板

- 批次名：
- 原路径：
- 新路径：
- 当前关联对象：
- 去重结论：
- 迁入理由：
