# A5 首张真实案例采样记录卡 sample_date 确认页

更新时间：2026-07-27

## 一、这页用途

- 本页只做：
  - 正式确认首张真实案例采样记录卡的
    `sample_date`
  - 同时把
    `sample_date`
    和
    `occurredAt`
    的证据层级拆开

## 二、当前确认结果

- 当前正式确认：
  - `sample_date = 2026-07-20`

## 三、当前确认依据

### 3.1 三张对象卡共同日期

- 当前三张对象卡都明确写有：
  - `date_tag : 2026-07-20`

- 对应文件：
  - `03_quantize/batch149_object_card_HYDB行业对比__20260720.md`
  - `03_quantize/batch149_object_card_沪深涨跌停__20260720.md`
  - `03_quantize/batch149_object_card_上榜资金__20260720.md`

### 3.2 事件层日期提取路径

- `00_raw_snapshot/pages/市场情绪.html`
  当前明确存在：
  - `tt = data2.match(/"date":"(\\S*)","time"/)[1];`
  - `dt = tt;`

- 这说明：
  - 原始页面事件流本身就从接口返回里提取了
    `date`
  - 对象卡里的
    `date_tag`
    不是无来源悬空字段

### 3.3 字段桥合同

- `batch149_formula_semantics_to_batch1_field_bridge_v1.md`
- `batch149_six_card_event_field_bundle_v1.md`

- 这两页共同冻结了：
  - `occurredAt`
    属于事件层字段
  - 且当前口径是：
    `用当次触发时间`

## 四、为什么现在可以确认 sample_date

- 当前可以确认
  `sample_date = 2026-07-20`
  的原因是：
  1. 三张对象卡已有共同日期
  2. 原始页面存在事件层日期提取逻辑
  3. 首张记录卡当前要确认的是
     `案例日期`
     而不是
     `精确触发时刻`

## 五、为什么还不能确认精确 occurredAt

- 当前还不能确认的是：
  - 精确到时刻的
    `occurredAt`

- 原因是：
  1. 字段桥和对象卡都只保留了
     `当次触发时间`
     这类占位说明
  2. 当前仓内还没把该首张案例的具体
     `hh:mm:ss`
     或事件时点单独落盘

## 六、主负责人裁决

- 当前正式裁决为：
  1. 首张真实案例采样记录卡的
     `sample_date`
     现正式冻结为：
     `2026-07-20`
  2. 当前不再把
     `sample_date`
     视作缺口
  3. 当前若仍有时间相关缺口，
     仅限于：
     `事件层精确 occurredAt`

## 七、一句话口径

- 当前首张真实案例采样记录卡的
  `sample_date`
  已正式确认是
  `2026-07-20`
  ；
  还未补齐的只剩事件层精确触发时刻，而不是案例日期本身。
