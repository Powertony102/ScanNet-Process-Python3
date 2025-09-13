#!/usr/bin/env python3
"""
按照 FastVGGT 的方法等间隔抽取场景，生成 eval_list.txt。

规则：
- 从数据目录中读取所有场景文件夹名并排序
- 若总数大于目标数量 N，则按间隔 floor(len(all)/N) 等间隔采样，再截断为 N 个
- 否则返回全部场景

默认从 ScanNet 的 `raw/scans` 目录读取场景名，可选验证 `.sens` 是否存在。
"""

import argparse
from pathlib import Path
from typing import List


def get_all_scenes(data_dir: Path, num_scenes: int) -> List[str]:
    all_scenes = sorted([d.name for d in data_dir.iterdir() if d.is_dir()])
    if len(all_scenes) > num_scenes:
        sample_interval = max(1, len(all_scenes) // num_scenes)
        return all_scenes[::sample_interval][:num_scenes]
    return all_scenes


def filter_scenes_with_sens(scans_dir: Path, scene_names: List[str]) -> List[str]:
    """只保留存在对应 .sens 文件的场景。"""
    valid: List[str] = []
    for name in scene_names:
        sens_path = scans_dir / name / f"{name}.sens"
        if sens_path.exists():
            valid.append(name)
    return valid


def save_eval_list(scene_names: List[str], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as f:
        for s in scene_names:
            f.write(f"{s}\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="按 FastVGGT 规则等间隔抽取场景并生成 eval_list.txt"
    )
    parser.add_argument(
        "--dataset_root",
        type=Path,
        default=Path("."),
        help="ScanNet 数据集根目录（包含 raw/scans）",
    )
    parser.add_argument(
        "--scans_subdir",
        type=str,
        default="raw/scans",
        help="相对 dataset_root 的 scans 目录，默认 raw/scans",
    )
    parser.add_argument(
        "--num_scenes",
        type=int,
        default=50,
        help="需要抽取的场景数量，默认 50",
    )
    parser.add_argument(
        "--output_file",
        type=Path,
        default=Path("eval_list.txt"),
        help="输出的 eval_list 文件路径，默认 eval_list.txt",
    )
    parser.add_argument(
        "--verify_sens",
        action="store_true",
        help="只保留存在 .sens 文件的场景",
    )

    args = parser.parse_args()

    scans_dir = args.dataset_root / args.scans_subdir
    if not scans_dir.exists() or not scans_dir.is_dir():
        print(f"错误：找不到 scans 目录：{scans_dir}")
        return 1

    scenes = get_all_scenes(scans_dir, args.num_scenes)
    if args.verify_sens:
        scenes = filter_scenes_with_sens(scans_dir, scenes)

    if not scenes:
        print("未找到任何场景，检查数据路径或参数。")
        return 1

    save_eval_list(scenes, args.output_file)

    print("生成完成：")
    print(f"scans 目录：{scans_dir}")
    print(f"目标数量：{args.num_scenes}")
    print(f"实际写入：{len(scenes)} 个场景 -> {args.output_file}")
    if args.verify_sens:
        print("已启用 .sens 校验，仅保留存在 .sens 的场景。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


