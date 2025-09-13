#!/usr/bin/env python3
"""
Randomly sample 50 scenes from ScanNet dataset and output to eval_list
"""

import re
import random
import os
import glob

def extract_scene_names_from_structure(structure_file, data_source='all'):
    """
    Extract scene names from the structure.txt file
    
    Args:
        structure_file: Path to structure.txt file
        data_source: 'raw', 'processed', or 'all' - which data source to sample from
    """
    scene_names = []
    
    with open(structure_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Match lines that contain scene directories
            # The line format is: │   │   ├── scene0000_00
            if '├── scene' in line:
                # Extract the scene name from the line
                match = re.search(r'scene(\d+_\d+)', line)
                if match:
                    scene_name = 'scene' + match.group(1)
                    
                    # Filter by data source if specified
                    if data_source == 'all':
                        scene_names.append(scene_name)
                    elif data_source == 'raw' and 'raw' in line:
                        scene_names.append(scene_name)
                    elif data_source == 'processed' and 'raw' not in line:
                        scene_names.append(scene_name)
    
    return scene_names

def scan_scenes_from_filesystem(dataset_root, data_source='all', verify_sens=True):
    """
    Scan for scenes directly from the file system
    
    Args:
        dataset_root: Root directory of the ScanNet dataset
        data_source: 'raw', 'processed', or 'all' - which data source to scan
        verify_sens: If True, verify that .sens file exists for each scene
    """
    scene_names = []
    
    if data_source in ['all', 'raw']:
        # Scan raw/scans directory
        raw_scans_dir = os.path.join(dataset_root, 'raw', 'scans')
        if os.path.exists(raw_scans_dir):
            for item in os.listdir(raw_scans_dir):
                if os.path.isdir(os.path.join(raw_scans_dir, item)) and item.startswith('scene'):
                    # Verify .sens file exists if requested
                    if verify_sens:
                        sens_file = os.path.join(raw_scans_dir, item, f"{item}.sens")
                        if os.path.exists(sens_file):
                            scene_names.append(item)
                        else:
                            print(f"Warning: .sens file not found for {item}, skipping...")
                    else:
                        scene_names.append(item)
    
    if data_source in ['all', 'processed']:
        # Scan for other processed data directories
        # Look for directories that might contain processed scene data
        for root, dirs, files in os.walk(dataset_root):
            # Skip raw directory if we're looking for processed data
            if data_source == 'processed' and 'raw' in root:
                continue
            
            for dir_name in dirs:
                if dir_name.startswith('scene') and dir_name not in scene_names:
                    scene_names.append(dir_name)
    
    return sorted(list(set(scene_names)))  # Remove duplicates and sort

def verify_scenes_exist(scene_names, dataset_root):
    """
    Verify that .sens files exist for the given scenes
    
    Args:
        scene_names: List of scene names to verify
        dataset_root: Root directory of the ScanNet dataset
    
    Returns:
        List of scene names that have valid .sens files
    """
    valid_scenes = []
    raw_scans_dir = os.path.join(dataset_root, 'raw', 'scans')
    
    for scene_name in scene_names:
        sens_file = os.path.join(raw_scans_dir, scene_name, f"{scene_name}.sens")
        if os.path.exists(sens_file):
            valid_scenes.append(scene_name)
        else:
            print(f"Warning: .sens file not found for {scene_name}, skipping...")
    
    return valid_scenes

def random_sample_scenes(scene_names, num_samples=50):
    """
    Randomly sample specified number of scenes
    """
    if len(scene_names) < num_samples:
        print(f"Warning: Only {len(scene_names)} scenes available, sampling all of them")
        return scene_names
    
    return random.sample(scene_names, num_samples)

def save_to_eval_list(sampled_scenes, output_file='eval_list.txt'):
    """
    Save sampled scene names to eval_list file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for scene in sampled_scenes:
            f.write(f"{scene}\n")
    
    print(f"Successfully saved {len(sampled_scenes)} scenes to {output_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Randomly sample scenes from ScanNet dataset')
    parser.add_argument('--dataset_root', default='.',
                       help='Root directory of the ScanNet dataset (default: current directory)')
    parser.add_argument('--structure_file', default='structure.txt',
                       help='Path to structure.txt file (default: structure.txt)')
    parser.add_argument('--data_source', choices=['raw', 'processed', 'all'], default='all',
                       help='Data source to sample from: raw, processed, or all (default: all)')
    parser.add_argument('--num_samples', type=int, default=50,
                       help='Number of scenes to sample (default: 50)')
    parser.add_argument('--use_filesystem', action='store_true',
                       help='Scan filesystem directly instead of using structure.txt')
    parser.add_argument('--output_file', default='eval_list.txt',
                       help='Output file name (default: eval_list.txt)')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed for reproducibility (default: 42)')
    parser.add_argument('--verify_sens', action='store_true',
                       help='Verify that .sens files exist for sampled scenes')
    
    args = parser.parse_args()
    
    # Set random seed for reproducibility
    random.seed(args.seed)
    
    print(f"Sampling {args.num_samples} scenes from {args.data_source} data source")
    
    if args.use_filesystem:
        print(f"Scanning filesystem in {args.dataset_root}...")
        scene_names = scan_scenes_from_filesystem(args.dataset_root, args.data_source)
    else:
        if not os.path.exists(args.structure_file):
            print(f"Error: {args.structure_file} not found!")
            print("Use --use_filesystem to scan the filesystem directly")
            return
        
        print(f"Extracting scene names from {args.structure_file}...")
        scene_names = extract_scene_names_from_structure(args.structure_file, args.data_source)
    
    print(f"Found {len(scene_names)} total scenes")
    
    if len(scene_names) == 0:
        print("No scenes found! Please check your dataset path and data source.")
        return
    
    # Verify scenes exist if requested
    if args.verify_sens:
        print("Verifying that .sens files exist for all scenes...")
        scene_names = verify_scenes_exist(scene_names, args.dataset_root)
        print(f"Found {len(scene_names)} scenes with valid .sens files")
        
        if len(scene_names) == 0:
            print("No valid scenes found! Please check your dataset.")
            return
    
    print(f"Randomly sampling {args.num_samples} scenes...")
    sampled_scenes = random_sample_scenes(scene_names, args.num_samples)
    
    print("Sampled scenes:")
    for i, scene in enumerate(sampled_scenes, 1):
        print(f"{i:2d}. {scene}")
    
    print(f"\nSaving to {args.output_file}...")
    save_to_eval_list(sampled_scenes, args.output_file)
    
    print("\nDone!")

if __name__ == "__main__":
    main()
