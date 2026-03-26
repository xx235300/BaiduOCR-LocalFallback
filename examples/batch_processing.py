#!/usr/bin/env python3
"""
百度OCR - 批量处理示例

本示例展示如何批量处理多张图片，支持文件夹扫描和并发处理。
"""

import os
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional

from scripts.ocr import OCR
from scripts.baidu_client import BaiduOCRError


def process_single_image(
    image_path: str,
    api: str = "general_basic",
    use_fallback: bool = True
) -> Dict[str, Any]:
    """
    处理单张图片
    
    Args:
        image_path: 图片路径
        api: 使用的 API
        use_fallback: 是否使用本地兜底
    
    Returns:
        处理结果字典
    """
    result = {
        "image": image_path,
        "success": False,
        "words_result_num": 0,
        "words": [],
        "error": None,
        "fallback_used": False,
        "time_ms": 0
    }
    
    ocr = OCR(use_fallback=use_fallback)
    
    start_time = time.time()
    
    try:
        response = ocr.recognize(image=image_path, api=api)
        
        result["success"] = True
        result["words_result_num"] = response.get("words_result_num", 0)
        
        # 提取识别的文字
        for item in response.get("words_result", []):
            if item.get("words"):
                result["words"].append(item["words"])
        
        # 检查是否使用了兜底
        if "fallback_info" in response:
            result["fallback_used"] = True
        
    except BaiduOCRError as e:
        result["error"] = f"BaiduOCR错误: {e.error_code} - {e.error_msg}"
    except Exception as e:
        result["error"] = str(e)
    finally:
        result["time_ms"] = int((time.time() - start_time) * 1000)
    
    return result


def batch_process(
    image_paths: List[str],
    api: str = "general_basic",
    max_workers: int = 4,
    use_fallback: bool = True,
    show_progress: bool = True
) -> List[Dict[str, Any]]:
    """
    批量处理图片（并发）
    
    Args:
        image_paths: 图片路径列表
        api: 使用的 API
        max_workers: 最大并发数
        use_fallback: 是否使用本地兜底
        show_progress: 是否显示进度
    
    Returns:
        处理结果列表
    """
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_path = {
            executor.submit(
                process_single_image,
                path,
                api,
                use_fallback
            ): path
            for path in image_paths
        }
        
        # 收集结果
        completed = 0
        total = len(image_paths)
        
        for future in as_completed(future_to_path):
            completed += 1
            path = future_to_path[future]
            
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append({
                    "image": path,
                    "success": False,
                    "error": str(e)
                })
            
            if show_progress:
                print(f"进度: {completed}/{total} ({100*completed//total}%) - {path}")
    
    return results


def process_folder(
    folder_path: str,
    api: str = "general_basic",
    extensions: List[str] = None,
    recursive: bool = False,
    max_workers: int = 4,
    output_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    处理文件夹中的所有图片
    
    Args:
        folder_path: 文件夹路径
        api: 使用的 API
        extensions: 要处理的文件扩展名
        recursive: 是否递归子文件夹
        max_workers: 最大并发数
        output_file: 结果输出文件路径
    
    Returns:
        汇总结果
    """
    if extensions is None:
        extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
    
    # 扫描图片文件
    folder = Path(folder_path)
    image_paths = []
    
    if recursive:
        for ext in extensions:
            image_paths.extend(folder.rglob(f"*{ext}"))
            image_paths.extend(folder.rglob(f"*{ext.upper()}"))
    else:
        for ext in extensions:
            image_paths.extend(folder.glob(f"*{ext}"))
            image_paths.extend(folder.glob(f"*{ext.upper()}"))
    
    image_paths = [str(p) for p in image_paths]
    
    print(f"找到 {len(image_paths)} 张图片")
    
    if not image_paths:
        return {"error": "没有找到图片文件"}
    
    # 批量处理
    print(f"开始处理，使用 {max_workers} 个并发线程...")
    start_time = time.time()
    
    results = batch_process(
        image_paths,
        api=api,
        max_workers=max_workers,
        show_progress=True
    )
    
    total_time = time.time() - start_time
    
    # 统计
    success_count = sum(1 for r in results if r["success"])
    fallback_count = sum(1 for r in results if r.get("fallback_used", False))
    total_words = sum(r["words_result_num"] for r in results)
    
    summary = {
        "total": len(results),
        "success": success_count,
        "failed": len(results) - success_count,
        "fallback_used": fallback_count,
        "total_words": total_words,
        "total_time_s": round(total_time, 2),
        "avg_time_ms": round(sum(r["time_ms"] for r in results) / len(results)),
        "results": results
    }
    
    # 输出到文件
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"\n结果已保存到: {output_file}")
    
    return summary


def main():
    print("=" * 60)
    print("百度 OCR 批量处理示例")
    print("=" * 60)
    
    # 示例 1: 处理指定图片列表
    print("\n【示例 1】处理指定图片列表")
    print("-" * 40)
    
    image_list = [
        "examples/test_images/photo1.jpg",
        "examples/test_images/photo2.jpg",
        "examples/test_images/idcard.jpg",
        "examples/test_images/receipt.jpg",
    ]
    
    # 过滤存在的文件
    existing_images = [img for img in image_list if os.path.exists(img)]
    
    if existing_images:
        results = batch_process(
            existing_images,
            api="general_basic",
            max_workers=2,
            show_progress=True
        )
        
        print("\n处理结果:")
        for result in results:
            status = "✓" if result["success"] else "✗"
            fallback = " [本地兜底]" if result.get("fallback_used") else ""
            print(f"  {status} {result['image']}")
            print(f"     识别: {result['words_result_num']} 个文字区域, "
                  f"耗时: {result['time_ms']}ms{fallback}")
            if result["error"]:
                print(f"     错误: {result['error']}")
    else:
        print("  (请准备测试图片)")
    
    # 示例 2: 处理文件夹
    print("\n【示例 2】处理文件夹")
    print("-" * 40)
    
    # 替换为你的图片文件夹
    folder_path = "examples/test_images"
    
    if os.path.exists(folder_path):
        summary = process_folder(
            folder_path,
            api="general_basic",
            max_workers=2,
            output_file="batch_results.json"
        )
        
        print("\n汇总统计:")
        print(f"  总数: {summary['total']}")
        print(f"  成功: {summary['success']}")
        print(f"  失败: {summary['failed']}")
        print(f"  使用兜底: {summary['fallback_used']}")
        print(f"  识别总字数: {summary['total_words']}")
        print(f"  总耗时: {summary['total_time_s']}s")
        print(f"  平均耗时: {summary['avg_time_ms']}ms/张")
    else:
        print(f"  文件夹不存在: {folder_path}")
        print("  (请创建 examples/test_images 文件夹并放入图片)")
    
    # 示例 3: 导出为文本
    print("\n【示例 3】导出识别结果为文本")
    print("-" * 40)
    
    if existing_images:
        output_lines = []
        
        for result in results:
            if result["success"]:
                output_lines.append(f"=== {result['image']} ===")
                for word in result["words"]:
                    output_lines.append(word)
                output_lines.append("")
        
        if output_lines:
            output_file = "ocr_results.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(output_lines))
            print(f"  结果已导出到: {output_file}")
    
    print("\n" + "=" * 60)
    print("批量处理示例结束")
    print("=" * 60)


if __name__ == "__main__":
    main()
