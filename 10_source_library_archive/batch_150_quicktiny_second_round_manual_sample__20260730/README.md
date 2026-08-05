# batch_150 quicktiny second round manual sample

更新时间：2026-07-30

## 作用

- 本批次只收：
  - A5 真实案例采样第二轮所需的新日期人工补证截图
- 当前用途是：
  - 为 `sample_date=2026-07-29` 提供可回链的最小页面级锚点
  - 让第二轮不再继续卡在“新日期样本是否存在”

## 当前批次内容

- 已正式吸收：
  1. `00_raw_snapshot/user_screenshots/2026-07-29__市场情绪总览.png`
  2. `00_raw_snapshot/user_screenshots/2026-07-29__市场宽度涨停跌停.png`
  3. `00_raw_snapshot/user_screenshots/2026-07-29__龙虎榜异动资金.png`
  4. `00_raw_snapshot/user_screenshots/2026-07-29__题材中心.png`
  5. `00_raw_snapshot/user_screenshots/2026-07-29__看盘工作台.png`
  6. `00_raw_snapshot/user_screenshots/2026-07-29__涨停.png`
  7. `00_raw_snapshot/user_screenshots/2026-07-29__炸板.png`
  4. `00_raw_snapshot/formula_shells/HYDB行业对比__formula_shell.(png/txt)`
  5. `00_raw_snapshot/formula_shells/ZSDB指数对比__formula_shell.(png/txt)`

- 当前未随文件一并入库、但已在本轮会话中人工核验的证据：
  1. `打板/封板强弱` 截图

## 当前判断

- 这批截图已经足以支撑：
  1. 新日期锚点确认
  2. `市场情绪` 总览回链
  3. `沪深涨跌停` 背景对象回链
  4. `上榜资金` 触发对象回链
  5. `打板资金`
     从“文件待落盘”
     推进为“候选页对已吸收”
  6. `HYDB`
     从“只有公式壳”
     推进为“有同日题材背景候选页”

- 当前新增吸收的公式壳已经足以支撑：
  1. `HYDB行业对比`
     对象本体继续保留为已定义状态
  2. `ZSDB指数对比`
     对象本体继续保留为已定义状态
  3. 第二轮当前真正缺的是：
     - 同日输入
     而不是对象本身不存在

- `打板/封板强弱` 这条证据当前已实质成立，
  但仍需要在后续回合把截图文件补落到仓内正式路径，
  避免长期只停留在会话附件层。

## 入口文件

- `provenance.md`
- `manifest_v1.tsv`
- `03_quantize/README.md`
- `03_quantize/batch150_page_to_second_round_object_bridge_v1.md`

## 一句话口径

- 本批次是第二轮新日期样本的最小人工补证吸收包，
  当前先把 `2026-07-29` 的页面级锚点立住，
  再继续推进第二轮三张最小代表卡。
