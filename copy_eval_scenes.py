#!/usr/bin/env python3
"""
复制 eval_list.txt 中列出的场景文件夹到新的输出目录。

从 ScanNet 的 raw/scans 目录复制整个场景文件夹（包含 .sens 文件和其他相关文件）
到指定的输出目录，保持原有的目录结构。
"""

import argparse
import os
import shutil
from pathlib import Path
from typing import List


def load_eval_list(eval_list_file: Path) -> List[str]:
    """从 eval_list.txt 文件加载场景名称列表"""
    scene_names = []
    
    if not eval_list_file.exists():
        print(f"错误：找不到文件 {eval_list_file}")
        return scene_names
    
    try:
        with eval_list_file.open('r', encoding='utf-8') as f:
            for line in f:
                scene_name = line.strip()
                if scene_name:  # 跳过空行
                    scene_names.append(scene_name)
        
        print(f"从 {eval_list_file} 加载了 {len(scene_names)} 个场景")
        return scene_names
    except Exception as e:
        print(f"读取 eval_list 文件时出错：{str(e)}")
        return []


def copy_scene(scene_name: str, source_dir: Path, target_dir: Path) -> bool:
    """复制单个场景文件夹"""
    source_scene_dir = source_dir / scene_name
    target_scene_dir = target_dir / scene_name
    
    if not source_scene_dir.exists():
        print(f"✗ {scene_name}: 源目录不存在 {source_scene_dir}")
        return False
    
    if not source_scene_dir.is_dir():
        print(f"✗ {scene_name}: 源路径不是目录 {source_scene_dir}")
        return False
    
    try:
        # 创建目标目录的父目录
        target_scene_dir.parent.mkdir(parents=True, exist_ok=True)
        
        # 如果目标目录已存在，先删除
        if target_scene_dir.exists():
            shutil.rmtree(target_scene_dir)
        
        # 复制整个场景目录
        shutil.copytree(source_scene_dir, target_scene_dir)
        
        # 验证 .sens 文件是否存在
        sens_file = target_scene_dir / f"{scene_name}.sens"
        if sens_file.exists():
            print(f"✓ {scene_name}: 复制成功，包含 .sens 文件")
            return True
        else:
            print(f"⚠ {scene_name}: 复制成功，但缺少 .sens 文件")
            return True
            
    except Exception as e:
        print(f"✗ {scene_name}: 复制失败 - {str(e)}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="复制 eval_list.txt 中的场景文件夹到输出目录"
    )
    parser.add_argument(
        "--dataset_root",
        type=Path,
        required=True,
        help="ScanNet 数据集根目录（包含 raw/scans）"
    )
    parser.add_argument(
        "--scans_subdir",
        type=str,
        default="raw/scans",
        help="相对 dataset_root 的 scans 目录，默认 raw/scans"
    )
    parser.add_argument(
        "--eval_list",
        type=Path,
        default=Path("eval_list.txt"),
        help="eval_list.txt 文件路径，默认 eval_list.txt"
    )
    parser.add_argument(
        "--output_dir",
        type=Path,
        required=True,
        help="输出目录路径"
    )
    parser.add_argument(
        "--verify_sens",
        action="store_true",
        help="只复制包含 .sens 文件的场景"
    )
    
    args = parser.parse_args()
    
    # 验证输入路径
    scans_dir = args.dataset_root / args.scans_subdir
    if not scans_dir.exists() or not scans_dir.is_dir():
        print(f"错误：找不到 scans 目录：{scans_dir}")
        return 1
    
    # 加载场景列表
    scene_names = load_eval_list(args.eval_list)
    if not scene_names:
        print("没有找到任何场景，请检查 eval_list.txt 文件")
        return 1
    
    # 创建输出目录
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"开始复制场景...")
    print(f"源目录：{scans_dir}")
    print(f"目标目录：{args.output_dir}")
    print(f"场景数量：{len(scene_names)}")
    if args.verify_sens:
        print("已启用 .sens 文件验证")
    print("-" * 50)
    
    # 复制场景
    success_count = 0
    failed_scenes = []
    
    for i, scene_name in enumerate(scene_names, 1):
        print(f"[{i}/{len(scene_names)}] 处理 {scene_name}...")
        
        # 如果启用了验证，先检查源目录是否有 .sens 文件
        if args.verify_sens:
            source_sens_file = scans_dir / scene_name / f"{scene_name}.sens"
            if not source_sens_file.exists():
                print(f"✗ {scene_name}: 源目录缺少 .sens 文件，跳过")
                failed_scenes.append(scene_name)
                continue
        
        # 复制场景
        if copy_scene(scene_name, scans_dir, args.output_dir):
            success_count += 1
        else:
            failed_scenes.append(scene_name)
    
    # 输出结果统计
    print("-" * 50)
    print(f"复制完成！")
    print(f"成功复制：{success_count} 个场景")
    print(f"失败/跳过：{len(failed_scenes)} 个场景")
    
    if failed_scenes:
        print(f"失败的场景：{', '.join(failed_scenes)}")
    
    print(f"输出目录：{args.output_dir}")
    
    return 0 if len(failed_scenes) == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
