#!/usr/bin/env python3
"""
百度OCR - 配置示例

展示不同的配置方式和使用场景。
"""

import os
import json
from pathlib import Path

from scripts.ocr import OCR
from scripts.config import Config, interactive_configure


def example_environment_variables():
    """示例：使用环境变量配置"""
    print("\n【示例 1】环境变量配置")
    print("-" * 40)
    
    # 设置环境变量
    os.environ["BAIDU_OCR_API_KEY"] = "<your_api_key>"
    os.environ["BAIDU_OCR_SECRET_KEY"] = "<your_secret_key>"
    
    # 初始化 OCR（会自动读取环境变量）
    ocr = OCR()
    
    # 验证配置
    config = Config()
    print(f"API Key: {config.api_key[:10]}..." if config.api_key else "未设置")
    print(f"Secret Key: {config.secret_key[:10]}..." if config.secret_key else "未设置")
    
    # 清理环境变量
    # del os.environ["BAIDU_OCR_API_KEY"]
    # del os.environ["BAIDU_OCR_SECRET_KEY"]


def example_config_file():
    """示例：使用配置文件"""
    print("\n【示例 2】配置文件方式")
    print("-" * 40)
    
    config = Config()
    
    # 检查配置文件路径
    config_file = Path("~/.openclaw/skills/BaiduOCR-LocalFallback/config.json").expanduser()
    
    if config_file.exists():
        print(f"配置文件位置: {config_file}")
        
        with open(config_file, "r") as f:
            data = json.load(f)
            print(f"API Key: {data.get('api_key', 'N/A')[:10]}...")
            print(f"Secret Key: {data.get('secret_key', 'N/A')[:10]}...")
    else:
        print(f"配置文件不存在: {config_file}")
        print("请运行: python3 scripts/ocr.py --configure")


def example_interactive_config():
    """示例：交互式配置"""
    print("\n【示例 3】交互式配置")
    print("-" * 40)
    
    # 注意：交互式配置会阻塞等待用户输入
    # 取消注释以启用
    # print("启动交互式配置向导...")
    # if interactive_configure():
    #     print("配置完成！")
    # else:
    #     print("配置已取消")
    
    print("（交互式配置已禁用，如需启用请取消代码注释）")


def example_custom_config():
    """示例：代码中直接指定配置"""
    print("\n【示例 4】代码中直接指定配置")
    print("-" * 40)
    
    # 直接在代码中指定 API Key
    api_key = "<your_api_key>"
    secret_key = "<your_secret_key>"
    
    ocr = OCR(api_key=api_key, secret_key=secret_key)
    
    print(f"API Key: {api_key[:10]}...")
    print(f"Secret Key: {secret_key[:10]}...")
    print("配置方式: 代码直接指定")


def example_disable_fallback():
    """示例：禁用本地兜底"""
    print("\n【示例 5】禁用本地兜底")
    print("-" * 40)
    
    # 禁用本地 EasyOCR 兜底
    ocr = OCR(use_fallback=False)
    
    print("本地兜底已禁用")
    print("当百度 OCR 服务不可用时，将直接抛出异常")
    print("而不是切换到本地 EasyOCR")


def example_enable_fallback():
    """示例：启用本地兜底（默认）"""
    print("\n【示例 6】启用本地兜底（默认）")
    print("-" * 40)
    
    # 默认启用本地兜底
    ocr = OCR(use_fallback=True)
    
    print("本地兜底已启用")
    print("当百度 OCR 服务不可用时，会自动切换到本地 EasyOCR")


def example_config_priority():
    """示例：配置优先级说明"""
    print("\n【示例 7】配置优先级说明")
    print("-" * 40)
    
    print("配置加载优先级（从高到低）：")
    print("  1. 代码中直接指定的 api_key/secret_key")
    print("  2. 环境变量 BAIDU_OCR_API_KEY / BAIDU_OCR_SECRET_KEY")
    print("  3. 配置文件 ~/.openclaw/skills/BaiduOCR-LocalFallback/config.json")
    
    print("\n示例：环境变量覆盖配置文件")
    
    # 设置环境变量
    os.environ["BAIDU_OCR_API_KEY"] = "env_api_key"
    os.environ["BAIDU_OCR_SECRET_KEY"] = "env_secret_key"
    
    config = Config()
    print(f"当前 API Key: {config.api_key}")
    print("(来自环境变量)")


def example_advanced_config():
    """示例：高级配置选项"""
    print("\n【示例 8】高级配置")
    print("-" * 40)
    
    # 配置缓存目录
    cache_dir = Path("~/.openclaw/skills/BaiduOCR-LocalFallback/cache").expanduser()
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Token 缓存目录: {cache_dir}")
    print(f"access_token 文件: {cache_dir / 'access_token.txt'}")
    
    # 手动刷新 Token
    from scripts.auth import auth
    print("\n手动刷新 Token...")
    try:
        token = auth.get_access_token(force_refresh=True)
        print(f"新 Token: {token[:20]}...")
    except Exception as e:
        print(f"刷新失败: {e}")


def example_multi_account():
    """示例：多账户切换"""
    print("\n【示例 9】多账户切换")
    print("-" * 40)
    
    # 账户 A
    account_a = OCR(
        api_key="account_a_api_key",
        secret_key="account_a_secret_key"
    )
    
    # 账户 B
    account_b = OCR(
        api_key="account_b_api_key",
        secret_key="account_b_secret_key"
    )
    
    print("已创建两个 OCR 实例，分别使用不同的账户")
    print("account_a:", id(account_a))
    print("account_b:", id(account_b))


def example_test_connection():
    """示例：测试连接"""
    print("\n【示例 10】测试 API 连接")
    print("-" * 40)
    
    from scripts.auth import auth
    
    try:
        token = auth.get_access_token()
        print(f"✓ 连接成功")
        print(f"  Token: {token[:30]}...")
        
        # 检查 token 是否有效
        if auth._is_token_valid(token):
            print("  Token 状态: 有效")
        else:
            print("  Token 状态: 已过期，需要刷新")
            
    except Exception as e:
        print(f"✗ 连接失败: {e}")


def main():
    print("=" * 60)
    print("百度 OCR 配置示例")
    print("=" * 60)
    
    example_environment_variables()
    example_config_file()
    example_interactive_config()
    example_custom_config()
    example_disable_fallback()
    example_enable_fallback()
    example_config_priority()
    example_advanced_config()
    example_multi_account()
    example_test_connection()
    
    print("\n" + "=" * 60)
    print("配置示例结束")
    print("=" * 60)


if __name__ == "__main__":
    main()
