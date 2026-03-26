# API 参考文档

本文档列出百度 OCR 技能支持的所有 115+ API 接口。

## 目录

- [OCR 类](#ocr-类)
- [通用文字识别](#通用文字识别)
- [网络图片](#网络图片)
- [身份证](#身份证)
- [银行卡](#银行卡)
- [营业执照](#营业执照)
- [驾驶证/行驶证](#驾驶证行驶证)
- [票据识别](#票据识别)
- [护照/通行证](#护照通行证)
- [名片/证件](#名片证件)
- [医疗票据](#医疗票据)
- [文档表格](#文档表格)
- [合同比对](#合同比对)
- [企业核验](#企业核验)
- [教育类](#教育类)
- [其他专业接口](#其他专业接口)
- [智能结构化](#智能结构化)
- [iOCR](#iocr)
- [其他](#其他)

---

## OCR 类

### 构造函数

```python
from scripts.ocr import OCR

ocr = OCR(use_fallback=True, api_key=None, secret_key=None)
```

**参数**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `use_fallback` | `bool` | `True` | 百度OCR失败时是否使用EasyOCR本地兜底 |
| `api_key` | `str` | `None` | 百度API Key（默认从环境变量/配置读取） |
| `secret_key` | `str` | `None` | 百度Secret Key（默认从环境变量/配置读取） |

### recognize 方法

```python
result = ocr.recognize(
    image=None,
    image_url=None,
    api="general_basic",
    fallback=None,
    **kwargs
)
```

**参数**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `image` | `str` | `None` | 图片路径或Base64字符串 |
| `image_url` | `str` | `None` | 图片URL（二选一） |
| `api` | `str` | `"general_basic"` | API名称 |
| `fallback` | `bool` | `None` | 是否启用兜底（None使用默认值） |
| `**kwargs` | - | - | 特定API的额外参数 |

**返回**：`Dict[str, Any]` - 百度OCR格式的识别结果

---

## 通用文字识别

### general

通用文字识别（含位置信息）

```python
result = ocr.recognize(image="photo.jpg", api="general")
```

**额外参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `detect_direction` | `bool` | 是否检测图像朝向 |
| `recognize_granularity` | `str` | 识别粒度：`big`（词级）/ `small`（字符级） |
| `language_type` | `str` | 语言类型：CHN_ENG/ENG/POR/FRE/GER/ITA/SPA/MAL/JPN/KOR |
| `detect_language` | `bool` | 是否检测语言 |

---

### general_basic

通用文字识别（基础版，不含位置）

```python
result = ocr.recognize(image="photo.jpg", api="general_basic")
```

**额外参数**：同 `general`

---

### accurate

高精度文字识别（含位置）

```python
result = ocr.recognize(image="photo.jpg", api="accurate")
```

**额外参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `detect_direction` | `bool` | 是否检测图像朝向 |

---

### accurate_basic

高精度文字识别（基础版）

```python
result = ocr.recognize(image="photo.jpg", api="accurate_basic")
```

---

## 网络图片

### webimage

网络图片文字识别（含位置）

```python
result = ocr.recognize(image_url="https://example.com/image.jpg", api="webimage")
```

**额外参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `detect_direction` | `bool` | 是否检测图像朝向 |

---

### webimage_loc

网络图片文字识别（与 webimage 相同）

```python
result = ocr.recognize(image_url="https://example.com/image.jpg", api="webimage_loc")
```

---

## 身份证

### idcard

身份证识别

```python
# 正面
result = ocr.recognize(
    image="idcard_front.jpg",
    api="idcard",
    id_card_side="front"
)

# 反面
result = ocr.recognize(
    image="idcard_back.jpg",
    api="idcard",
    id_card_side="back"
)
```

**额外参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id_card_side` | `str` | 是 | `front`（正面）/ `back`（背面） |
| `detect_risk` | `bool` | 否 | 是否检测身份证风险（照片翻拍/复印件等） |

---

### multi_idcard

多张身份证识别

```python
result = ocr.recognize(image="multiple_idcards.jpg", api="multi_idcard")
```

---

## 银行卡

### bankcard

银行卡识别

```python
result = ocr.recognize(image="bankcard.jpg", api="bankcard")
```

---

## 营业执照

### business_license

营业执照识别

```python
result = ocr.recognize(image="license.jpg", api="business_license")
```

---

## 车牌

### license_plate

车牌识别

```python
result = ocr.recognize(image="car.jpg", api="license_plate")
```

---

## 驾驶证/行驶证

### driving_license

驾驶证识别

```python
result = ocr.recognize(image="license.jpg", api="driving_license")
```

---

### vehicle_license

行驶证识别

```python
result = ocr.recognize(image="vehicle.jpg", api="vehicle_license")
```

---

### vehicle_invoice

机动车销售发票识别

```python
result = ocr.recognize(image="vehicle_invoice.jpg", api="vehicle_invoice")
```

---

### vehicle_certificate

车辆合格证识别

```python
result = ocr.recognize(image="certificate.jpg", api="vehicle_certificate")
```

---

## 票据识别

### receipt

通用票据识别

```python
result = ocr.recognize(image="receipt.jpg", api="receipt")
```

**额外参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `recognize_granularity` | `str` | 识别粒度 |

---

### vat_invoice

增值税发票识别

```python
result = ocr.recognize(image="invoice.jpg", api="vat_invoice")
```

---

### taxi_receipt

出租车票识别

```python
result = ocr.recognize(image="taxi.jpg", api="taxi_receipt")
```

---

### train_ticket

火车票识别

```python
result = ocr.recognize(image="train.jpg", api="train_ticket")
```

---

### air_ticket

机票识别

```python
result = ocr.recognize(image="airline.jpg", api="air_ticket")
```

---

### quota_invoice

定额发票识别

```python
result = ocr.recognize(image="quota.jpg", api="quota_invoice")
```

---

### invoice

发票识别（通用）

```python
result = ocr.recognize(image="invoice.jpg", api="invoice")
```

---

### bus_ticket

汽车票识别

```python
result = ocr.recognize(image="bus.jpg", api="bus_ticket")
```

---

### toll_invoice

过路过桥费发票识别

```python
result = ocr.recognize(image="toll.jpg", api="toll_invoice")
```

---

### ferry_ticket

船票识别

```python
result = ocr.recognize(image="ferry.jpg", api="ferry_ticket")
```

---

### used_vehicle_invoice

二手车发票识别

```python
result = ocr.recognize(image="used_car.jpg", api="used_vehicle_invoice")
```

---

### bank_receipt_new

银行回单识别

```python
result = ocr.recognize(image="receipt.jpg", api="bank_receipt_new")
```

---

### bank_receipt_new_pro

银行回单识别（高级版）

```python
result = ocr.recognize(image="receipt.jpg", api="bank_receipt_new_pro")
```

---

### multiple_invoice

多张票据识别

```python
result = ocr.recognize(image="invoices.jpg", api="multiple_invoice")
```

---

## 护照/通行证

### passport

护照识别

```python
result = ocr.recognize(image="passport.jpg", api="passport")
```

---

### overseas_passport

往来港澳台通行证识别

```python
result = ocr.recognize(image="pass.jpg", api="overseas_passport")
```

---

### HK_Macau_exitentrypermit

港澳通行证识别

```python
result = ocr.recognize(image="hk_permit.jpg", api="HK_Macau_exitentrypermit")
```

---

### taiwan_exitentrypermit

台湾通行证识别

```python
result = ocr.recognize(image="tw_permit.jpg", api="taiwan_exitentrypermit")
```

---

### hk_macau_taiwan_exitentrypermit

港澳台通行证识别（统一）

```python
result = ocr.recognize(image="permit.jpg", api="hk_macau_taiwan_exitentrypermit")
```

---

## 名片/证件

### business_card

名片识别

```python
result = ocr.recognize(image="card.jpg", api="business_card")
```

---

### social_security_card

社保卡识别

```python
result = ocr.recognize(image="social.jpg", api="social_security_card")
```

---

### household_register

户口本识别

```python
result = ocr.recognize(image="household.jpg", api="household_register")
```

---

### birth_certificate

出生证明识别

```python
result = ocr.recognize(image="birth.jpg", api="birth_certificate")
```

---

### marriage_certificate

结婚证识别

```python
result = ocr.recognize(image="marriage.jpg", api="marriage_certificate")
```

---

### divorce_certificate

离婚证识别

```python
result = ocr.recognize(image="divorce.jpg", api="divorce_certificate")
```

---

### account_opening

开户许可证识别

```python
result = ocr.recognize(image="account.jpg", api="account_opening")
```

---

### real_estate_certificate

不动产权证识别

```python
result = ocr.recognize(image="estate.jpg", api="real_estate_certificate")
```

---

### food_business_license

食品经营许可证识别

```python
result = ocr.recognize(image="food_license.jpg", api="food_business_license")
```

---

### food_product_license

食品生产许可证识别

```python
result = ocr.recognize(image="product_license.jpg", api="food_product_license")
```

---

## 医疗票据

### medical_record

医疗记录识别

```python
result = ocr.recognize(image="record.jpg", api="medical_record")
```

---

### medical_statement

医疗费用清单识别

```python
result = ocr.recognize(image="statement.jpg", api="medical_statement")
```

---

### medical_invoice

医疗发票识别

```python
result = ocr.recognize(image="medical_invoice.jpg", api="medical_invoice")
```

---

### medical_detail

门诊费用明细识别

```python
result = ocr.recognize(image="detail.jpg", api="medical_detail")
```

---

### medical_report_detection

医学检验报告识别

```python
result = ocr.recognize(image="report.jpg", api="medical_report_detection")
```

---

### medical_summary

病案首页识别

```python
result = ocr.recognize(image="summary.jpg", api="medical_summary")
```

---

### health_report

健康体检报告识别

```python
result = ocr.recognize(image="health.jpg", api="health_report")
```

---

## 文档表格

### table

表格文字识别

```python
result = ocr.recognize(
    image="table.jpg",
    api="table",
    request_type="excel"  # 返回 Excel 格式
)
```

**额外参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `location` | `bool` | 是否返回位置信息 |
| `is_sync` | `bool` | 同步/异步模式 |
| `request_type` | `str` | `excel`（返回Excel）/ `json`（返回JSON） |

---

### handwriting

手写文字识别

```python
result = ocr.recognize(image="handwriting.jpg", api="handwriting")
```

---

### formula

公式识别

```python
result = ocr.recognize(image="formula.jpg", api="formula")
```

---

### doc_analysis_office

办公文档识别

```python
result = ocr.recognize(
    image="document.jpg",
    api="doc_analysis_office",
    lang_type="CHN_ENG",
    data_format="json"
)
```

**额外参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `lang_type` | `str` | 语言类型 |
| `data_format` | `str` | 返回格式：json/html/docx |
| `coord_ratio` | `float` | 坐标缩放比例 |

---

### doc_analysis

文档识别（doc_analysis_office 的别名）

```python
result = ocr.recognize(image="doc.jpg", api="doc_analysis")
```

---

### remove_handwriting

去除手写文字

```python
result = ocr.recognize(image="doc.jpg", api="remove_handwriting")
```

---

### doc_crop_enhance

文档图像切边增强

```python
result = ocr.recognize(image="doc.jpg", api="doc_crop_enhance")
```

---

### doc_convert_request

文档转换请求

```python
result = ocr.recognize(
    image="doc.jpg",
    api="doc_convert_request",
    file_type="doc",
    lang_type="CHN_ENG"
)
```

**额外参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `file_type` | `str` | 目标文件类型 |
| `lang_type` | `str` | 语言类型 |

---

### doc_convert_get_result

文档转换结果查询

```python
result = ocr.recognize(api="doc_convert_get_result", task_id="xxx")
```

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_id` | `str` | 是 | doc_convert_request 返回的 task_id |
| `get_file` | `bool` | 否 | 是否返回文件内容 |

---

### doc_parse_request

文档解析请求

```python
result = ocr.recognize(
    image="doc.jpg",
    api="doc_parse_request",
    parse_direction="horizontal",
    parse_type="doc"
)
```

---

### doc_parse_get_result

文档解析结果查询

```python
result = ocr.recognize(api="doc_parse_get_result", request_id="xxx")
```

---

### doc_extract_request

文档抽取请求

```python
result = ocr.recognize(
    image="doc.jpg",
    api="doc_extract_request",
    extract_formulas=True,
    extract_tables=True,
    extract_word=True
)
```

---

### doc_extract_get_result

文档抽取结果查询

```python
result = ocr.recognize(api="doc_extract_get_result", request_id="xxx")
```

---

### doc_classify

文档分类

```python
result = ocr.recognize(image="doc.jpg", api="doc_classify")
```

---

## 合同比对

### contract_review_submit

合同比对提交

```python
result = ocr.recognize(
    image="contract1.jpg",
    image_url="https://example.com/contract2.jpg",
    api="contract_review_submit",
    contract_type="standard"
)
```

---

### contract_review_get_result

合同比对结果查询

```python
result = ocr.recognize(api="contract_review_get_result", task_id="xxx")
```

---

### doc_compare_submit

文档比对提交

```python
result = ocr.recognize(
    image1="doc1.jpg",
    image2="doc2.jpg",
    api="doc_compare_submit"
)
```

---

### doc_compare_get_result

文档比对结果查询

```python
result = ocr.recognize(api="doc_compare_get_result", request_id="xxx")
```

---

## 企业核验

### businesslicense_verification_standard

营业执照标准化核验

```python
result = ocr.recognize(
    api="businesslicense_verification_standard",
    license_no="91110000XXXXXXXX",
    enterprise_name="示例公司",
    legal_person="张三",
    registered_capital="1000万元",
    enterprise_address="北京市海淀区",
    business_scope="技术开发",
    establishment_date="2020-01-01"
)
```

---

### businesslicense_verification_detailed

营业执照详细核验

```python
result = ocr.recognize(
    api="businesslicense_verification_detailed",
    license_no="91110000XXXXXXXX",
    enterprise_name="示例公司"
)
```

---

### three_factors_verification

三要素验证（企业名+法人+注册资本）

```python
result = ocr.recognize(
    api="three_factors_verification",
    enterprise_name="示例公司",
    legal_person="张三",
    registered_capital="1000万元"
)
```

---

### four_factors_verification

四要素验证（企业名+法人+注册资本+地址）

```python
result = ocr.recognize(
    api="four_factors_verification",
    enterprise_name="示例公司",
    legal_person="张三",
    registered_capital="1000万元",
    enterprise_address="北京市海淀区"
)
```

---

### two_factors_verification

二要素验证（企业名+法人）

```python
result = ocr.recognize(
    api="two_factors_verification",
    enterprise_name="示例公司",
    legal_person="张三"
)
```

---

## 教育类

### paper_cut_edu

试卷切割识别

```python
result = ocr.recognize(
    image="paper.jpg",
    api="paper_cut_edu",
    cut_type="answer"
)
```

**额外参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `cut_type` | `str` | 切割类型：question/answer |

---

### composition_create_task

作文批改创建任务

```python
result = ocr.recognize(
    image="composition.jpg",
    api="composition_create_task",
    title="我的妈妈",
    grade="三年级"
)
```

---

### composition_get_result

作文批改结果查询

```python
result = ocr.recognize(api="composition_get_result", request_id="xxx")
```

---

### correct_edu_create_task

批改教育创建任务

```python
result = ocr.recognize(
    image="homework.jpg",
    api="correct_edu_create_task",
    task_type="math",
    grade="初二"
)
```

---

### correct_edu_get_result

批改教育结果查询

```python
result = ocr.recognize(api="correct_edu_get_result", request_id="xxx")
```

---

## 其他专业接口

### vin_code

车架号识别

```python
result = ocr.recognize(image="vin.jpg", api="vin_code")
```

---

### weight_note

重量单位识别

```python
result = ocr.recognize(image="weight.jpg", api="weight_note")
```

---

### mixed_multi_vehicle

多车型识别

```python
result = ocr.recognize(image="vehicles.jpg", api="mixed_multi_vehicle")
```

---

### waybill

运单识别

```python
result = ocr.recognize(image="waybill.jpg", api="waybill")
```

---

### insurance_documents

保险单识别

```python
result = ocr.recognize(image="insurance.jpg", api="insurance_documents")
```

---

### online_taxi_itinerary

网约车行程单识别

```python
result = ocr.recognize(image="taxi_itinerary.jpg", api="online_taxi_itinerary")
```

---

### pen

笔迹识别

```python
result = ocr.recognize(image="pen.jpg", api="pen")
```

---

### shopping_receipt

购物小票识别

```python
result = ocr.recognize(image="receipt.jpg", api="shopping_receipt")
```

---

### road_transport_certificate

道路运输证识别

```python
result = ocr.recognize(image="transport.jpg", api="road_transport_certificate")
```

---

### seal

印章识别

```python
result = ocr.recognize(image="seal.jpg", api="seal")
```

---

### facade

门脸识别

```python
result = ocr.recognize(image="facade.jpg", api="facade")
```

---

### meter

仪表盘识别

```python
result = ocr.recognize(image="meter.jpg", api="meter")
```

---

## 智能结构化

### smart_struct

智能结构化

```python
result = ocr.recognize(
    image="doc.jpg",
    api="smart_struct",
    structured_flag=1,
    schema_conf="..."
)
```

**额外参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `structured_flag` | `int` | 结构化标识 |
| `schema_conf` | `str` | Schema 配置 |

---

## iOCR

### iocr

iOCR 通用识别

```python
result = ocr.recognize(
    image="doc.jpg",
    api="iocr",
    template_id="xxx"
)
```

---

### iocr_finance

iOCR 财务票据识别

```python
result = ocr.recognize(
    image="invoice.jpg",
    api="iocr_finance",
    template_sign="xxx"
)
```

---

## EasyDL

### easydl

EasyDL 通用识别

```python
result = ocr.recognize(
    image="doc.jpg",
    api="easydl",
    easy_ocr="..."
)
```

---

## 其他

### qrcode

二维码识别

```python
result = ocr.recognize(image="qrcode.jpg", api="qrcode")
```

---

### forgery_detection

印章检测

```python
result = ocr.recognize(image="doc.jpg", api="forgery_detection")
```

---

### numbers

数字识别

```python
result = ocr.recognize(image="numbers.jpg", api="numbers")
```

---

### live_config_save

活体检测配置保存

```python
result = ocr.recognize(
    api="live_config_save",
    api_id="xxx",
    group_id="xxx"
)
```

---

### live_config_stop

活体检测配置停止

```python
result = ocr.recognize(api="live_config_stop")
```

---

### live_config_view

活体检测配置查询

```python
result = ocr.recognize(api="live_config_view", api_id="xxx")
```

---

### live_audit_pull

活体审计拉取

```python
result = ocr.recognize(
    api="live_audit_pull",
    api_id="xxx",
    group_id="xxx"
)
```

---

### paddle_vl_parser_task

PaddleVL 解析任务创建

```python
result = ocr.recognize(
    image="doc.jpg",
    api="paddle_vl_parser_task"
)
```

---

### paddle_vl_parser_query

PaddleVL 解析结果查询

```python
result = ocr.recognize(api="paddle_vl_parser_query", request_id="xxx")
```

---

## 返回值格式

所有 API 返回统一的字典格式：

```json
{
  "words_result": [
    {
      "words": "识别的文字",
      "location": {
        "vertices": [
          {"x": 0, "y": 0},
          {"x": 100, "y": 0},
          {"x": 100, "y": 30},
          {"x": 0, "y": 30}
        ]
      }
    }
  ],
  "words_result_num": 1
}
```

**本地兜底时额外字段**：

```json
{
  "words_result": [...],
  "words_result_num": 1,
  "fallback_info": {
    "engine": "EasyOCR",
    "message": "百度OCR服务不可用，使用本地EasyOCR进行识别"
  }
}
```

---

## 错误处理

```python
from scripts.ocr import OCR
from scripts.baidu_client import BaiduOCRError

ocr = OCR()
try:
    result = ocr.recognize(image="image.jpg", api="general_basic")
except BaiduOCRError as e:
    print(f"错误码: {e.error_code}")
    print(f"错误信息: {e.error_msg}")
except Exception as e:
    print(f"其他错误: {e}")
```

### 常见 BaiduOCRError 错误码

| 错误码 | 说明 |
|--------|------|
| 100 | Access token 无效 |
| 110 | Access token 没有调用权限 |
| 111 | Access token 已过期 |
| 216015 | 服务被关闭 |
| 216020 | 图片大小错误（超过4MB） |
| 216022 | 图片格式错误 |
| 282004 | 参数错误 |
| 336004 | 限流 |
