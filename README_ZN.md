# BaiduOCR-LocalFallback

[[English](https://github.com/xx235300/BaiduOCR-LocalFallback/blob/main/README.md)] ｜ 简体中文

> **免责声明**：
> 1. 本项目非百度官方产品，与百度公司无隶属关系。本项目仅提供对百度 OCR API 的调用封装，用户需自行申请百度智能云账号并遵守百度服务条款。
> 2. 本项目99%由AI开发，AI的主人没有代码基础，请自行辨别项目可行性后再使用。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

**支持 115+ 个百度 OCR API 接口，集成 EasyOCR 本地兜底方案，网络不稳定时自动切换本地识别。**

## 为什么需要这个

当你需要在项目中使用 OCR 文字识别时，通常会面临两个问题：

1. **依赖云服务** —— 百度 OCR 等云服务依赖网络质量，网络波动时服务不稳定
2. **手写/特殊场景** —— 云服务对手写文字、模糊图片的识别效果不佳

本技能提供：
- 🌐 **115+ 百度 OCR API** —— 覆盖通用、证件、票据、文档、教育等全场景
- 🔄 **本地兜底** —— 集成 EasyOCR，百度 OCR 不可用时自动切换本地识别
- 🖼️ **智能预处理** —— 自动压缩、格式转换，适配 4MB API 限制
- 💾 **Token 缓存** —— access_token 缓存 25 天，减少重复请求（百度官方规定access_token的有效期为30天，需要每30天进行定期更换）
- ⚡ **自动重试** —— 网络波动时自动重试 3 次

## 识别效果测试

- 测试图片: https://picui.ogmua.cn/s1/2026/03/26/69c40faadc447.webp
- 识别结果:
- 测试英文识别：hello world
- 测试简体中文识别：你好世界
- 测试繁体中文识别：今日氣溫有所降低，請穿好棉服
- 测试标点符号识别：，。；""/？'！~、|\@#$%&*()_-=+；：[]{}【】「」《》，<>

## 快速开始

### 第 1 步：安装依赖

```bash
pip3 install requests easyocr Pillow
```

### 第 2 步：配置 API 密钥

**方式 A：交互式配置（推荐）**
```bash
python3 scripts/ocr.py --configure
```

**方式 B：环境变量**
```bash
export BAIDU_OCR_API_KEY="<your_api_key>"
export BAIDU_OCR_SECRET_KEY="<your_secret_key>"
```

**方式 C：配置文件**
```bash
mkdir -p ~/.openclaw/skills/BaiduOCR-LocalFallback
# 编辑配置文件
cat > ~/.openclaw/skills/BaiduOCR-LocalFallback/config.json << 'EOF'
{
  "api_key": "<your_api_key>",
  "secret_key": "<your_secret_key>"
}
EOF
```

> ⚠️ **获取 API 密钥**：前往 [百度智能云控制台](https://console.bce.baidu.com/) → 搜索 "文字识别" → 创建应用获取 AK/SK

### 第 3 步：开始识别

```python
from scripts.ocr import OCR

ocr = OCR()

# 通用文字识别
result = ocr.recognize(image="/path/to/image.jpg", api="general_basic")

# 网络图片
result = ocr.recognize(image_url="https://example.com/image.jpg", api="webimage")

# 身份证识别
result = ocr.recognize(image="/path/to/idcard.jpg", api="idcard", id_card_side="front")

# 手写文字（本地兜底）
result = ocr.recognize(image="/path/to/handwriting.jpg", api="handwriting")
```

## 配置选项详解

### 三种配置方式优先级

| 优先级 | 方式 | 配置位置 |
|--------|------|----------|
| 1 | 环境变量 | `BAIDU_OCR_API_KEY`, `BAIDU_OCR_SECRET_KEY` |
| 2 | 配置文件 | `~/.openclaw/skills/BaiduOCR-LocalFallback/config.json` |
| 3 | 交互式 | `python3 scripts/ocr.py --configure` |

### 交互式配置

```bash
$ python3 scripts/ocr.py --configure
==================================================
百度OCR配置向导
==================================================
请输入百度OCR API Key: <your_api_key>
请输入百度OCR Secret Key: <your_secret_key>
配置已保存到: ~/.openclaw/skills/BaiduOCR-LocalFallback/config.json
```

### 配置文件格式

```json
{
  "api_key": "<your_api_key>",
  "secret_key": "<your_secret_key>"
}
```

### 禁用本地兜底

如果不需要 EasyOCR 本地兜底功能：

```python
ocr = OCR(use_fallback=False)

# 或者命令行
python3 scripts/ocr.py --image /path/to/image.jpg --no-fallback
```

## 使用示例

### Python API

#### 通用文字识别

```python
from scripts.ocr import OCR

ocr = OCR()

# 基础用法
result = ocr.recognize(image="photo.jpg", api="general_basic")
print(result["words_result"][0]["words"])

# 高精度识别（含位置信息）
result = ocr.recognize(image="photo.jpg", api="accurate")

# 指定语言
result = ocr.recognize(
    image="photo.jpg",
    api="general_basic",
    language_type="CHN_ENG"  # 中英混合
)
```

#### 身份证识别

```python
# 身份证正面
result = ocr.recognize(
    image="idcard_front.jpg",
    api="idcard",
    id_card_side="front"
)

# 身份证反面
result = ocr.recognize(
    image="idcard_back.jpg",
    api="idcard",
    id_card_side="back"
)

# 提取信息
name = result["words_result"][0]["words"]  # 姓名
address = result["words_result"][5]["words"]  # 地址
```

#### 票据识别

```python
# 增值税发票
result = ocr.recognize(image="invoice.jpg", api="vat_invoice")

# 火车票
result = ocr.recognize(image="train.jpg", api="train_ticket")

# 出租车票
result = ocr.recognize(image="taxi.jpg", api="taxi_receipt")

# 多张票据
result = ocr.recognize(image="receipts.jpg", api="multiple_invoice")
```

#### 表格识别

```python
result = ocr.recognize(
    image="table.jpg",
    api="table",
    request_type="excel"  # 返回 Excel 格式
)
```

### 命令行工具

```bash
# 识别本地图片
python3 scripts/ocr.py --image /path/to/image.jpg

# 识别网络图片
python3 scripts/ocr.py --image-url "https://example.com/image.jpg"

# 指定 API
python3 scripts/ocr.py --image /path/to/idcard.jpg --api idcard --id-card-side front

# JSON 输出
python3 scripts/ocr.py --image /path/to/image.jpg --json

# 保存结果到文件
python3 scripts/ocr.py --image /path/to/image.jpg --output result.txt

# 测试连接
python3 scripts/ocr.py --test-connection

# 查看所有 API
python3 scripts/ocr.py --show-apis
```

### 返回格式

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

**本地兜底时额外返回：**

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

### 错误处理

```python
from scripts.ocr import OCR
from scripts.baidu_client import BaiduOCRError

ocr = OCR()
try:
    result = ocr.recognize(image="/path/to/image.jpg")
except BaiduOCRError as e:
    print(f"百度OCR错误: {e.error_code} - {e.error_msg}")
except Exception as e:
    print(f"其他错误: {e}")
```

## 支持的 API 列表

### 通用文字识别
| API | 说明 | 位置信息 |
|-----|------|---------|
| `general` | 通用文字识别 | ✅ |
| `general_basic` | 通用文字识别（基础版） | ❌ |
| `accurate` | 高精度文字识别 | ✅ |
| `accurate_basic` | 高精度文字识别（基础版） | ❌ |

### 网络图片
| API | 说明 |
|-----|------|
| `webimage` | 网络图片文字识别 |

### 证件卡片
| API | 说明 |
|-----|------|
| `idcard` | 身份证识别 |
| `multi_idcard` | 多张身份证识别 |
| `bankcard` | 银行卡识别 |
| `business_license` | 营业执照识别 |
| `passport` | 护照识别 |
| `driving_license` | 驾驶证识别 |
| `vehicle_license` | 行驶证识别 |

### 票据
| API | 说明 |
|-----|------|
| `receipt` | 通用票据识别 |
| `vat_invoice` | 增值税发票 |
| `taxi_receipt` | 出租车票 |
| `train_ticket` | 火车票 |
| `air_ticket` | 机票 |
| `invoice` | 发票识别 |
| `quota_invoice` | 定额发票 |
| `bus_ticket` | 汽车票 |
| `toll_invoice` | 过路过桥费 |
| `bank_receipt_new` | 银行回单 |

### 手写/文档
| API | 说明 |
|-----|------|
| `handwriting` | 手写文字识别 |
| `table` | 表格识别 |
| `formula` | 公式识别 |

### 医疗
| API | 说明 |
|-----|------|
| `medical_record` | 医疗记录 |
| `medical_statement` | 医疗费用清单 |
| `medical_invoice` | 医疗发票 |

### 教育
| API | 说明 |
|-----|------|
| `paper_cut_edu` | 试卷切割 |
| `composition_create_task` | 作文批改 |

### 其他（共 115+ 个 API）
运行 `python3 scripts/ocr.py --show-apis` 查看完整列表。

## 架构

```
scripts/
├── __init__.py          # 包初始化
├── ocr.py               # 主入口/CLI
├── auth.py              # 认证模块(Token管理)
├── baidu_client.py      # 百度OCR HTTP客户端
├── api_router.py        # 115个API路由
├── local_ocr.py         # EasyOCR本地兜底
├── config.py            # 配置管理
└── image_processor.py   # 图片预处理
```

## 性能提示

- 🐍 **首次使用 EasyOCR** 需要下载模型（约 100MB），请耐心等待
- 📏 **图片大小** 建议控制在 2MB 以内以获得最佳性能
- 🖼️ **大图片** 会自动压缩和缩放
- 💾 **access_token** 会自动缓存和刷新（25天）
- ⚡ **GPU 加速** EasyOCR 会自动使用 GPU（如可用）

## 常见问题

### Q: 我没有代码基础，但是使用中出现错误了怎么办？

把云文档丢给AI，让他自行排查寻找解决方案
示例提示词：
```
请按照技能使用方法文档排查并解决问题
技能使用方法文档：https://my.feishu.cn/docx/Gjy0djSado5YqVxzO6ecYbOmn4g?from=from_copylink
```

### Q: 如何获取百度 OCR API 密钥？

1. 前往 [百度智能云控制台](https://console.bce.baidu.com/)
2. 搜索 "文字识别" 或 "OCR"
3. 创建应用，勾选需要的 OCR 服务
4. 在 "我的应用" 中获取 API Key 和 Secret Key

### Q: 提示 "百度OCR调用失败" 但没有自动切换本地识别？

检查是否禁用了兜底功能：
```python
ocr = OCR(use_fallback=False)  # 禁用了兜底
```

### Q: EasyOCR 初始化很慢？

首次运行 EasyOCR 需要下载模型（约 100MB）。可以预先初始化：
```python
from scripts.local_ocr import local_ocr
local_ocr._init_reader()  # 预热
```

### Q: 如何处理 Base64 图片？

```python
import base64

# 读取图片并转为 Base64
with open("image.jpg", "rb") as f:
    img_base64 = base64.b64encode(f.read()).decode()

result = ocr.recognize(image=img_base64, api="general_basic")
```

### Q: 如何指定输出格式？

```python
# 表格识别 - 返回 Excel
result = ocr.recognize(image="table.jpg", api="table", request_type="excel")

# 表格识别 - 返回 JSON
result = ocr.recognize(image="table.jpg", api="table", request_type="json")
```

### Q: 网络图片识别失败？

网络图片需要可公开访问。确保：
1. 图片 URL 可公网访问
2. 防火墙允许 80/443 端口出站
3. 尝试下载到本地后识别

### Q: 如何禁用 SSL 证书验证（开发环境）？

```python
import os
os.environ['REQUESTS_CA_BUNDLE'] = '/path/to/ca-bundle.crt'
```

## 参与贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

MIT © 2026 xx235300
