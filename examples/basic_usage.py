#!/usr/bin/env python3
"""
百度OCR - 基础使用示例

本示例展示最常用的 OCR 功能，适合入门学习。
"""

from scripts.ocr import OCR


def main():
    print("=" * 60)
    print("百度 OCR 基础使用示例")
    print("=" * 60)

    # 初始化 OCR 识别器
    ocr = OCR()

    # ========================================
    # 示例 1: 通用文字识别
    # ========================================
    print("\n【示例 1】通用文字识别")
    print("-" * 40)

    try:
        result = ocr.recognize(
            image="examples/test_images/photo.jpg",
            api="general_basic"
        )
        
        print(f"识别到 {result['words_result_num']} 个文字区域：")
        for item in result["words_result"]:
            print(f"  - {item['words']}")
            
    except FileNotFoundError:
        print("  (请准备测试图片，或修改代码中的图片路径)")
    except Exception as e:
        print(f"  错误: {e}")

    # ========================================
    # 示例 2: 网络图片识别
    # ========================================
    print("\n【示例 2】网络图片识别")
    print("-" * 40)

    try:
        result = ocr.recognize(
            image_url="https://raw.githubusercontent.com/xx235300/BaiduOCR-LocalFallback/main/examples/test_images/demo.jpg",
            api="webimage"
        )
        
        print(f"识别结果:")
        for item in result["words_result"]:
            print(f"  - {item['words']}")
            
    except Exception as e:
        print(f"  错误: {e}")

    # ========================================
    # 示例 3: 身份证识别
    # ========================================
    print("\n【示例 3】身份证识别（正面）")
    print("-" * 40)

    try:
        result = ocr.recognize(
            image="examples/test_images/idcard_front.jpg",
            api="idcard",
            id_card_side="front"
        )
        
        # 打印所有识别字段
        print("身份证信息:")
        for item in result["words_result"]:
            if item.get("words"):  # 跳过空字段
                print(f"  - {item['words']}")
                
    except FileNotFoundError:
        print("  (请准备身份证图片 examples/test_images/idcard_front.jpg)")
    except Exception as e:
        print(f"  错误: {e}")

    # ========================================
    # 示例 4: 银行卡识别
    # ========================================
    print("\n【示例 4】银行卡识别")
    print("-" * 40)

    try:
        result = ocr.recognize(
            image="examples/test_images/bankcard.jpg",
            api="bankcard"
        )
        
        if "result" in result:
            bank_info = result["result"]
            print(f"银行名称: {bank_info.get('bank_name', 'N/A')}")
            print(f"银行卡号: {bank_info.get('bank_card_number', 'N/A')}")
            
    except FileNotFoundError:
        print("  (请准备银行卡图片 examples/test_images/bankcard.jpg)")
    except Exception as e:
        print(f"  错误: {e}")

    # ========================================
    # 示例 5: 票据识别
    # ========================================
    print("\n【示例 5】增值税发票识别")
    print("-" * 40)

    try:
        result = ocr.recognize(
            image="examples/test_images/invoice.jpg",
            api="vat_invoice"
        )
        
        print("发票信息:")
        for item in result.get("words_result", []):
            print(f"  - {item.get('words', '')}")
            
    except FileNotFoundError:
        print("  (请准备发票图片 examples/test_images/invoice.jpg)")
    except Exception as e:
        print(f"  错误: {e}")

    # ========================================
    # 示例 6: 手写文字识别（本地兜底）
    # ========================================
    print("\n【示例 6】手写文字识别（本地 EasyOCR）")
    print("-" * 40)

    try:
        result = ocr.recognize(
            image="examples/test_images/handwriting.jpg",
            api="handwriting"
        )
        
        # 检查是否使用了本地兜底
        if "fallback_info" in result:
            print(f"  (使用本地兜底: {result['fallback_info']['engine']})")
        
        print("手写内容:")
        for item in result["words_result"]:
            print(f"  - {item['words']}")
            
    except FileNotFoundError:
        print("  (请准备手写图片 examples/test_images/handwriting.jpg)")
    except Exception as e:
        print(f"  错误: {e}")

    # ========================================
    # 示例 7: 表格识别
    # ========================================
    print("\n【示例 7】表格识别")
    print("-" * 40)

    try:
        result = ocr.recognize(
            image="examples/test_images/table.jpg",
            api="table",
            request_type="excel"
        )
        
        print("表格识别结果:")
        if "result" in result:
            print(f"  内容: {result['result']}")
            
    except FileNotFoundError:
        print("  (请准备表格图片 examples/test_images/table.jpg)")
    except Exception as e:
        print(f"  错误: {e}")

    print("\n" + "=" * 60)
    print("示例结束")
    print("=" * 60)


if __name__ == "__main__":
    main()
