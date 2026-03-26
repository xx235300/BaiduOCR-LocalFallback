# 故障排除指南

本文档帮助您解决使用百度 OCR 技能时可能遇到的常见问题。

## 目录

- [认证与连接问题](#认证与连接问题)
- [API 调用问题](#api-调用问题)
- [本地兜底问题](#本地兜底问题)
- [图片处理问题](#图片处理问题)
- [性能问题](#性能问题)
- [错误码参考](#错误码参考)

---

## 认证与连接问题

### 症状：提示 "API Key 或 Secret Key 为空"

**错误信息**：
```
ValueError: API Key 和 Secret Key 不能为空
```

**原因**：未正确配置 API 密钥

**解决方案**：
1. 确认已获取有效的 API 密钥（不是 App ID）
2. 设置环境变量：
```bash
export BAIDU_OCR_API_KEY="<your_api_key>"
export BAIDU_OCR_SECRET_KEY="<your_secret_key>"
```
3. 或使用交互式配置：
```bash
python3 scripts/ocr.py --configure
```

---

### 症状：提示 "access_token 获取失败"

**错误信息**：
```
BaiduOCRError: 错误码: 110, 错误信息: Access token has no license to call this API
```

**原因**：API 密钥没有开通对应的服务

**解决方案**：
1. 登录 [百度智能云控制台](https://console.bce.baidu.com/)
2. 进入 "文字识别" 服务
3. 确认你的应用已开通需要的 OCR 服务（如高精度识别、身份证识别等）
4. 如未开通，点击 "开通服务" 后重新获取 token

---

### 症状：提示 "Access token has expired"

**错误信息**：
```
BaiduOCRError: 错误码: 111, 错误信息: Access token has expired
```

**原因**：access_token 过期（默认 30 天）

**解决方案**：
```python
from scripts.auth import auth
# 强制刷新 token
token = auth.get_access_token(force_refresh=True)
```

access_token 会自动缓存，本技能会自动处理过期情况。如需手动刷新，删除缓存文件：
```bash
rm ~/.openclaw/skills/BaiduOCR-LocalFallback/cache/access_token.txt
```

---

### 症状：无法连接到百度服务器

**错误信息**：
```
ConnectionError: HTTPSConnectionPool(host='aip.baidubce.com', port=443)
```

**原因**：
- 网络连接问题
- 代理配置错误
- 防火墙阻止

**解决方案**：
1. 检查网络连接：
```bash
ping aip.baidubce.com
```

2. 配置代理（如需要）：
```bash
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"
```

3. 检查防火墙规则，确保允许 443 端口出站

4. 使用命令行测试：
```bash
curl -I https://aip.baidubce.com
```

---

## API 调用问题

### 症状：所有 API 都返回 216015

**错误信息**：
```
BaiduOCRError: 错误码: 216015, 错误信息: module closed
```

**原因**：服务被关闭或欠费

**解决方案**：
1. 登录百度智能云控制台检查账户余额
2. 确认 OCR 服务已开通且未过期
3. 部分服务需要付费，确认已购买相应套餐

---

### 症状：特定 API 不可用

**错误信息**：
```
BaiduOCRError: 错误码: 282004, 错误信息: param invalid
```

**原因**：API 参数错误或该 API 未开通

**解决方案**：
1. 检查 API 名称是否正确（区分大小写）
2. 确认该 API 服务已开通：
   - 登录控制台 → 文字识别 → 我的应用
   - 查看已开通的服务列表
3. 检查必填参数是否提供

---

### 症状：图片大小超限

**错误信息**：
```
BaiduOCRError: 错误码: 216202, 错误信息: image size error
```

**原因**：图片超过 4MB 限制

**解决方案**：
本技能会自动压缩图片，但如需手动处理：

```python
from PIL import Image

# 压缩图片
img = Image.open("large_image.jpg")
img = img.resize((img.width // 2, img.height // 2), Image.LANCZOS)
img.save("compressed_image.jpg", quality=85)
```

或使用命令行：
```bash
# 使用 ImageMagick
convert large_image.jpg -resize 50% compressed_image.jpg
```

---

### 症状：返回结果为空

**可能原因**：
1. 图片中没有文字
2. 图片质量太差
3. 文字被水印遮挡

**解决方案**：
1. 确认图片中确实包含可识别的文字
2. 提高图片分辨率和清晰度
3. 检查是否有严重遮挡或水印
4. 尝试使用高精度 API：
```python
result = ocr.recognize(image="image.jpg", api="accurate_basic")
```

---

## 本地兜底问题

### 症状：提示 "EasyOCR 未安装"

**错误信息**：
```
EasyOCRNotAvailableError: EasyOCR未安装
```

**解决方案**：
```bash
pip3 install easyocr
```

---

### 症状：EasyOCR 初始化很慢

**原因**：首次运行需要下载模型（约 100MB）

**解决方案**：
1. 耐心等待，首次初始化后模型会缓存
2. 或手动预下载模型：
```python
from scripts.local_ocr import local_ocr
import easyocr

# 手动触发模型下载
print("正在下载 EasyOCR 模型...")
reader = easyocr.Reader(["ch_sim", "en"], verbose=True)
```

3. 使用国内镜像（可选）：
```python
import os
os.environ["EASYOCR_MODULE_PATH"] = "~/.easyocr"
# 或从 BaiduDrive 下载模型后放到此目录
```

---

### 症状：EasyOCR 识别效果差

**原因**：
- 模型不支持某些字体
- 图片质量低
- 手写文字识别困难

**解决方案**：
1. 确保图片清晰、光照均匀
2. 使用适当的图片预处理：
```python
from scripts.image_processor import processor

# 增强对比度
processed_data, info = processor.process(
    raw_data,
    max_size=2097152,  # 2MB
    enhance_contrast=True
)
```

3. 对于复杂场景，考虑：
   - 调整图片角度
   - 去噪声
   - 二值化处理

---

### 症状：本地兜底没有自动触发

**原因**：禁用了兜底功能

**解决方案**：
```python
# 默认 use_fallback=True
ocr = OCR(use_fallback=True)
```

命令行：
```bash
# 不要加 --no-fallback 参数
python3 scripts/ocr.py --image image.jpg
```

---

## 图片处理问题

### 症状：图片方向错误

**原因**：百度 OCR 默认不检测方向

**解决方案**：
```python
result = ocr.recognize(
    image="rotated_image.jpg",
    api="general",
    detect_direction="true"  # 检测方向并旋转
)
```

---

### 症状：语言识别错误

**原因**：未正确指定语言类型

**解决方案**：
```python
# 自动检测语言
result = ocr.recognize(
    image="image.jpg",
    api="general",
    detect_language="true"
)

# 手动指定语言
result = ocr.recognize(
    image="image.jpg",
    api="general_basic",
    language_type="ENG"  # 英文
)
```

支持的参数：
- `CHN_ENG`：中英混合
- `ENG`：英文
- `POR`：葡萄牙语
- `FRE`：法语
- `GER`：德语
- `JPN`：日语
- `KOR`：韩语

---

### 症状：Base64 图片无法识别

**原因**：Base64 格式不正确

**解决方案**：
```python
import base64

# 正确：Data URI 格式
# data:image/jpeg;base64,/9j/4AAQSkZJRg...

# 正确：纯 Base64 字符串
with open("image.jpg", "rb") as f:
    img_base64 = base64.b64encode(f.read()).decode()
    
result = ocr.recognize(image=img_base64, api="general_basic")
```

---

## 性能问题

### 症状：识别速度慢

**原因**：
- 图片太大
- 网络延迟
- 未使用 GPU

**解决方案**：
1. 压缩图片到 2MB 以内：
```python
# 自动压缩（已内置）
result = ocr.recognize(image="large_image.jpg", api="general_basic")
```

2. 使用本地兜底（无网络延迟）：
```python
result = ocr.recognize(
    image="image.jpg",
    api="handwriting",
    fallback=True  # 使用本地 EasyOCR
)
```

3. 启用 GPU 加速（EasyOCR）：
```python
# 确保安装了 GPU 版本
pip3 install easyocr[gpu]
# 或
pip3 install torch --index-url https://download.pytorch.org/whl/cu118
```

---

### 症状：内存占用高

**原因**：EasyOCR 模型加载到内存

**解决方案**：
1. 处理完成后释放资源：
```python
from scripts.local_ocr import local_ocr
local_ocr._reader = None
import gc
gc.collect()
```

2. 使用单例模式避免重复加载（已内置）

---

## 错误码参考

### 认证错误 (1xxxx)

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 110 | Access token has no license | 开通对应服务 |
| 111 | Access token has expired | 刷新 token |
| 100 | Access token invalid | 检查 API 密钥 |

### 参数错误 (2xxxx)

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 216015 | module closed | 检查服务是否开通/欠费 |
| 216020 | image size error | 压缩图片到 4MB 以内 |
| 216022 | image format error | 转换为 JPG/PNG/BMP |
| 282004 | param invalid | 检查 API 参数 |

### 服务错误 (3xxxx)

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 336004 | rate limit exceeded | 降低请求频率 |
| 336100 | server error | 稍后重试 |

### 网络错误

| 错误 | 说明 | 解决方案 |
|------|------|----------|
| ConnectionError | 无法连接服务器 | 检查网络/代理 |
| Timeout | 请求超时 | 增加超时时间或重试 |
| SSLError | SSL 证书错误 | 更新 CA 证书 |

---

## 获取帮助

如果问题仍未解决：

1. 查看 [GitHub Issues](https://github.com/xx235300/BaiduOCR-LocalFallback/issues)
2. 运行诊断命令：
```bash
python3 scripts/ocr.py --test-connection
python3 scripts/ocr.py --show-apis
```
3. 提交 Issue 时请附上：
   - 错误完整信息
   - Python 版本
   - 操作系统
   - 相关代码片段
