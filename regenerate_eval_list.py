#!/usr/bin/env python3
"""
Regenerate eval_list.txt with only valid scenes that have .sens files
"""

import os
import sys

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
    
    print(f"Verifying scenes in {raw_scans_dir}...")
    
    for scene_name in scene_names:
        sens_file = os.path.join(raw_scans_dir, scene_name, f"{scene_name}.sens")
        if os.path.exists(sens_file):
            valid_scenes.append(scene_name)
            print(f"✓ {scene_name}")
        else:
            print(f"✗ {scene_name} (missing .sens file)")
    
    return valid_scenes

def load_eval_list(eval_list_file):
    """Load scene names from eval_list.txt file"""
    scene_names = []
    
    if not os.path.exists(eval_list_file):
        print(f"Error: {eval_list_file} not found!")
        return scene_names
    
    try:
        with open(eval_list_file, 'r', encoding='utf-8') as f:
            for line in f:
                scene_name = line.strip()
                if scene_name:  # Skip empty lines
                    scene_names.append(scene_name)
        
        print(f"Loaded {len(scene_names)} scenes from {eval_list_file}")
        return scene_names
    except Exception as e:
        print(f"Error reading eval list file: {str(e)}")
        return []

def save_to_eval_list(scene_names, output_file='eval_list.txt'):
    """Save scene names to eval_list file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        for scene in scene_names:
            f.write(f"{scene}\n")
    
    print(f"Successfully saved {len(scene_names)} scenes to {output_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Regenerate eval_list.txt with only valid scenes')
    parser.add_argument('--dataset_root', default='.',
                       help='Root directory of the ScanNet dataset (default: current directory)')
    parser.add_argument('--eval_list', default='eval_list.txt',
                       help='Input eval_list.txt file (default: eval_list.txt)')
    parser.add_argument('--output_file', default='eval_list_valid.txt',
                       help='Output file name (default: eval_list_valid.txt)')
    
    args = parser.parse_args()
    
    print(f"Regenerating eval list with valid scenes...")
    print(f"Dataset root: {args.dataset_root}")
    print(f"Input eval list: {args.eval_list}")
    print(f"Output file: {args.output_file}")
    
    # Load current eval list
    scene_names = load_eval_list(args.eval_list)
    
    if not scene_names:
        print("No scenes found in eval list!")
        return 1
    
    # Verify scenes exist
    valid_scenes = verify_scenes_exist(scene_names, args.dataset_root)
    
    print(f"\nSummary:")
    print(f"Total scenes in eval list: {len(scene_names)}")
    print(f"Valid scenes with .sens files: {len(valid_scenes)}")
    print(f"Missing scenes: {len(scene_names) - len(valid_scenes)}")
    
    if valid_scenes:
        # Save valid scenes
        save_to_eval_list(valid_scenes, args.output_file)
        print(f"\nValid scenes saved to {args.output_file}")
        print("You can now use this file with batch_process.py")
    else:
        print("\nNo valid scenes found!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
