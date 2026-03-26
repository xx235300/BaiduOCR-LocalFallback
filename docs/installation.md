# 安装指南

本指南详细说明如何安装和配置百度 OCR 技能。

## 前置要求

### 系统要求

- **操作系统**: macOS、Linux、Windows
- **Python**: 3.8 或更高版本
- **网络**: 能够访问百度智能云 API（国内用户可直接访问）

### 硬件建议

- **内存**: 建议 4GB 以上（EasyOCR 首次运行需要加载模型）
- **存储**: 预留 500MB 以上空间（EasyOCR 模型约 100MB）
- **GPU**（可选）: NVIDIA GPU + CUDA 可加速 EasyOCR 识别

## 安装步骤

### 第 1 步：安装 Python 依赖

```bash
pip3 install requests easyocr Pillow
```

或使用 requirements.txt：

```bash
pip3 install -r requirements.txt
```

#### 各依赖说明

| 依赖 | 版本 | 说明 |
|------|------|------|
| `requests` | >=2.28.0 | HTTP 请求库，用于调用百度 OCR API |
| `easyocr` | >=1.7.0 | 本地 OCR 引擎，作为百度 OCR 的兜底方案 |
| `Pillow` | >=9.0.0 | 图片处理库，用于图片预处理和格式转换 |

#### GPU 加速（可选）

如果你有 NVIDIA 显卡，可以安装 GPU 版本的 EasyOCR：

```bash
pip3 install easyocr[gpu]
```

或者先安装 CUDA 工具包，再安装 easyocr：

```bash
# Ubuntu/Debian
sudo apt-get install nvidia-cuda-toolkit

# 安装 easyocr
pip3 install easyocr
```

### 第 2 步：获取百度 OCR API 密钥

1. 访问 [百度智能云控制台](https://console.bce.baidu.com/)
2. 登录百度账号（如没有需要注册）
3. 搜索 "文字识别" 或点击 "人工智能" → "文字识别"
4. 点击 "创建应用"
5. 填写应用信息：
   - 应用名称：任意名称，如 `my-ocr-app`
   - 应用类型：选择 "前端操作" 或 "后端服务"
   - 文字识别服务：勾选你需要的服务（可全选）
6. 点击 "立即创建"
7. 在 "我的应用" 页面获取 `API Key` 和 `Secret Key`

### 第 3 步：配置 API 密钥

选择以下方式之一配置 API 密钥：

#### 方式 A：交互式配置（推荐新手）

```bash
python3 scripts/ocr.py --configure
```

按照提示输入 API Key 和 Secret Key。

#### 方式 B：环境变量

```bash
export BAIDU_OCR_API_KEY="<your_api_key>"
export BAIDU_OCR_SECRET_KEY="<your_secret_key>"
```

建议将以上内容添加到 `~/.bashrc` 或 `~/.zshrc`：

```bash
echo 'export BAIDU_OCR_API_KEY="<your_api_key>"' >> ~/.bashrc
echo 'export BAIDU_OCR_SECRET_KEY="<your_secret_key>"' >> ~/.bashrc
source ~/.bashrc
```

#### 方式 C：配置文件

```bash
mkdir -p ~/.openclaw/skills/BaiduOCR-LocalFallback
```

创建 `~/.openclaw/skills/BaiduOCR-LocalFallback/config.json`：

```json
{
  "api_key": "<your_api_key>",
  "secret_key": "<your_secret_key>"
}
```

### 第 4 步：验证安装

运行测试命令验证安装是否成功：

```bash
python3 scripts/ocr.py --test-connection
```

成功输出示例：

```
测试API连接...
✓ API连接成功!
  access_token: <your_access_token>
```

## 安装验证测试

创建一个测试脚本 `test_installation.py`：

```python
#!/usr/bin/env python3
"""安装验证测试"""

from scripts.ocr import OCR
from scripts.baidu_client import BaiduOCRError

def test_basic_recognition():
    """测试基本识别功能"""
    print("测试 1: 基本文字识别...")
    try:
        ocr = OCR()
        # 使用内置测试图片或你自己的图片
        result = ocr.recognize(
            image="test.jpg",  # 替换为你的测试图片路径
            api="general_basic"
        )
        if "words_result" in result:
            print(f"✓ 识别成功: {result['words_result_num']} 个文字区域")
            return True
        else:
            print(f"✗ 识别失败: {result}")
            return False
    except FileNotFoundError:
        print("⚠ 请准备测试图片 test.jpg")
        return False
    except Exception as e:
        print(f"✗ 错误: {e}")
        return False

def test_config():
    """测试配置读取"""
    print("\n测试 2: 配置读取...")
    from scripts.config import Config
    config = Config()
    if config.api_key and config.secret_key:
        print(f"✓ 配置正确: API Key = {config.api_key[:10]}...")
        return True
    else:
        print("✗ 配置不完整，请检查环境变量或配置文件")
        return False

def test_easyocr():
    """测试 EasyOCR（可选）"""
    print("\n测试 3: EasyOCR 本地识别...")
    try:
        from scripts.local_ocr import local_ocr
        local_ocr._init_reader()
        print("✓ EasyOCR 可用")
        return True
    except Exception as e:
        print(f"⚠ EasyOCR 不可用: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("百度 OCR 技能安装验证")
    print("=" * 50)
    
    results = []
    results.append(test_config())
    results.append(test_basic_recognition())
    results.append(test_easyocr())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✓ 所有测试通过！")
    else:
        print("⚠ 部分测试失败，请检查上述错误信息")
    print("=" * 50)
```

运行测试：

```bash
python3 test_installation.py
```

## 卸载

如需卸载：

```bash
pip3 uninstall requests easyocr Pillow
rm -rf ~/.openclaw/skills/BaiduOCR-LocalFallback
```

## 常见安装问题

### 问题 1：pip 安装超时

```
Socket timeout error
```

**解决方案**：使用国内镜像源

```bash
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple requests easyocr Pillow
```

或配置永久镜像：

```bash
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 2：EasyOCR 模型下载失败

```
Downloading EasyOCR model...
ConnectionError: HTTPSConnectionPool
```

**解决方案**：
1. 检查网络连接
2. 使用代理：
```bash
export HTTPS_PROXY="http://proxy.example.com:8080"
python3 -c "import easyocr; easyocr.Reader(['ch_sim', 'en'])"
```

### 问题 3：easyocr 安装报错

```
ERROR: Could not build wheels for opencv-python
```

**解决方案**：
1. 安装编译依赖：
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev python3-pip python3-venv
sudo apt-get install libgl1-mesa-glx libglib2.0-0

# macOS
brew install opencv
```

2. 使用预编译版本：
```bash
pip3 install opencv-python-headless
pip3 install easyocr
```

### 问题 4：ModuleNotFoundError

```
ModuleNotFoundError: No module named 'requests'
```

**解决方案**：确保已安装所有依赖：

```bash
pip3 install -r requirements.txt
```

### 问题 5：CUDA/GPU 相关问题

如果你想使用 GPU 加速：

1. 确认 NVIDIA 驱动已安装：
```bash
nvidia-smi
```

2. 确认 CUDA 版本：
```bash
nvcc --version
```

3. 安装对应版本的 PyTorch：
```bash
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## Docker 环境安装

如需在 Docker 中使用：

```dockerfile
FROM python:3.10

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# 复制代码
COPY . /app
WORKDIR /app

# 配置环境变量
ENV BAIDU_OCR_API_KEY=<your_api_key>
ENV BAIDU_OCR_SECRET_KEY=<your_secret_key>

CMD ["python3", "scripts/ocr.py", "--test-connection"]
```

构建和运行：

```bash
docker build -t BaiduOCR-LocalFallback .
docker run -e BAIDU_OCR_API_KEY=xxx -e BAIDU_OCR_SECRET_KEY=xxx BaiduOCR-LocalFallback
```

## 下一步

- 📖 查看 [API 参考文档](./api_reference.md)
- 🔧 查看 [故障排除指南](./troubleshooting.md)
- 💡 查看 [使用示例](../examples/)
