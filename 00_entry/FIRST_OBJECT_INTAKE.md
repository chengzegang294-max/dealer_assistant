# First Object Intake

## 目的

- 这份文件定义 `DY-R1 / KD_MTF_P0` 作为第一个活跃对象时，进入 `trading_assistant` 的最小准入规则。
- 目标不是复制旧目录，而是先把“最小活跃对象包”定义清楚，再按合同纳入。

## 对象定义

- 对象名：`DY-R1 / KD_MTF_P0`
- 当前角色：
  - 多周期 KD 的第一批活跃运行时对象
  - 具备文档入口、参数合同、样本、append stub、runtime 产物边界
- 迁入目标：
  - 让它在新目录中成为一个可独立维护、可继续收口、可继续扩展的对象包

## 最小准入原则

- 只迁当前活跃运行真正需要的最小集
- 只保留一个活跃维护位置
- 先保证对象包内部自洽，再考虑补充背景材料
- 背景来源、历史备份、冻结总结默认不进入第一刀

## 第一刀建议迁入

- 入口文档：
  - `directory_index_card`
  - `quick_entry_card`
  - `object_responsibility_card`
  - `runtime_notes`
  - `runtime_gaps`
  - `runtime_append_protocol`
  - `runtime_append_acceptance`
  - `real_input_mapping_draft`
  - `b_blocker_note`
- 运行时对象：
  - `kd_mtf_p0_runtime_append_stub_v1.py`
  - `kd_mtf_p0_runtime_params_template_v1.json`
  - `kd_mtf_p0_fields_runtime_header_v1.txt`
  - `kd_mtf_p0_fields_runtime_v1.csv`
- 样本对象：
  - `real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `real_input_samples\kd_mtf_p0_proof_output_v1.csv`
  - 上游 canonical bars 的最小本地副本 `n01_first_real_input_bars_v1.csv`

## 第一刀不迁

- `10_来源库_SOURCE_LIBRARY\` 整包
- `11_冻结总结层_FROZEN_SUMMARIES\` 整包
- `12_工具运行时_TOOLING_RUNTIME\` 其他无关对象
- 历史损坏备份、乱码文件、临时恢复副本
- 与 `DY-R1 / KD_MTF_P0` 无直接执行关系的历史说明材料
- 只为“也许以后有用”而预先打包的资料

## 迁入后的目标落位

- `01_active_objects`
  - 放对象级入口与职责说明
- `02_runtime`
  - 放脚本、参数、表头、runtime csv、proof 样本、上游样本
- `03_docs`
  - 放该对象的活跃长文、阶段记录、阻塞说明

## 必须避免

- 把旧目录原样整包复制进来
- 让新目录同时依赖多个旧绝对路径
- 让同一个对象同时在旧目录和新目录并行扩写
- 把对象背景材料误当成运行时必需材料

## 准入前确认

1. 新目录中的 `DY-R1 / KD_MTF_P0` 是否将成为唯一活跃维护位置？
2. 是否只迁最小活跃对象包，而不是旧目录全量复制？
3. 是否先改成本地相对结构，再允许继续执行？
4. 是否明确旧目录只保留为历史冻结对照？

## 当前建议裁决

- 当开始迁入 `DY-R1 / KD_MTF_P0` 时：
  - 直接按“最小活跃对象包”进入新目录
  - 不再延续旧目录的混合结构
  - 不把来源库和冻结层一起带入第一刀
