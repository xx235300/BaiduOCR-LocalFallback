# BaiduOCR-LocalFallback

English ｜ [[简体中文](https://github.com/xx235300/BaiduOCR-LocalFallback/blob/main/README_ZN.md)]

> **Disclaimer**:
> 1. This project is not an official Baidu product and has no affiliation with Baidu. This project only provides a wrapper for Baidu OCR API; users must apply for a Baidu Cloud account and comply with Baidu's terms of service.
> 2. This project is 99% AI-generated. The AI's owner has no programming background. Please evaluate the project's feasibility before use.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

**115+ Baidu OCR API support with EasyOCR local fallback — auto-switches to local recognition when the network is unstable.**

## Why This Project?

OCR text recognition typically faces two problems:

1. **Cloud service dependency** — Baidu OCR and similar cloud services rely on network quality, leading to instability during fluctuations
2. **Handwriting / special scenarios** — Cloud services struggle with handwritten text and blurry images

This skill provides:
- 🌐 **115+ Baidu OCR APIs** — General, ID cards, receipts, documents, education, and more
- 🔄 **Local fallback** — Integrates EasyOCR; auto-switches when Baidu OCR is unavailable
- 🖼️ **Smart preprocessing** — Auto compresses and converts formats to fit the 4MB API limit
- 💾 **Token caching** — access_token cached for 25 days to reduce redundant requests（According to Baidu's official regulations, the validity period of the access_token is 30 days, and it needs to be replaced regularly every 30 days.）
- ⚡ **Auto retry** — Retries up to 3 times on network fluctuations

## Recognition Test

- Test image: 
![Alt text](https://picui.ogmua.cn/s1/2026/03/26/69c40faadc447.webp)
- Results:
```
测试英文识别：hello world
测试简体中文识别：你好世界
测试繁体中文识别：今日氣溫有所降低，請穿好棉服
测试标点符号识别：，。；""/？'！~、|\@#$%&*()_-=+；：[]{}【】「」《》，<>
```

## Quick Start

### Step 1: Install Dependencies

```bash
pip3 install requests easyocr Pillow
```

### Step 2: Configure API Credentials

**Method A: Interactive configuration (recommended)**
```bash
python3 scripts/ocr.py --configure
```

**Method B: Environment variables**
```bash
export BAIDU_OCR_API_KEY="<your_api_key>"
export BAIDU_OCR_SECRET_KEY="<your_secret_key>"
```

**Method C: Config file**
```bash
mkdir -p ~/.openclaw/skills/BaiduOCR-LocalFallback
# Edit the config file
cat > ~/.openclaw/skills/BaiduOCR-LocalFallback/config.json << 'EOF'
{
  "api_key": "<your_api_key>",
  "secret_key": "<your_secret_key>"
}
EOF
```

> ⚠️ **Get API credentials**: Go to [Baidu Cloud Console](https://console.bce.baidu.com/) → Search "OCR" → Create an app to get AK/SK

### Step 3: Start Recognizing

```python
from scripts.ocr import OCR

ocr = OCR()

# General text recognition
result = ocr.recognize(image="/path/to/image.jpg", api="general_basic")

# Web image
result = ocr.recognize(image_url="https://example.com/image.jpg", api="webimage")

# ID card recognition
result = ocr.recognize(image="/path/to/idcard.jpg", api="idcard", id_card_side="front")

# Handwriting (local fallback)
result = ocr.recognize(image="/path/to/handwriting.jpg", api="handwriting")
```

## Configuration Options

### Configuration Priority

| Priority | Method | Location |
|---------|--------|----------|
| 1 | Environment variables | `BAIDU_OCR_API_KEY`, `BAIDU_OCR_SECRET_KEY` |
| 2 | Config file | `~/.openclaw/skills/BaiduOCR-LocalFallback/config.json` |
| 3 | Interactive | `python3 scripts/ocr.py --configure` |

### Interactive Configuration

```bash
$ python3 scripts/ocr.py --configure
==================================================
BaiduOCR Configuration Wizard
==================================================
Enter Baidu OCR API Key: <your_api_key>
Enter Baidu OCR Secret Key: <your_secret_key>
Config saved to: ~/.openclaw/skills/BaiduOCR-LocalFallback/config.json
```

### Config File Format

```json
{
  "api_key": "<your_api_key>",
  "secret_key": "<your_secret_key>"
}
```

### Disable Local Fallback

```python
ocr = OCR(use_fallback=False)

# Or via CLI
python3 scripts/ocr.py --image /path/to/image.jpg --no-fallback
```

## Usage Examples

### Python API

#### General Text Recognition

```python
from scripts.ocr import OCR

ocr = OCR()

# Basic usage
result = ocr.recognize(image="photo.jpg", api="general_basic")
print(result["words_result"][0]["words"])

# High-accuracy recognition (with location info)
result = ocr.recognize(image="photo.jpg", api="accurate")

# Specify language
result = ocr.recognize(
    image="photo.jpg",
    api="general_basic",
    language_type="CHN_ENG"  # Chinese & English
)
```

#### ID Card Recognition

```python
# Front side
result = ocr.recognize(
    image="idcard_front.jpg",
    api="idcard",
    id_card_side="front"
)

# Back side
result = ocr.recognize(
    image="idcard_back.jpg",
    api="idcard",
    id_card_side="back"
)

# Extract info
name = result["words_result"][0]["words"]  # Name
address = result["words_result"][5]["words"]  # Address
```

#### Receipt Recognition

```python
# VAT invoice
result = ocr.recognize(image="invoice.jpg", api="vat_invoice")

# Train ticket
result = ocr.recognize(image="train.jpg", api="train_ticket")

# Taxi receipt
result = ocr.recognize(image="taxi.jpg", api="taxi_receipt")

# Multiple receipts
result = ocr.recognize(image="receipts.jpg", api="multiple_invoice")
```

#### Table Recognition

```python
result = ocr.recognize(
    image="table.jpg",
    api="table",
    request_type="excel"  # Returns Excel format
)
```

### CLI Tool

```bash
# Recognize local image
python3 scripts/ocr.py --image /path/to/image.jpg

# Recognize web image
python3 scripts/ocr.py --image-url "https://example.com/image.jpg"

# Specify API
python3 scripts/ocr.py --image /path/to/idcard.jpg --api idcard --id-card-side front

# JSON output
python3 scripts/ocr.py --image /path/to/image.jpg --json

# Save result to file
python3 scripts/ocr.py --image /path/to/image.jpg --output result.txt

# Test connection
python3 scripts/ocr.py --test-connection

# Show all APIs
python3 scripts/ocr.py --show-apis
```

### Response Format

```json
{
  "words_result": [
    {
      "words": "Recognized text",
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

**When using local fallback, additional fields:**

```json
{
  "words_result": [...],
  "words_result_num": 1,
  "fallback_info": {
    "engine": "EasyOCR",
    "message": "Baidu OCR unavailable, using local EasyOCR"
  }
}
```

### Error Handling

```python
from scripts.ocr import OCR
from scripts.baidu_client import BaiduOCRError

ocr = OCR()
try:
    result = ocr.recognize(image="/path/to/image.jpg")
except BaiduOCRError as e:
    print(f"Baidu OCR error: {e.error_code} - {e.error_msg}")
except Exception as e:
    print(f"Other error: {e}")
```

## Supported APIs

### General Text
| API | Description | Location Info |
|-----|-------------|---------------|
| `general` | General text recognition | ✅ |
| `general_basic` | General text (basic) | ❌ |
| `accurate` | High-accuracy recognition | ✅ |
| `accurate_basic` | High-accuracy (basic) | ❌ |

### Web Image
| API | Description |
|-----|-------------|
| `webimage` | Web image text recognition |

### ID & Cards
| API | Description |
|-----|-------------|
| `idcard` | ID card |
| `multi_idcard` | Multiple ID cards |
| `bankcard` | Bank card |
| `business_license` | Business license |
| `passport` | Passport |
| `driving_license` | Driver's license |
| `vehicle_license` | Vehicle license |

### Receipts
| API | Description |
|-----|-------------|
| `receipt` | General receipt |
| `vat_invoice` | VAT invoice |
| `taxi_receipt` | Taxi receipt |
| `train_ticket` | Train ticket |
| `air_ticket` | Air ticket |
| `invoice` | Invoice |
| `quota_invoice` | Quota invoice |
| `bus_ticket` | Bus ticket |
| `toll_invoice` | Toll receipt |
| `bank_receipt_new` | Bank receipt |

### Handwriting / Documents
| API | Description |
|-----|-------------|
| `handwriting` | Handwriting recognition |
| `table` | Table recognition |
| `formula` | Formula recognition |

### Medical
| API | Description |
|-----|-------------|
| `medical_record` | Medical record |
| `medical_statement` | Medical expense list |
| `medical_invoice` | Medical invoice |

### Education
| API | Description |
|-----|-------------|
| `paper_cut_edu` | Paper cut |
| `composition_create_task` | Essay grading |

### Others (115+ APIs)
Run `python3 scripts/ocr.py --show-apis` for the full list.

## Architecture

```
scripts/
├── __init__.py          # Package init
├── ocr.py               # Main entry / CLI
├── auth.py              # Auth module (Token management)
├── baidu_client.py      # Baidu OCR HTTP client
├── api_router.py        # 115 API routes
├── local_ocr.py         # EasyOCR local fallback
├── config.py            # Config management
└── image_processor.py  # Image preprocessing
```

## Performance Tips

- 🐍 **First-time EasyOCR** requires downloading models (~100MB), please be patient
- 📏 **Image size** recommended under 2MB for best performance
- 🖼️ **Large images** are auto-compressed and scaled
- 💾 **access_token** is auto-cached and refreshed (25 days)
- ⚡ **GPU acceleration** EasyOCR auto-uses GPU if available

## FAQ

### Q: I have no coding experience, what should I do if an error occurs during use?

Just send the cloud document link to the AI and let it troubleshoot and find a solution on its own.
Sample prompt:
```
Please troubleshoot and resolve the issue according to the skill usage documentation.
Skill Usage Documentation: https://my.feishu.cn/docx/Gjy0djSado5YqVxzO6ecYbOmn4g?from=from_copylink
```

### Q: How to get Baidu OCR API credentials?

1. Go to [Baidu Cloud Console](https://console.bce.baidu.com/)
2. Search "OCR" or "文字识别"
3. Create an app and enable the OCR services you need
4. Get API Key and Secret Key from "My Apps"

### Q: "Baidu OCR call failed" but no auto-switch to local fallback?

Check if fallback is disabled:
```python
ocr = OCR(use_fallback=False)  # Fallback disabled
```

### Q: EasyOCR initialization is slow?

First run requires downloading models (~100MB). Pre-initialize:
```python
from scripts.local_ocr import local_ocr
local_ocr._init_reader()  # Warm up
```

### Q: How to handle Base64 images?

```python
import base64

# Read image and convert to Base64
with open("image.jpg", "rb") as f:
    img_base64 = base64.b64encode(f.read()).decode()

result = ocr.recognize(image=img_base64, api="general_basic")
```

### Q: How to specify output format?

```python
# Table - returns Excel
result = ocr.recognize(image="table.jpg", api="table", request_type="excel")

# Table - returns JSON
result = ocr.recognize(image="table.jpg", api="table", request_type="json")
```

### Q: Web image recognition failed?

Web images must be publicly accessible. Ensure:
1. Image URL is publicly reachable
2. Firewall allows outbound 80/443
3. Try downloading locally first

### Q: How to disable SSL certificate verification (dev only)?

```python
import os
os.environ['REQUESTS_CA_BUNDLE'] = '/path/to/ca-bundle.crt'
```

## Contributing

Issues and Pull Requests are welcome!

1. Fork this repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

## License

MIT © 2026 xx235300
